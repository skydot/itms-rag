from app.services.db_service import get_connection

def search_field_training_courses(course_name: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT id, course_batch FROM training_calendars WHERE status = 1"
        params = []
        if course_name:
            query += " AND course_batch LIKE %s"
            params.append(f"%{course_name}%")
        query += " LIMIT %s"
        params.append(limit)
        cur.execute(query, params)
        return [{"label": r['course_batch'], "value": r['id'], "meta": {}} for r in cur.fetchall()]
    finally:
        conn.close()

def search_tours(tour_name: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT id, from_where, to_where FROM study_tour WHERE status = 1"
        params = []
        query += " LIMIT %s"
        params.append(limit)
        cur.execute(query, params)
        return [{"label": f"{r['from_where']} -> {r['to_where']}", "value": r['id'], "meta": {}} for r in cur.fetchall()]
    finally:
        conn.close()
