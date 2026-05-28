"""Complaint query executor — runs final parameterized SQL for complaint guided flows.

Uses existing response_mode_service and report_service for output formatting.
"""

from typing import Dict, Optional
from app.services.db_service import get_connection
from app.services.response_mode_service import detect_response_mode
from app.services.report_service import generate_report
from app.services.llm_service import format_answer


# Sensitive columns to strip from chat output
_SENSITIVE_COLS = {
    'id', 'user_id', 'cm_id', 'building_id', 'office_id', 'password',
    'created_by', 'updated_by', 'created_at', 'updated_at', 'status', 'cm_status',
    'aadhar', 'uan', 'pf_no', 'bank_acc', 'ifsc_code', 'android_id',
    'permanent_identity', 'photo', 'signature', 'email', 'office_email',
    'whatsapp_number', 'emergency_numbers', 'office_mobile', 'emg_mobile_no',
    'present_address', 'permanent_address', 'resi_address', 'pass_file',
    'user_log', 'room_log', 'attachment', 'hrms_id',
}


def _clean_val(v):
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


def execute_complaint_guided_query(
    flow_id: str,
    slots: dict,
    office_id: int,
    role: str,
    session_id: str = None,
    user_question: str = "",
    base_url: str = "http://localhost:8000",
) -> dict:
    """Execute the final guided query and return formatted result."""
    try:
        print(f"[Complaint Guided] Executing: {flow_id} with slots: {slots}")
        handler = {
            "pending_complaints": _exec_pending_complaints,
            "resolved_complaints": _exec_resolved_complaints,
            "complaint_status_summary": _exec_complaint_status_summary,
            "complaints_by_category": _exec_complaints_by_category,
            "complaints_by_trainee": _exec_complaints_by_trainee,
            "complaint_details_by_id": _exec_complaint_details_by_id,
            "department_wise_complaints": _exec_department_wise_complaints,
            "recent_complaints": _exec_recent_complaints,
            "overdue_complaints": _exec_overdue_complaints,
            "complaint_count": _exec_complaint_count,
        }.get(flow_id)
        if not handler:
            return None
        return handler(slots, office_id, user_question, session_id, base_url)
    except Exception as e:
        print(f"[Complaint Guided] Error executing {flow_id}: {e}")
        return {"type": "text", "message": f"Error retrieving complaint data: {str(e)}"}


def _build_response(rows, question, office_id, session_id, base_url,
                     force_report=False, force_chat=False, total_count=None):
    row_count = len(rows)
    actual_count = total_count if total_count is not None else row_count

    if actual_count == 0:
        return {"type": "text", "message": "No matching complaint data found for your request."}

    # "Count" questions trigger chat
    import re
    if not force_report and re.search(r"how\s+many|total|count", question.lower()):
        force_chat = True

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
            module_name="complaint",
            title="Complaint Report",
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


def _resolve_status_sql(status: str) -> str:
    """Resolve user-friendly status to DB cm_status values."""
    if not status or status == "all":
        return ""
    if status == "pending":
        # Usually 0, 1, or 2 for pending/in-progress
        return " AND c.cm_status IN (0, 1, 2)"
    if status == "resolved":
        # Usually 3 or 4 for resolved/closed
        return " AND c.cm_status IN (3, 4)"
    return ""


def _resolve_category_sql(category) -> tuple:
    """Resolve category filter."""
    if not category or str(category).lower() == "all":
        return "", []
        
    if isinstance(category, int) or (isinstance(category, str) and str(category).isdigit()):
        return " AND (c.ctype_id = %s OR c.ctype_sub_id = %s)", [int(category), int(category)]
        
    if isinstance(category, str):
        cat_lower = category.lower()
        if cat_lower == "hostel":
            return " AND c.building_id IS NOT NULL", []
        # Try text search in description/remarks as fallback for broad categories
        return " AND LOWER(c.description) LIKE LOWER(%s)", [f"%{category}%"]
        
    return "", []


# ═══════════════════════════════════════════════════════════════════
# Individual executor handlers
# ═══════════════════════════════════════════════════════════════════

