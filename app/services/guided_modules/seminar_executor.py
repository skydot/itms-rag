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

def execute_seminar_guided_query(flow_id: str, slots: dict, office_id: int, role: str, session_id: str = None, user_question: str = "", base_url: str = "") -> dict:
    try:
        conn = get_connection()
        cur = conn.cursor()
        if flow_id == "upcoming_seminars":
            cur.execute("SELECT id, subject, sem_date, start_time, end_time, main_speaker FROM seminars WHERE sem_date >= CURDATE() ORDER BY sem_date ASC LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "seminar", office_id, session_id, base_url)
        elif flow_id == "seminar_details":
            cur.execute("SELECT id, subject, sem_date, start_time, end_time, topic_des, main_speaker FROM seminars WHERE id=%s", (slots.get("seminar_id"),))
            return _build_response(cur.fetchall(), user_question, "seminar", office_id, session_id, base_url, force_chat=True)
        elif flow_id == "seminar_topics":
            cur.execute("SELECT s.id, s.subject, st.sub_topic FROM seminars_topic st JOIN seminars s ON st.office_id = s.id WHERE st.status=1 AND s.id=%s", (slots.get("seminar_id"),))
            return _build_response(cur.fetchall(), user_question, "seminar", office_id, session_id, base_url)
        elif flow_id == "seminar_by_faculty":
            # Assuming main_speaker maps to faculty
            cur.execute("SELECT id, subject, sem_date, main_speaker FROM seminars WHERE main_speaker LIKE %s ORDER BY sem_date DESC LIMIT 50", (f"%{slots.get('faculty_name', '')}%",))
            return _build_response(cur.fetchall(), user_question, "seminar", office_id, session_id, base_url)
        elif flow_id == "seminar_by_subject":
            cur.execute("SELECT id, subject, sem_date, main_speaker FROM seminars WHERE subject LIKE %s ORDER BY sem_date DESC LIMIT 50", (f"%{slots.get('subject_name', '')}%",))
            return _build_response(cur.fetchall(), user_question, "seminar", office_id, session_id, base_url)
        elif flow_id == "seminar_participants":
            return {"type": "text", "message": "Participant tracking for seminars is not currently implemented in the database.", "rows": [], "row_count": 0, "response_mode": "chat"}
        elif flow_id == "seminar_count":
            raw_month = str(slots.get("month") or "").strip().lower()
            raw_year = slots.get("year")
            
            months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
            mo = None
            for i, m in enumerate(months, 1):
                if raw_month == m or raw_month == m[:3]:
                    mo = i
                    break
                    
            if mo and raw_year:
                cur.execute("SELECT COUNT(*) as total_seminars FROM seminars WHERE MONTH(sem_date) = %s AND YEAR(sem_date) = %s AND status = 1", (mo, raw_year))
            elif mo:
                cur.execute("SELECT COUNT(*) as total_seminars FROM seminars WHERE MONTH(sem_date) = %s AND status = 1", (mo,))
            elif raw_year:
                cur.execute("SELECT COUNT(*) as total_seminars FROM seminars WHERE YEAR(sem_date) = %s AND status = 1", (raw_year,))
            else:
                cur.execute("SELECT COUNT(*) as total_seminars FROM seminars WHERE status = 1")
                
            return {"type": "text", "message": f"Total seminars: {cur.fetchone()['total_seminars']}", "rows": [], "row_count": 0, "response_mode": "chat"}
        elif flow_id == "recent_seminars":
            cur.execute("SELECT id, subject, sem_date, start_time, end_time, main_speaker FROM seminars ORDER BY sem_date DESC LIMIT %s", (slots.get("limit") or 10,))
            return _build_response(cur.fetchall(), user_question, "seminar", office_id, session_id, base_url)
        elif flow_id == "department_wise_seminars":
            cur.execute("SELECT id, subject, sem_date FROM seminars ORDER BY sem_date DESC LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "seminar", office_id, session_id, base_url)
        elif flow_id == "seminar_summary":
            cur.execute("SELECT DATE_FORMAT(sem_date, '%Y-%m') as month, COUNT(*) as count FROM seminars GROUP BY month ORDER BY month DESC LIMIT 12")
            return _build_response(cur.fetchall(), user_question, "seminar", office_id, session_id, base_url)
        elif flow_id in ("all_seminars", "seminars_by_month", "seminar_by_month"):
            raw_month = str(slots.get("month") or "").strip().lower()
            raw_year = slots.get("year")
            
            months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
            mo = None
            for i, m in enumerate(months, 1):
                if raw_month == m or raw_month == m[:3]:
                    mo = i
                    break
                    
            if mo and raw_year:
                cur.execute("""
                    SELECT id, subject, sem_date, start_time, end_time, judge, main_speaker 
                    FROM seminars 
                    WHERE MONTH(sem_date) = %s AND YEAR(sem_date) = %s AND status = 1 
                    ORDER BY sem_date DESC, start_time LIMIT 50
                """, (mo, raw_year))
            elif mo:
                cur.execute("""
                    SELECT id, subject, sem_date, start_time, end_time, judge, main_speaker 
                    FROM seminars 
                    WHERE MONTH(sem_date) = %s AND status = 1 
                    ORDER BY sem_date DESC, start_time LIMIT 50
                """, (mo,))
            elif raw_year:
                cur.execute("""
                    SELECT id, subject, sem_date, start_time, end_time, judge, main_speaker 
                    FROM seminars 
                    WHERE YEAR(sem_date) = %s AND status = 1 
                    ORDER BY sem_date DESC, start_time LIMIT 50
                """, (raw_year,))
            else:
                cur.execute("""
                    SELECT id, subject, sem_date, start_time, end_time, judge, main_speaker 
                    FROM seminars WHERE status = 1 ORDER BY sem_date DESC, start_time LIMIT 50
                """)
            return _build_response(cur.fetchall(), user_question, "seminar", office_id, session_id, base_url, force_chat=False)
        return {"type": "text", "message": "Unknown seminar flow.", "rows": [], "row_count": 0, "response_mode": "chat"}
    finally:
        conn.close()
