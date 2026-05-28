"""Guided query executor — runs final parameterized SQL once all slots are filled.

Uses existing response_mode_service and report_service for output formatting.
"""

from typing import Dict, Optional
from app.services.db_service import get_connection
from app.services.response_mode_service import detect_response_mode
from app.services.report_service import generate_report
from app.services.llm_service import format_answer


# Sensitive columns to strip from results shown in chat
_SENSITIVE_COLS = {
    'id', 'user_id', 'trainee_id', 'course_id', 'office_id', 'password',
    'created_by', 'updated_by', 'created_at', 'updated_at', 'status',
    'aadhar', 'uan', 'pf_no', 'bank_acc', 'ifsc_code', 'android_id',
    'permanent_identity', 'photo', 'signature', 'email', 'office_email',
    'whatsapp_number', 'emergency_numbers', 'office_mobile', 'emg_mobile_no',
    'present_address', 'permanent_address', 'resi_address', 'pass_file',
    'user_log', 'room_log', 'attachment', 'hrms_id',
}


def _format_rows_for_chat(rows: list, max_rows: int = 10, total_count: Optional[int] = None) -> str:
    """Convert rows to readable text for LLM formatting."""
    if not rows:
        return "No data found."
    if len(rows) == 1 and len(rows[0]) == 1:
        k = list(rows[0].keys())[0]
        v = rows[0][k]
        return f"{k}: {'N/A' if v is None else str(v)}"

    limited = rows[:max_rows]
    lines = []
    for i, row in enumerate(limited, 1):
        parts = []
        for k, v in row.items():
            if k.lower() not in _SENSITIVE_COLS and v is not None and str(v).strip() != "":
                label = k.replace('_', ' ').title()
                parts.append(f"{label}: {str(v)}")
        if parts:
            lines.append(f"{i}. " + " | ".join(parts))
            
    actual_total = total_count if total_count is not None else len(rows)
    summary = f"Total count: {actual_total}"
    if actual_total > max_rows:
        summary += f"\n(showing top {max_rows} to avoid text overload. Use 'show list' for full report)"
    return summary + "\n" + "\n".join(lines)


