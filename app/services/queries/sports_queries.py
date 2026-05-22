"""Sports module query templates."""

TEMPLATES = [
    
    {
        "id": "SPORTS_UPCOMING",
        "module": "sports",
        "description": "Upcoming sports",
        "example_questions": ["Upcoming sports?", "Future sports events?"],
        "required_params": [],
        "optional_params": ["office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff", "trainee"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SPORTS_COMPLETED",
        "module": "sports",
        "description": "Completed sports",
        "example_questions": ["Completed sports?", "Past sports events?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SPORTS_TEAMS",
        "module": "sports",
        "description": "Sports teams",
        "example_questions": ["Sports teams?", "How many teams?"],
        "required_params": [],
        "optional_params": ["program_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff", "sports_coordinator"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SPORTS_PARTICIPANTS_COUNT",
        "module": "sports",
        "description": "Participants count",
        "example_questions": ["Sports participants?", "How many participants?"],
        "required_params": [],
        "optional_params": ["program_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "SPORTS_ITEM_LIST",
        "module": "sports",
        "description": "Sport item list",
        "example_questions": ["Sports items?", "Equipment list?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff", "sports_coordinator"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SPORTS_ITEM_ISSUED",
        "module": "sports",
        "description": "Issued sport items",
        "example_questions": ["Issued items?", "Equipment issued?"],
        "required_params": [],
        "optional_params": ["office_id", "user_id"],
        "allowed_roles": ["principal", "admin", "staff", "sports_coordinator"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SPORTS_MATERIAL_PURCHASE",
        "module": "sports",
        "description": "Sport material purchase",
        "example_questions": ["Material purchases?", "Sports items bought?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "sports_coordinator"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SPORTS_PHOTOS",
        "module": "sports",
        "description": "Sports photos",
        "example_questions": ["Sports photos?", "Event pictures?"],
        "required_params": [],
        "optional_params": ["sport_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff", "trainee"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SPORTS_TEAM_SUMMARY",
        "module": "sports",
        "description": "Sport team summary",
        "example_questions": ["Team summary?", "Team-wise stats?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "SPORTS_ITEM_STOCK",
        "module": "sports",
        "description": "Sport item stock",
        "example_questions": ["Item stock?", "Equipment available?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "sports_coordinator"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "SPORTS_PAYMENT",
        "module": "sports",
        "description": "Sport payment/receipt",
        "example_questions": ["Sports payments?", "Sports receipts?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "sports_coordinator"],
        "result_type": "summary",
        "security_level": "medium"
    },
    {
        "id": "SPORTS_BY_DATE",
        "module": "sports",
        "description": "Sports by date",
        "example_questions": ["Sports on date?", "Date-wise sports?"],
        "required_params": [],
        "optional_params": ["date", "from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SPORTS_BY_COORDINATOR",
        "module": "sports",
        "description": "Coordinator-wise sports",
        "example_questions": ["Sports by coordinator?", "Coordinator events?"],
        "required_params": [],
        "optional_params": ["coordinator_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SPORTS_TEAM_PARTICIPANTS",
        "module": "sports",
        "description": "Team-wise participants",
        "example_questions": ["Team participants?", "Participants by team?"],
        "required_params": [],
        "optional_params": ["team_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SPORTS_MATERIAL_COST",
        "module": "sports",
        "description": "Material cost summary",
        "example_questions": ["Material costs?", "Sports expenditure?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "sports_coordinator"],
        "result_type": "summary",
        "security_level": "medium"
    },
    {
        "id": "SPORTS_ISSUE_FINE",
        "module": "sports",
        "description": "Sports issue fine",
        "example_questions": ["Sports fines?", "Equipment fines?"],
        "required_params": [],
        "optional_params": ["office_id", "user_id"],
        "allowed_roles": ["principal", "admin", "sports_coordinator"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "SPORTS_BY_COURSE",
        "module": "sports",
        "description": "Sports by course",
        "example_questions": ["Sports by course?", "Course-wise sports?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SPORTS_STATUS_SUMMARY",
        "module": "sports",
        "description": "Sports status summary",
        "example_questions": ["Sports status?", "Event status?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "SPORTS_MODULE_SUMMARY",
        "module": "sports",
        "description": "Sports module summary",
        "example_questions": ["Sports summary?", "Sports module overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute sports queries."""
    p = params or {}
    
    if query_id == "SPORTS_UPCOMING":
        cur.execute("""
            SELECT s.id, s.program, s.from_date, s.to_date,
                   s.start_timing, s.end_timing, s.coordinator
            FROM sport s
            WHERE s.from_date >= CURDATE() AND s.status = 1
            ORDER BY s.from_date ASC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No upcoming sports programs found."
        lines = [f"- {r['program']} ({r['from_date']} to {r['to_date']}): Coordinator {r['coordinator']}" for r in rows]
        return "Upcoming Sports:\n" + "\n".join(lines)

    elif query_id == "SPORTS_COMPLETED":
        cur.execute("""
            SELECT s.id, s.program, s.from_date, s.to_date,
                   s.start_timing, s.end_timing
            FROM sport s
            WHERE s.to_date < CURDATE() AND s.status = 1
            ORDER BY s.to_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No completed sports programs found."
        lines = [f"- {r['program']} ({r['from_date']} to {r['to_date']})" for r in rows]
        return "Completed Sports:\n" + "\n".join(lines)

    elif query_id == "SPORTS_TEAMS":
        cur.execute("""
            SELECT st.id, st.team_name, s.program AS event_name, s.from_date
            FROM sport_team st
            JOIN sport s ON s.id = st.program_id
            WHERE st.status = 1
            ORDER BY s.from_date DESC, st.team_name
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No sports teams found."
        lines = [f"- {r['team_name']} for {r['event_name']} ({r['from_date']})" for r in rows]
        return "Sports Teams:\n" + "\n".join(lines)

    elif query_id == "SPORTS_PARTICIPANTS_COUNT":
        cur.execute("""
            SELECT s.program, s.from_date, s.to_date,
                   COUNT(DISTINCT sr.id) AS participant_count
            FROM sport s
            LEFT JOIN srec_sport sr ON sr.type_id = s.id AND sr.status = 1
            WHERE s.status = 1
            GROUP BY s.id, s.program, s.from_date, s.to_date
            ORDER BY s.from_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No participants count found."
        lines = [f"- {r['program']} ({r['from_date']}): {r['participant_count']} Participants" for r in rows]
        return "Sports Participants:\n" + "\n".join(lines)

    elif query_id == "SPORTS_ITEM_LIST":
        cur.execute("""
            SELECT si.id, si.sport_item, si.office_id, si.status
            FROM sport_item si
            WHERE si.status = 1 AND si.office_id = %s
            ORDER BY si.sport_item
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No sports items found."
        lines = [f"- {r['sport_item']}" for r in rows]
        return "Sports Items:\n" + "\n".join(lines)

    elif query_id == "SPORTS_ITEM_ISSUED":
        cur.execute("""
            SELECT sii.id, si.sport_item,
                   u.name AS issued_to, u.mobile,
                   sii.qty, sii.issue_date, sii.return_date, sii.fine
            FROM sportitem_issue sii
            JOIN sport_item si ON si.id = sii.sitem_id
            JOIN users u ON u.id = sii.user_id
            WHERE sii.status = 1 AND u.office_id = %s
            ORDER BY sii.issue_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No sports item issues found."
        lines = [f"- {r['qty']}x {r['sport_item']} to {r['issued_to']} (Due: {r['return_date']})" for r in rows]
        return "Issued Sports Items:\n" + "\n".join(lines)

    elif query_id == "SPORTS_MATERIAL_PURCHASE":
        cur.execute("""
            SELECT sm.id, si.sport_item, p.p_name AS vendor,
                   sm.purchase_date, sm.qty, sm.item_price, sm.total_price
            FROM sport_material sm
            JOIN sport_item si ON si.id = sm.item_id
            JOIN partys p ON p.id = sm.party_id
            WHERE sm.status = 1 AND si.office_id = %s
            ORDER BY sm.purchase_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No sports material purchases found."
        lines = [f"- {r['qty']}x {r['sport_item']} from {r['vendor']} on {r['purchase_date']} (Total: {r['total_price']})" for r in rows]
        return "Sports Material Purchases:\n" + "\n".join(lines)

    elif query_id == "SPORTS_PHOTOS":
        cur.execute("""
            SELECT sp.id, sp.sport_photo, s.program AS event,
                   s.from_date, sp.created_at
            FROM sports_photos sp
            JOIN sport s ON s.id = sp.sport_id
            WHERE sp.status = 1
            ORDER BY sp.created_at DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No sports photos found."
        lines = [f"- {r['event']} ({r['from_date']}): Photo {r['sport_photo']}" for r in rows]
        return "Sports Photos:\n" + "\n".join(lines)

    elif query_id == "SPORTS_TEAM_SUMMARY":
        cur.execute("""
            SELECT s.program, COUNT(st.id) AS team_count
            FROM sport s
            LEFT JOIN sport_team st ON st.program_id = s.id AND st.status = 1
            WHERE s.status = 1
            GROUP BY s.id, s.program
            ORDER BY team_count DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No sports team summary found."
        lines = [f"- {r['program']}: {r['team_count']} Teams" for r in rows]
        return "Sports Team Summary:\n" + "\n".join(lines)

    elif query_id == "SPORTS_ITEM_STOCK":
        cur.execute("""
            SELECT si.sport_item,
                   COALESCE(SUM(sm.qty), 0) AS purchased_qty,
                   COALESCE(SUM(CASE WHEN sii.status=1 THEN sii.qty ELSE 0 END), 0) AS issued_qty,
                   COALESCE(SUM(sm.qty), 0) - COALESCE(SUM(CASE WHEN sii.status=1 THEN sii.qty ELSE 0 END), 0) AS available_qty
            FROM sport_item si
            LEFT JOIN sport_material sm ON sm.item_id = si.id AND sm.status = 1
            LEFT JOIN sportitem_issue sii ON sii.sitem_id = si.id
            WHERE si.status = 1 AND si.office_id = %s
            GROUP BY si.id, si.sport_item
            ORDER BY si.sport_item
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No sports item stock found."
        lines = [f"- {r['sport_item']}: {r['available_qty']} Available (Total: {r['purchased_qty']}, Issued: {r['issued_qty']})" for r in rows]
        return "Sports Item Stock:\n" + "\n".join(lines)

    elif query_id == "SPORTS_PAYMENT":
        cur.execute("""
            SELECT sr.id, sr.name, sr.amount, sr.total,
                   sr.receipt_no, sr.receipt_date, sr.payment_by, sr.utr_no
            FROM srec_sport sr
            WHERE sr.status = 1
            ORDER BY sr.receipt_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No sports payments found."
        lines = [f"- {r['name']} paid {r['amount']} on {r['receipt_date']} (Receipt: {r['receipt_no']})" for r in rows]
        return "Sports Payments:\n" + "\n".join(lines)

    elif query_id == "SPORTS_BY_DATE":
        fd = p.get("from_date") or p.get("date")
        if not fd: return "Please specify from_date."
        cur.execute("""
            SELECT s.id, s.program, s.from_date, s.to_date, s.start_timing
            FROM sport s
            WHERE s.from_date = %s AND s.status = 1
            ORDER BY s.start_timing
            LIMIT 50
        """, (fd,))
        rows = cur.fetchall()
        if not rows: return f"No sports found on {fd}."
        lines = [f"- {r['program']} at {r['start_timing']}" for r in rows]
        return f"Sports on {fd}:\n" + "\n".join(lines)

    elif query_id == "SPORTS_BY_COORDINATOR":
        coord = p.get("coordinator_name") or p.get("coordinator")
        if not coord: return "Please specify coordinator_name."
        cur.execute("""
            SELECT s.id, s.program, s.from_date, s.to_date, s.coordinator
            FROM sport s
            WHERE s.coordinator LIKE CONCAT('%%', %s, '%%') AND s.status = 1
            ORDER BY s.from_date DESC
            LIMIT 50
        """, (coord,))
        rows = cur.fetchall()
        if not rows: return f"No sports found for coordinator '{coord}'."
        lines = [f"- {r['program']} ({r['from_date']})" for r in rows]
        return f"Sports coordinated by '{coord}':\n" + "\n".join(lines)

    elif query_id == "SPORTS_TEAM_PARTICIPANTS":
        cur.execute("""
            SELECT sr.id, sr.name, sr.course_id, sr.days, sr.trainee,
                   s.program, st.team_name
            FROM srec_sport sr
            JOIN sport s ON s.id = sr.type_id
            LEFT JOIN sport_team st ON st.program_id = s.id AND st.status = 1
            WHERE sr.status = 1
            ORDER BY s.from_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No team participants found."
        lines = [f"- {r['name']} in {r['team_name']} ({r['program']})" for r in rows]
        return "Team Participants:\n" + "\n".join(lines)

    elif query_id == "SPORTS_MATERIAL_COST":
        cur.execute("""
            SELECT si.sport_item,
                   SUM(sm.total_price) AS total_cost,
                   SUM(sm.qty) AS total_qty
            FROM sport_material sm
            JOIN sport_item si ON si.id = sm.item_id
            WHERE sm.status = 1 AND si.office_id = %s
            GROUP BY si.id, si.sport_item
            ORDER BY total_cost DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No material cost found."
        lines = [f"- {r['sport_item']}: {r['total_cost']} Cost ({r['total_qty']} Qty)" for r in rows]
        return "Sports Material Cost:\n" + "\n".join(lines)

    elif query_id == "SPORTS_ISSUE_FINE":
        cur.execute("""
            SELECT sii.id, si.sport_item, u.name AS issued_to,
                   sii.issue_date, sii.return_date, sii.fine
            FROM sportitem_issue sii
            JOIN sport_item si ON si.id = sii.sitem_id
            JOIN users u ON u.id = sii.user_id
            WHERE sii.fine > 0 AND u.office_id = %s
            ORDER BY sii.fine DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No issue fines found."
        lines = [f"- {r['issued_to']} fined {r['fine']} for {r['sport_item']} (Due: {r['return_date']})" for r in rows]
        return "Sports Issue Fines:\n" + "\n".join(lines)

    elif query_id == "SPORTS_BY_COURSE":
        cur.execute("""
            SELECT sr.course_id, c.course_name, tc.course_batch,
                   COUNT(sr.id) AS participant_records,
                   SUM(sr.trainee) AS total_trainees
            FROM srec_sport sr
            JOIN training_calendars tc ON tc.id = sr.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE sr.status = 1 AND tc.office_id = %s
            GROUP BY sr.course_id, c.course_name, tc.course_batch
            ORDER BY total_trainees DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No course-wise sports data found."
        lines = [f"- {r['course_name']} ({r['course_batch']}): {r['total_trainees']} Trainees" for r in rows]
        return "Sports by Course:\n" + "\n".join(lines)

    elif query_id == "SPORTS_STATUS_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(id) FROM sport WHERE status=1) AS total_events,
              (SELECT COUNT(id) FROM sport WHERE from_date >= CURDATE() AND status=1) AS upcoming,
              (SELECT COUNT(id) FROM sport WHERE to_date < CURDATE() AND status=1) AS completed,
              (SELECT COUNT(id) FROM sport_team WHERE status=1) AS total_teams,
              (SELECT COUNT(id) FROM sportitem_issue WHERE status=1) AS items_issued
        """)
        r = cur.fetchone()
        if not r: return "Could not generate status summary."
        return (f"Sports Status Summary:\n"
                f"Total Events: {r['total_events']}\n"
                f"Upcoming Events: {r['upcoming']}\n"
                f"Completed Events: {r['completed']}\n"
                f"Total Teams: {r['total_teams']}\n"
                f"Items Issued: {r['items_issued']}")

    elif query_id == "SPORTS_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(id) FROM sport WHERE status=1) AS total_events,
              (SELECT COUNT(id) FROM sport_item WHERE status=1 AND office_id=%s) AS total_items,
              (SELECT SUM(sm.total_price) FROM sport_material sm JOIN sport_item si ON si.id=sm.item_id WHERE sm.status=1 AND si.office_id=%s) AS total_material_cost,
              (SELECT SUM(sii.fine) FROM sportitem_issue sii JOIN sport_item si ON si.id=sii.sitem_id WHERE sii.fine > 0 AND si.office_id=%s) AS total_fines,
              (SELECT COUNT(id) FROM sports_photos WHERE status=1) AS total_photos
        """, (office_id, office_id, office_id))
        r = cur.fetchone()
        if not r: return "Could not generate module summary."
        return (f"Sports Module Summary:\n"
                f"Total Events: {r['total_events']}\n"
                f"Total Items: {r['total_items']}\n"
                f"Total Material Cost: {r['total_material_cost']}\n"
                f"Total Fines: {r['total_fines']}\n"
                f"Total Photos: {r['total_photos']}")

    return None
