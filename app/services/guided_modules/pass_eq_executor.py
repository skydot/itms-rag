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

def execute_pass_eq_guided_query(flow_id: str, slots: dict, office_id: int, role: str, session_id: str = None, user_question: str = "", base_url: str = "") -> dict:
    try:
        conn = get_connection()
        cur = conn.cursor()
        if flow_id == "pass_by_trainee":
            cur.execute("SELECT p.id, p.pass_type, p.out_from, p.out_to FROM pass p WHERE p.user_id=%s", (slots.get("user_id"),))
            return _build_response(cur.fetchall(), user_question, "pass_eq", office_id, session_id, base_url, force_chat=True)
        elif flow_id == "pending_passes":
            cur.execute("SELECT id, pass_type, out_from, out_to FROM pass WHERE c_d IS NULL LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "pass_eq", office_id, session_id, base_url)
        elif flow_id == "issued_passes":
            cur.execute("SELECT id, pass_type, out_from, out_to FROM pass WHERE c_d IS NOT NULL LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "pass_eq", office_id, session_id, base_url)
        elif flow_id == "pass_type_summary":
            cur.execute("SELECT pt.pass_type, COUNT(p.id) as count FROM pass p JOIN pass_type pt ON p.pass_type = pt.id GROUP BY pt.pass_type")
            return _build_response(cur.fetchall(), user_question, "pass_eq", office_id, session_id, base_url)
        elif flow_id == "eq_by_trainee":
            cur.execute("SELECT id, train_no, journey_date, from_place, to_place, pnr FROM eqs WHERE user_id=%s", (slots.get("user_id"),))
            return _build_response(cur.fetchall(), user_question, "pass_eq", office_id, session_id, base_url, force_chat=True)
        elif flow_id == "pending_eqs":
            cur.execute("SELECT id, train_no, journey_date, from_place, to_place FROM eqs WHERE pnr IS NULL OR pnr = '' LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "pass_eq", office_id, session_id, base_url)
        elif flow_id == "train_class_summary":
            return {"type": "text", "message": "Train class summary not available in current schema.", "rows": [], "row_count": 0, "response_mode": "chat"}
        elif flow_id == "station_wise_passes":
            cur.execute("SELECT out_from, COUNT(*) as count FROM pass GROUP BY out_from ORDER BY count DESC LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "pass_eq", office_id, session_id, base_url)
        elif flow_id == "pass_count":
            cur.execute("SELECT COUNT(*) as total_passes FROM pass")
            pass_cnt = cur.fetchone()["total_passes"]
            cur.execute("SELECT COUNT(*) as total_eqs FROM eqs")
            eq_cnt = cur.fetchone()["total_eqs"]
            return {"type": "text", "message": f"Total passes: {pass_cnt}, Total EQs: {eq_cnt}", "rows": [], "row_count": 0, "response_mode": "chat"}
        elif flow_id == "recent_pass_eq_activity":
            cur.execute("SELECT id, 'Pass' as type, out_from, out_to FROM pass ORDER BY id DESC LIMIT %s", (slots.get("limit") or 10,))
            return _build_response(cur.fetchall(), user_question, "pass_eq", office_id, session_id, base_url)
        return {"type": "text", "message": "Unknown Pass/EQ flow.", "rows": [], "row_count": 0, "response_mode": "chat"}
    finally:
        conn.close()
