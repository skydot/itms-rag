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

def execute_meeting_guided_query(flow_id: str, slots: dict, office_id: int, role: str, session_id: str = None, user_question: str = "", base_url: str = "") -> dict:
    try:
        conn = get_connection()
        cur = conn.cursor()
        if flow_id == "upcoming_meetings":
            cur.execute("SELECT id, title, subject, date, start_time, end_time, chairman FROM meeting_create WHERE date >= CURDATE() ORDER BY date ASC LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "meeting", office_id, session_id, base_url)
        elif flow_id == "today_meetings":
            cur.execute("SELECT id, title, subject, start_time, end_time, chairman FROM meeting_create WHERE date = CURDATE() ORDER BY start_time ASC")
            return _build_response(cur.fetchall(), user_question, "meeting", office_id, session_id, base_url, force_chat=True)
        elif flow_id == "meeting_details_by_id":
            cur.execute("SELECT id, title, subject, date, start_time, end_time, description, chairman, invitee FROM meeting_create WHERE id=%s", (slots.get("meeting_id"),))
            return _build_response(cur.fetchall(), user_question, "meeting", office_id, session_id, base_url, force_chat=True)
        elif flow_id == "meeting_agenda":
            cur.execute("SELECT ma.id, ma.type_agenda, mc.title FROM meet_agenda ma JOIN meeting_create mc ON ma.meeting_id = mc.id WHERE ma.meeting_id=%s", (slots.get("meeting_id"),))
            return _build_response(cur.fetchall(), user_question, "meeting", office_id, session_id, base_url)
        elif flow_id == "meeting_by_department":
            # Department linking might not be direct in meeting_create, fallback to all upcoming for now or filter if column exists
            cur.execute("SELECT id, title, subject, date, start_time, end_time FROM meeting_create ORDER BY date DESC LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "meeting", office_id, session_id, base_url)
        elif flow_id == "meeting_participants":
            cur.execute("SELECT invitee, chairman FROM meeting_create WHERE id=%s", (slots.get("meeting_id"),))
            return _build_response(cur.fetchall(), user_question, "meeting", office_id, session_id, base_url, force_chat=True)
        elif flow_id == "past_meetings":
            cur.execute("SELECT id, title, subject, date, start_time, end_time, chairman FROM meeting_create WHERE date < CURDATE() ORDER BY date DESC LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "meeting", office_id, session_id, base_url)
        elif flow_id == "meeting_count":
            cur.execute("SELECT COUNT(*) as total_meetings FROM meeting_create")
            return {"type": "text", "message": f"Total meetings: {cur.fetchone()['total_meetings']}", "rows": [], "row_count": 0, "response_mode": "chat"}
        elif flow_id == "recent_meetings":
            cur.execute("SELECT id, title, subject, date, start_time, end_time, chairman FROM meeting_create ORDER BY date DESC LIMIT %s", (slots.get("limit") or 10,))
            return _build_response(cur.fetchall(), user_question, "meeting", office_id, session_id, base_url)
        elif flow_id == "meeting_calendar_summary":
            cur.execute("SELECT DATE_FORMAT(date, '%Y-%m') as month, COUNT(*) as count FROM meeting_create GROUP BY month ORDER BY month DESC LIMIT 12")
            return _build_response(cur.fetchall(), user_question, "meeting", office_id, session_id, base_url)
        return {"type": "text", "message": "Unknown meeting flow.", "rows": [], "row_count": 0, "response_mode": "chat"}
    finally:
        conn.close()
