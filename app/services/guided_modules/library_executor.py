from typing import Optional
from app.services.db_service import get_connection
from app.services.response_mode_service import detect_response_mode
from app.services.report_service import generate_report
from app.services.llm_service import format_answer

def _format_rows_for_chat(rows: list, max_rows: int = 10, total_count: Optional[int] = None) -> str:
    if not rows:
        return "No data found."
    if len(rows) == 1 and len(rows[0]) == 1:
        k = list(rows[0].keys())[0]
        v = rows[0][k]
        return f"{k}: {'N/A' if v is None else str(v)}"

    limited = rows[:max_rows]
    lines = []
    for i, row in enumerate(limited, 1):
        parts = []
        for k, v in row.items():
            if v is not None and str(v).strip() != "":
                label = k.replace('_', ' ').title()
                parts.append(f"{label}: {str(v)}")
        if parts:
            lines.append(f"{i}. " + " | ".join(parts))
            
    actual_total = total_count if total_count is not None else len(rows)
    summary = f"Total count: {actual_total}"
    if actual_total > max_rows:
        summary += f"\n(showing top {max_rows} to avoid text overload. Use 'show list' for full report)"
    return summary + "\n" + "\n".join(lines)

def _build_response(rows: list, original_question: str, module: str,
                    office_id: int, session_id: str, base_url: str,
                    force_report: bool = False, force_chat: bool = False,
                    total_count: Optional[int] = None) -> dict:
    row_count = len(rows)
    actual_count = total_count if total_count is not None else row_count
    
    if actual_count == 0:
        return {"type": "text", "message": "No matching records found in the library."}

    if force_chat:
        mode = "chat"
    elif force_report:
        mode = "report"
    else:
        mode = detect_response_mode(
            user_question=original_question,
            result_type="list" if actual_count > 1 else "single",
            row_count=actual_count,
        )

    if mode == "report" and row_count > 1:
        report = generate_report(
            module_name=module,
            title=f"{module.title()} Report",
            user_question=original_question,
            rows=rows,
            office_id=office_id,
            session_id=session_id,
        )
        full_url = base_url.rstrip("/") + report["url"]
        ttl = report["ttl_seconds"]
        if ttl < 60:
            exp = f"{ttl} seconds"
        elif ttl < 3600:
            exp = f"{ttl // 60} minute{'s' if ttl // 60 != 1 else ''}"
        else:
            exp = f"{ttl // 3600} hour{'s' if ttl // 3600 != 1 else ''}"
            
        if total_count and total_count > row_count:
            count_msg = f"Found {total_count} records (showing {report['row_count']} in report)."
        else:
            count_msg = f"Found {report['row_count']} records for your request."
            
        answer = (
            f"{count_msg}\n\n"
            f"Open full report: {full_url}\n\n"
            f"This report link will expire in {exp}."
        )
        return {
            "type": "text",
            "message": answer,
            "report_url": full_url,
            "row_count": report["row_count"],
            "response_mode": "report",
            "expires_at": report["expires_at"],
        }
    else:
        formatted_text = _format_rows_for_chat(rows, total_count=total_count)
        answer = format_answer(original_question, formatted_text)
        return {"type": "text", "message": answer}

