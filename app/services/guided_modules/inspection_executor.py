import os
from app.services.db_service import get_connection
from app.services.report_service import generate_report
from app.services.response_mode_service import detect_response_mode

def _build_response(rows: list, question: str, module: str, office_id: int, session_id: str, base_url: str, force_chat: bool = False) -> dict:
    row_count = len(rows)
    response_mode = "chat" if force_chat else detect_response_mode(question, result_type=module, row_count=row_count)
    if response_mode == "report":
        if row_count == 0: return {"type": "text", "message": "No matching records found.", "rows": [], "row_count": 0, "response_mode": "chat"}
        report = generate_report(module_name=module, title=f"{module.capitalize()} Report", user_question=question, rows=rows, office_id=office_id, session_id=session_id)
        return {"type": "text", "message": f"Found {row_count} records. View report: {base_url.rstrip('/') + report['url']}", "report_url": base_url.rstrip('/') + report['url'], "row_count": row_count, "response_mode": "report"}
    else:
        if row_count == 0: return {"type": "text", "message": "No matching records found.", "rows": [], "row_count": 0, "response_mode": "chat"}
        from app.services.llm_service import format_answer
        text = "\n".join([", ".join([f"{k}: {v}" for k, v in r.items()]) for r in rows])
        return {"type": "text", "message": format_answer(question, text), "rows": rows, "row_count": row_count, "response_mode": "chat"}

def execute_inspection_guided_query(flow_id: str, slots: dict, office_id: int, role: str, session_id: str = None, user_question: str = "", base_url: str = "") -> dict:
    try:
        conn = get_connection()
        cur = conn.cursor()
        if flow_id == "inspection_notes":
            cur.execute("SELECT id, title, from_date, to_date, short_desc, created_by FROM inspection_notes ORDER BY from_date DESC LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "inspection", office_id, session_id, base_url)
        elif flow_id == "inspection_details":
            cur.execute("SELECT id, title, from_date, short_desc, created_by FROM inspection_notes WHERE id=%s", (slots.get("inspection_id"),))
            notes = cur.fetchall()
            cur.execute("SELECT description, i_status, remarks FROM inspection_description WHERE status=1 AND insp_id=%s", (slots.get("inspection_id"),))
            obs = cur.fetchall()
            combined = notes + obs
            return _build_response(combined, user_question, "inspection", office_id, session_id, base_url, force_chat=True)
        elif flow_id in ("pending_inspections", "resolved_inspections", "inspection_action_items"):
            status_val = 1 if flow_id == "pending_inspections" else 2 # Guessing 1=pending, 2=resolved
            cur.execute("SELECT i.id, i.description, i.i_status, i.remarks, n.title FROM inspection_description i JOIN inspection_notes n ON i.insp_id = n.id WHERE i.status=1 ORDER BY n.from_date DESC LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "inspection", office_id, session_id, base_url)
        elif flow_id == "inspection_by_department":
            cur.execute("SELECT id, title, from_date, short_desc FROM inspection_notes ORDER BY from_date DESC LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "inspection", office_id, session_id, base_url)
        elif flow_id == "inspection_by_user":
            cur.execute("SELECT id, title, from_date, short_desc, created_by FROM inspection_notes WHERE created_by LIKE %s ORDER BY from_date DESC LIMIT 50", (f"%{slots.get('user_name', '')}%",))
            return _build_response(cur.fetchall(), user_question, "inspection", office_id, session_id, base_url)
        elif flow_id == "inspection_count":
            cur.execute("SELECT COUNT(*) as total_inspections FROM inspection_notes")
            return {"type": "text", "message": f"Total inspections: {cur.fetchone()['total_inspections']}", "rows": [], "row_count": 0, "response_mode": "chat"}
        elif flow_id == "recent_inspections":
            cur.execute("SELECT id, title, from_date, short_desc, created_by FROM inspection_notes ORDER BY from_date DESC LIMIT %s", (slots.get("limit") or 10,))
            return _build_response(cur.fetchall(), user_question, "inspection", office_id, session_id, base_url)
        elif flow_id == "inspection_summary":
            cur.execute("SELECT DATE_FORMAT(from_date, '%Y-%m') as month, COUNT(*) as count FROM inspection_notes GROUP BY month ORDER BY month DESC LIMIT 12")
            return _build_response(cur.fetchall(), user_question, "inspection", office_id, session_id, base_url)
        return {"type": "text", "message": "Unknown inspection flow.", "rows": [], "row_count": 0, "response_mode": "chat"}
    finally:
        conn.close()
