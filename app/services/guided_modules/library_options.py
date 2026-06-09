from app.services.db_service import get_connection

def search_library_trainees_by_name(name: str, office_id: int, limit: int = 1000) -> list[dict]:
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

def search_books_by_title(title: str, office_id: int, limit: int = 1000) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT id, title, code, author
            FROM books
            WHERE title LIKE %s AND office_id = %s AND status = 1
            LIMIT %s
        """
        like_title = f"%{title}%"
        cur.execute(query, (like_title, office_id, limit))
        rows = cur.fetchall()
        
        options = []
        for r in rows:
            author_str = f" by {r['author']}" if r['author'] else ""
            label = f"{r['title']}{author_str} (Acc No: {r['code']})"
            options.append({
                "label": label,
                "value": r["id"],
                "meta": {"book_id": r["id"]}
            })
        return options
    finally:
        conn.close()

def get_book_types(office_id: int) -> list[dict]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT id, book_type
            FROM book_type
            WHERE office_id = %s AND status = 1
        """
        cur.execute(query, (office_id,))
        rows = cur.fetchall()
        
        options = []
        for r in rows:
            options.append({
                "label": r["book_type"],
                "value": r["id"],
                "meta": {"book_type_id": r["id"]}
            })
        return options
    finally:
        conn.close()

def get_library_status_options() -> list[dict]:
    return [
        {"label": "Available", "value": "available"},
        {"label": "Issued", "value": "issued"},
        {"label": "Overdue", "value": "overdue"},
        {"label": "Pending Return", "value": "pending"}
    ]
