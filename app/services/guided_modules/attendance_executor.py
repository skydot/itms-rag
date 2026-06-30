import os
"""Attendance query executor — runs final parameterized SQL for attendance guided flows.

Uses existing response_mode_service and report_service for output formatting.

Schema notes:
- attendances.punch: '4'=Present, '5'=Absent, '1'=CL, '2'=LAP, '3'=SL
- attendances.course_id = training_calendars.id
- attendances.user_id = users.id
- No office_id on attendances — use users.office_id or tc.office_id
- attendances.status = 1 for active records
"""

from typing import Dict, Optional
from app.services.db_service import get_connection
from app.services.response_mode_service import detect_response_mode
from app.services.report_service import generate_report
from app.services.llm_service import format_answer


# Sensitive columns to strip from chat output
_SENSITIVE_COLS = {
    'id', 'user_id', 'trainee_id', 'course_id', 'office_id', 'password',
    'created_by', 'updated_by', 'created_at', 'updated_at', 'status',
    'aadhar', 'uan', 'pf_no', 'bank_acc', 'ifsc_code', 'android_id',
    'permanent_identity', 'photo', 'signature', 'email', 'office_email',
    'whatsapp_number', 'emergency_numbers', 'office_mobile', 'emg_mobile_no',
    'present_address', 'permanent_address', 'resi_address', 'pass_file',
    'user_log', 'room_log', 'attachment', 'hrms_id',
}


def _clean_val(v):
    """Convert Decimal/datetime to plain types for clean output."""
    from decimal import Decimal
    import datetime
    if isinstance(v, Decimal):
        if v % 1 == 0:
            return int(v)
        return float(v)
    if isinstance(v, (datetime.date, datetime.datetime)):
        return str(v)
    return v


def _format_rows_for_chat(rows: list, max_rows: int = 10, total_count: Optional[int] = None) -> str:
    """Convert rows to readable text for LLM formatting."""
    if not rows:
        return "No data found."
    if len(rows) == 1 and len(rows[0]) == 1:
        k = list(rows[0].keys())[0]
        v = _clean_val(rows[0][k])
        return f"{k}: {'N/A' if v is None else str(v)}"

    limited = rows[:max_rows]
    lines = []
    for i, row in enumerate(limited, 1):
        parts = []
        for k, v in row.items():
            if k.lower() not in _SENSITIVE_COLS:
                v = _clean_val(v)
                val = "None / 0" if v is None else str(v)
                label = k.replace('_', ' ').title()
                parts.append(f"{label}: {val}")
        if parts:
            lines.append(f"{i}. " + " | ".join(parts))

    actual_total = total_count if total_count is not None else len(rows)
    summary = f"Total count: {actual_total}"
    if actual_total > max_rows:
        summary += f"\n(showing top {max_rows} to avoid text overload. Use 'show list' for full report)"
    return summary + "\n" + "\n".join(lines)


def execute_attendance_guided_query(
    flow_id: str,
    slots: dict,
    office_id: int,
    role: str,
    session_id: str = None,
    user_question: str = "",
    base_url: str = os.getenv("API_BASE_URL", ""),
) -> dict:
    """Execute the final guided query and return formatted result."""
    try:
        print(f"[Attendance Guided] Executing: {flow_id} with slots: {slots}")
        handler = {
            "attendance_by_trainee": _exec_attendance_by_trainee,
            "attendance_percentage_by_trainee": _exec_attendance_percentage_by_trainee,
            "absent_trainees": _exec_absent_trainees,
            "present_trainees": _exec_present_trainees,
            "course_attendance_summary": _exec_course_attendance_summary,
            "low_attendance_trainees": _exec_low_attendance_trainees,
            "date_wise_attendance": _exec_date_wise_attendance,
            "trainee_absent_count": _exec_trainee_absent_count,
            "trainee_present_count": _exec_trainee_present_count,
            "batch_attendance_report": _exec_batch_attendance_report,
        }.get(flow_id)
        if not handler:
            return None
        return handler(slots, office_id, user_question, session_id, base_url)
    except Exception as e:
        print(f"[Attendance Guided] Error executing {flow_id}: {e}")
        return {"type": "text", "message": f"Error retrieving attendance data: {str(e)}"}


