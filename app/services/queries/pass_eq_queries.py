"""Pass and EQ module query templates."""

TEMPLATES = [
    {
        "id": "PASS_EQ_TOTAL_PASS",
        "module": "pass_eq",
        "description": "Total pass requests",
        "example_questions": ["Total pass requests?", "How many pass applications?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_PENDING",
        "module": "pass_eq",
        "description": "Pending pass",
        "example_questions": ["Pending pass?", "Awaiting approval?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "PASS_EQ_APPROVED",
        "module": "pass_eq",
        "description": "Approved pass",
        "example_questions": ["Approved pass?", "Granted passes?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_BY_USER",
        "module": "pass_eq",
        "description": "Pass by user",
        "example_questions": ["Pass by user?", "User's pass history?"],
        "required_params": [],
        "optional_params": ["user_id", "user_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff", "trainee"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_BY_YEAR",
        "module": "pass_eq",
        "description": "Pass by year",
        "example_questions": ["Pass by year?", "Year-wise pass?"],
        "required_params": [],
        "optional_params": ["year", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_TYPE_SUMMARY",
        "module": "pass_eq",
        "description": "Pass type summary",
        "example_questions": ["Pass type summary?", "By pass type?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_TOTAL_EQ",
        "module": "pass_eq",
        "description": "EQ requests",
        "example_questions": ["Total EQ?", "How many EQ requests?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_BY_JOURNEY_DATE",
        "module": "pass_eq",
        "description": "EQ by journey date",
        "example_questions": ["EQ by journey date?", "Journey-wise EQ?"],
        "required_params": [],
        "optional_params": ["journey_date", "from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_TICKET_STATUS",
        "module": "pass_eq",
        "description": "EQ ticket status",
        "example_questions": ["EQ ticket status?", "Ticket confirmed?"],
        "required_params": [],
        "optional_params": ["eq_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff", "trainee"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_TRAIN_CLASS_SUMMARY",
        "module": "pass_eq",
        "description": "Train class summary",
        "example_questions": ["Train class summary?", "Class-wise pass?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_STATION_SUMMARY",
        "module": "pass_eq",
        "description": "Station/from-to summary",
        "example_questions": ["Station summary?", "Route-wise pass?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_PNR_SEARCH",
        "module": "pass_eq",
        "description": "PNR search",
        "example_questions": ["Search PNR?", "Find by PNR?"],
        "required_params": [],
        "optional_params": ["pnr_number", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "PASS_EQ_PASSENGER_LIST",
        "module": "pass_eq",
        "description": "Passenger list",
        "example_questions": ["Passenger list?", "Who is traveling?"],
        "required_params": [],
        "optional_params": ["pass_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_ISSUE_DATE_SUMMARY",
        "module": "pass_eq",
        "description": "Pass issue date summary",
        "example_questions": ["Issue date summary?", "When issued?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_STATUS_SUMMARY",
        "module": "pass_eq",
        "description": "Pass status summary",
        "example_questions": ["Pass status?", "Approval status?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_EQ_STATUS_SUMMARY",
        "module": "pass_eq",
        "description": "EQ status summary",
        "example_questions": ["EQ status?", "EQ approval status?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_REMARKS",
        "module": "pass_eq",
        "description": "Pass remarks",
        "example_questions": ["Pass remarks?", "Comments on pass?"],
        "required_params": [],
        "optional_params": ["pass_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_RETURN_ROUTE",
        "module": "pass_eq",
        "description": "Pass return route",
        "example_questions": ["Return route?", "Return journey?"],
        "required_params": [],
        "optional_params": ["pass_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_BY_COURSE",
        "module": "pass_eq",
        "description": "Pass/EQ by course",
        "example_questions": ["Pass by course?", "Course-wise EQ?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "PASS_EQ_MODULE_SUMMARY",
        "module": "pass_eq",
        "description": "Pass/EQ module summary",
        "example_questions": ["Pass/EQ summary?", "Pass EQ module overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute pass EQ queries."""
    p = params or {}
    
    if query_id == "PASS_EQ_PENDING":
        cur.execute("""
            SELECT p.id, u.name, p.pass_year, pt.pass_type,
                   p.out_from, p.out_to, p.issue_date, p.p_status
            FROM pass p
            JOIN users u ON u.id = p.user_id
            JOIN pass_type pt ON pt.id = p.pass_type
            WHERE p.p_status = 1 AND p.status = 1 AND u.office_id = %s
            ORDER BY p.created_at DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No pending passes found."
        lines = [f"- {r['name']} ({r['pass_year']}): {r['out_from']} to {r['out_to']} (Type: {r['pass_type']})" for r in rows]
        return "Pending Passes:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_APPROVED":
        cur.execute("""
            SELECT p.id, u.name, p.pass_year, pt.pass_type,
                   p.out_from, p.out_to, p.pass_no, p.issue_date
            FROM pass p
            JOIN users u ON u.id = p.user_id
            JOIN pass_type pt ON pt.id = p.pass_type
            WHERE p.p_status = 3 AND p.status = 1 AND u.office_id = %s
            ORDER BY p.issue_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No approved passes found."
        lines = [f"- {r['name']} (Pass No: {r['pass_no']}): {r['out_from']} to {r['out_to']} ({r['issue_date']})" for r in rows]
        return "Approved Passes:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_BY_USER":
        uid = p.get("user_id")
        if not uid: return "Please specify user_id."
        cur.execute("""
            SELECT p.id, pt.pass_type, p.pass_year,
                   p.out_from, p.out_to, p.out_via,
                   p.return_from, p.return_to, p.pass_no,
                   p.issue_date, p.p_status
            FROM pass p
            JOIN pass_type pt ON pt.id = p.pass_type
            WHERE p.user_id = %s AND p.status = 1
            ORDER BY p.pass_year DESC, p.issue_date DESC
            LIMIT 50
        """, (uid,))
        rows = cur.fetchall()
        if not rows: return f"No passes found for user {uid}."
        lines = [f"- {r['pass_type']} ({r['pass_year']}): {r['out_from']} to {r['out_to']} (Pass No: {r['pass_no']})" for r in rows]
        return f"Passes for User {uid}:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_BY_YEAR":
        cur.execute("""
            SELECT p.pass_year,
                   COUNT(p.id) AS total_passes,
                   SUM(CASE WHEN p.p_status = 3 THEN 1 ELSE 0 END) AS approved
            FROM pass p
            JOIN users u ON u.id = p.user_id
            WHERE p.status = 1 AND u.office_id = %s
            GROUP BY p.pass_year
            ORDER BY p.pass_year DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No year-wise pass data found."
        lines = [f"- {r['pass_year']}: {r['total_passes']} Total, {r['approved']} Approved" for r in rows]
        return "Passes by Year:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_TYPE_SUMMARY":
        cur.execute("""
            SELECT pt.pass_type, COUNT(p.id) AS total
            FROM pass_type pt
            LEFT JOIN pass p ON p.pass_type = pt.id AND p.status = 1
            LEFT JOIN users u ON u.id = p.user_id
            WHERE pt.status = 1 AND (u.office_id = %s OR u.office_id IS NULL)
            GROUP BY pt.id, pt.pass_type
            ORDER BY total DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No pass type summary found."
        lines = [f"- {r['pass_type']}: {r['total']} Passes" for r in rows]
        return "Pass Type Summary:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_TOTAL_EQ":
        cur.execute("""
            SELECT COUNT(e.id) AS total_eq_requests
            FROM eqs e
            JOIN users u ON u.id = e.user_id
            WHERE e.status = 1 AND u.office_id = %s
        """, (office_id,))
        r = cur.fetchone()
        return f"Total EQ Requests: {r['total_eq_requests'] or 0}"

    elif query_id == "PASS_EQ_BY_JOURNEY_DATE":
        jd = p.get("journey_date") or p.get("date")
        if not jd: return "Please specify journey_date."
        cur.execute("""
            SELECT e.id, u.name, e.journey_date, e.dep_time,
                   e.train_no, e.from_place, e.to_place, e.pnr,
                   e.ticket_status, e.eq_class
            FROM eqs e
            JOIN users u ON u.id = e.user_id
            WHERE DATE(e.journey_date) = %s AND e.status = 1 AND u.office_id = %s
            ORDER BY e.dep_time
            LIMIT 50
        """, (jd, office_id))
        rows = cur.fetchall()
        if not rows: return f"No EQ requests found for date {jd}."
        lines = [f"- {r['name']}: {r['from_place']} to {r['to_place']} (Train {r['train_no']}, PNR: {r['pnr']})" for r in rows]
        return f"EQ Requests on {jd}:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_TICKET_STATUS":
        cur.execute("""
            SELECT e.ticket_status, COUNT(e.id) AS count
            FROM eqs e
            JOIN users u ON u.id = e.user_id
            WHERE e.status = 1 AND u.office_id = %s
            GROUP BY e.ticket_status
            ORDER BY count DESC
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No EQ ticket status summary found."
        lines = [f"- {r['ticket_status']}: {r['count']} Tickets" for r in rows]
        return "EQ Ticket Status:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_TRAIN_CLASS_SUMMARY":
        cur.execute("""
            SELECT e.eq_class, COUNT(e.id) AS count
            FROM eqs e
            JOIN users u ON u.id = e.user_id
            WHERE e.status = 1 AND u.office_id = %s
            GROUP BY e.eq_class
            ORDER BY count DESC
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No train class summary found."
        lines = [f"- {r['eq_class']}: {r['count']} Tickets" for r in rows]
        return "Train Class Summary:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_STATION_SUMMARY":
        cur.execute("""
            SELECT e.from_place, e.to_place, COUNT(e.id) AS journey_count
            FROM eqs e
            JOIN users u ON u.id = e.user_id
            WHERE e.status = 1 AND u.office_id = %s
            GROUP BY e.from_place, e.to_place
            ORDER BY journey_count DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No station summary found."
        lines = [f"- {r['from_place']} to {r['to_place']}: {r['journey_count']} Journeys" for r in rows]
        return "EQ Station Summary:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_PNR_SEARCH":
        pnr = p.get("pnr")
        if not pnr: return "Please specify PNR."
        cur.execute("""
            SELECT e.id, u.name, e.pnr, e.journey_date,
                   e.train_no, e.from_place, e.to_place, e.ticket_status
            FROM eqs e
            JOIN users u ON u.id = e.user_id
            WHERE e.pnr = %s AND e.status = 1 AND u.office_id = %s
            LIMIT 10
        """, (pnr, office_id))
        rows = cur.fetchall()
        if not rows: return f"No EQ found for PNR {pnr}."
        lines = [f"- {r['name']}: {r['from_place']} to {r['to_place']} on {r['journey_date']} (Status: {r['ticket_status']})" for r in rows]
        return f"PNR {pnr} details:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_PASSENGER_LIST":
        cur.execute("""
            SELECT e.id, u.name, e.journey_date, e.train_no,
                   e.passenger, e.passenger2, e.passenger3, e.passenger4
            FROM eqs e
            JOIN users u ON u.id = e.user_id
            WHERE e.status = 1 AND u.office_id = %s
            ORDER BY e.journey_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No passenger lists found."
        lines = []
        for r in rows:
            passengers = [x for x in [r['passenger'], r['passenger2'], r['passenger3'], r['passenger4']] if x]
            lines.append(f"- Train {r['train_no']} on {r['journey_date']} (Req by {r['name']}): " + ", ".join(passengers))
        return "EQ Passenger List:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_ISSUE_DATE_SUMMARY":
        cur.execute("""
            SELECT DATE(p.issue_date) AS issue_date, COUNT(p.id) AS passes_issued
            FROM pass p
            JOIN users u ON u.id = p.user_id
            WHERE p.status = 1 AND p.p_status = 3 AND u.office_id = %s
            GROUP BY DATE(p.issue_date)
            ORDER BY issue_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No issue date summary found."
        lines = [f"- {r['issue_date']}: {r['passes_issued']} Passes Issued" for r in rows]
        return "Pass Issue Summary:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_STATUS_SUMMARY":
        cur.execute("""
            SELECT p.p_status,
                   COUNT(p.id) AS count
            FROM pass p
            JOIN users u ON u.id = p.user_id
            WHERE p.status = 1 AND u.office_id = %s
            GROUP BY p.p_status
            ORDER BY count DESC
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No pass status summary found."
        lines = [f"- Status {r['p_status']}: {r['count']} Passes" for r in rows]
        return "Pass Status Summary:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_EQ_STATUS_SUMMARY":
        cur.execute("""
            SELECT e.eq_status,
                   COUNT(e.id) AS count
            FROM eqs e
            JOIN users u ON u.id = e.user_id
            WHERE e.status = 1 AND u.office_id = %s
            GROUP BY e.eq_status
            ORDER BY count DESC
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No EQ status summary found."
        lines = [f"- Status {r['eq_status']}: {r['count']} Requests" for r in rows]
        return "EQ Status Summary:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_REMARKS":
        cur.execute("""
            SELECT p.id, u.name, p.pass_year, p.remarks, p.issue_date
            FROM pass p
            JOIN users u ON u.id = p.user_id
            WHERE p.remarks IS NOT NULL AND p.status = 1 AND u.office_id = %s
            ORDER BY p.issue_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No remarks found on passes."
        lines = [f"- {r['name']} ({r['pass_year']}): {r['remarks']}" for r in rows]
        return "Pass Remarks:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_RETURN_ROUTE":
        cur.execute("""
            SELECT p.id, u.name,
                   p.return_from, p.return_to, p.return_via, p.return_break,
                   p.pass_year, p.pass_no
            FROM pass p
            JOIN users u ON u.id = p.user_id
            WHERE p.return_from IS NOT NULL AND p.status = 1 AND u.office_id = %s
            ORDER BY p.issue_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No return routes found."
        lines = [f"- {r['name']} ({r['pass_no']}): {r['return_from']} to {r['return_to']} via {r['return_via']}" for r in rows]
        return "Return Routes:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_BY_COURSE":
        cur.execute("""
            SELECT tc.course_batch, c.course_name,
                   COUNT(p.id) AS total_passes
            FROM pass p
            JOIN users u ON u.id = p.user_id
            JOIN tra_masters tm ON tm.user_id = u.id
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE p.status = 1 AND tc.office_id = %s
            GROUP BY tm.course_id, tc.course_batch, c.course_name
            ORDER BY total_passes DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No course-wise pass data found."
        lines = [f"- {r['course_name']} ({r['course_batch']}): {r['total_passes']} Passes" for r in rows]
        return "Passes by Course:\n" + "\n".join(lines)

    elif query_id == "PASS_EQ_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(id) FROM pass p JOIN users u ON u.id=p.user_id WHERE p.status=1 AND u.office_id=%s) AS total_passes,
              (SELECT COUNT(id) FROM eqs e JOIN users u ON u.id=e.user_id WHERE e.status=1 AND u.office_id=%s) AS total_eq,
              (SELECT COUNT(id) FROM pass p JOIN users u ON u.id=p.user_id WHERE p.p_status=1 AND p.status=1 AND u.office_id=%s) AS pending_passes,
              (SELECT COUNT(id) FROM pass p JOIN users u ON u.id=p.user_id WHERE p.p_status=3 AND p.status=1 AND u.office_id=%s) AS approved_passes,
              (SELECT COUNT(id) FROM eqs e JOIN users u ON u.id=e.user_id WHERE e.journey_date >= CURDATE() AND e.status=1 AND u.office_id=%s) AS upcoming_journeys
        """, (office_id, office_id, office_id, office_id, office_id))
        r = cur.fetchone()
        if not r: return "Could not generate pass/EQ module summary."
        return (f"Pass & EQ Module Summary:\n"
                f"Total Passes: {r['total_passes']}\n"
                f"Total EQ Requests: {r['total_eq']}\n"
                f"Pending Passes: {r['pending_passes']}\n"
                f"Approved Passes: {r['approved_passes']}\n"
                f"Upcoming Journeys: {r['upcoming_journeys']}")

    return None
