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

def execute_master_admin_guided_query(flow_id: str, slots: dict, office_id: int, role: str, session_id: str = None, user_question: str = "", base_url: str = "") -> dict:
    try:
        conn = get_connection()
        cur = conn.cursor()
        if flow_id == "department_list":
            cur.execute("SELECT id, department_name, sort_no FROM departments WHERE status=1 ORDER BY sort_no LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "master_admin", office_id, session_id, base_url)
        elif flow_id == "designation_list":
            query = "SELECT id, desi_name, desi_code FROM designations"
            params = []
            if slots.get("department_id"):
                query += " WHERE office_id=%s"
                params.append(slots.get("department_id"))
            query += " LIMIT 50"
            cur.execute(query, params)
            return _build_response(cur.fetchall(), user_question, "master_admin", office_id, session_id, base_url)
        elif flow_id == "role_list":
            cur.execute("SELECT id, role_name FROM roles WHERE status=1 LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "master_admin", office_id, session_id, base_url)
        elif flow_id == "user_role_summary":
            cur.execute("SELECT r.role_name, COUNT(u.id) as user_count FROM users u JOIN roles r ON u.role_id = r.id WHERE u.status=1 GROUP BY r.role_name LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "master_admin", office_id, session_id, base_url)
        elif flow_id == "railway_zone_list":
            cur.execute("SELECT id, zone_name, zone_code FROM rail_zones WHERE status=1 LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "master_admin", office_id, session_id, base_url)
        elif flow_id == "division_list":
            query = "SELECT id, division, div_code FROM divisions WHERE status=1"
            params = []
            if slots.get("zone_id"):
                query += " AND zone_id=%s"
                params.append(slots.get("zone_id"))
            query += " LIMIT 50"
            cur.execute(query, params)
            return _build_response(cur.fetchall(), user_question, "master_admin", office_id, session_id, base_url)
        elif flow_id == "station_list":
            cur.execute("SELECT id, st_name, st_code FROM rail_stations WHERE status=1 LIMIT 50")
            return _build_response(cur.fetchall(), user_question, "master_admin", office_id, session_id, base_url)
        elif flow_id == "holiday_list":
            return {"type": "text", "message": "Holiday table structure not available or missing data.", "rows": [], "row_count": 0, "response_mode": "chat"}
        elif flow_id == "company_info":
            return {"type": "text", "message": "Company info table structure not available or missing data.", "rows": [], "row_count": 0, "response_mode": "chat"}
        elif flow_id == "master_count_summary":
            cur.execute("SELECT 'Departments' as Entity, COUNT(*) as Count FROM departments WHERE status=1")
            d_count = cur.fetchone()
            cur.execute("SELECT 'Designations' as Entity, COUNT(*) as Count FROM designations")
            de_count = cur.fetchone()
            cur.execute("SELECT 'Roles' as Entity, COUNT(*) as Count FROM roles WHERE status=1")
            r_count = cur.fetchone()
            cur.execute("SELECT 'Users' as Entity, COUNT(*) as Count FROM users WHERE status=1")
            u_count = cur.fetchone()
            return _build_response([d_count, de_count, r_count, u_count], user_question, "master_admin", office_id, session_id, base_url)
        return {"type": "text", "message": "Unknown master admin flow.", "rows": [], "row_count": 0, "response_mode": "chat"}
    finally:
        conn.close()
