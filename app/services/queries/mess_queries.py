"""Mess module query templates."""

TEMPLATES = [
    {
        "id": "MESS_TOTAL_BILLS",
        "module": "mess",
        "description": "Total bills",
        "example_questions": ["Total mess bills?", "How many bills?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff", "mess_manager"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "MESS_BILL_AMOUNT_SUMMARY",
        "module": "mess",
        "description": "Bill amount summary",
        "example_questions": ["Total bill amount?", "Mess collection?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "summary",
        "security_level": "medium"
    },
    {
        "id": "MESS_BILL_DETAILS_TRAINEE",
        "module": "mess",
        "description": "Bill details by trainee",
        "example_questions": ["Trainee bill details?", "Show trainee mess bill?"],
        "required_params": [],
        "optional_params": ["user_id", "user_name", "office_id"],
        "allowed_roles": ["principal", "admin", "mess_manager", "trainee"],
        "result_type": "detail",
        "security_level": "low"
    },
    {
        "id": "MESS_RECEIPTS",
        "module": "mess",
        "description": "Bill receipts",
        "example_questions": ["Mess receipts?", "Show receipts?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MESS_PENDING_DUES",
        "module": "mess",
        "description": "Pending dues",
        "example_questions": ["Pending mess dues?", "Unpaid mess bills?"],
        "required_params": [],
        "optional_params": ["office_id", "user_id"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "MESS_PAID_RECEIPTS",
        "module": "mess",
        "description": "Paid receipts",
        "example_questions": ["Paid mess bills?", "Paid receipts?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MESS_REFUND_SUMMARY",
        "module": "mess",
        "description": "Refund summary",
        "example_questions": ["Mess refunds?", "Total refunds?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "summary",
        "security_level": "medium"
    },
    {
        "id": "MESS_MATERIAL_LIST",
        "module": "mess",
        "description": "Mess material list",
        "example_questions": ["Mess materials?", "List mess items?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MESS_ITEM_PRICE_LIST",
        "module": "mess",
        "description": "Item price list",
        "example_questions": ["Item prices?", "Mess item rates?"],
        "required_params": [],
        "optional_params": ["office_id", "item_id"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MESS_MONTHLY_BILL_SUMMARY",
        "module": "mess",
        "description": "Monthly bill summary",
        "example_questions": ["Monthly mess bill?", "This month mess collection?"],
        "required_params": [],
        "optional_params": ["month", "year", "office_id"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "MESS_COURSE_WISE",
        "module": "mess",
        "description": "Course-wise mess bills",
        "example_questions": ["Course-wise mess bills?", "Mess by course?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MESS_HOSTEL_WISE",
        "module": "mess",
        "description": "Hostel-wise mess bills",
        "example_questions": ["Hostel-wise mess?", "Mess by hostel?"],
        "required_params": [],
        "optional_params": ["hostel_id", "office_id"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MESS_TOTAL_COLLECTION",
        "module": "mess",
        "description": "Total collection",
        "example_questions": ["Total mess collection?", "Overall mess revenue?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "summary",
        "security_level": "medium"
    },
    {
        "id": "MESS_TOTAL_DUE",
        "module": "mess",
        "description": "Total due",
        "example_questions": ["Total mess dues?", "Outstanding mess amount?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "summary",
        "security_level": "medium"
    },
    {
        "id": "MESS_BILL_BY_DATE",
        "module": "mess",
        "description": "Bill by date",
        "example_questions": ["Bills on date?", "Date-wise bills?"],
        "required_params": [],
        "optional_params": ["date", "from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MESS_RECEIPT_BY_DATE",
        "module": "mess",
        "description": "Receipt by date",
        "example_questions": ["Receipts on date?", "Date-wise receipts?"],
        "required_params": [],
        "optional_params": ["date", "from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MESS_ITEM_WISE_SUMMARY",
        "module": "mess",
        "description": "Item-wise bill summary",
        "example_questions": ["Item-wise bill?", "Bill by item?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "MESS_PARTY_VENDOR_SUMMARY",
        "module": "mess",
        "description": "Party/vendor summary",
        "example_questions": ["Vendor summary?", "Party-wise summary?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "MESS_FORMAT_DETAILS",
        "module": "mess",
        "description": "Mess format/company details",
        "example_questions": ["Mess format?", "Company details?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "mess_manager"],
        "result_type": "detail",
        "security_level": "low"
    },
    {
        "id": "MESS_MODULE_SUMMARY",
        "module": "mess",
        "description": "Mess module summary",
        "example_questions": ["Mess summary?", "Mess module overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute mess queries."""
    p = params or {}
    
    if query_id == "MESS_BILL_AMOUNT_SUMMARY":
        cur.execute("""
            SELECT SUM(bd.amount) AS total_bill_amount,
                   COUNT(DISTINCT b.user_id) AS total_trainees,
                   COUNT(DISTINCT b.id) AS total_bills
            FROM bills b
            JOIN bill_details bd ON bd.bill_id = b.id
            JOIN users u ON u.id = b.user_id
            WHERE b.status = 1 AND bd.status = 1 AND u.office_id = %s
        """, (office_id,))
        r = cur.fetchone()
        if not r or r['total_bills'] == 0: return "No mess bill summary available."
        return (f"Mess Bill Summary:\n"
                f"Total Bill Amount: {r['total_bill_amount']}\n"
                f"Total Trainees: {r['total_trainees']}\n"
                f"Total Bills: {r['total_bills']}")

    elif query_id == "MESS_BILL_DETAILS_TRAINEE":
        uid = p.get("user_id")
        if not uid: return "Please specify user_id."
        cur.execute("""
            SELECT b.id AS bill_id, b.bill_no, b.bill_date,
                   u.name AS trainee_name, i.item_name,
                   bd.qty, bd.rate, bd.amount, bd.from_date, bd.to_date
            FROM bills b
            JOIN bill_details bd ON bd.bill_id = b.id
            JOIN users u ON u.id = b.user_id
            JOIN items i ON i.id = bd.item_id
            WHERE b.user_id = %s AND b.status = 1 AND bd.status = 1 AND u.office_id = %s
            ORDER BY b.bill_date DESC
            LIMIT 50
        """, (uid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No mess bill details found for trainee {uid}."
        lines = [f"- Bill {r['bill_no']} ({r['bill_date']}): {r['item_name']} (Qty: {r['qty']}, Amount: {r['amount']})" for r in rows]
        return f"Mess Bills for Trainee {uid}:\n" + "\n".join(lines)

    elif query_id == "MESS_RECEIPTS":
        cur.execute("""
            SELECT br.id, br.receipt_no, br.receipt_date, br.amount,
                   br.pay_by, br.txn_no, br.remarks,
                   u.name AS trainee_name, c.course_name
            FROM bill_receipts br
            JOIN users u ON u.id = br.user_id
            LEFT JOIN training_calendars tc ON tc.id = br.course_id
            LEFT JOIN courses c ON c.id = tc.ct_id
            WHERE br.status = 1 AND u.office_id = %s
            ORDER BY br.receipt_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No mess receipts found."
        lines = [f"- Receipt {r['receipt_no']} ({r['receipt_date']}): {r['amount']} from {r['trainee_name']}" for r in rows]
        return "Mess Receipts:\n" + "\n".join(lines)

    elif query_id == "MESS_PENDING_DUES":
        cur.execute("""
            SELECT b.id AS bill_id, b.bill_no, b.bill_date,
                   u.name AS trainee_name, u.mobile,
                   SUM(bd.amount) AS bill_amount,
                   COALESCE(SUM(br.amount), 0) AS paid_amount,
                   SUM(bd.amount) - COALESCE(SUM(br.amount), 0) AS pending_amount
            FROM bills b
            JOIN bill_details bd ON bd.bill_id = b.id
            JOIN users u ON u.id = b.user_id
            LEFT JOIN bill_receipts br ON br.bill_id = b.id AND br.status = 1
            WHERE b.status = 1 AND bd.status = 1 AND br.due = 0 AND u.office_id = %s
            GROUP BY b.id, b.bill_no, b.bill_date, u.name, u.mobile
            HAVING pending_amount > 0
            ORDER BY pending_amount DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No pending mess dues found."
        lines = [f"- Bill {r['bill_no']}: {r['trainee_name']} ({r['mobile']}) owes {r['pending_amount']} (Billed: {r['bill_amount']})" for r in rows]
        return "Pending Mess Dues:\n" + "\n".join(lines)

    elif query_id == "MESS_PAID_RECEIPTS":
        cur.execute("""
            SELECT br.receipt_no, br.receipt_date, br.amount, br.txn_no,
                   u.name AS trainee_name,
                   CASE br.pay_by WHEN 1 THEN 'Cash' WHEN 2 THEN 'Bank' ELSE 'Online' END AS payment_mode
            FROM bill_receipts br
            JOIN users u ON u.id = br.user_id
            WHERE br.due = 1 AND br.status = 1 AND u.office_id = %s
            ORDER BY br.receipt_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No paid receipts found."
        lines = [f"- Receipt {r['receipt_no']} ({r['receipt_date']}): {r['amount']} via {r['payment_mode']} from {r['trainee_name']}" for r in rows]
        return "Paid Mess Receipts:\n" + "\n".join(lines)

    elif query_id == "MESS_REFUND_SUMMARY":
        cur.execute("""
            SELECT brr.id, brr.receipt_no, brr.receipt_date, brr.amount,
                   u.name AS trainee_name,
                   brr.txn_no, brr.remarks
            FROM bill_receipts_refund brr
            JOIN users u ON u.id = brr.user_id
            WHERE brr.status = 1 AND u.office_id = %s
            ORDER BY brr.receipt_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No mess refunds found."
        lines = [f"- Refund {r['receipt_no']} ({r['receipt_date']}): {r['amount']} to {r['trainee_name']}" for r in rows]
        return "Mess Refunds:\n" + "\n".join(lines)

    elif query_id == "MESS_MATERIAL_LIST":
        cur.execute("""
            SELECT id, item_name, units, status, created_at
            FROM mess_material
            WHERE status = 1
            ORDER BY item_name
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No mess materials found."
        lines = [f"- {r['item_name']} (Units: {r['units']})" for r in rows]
        return "Mess Materials:\n" + "\n".join(lines)

    elif query_id == "MESS_ITEM_PRICE_LIST":
        cur.execute("""
            SELECT i.item_name, ip.price, ip.gst_rate, ip.effect_date
            FROM item_prices ip
            JOIN items i ON i.id = ip.item_id
            WHERE i.type = 1 AND ip.status = 1
            ORDER BY ip.effect_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No mess item prices found."
        lines = [f"- {r['item_name']}: {r['price']} (GST: {r['gst_rate']}%) from {r['effect_date']}" for r in rows]
        return "Mess Item Prices:\n" + "\n".join(lines)

    elif query_id == "MESS_MONTHLY_BILL_SUMMARY":
        cur.execute("""
            SELECT YEAR(b.bill_date) AS yr, MONTH(b.bill_date) AS mo,
                   MONTHNAME(b.bill_date) AS month_name,
                   COUNT(DISTINCT b.id) AS total_bills,
                   SUM(bd.amount) AS total_amount,
                   COUNT(DISTINCT b.user_id) AS total_trainees
            FROM bills b
            JOIN bill_details bd ON bd.bill_id = b.id
            JOIN users u ON u.id = b.user_id
            WHERE b.status = 1 AND bd.status = 1 AND u.office_id = %s
            GROUP BY YEAR(b.bill_date), MONTH(b.bill_date)
            ORDER BY yr DESC, mo DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No monthly bill summary found."
        lines = [f"- {r['month_name']} {r['yr']}: {r['total_bills']} Bills, Total Amount: {r['total_amount']} ({r['total_trainees']} Trainees)" for r in rows]
        return "Monthly Mess Bill Summary:\n" + "\n".join(lines)

    elif query_id == "MESS_COURSE_WISE":
        cur.execute("""
            SELECT tc.course_batch, c.course_name,
                   COUNT(DISTINCT b.user_id) AS trainees,
                   SUM(bd.amount) AS total_bill,
                   COALESCE(SUM(br.amount), 0) AS collected
            FROM bills b
            JOIN bill_details bd ON bd.bill_id = b.id
            JOIN training_calendars tc ON tc.id = b.course_id
            JOIN courses c ON c.id = tc.ct_id
            LEFT JOIN bill_receipts br ON br.bill_id = b.id AND br.status = 1
            WHERE b.status = 1 AND bd.status = 1 AND tc.office_id = %s
            GROUP BY b.course_id, tc.course_batch, c.course_name
            ORDER BY total_bill DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No course-wise mess data found."
        lines = [f"- {r['course_name']} ({r['course_batch']}): Billed {r['total_bill']}, Collected {r['collected']} ({r['trainees']} Trainees)" for r in rows]
        return "Course-wise Mess Summary:\n" + "\n".join(lines)

    elif query_id == "MESS_HOSTEL_WISE":
        cur.execute("""
            SELECT hb.building_name,
                   COUNT(DISTINCT b.user_id) AS trainees,
                   SUM(bd.amount) AS total_bill
            FROM bills b
            JOIN bill_details bd ON bd.bill_id = b.id
            JOIN hostel_buildings hb ON hb.id = b.hostel_id
            WHERE b.status = 1 AND bd.status = 1 AND hb.office_id = %s
            GROUP BY b.hostel_id, hb.building_name
            ORDER BY total_bill DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No hostel-wise mess data found."
        lines = [f"- {r['building_name']}: {r['total_bill']} Billed ({r['trainees']} Trainees)" for r in rows]
        return "Hostel-wise Mess Summary:\n" + "\n".join(lines)

    elif query_id == "MESS_TOTAL_COLLECTION":
        cur.execute("""
            SELECT SUM(br.amount) AS total_collected,
                   COUNT(br.id) AS total_receipts
            FROM bill_receipts br
            JOIN users u ON u.id = br.user_id
            WHERE br.status = 1 AND u.office_id = %s
        """, (office_id,))
        r = cur.fetchone()
        return f"Total Mess Collection: {r['total_collected'] or 0} from {r['total_receipts']} receipts."

    elif query_id == "MESS_TOTAL_DUE":
        cur.execute("""
            SELECT SUM(bd.amount) - COALESCE(SUM(br.amount), 0) AS total_due
            FROM bills b
            JOIN bill_details bd ON bd.bill_id = b.id AND bd.status = 1
            JOIN users u ON u.id = b.user_id
            LEFT JOIN bill_receipts br ON br.bill_id = b.id AND br.status = 1
            WHERE b.status = 1 AND u.office_id = %s
        """, (office_id,))
        r = cur.fetchone()
        return f"Total Mess Dues: {r['total_due'] or 0}"

    elif query_id == "MESS_BILL_BY_DATE":
        bd = p.get("bill_date") or p.get("date")
        if not bd: return "Please specify bill_date."
        cur.execute("""
            SELECT b.id, b.bill_no, b.bill_date,
                   u.name AS trainee_name,
                   SUM(bd.amount) AS total_amount
            FROM bills b
            JOIN bill_details bd ON bd.bill_id = b.id
            JOIN users u ON u.id = b.user_id
            WHERE DATE(b.bill_date) = %s AND b.status = 1 AND bd.status = 1 AND u.office_id = %s
            GROUP BY b.id, b.bill_no, b.bill_date, u.name
            ORDER BY b.bill_date DESC
            LIMIT 50
        """, (bd, office_id))
        rows = cur.fetchall()
        if not rows: return f"No bills found on {bd}."
        lines = [f"- Bill {r['bill_no']}: {r['total_amount']} for {r['trainee_name']}" for r in rows]
        return f"Mess Bills on {bd}:\n" + "\n".join(lines)

    elif query_id == "MESS_RECEIPT_BY_DATE":
        rd = p.get("receipt_date") or p.get("date")
        if not rd: return "Please specify receipt_date."
        cur.execute("""
            SELECT br.receipt_no, br.receipt_date, br.amount,
                   u.name AS trainee_name, br.txn_no
            FROM bill_receipts br
            JOIN users u ON u.id = br.user_id
            WHERE DATE(br.receipt_date) = %s AND br.status = 1 AND u.office_id = %s
            ORDER BY br.receipt_date DESC
            LIMIT 50
        """, (rd, office_id))
        rows = cur.fetchall()
        if not rows: return f"No receipts found on {rd}."
        lines = [f"- Receipt {r['receipt_no']}: {r['amount']} from {r['trainee_name']}" for r in rows]
        return f"Mess Receipts on {rd}:\n" + "\n".join(lines)

    elif query_id == "MESS_ITEM_WISE_SUMMARY":
        cur.execute("""
            SELECT i.item_name,
                   SUM(bd.qty) AS total_qty,
                   SUM(bd.amount) AS total_amount,
                   COUNT(DISTINCT bd.bill_id) AS bills_count
            FROM bill_details bd
            JOIN items i ON i.id = bd.item_id
            JOIN bills b ON b.id = bd.bill_id
            JOIN users u ON u.id = b.user_id
            WHERE bd.status = 1 AND i.type = 1 AND u.office_id = %s
            GROUP BY i.id, i.item_name
            ORDER BY total_amount DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No item-wise summary found."
        lines = [f"- {r['item_name']}: {r['total_qty']} Qty, Amount {r['total_amount']} ({r['bills_count']} Bills)" for r in rows]
        return "Item-wise Mess Summary:\n" + "\n".join(lines)

    elif query_id == "MESS_PARTY_VENDOR_SUMMARY":
        cur.execute("""
            SELECT p.p_name AS vendor_name, p.p_mobile,
                   COUNT(sm.id) AS purchase_count
            FROM partys p
            LEFT JOIN sport_material sm ON sm.party_id = p.id AND sm.status = 1
            WHERE p.status = 1
            GROUP BY p.id, p.p_name, p.p_mobile
            ORDER BY purchase_count DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No vendor summary found."
        lines = [f"- {r['vendor_name']} ({r['p_mobile']}): {r['purchase_count']} Purchases" for r in rows]
        return "Mess Vendors:\n" + "\n".join(lines)

    elif query_id == "MESS_FORMAT_DETAILS":
        cur.execute("""
            SELECT id, company_name, bill_prefix, gst_no, bank_name,
                   bank_acc, ifsc_code, upi_code, fssai_license_no, effective_date
            FROM mess_bill_format
            WHERE status = 1
            ORDER BY effective_date DESC
            LIMIT 1
        """)
        r = cur.fetchone()
        if not r: return "No mess bill format found."
        return (f"Mess Bill Format ({r['effective_date']}):\n"
                f"Company: {r['company_name']}\n"
                f"Prefix: {r['bill_prefix']}\n"
                f"GST: {r['gst_no']}\n"
                f"FSSAI: {r['fssai_license_no']}\n"
                f"Bank: {r['bank_name']} ({r['bank_acc']}, {r['ifsc_code']})\n"
                f"UPI: {r['upi_code']}")

    elif query_id == "MESS_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(id) FROM bills b JOIN users u ON u.id=b.user_id WHERE b.status=1 AND u.office_id=%s) AS total_bills,
              (SELECT SUM(bd.amount) FROM bill_details bd JOIN bills b ON b.id=bd.bill_id JOIN users u ON u.id=b.user_id WHERE bd.status=1 AND u.office_id=%s) AS total_billed_amount,
              (SELECT SUM(br.amount) FROM bill_receipts br JOIN users u ON u.id=br.user_id WHERE br.status=1 AND u.office_id=%s) AS total_collected,
              (SELECT COUNT(id) FROM bill_receipts br JOIN users u ON u.id=br.user_id WHERE br.status=1 AND u.office_id=%s) AS total_receipts,
              (SELECT COUNT(id) FROM bill_receipts_refund brr JOIN users u ON u.id=brr.user_id WHERE brr.status=1 AND u.office_id=%s) AS total_refunds
        """, (office_id, office_id, office_id, office_id, office_id))
        r = cur.fetchone()
        if not r: return "Could not generate mess module summary."
        return (f"Mess Module Summary:\n"
                f"Total Bills: {r['total_bills']}\n"
                f"Total Billed: {r['total_billed_amount']}\n"
                f"Total Collected: {r['total_collected']}\n"
                f"Total Receipts: {r['total_receipts']}\n"
                f"Total Refunds: {r['total_refunds']}")

    return None
