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

def execute_field_study_tour_guided_query(flow_id: str, slots: dict, office_id: int, role: str, session_id: str = None, user_question: str = "", base_url: str = "") -> dict:
    try:
        conn = get_connection()
        cur = conn.cursor()
        if flow_id == "field_training_list":
            cur.execute("SELECT id, from_date, return_date, total_trainee FROM field_training WHERE status=1 ORDER BY from_date DESC LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "field_study_tour", office_id, session_id, base_url)
        elif flow_id == "field_training_by_course":
            cur.execute("SELECT id, from_date, return_date, total_trainee FROM field_training WHERE status=1 AND FIND_IN_SET(%s, course_id) ORDER BY from_date DESC LIMIT 50", (slots.get("course_id"),))
            return _build_response(cur.fetchall(), user_question, "field_study_tour", office_id, session_id, base_url)
        elif flow_id == "study_tour_list":
            cur.execute("SELECT id, from_where, to_where, from_date, return_date, total_trainee FROM study_tour WHERE status=1 ORDER BY from_date DESC LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "field_study_tour", office_id, session_id, base_url)
        elif flow_id == "study_tour_by_course":
            cur.execute("SELECT id, from_where, to_where, from_date, return_date, total_trainee FROM study_tour WHERE status=1 AND FIND_IN_SET(%s, course_id) ORDER BY from_date DESC LIMIT 50", (slots.get("course_id"),))
            return _build_response(cur.fetchall(), user_question, "field_study_tour", office_id, session_id, base_url)
        elif flow_id == "trainee_field_training":
            return {"type": "text", "message": "Trainee specific field training is not explicitly tracked in the current schema.", "rows": [], "row_count": 0, "response_mode": "chat"}
        elif flow_id == "trainee_study_tour":
            return {"type": "text", "message": "Trainee specific study tour is not explicitly tracked in the current schema.", "rows": [], "row_count": 0, "response_mode": "chat"}
        elif flow_id == "field_training_attendance":
            cur.execute("SELECT user_id, attendance FROM filled_training_data WHERE status=1 AND tra_id=%s", (slots.get("field_training_id"),))
            return _build_response(cur.fetchall(), user_question, "field_study_tour", office_id, session_id, base_url)
        elif flow_id == "tour_vehicle_details":
            cur.execute("SELECT bus_num, driver_name, from_where, to_where FROM vehicle_registers WHERE status=1 AND study_id=%s", (slots.get("tour_id"),))
            return _build_response(cur.fetchall(), user_question, "field_study_tour", office_id, session_id, base_url, force_chat=True)
        elif flow_id == "field_study_summary":
            cur.execute("SELECT year, SUM(total_trainee) as trainees FROM study_tour WHERE status=1 GROUP BY year")
            return _build_response(cur.fetchall(), user_question, "field_study_tour", office_id, session_id, base_url)
        elif flow_id == "recent_field_study_activity":
            cur.execute("SELECT 'Study Tour' as type, from_date FROM study_tour WHERE status=1 ORDER BY from_date DESC LIMIT %s", (slots.get("limit") or 10,))
            st = cur.fetchall()
            cur.execute("SELECT 'Field Training' as type, from_date FROM field_training WHERE status=1 ORDER BY from_date DESC LIMIT %s", (slots.get("limit") or 10,))
            ft = cur.fetchall()
            combined = sorted(st + ft, key=lambda x: str(x['from_date']) if x['from_date'] else "", reverse=True)[:(slots.get("limit") or 10)]
            return _build_response(combined, user_question, "field_study_tour", office_id, session_id, base_url)
        return {"type": "text", "message": "Unknown Field/Study Tour flow.", "rows": [], "row_count": 0, "response_mode": "chat"}
    finally:
        conn.close()
