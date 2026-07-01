"""Library module query templates."""

TEMPLATES = [
    {
        "id": "LIBRARY_TOTAL_BOOKS",
        "module": "library",
        "description": "Number of books count",
        "example_questions": ["How many books in library?", "Count of books"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_BOOK_LIST",
        "module": "library",
        "description": "List and details of all books",
        "example_questions": ["List all books?", "Show books?", "show all library books", "give me a report of all books", "what are all the books"],
        "required_params": [],
        "optional_params": ["office_id", "book_type", "limit"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_BOOKS_BY_TYPE",
        "module": "library",
        "description": "Books by type",
        "example_questions": ["Books by type?", "Show books by category?"],
        "required_params": [],
        "optional_params": ["book_type_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_BOOK_DETAILS",
        "module": "library",
        "description": "Book details by title",
        "example_questions": ["Book details?", "Show book information?"],
        "required_params": [],
        "optional_params": ["book_title", "book_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "detail",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_ISSUED_BOOKS",
        "module": "library",
        "description": "Issued books",
        "example_questions": ["Which books are issued?", "Show issued books?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_RETURNED_BOOKS",
        "module": "library",
        "description": "Returned books",
        "example_questions": ["Returned books?", "Show returned books?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_OVERDUE_BOOKS",
        "module": "library",
        "description": "Overdue books",
        "example_questions": ["Overdue books?", "Which books are overdue?"],
        "required_params": [],
        "optional_params": ["office_id", "due_date"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_BOOKS_ISSUED_TO_TRAINEE",
        "module": "library",
        "description": "Books issued to trainee",
        "example_questions": ["Books issued to trainee?", "What books does trainee have?"],
        "required_params": [],
        "optional_params": ["user_id", "user_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff", "librarian", "trainee"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_ISSUE_COUNT_BY_COURSE",
        "module": "library",
        "description": "Issue count by course",
        "example_questions": ["Issues by course?", "Book issues course-wise?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_BOOK_STOCK",
        "module": "library",
        "description": "Book stock quantity",
        "example_questions": ["Book stock?", "How many copies available?"],
        "required_params": [],
        "optional_params": ["book_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_FINE_SUMMARY",
        "module": "library",
        "description": "Book fine summary",
        "example_questions": ["Library fines?", "Total fines collected?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_BOOKS_BY_AUTHOR",
        "module": "library",
        "description": "Books by author",
        "example_questions": ["Books by author?", "Author-wise books?"],
        "required_params": [],
        "optional_params": ["author_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_BOOKS_PURCHASED",
        "module": "library",
        "description": "Books purchased by date",
        "example_questions": ["Books purchased?", "New book arrivals?"],
        "required_params": [],
        "optional_params": ["from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_AVAILABLE_BOOKS",
        "module": "library",
        "description": "Available books",
        "example_questions": ["Available books?", "Books in stock?"],
        "required_params": [],
        "optional_params": ["office_id", "book_type"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_MOST_ISSUED",
        "module": "library",
        "description": "Most issued books",
        "example_questions": ["Most issued books?", "Popular books?"],
        "required_params": [],
        "optional_params": ["office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "ranking",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_BOOK_TYPE_SUMMARY",
        "module": "library",
        "description": "Book type summary",
        "example_questions": ["Book type summary?", "Books by category count?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_OFFICE_SUMMARY",
        "module": "library",
        "description": "Library office summary",
        "example_questions": ["Library summary?", "Office library stats?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_PENDING_RETURNS",
        "module": "library",
        "description": "Pending returns",
        "example_questions": ["Pending returns?", "Books not returned?"],
        "required_params": [],
        "optional_params": ["office_id", "due_date"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_ISSUE_HISTORY",
        "module": "library",
        "description": "Book issue history",
        "example_questions": ["Issue history?", "Book transaction history?"],
        "required_params": [],
        "optional_params": ["book_id", "user_id", "office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff", "librarian"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "LIBRARY_MODULE_SUMMARY",
        "module": "library",
        "description": "Library module summary",
        "example_questions": ["Library module summary?", "Overall library stats?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute library queries."""
    p = params or {}
    
    if query_id == "LIBRARY_TOTAL_BOOKS":
        cur.execute("SELECT COUNT(*) AS total FROM books WHERE office_id = %s AND status = 1", (office_id,))
        r = cur.fetchone()
        return f"Total books: {r['total'] if r else 0}"

    elif query_id == "LIBRARY_BOOK_LIST":
        cur.execute("SELECT COUNT(*) AS total FROM books WHERE office_id = %s AND status = 1", (office_id,))
        total_r = cur.fetchone()
        total_count = total_r['total'] if total_r else 0

        cur.execute("""
            SELECT b.id, b.title, b.author, bt.book_type AS type,
                   b.qty, b.code, b.price, b.purchase_date
            FROM books b
            JOIN book_type bt ON bt.id = b.book_type
            WHERE b.status = 1 AND b.office_id = %s
            ORDER BY b.title
            LIMIT 500
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No books found in the library."
        lines = [f"- {r['title']} | {r['author']} | Type: {r['type']} | Qty: {r['qty']} | Code: {r['code']}" for r in rows]
        return f"Library Book List (Total: {total_count}):\n" + "\n".join(lines)

    elif query_id == "LIBRARY_BOOKS_BY_TYPE":
        cur.execute("""
            SELECT bt.book_type, COUNT(b.id) AS book_count,
                   SUM(b.qty) AS total_qty
            FROM book_type bt
            LEFT JOIN books b ON b.book_type = bt.id AND b.status = 1 AND b.office_id = %s
            WHERE bt.status = 1
            GROUP BY bt.id, bt.book_type
            ORDER BY book_count DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No book type distribution found."
        lines = [f"- {r['book_type']}: {r['book_count']} Books (Total Qty: {r['total_qty']})" for r in rows]
        return "Books by Type:\n" + "\n".join(lines)

    elif query_id == "LIBRARY_BOOK_DETAILS":
        bid = p.get("book_id")
        title = p.get("book_title")
        if not bid and not title: return "Please specify book_id or book_title."
        
        query = """
            SELECT b.id, b.title, b.author, bt.book_type AS type,
                   b.qty, b.code, b.price, b.purchase_date, b.upload_cover
            FROM books b
            JOIN book_type bt ON bt.id = b.book_type
            WHERE b.status = 1 AND b.office_id = %s
        """
        if bid:
            cur.execute(query + " AND b.id = %s LIMIT 1", (office_id, bid))
        else:
            cur.execute(query + " AND b.title LIKE CONCAT('%%', %s, '%%') LIMIT 1", (office_id, title))
            
        r = cur.fetchone()
        if not r: return "Book details not found."
        return (f"Book Details for '{r['title']}':\n"
                f"Author: {r['author']}\n"
                f"Type: {r['type']}\n"
                f"Code: {r['code']}\n"
                f"Total Quantity: {r['qty']}\n"
                f"Price: {r['price']}\n"
                f"Purchase Date: {r['purchase_date']}")

    elif query_id == "LIBRARY_ISSUED_BOOKS":
        cur.execute("""
            SELECT bi.id, b.title, b.author, bt.book_type AS type,
                   u.name AS issued_to, bi.issue_date, bi.return_date,
                   bi.qty, bi.fine, c.course_name
            FROM book_issue bi
            JOIN books b ON b.id = bi.book_id
            JOIN book_type bt ON bt.id = b.book_type
            JOIN users u ON u.id = bi.user_id
            LEFT JOIN training_calendars tc ON tc.id = bi.course_id
            LEFT JOIN courses c ON c.id = tc.ct_id
            WHERE bi.status = 1 AND b.office_id = %s
            ORDER BY bi.issue_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No currently issued books found."
        lines = [f"- '{r['title']}' to {r['issued_to']} (Issued: {r['issue_date']}, Due: {r['return_date']})" for r in rows]
        return "Currently Issued Books:\n" + "\n".join(lines)

    elif query_id == "LIBRARY_RETURNED_BOOKS":
        cur.execute("""
            SELECT bi.id, b.title, b.author,
                   u.name AS returned_by, bi.issue_date, bi.return_date,
                   bi.fine, c.course_name
            FROM book_issue bi
            JOIN books b ON b.id = bi.book_id
            JOIN users u ON u.id = bi.user_id
            LEFT JOIN training_calendars tc ON tc.id = bi.course_id
            LEFT JOIN courses c ON c.id = tc.ct_id
            WHERE bi.status = 2 AND b.office_id = %s
            ORDER BY bi.return_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No returned books found."
        lines = [f"- '{r['title']}' returned by {r['returned_by']} on {r['return_date']} (Fine: {r['fine']})" for r in rows]
        return "Recently Returned Books:\n" + "\n".join(lines)

    elif query_id == "LIBRARY_OVERDUE_BOOKS":
        cur.execute("""
            SELECT bi.id, b.title, b.author,
                   u.name AS issued_to, u.mobile,
                   bi.issue_date, bi.return_date,
                   DATEDIFF(NOW(), bi.return_date) AS overdue_days,
                   bi.fine
            FROM book_issue bi
            JOIN books b ON b.id = bi.book_id
            JOIN users u ON u.id = bi.user_id
            WHERE bi.status = 1 AND bi.return_date < NOW() AND b.office_id = %s
            ORDER BY overdue_days DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No overdue books found."
        lines = [f"- '{r['title']}' to {r['issued_to']} ({r['mobile']}): Overdue by {r['overdue_days']} days (Due: {r['return_date']})" for r in rows]
        return "Overdue Books:\n" + "\n".join(lines)

    elif query_id == "LIBRARY_BOOKS_ISSUED_TO_TRAINEE":
        uid = p.get("user_id")
        if not uid: return "Please specify user_id."
        cur.execute("""
            SELECT b.title, b.author, bt.book_type AS type,
                   bi.issue_date, bi.return_date, bi.qty, bi.fine, bi.status
            FROM book_issue bi
            JOIN books b ON b.id = bi.book_id
            JOIN book_type bt ON bt.id = b.book_type
            WHERE bi.user_id = %s AND b.office_id = %s
            ORDER BY bi.issue_date DESC
            LIMIT 50
        """, (uid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No books issued to trainee {uid}."
        lines = [f"- '{r['title']}': Status {'Returned' if r['status']==2 else 'Issued'} (Issued: {r['issue_date']}, Due: {r['return_date']})" for r in rows]
        return f"Books Issued to Trainee {uid}:\n" + "\n".join(lines)

    elif query_id == "LIBRARY_ISSUE_COUNT_BY_COURSE":
        cur.execute("""
            SELECT c.course_name, tc.course_batch,
                   COUNT(bi.id) AS total_issued,
                   COUNT(DISTINCT bi.user_id) AS unique_borrowers
            FROM book_issue bi
            JOIN training_calendars tc ON tc.id = bi.course_id
            JOIN courses c ON c.id = tc.ct_id
            JOIN books b ON b.id = bi.book_id
            WHERE bi.status IN (1, 2) AND b.office_id = %s
            GROUP BY bi.course_id, c.course_name, tc.course_batch
            ORDER BY total_issued DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No course-wise issue data found."
        lines = [f"- {r['course_name']} ({r['course_batch']}): {r['total_issued']} Issues ({r['unique_borrowers']} Borrowers)" for r in rows]
        return "Book Issues by Course:\n" + "\n".join(lines)

    elif query_id == "LIBRARY_BOOK_STOCK":
        cur.execute("""
            SELECT b.id, b.title, b.author, bt.book_type AS type,
                   b.qty AS total_qty,
                   COALESCE(SUM(CASE WHEN bi.status=1 THEN bi.qty ELSE 0 END), 0) AS issued_qty,
                   b.qty - COALESCE(SUM(CASE WHEN bi.status=1 THEN bi.qty ELSE 0 END), 0) AS available_qty
            FROM books b
            JOIN book_type bt ON bt.id = b.book_type
            LEFT JOIN book_issue bi ON bi.book_id = b.id
            WHERE b.status = 1 AND b.office_id = %s
            GROUP BY b.id, b.title, b.author, bt.book_type, b.qty
            ORDER BY b.title
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No book stock data found."
        lines = [f"- '{r['title']}': {r['available_qty']} Available (Out of {r['total_qty']} Total, {r['issued_qty']} Issued)" for r in rows]
        return "Library Book Stock:\n" + "\n".join(lines)

    elif query_id == "LIBRARY_FINE_SUMMARY":
        cur.execute("""
            SELECT u.name, u.mobile,
                   SUM(bi.fine) AS total_fine,
                   COUNT(bi.id) AS overdue_count
            FROM book_issue bi
            JOIN users u ON u.id = bi.user_id
            JOIN books b ON b.id = bi.book_id
            WHERE bi.fine > 0 AND b.office_id = %s
            GROUP BY bi.user_id, u.name, u.mobile
            ORDER BY total_fine DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No fines collected/due found."
        lines = [f"- {r['name']} ({r['mobile']}): Total Fine {r['total_fine']} ({r['overdue_count']} incidents)" for r in rows]
        return "Library Fine Summary:\n" + "\n".join(lines)

    elif query_id == "LIBRARY_BOOKS_BY_AUTHOR":
        cur.execute("""
            SELECT b.author,
                   COUNT(b.id) AS book_count,
                   SUM(b.qty) AS total_qty
            FROM books b
            WHERE b.status = 1 AND b.office_id = %s
            GROUP BY b.author
            ORDER BY book_count DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No author-wise data found."
        lines = [f"- {r['author']}: {r['book_count']} Books (Total Qty: {r['total_qty']})" for r in rows]
        return "Books by Author:\n" + "\n".join(lines)

    elif query_id == "LIBRARY_BOOKS_PURCHASED":
        fdate = p.get("from_date")
        tdate = p.get("to_date")
        if not fdate or not tdate: return "Please specify from_date and to_date."
        cur.execute("""
            SELECT b.id, b.title, b.author, bt.book_type AS type,
                   b.qty, b.price, b.purchase_date
            FROM books b
            JOIN book_type bt ON bt.id = b.book_type
            WHERE b.purchase_date BETWEEN %s AND %s
              AND b.status = 1 AND b.office_id = %s
            ORDER BY b.purchase_date DESC
            LIMIT 50
        """, (fdate, tdate, office_id))
        rows = cur.fetchall()
        if not rows: return "No books purchased in this date range."
        lines = [f"- '{r['title']}': Purchased {r['purchase_date']} (Qty: {r['qty']}, Price: {r['price']})" for r in rows]
        return f"Books Purchased ({fdate} to {tdate}):\n" + "\n".join(lines)

    elif query_id == "LIBRARY_AVAILABLE_BOOKS":
        cur.execute("""
            SELECT b.id, b.title, b.author, bt.book_type AS type, b.code,
                   b.qty - COALESCE(SUM(CASE WHEN bi.status=1 THEN bi.qty ELSE 0 END), 0) AS available_qty
            FROM books b
            JOIN book_type bt ON bt.id = b.book_type
            LEFT JOIN book_issue bi ON bi.book_id = b.id
            WHERE b.status = 1 AND b.office_id = %s
            GROUP BY b.id, b.title, b.author, bt.book_type, b.code, b.qty
            HAVING available_qty > 0
            ORDER BY b.title
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No available books found."
        lines = [f"- '{r['title']}' by {r['author']}: {r['available_qty']} Copies Available" for r in rows]
        return "Available Books:\n" + "\n".join(lines)

    elif query_id == "LIBRARY_MOST_ISSUED":
        cur.execute("""
            SELECT b.title, b.author, COUNT(bi.id) AS issue_count
            FROM book_issue bi
            JOIN books b ON b.id = bi.book_id
            WHERE b.status = 1 AND b.office_id = %s
            GROUP BY bi.book_id, b.title, b.author
            ORDER BY issue_count DESC
            LIMIT 10
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No issue data found."
        lines = [f"- '{r['title']}' by {r['author']}: {r['issue_count']} Times Issued" for r in rows]
        return "Most Issued Books (Top 10):\n" + "\n".join(lines)

    elif query_id == "LIBRARY_BOOK_TYPE_SUMMARY":
        cur.execute("""
            SELECT bt.book_type, COUNT(b.id) AS books, SUM(b.qty) AS qty
            FROM book_type bt
            LEFT JOIN books b ON b.book_type = bt.id AND b.status = 1 AND b.office_id = %s
            WHERE bt.status = 1
            GROUP BY bt.id, bt.book_type
            ORDER BY books DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No book type summary found."
        lines = [f"- {r['book_type']}: {r['books']} Book Titles, {r['qty'] or 0} Total Copies" for r in rows]
        return "Book Type Summary:\n" + "\n".join(lines)

    elif query_id == "LIBRARY_OFFICE_SUMMARY":
        cur.execute("""
            SELECT b.office_id, COUNT(b.id) AS total_books, SUM(b.qty) AS total_qty
            FROM books b
            WHERE b.status = 1 AND b.office_id = %s
            GROUP BY b.office_id
        """, (office_id,))
        r = cur.fetchone()
        if not r: return "No office summary found."
        return f"Library Office {office_id} Summary: {r['total_books']} Book Titles, {r['total_qty']} Total Copies"

    elif query_id == "LIBRARY_PENDING_RETURNS":
        cur.execute("""
            SELECT bi.id, b.title, b.author,
                   u.name AS issued_to, u.mobile,
                   bi.issue_date, bi.return_date,
                   DATEDIFF(NOW(), bi.return_date) AS overdue_days
            FROM book_issue bi
            JOIN books b ON b.id = bi.book_id
            JOIN users u ON u.id = bi.user_id
            WHERE bi.status = 1 AND b.office_id = %s
            ORDER BY bi.return_date
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No pending returns found."
        lines = [f"- '{r['title']}' to {r['issued_to']} (Due: {r['return_date']}, Overdue: {r['overdue_days']} days)" for r in rows]
        return "Pending Book Returns:\n" + "\n".join(lines)

    elif query_id == "LIBRARY_ISSUE_HISTORY":
        cur.execute("""
            SELECT bi.id, b.title, b.author,
                   u.name AS issued_to,
                   bi.issue_date, bi.return_date,
                   bi.qty, bi.fine,
                   CASE bi.status WHEN 1 THEN 'Issued' WHEN 2 THEN 'Returned' ELSE 'Other' END AS status_label
            FROM book_issue bi
            JOIN books b ON b.id = bi.book_id
            JOIN users u ON u.id = bi.user_id
            WHERE b.office_id = %s
            ORDER BY bi.issue_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No issue history found."
        lines = [f"- '{r['title']}' to {r['issued_to']}: {r['status_label']} (Issued: {r['issue_date']}, Returned: {r['return_date']})" for r in rows]
        return "Library Issue History:\n" + "\n".join(lines)

    elif query_id == "LIBRARY_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(id) FROM books WHERE status=1 AND office_id=%s) AS total_books,
              (SELECT SUM(qty) FROM books WHERE status=1 AND office_id=%s) AS total_qty,
              (SELECT COUNT(bi.id) FROM book_issue bi JOIN books b ON b.id=bi.book_id WHERE bi.status=1 AND b.office_id=%s) AS currently_issued,
              (SELECT COUNT(bi.id) FROM book_issue bi JOIN books b ON b.id=bi.book_id WHERE bi.status=1 AND bi.return_date < NOW() AND b.office_id=%s) AS overdue_count,
              (SELECT SUM(bi.fine) FROM book_issue bi JOIN books b ON b.id=bi.book_id WHERE bi.fine > 0 AND b.office_id=%s) AS total_fines_collected
        """, (office_id, office_id, office_id, office_id, office_id))
        r = cur.fetchone()
        if not r: return "Could not generate library module summary."
        return (f"Library Module Summary:\n"
                f"Total Book Titles: {r['total_books']}\n"
                f"Total Physical Copies: {r['total_qty']}\n"
                f"Currently Issued: {r['currently_issued']}\n"
                f"Overdue Returns: {r['overdue_count']}\n"
                f"Total Fines Collected: {r['total_fines_collected']}")

    return None
