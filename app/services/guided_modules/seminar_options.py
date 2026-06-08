from app.services.db_service import get_connection

def search_seminars(seminar_title: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT id, subject, sem_date FROM seminars"
        params = []
        if seminar_title:
            query += " AND subject LIKE %s"
            params.append(f"%{seminar_title}%")
        query += " ORDER BY sem_date DESC LIMIT %s"
        params.append(limit)
        cur.execute(query, params)
        return [{"label": f"{r['subject']} ({r['sem_date']})", "value": r['id'], "meta": {}} for r in cur.fetchall()]
    finally:
        conn.close()