def _build_response(rows, question, office_id, session_id, base_url,
                     force_report=False, force_chat=False, total_count=None):
    """Build chat or report response from query rows."""
    row_count = len(rows)
    actual_count = total_count if total_count is not None else row_count

    if actual_count == 0:
        return {"type": "text", "message": "No matching attendance data found for your request."}

    if force_chat:
        mode = "chat"
    elif force_report:
        mode = "report"
    else:
        mode = detect_response_mode(
            user_question=question,
            result_type="list" if actual_count > 1 else "single",
            row_count=actual_count,
        )

    if mode == "report" and row_count >= 1:
        report = generate_report(
            module_name="attendance",
            title="Attendance Report",
            user_question=question,
            rows=rows,
            office_id=office_id,
            session_id=session_id,
        )
        full_url = base_url.rstrip("/") + report["url"]
        ttl = report["ttl_seconds"]
        if ttl < 60:
            exp = f"{ttl} seconds"
        elif ttl < 3600:
            exp = f"{ttl // 60} minute{'s' if ttl // 60 != 1 else ''}"
        else:
            exp = f"{ttl // 3600} hour{'s' if ttl // 3600 != 1 else ''}"

        if total_count and total_count > row_count:
            count_msg = f"Found {total_count} records (showing {report['row_count']} in report)."
        else:
            count_msg = f"Found {report['row_count']} records for your request."

        answer = (
            f"{count_msg}\n\n"
            f"Open full report: {full_url}\n\n"
            f"This report link will expire in {exp}."
        )
        return {
            "type": "text",
            "message": answer,
            "report_url": full_url,
            "row_count": report["row_count"],
            "response_mode": "report",
            "expires_at": report["expires_at"],
        }
    else:
        formatted_text = _format_rows_for_chat(rows, total_count=total_count)
        answer = format_answer(question, formatted_text)
        return {"type": "text", "message": answer}


def _get_latest_attendance_date(cur, office_id):
    """Get the latest date that has attendance data for this office."""
    cur.execute("""
        SELECT MAX(DATE(a.punch_time)) AS latest_date
        FROM attendances a
        JOIN users u ON u.id = a.user_id
        WHERE a.status = 1 AND u.office_id = %s
    """, (office_id,))
    row = cur.fetchone()
    return str(row["latest_date"]) if row and row["latest_date"] else None


def _resolve_date_sql(date_val: str):
    """Convert date slot value into SQL date expression and params.
    Returns (sql_fragment, params_list).
    """
    from app.services.date_parser import parse_loose_date
    date_val = parse_loose_date(date_val)
    
    if not date_val or date_val == "ALL":
        return None, []
    if date_val == "today":
        return "DATE(a.punch_time) = CURDATE()", []
    if date_val == "yesterday":
        return "DATE(a.punch_time) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)", []
    if date_val == "last_7_days":
        return "DATE(a.punch_time) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)", []
    if date_val == "last_30_days":
        return "DATE(a.punch_time) >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)", []
    # Explicit date
    return "DATE(a.punch_time) = %s", [date_val]


def _resolve_course_filter(course_id, alias="a"):
    """Build course filter SQL fragment.
    Returns (sql_fragment, params_list).
    """
    if not course_id or course_id == "ALL":
        return "", []
    return f" AND {alias}.course_id = %s", [course_id]


# ═══════════════════════════════════════════════════════════════════
# Individual executor handlers
# ═══════════════════════════════════════════════════════════════════

