import os
"""Course query executor — runs final parameterized SQL for course guided flows.

Uses existing response_mode_service and report_service for output formatting.

Schema notes:
- training_calendars.ct_id = courses.id
- training_calendars has: from_date, to_date, course_batch, status, office_id
- courses has: course_name, office_id, status
- tra_masters.course_id = training_calendars.id (trainee enrollment)
- tra_masters.status = 1 for active enrollment
"""

from typing import Dict, Optional
from app.services.db_service import get_connection
from app.services.response_mode_service import detect_response_mode
from app.services.report_service import generate_report
from app.services.llm_service import format_answer


# Sensitive columns to strip from chat output
_SENSITIVE_COLS = {
    'id', 'user_id', 'trainee_id', 'ct_id', 'office_id', 'password',
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


def execute_course_guided_query(
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
        print(f"[Course Guided] Executing: {flow_id} with slots: {slots}")
        handler = {
            "current_courses": _exec_current_courses,
            "latest_course": _exec_latest_course,
            "upcoming_courses": _exec_upcoming_courses,
            "completed_courses": _exec_completed_courses,
            "course_details_by_name": _exec_course_details_by_name,
            "course_trainee_count": _exec_course_trainee_count,
            "course_wise_trainee_count": _exec_course_wise_trainee_count,
            "course_duration_summary": _exec_course_duration_summary,
            "batch_details": _exec_batch_details,
            "course_calendar_summary": _exec_course_calendar_summary,
        }.get(flow_id)
        if not handler:
            return None
        return handler(slots, office_id, user_question, session_id, base_url)
    except Exception as e:
        print(f"[Course Guided] Error executing {flow_id}: {e}")
        return {"type": "text", "message": f"Error retrieving course data: {str(e)}"}


def _build_response(rows, question, office_id, session_id, base_url,
                     force_report=False, force_chat=False, total_count=None):
    """Build chat or report response from query rows."""
    row_count = len(rows)
    actual_count = total_count if total_count is not None else row_count

    if actual_count == 0:
        return {"type": "text", "message": "No matching course data found for your request."}

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

    if mode == "report" and row_count > 1:
        report = generate_report(
            module_name="course",
            title="Course Report",
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


# ═══════════════════════════════════════════════════════════════════
# Individual executor handlers
# ═══════════════════════════════════════════════════════════════════

def _resolve_course_id_filter(course_id, alias="tc"):
    """Build course_id filter SQL fragment."""
    if not course_id or course_id == "ALL":
        return "", []
    return f" AND {alias}.id = %s", [course_id]


def _exec_current_courses(slots, office_id, question, session_id, base_url):
    """Currently ongoing courses."""
    conn = get_connection()
    try:
        cur = conn.cursor()

        sql = """
            SELECT c.course_name, tc.course_batch,
                   tc.from_date AS start_date, tc.to_date AS end_date,
                   DATEDIFF(tc.to_date, tc.from_date) + 1 AS duration_days,
                   (SELECT COUNT(*) FROM tra_masters tm
                    WHERE tm.course_id = tc.id AND tm.status = 1) AS trainee_count
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE tc.status = 1
              AND tc.from_date <= CURDATE()
              AND tc.to_date >= CURDATE()
            ORDER BY tc.from_date DESC
        """
        cur.execute(sql, (office_id,))
        rows = cur.fetchall()

        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_latest_course(slots, office_id, question, session_id, base_url):
    """Latest/most recently started course."""
    conn = get_connection()
    try:
        cur = conn.cursor()

        sql = """
            SELECT c.course_name, tc.course_batch,
                   tc.from_date AS start_date, tc.to_date AS end_date,
                   DATEDIFF(tc.to_date, tc.from_date) + 1 AS duration_days,
                   (SELECT COUNT(*) FROM tra_masters tm
                    WHERE tm.course_id = tc.id AND tm.status = 1) AS trainee_count
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE tc.status = 1
            ORDER BY tc.from_date DESC
            LIMIT 1
        """
        cur.execute(sql, (office_id,))
        rows = cur.fetchall()

        return _build_response(rows, question, office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_upcoming_courses(slots, office_id, question, session_id, base_url):
    """Upcoming courses (from_date > today)."""
    year = slots.get("year")
    month = slots.get("month")
    conn = get_connection()
    try:
        cur = conn.cursor()

        sql = """
            SELECT c.course_name, tc.course_batch,
                   tc.from_date AS start_date, tc.to_date AS end_date,
                   DATEDIFF(tc.to_date, tc.from_date) + 1 AS duration_days
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE tc.status = 1
              AND tc.from_date > CURDATE()
        """
        params = [office_id]

        if year:
            sql += " AND YEAR(tc.from_date) = %s"
            params.append(year)
        if month:
            sql += " AND MONTH(tc.from_date) = %s"
            params.append(month)

        sql += " ORDER BY tc.from_date ASC LIMIT 100"
        cur.execute(sql, params)
        rows = cur.fetchall()

        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_completed_courses(slots, office_id, question, session_id, base_url):
    """Completed courses (to_date < today)."""
    year = slots.get("year")
    conn = get_connection()
    try:
        cur = conn.cursor()

        sql = """
            SELECT c.course_name, tc.course_batch,
                   tc.from_date AS start_date, tc.to_date AS end_date,
                   DATEDIFF(tc.to_date, tc.from_date) + 1 AS duration_days,
                   (SELECT COUNT(*) FROM tra_masters tm
                    WHERE tm.course_id = tc.id AND tm.status = 1) AS trainee_count
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE tc.status = 1
              AND tc.to_date < CURDATE()
        """
        params = [office_id]

        if year:
            sql += " AND YEAR(tc.from_date) = %s"
            params.append(year)

        sql += " ORDER BY tc.to_date DESC LIMIT 200"
        cur.execute(sql, params)
        rows = cur.fetchall()

        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_course_details_by_name(slots, office_id, question, session_id, base_url):
    """Course details — specific course or latest/current auto-resolve."""
    course_id = slots.get("course_id")
    recent_filter = slots.get("recent_filter")
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Auto-resolve latest
        if not course_id and recent_filter == "latest":
            cur.execute("""
                SELECT tc.id FROM training_calendars tc
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                WHERE tc.status = 1
                ORDER BY tc.from_date DESC LIMIT 1
            """, (office_id,))
            row = cur.fetchone()
            if row:
                course_id = row["id"]

        # Auto-resolve current
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

        course_filter, course_params = _resolve_course_id_filter(course_id)

        sql = f"""
            SELECT c.course_name, tc.course_batch,
                   tc.from_date AS start_date, tc.to_date AS end_date,
                   DATEDIFF(tc.to_date, tc.from_date) + 1 AS duration_days,
                   (SELECT COUNT(*) FROM tra_masters tm
                    WHERE tm.course_id = tc.id AND tm.status = 1) AS trainee_count,
                   CASE
                     WHEN tc.from_date > CURDATE() THEN 'Upcoming'
                     WHEN tc.to_date < CURDATE() THEN 'Completed'
                     ELSE 'Ongoing'
                   END AS course_status
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE tc.status = 1{course_filter}
            ORDER BY tc.from_date DESC
            LIMIT 20
        """
        cur.execute(sql, [office_id] + course_params)
        rows = cur.fetchall()

        force_chat = len(rows) <= 3
        return _build_response(rows, question, office_id, session_id, base_url,
                               force_chat=force_chat)
    finally:
        conn.close()


def _exec_course_trainee_count(slots, office_id, question, session_id, base_url):
    """Trainee count for a specific course."""
    course_id = slots.get("course_id")
    recent_filter = slots.get("recent_filter")
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Auto-resolve latest
        if not course_id and recent_filter == "latest":
            cur.execute("""
                SELECT tc.id FROM training_calendars tc
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                WHERE tc.status = 1
                ORDER BY tc.from_date DESC LIMIT 1
            """, (office_id,))
            row = cur.fetchone()
            if row:
                course_id = row["id"]

        # Auto-resolve current
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

        course_filter, course_params = _resolve_course_id_filter(course_id)

        sql = f"""
            SELECT c.course_name, tc.course_batch,
                   tc.from_date AS start_date, tc.to_date AS end_date,
                   COUNT(tm.id) AS trainee_count
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            LEFT JOIN tra_masters tm ON tm.course_id = tc.id AND tm.status = 1
            WHERE tc.status = 1{course_filter}
            GROUP BY tc.id, c.course_name, tc.course_batch, tc.from_date, tc.to_date
            ORDER BY tc.from_date DESC
            LIMIT 20
        """
        cur.execute(sql, [office_id] + course_params)
        rows = cur.fetchall()

        # Count question → always chat
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_course_wise_trainee_count(slots, office_id, question, session_id, base_url):
    """Course-wise trainee count summary."""
    year = slots.get("year")
    conn = get_connection()
    try:
        cur = conn.cursor()

        sql = """
            SELECT c.course_name, tc.course_batch,
                   tc.from_date AS start_date, tc.to_date AS end_date,
                   COUNT(tm.id) AS trainee_count
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            LEFT JOIN tra_masters tm ON tm.course_id = tc.id AND tm.status = 1
            WHERE tc.status = 1
        """
        params = [office_id]

        if year:
            sql += " AND YEAR(tc.from_date) = %s"
            params.append(year)

        sql += """
            GROUP BY tc.id, c.course_name, tc.course_batch, tc.from_date, tc.to_date
            ORDER BY tc.from_date DESC
            LIMIT 200
        """
        cur.execute(sql, params)
        rows = cur.fetchall()

        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_course_duration_summary(slots, office_id, question, session_id, base_url):
    """Course duration — start date, end date, and duration days."""
    course_id = slots.get("course_id")
    recent_filter = slots.get("recent_filter")
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Auto-resolve latest
        if not course_id and recent_filter == "latest":
            cur.execute("""
                SELECT tc.id FROM training_calendars tc
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                WHERE tc.status = 1
                ORDER BY tc.from_date DESC LIMIT 1
            """, (office_id,))
            row = cur.fetchone()
            if row:
                course_id = row["id"]

        # Auto-resolve current
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

        course_filter, course_params = _resolve_course_id_filter(course_id)

        sql = f"""
            SELECT c.course_name, tc.course_batch,
                   tc.from_date AS start_date, tc.to_date AS end_date,
                   DATEDIFF(tc.to_date, tc.from_date) + 1 AS duration_days,
                   CASE
                     WHEN tc.from_date > CURDATE() THEN 'Upcoming'
                     WHEN tc.to_date < CURDATE() THEN 'Completed'
                     ELSE 'Ongoing'
                   END AS course_status
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE tc.status = 1{course_filter}
            ORDER BY tc.from_date DESC
            LIMIT 50
        """
        cur.execute(sql, [office_id] + course_params)
        rows = cur.fetchall()

        force_chat = len(rows) <= 3
        return _build_response(rows, question, office_id, session_id, base_url,
                               force_chat=force_chat)
    finally:
        conn.close()


def _exec_batch_details(slots, office_id, question, session_id, base_url):
    """Batch details — same as course details but batch-focused."""
    # Reuse course_details logic
    return _exec_course_details_by_name(slots, office_id, question, session_id, base_url)


def _exec_course_calendar_summary(slots, office_id, question, session_id, base_url):
    """Course calendar summary — month/year wise."""
    year = slots.get("year")
    month = slots.get("month")
    status = slots.get("status")
    conn = get_connection()
    try:
        cur = conn.cursor()

        sql = """
            SELECT c.course_name, tc.course_batch,
                   tc.from_date AS start_date, tc.to_date AS end_date,
                   DATEDIFF(tc.to_date, tc.from_date) + 1 AS duration_days,
                   (SELECT COUNT(*) FROM tra_masters tm
                    WHERE tm.course_id = tc.id AND tm.status = 1) AS trainee_count,
                   CASE
                     WHEN tc.from_date > CURDATE() THEN 'Upcoming'
                     WHEN tc.to_date < CURDATE() THEN 'Completed'
                     ELSE 'Ongoing'
                   END AS course_status
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE tc.status = 1
        """
        params = [office_id]

        if year:
            sql += " AND YEAR(tc.from_date) = %s"
            params.append(year)
        if month:
            sql += " AND MONTH(tc.from_date) = %s"
            params.append(month)
        if status and status != "all":
            if status == "current":
                sql += " AND tc.from_date <= CURDATE() AND tc.to_date >= CURDATE()"
            elif status == "upcoming":
                sql += " AND tc.from_date > CURDATE()"
            elif status == "completed":
                sql += " AND tc.to_date < CURDATE()"

        sql += " ORDER BY tc.from_date DESC LIMIT 200"
        cur.execute(sql, params)
        rows = cur.fetchall()

        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()