def execute_library_guided_query(flow_id: str, slots: dict, office_id: int, role: str, session_id: str = None, user_question: str = "", base_url: str = "http://localhost:8000") -> dict:
    try:
        print(f"[Library Guided] Executing: {flow_id} with slots: {slots}")
        if flow_id == "book_search":
            return _exec_book_search(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "book_availability":
            return _exec_book_availability(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "issued_books_by_trainee":
            return _exec_issued_books_by_trainee(slots, office_id, user_question, session_id, base_url)
        elif flow_id in ("overdue_books", "overdue_books_by_trainee"):
            return _exec_overdue_books(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "book_issue_history":
            return _exec_book_issue_history(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "library_book_count":
            return _exec_library_book_count(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "book_type_summary":
            return _exec_book_type_summary(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "most_issued_books":
            return _exec_most_issued_books(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "recent_book_issues":
            return _exec_recent_book_issues(slots, office_id, user_question, session_id, base_url)
        elif flow_id in ("pending_book_returns", "pending_returns_by_trainee"):
            return _exec_pending_book_returns(slots, office_id, user_question, session_id, base_url)
        else:
            return {"type": "text", "message": "Flow not recognized."}
    except Exception as e:
        print(f"[Library Guided] Error executing {flow_id}: {e}")
        return {"type": "text", "message": f"Error retrieving data: {str(e)}"}

def _exec_book_search(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    book_id = slots.get("book_id")
    book_title = slots.get("book_title")
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT b.title AS book_title, b.author, b.code AS accession_number, bt.book_type, b.qty AS total_quantity
            FROM books b
            LEFT JOIN book_type bt ON b.book_type = bt.id
            WHERE b.office_id = %s AND b.status = 1
        """
        params = [office_id]
        if book_id:
            query += " AND b.id = %s"
            params.append(book_id)
        elif book_title:
            query += " AND b.title LIKE %s"
            params.append(f"%{book_title}%")
        query += " LIMIT 100"
        cur.execute(query, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "library", office_id, session_id, base_url)
    finally:
        conn.close()

def _exec_book_availability(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    book_id = slots.get("book_id")
    book_title = slots.get("book_title")
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        sum_query = """
            SELECT SUM(b.qty) as total_qty, 
                   SUM((SELECT COALESCE(SUM(bi.qty), 0) FROM book_issue bi WHERE bi.book_id = b.id AND bi.status = 1)) as total_issued
            FROM books b
            WHERE b.office_id = %s AND b.status = 1
        """
        sum_params = [office_id]
        if book_id:
            sum_query += " AND b.id = %s"
            sum_params.append(book_id)
        elif book_title:
            sum_query += " AND b.title LIKE %s"
            sum_params.append(f"%{book_title}%")
        
        cur.execute(sum_query, sum_params)
        totals = cur.fetchone()
        overall_total = totals['total_qty'] or 0
        overall_issued = totals['total_issued'] or 0
        overall_available = overall_total - overall_issued
        if overall_available < 0: overall_available = 0

        # total copies vs issued copies where status = 1 (pending)
        query = """
            SELECT b.title AS book_title, b.author, b.code AS accession_number, b.qty AS total_quantity,
                   (SELECT COALESCE(SUM(bi.qty), 0) FROM book_issue bi WHERE bi.book_id = b.id AND bi.status = 1) AS issued_quantity
            FROM books b
            WHERE b.office_id = %s AND b.status = 1
        """
        params = [office_id]
        if book_id:
            query += " AND b.id = %s"
            params.append(book_id)
        elif book_title:
            query += " AND b.title LIKE %s"
            params.append(f"%{book_title}%")
        query += " LIMIT 100"
        cur.execute(query, params)
        rows = cur.fetchall()
        for r in rows:
            r['available_quantity'] = r['total_quantity'] - r['issued_quantity']
            if r['available_quantity'] < 0: r['available_quantity'] = 0
            
        force_report = (not book_id and not book_title and len(rows) > 0) or len(rows) > 10
        resp = _build_response(rows, question, "library", office_id, session_id, base_url, force_report=force_report)
        summary_text = f"Total quantity of matching books: **{overall_total}** (Available: **{overall_available}**, Issued: **{overall_issued}**)."

        
        if resp.get("response_mode") == "report":
            resp["message"] = summary_text + "<br><br>" + resp["message"].replace("\n", "<br>")
        else:
            # For chat mode, we can just prepend it
            if "No matching records found" not in resp["message"]:
                resp["message"] = summary_text + "\n\n" + resp["message"]
                
        return resp
    finally:
        conn.close()

def _exec_issued_books_by_trainee(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    user_id = slots.get("user_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT b.title AS book_title, b.code AS accession_number, bi.issue_date, bi.return_date AS due_date,
                   u.name AS trainee_name, tc.course_batch
            FROM book_issue bi
            JOIN books b ON bi.book_id = b.id
            JOIN users u ON bi.user_id = u.id
            LEFT JOIN training_calendars tc ON bi.course_id = tc.id
            WHERE bi.office_id = %s AND bi.status = 1 AND u.id = %s
        """
        cur.execute(query, (office_id, user_id))
        rows = cur.fetchall()
        return _build_response(rows, question, "library", office_id, session_id, base_url)
    finally:
        conn.close()

def _exec_overdue_books(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    user_id = slots.get("user_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT b.title AS book_title, b.code AS accession_number, bi.issue_date, bi.return_date AS due_date,
                   u.name AS trainee_name, u.mobile AS phone
            FROM book_issue bi
            JOIN books b ON bi.book_id = b.id
            JOIN users u ON bi.user_id = u.id
            WHERE bi.office_id = %s AND bi.status = 1 AND bi.return_date < CURDATE()
        """
        params = [office_id]
        if user_id:
            query += " AND u.id = %s"
            params.append(user_id)
        query += " ORDER BY bi.return_date ASC LIMIT 500"
        cur.execute(query, params)
        rows = cur.fetchall()
        # safe column
        for r in rows:
            if 'phone' in r: del r['phone']
        return _build_response(rows, question, "library", office_id, session_id, base_url)
    finally:
        conn.close()

def _exec_book_issue_history(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    book_id = slots.get("book_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT b.title AS book_title, u.name AS trainee_name, bi.issue_date, bi.return_date AS due_date,
                   CASE WHEN bi.status = 1 THEN 'Pending' WHEN bi.status = 2 THEN 'Returned' ELSE 'Unknown' END AS return_status
            FROM book_issue bi
            JOIN books b ON bi.book_id = b.id
            JOIN users u ON bi.user_id = u.id
            WHERE bi.office_id = %s AND bi.book_id = %s
            ORDER BY bi.issue_date DESC LIMIT 100
        """
        cur.execute(query, (office_id, book_id))
        rows = cur.fetchall()
        return _build_response(rows, question, "library", office_id, session_id, base_url)
    finally:
        conn.close()

def _exec_library_book_count(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT COUNT(id) AS total_books
            FROM books
            WHERE office_id = %s AND status = 1
        """
        cur.execute(query, (office_id,))
        rows = cur.fetchall()
        return _build_response(rows, question, "library", office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()

def _exec_book_type_summary(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT bt.book_type AS category, SUM(b.qty) AS total_quantity, COUNT(b.id) AS total_titles
            FROM books b
            LEFT JOIN book_type bt ON b.book_type = bt.id
            WHERE b.office_id = %s AND b.status = 1
            GROUP BY bt.id
            ORDER BY total_quantity DESC LIMIT 100
        """
        cur.execute(query, (office_id,))
        rows = cur.fetchall()
        return _build_response(rows, question, "library", office_id, session_id, base_url)
    finally:
        conn.close()

def _exec_most_issued_books(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    limit = slots.get("limit") or 10
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT b.title AS book_title, b.author, COUNT(bi.id) AS issue_count
            FROM book_issue bi
            JOIN books b ON bi.book_id = b.id
            WHERE bi.office_id = %s
            GROUP BY b.id
            ORDER BY issue_count DESC LIMIT %s
        """
        cur.execute(query, (office_id, limit))
        rows = cur.fetchall()
        return _build_response(rows, question, "library", office_id, session_id, base_url)
    finally:
        conn.close()

def _exec_recent_book_issues(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    limit = slots.get("limit") or 10
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT b.title AS book_title, u.name AS trainee_name, bi.issue_date, tc.course_batch
            FROM book_issue bi
            JOIN books b ON bi.book_id = b.id
            JOIN users u ON bi.user_id = u.id
            LEFT JOIN training_calendars tc ON bi.course_id = tc.id
            WHERE bi.office_id = %s
            ORDER BY bi.issue_date DESC LIMIT %s
        """
        cur.execute(query, (office_id, limit))
        rows = cur.fetchall()
        return _build_response(rows, question, "library", office_id, session_id, base_url, force_report=True)
    finally:
        conn.close()

def _exec_pending_book_returns(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    user_id = slots.get("user_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT b.title AS book_title, bi.issue_date, bi.return_date AS due_date,
                   u.name AS trainee_name, tc.course_batch
            FROM book_issue bi
            JOIN books b ON bi.book_id = b.id
            JOIN users u ON bi.user_id = u.id
            LEFT JOIN training_calendars tc ON bi.course_id = tc.id
            WHERE bi.office_id = %s AND bi.status = 1
        """
        params = [office_id]
        if user_id:
            query += " AND u.id = %s"
            params.append(user_id)
        query += " ORDER BY bi.issue_date ASC LIMIT 500"
        cur.execute(query, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "library", office_id, session_id, base_url)
    finally:
        conn.close()
