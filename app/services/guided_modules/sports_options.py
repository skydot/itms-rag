from app.services.db_service import get_connection

def search_sports(sport_name: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT id, program, from_date FROM sport WHERE status = 1"
        params = []
        if sport_name:
            query += " AND program LIKE %s"
            params.append(f"%{sport_name}%")
        query += " ORDER BY from_date DESC LIMIT %s"
        params.append(limit)
        cur.execute(query, params)
        return [{"label": f"{r['program']} ({r['from_date']})", "value": r['id'], "meta": {}} for r in cur.fetchall()]
    finally:
        conn.close()

def search_sport_items(item_name: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT id, sport_item FROM sport_item WHERE status = 1"
        params = []
        if item_name:
            query += " AND sport_item LIKE %s"
            params.append(f"%{item_name}%")
        query += " LIMIT %s"
        params.append(limit)
        cur.execute(query, params)
        return [{"label": r['sport_item'], "value": r['id'], "meta": {}} for r in cur.fetchall()]
    finally:
        conn.close()