def execute_guided_query(
    flow_id: str,
    slots: dict,
    office_id: int,
    role: str,
    original_question: str = "",
    session_id: str = None,
    base_url: str = "http://localhost:8000",
) -> dict:
    """Execute the final guided query and return formatted result."""
    try:
        # Trainee specific exam flows
        if flow_id == "exam_marks_by_trainee":
            return _exec_exam_marks_by_trainee(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "exam_result_by_trainee":
            return _exec_exam_result_by_trainee(slots, office_id, original_question, session_id, base_url)
            
        # Generic exam flows
        elif flow_id == "failed_trainees":
            return _exec_exam_generic(slots, office_id, original_question, session_id, base_url, result_filter=2, label="Failed Trainees")
        elif flow_id == "passed_trainees":
            return _exec_exam_generic(slots, office_id, original_question, session_id, base_url, result_filter=1, label="Passed Trainees")
        elif flow_id == "not_appeared_trainees":
            return _exec_exam_generic(slots, office_id, original_question, session_id, base_url, result_filter=0, label="Not Appeared Trainees")
        elif flow_id == "re_exam_trainees":
            return _exec_re_exam_trainees(slots, office_id, original_question, session_id, base_url)
            
        # Analytics exam flows
        elif flow_id == "failed_trainees_by_subject":
            return _exec_failed_trainees_by_subject(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "top_performers":
            return _exec_performers(slots, office_id, original_question, session_id, base_url, order="DESC")
        elif flow_id == "lowest_performers":
            return _exec_performers(slots, office_id, original_question, session_id, base_url, order="ASC")
        elif flow_id == "subject_wise_marks_summary":
            return _exec_subject_wise_marks_summary(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "course_exam_summary":
            return _exec_course_exam_summary(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "pass_percentage":
            return _exec_pass_percentage(slots, office_id, original_question, session_id, base_url)
            
        # Non-exam flows
        elif flow_id == "pending_dues_by_person":
            return _exec_pending_dues(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "hostel_room_of_trainee":
            return _exec_hostel_room(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "hostel_availability_occupency":
            return _exec_hostel_availability_occupency(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "attendance_by_trainee":
            return _exec_attendance(slots, office_id, original_question, session_id, base_url)
        else:
            return None
    except Exception as e:
        print(f"[GuidedExecutor] Error executing {flow_id}: {e}")
        return {"type": "text", "message": f"Error retrieving data: {str(e)}"}


def _build_response(rows: list, original_question: str, module: str,
                    office_id: int, session_id: str, base_url: str,
                    force_report: bool = False,
                    total_count: Optional[int] = None) -> dict:
    """Build chat or report response from query rows."""
    row_count = len(rows)
    actual_count = total_count if total_count is not None else row_count
    
    if actual_count == 0:
        return {"type": "text", "message": "No matching records found. For exam queries, this usually means there are no trainees matching this specific filter (e.g. no failed trainees in this course)."}

    mode = "report" if force_report else detect_response_mode(
        user_question=original_question,
        result_type="list" if actual_count > 1 else "single",
        row_count=actual_count,
    )

    if mode == "report" and row_count > 1:
        report = generate_report(
            module_name=module,
            title=f"{module.title()} Report",
            user_question=original_question,
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
        answer = format_answer(original_question, formatted_text)
        return {"type": "text", "message": answer}


# ── Exam Module Executions ───────────────────────────────────────────

def _exec_exam_marks_by_trainee(slots: dict, office_id: int, question: str,
                     session_id: str, base_url: str) -> dict:
    user_id = slots.get("user_id")
    course_id = slots.get("course_id", "ALL")
    exam_type_id = slots.get("exam_type_id", "ALL")
    exam_filter = slots.get("exam_filter", None)

    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT u.name AS trainee_name, c.course_name, tc.course_batch,
                   s.subject_name, em.mark_obtained, em.total_mark,
                   CASE em.result WHEN 1 THEN 'Pass' WHEN 2 THEN 'Fail' ELSE 'Not Appeared' END AS result,
                   et.title AS exam_type, DATE(em.created_at) AS exam_date, em.created_at
            FROM exam_marks em
            JOIN users u ON u.id = em.user_id
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            LEFT JOIN subjects s ON s.id = em.subject_id
            LEFT JOIN exam_type et ON et.id = em.exam_type_id
            WHERE em.user_id = %s AND em.status = 1
        """
        params = [office_id, user_id]

        if course_id != "ALL":
            sql += " AND em.course_id = %s"
            params.append(course_id)
        if exam_type_id != "ALL":
            sql += " AND em.exam_type_id = %s"
            params.append(exam_type_id)

        if exam_filter == "final":
            sql += " AND LOWER(et.title) LIKE '%%final%%'"
        elif exam_filter == "phase_1":
            sql += " AND (LOWER(et.title) LIKE '%%phase 1%%' OR LOWER(et.title) LIKE '%%phase1%%')"
        elif exam_filter == "phase_2":
            sql += " AND (LOWER(et.title) LIKE '%%phase 2%%' OR LOWER(et.title) LIKE '%%phase2%%')"
        elif exam_filter == "re_exam":
            sql += " AND (LOWER(et.title) LIKE '%%re-exam%%' OR LOWER(et.title) LIKE '%%re exam%%' OR LOWER(et.title) LIKE '%%reexam%%')"

        sql += " ORDER BY em.created_at DESC, c.course_name, s.subject_name LIMIT 300"
        cur.execute(sql, params)
        rows = cur.fetchall()
        
        if rows and exam_filter in ["recent", "latest", "last", "current"]:
            latest_exam_type = rows[0].get("exam_type")
            if latest_exam_type:
                rows = [r for r in rows if r.get("exam_type") == latest_exam_type]
            else:
                latest_date = rows[0].get("exam_date")
                rows = [r for r in rows if r.get("exam_date") == latest_date]

        return _build_response(rows, question, "exam", office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_exam_result_by_trainee(slots: dict, office_id: int, question: str,
                                 session_id: str, base_url: str) -> dict:
    # Just an alias to marks flow for now, since it returns 'result' column too
    return _exec_exam_marks_by_trainee(slots, office_id, question, session_id, base_url)


def _build_exam_date_filter(slots, alias="em"):
    """
    Build date filter from slots: year, date_range, from_date, to_date, date.
    Returns (sql_where, params)
    """
    date = slots.get("date")
    year = slots.get("year")
    date_range = slots.get("date_range") or slots.get("exam_filter")
    
    # Try year first (e.g. '2023')
    if year:
        return f" AND YEAR({alias}.created_at) = %s", [year]
        
    # Try date range (e.g. 'last year', 'last month', 'past 4 months')
    if date_range:
        dr = str(date_range).lower()
        if "last year" in dr or "past year" in dr or "previous year" in dr:
            return f" AND YEAR({alias}.created_at) = YEAR(CURDATE()) - 1", []
        if "this year" in dr or "current year" in dr:
            return f" AND YEAR({alias}.created_at) = YEAR(CURDATE())", []
        if "last month" in dr or "past month" in dr or "previous month" in dr:
            return f" AND {alias}.created_at >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)", []
        import re
        m = re.search(r"past\s+(\d+)\s+month", dr)
        if m:
            return f" AND {alias}.created_at >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)", [int(m.group(1))]
        if "last 30 days" in dr:
            return f" AND {alias}.created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)", []
            
    # Explicit from/to
    from_date = slots.get("from_date")
    to_date = slots.get("to_date")
    if from_date and to_date:
        return f" AND DATE({alias}.created_at) BETWEEN %s AND %s", [from_date, to_date]
    if from_date:
        return f" AND DATE({alias}.created_at) >= %s", [from_date]
    if to_date:
        return f" AND DATE({alias}.created_at) <= %s", [to_date]
        
    # Explicit single date
    if date:
        return f" AND DATE({alias}.created_at) = %s", [date]
        
    return "", []


def _exec_exam_generic(slots: dict, office_id: int, question: str,
                       session_id: str, base_url: str, result_filter: int, label: str) -> dict:
    course_id = slots.get("course_id", "ALL")
    date_sql, date_params = _build_exam_date_filter(slots, "em")

    conn = get_connection()
    try:
        cur = conn.cursor()
        
        # Get total count first before LIMIT
        count_sql = """
            SELECT COUNT(em.id) AS cnt
            FROM exam_marks em
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE em.result = %s AND em.status = 1
        """
        params = [office_id, result_filter]
        if course_id != "ALL":
            count_sql += " AND em.course_id = %s"
            params.append(course_id)
        
        count_sql += date_sql
        params.extend(date_params)
            
        cur.execute(count_sql, params)
        count_row = cur.fetchone()
        total_count = count_row.get('cnt', 0) if count_row else 0
        
        sql = """
            SELECT u.name AS trainee_name, c.course_name, tc.course_batch,
                   s.subject_name, em.mark_obtained, em.total_mark,
                   et.title AS exam_type
            FROM exam_marks em
            JOIN users u ON u.id = em.user_id
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            LEFT JOIN subjects s ON s.id = em.subject_id
            LEFT JOIN exam_type et ON et.id = em.exam_type_id
            WHERE em.result = %s AND em.status = 1
        """
        params = [office_id, result_filter]

        if course_id != "ALL":
            sql += " AND em.course_id = %s"
            params.append(course_id)

        sql += date_sql
        params.extend(date_params)

        sql += " ORDER BY em.created_at DESC, c.course_name, s.subject_name LIMIT 500"
        cur.execute(sql, params)
        rows = cur.fetchall()
        
        return _build_response(rows, question, "exam", office_id, session_id, base_url, total_count=total_count)
    finally:
        conn.close()


def _exec_failed_trainees_by_subject(slots: dict, office_id: int, question: str,
                                     session_id: str, base_url: str) -> dict:
    course_id = slots.get("course_id", "ALL")
    date_sql, date_params = _build_exam_date_filter(slots, "em")
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT c.course_name, s.subject_name, COUNT(em.id) AS fail_count
            FROM exam_marks em
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            JOIN subjects s ON s.id = em.subject_id
            WHERE em.result = 2 AND em.status = 1
        """
        params = [office_id]
        if course_id != "ALL":
            sql += " AND em.course_id = %s"
            params.append(course_id)
            
        sql += date_sql
        params.extend(date_params)
            
        sql += " GROUP BY c.course_name, s.subject_name ORDER BY fail_count DESC LIMIT 50"
        cur.execute(sql, params)
        rows = cur.fetchall()
        
        # If "All courses" is selected, force a report so the user can see the full course-wise breakdown
        force_report = (course_id == "ALL" and len(rows) > 1)
        
        return _build_response(rows, question, "exam", office_id, session_id, base_url, force_report=force_report)
    finally:
        conn.close()


def _exec_performers(slots: dict, office_id: int, question: str,
                     session_id: str, base_url: str, order: str) -> dict:
    course_id = slots.get("course_id", "ALL")
    limit = slots.get("limit", 5)
    if limit is None or limit > 100:
        limit = 5
    date_sql, date_params = _build_exam_date_filter(slots, "em")

    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = f"""
            SELECT u.name AS trainee_name, c.course_name, tc.course_batch,
                   s.subject_name, em.mark_obtained, em.total_mark,
                   CASE WHEN em.total_mark > 0 THEN (CAST(em.mark_obtained AS DECIMAL(10,2)) / em.total_mark * 100) ELSE 0 END AS percentage,
                   et.title AS exam_type
            FROM exam_marks em
            JOIN users u ON u.id = em.user_id
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            LEFT JOIN subjects s ON s.id = em.subject_id
            LEFT JOIN exam_type et ON et.id = em.exam_type_id
            WHERE em.status = 1 AND em.result = 1
              AND em.mark_obtained REGEXP '^[0-9]+([.][0-9]+)?$'
        """
        params = [office_id]

        if course_id != "ALL":
            sql += " AND em.course_id = %s"
            params.append(course_id)
            
        sql += date_sql
        params.extend(date_params)

        sql += f" ORDER BY percentage {order}, CAST(em.mark_obtained AS DECIMAL(10,2)) {order} LIMIT %s"
        params.append(limit)
        cur.execute(sql, params)
        rows = cur.fetchall()
        
        # Round percentages
        for r in rows:
            if r.get("percentage") is not None:
                r["percentage"] = round(float(r["percentage"]), 2)
                
        return _build_response(rows, question, "exam", office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_subject_wise_marks_summary(slots: dict, office_id: int, question: str,
                                     session_id: str, base_url: str) -> dict:
    course_id = slots.get("course_id", "ALL")
    date_sql, date_params = _build_exam_date_filter(slots, "em")
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT c.course_name, tc.course_batch, s.subject_name,
                   AVG(CAST(em.mark_obtained AS DECIMAL(10,2))) AS average_marks,
                   MAX(CAST(em.mark_obtained AS DECIMAL(10,2))) AS highest_marks,
                   MIN(CAST(em.mark_obtained AS DECIMAL(10,2))) AS lowest_marks,
                   COUNT(em.id) AS students_appeared
            FROM exam_marks em
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            JOIN subjects s ON s.id = em.subject_id
            WHERE em.status = 1 AND em.result IN (1, 2)
              AND em.mark_obtained REGEXP '^[0-9]+([.][0-9]+)?$'
        """
        params = [office_id]
        if course_id != "ALL":
            sql += " AND em.course_id = %s"
            params.append(course_id)
            
        sql += date_sql
        params.extend(date_params)
            
        sql += " GROUP BY c.course_name, tc.course_batch, s.subject_name ORDER BY c.course_name, s.subject_name LIMIT 500"
        cur.execute(sql, params)
        rows = cur.fetchall()
        
        for r in rows:
            if r.get("average_marks") is not None:
                r["average_marks"] = round(float(r["average_marks"]), 2)
                
        return _build_response(rows, question, "exam", office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_course_exam_summary(slots: dict, office_id: int, question: str,
                              session_id: str, base_url: str) -> dict:
    date_sql, date_params = _build_exam_date_filter(slots, "em")
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT c.course_name, tc.course_batch,
                   COUNT(em.id) AS total_records,
                   SUM(CASE WHEN em.result = 1 THEN 1 ELSE 0 END) AS passed,
                   SUM(CASE WHEN em.result = 2 THEN 1 ELSE 0 END) AS failed,
                   SUM(CASE WHEN em.result = 0 THEN 1 ELSE 0 END) AS not_appeared
            FROM exam_marks em
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE em.status = 1
        """
        params = [office_id]
        
        sql += date_sql
        params.extend(date_params)
        
        sql += " GROUP BY c.course_name, tc.course_batch ORDER BY c.course_name LIMIT 500"
        cur.execute(sql, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "exam", office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_re_exam_trainees(slots: dict, office_id: int, question: str,
                           session_id: str, base_url: str) -> dict:
    course_id = slots.get("course_id", "ALL")
    date_sql, date_params = _build_exam_date_filter(slots, "em")
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        count_sql = """
            SELECT COUNT(em.id) AS cnt
            FROM exam_marks em
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            LEFT JOIN exam_type et ON et.id = em.exam_type_id
            WHERE em.status = 1 AND (LOWER(et.title) LIKE '%%re-exam%%' OR LOWER(et.title) LIKE '%%re exam%%' OR em.re_exam_mark IS NOT NULL)
        """
        params = [office_id]
        if course_id != "ALL":
            count_sql += " AND em.course_id = %s"
            params.append(course_id)
            
        count_sql += date_sql
        params.extend(date_params)
            
        cur.execute(count_sql, params)
        count_row = cur.fetchone()
        total_count = count_row.get('cnt', 0) if count_row else 0
        
        sql = """
            SELECT u.name AS trainee_name, c.course_name, tc.course_batch,
                   s.subject_name, em.re_exam_mark,
                   CASE em.re_exam_result WHEN 1 THEN 'Pass' WHEN 2 THEN 'Fail' ELSE 'Pending' END AS re_exam_result,
                   et.title AS exam_type
            FROM exam_marks em
            JOIN users u ON u.id = em.user_id
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            LEFT JOIN subjects s ON s.id = em.subject_id
            LEFT JOIN exam_type et ON et.id = em.exam_type_id
            WHERE em.status = 1 AND (LOWER(et.title) LIKE '%%re-exam%%' OR LOWER(et.title) LIKE '%%re exam%%' OR em.re_exam_mark IS NOT NULL)
        """
        params = [office_id]
        if course_id != "ALL":
            sql += " AND em.course_id = %s"
            params.append(course_id)

        sql += date_sql
        params.extend(date_params)

        sql += " ORDER BY c.course_name, u.name LIMIT 500"
        cur.execute(sql, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "exam", office_id, session_id, base_url, total_count=total_count)
    finally:
        conn.close()


def _exec_pass_percentage(slots: dict, office_id: int, question: str,
                          session_id: str, base_url: str) -> dict:
    course_id = slots.get("course_id", "ALL")
    date_sql, date_params = _build_exam_date_filter(slots, "em")
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT c.course_name, tc.course_batch,
                   SUM(CASE WHEN em.result = 1 THEN 1 ELSE 0 END) AS passed,
                   SUM(CASE WHEN em.result IN (1, 2) THEN 1 ELSE 0 END) AS total_appeared,
                   CASE WHEN SUM(CASE WHEN em.result IN (1, 2) THEN 1 ELSE 0 END) > 0 
                        THEN (SUM(CASE WHEN em.result = 1 THEN 1 ELSE 0 END) / SUM(CASE WHEN em.result IN (1, 2) THEN 1 ELSE 0 END) * 100) 
                        ELSE 0 END AS pass_percentage
            FROM exam_marks em
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE em.status = 1
        """
        params = [office_id]
        if course_id != "ALL":
            sql += " AND em.course_id = %s"
            params.append(course_id)
            
        sql += date_sql
        params.extend(date_params)
            
        sql += " GROUP BY c.course_name, tc.course_batch ORDER BY c.course_name LIMIT 500"
        cur.execute(sql, params)
        rows = cur.fetchall()
        
        for r in rows:
            if r.get("pass_percentage") is not None:
                r["pass_percentage"] = round(float(r["pass_percentage"]), 2)
                
        return _build_response(rows, question, "exam", office_id, session_id, base_url)
    finally:
        conn.close()


# ── Pending Dues ────────────────────────────────────────────────────

def _exec_pending_dues(slots: dict, office_id: int, question: str,
                       session_id: str, base_url: str) -> dict:
    user_id = slots.get("user_id")
    dues_type = slots.get("dues_type", "ALL")

    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT u.name AS trainee_name, c.course_name, tc.course_batch,
                   ad.hostel AS hostel_dues, ad.mess AS mess_dues,
                   ad.library AS library_dues, ad.sports AS sports_dues
            FROM all_dues ad
            JOIN training_calendars tc ON tc.id = ad.course_id
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            JOIN tra_masters tm ON tm.course_id = tc.id AND tm.user_id = %s AND tm.status = 1
            JOIN users u ON u.id = tm.user_id
            WHERE ad.status = 1
        """
        params = [office_id, user_id]
        sql += " ORDER BY tc.from_date DESC LIMIT 50"
        cur.execute(sql, params)
        rows = cur.fetchall()

        # Filter by dues type if specified
        if dues_type != "ALL" and rows:
            col_map = {"hostel": "hostel_dues", "mess": "mess_dues", "library": "library_dues"}
            col = col_map.get(dues_type)
            if col:
                rows = [r for r in rows if r.get(col) and str(r.get(col)) not in ("0", "None", "")]

        return _build_response(rows, question, "dues", office_id, session_id, base_url)
    finally:
        conn.close()


# ── Hostel Room ─────────────────────────────────────────────────────

def _exec_hostel_room(slots: dict, office_id: int, question: str,
                      session_id: str, base_url: str) -> dict:
    user_id = slots.get("user_id")
    stay_filter = slots.get("stay_filter", "current")

    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT u.name AS trainee_name, hb.building_name, hr.room_name,
                   hm.in_date, hm.out_date,
                   CASE WHEN (hm.h_status = 1 OR hm.h_status = '1') THEN 'Currently Staying' ELSE 'Checked Out' END AS stay_status
            FROM hostel_masters hm
            JOIN users u ON u.id = hm.user_id
            JOIN hostel_buildings hb ON hb.id = hm.building_id
            JOIN hostel_rooms hr ON hr.id = hm.room_id
            WHERE hm.user_id = %s AND hm.office_id = %s
        """
        params = [user_id, office_id]

        if stay_filter == "current":
            sql += " AND (hm.h_status = 1 OR hm.h_status = '1')"

        sql += " ORDER BY hm.in_date DESC LIMIT 20"
        cur.execute(sql, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "hostel", office_id, session_id, base_url)
    finally:
        conn.close()


# ── Hostel Availability ─────────────────────────────────────────────

def _exec_hostel_availability_occupency(slots: dict, office_id: int, question: str,
                              session_id: str, base_url: str) -> dict:
    building_id = slots.get("building_id", "ALL")

    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT
                hb.building_name,
                COUNT(hr.id)                                                        AS total_rooms,
                SUM(hr.room_beds)                                                   AS total_beds,
                COUNT(CASE WHEN ac.occupied_beds > 0 THEN 1 END)                   AS partially_or_fully_occupied_rooms,
                COUNT(hr.id) - COUNT(CASE WHEN ac.occupied_beds > 0 THEN 1 END)    AS fully_empty_rooms,
                COUNT(CASE WHEN ac.occupied_beds IS NULL OR ac.occupied_beds < hr.room_beds THEN 1 END) AS rooms_with_free_beds,
                COALESCE(SUM(ac.occupied_beds), 0)                                 AS occupied_beds,
                SUM(hr.room_beds) - COALESCE(SUM(ac.occupied_beds), 0)             AS available_beds
            FROM hostel_buildings hb
            JOIN hostel_rooms hr
                ON hr.building_id = hb.id
                AND hr.status = 1
            LEFT JOIN (
                SELECT
                    room_id,
                    COUNT(*) AS occupied_beds
                FROM hostel_masters
                WHERE office_id = %s
                  AND (h_status = 1 OR h_status = '1')
                  AND (out_date IS NULL OR out_date >= CURDATE())
                GROUP BY room_id
            ) ac ON ac.room_id = hr.id
            WHERE hb.office_id = %s
              AND hb.status = 1
        """
        params = [office_id, office_id]

        if building_id != "ALL":
            sql += " AND hb.id = %s"
            params.append(building_id)

        sql += " GROUP BY hb.id, hb.building_name"
        cur.execute(sql, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "hostel", office_id, session_id, base_url)
    finally:
        conn.close()


# ── Attendance ──────────────────────────────────────────────────────

def _exec_attendance(slots: dict, office_id: int, question: str,
                     session_id: str, base_url: str) -> dict:
    user_id = slots.get("user_id")
    course_id = slots.get("course_id", "ALL")

    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT u.name AS trainee_name, c.course_name, tc.course_batch,
                   DATE(a.punch_time) AS attendance_date,
                   CASE a.punch
                       WHEN 4 THEN 'Present'
                       WHEN 5 THEN 'Absent'
                       WHEN 1 THEN 'CL'
                       WHEN 2 THEN 'LAP'
                       WHEN 3 THEN 'SL'
                       ELSE CONCAT('Status-', a.punch)
                   END AS attendance_status
            FROM attendances a
            JOIN users u ON u.id = a.user_id AND u.office_id = %s
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.user_id = %s
        """
        params = [office_id, user_id]

        if course_id != "ALL":
            sql += " AND a.course_id = %s"
            params.append(course_id)
        else:
            # Default: last 30 days
            sql += " AND a.punch_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)"

        sql += " ORDER BY a.punch_time DESC LIMIT 500"
        cur.execute(sql, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "attendance", office_id, session_id, base_url)
    finally:
        conn.close()
