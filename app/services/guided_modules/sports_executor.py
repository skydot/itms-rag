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

def execute_sports_guided_query(flow_id: str, slots: dict, office_id: int, role: str, session_id: str = None, user_question: str = "", base_url: str = "") -> dict:
    try:
        conn = get_connection()
        cur = conn.cursor()
        if flow_id == "sports_events":
            cur.execute("SELECT id, program, from_date, to_date, coordinator FROM sport WHERE status=1 ORDER BY from_date DESC LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "sports", office_id, session_id, base_url)
        elif flow_id == "sports_participants":
            cur.execute("SELECT s.name, s.payment_by, s.receipt_no FROM srec_sport s WHERE s.status=1 LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "sports", office_id, session_id, base_url)
        elif flow_id == "sports_team_details":
            cur.execute("SELECT id, team_name FROM sport_team WHERE status=1 LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "sports", office_id, session_id, base_url)
        elif flow_id == "sports_item_stock":
            cur.execute("SELECT m.item_id, i.sport_item, SUM(m.qty) as total_qty FROM sport_material m JOIN sport_item i ON m.item_id = i.id WHERE m.status=1 GROUP BY m.item_id LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "sports", office_id, session_id, base_url)
        elif flow_id == "sports_item_issues":
            cur.execute("SELECT i.sport_item, si.qty, si.issue_date, si.return_date FROM sportitem_issue si JOIN sport_item i ON si.sitem_id = i.id WHERE si.status=1 LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "sports", office_id, session_id, base_url)
        elif flow_id == "sports_material_summary":
            cur.execute("SELECT m.type, i.sport_item, SUM(m.qty) as total_qty FROM sport_material m JOIN sport_item i ON m.item_id = i.id WHERE m.status=1 GROUP BY m.type, i.sport_item LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "sports", office_id, session_id, base_url)
        elif flow_id == "sports_by_course":
            cur.execute("SELECT course_id, COUNT(*) as count FROM srec_sport WHERE status=1 GROUP BY course_id LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "sports", office_id, session_id, base_url)
        elif flow_id == "sports_count":
            cur.execute("SELECT COUNT(*) as total_events FROM sport WHERE status=1")
            return {"type": "text", "message": f"Total sports events: {cur.fetchone()['total_events']}", "rows": [], "row_count": 0, "response_mode": "chat"}
        elif flow_id == "recent_sports_activity":
            cur.execute("SELECT id, program, from_date, coordinator FROM sport WHERE status=1 ORDER BY from_date DESC LIMIT %s", (slots.get("limit") or 10,))
            return _build_response(cur.fetchall(), user_question, "sports", office_id, session_id, base_url)
        elif flow_id == "sports_winners":
            return {"type": "text", "message": "Winner tracking is not fully implemented in the current schema.", "rows": [], "row_count": 0, "response_mode": "chat"}
        return {"type": "text", "message": "Unknown sports flow.", "rows": [], "row_count": 0, "response_mode": "chat"}
    finally:
        conn.close()
