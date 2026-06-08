from app.services.db_service import get_connection

def search_meetings(meeting_title: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT id, title, subject, date FROM meeting_create"
        params = []
        if meeting_title:
            query += " AND (title LIKE %s OR subject LIKE %s)"
            params.extend([f"%{meeting_title}%", f"%{meeting_title}%"])
        query += " ORDER BY date DESC LIMIT %s"
        params.append(limit)
        cur.execute(query, params)
        rows = cur.fetchall()
        return [{"label": f"{r['title']} ({r['date']})", "value": r['id'], "meta": {}} for r in rows]
    finally:
        conn.close()

def search_departments(dept_name: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT id, department_name FROM departments WHERE status = 1"
        params = []
        if dept_name:
            query += " AND department_name LIKE %s"
            params.append(f"%{dept_name}%")
        query += " LIMIT %s"
        params.append(limit)
        cur.execute(query, params)
        return [{"label": r["department_name"], "value": r["id"], "meta": {}} for r in cur.fetchall()]
    finally:
        conn.close()
