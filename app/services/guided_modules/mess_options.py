from app.services.db_service import get_connection

def search_mess_trainees_by_name(name: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT u.id, u.name, u.user_code, tc.course_batch
            FROM users u
            JOIN tra_masters tm ON tm.user_id = u.id AND tm.status = 1
            JOIN training_calendars tc ON tc.id = tm.course_id AND tc.status = 1
            WHERE u.name LIKE %s AND u.office_id = %s AND u.status = 1
            LIMIT %s
        """
        like_name = f"%{name}%"
        cur.execute(query, (like_name, office_id, limit))
        rows = cur.fetchall()
        
        options = []
        for r in rows:
            label = f"{r['name']} - {r['course_batch']} ({r['user_code']})"
            options.append({
                "label": label,
                "value": r["id"],
                "meta": {"user_id": r["id"]}
            })
        return options
    finally:
        conn.close()

def search_mess_courses(course_name: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT c.id, c.course_name
            FROM courses c
            WHERE c.course_name LIKE %s AND c.office_id = %s AND c.status = 1
            LIMIT %s
        """
        like_name = f"%{course_name}%"
        cur.execute(query, (like_name, office_id, limit))
        rows = cur.fetchall()
        
        options = []
        for r in rows:
            options.append({
                "label": r["course_name"],
                "value": r["id"],
                "meta": {"course_id": r["id"]}
            })
        return options
    finally:
        conn.close()

def search_mess_items(item_name: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT id, item_name, units
            FROM mess_material
            WHERE item_name LIKE %s AND status = 1
            LIMIT %s
        """
        like_name = f"%{item_name}%"
        cur.execute(query, (like_name, limit))
        rows = cur.fetchall()
        
        options = []
        for r in rows:
            options.append({
                "label": f"{r['item_name']} ({r['units']})",
                "value": r["id"],
                "meta": {"item_id": r["id"]}
            })
        return options
    finally:
        conn.close()

def search_mess_parties(party_name: str, office_id: int, limit: int = 10) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT id, p_name, p_mobile
            FROM partys
            WHERE p_name LIKE %s AND office_id = %s AND status = 1
            LIMIT %s
        """
        like_name = f"%{party_name}%"
        cur.execute(query, (like_name, office_id, limit))
        rows = cur.fetchall()
        
        options = []
        for r in rows:
            options.append({
                "label": f"{r['p_name']} ({r['p_mobile']})",
                "value": r["id"],
                "meta": {"party_id": r["id"]}
            })
        return options
    finally:
        conn.close()

def get_mess_month_options() -> list[dict]:
    return [
        {"label": "January", "value": "1"},
        {"label": "February", "value": "2"},
        {"label": "March", "value": "3"},
        {"label": "April", "value": "4"},
        {"label": "May", "value": "5"},
        {"label": "June", "value": "6"},
        {"label": "July", "value": "7"},
        {"label": "August", "value": "8"},
        {"label": "September", "value": "9"},
        {"label": "October", "value": "10"},
        {"label": "November", "value": "11"},
        {"label": "December", "value": "12"}
    ]

def get_mess_due_status_options() -> list[dict]:
    return [
        {"label": "Pending/Unpaid", "value": "pending"},
        {"label": "Paid/Cleared", "value": "paid"},
        {"label": "All", "value": "all"}
    ]
