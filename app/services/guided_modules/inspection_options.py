from app.services.db_service import get_connection

def search_inspections(insp_title: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT id, title, from_date FROM inspection_notes"
        params = []
        if insp_title:
            query += " AND title LIKE %s"
            params.append(f"%{insp_title}%")
        query += " ORDER BY from_date DESC LIMIT %s"
        params.append(limit)
        cur.execute(query, params)
        return [{"label": f"{r['title']} ({r['from_date']})", "value": r['id'], "meta": {}} for r in cur.fetchall()]
    finally:
        conn.close()
