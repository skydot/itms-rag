import os
"""Trainee query executor — runs final parameterized SQL for trainee guided flows.

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


def execute_trainee_guided_query(
    flow_id: str,
    slots: dict,
    office_id: int,
    role: str,
    original_question: str = "",
    session_id: str = None,
    base_url: str = os.getenv("API_BASE_URL", ""),
) -> dict:
    """Execute the final guided query and return formatted result."""
    try:
        print(f"[Trainee Guided] Executing: {flow_id} with slots: {slots}")
        if flow_id == "trainee_profile_by_name":
            return _exec_trainee_profile_by_name(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "active_trainee_count":
            return _exec_active_trainee_count(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "total_trainee_count":
            return _exec_total_trainee_count(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "trainee_joined_by_year":
            return _exec_trainee_joined_by_year(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "trainees_by_course":
            return _exec_trainees_by_course(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "recent_course_trainees":
            return _exec_recent_course_trainees(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "course_wise_trainee_count":
            return _exec_course_wise_trainee_count(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "batch_wise_trainee_count":
            return _exec_batch_wise_trainee_count(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "gender_wise_trainee_count":
            return _exec_gender_wise_trainee_count(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "approved_trainees":
            return _exec_approved_trainees(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "pending_approval_trainees":
            return _exec_pending_approval_trainees(slots, office_id, original_question, session_id, base_url)
        elif flow_id == "outstay_trainees":
            return _exec_outstay_trainees(slots, office_id, original_question, session_id, base_url)
        else:
            return None
    except Exception as e:
        print(f"[Trainee Guided] Error executing {flow_id}: {e}")
        return {"type": "text", "message": f"Error retrieving data: {str(e)}"}


def _build_response(rows: list, original_question: str, module: str,
                    office_id: int, session_id: str, base_url: str,
                    force_report: bool = False,
                    force_chat: bool = False,
                    total_count: Optional[int] = None) -> dict:
    """Build chat or report response from query rows."""
    row_count = len(rows)
    actual_count = total_count if total_count is not None else row_count
    
    if actual_count == 0:
        return {"type": "text", "message": "No matching trainees found for your request."}

    if force_chat:
        mode = "chat"
    elif force_report:
        mode = "report"
    else:
        mode = detect_response_mode(
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


def _exec_trainee_profile_by_name(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    user_id = slots.get("user_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT u.name AS trainee_name, u.user_code, u.gender, u.mobile, u.designation,
                   c.course_name, tc.course_batch, tc.from_date, tc.to_date,
                   tm.role, tm.posted_at, tm.is_approved, tm.out_stay
            FROM users u
            LEFT JOIN tra_masters tm ON tm.user_id = u.id AND tm.status = 1
            LEFT JOIN training_calendars tc ON tc.id = tm.course_id AND tc.status = 1
            LEFT JOIN courses c ON c.id = tc.ct_id
            WHERE u.id = %s AND u.office_id = %s AND u.status = 1
            ORDER BY tc.from_date DESC LIMIT 1
        """
        cur.execute(sql, (user_id, office_id))
        rows = cur.fetchall()
        return _build_response(rows, question, "trainee", office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_active_trainee_count(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT COUNT(tm.id) AS active_trainees
            FROM tra_masters tm 
            LEFT JOIN training_calendars tc ON tc.id = tm.course_id AND tc.status = 1 
            WHERE tc.from_date <= CURDATE()
            AND tc.to_date >= CURDATE() 
            AND tm.office_id = %s 
            AND tm.status = 1 
            AND tm.is_approved = 1
        """
        cur.execute(sql, (office_id,))
        rows = cur.fetchall()
        return _build_response(rows, question, "trainee", office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_total_trainee_count(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT COUNT(tm.id) AS total_trainees
            FROM tra_masters tm 
            WHERE tm.office_id = %s 
        """
        cur.execute(sql, (office_id,))
        rows = cur.fetchall()
        return _build_response(rows, question, "trainee", office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_trainee_joined_by_year(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    year = slots.get("year")
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        date_range = slots.get("date_range") or slots.get("exam_filter")
        date_sql = ""
        date_params = []
        if year and year != "ALL" and str(year).isdigit():
            date_sql += " AND YEAR(tc.from_date) = %s"
            date_params.append(int(year))
        elif date_range:
            dr = str(date_range).lower()
            if "last year" in dr or "past year" in dr or "previous year" in dr:
                date_sql += " AND YEAR(tc.from_date) = YEAR(CURDATE()) - 1"
            elif "this year" in dr or "current year" in dr:
                date_sql += " AND YEAR(tc.from_date) = YEAR(CURDATE())"
            elif "last month" in dr or "past month" in dr or "previous month" in dr:
                date_sql += " AND tc.from_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)"
            elif "last 30 days" in dr:
                date_sql += " AND tc.from_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)"
            else:
                import re
                m = re.search(r"past\s+(\d+)\s+month", dr)
                if m:
                    date_sql += f" AND tc.from_date >= DATE_SUB(CURDATE(), INTERVAL {int(m.group(1))} MONTH)"

        count_sql = f"""
            SELECT COUNT(DISTINCT tm.user_id) AS cnt
            FROM tra_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            WHERE tm.office_id = %s AND tm.status = 1 {date_sql}
        """
        params = [office_id] + date_params
        cur.execute(count_sql, params)
        total_count = cur.fetchone()["cnt"]

        # Get list
        sql = f"""
            SELECT u.name AS trainee_name, u.user_code, u.gender,
                   c.course_name, tc.course_batch, tc.from_date
            FROM tra_masters tm
            JOIN users u ON u.id = tm.user_id
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE tm.office_id = %s AND tm.status = 1 {date_sql}
        """
        params = [office_id] + date_params
        sql += " ORDER BY tc.from_date DESC, u.name LIMIT 500"
        cur.execute(sql, params)
        rows = cur.fetchall()

        # If it's a "how many" question, force chat mode. Otherwise let report_service decide (usually report).
        
        return _build_response(rows, question, "trainee", office_id, session_id, base_url, total_count=total_count)
    finally:
        conn.close()


def _exec_trainees_by_course(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    course_id = slots.get("course_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        count_sql = """
            SELECT COUNT(DISTINCT tm.user_id) AS cnt
            FROM tra_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            WHERE tc.ct_id = %s AND tm.status = 1
        """
        if course_id == "ALL":
            count_sql = """
                SELECT COUNT(DISTINCT tm.user_id) AS cnt
                FROM tra_masters tm
                WHERE tm.status = 1
            """
            cur.execute(count_sql)
        else:
            cur.execute(count_sql, (course_id,))
            
        total_count = cur.fetchone()["cnt"]

        sql = """
            SELECT u.name AS trainee_name, u.user_code, u.gender,
                   c.course_name, tc.course_batch, tc.from_date, tc.to_date
            FROM tra_masters tm
            JOIN users u ON u.id = tm.user_id
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE tm.status = 1
        """
        params = []
        if course_id != "ALL":
            sql += " AND tc.ct_id = %s"
            params.append(course_id)
            
        sql += " ORDER BY u.name LIMIT 500"
        cur.execute(sql, params)
        rows = cur.fetchall()

        return _build_response(rows, question, "trainee", office_id, session_id, base_url, total_count=total_count)
    finally:
        conn.close()


def _exec_recent_course_trainees(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    recent_filter = slots.get("recent_filter", "recent")
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        if recent_filter == "current":
            # Ongoing courses
            course_cond = "tc.from_date <= CURDATE() AND tc.to_date >= CURDATE()"
        else:
            # Latest course by from_date that has trainees
            course_cond = "tc.id = (SELECT tc2.id FROM training_calendars tc2 JOIN tra_masters tm2 ON tm2.course_id = tc2.id WHERE tc2.status = 1 AND tc2.office_id = %s AND tm2.status = 1 ORDER BY tc2.from_date DESC LIMIT 1)"

        count_sql = f"""
            SELECT COUNT(DISTINCT tm.user_id) AS cnt
            FROM tra_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            WHERE tm.office_id = %s AND tm.status = 1 AND {course_cond}
        """
        params = [office_id]
        if recent_filter != "current":
            params = [office_id, office_id]
        cur.execute(count_sql, params)
        total_count = cur.fetchone()["cnt"]

        sql = f"""
            SELECT u.name AS trainee_name, u.user_code, u.gender,
                   c.course_name, tc.course_batch, tc.from_date, tc.to_date
            FROM tra_masters tm
            JOIN users u ON u.id = tm.user_id
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE tm.office_id = %s AND tm.status = 1 AND {course_cond}
            ORDER BY u.name LIMIT 500
        """
        cur.execute(sql, params)
        rows = cur.fetchall()

        
        return _build_response(rows, question, "trainee", office_id, session_id, base_url, total_count=total_count)
    finally:
        conn.close()


def _exec_course_wise_trainee_count(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT c.course_name, COUNT(DISTINCT tm.user_id) AS trainee_count
            FROM tra_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE tm.office_id = %s AND tm.status = 1
            GROUP BY c.course_name
            ORDER BY trainee_count DESC LIMIT 100
        """
        cur.execute(sql, (office_id,))
        rows = cur.fetchall()
        
        # Course-wise usually looks good in chat if it's small, report if it's large.
        return _build_response(rows, question, "trainee", office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_batch_wise_trainee_count(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT c.course_name, tc.course_batch, tc.from_date, COUNT(DISTINCT tm.user_id) AS trainee_count
            FROM tra_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE tm.office_id = %s AND tm.status = 1
            GROUP BY c.course_name, tc.course_batch, tc.from_date
            ORDER BY tc.from_date DESC LIMIT 100
        """
        cur.execute(sql, (office_id,))
        rows = cur.fetchall()
        return _build_response(rows, question, "trainee", office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_gender_wise_trainee_count(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT u.gender, COUNT(DISTINCT tm.user_id) AS count
            FROM tra_masters tm
            JOIN users u ON u.id = tm.user_id
            WHERE tm.office_id = %s AND tm.status = 1
            GROUP BY u.gender
        """
        cur.execute(sql, (office_id,))
        rows = cur.fetchall()
        return _build_response(rows, question, "trainee", office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_approved_trainees(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        count_sql = "SELECT COUNT(DISTINCT user_id) as cnt FROM tra_masters WHERE office_id = %s AND status = 1 AND is_approved = 1"
        cur.execute(count_sql, (office_id,))
        total_count = cur.fetchone()["cnt"]

        sql = """
            SELECT u.name AS trainee_name, u.user_code, c.course_name, tc.course_batch
            FROM tra_masters tm
            JOIN users u ON u.id = tm.user_id
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE tm.office_id = %s AND tm.status = 1 AND tm.is_approved = 1
            ORDER BY u.name LIMIT 500
        """
        cur.execute(sql, (office_id,))
        rows = cur.fetchall()
        
        
        return _build_response(rows, question, "trainee", office_id, session_id, base_url, total_count=total_count)
    finally:
        conn.close()


def _exec_pending_approval_trainees(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        count_sql = "SELECT COUNT(DISTINCT user_id) as cnt FROM tra_masters WHERE office_id = %s AND status = 1 AND (is_approved = 0 OR is_approved IS NULL)"
        cur.execute(count_sql, (office_id,))
        total_count = cur.fetchone()["cnt"]

        sql = """
            SELECT u.name AS trainee_name, u.user_code, c.course_name, tc.course_batch
            FROM tra_masters tm
            JOIN users u ON u.id = tm.user_id
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE tm.office_id = %s AND tm.status = 1 AND (tm.is_approved = 0 OR tm.is_approved IS NULL)
            ORDER BY u.name LIMIT 500
        """
        cur.execute(sql, (office_id,))
        rows = cur.fetchall()
        
        
        return _build_response(rows, question, "trainee", office_id, session_id, base_url, total_count=total_count)
    finally:
        conn.close()


def _exec_outstay_trainees(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        count_sql = "SELECT COUNT(DISTINCT user_id) as cnt FROM tra_masters WHERE office_id = %s AND status = 1 AND out_stay = 1"
        cur.execute(count_sql, (office_id,))
        total_count = cur.fetchone()["cnt"]

        sql = """
            SELECT u.name AS trainee_name, u.user_code, c.course_name, tc.course_batch
            FROM tra_masters tm
            JOIN users u ON u.id = tm.user_id
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE tm.office_id = %s AND tm.status = 1 AND tm.out_stay = 1
            ORDER BY u.name LIMIT 500
        """
        cur.execute(sql, (office_id,))
        rows = cur.fetchall()
        
        
        return _build_response(rows, question, "trainee", office_id, session_id, base_url, total_count=total_count)
    finally:
        conn.close()
