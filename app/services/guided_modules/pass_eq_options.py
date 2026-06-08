from app.services.db_service import get_connection

def search_pass_trainees(name: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT u.id, u.name_eng FROM users u JOIN pass p ON u.id = p.user_id"
        params = []
        if name:
            query += " AND u.name_eng LIKE %s"
            params.append(f"%{name}%")
        query += " LIMIT %s"
        params.append(limit)
        cur.execute(query, params)
        return [{"label": r['name_eng'], "value": r['id'], "meta": {}} for r in cur.fetchall()]
    finally:
        conn.close()
