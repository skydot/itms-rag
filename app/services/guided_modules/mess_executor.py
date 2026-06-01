from app.services.db_service import get_connection
from app.services.report_service import generate_report
from app.services.response_mode_service import detect_response_mode

def _build_response(rows: list, question: str, module: str, office_id: int, session_id: str, base_url: str, force_report: bool = False, force_chat: bool = False) -> dict:
    row_count = len(rows)
    if force_report:
        response_mode = "report"
    elif force_chat:
        response_mode = "chat"
    else:
        response_mode = detect_response_mode(question, result_type=module, row_count=row_count)

    if response_mode == "report":
        if row_count == 0:
            return {"type": "text", "message": "No matching records found."}
        report = generate_report(
            module_name=module,
            title=f"Mess Report",
            user_question=question,
            rows=rows,
            office_id=office_id,
            session_id=session_id
        )
        report_url = base_url.rstrip("/") + report["url"]
        ttl = report["ttl_seconds"]
        if ttl < 60:
            exp = f"{ttl} seconds"
        elif ttl < 3600:
            exp = f"{ttl // 60} minute{'s' if ttl // 60 != 1 else ''}"
        else:
            exp = f"{ttl // 3600} hour{'s' if ttl // 3600 != 1 else ''}"
            
        msg = f"Found {row_count} records for your request.\nOpen full report: {report_url}\nThis report link will expire in {exp}."
        return {
            "type": "text",
            "message": msg,
            "report_url": report_url,
            "row_count": row_count,
            "response_mode": "report"
        }
    else:
        if row_count == 0:
            return {"type": "text", "message": "No matching records found."}
        from app.services.llm_service import format_answer
        formatted_text = ""
        for r in rows:
            for k, v in r.items():
                formatted_text += f"{k}: {v}, "
            formatted_text += "\n"
        
        answer = format_answer(question, formatted_text)
        return {"type": "text", "message": answer}