def _exec_pending_complaints(slots, office_id, question, session_id, base_url):
    category = slots.get("complaint_category")
    status_sql = " AND c.cm_status IN (0, 1, 2)"
    cat_sql, params = _resolve_category_sql(category)
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = f"""
            SELECT c.cm_no AS complaint_no, u.name AS raised_by,
                   hb.building_name AS hostel, c.description, c.created_at AS date,
                   CASE 
                     WHEN c.cm_status = 0 THEN 'Pending'
                     WHEN c.cm_status = 1 THEN 'In Progress'
                     WHEN c.cm_status = 2 THEN 'Forwarded'
                     ELSE 'Other'
                   END AS current_status
            FROM complaints c
            LEFT JOIN users u ON u.id = c.user_id
            LEFT JOIN hostel_buildings hb ON hb.id = c.building_id
            WHERE c.office_id = %s AND c.status = 1
              {status_sql}
              {cat_sql}
            ORDER BY c.id DESC LIMIT 300
        """
        cur.execute(sql, [office_id] + params)
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_resolved_complaints(slots, office_id, question, session_id, base_url):
    category = slots.get("complaint_category")
    status_sql = " AND c.cm_status IN (3, 4)"
    cat_sql, params = _resolve_category_sql(category)
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = f"""
            SELECT c.cm_no AS complaint_no, u.name AS raised_by,
                   c.description, c.remarks, c.updated_at AS resolved_date
            FROM complaints c
            LEFT JOIN users u ON u.id = c.user_id
            WHERE c.office_id = %s AND c.status = 1
              {status_sql}
              {cat_sql}
            ORDER BY c.updated_at DESC LIMIT 300
        """
        cur.execute(sql, [office_id] + params)
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_complaint_status_summary(slots, office_id, question, session_id, base_url):
    year = slots.get("year")
    category = slots.get("complaint_category")
    cat_sql, params = _resolve_category_sql(category)
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = f"""
            SELECT 
                CASE 
                    WHEN cm_status IN (0, 1, 2) THEN 'Pending/In-Progress'
                    WHEN cm_status IN (3, 4) THEN 'Resolved/Closed'
                    ELSE 'Other'
                END AS status_group,
                COUNT(id) AS complaint_count
            FROM complaints c
            WHERE c.office_id = %s AND c.status = 1
              {cat_sql}
        """
        p = [office_id] + params
        if year:
            sql += " AND YEAR(c.created_at) = %s"
            p.append(year)
        
        sql += " GROUP BY status_group"
        cur.execute(sql, p)
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_complaints_by_category(slots, office_id, question, session_id, base_url):
    category = slots.get("complaint_category")
    status = slots.get("complaint_status")
    status_sql = _resolve_status_sql(status)
    cat_sql, params = _resolve_category_sql(category)
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = f"""
            SELECT c.cm_no, u.name AS raised_by, c.description, c.created_at,
                   CASE 
                     WHEN c.cm_status IN (0,1,2) THEN 'Pending'
                     WHEN c.cm_status IN (3,4) THEN 'Resolved'
                     ELSE 'Other'
                   END AS status_group
            FROM complaints c
            LEFT JOIN users u ON u.id = c.user_id
            WHERE c.office_id = %s AND c.status = 1
              {status_sql}
              {cat_sql}
            ORDER BY c.id DESC LIMIT 300
        """
        cur.execute(sql, [office_id] + params)
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_complaints_by_trainee(slots, office_id, question, session_id, base_url):
    user_id = slots.get("user_id")
    status = slots.get("complaint_status")
    status_sql = _resolve_status_sql(status)
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = f"""
            SELECT c.cm_no, c.description, c.created_at, c.remarks,
                   CASE 
                     WHEN c.cm_status IN (0,1,2) THEN 'Pending'
                     WHEN c.cm_status IN (3,4) THEN 'Resolved'
                     ELSE 'Other'
                   END AS status_group
            FROM complaints c
            WHERE c.office_id = %s AND c.status = 1 AND c.user_id = %s
              {status_sql}
            ORDER BY c.id DESC LIMIT 100
        """
        cur.execute(sql, (office_id, user_id))
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_complaint_details_by_id(slots, office_id, question, session_id, base_url):
    complaint_id = slots.get("complaint_id")
    if not complaint_id:
        return {"type": "text", "message": "Please provide a valid complaint ID."}
        
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT c.cm_no, c.description, c.remarks, c.created_at, c.updated_at,
                   u.name AS raised_by, hb.building_name AS hostel,
                   CASE 
                     WHEN c.cm_status = 0 THEN 'Pending'
                     WHEN c.cm_status = 1 THEN 'In Progress'
                     WHEN c.cm_status = 2 THEN 'Forwarded'
                     WHEN c.cm_status = 3 THEN 'Resolved'
                     WHEN c.cm_status = 4 THEN 'Closed'
                     ELSE 'Unknown'
                   END AS current_status
            FROM complaints c
            LEFT JOIN users u ON u.id = c.user_id
            LEFT JOIN hostel_buildings hb ON hb.id = c.building_id
            WHERE c.office_id = %s AND (c.id = %s OR c.cm_no = %s)
            LIMIT 1
        """
        # complaint_id might be the numeric id or a numeric cm_no
        cur.execute(sql, (office_id, complaint_id, str(complaint_id)))
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_department_wise_complaints(slots, office_id, question, session_id, base_url):
    year = slots.get("year")
    status = slots.get("complaint_status")
    status_sql = _resolve_status_sql(status)
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        # Fallback to category if departments not strictly linked, 
        sql = f"""
            SELECT cc.comp_name AS category_or_department, COUNT(c.id) AS complaint_count
            FROM complaints c
            JOIN complaint_cat cc ON cc.id = c.ctype_id
            WHERE c.office_id = %s AND c.status = 1
              {status_sql}
        """
        p = [office_id]
        if year:
            sql += " AND YEAR(c.created_at) = %s"
            p.append(year)
            
        sql += " GROUP BY cc.comp_name ORDER BY complaint_count DESC LIMIT 100"
        cur.execute(sql, p)
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_recent_complaints(slots, office_id, question, session_id, base_url):
    limit = slots.get("limit") or 10
    limit = min(limit, 100) # cap
    status = slots.get("complaint_status")
    status_sql = _resolve_status_sql(status)
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = f"""
            SELECT c.cm_no, u.name AS raised_by, c.description, c.created_at,
                   CASE 
                     WHEN c.cm_status IN (0,1,2) THEN 'Pending'
                     WHEN c.cm_status IN (3,4) THEN 'Resolved'
                     ELSE 'Other'
                   END AS status_group
            FROM complaints c
            LEFT JOIN users u ON u.id = c.user_id
            WHERE c.office_id = %s AND c.status = 1
              {status_sql}
            ORDER BY c.id DESC LIMIT %s
        """
        cur.execute(sql, (office_id, limit))
        rows = cur.fetchall()
        
        force_chat = limit <= 5
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=force_chat)
    finally:
        conn.close()


def _exec_overdue_complaints(slots, office_id, question, session_id, base_url):
    days = slots.get("days") or 7
    category = slots.get("complaint_category")
    cat_sql, params = _resolve_category_sql(category)
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = f"""
            SELECT c.cm_no, u.name AS raised_by, c.description, c.created_at,
                   DATEDIFF(CURDATE(), DATE(c.created_at)) AS days_pending
            FROM complaints c
            LEFT JOIN users u ON u.id = c.user_id
            WHERE c.office_id = %s AND c.status = 1
              AND c.cm_status IN (0, 1, 2)
              AND DATEDIFF(CURDATE(), DATE(c.created_at)) >= %s
              {cat_sql}
            ORDER BY days_pending DESC LIMIT 300
        """
        cur.execute(sql, [office_id, days] + params)
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_complaint_count(slots, office_id, question, session_id, base_url):
    year = slots.get("year")
    category = slots.get("complaint_category")
    status = slots.get("complaint_status")
    
    status_sql = _resolve_status_sql(status)
    cat_sql, params = _resolve_category_sql(category)
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = f"""
            SELECT COUNT(c.id) AS total_complaints
            FROM complaints c
            WHERE c.office_id = %s AND c.status = 1
              {status_sql}
              {cat_sql}
        """
        p = [office_id] + params
        if year:
            sql += " AND YEAR(c.created_at) = %s"
            p.append(year)
            
        cur.execute(sql, p)
        rows = cur.fetchall()
        return _build_response(rows, question, office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()