def _exec_attendance_by_trainee(slots, office_id, question, session_id, base_url):
    """Trainee attendance records — date-wise list or report."""
    user_id = slots.get("user_id")
    if not user_id:
        return {"type": "text", "message": "Please specify which trainee you mean."}

    course_id = slots.get("course_id")
    conn = get_connection()
    try:
        cur = conn.cursor()

        course_filter, course_params = _resolve_course_filter(course_id)

        # Count
        count_sql = f"""
            SELECT COUNT(*) AS cnt
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            WHERE a.user_id = %s AND u.office_id = %s AND a.status = 1{course_filter}
        """
        cur.execute(count_sql, [user_id, office_id] + course_params)
        total_count = cur.fetchone()["cnt"]

        # Data
        sql = f"""
            SELECT DATE(a.punch_time) AS attendance_date,
                   c.course_name, tc.course_batch,
                   CASE a.punch
                     WHEN '4' THEN 'Present'
                     WHEN '5' THEN 'Absent'
                     WHEN '1' THEN 'CL'
                     WHEN '2' THEN 'LAP'
                     WHEN '3' THEN 'SL'
                     ELSE 'Unknown'
                   END AS attendance_status,
                   a.remarks
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.user_id = %s AND u.office_id = %s AND a.status = 1{course_filter}
            ORDER BY a.punch_time DESC
            LIMIT 500
        """
        cur.execute(sql, [user_id, office_id] + course_params)
        rows = cur.fetchall()

        return _build_response(rows, question, office_id, session_id, base_url,
                               force_report=True, total_count=total_count)
    finally:
        conn.close()


