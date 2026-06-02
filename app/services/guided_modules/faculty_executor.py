import os
"""Faculty / VL query executor — runs final parameterized SQL for faculty guided flows.

Uses existing response_mode_service and report_service for output formatting.
"""

from typing import Dict, Optional
from app.services.db_service import get_connection
from app.services.response_mode_service import detect_response_mode
from app.services.report_service import generate_report
from app.services.llm_service import format_answer


_SENSITIVE_COLS = {
    'id', 'user_id', 'course_id', 'office_id', 'password',
    'created_by', 'updated_by', 'created_at', 'updated_at', 'status',
    'aadhar', 'uan', 'pf_no', 'bank_acc', 'ifsc_code', 'android_id',
    'permanent_identity', 'photo', 'signature', 'email', 'office_email',
    'whatsapp_number', 'emergency_numbers', 'office_mobile', 'emg_mobile_no',
    'present_address', 'permanent_address', 'resi_address', 'pass_file',
    'user_log', 'room_log', 'attachment', 'hrms_id',
}


def _clean_val(v):
    from decimal import Decimal
    import datetime as dt
    if isinstance(v, Decimal): return float(v)
    if isinstance(v, (dt.date, dt.datetime, dt.timedelta)): return str(v)
    return v


def _format_rows_for_chat(rows: list, max_rows: int = 10, total_count: Optional[int] = None) -> str:
    if not rows: return "No data found."
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
        summary += f"\n(showing top {max_rows}. Use 'show list' for full report)"
    return summary + "\n" + "\n".join(lines)