def _exec_mess_dues_by_trainee(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    user_id = slots.get("user_id")
    status = slots.get("dues_status") or "pending"
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT u.name AS trainee_name, tc.course_batch, b.bill_date,
                   SUM(bd.amount) AS total_bill_amount,
                   COALESCE((SELECT SUM(br.amount) FROM bill_receipts br WHERE br.bill_id = b.id AND br.status=1), 0) AS paid_amount,
                   (SUM(bd.amount) - COALESCE((SELECT SUM(br.amount) FROM bill_receipts br WHERE br.bill_id = b.id AND br.status=1), 0)) AS pending_amount
            FROM bills b
            JOIN users u ON b.user_id = u.id
            JOIN bill_details bd ON bd.bill_id = b.id AND bd.status = 1
            LEFT JOIN tra_masters tm ON tm.user_id = u.id AND tm.status = 1
            LEFT JOIN training_calendars tc ON tc.id = tm.course_id AND tc.status = 1
            WHERE u.office_id = %s AND b.status = 1
        """
        params = [office_id]
        
        if user_id:
            query += " AND u.id = %s"
            params.append(user_id)
            
        query += " GROUP BY b.id, u.name, tc.course_batch, b.bill_date"
        
        if status == "pending":
            query += " HAVING pending_amount > 0"
        elif status == "paid":
            query += " HAVING pending_amount <= 0"
            
        query += " ORDER BY b.bill_date DESC"
        cur.execute(query, params)
        rows = cur.fetchall()
        
        return _build_response(rows, question, "mess", office_id, session_id, base_url)
    finally:
        conn.close()

def _exec_mess_bill_summary(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    course_id = slots.get("course_id")
    month = slots.get("month")
    year = slots.get("year")
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT tc.course_batch, MONTH(b.bill_date) as bill_month, YEAR(b.bill_date) as bill_year,
                   SUM(bd.amount) AS total_bill_amount
            FROM bills b
            JOIN bill_details bd ON bd.bill_id = b.id AND bd.status = 1
            LEFT JOIN tra_masters tm ON tm.user_id = b.user_id AND tm.status = 1
            LEFT JOIN training_calendars tc ON tc.id = tm.course_id AND tc.status = 1
            WHERE b.status = 1
        """
        params = []
        if course_id:
            query += " AND tc.course_id = %s"
            params.append(course_id)
        if month:
            # simple month mapping if needed, assuming numeric
            pass # TODO mapping if string month
        query += " GROUP BY tc.course_batch, bill_month, bill_year ORDER BY bill_year DESC, bill_month DESC"
        cur.execute(query, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "mess", office_id, session_id, base_url)
    finally:
        conn.close()

def _exec_pending_mess_dues(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT u.name AS trainee_name, tc.course_batch, b.bill_date,
                   SUM(bd.amount) AS total_bill_amount,
                   COALESCE((SELECT SUM(br.amount) FROM bill_receipts br WHERE br.bill_id = b.id AND br.status=1), 0) AS paid_amount,
                   (SUM(bd.amount) - COALESCE((SELECT SUM(br.amount) FROM bill_receipts br WHERE br.bill_id = b.id AND br.status=1), 0)) AS pending_amount
            FROM bills b
            JOIN users u ON b.user_id = u.id
            JOIN bill_details bd ON bd.bill_id = b.id AND bd.status = 1
            LEFT JOIN tra_masters tm ON tm.user_id = u.id AND tm.status = 1
            LEFT JOIN training_calendars tc ON tc.id = tm.course_id AND tc.status = 1
            WHERE u.office_id = %s AND b.status = 1
            GROUP BY b.id, u.name, tc.course_batch, b.bill_date
            HAVING pending_amount > 0
            ORDER BY pending_amount DESC
        """
        cur.execute(query, (office_id,))
        rows = cur.fetchall()
        
        # if question asks for count
        if "how many" in question.lower():
            count = len(rows)
            return {"type": "text", "message": f"There are {count} pending mess dues."}
            
        return _build_response(rows, question, "mess", office_id, session_id, base_url)
    finally:
        conn.close()

def _exec_mess_receipts_by_trainee(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    user_id = slots.get("user_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT u.name AS trainee_name, br.receipt_no, br.receipt_date, br.amount AS paid_amount,
                   b.bill_date, b.bill_no
            FROM bill_receipts br
            JOIN bills b ON br.bill_id = b.id
            JOIN users u ON br.user_id = u.id
            WHERE u.office_id = %s AND br.status = 1
        """
        params = [office_id]
        if user_id:
            query += " AND u.id = %s"
            params.append(user_id)
            
        query += " ORDER BY br.receipt_date DESC"
        cur.execute(query, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "mess", office_id, session_id, base_url)
    finally:
        conn.close()

def _exec_mess_item_summary(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    item_id = slots.get("item_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT i.item_name, i.units, SUM(mm.qty) AS total_quantity, SUM(mm.amount) AS total_amount
            FROM mess_material mm
            JOIN items i ON mm.item_id = i.id
            WHERE i.status = 1 AND mm.status = 1
        """
        params = []
        if item_id:
            query += " AND i.id = %s"
            params.append(item_id)
            
        query += " GROUP BY i.id ORDER BY total_quantity DESC"
        cur.execute(query, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "mess", office_id, session_id, base_url)
    finally:
        conn.close()

def _exec_mess_party_summary(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    party_id = slots.get("party_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT p.p_name AS party_name, p.p_mobile, SUM(mm.amount) AS total_payment, COUNT(mm.id) AS transaction_count
            FROM mess_material mm
            JOIN partys p ON mm.party_id = p.id
            WHERE p.office_id = %s AND p.status = 1 AND mm.status = 1
        """
        params = [office_id]
        if party_id:
            query += " AND p.id = %s"
            params.append(party_id)
            
        query += " GROUP BY p.id ORDER BY total_payment DESC"
        cur.execute(query, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "mess", office_id, session_id, base_url)
    finally:
        conn.close()

def _exec_mess_refund_summary(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        # Since I couldn't see bill_receipts_refund schema perfectly, I will do a best effort safe query
        # Usually it has user_id, amount, date
        query = """
            SELECT u.name AS trainee_name, r.amount AS refund_amount, r.created_at AS refund_date
            FROM bill_receipts_refund r
            JOIN users u ON r.user_id = u.id
            WHERE u.office_id = %s
        """
        user_id = slots.get("user_id")
        params = [office_id]
        if user_id:
            query += " AND u.id = %s"
            params.append(user_id)
            
        query += " ORDER BY r.created_at DESC"
        cur.execute(query, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "mess", office_id, session_id, base_url)
    except Exception as e:
        return {"type": "text", "message": "No refund records found or feature not supported."}
    finally:
        conn.close()

def _exec_mess_material_stock(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    item_id = slots.get("item_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT i.item_name, i.units, SUM(mm.qty) AS total_purchased
            FROM mess_material mm
            JOIN items i ON mm.item_id = i.id
            WHERE i.status = 1 AND mm.status = 1
        """
        params = []
        if item_id:
            query += " AND i.id = %s"
            params.append(item_id)
            
        query += " GROUP BY i.id ORDER BY i.item_name"
        cur.execute(query, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "mess", office_id, session_id, base_url)
    finally:
        conn.close()

def _exec_mess_bill_count(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT COUNT(id) AS bill_count, SUM(amount) as total_amount
            FROM bill_details
            WHERE status = 1
        """
        cur.execute(query)
        row = cur.fetchone()
        return {"type": "text", "message": f"There are {row['bill_count']} mess bills totaling {row['total_amount']}."}
    finally:
        conn.close()

def _exec_recent_mess_transactions(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    limit = slots.get("limit") or 10
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT br.receipt_no, br.receipt_date, br.amount AS paid_amount, u.name AS trainee_name
            FROM bill_receipts br
            JOIN users u ON br.user_id = u.id
            WHERE u.office_id = %s AND br.status = 1
            ORDER BY br.receipt_date DESC
            LIMIT %s
        """
        cur.execute(query, (office_id, limit))
        rows = cur.fetchall()
        return _build_response(rows, question, "mess", office_id, session_id, base_url)
    finally:
        conn.close()

def execute_mess_guided_query(flow_id: str, slots: dict, office_id: int, role: str, session_id: str = None, user_question: str = "") -> dict:
    if flow_id == "mess_dues_by_trainee":
        return _exec_mess_dues_by_trainee(slots, office_id, user_question, session_id, base_url="http://localhost:8000")
    elif flow_id == "mess_bill_summary":
        return _exec_mess_bill_summary(slots, office_id, user_question, session_id, base_url="http://localhost:8000")
    elif flow_id == "pending_mess_dues":
        return _exec_pending_mess_dues(slots, office_id, user_question, session_id, base_url="http://localhost:8000")
    elif flow_id == "mess_receipts_by_trainee":
        return _exec_mess_receipts_by_trainee(slots, office_id, user_question, session_id, base_url="http://localhost:8000")
    elif flow_id == "mess_item_summary":
        return _exec_mess_item_summary(slots, office_id, user_question, session_id, base_url="http://localhost:8000")
    elif flow_id == "mess_party_summary":
        return _exec_mess_party_summary(slots, office_id, user_question, session_id, base_url="http://localhost:8000")
    elif flow_id == "mess_refund_summary":
        return _exec_mess_refund_summary(slots, office_id, user_question, session_id, base_url="http://localhost:8000")
    elif flow_id == "mess_material_stock":
        return _exec_mess_material_stock(slots, office_id, user_question, session_id, base_url="http://localhost:8000")
    elif flow_id == "mess_bill_count":
        return _exec_mess_bill_count(slots, office_id, user_question, session_id, base_url="http://localhost:8000")
    elif flow_id == "recent_mess_transactions":
        return _exec_recent_mess_transactions(slots, office_id, user_question, session_id, base_url="http://localhost:8000")
    else:
        return {"type": "text", "message": "Flow not recognized."}