def _exec_attendance_percentage_by_trainee(slots, office_id, question, session_id, base_url):
    """Attendance percentage for a specific trainee."""
    user_id = slots.get("user_id")
    if not user_id:
        return {"type": "text", "message": "Please specify which trainee you mean."}

    course_id = slots.get("course_id")
    conn = get_connection()
    try:
        cur = conn.cursor()

        course_filter, course_params = _resolve_course_filter(course_id)

        sql = f"""
            SELECT u.name AS trainee_name, u.user_code,
                   c.course_name, tc.course_batch,
                   COUNT(a.id) AS total_days,
                   SUM(IF(a.punch = '4', 1, 0)) AS present_days,
                   SUM(IF(a.punch = '5', 1, 0)) AS absent_days,
                   ROUND(SUM(IF(a.punch = '4', 1, 0)) * 100.0 / NULLIF(COUNT(a.id), 0), 1) AS attendance_percentage
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.user_id = %s AND u.office_id = %s AND a.status = 1{course_filter}
            GROUP BY a.course_id, u.name, u.user_code, c.course_name, tc.course_batch
            ORDER BY tc.from_date DESC
        """
        cur.execute(sql, [user_id, office_id] + course_params)
        rows = cur.fetchall()

        # Always chat for percentage
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_absent_trainees(slots, office_id, question, session_id, base_url):
    """List absent trainees. If date not specified, shows latest absent records."""
    date_val = slots.get("date")
    course_id = slots.get("course_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        course_filter, course_params = _resolve_course_filter(course_id)

        date_filter, date_params = _resolve_date_sql(date_val)
        date_where = f" AND {date_filter}" if date_filter else ""

        # Count
        count_sql = f"SELECT COUNT(*) AS cnt FROM attendances a JOIN users u ON u.id = a.user_id JOIN training_calendars tc ON tc.id = a.course_id WHERE a.punch NOT IN ('0','4') AND a.status = 1 AND tc.office_id = %s{date_where}{course_filter}"
        cur.execute(count_sql, [office_id] + date_params + course_params)
        total_count = cur.fetchone()["cnt"]

        sql = f"""
            SELECT u.name AS trainee_name, u.user_code,
                   c.course_name, tc.course_batch,
                   DATE(a.punch_time) AS attendance_date, a.remarks
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.punch NOT IN ('0','4') AND a.status = 1 AND tc.office_id = %s{date_where}{course_filter}
            ORDER BY a.punch_time DESC LIMIT 500
        """
        cur.execute(sql, [office_id] + date_params + course_params)
        rows = cur.fetchall()

        return _build_response(rows, question, office_id, session_id, base_url, total_count=total_count)
    finally:
        conn.close()


def _exec_present_trainees(slots, office_id, question, session_id, base_url):
    """List present trainees. If date not specified, shows latest present records."""
    date_val = slots.get("date")
    course_id = slots.get("course_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        course_filter, course_params = _resolve_course_filter(course_id)

        date_filter, date_params = _resolve_date_sql(date_val)
        date_where = f" AND {date_filter}" if date_filter else ""

        count_sql = f"SELECT COUNT(*) AS cnt FROM attendances a JOIN users u ON u.id = a.user_id JOIN training_calendars tc ON tc.id = a.course_id WHERE a.punch = '4' AND a.status = 1 AND tc.office_id = %s{date_where}{course_filter}"
        cur.execute(count_sql, [office_id] + date_params + course_params)
        total_count = cur.fetchone()["cnt"]

        sql = f"""
            SELECT u.name AS trainee_name, u.user_code,
                   c.course_name, tc.course_batch,
                   DATE(a.punch_time) AS attendance_date
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.punch = '4' AND a.status = 1 AND tc.office_id = %s{date_where}{course_filter}
            ORDER BY a.punch_time DESC LIMIT 500
        """
        cur.execute(sql, [office_id] + date_params + course_params)
        rows = cur.fetchall()

        return _build_response(rows, question, office_id, session_id, base_url, total_count=total_count)
    finally:
        conn.close()


def _exec_course_attendance_summary(slots, office_id, question, session_id, base_url):
    """Course-wise attendance summary."""
    course_id = slots.get("course_id")
    conn = get_connection()
    try:
        cur = conn.cursor()

        course_filter, course_params = _resolve_course_filter(course_id)

        sql = f"""
            SELECT c.course_name, tc.course_batch,
                   tc.from_date, tc.to_date,
                   COUNT(DISTINCT a.user_id) AS total_trainees,
                   COUNT(DISTINCT DATE(a.punch_time)) AS total_days,
                   SUM(CASE WHEN a.punch = '4' THEN 1 ELSE 0 END) AS present_count,
                   SUM(CASE WHEN a.punch = '5' THEN 1 ELSE 0 END) AS absent_count,
                   ROUND(
                     SUM(CASE WHEN a.punch = '4' THEN 1 ELSE 0 END) * 100.0
                     / NULLIF(COUNT(a.id), 0), 1
                   ) AS overall_present_pct
            FROM attendances a
            JOIN training_calendars tc ON tc.id = a.course_id AND tc.status = 1
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE a.status = 1{course_filter}
            GROUP BY a.course_id, c.course_name, tc.course_batch, tc.from_date, tc.to_date
            ORDER BY tc.from_date DESC
            LIMIT 100
        """
        cur.execute(sql, [office_id] + course_params)
        rows = cur.fetchall()

        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_low_attendance_trainees(slots, office_id, question, session_id, base_url):
    """Trainees with attendance percentage below threshold."""
    threshold = slots.get("threshold", 75)
    course_id = slots.get("course_id")
    conn = get_connection()
    try:
        cur = conn.cursor()

        course_filter, course_params = _resolve_course_filter(course_id)

        # Count first
        count_sql = f"""
            SELECT COUNT(*) AS cnt FROM (
                SELECT a.user_id,
                       ROUND(SUM(IF(a.punch='4',1,0))*100.0/NULLIF(COUNT(a.id),0),1) AS att_pct
                FROM attendances a
                JOIN users u ON u.id = a.user_id
                WHERE a.status = 1 AND u.office_id = %s{course_filter}
                GROUP BY a.user_id
                HAVING att_pct < %s
            ) sub
        """
        cur.execute(count_sql, [office_id] + course_params + [threshold])
        total_count = cur.fetchone()["cnt"]

        sql = f"""
            SELECT u.name AS trainee_name, u.user_code,
                   c.course_name, tc.course_batch,
                   COUNT(a.id) AS total_days,
                   SUM(IF(a.punch='4',1,0)) AS present_days,
                   ROUND(SUM(IF(a.punch='4',1,0))*100.0/NULLIF(COUNT(a.id),0),1) AS attendance_pct
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.status = 1 AND u.office_id = %s{course_filter}
            GROUP BY a.user_id, u.name, u.user_code, c.course_name, tc.course_batch
            HAVING attendance_pct < %s
            ORDER BY attendance_pct ASC
            LIMIT 500
        """
        cur.execute(sql, [office_id] + course_params + [threshold])
        rows = cur.fetchall()

        return _build_response(rows, question, office_id, session_id, base_url,
                               total_count=total_count)
    finally:
        conn.close()


def _exec_date_wise_attendance(slots, office_id, question, session_id, base_url):
    """Attendance summary for a specific date. Falls back to latest date if today has no data."""
    date_val = slots.get("date", "today")
    course_id = slots.get("course_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        course_filter, course_params = _resolve_course_filter(course_id)

        date_filter, date_params = _resolve_date_sql(date_val)
        date_where = f" AND {date_filter}" if date_filter else " AND DATE(a.punch_time) = CURDATE()"

        sql = f"""
            SELECT DATE(a.punch_time) AS attendance_date,
                   c.course_name, tc.course_batch,
                   COUNT(DISTINCT a.user_id) AS total_trainees,
                   SUM(CASE WHEN a.punch = '4' THEN 1 ELSE 0 END) AS present_count,
                   SUM(CASE WHEN a.punch = '5' THEN 1 ELSE 0 END) AS absent_count,
                   SUM(CASE WHEN a.punch IN ('1','2','3') THEN 1 ELSE 0 END) AS on_leave_count
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.status = 1 AND u.office_id = %s{date_where}{course_filter}
            GROUP BY DATE(a.punch_time), c.course_name, tc.course_batch
            ORDER BY attendance_date DESC LIMIT 100
        """
        cur.execute(sql, [office_id] + date_params + course_params)
        rows = cur.fetchall()

        fallback_note = ""
        if not rows and date_val in ("today", "yesterday"):
            latest = _get_latest_attendance_date(cur, office_id)
            if latest:
                date_where = " AND DATE(a.punch_time) = %s"
                date_params = [latest]
                cur.execute(f"""
                    SELECT DATE(a.punch_time) AS attendance_date,
                           c.course_name, tc.course_batch,
                           COUNT(DISTINCT a.user_id) AS total_trainees,
                           SUM(CASE WHEN a.punch = '4' THEN 1 ELSE 0 END) AS present_count,
                           SUM(CASE WHEN a.punch = '5' THEN 1 ELSE 0 END) AS absent_count,
                           SUM(CASE WHEN a.punch IN ('1','2','3') THEN 1 ELSE 0 END) AS on_leave_count
                    FROM attendances a
                    JOIN users u ON u.id = a.user_id
                    JOIN training_calendars tc ON tc.id = a.course_id
                    JOIN courses c ON c.id = tc.ct_id
                    WHERE a.status = 1 AND u.office_id = %s{date_where}{course_filter}
                    GROUP BY DATE(a.punch_time), c.course_name, tc.course_batch
                    ORDER BY attendance_date DESC LIMIT 100
                """, [office_id] + date_params + course_params)
                rows = cur.fetchall()
                fallback_note = f"No attendance data for {date_val}. Showing latest available date ({latest}).\n\n"

        result = _build_response(rows, question, office_id, session_id, base_url)
        if fallback_note and result.get("message"):
            result["message"] = fallback_note + result["message"]
        return result
    finally:
        conn.close()


def _exec_trainee_absent_count(slots, office_id, question, session_id, base_url):
    """Count of absent days for a specific trainee."""
    user_id = slots.get("user_id")
    if not user_id:
        return {"type": "text", "message": "Please specify which trainee you mean."}

    course_id = slots.get("course_id")
    conn = get_connection()
    try:
        cur = conn.cursor()

        course_filter, course_params = _resolve_course_filter(course_id)

        sql = f"""
            SELECT u.name AS trainee_name,
                   c.course_name, tc.course_batch,
                   SUM(IF(a.punch = '5', 1, 0)) AS absent_days,
                   COUNT(a.id) AS total_attendance_days
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.user_id = %s AND u.office_id = %s AND a.status = 1{course_filter}
            GROUP BY a.course_id, u.name, c.course_name, tc.course_batch
            ORDER BY tc.from_date DESC
        """
        cur.execute(sql, [user_id, office_id] + course_params)
        rows = cur.fetchall()

        # Always chat for count questions
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_trainee_present_count(slots, office_id, question, session_id, base_url):
    """Count of present days for a specific trainee."""
    user_id = slots.get("user_id")
    if not user_id:
        return {"type": "text", "message": "Please specify which trainee you mean."}

    course_id = slots.get("course_id")
    conn = get_connection()
    try:
        cur = conn.cursor()

        course_filter, course_params = _resolve_course_filter(course_id)

        sql = f"""
            SELECT u.name AS trainee_name,
                   c.course_name, tc.course_batch,
                   SUM(IF(a.punch = '4', 1, 0)) AS present_days,
                   COUNT(a.id) AS total_attendance_days
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.user_id = %s AND u.office_id = %s AND a.status = 1{course_filter}
            GROUP BY a.course_id, u.name, c.course_name, tc.course_batch
            ORDER BY tc.from_date DESC
        """
        cur.execute(sql, [user_id, office_id] + course_params)
        rows = cur.fetchall()

        # Always chat for count questions
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_batch_attendance_report(slots, office_id, question, session_id, base_url):
    """Attendance report for a batch/course — always report mode."""
    course_id = slots.get("course_id")
    recent_filter = slots.get("recent_filter")
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Auto-resolve latest/current course if not specified
        if not course_id and recent_filter in ("latest", "recent"):
            cur.execute("""
                SELECT tc.id FROM training_calendars tc
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                JOIN attendances a ON a.course_id = tc.id AND a.status = 1
                WHERE tc.status = 1
                ORDER BY tc.from_date DESC LIMIT 1
            """, (office_id,))
            row = cur.fetchone()
            if row:
                course_id = row["id"]

        if not course_id and recent_filter == "current":
            cur.execute("""
                SELECT tc.id FROM training_calendars tc
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                WHERE tc.status = 1
                  AND tc.from_date <= CURDATE()
                  AND tc.to_date >= CURDATE()
                ORDER BY tc.from_date DESC LIMIT 1
            """, (office_id,))
            row = cur.fetchone()
            if row:
                course_id = row["id"]

        course_filter, course_params = _resolve_course_filter(course_id)

        # Count
        count_sql = f"""
            SELECT COUNT(DISTINCT a.user_id) AS cnt
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            WHERE a.status = 1 AND u.office_id = %s{course_filter}
        """
        cur.execute(count_sql, [office_id] + course_params)
        total_count = cur.fetchone()["cnt"]

        sql = f"""
            SELECT u.name AS trainee_name, u.user_code,
                   c.course_name, tc.course_batch,
                   COUNT(a.id) AS total_days,
                   SUM(IF(a.punch='4',1,0)) AS present_days,
                   SUM(IF(a.punch='5',1,0)) AS absent_days,
                   ROUND(SUM(IF(a.punch='4',1,0))*100.0/NULLIF(COUNT(a.id),0),1) AS attendance_pct
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.status = 1 AND u.office_id = %s{course_filter}
            GROUP BY a.user_id, u.name, u.user_code, c.course_name, tc.course_batch
            ORDER BY attendance_pct DESC
            LIMIT 500
        """
        cur.execute(sql, [office_id] + course_params)
        rows = cur.fetchall()

        # Batch attendance report → always report mode
        return _build_response(rows, question, office_id, session_id, base_url,
                               force_report=True, total_count=total_count)
    finally:
        conn.close()