def execute_faculty_guided_query(
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
        print(f"[Faculty Guided] Executing: {flow_id} with slots: {slots}")
        handler = {
            "faculty_profile_by_name": _exec_faculty_profile_by_name,
            "faculty_schedule": _exec_faculty_schedule,
            "faculty_courses": _exec_faculty_courses,
            "faculty_subjects": _exec_faculty_subjects,
            "faculty_workload_summary": _exec_faculty_workload_summary,
            "visiting_lecturers": _exec_visiting_lecturers,
            "faculty_feedback_summary": _exec_faculty_feedback_summary,
            "faculty_by_subject": _exec_faculty_by_subject,
            "faculty_by_course": _exec_faculty_by_course,
            "faculty_availability": _exec_faculty_availability,
        }.get(flow_id)
        if not handler: return None
        return handler(slots, office_id, user_question, session_id, base_url)
    except Exception as e:
        print(f"[Faculty Guided] Error executing {flow_id}: {e}")
        return {"type": "text", "message": f"Error retrieving faculty data: {str(e)}"}


def _build_response(rows, question, office_id, session_id, base_url,
                     force_report=False, force_chat=False, total_count=None):
    row_count = len(rows)
    actual_count = total_count if total_count is not None else row_count
    if actual_count == 0:
        return {"type": "text", "message": "No matching faculty data found for your request."}

    import re
    if not force_report and re.search(r"how\s+many|total|count", question.lower()):
        force_chat = True

    if force_chat: mode = "chat"
    elif force_report: mode = "report"
    else:
        mode = detect_response_mode(
            user_question=question,
            result_type="list" if actual_count > 1 else "single",
            row_count=actual_count,
        )

    if mode == "report" and row_count > 1:
        report = generate_report(
            module_name="faculty", title="Faculty Report",
            user_question=question, rows=rows,
            office_id=office_id, session_id=session_id,
        )
        full_url = base_url.rstrip("/") + report["url"]
        ttl = report["ttl_seconds"]
        if ttl < 60: exp = f"{ttl} seconds"
        elif ttl < 3600: exp = f"{ttl // 60} minute{'s' if ttl // 60 != 1 else ''}"
        else: exp = f"{ttl // 3600} hour{'s' if ttl // 3600 != 1 else ''}"
        if total_count and total_count > row_count:
            count_msg = f"Found {total_count} records (showing {report['row_count']} in report)."
        else:
            count_msg = f"Found {report['row_count']} records for your request."
        answer = f"{count_msg}\n\nOpen full report: {full_url}\n\nThis report link will expire in {exp}."
        return {
            "type": "text", "message": answer,
            "report_url": full_url, "row_count": report["row_count"],
            "response_mode": "report", "expires_at": report["expires_at"],
        }
    else:
        formatted_text = _format_rows_for_chat(rows, total_count=total_count)
        answer = format_answer(question, formatted_text)
        return {"type": "text", "message": answer}


def _resolve_date_sql(date_slot: str, alias: str = "tm") -> tuple:
    if not date_slot: return "", []
    if date_slot == "today": return f" AND {alias}.tm_date = CURDATE()", []
    if date_slot == "tomorrow": return f" AND {alias}.tm_date = DATE_ADD(CURDATE(), INTERVAL 1 DAY)", []
    if date_slot == "yesterday": return f" AND {alias}.tm_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY)", []
    if date_slot == "last_7_days": return f" AND {alias}.tm_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND {alias}.tm_date <= CURDATE()", []
    if date_slot == "ALL": return "", []
    return f" AND {alias}.tm_date = %s", [date_slot]


# ═══════════════════════════════════════════════════════════════════
# Individual executor handlers
# ═══════════════════════════════════════════════════════════════════

def _exec_faculty_profile_by_name(slots, office_id, question, session_id, base_url):
    f_id = slots.get("faculty_id")
    if not f_id:
        return {"type": "text", "message": "Please specify a faculty member."}
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.name, u.user_code, u.gender,
                   desi.desi_name AS designation, u.mobile
            FROM users u
            LEFT JOIN designations desi ON desi.id = u.desi_id
            WHERE u.id = %s AND u.office_id = %s
        """, (f_id, office_id))
        rows = cur.fetchall()
        if not rows:
            return {"type": "text", "message": "No faculty found with that ID."}
        # Also check VL info
        cur.execute("""
            SELECT vm.subject_name AS vl_subject, vm.vl_date, vm.description_1
            FROM vl_management vm
            WHERE vm.vl_id = %s AND vm.office_id = %s AND vm.status = 1
            ORDER BY vm.vl_date DESC LIMIT 5
        """, (f_id, office_id))
        vl_rows = cur.fetchall()
        if vl_rows:
            for vr in vl_rows:
                rows[0]["vl_subject"] = vr.get("vl_subject", "")
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_faculty_schedule(slots, office_id, question, session_id, base_url):
    f_id = slots.get("faculty_id")
    d_slot = slots.get("date", "ALL")
    d_sql, d_params = _resolve_date_sql(d_slot)
    if not f_id:
        return {"type": "text", "message": "Please specify a faculty member."}
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = f"""
            SELECT tm.tm_date AS date, tm.start_time, tm.end_time,
                   c.course_name, tc.course_batch,
                   tm.topic_name, s.subject_name,
                   cr.class_name AS classroom,
                   ses.session AS session_name
            FROM time_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            LEFT JOIN subjects s ON s.id = tm.cs_id
            LEFT JOIN class_rooms cr ON cr.id = tm.class_id
            LEFT JOIN sessions ses ON ses.id = tm.session_id
            WHERE tm.desi_user_id = %s AND tm.office_id = %s AND tm.status = 1{d_sql}
            ORDER BY tm.tm_date DESC, tm.start_time
            LIMIT 300
        """
        cur.execute(sql, [f_id, office_id] + d_params)
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_faculty_courses(slots, office_id, question, session_id, base_url):
    f_id = slots.get("faculty_id")
    if not f_id:
        return {"type": "text", "message": "Please specify a faculty member."}
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT c.course_name, tc.course_batch, tc.from_date, tc.to_date
            FROM time_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE tm.desi_user_id = %s AND tm.office_id = %s AND tm.status = 1
            ORDER BY tc.from_date DESC
            LIMIT 50
        """, (f_id, office_id))
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_faculty_subjects(slots, office_id, question, session_id, base_url):
    f_id = slots.get("faculty_id")
    if not f_id:
        return {"type": "text", "message": "Please specify a faculty member."}
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT s.subject_name, COUNT(tm.id) AS session_count
            FROM time_masters tm
            JOIN subjects s ON s.id = tm.cs_id
            WHERE tm.desi_user_id = %s AND tm.office_id = %s AND tm.status = 1
            GROUP BY s.id, s.subject_name
            ORDER BY session_count DESC
            LIMIT 50
        """, (f_id, office_id))
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_faculty_workload_summary(slots, office_id, question, session_id, base_url):
    d_slot = slots.get("date", "ALL")
    d_sql, d_params = _resolve_date_sql(d_slot)
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = f"""
            SELECT u.name AS faculty_name, desi.desi_name AS designation,
                   COUNT(tm.id) AS lecture_count,
                   COUNT(DISTINCT tm.course_id) AS course_count,
                   COUNT(DISTINCT tm.cs_id) AS subject_count
            FROM time_masters tm
            JOIN users u ON u.id = tm.desi_user_id
            LEFT JOIN designations desi ON desi.id = u.desi_id
            WHERE tm.office_id = %s AND tm.status = 1{d_sql}
            GROUP BY u.id, u.name, desi.desi_name
            ORDER BY lecture_count DESC
            LIMIT 100
        """
        cur.execute(sql, [office_id] + d_params)
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_visiting_lecturers(slots, office_id, question, session_id, base_url):
    conn = get_connection()
    try:
        cur = conn.cursor()
        # Count
        cur.execute("""
            SELECT COUNT(*) AS cnt
            FROM vl_management vm
            WHERE vm.office_id = %s AND vm.status = 1
        """, (office_id,))
        total = cur.fetchone()["cnt"]

        cur.execute("""
            SELECT u.name AS vl_name, vm.subject_name, vm.vl_date,
                   vm.description_1 AS description
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            WHERE vm.office_id = %s AND vm.status = 1
            ORDER BY vm.vl_date DESC
            LIMIT 200
        """, (office_id,))
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url, total_count=total)
    finally:
        conn.close()


def _exec_faculty_feedback_summary(slots, office_id, question, session_id, base_url):
    f_id = slots.get("faculty_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        if f_id:
            cur.execute("""
                SELECT fqv.subject, fqv.year, COUNT(fqv.id) AS feedback_records
                FROM feed_que_vls fqv
                WHERE fqv.vl_id = %s AND fqv.office_id = %s AND fqv.status = 1
                GROUP BY fqv.subject, fqv.year
                ORDER BY fqv.year DESC
                LIMIT 50
            """, (f_id, office_id))
        else:
            cur.execute("""
                SELECT u.name AS faculty_name, fqv.subject, fqv.year,
                       COUNT(fqv.id) AS feedback_records
                FROM feed_que_vls fqv
                JOIN users u ON u.id = fqv.vl_id
                WHERE fqv.office_id = %s AND fqv.status = 1
                GROUP BY u.id, u.name, fqv.subject, fqv.year
                ORDER BY fqv.year DESC, feedback_records DESC
                LIMIT 100
            """, (office_id,))
        rows = cur.fetchall()
        if not rows:
            return {"type": "text", "message": "No faculty feedback data found. The feedback module may not have entries for this office."}
        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_faculty_by_subject(slots, office_id, question, session_id, base_url):
    s_id = slots.get("subject_id")
    if not s_id:
        return {"type": "text", "message": "Please specify a subject."}
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT u.name AS faculty_name, desi.desi_name AS designation,
                   COUNT(tm.id) AS session_count
            FROM time_masters tm
            JOIN users u ON u.id = tm.desi_user_id
            LEFT JOIN designations desi ON desi.id = u.desi_id
            WHERE tm.cs_id = %s AND tm.office_id = %s AND tm.status = 1
            GROUP BY u.id, u.name, desi.desi_name
            ORDER BY session_count DESC
            LIMIT 50
        """, (s_id, office_id))
        rows = cur.fetchall()
        # Also check VL for that subject
        cur.execute("""
            SELECT u.name AS faculty_name, 'Visiting Lecturer' AS designation,
                   vm.subject_name
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            JOIN subjects s ON LOWER(vm.subject_name) LIKE CONCAT('%%', LOWER(s.subject_name), '%%')
            WHERE s.id = %s AND vm.office_id = %s AND vm.status = 1
            LIMIT 20
        """, (s_id, office_id))
        vl_rows = cur.fetchall()
        all_rows = rows + vl_rows
        return _build_response(all_rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_faculty_by_course(slots, office_id, question, session_id, base_url):
    c_id = slots.get("course_id")
    if not c_id:
        return {"type": "text", "message": "Please specify a course."}
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT u.name AS faculty_name, desi.desi_name AS designation,
                   COUNT(tm.id) AS session_count
            FROM time_masters tm
            JOIN users u ON u.id = tm.desi_user_id
            LEFT JOIN designations desi ON desi.id = u.desi_id
            WHERE tm.course_id = %s AND tm.office_id = %s AND tm.status = 1
            GROUP BY u.id, u.name, desi.desi_name
            ORDER BY session_count DESC
            LIMIT 50
        """, (c_id, office_id))
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_faculty_availability(slots, office_id, question, session_id, base_url):
    return {
        "type": "text",
        "message": (
            "Faculty availability needs timetable sessions and faculty allocation records. "
            "I found timetable data but cannot reliably calculate free faculty from the current schema."
        )
    }
