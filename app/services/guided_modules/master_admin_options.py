from app.services.db_service import get_connection

def search_zones(zone_name: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT id, zone_name FROM rail_zones WHERE status = 1"
        params = []
        if zone_name:
            query += " AND zone_name LIKE %s"
            params.append(f"%{zone_name}%")
        query += " LIMIT %s"
        params.append(limit)
        cur.execute(query, params)
        return [{"label": r['zone_name'], "value": r['id'], "meta": {}} for r in cur.fetchall()]
    finally:
        conn.close()

def search_divisions(div_name: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT id, division FROM divisions WHERE status = 1"
        params = []
        if div_name:
            query += " AND division LIKE %s"
            params.append(f"%{div_name}%")
        query += " LIMIT %s"
        params.append(limit)
        cur.execute(query, params)
        return [{"label": r['division'], "value": r['id'], "meta": {}} for r in cur.fetchall()]
    finally:
        conn.close()

def search_roles(role_name: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT id, role_name FROM roles WHERE status = 1"
        params = []
        if role_name:
            query += " AND role_name LIKE %s"
            params.append(f"%{role_name}%")
        query += " LIMIT %s"
        params.append(limit)
        cur.execute(query, params)
        return [{"label": r['role_name'], "value": r['id'], "meta": {}} for r in cur.fetchall()]
    finally:
        conn.close()
