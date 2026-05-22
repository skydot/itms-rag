"""Meeting module query templates."""

TEMPLATES = [
    {
        "id": "MEETING_TOTAL",
        "module": "meeting",
        "description": "Total meetings",
        "example_questions": ["Total meetings?", "How many meetings?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "MEETING_UPCOMING",
        "module": "meeting",
        "description": "Upcoming meetings",
        "example_questions": ["Upcoming meetings?", "Future meetings?"],
        "required_params": [],
        "optional_params": ["office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_COMPLETED",
        "module": "meeting",
        "description": "Completed meetings",
        "example_questions": ["Completed meetings?", "Past meetings?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_BY_DATE",
        "module": "meeting",
        "description": "Meeting by date",
        "example_questions": ["Meetings on date?", "Date-wise meetings?"],
        "required_params": [],
        "optional_params": ["date", "from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_AGENDA_LIST",
        "module": "meeting",
        "description": "Meeting agenda list",
        "example_questions": ["Meeting agenda?", "Agenda items?"],
        "required_params": [],
        "optional_params": ["meeting_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_BY_CHAIRMAN",
        "module": "meeting",
        "description": "Meeting by chairman",
        "example_questions": ["Meetings by chairman?", "Chairman's meetings?"],
        "required_params": [],
        "optional_params": ["chairman_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_BY_CREATOR",
        "module": "meeting",
        "description": "Meeting by creator",
        "example_questions": ["Meetings by creator?", "Created meetings?"],
        "required_params": [],
        "optional_params": ["creator_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_INVITEES",
        "module": "meeting",
        "description": "Meeting invitees",
        "example_questions": ["Meeting invitees?", "Who is invited?"],
        "required_params": [],
        "optional_params": ["meeting_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_MOM_SUMMARY",
        "module": "meeting",
        "description": "MOM summary",
        "example_questions": ["Minutes of meeting?", "MOM?"],
        "required_params": [],
        "optional_params": ["meeting_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "MEETING_PENDING_AGENDA",
        "module": "meeting",
        "description": "Pending agenda",
        "example_questions": ["Pending agenda?", "Open agenda items?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_STATUS_SUMMARY",
        "module": "meeting",
        "description": "Meeting status summary",
        "example_questions": ["Meeting status?", "Status summary?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "MEETING_BY_SUBJECT",
        "module": "meeting",
        "description": "Meeting by subject",
        "example_questions": ["Meetings by subject?", "Subject-wise meetings?"],
        "required_params": [],
        "optional_params": ["subject", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_BY_DEPARTMENT",
        "module": "meeting",
        "description": "Meeting by department",
        "example_questions": ["Dept meetings?", "Department-wise meetings?"],
        "required_params": [],
        "optional_params": ["department_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_MONTHLY_COUNT",
        "module": "meeting",
        "description": "Monthly meeting count",
        "example_questions": ["Monthly meetings?", "Meetings this month?"],
        "required_params": [],
        "optional_params": ["month", "year", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "MEETING_FILES",
        "module": "meeting",
        "description": "Meeting files",
        "example_questions": ["Meeting files?", "Attachments?"],
        "required_params": [],
        "optional_params": ["meeting_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_FORWARDED",
        "module": "meeting",
        "description": "Forwarded meetings",
        "example_questions": ["Forwarded meetings?", "Delegated meetings?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_REMATCH",
        "module": "meeting",
        "description": "Re-meetings",
        "example_questions": ["Re-meetings?", "Follow-up meetings?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_ACTION_SUMMARY",
        "module": "meeting",
        "description": "Meeting action summary",
        "example_questions": ["Action items?", "Meeting actions?"],
        "required_params": [],
        "optional_params": ["meeting_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "MEETING_MASTER_LIST",
        "module": "meeting",
        "description": "Meeting master list",
        "example_questions": ["Meeting types?", "Master meeting list?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MEETING_MODULE_SUMMARY",
        "module": "meeting",
        "description": "Meeting module summary",
        "example_questions": ["Meeting summary?", "Meeting module overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute meeting queries."""
    p = params or {}
    
    if query_id == "MEETING_UPCOMING":
        cur.execute("""
            SELECT mc.id, mc.subject, mc.title, mc.date, mc.start_time, mc.end_time,
                   mc.description, mc.m_status,
                   u_creator.name AS created_by_name,
                   u_chair.name AS chairman_name
            FROM meeting_create mc
            LEFT JOIN users u_creator ON u_creator.id = mc.creator
            LEFT JOIN users u_chair ON u_chair.id = mc.chairman
            WHERE mc.date >= CURDATE() AND mc.status = 1
            ORDER BY mc.date ASC, mc.start_time ASC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No upcoming meetings found."
        lines = [f"- {r['title']} ({r['date']} {r['start_time']}): {r['subject']} (Chairman: {r['chairman_name']})" for r in rows]
        return "Upcoming Meetings:\n" + "\n".join(lines)

    elif query_id == "MEETING_COMPLETED":
        cur.execute("""
            SELECT mc.id, mc.subject, mc.title, mc.date, mc.start_time, mc.end_time,
                   mc.mom_meeting_agenda,
                   u_creator.name AS created_by_name,
                   u_chair.name AS chairman_name
            FROM meeting_create mc
            LEFT JOIN users u_creator ON u_creator.id = mc.creator
            LEFT JOIN users u_chair ON u_chair.id = mc.chairman
            WHERE mc.m_status = 3 AND mc.status = 1
            ORDER BY mc.date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No completed meetings found."
        lines = [f"- {r['title']} ({r['date']}): {r['subject']} (Chairman: {r['chairman_name']})" for r in rows]
        return "Completed Meetings:\n" + "\n".join(lines)

    elif query_id == "MEETING_BY_DATE":
        md = p.get("meeting_date") or p.get("date")
        if not md: return "Please specify meeting_date."
        cur.execute("""
            SELECT mc.id, mc.subject, mc.title, mc.date, mc.start_time, mc.end_time,
                   u_creator.name AS created_by_name
            FROM meeting_create mc
            LEFT JOIN users u_creator ON u_creator.id = mc.creator
            WHERE mc.date = %s AND mc.status = 1
            ORDER BY mc.start_time
            LIMIT 50
        """, (md,))
        rows = cur.fetchall()
        if not rows: return f"No meetings found on {md}."
        lines = [f"- {r['title']} at {r['start_time']}: {r['subject']}" for r in rows]
        return f"Meetings on {md}:\n" + "\n".join(lines)

    elif query_id == "MEETING_AGENDA_LIST":
        cur.execute("""
            SELECT ma.id, ma.agenda_title, ma.description, ma.incharge,
                   ma.mom_description, ma.a_status
            FROM meeting_agenda ma
            WHERE ma.office_id = %s AND ma.status = 1
            ORDER BY ma.no
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No agenda items found."
        lines = [f"- {r['agenda_title']}: {r['description']} (Status: {r['a_status']})" for r in rows]
        return "Meeting Agenda List:\n" + "\n".join(lines)

    elif query_id == "MEETING_BY_CHAIRMAN":
        uid = p.get("user_id") or p.get("chairman")
        if not uid: return "Please specify user_id."
        cur.execute("""
            SELECT mc.id, mc.subject, mc.title, mc.date, mc.start_time,
                   u_chair.name AS chairman
            FROM meeting_create mc
            JOIN users u_chair ON u_chair.id = mc.chairman
            WHERE mc.chairman = %s AND mc.status = 1
            ORDER BY mc.date DESC
            LIMIT 50
        """, (uid,))
        rows = cur.fetchall()
        if not rows: return f"No meetings found for chairman {uid}."
        lines = [f"- {r['title']} ({r['date']}): {r['subject']}" for r in rows]
        return f"Meetings chaired by {uid}:\n" + "\n".join(lines)

    elif query_id == "MEETING_BY_CREATOR":
        uid = p.get("user_id") or p.get("creator")
        if not uid: return "Please specify user_id."
        cur.execute("""
            SELECT mc.id, mc.subject, mc.title, mc.date, mc.start_time, mc.m_status
            FROM meeting_create mc
            WHERE mc.creator = %s AND mc.status = 1
            ORDER BY mc.date DESC
            LIMIT 50
        """, (uid,))
        rows = cur.fetchall()
        if not rows: return f"No meetings found created by {uid}."
        lines = [f"- {r['title']} ({r['date']}): {r['subject']} (Status: {r['m_status']})" for r in rows]
        return f"Meetings created by {uid}:\n" + "\n".join(lines)

    elif query_id == "MEETING_INVITEES":
        uid = p.get("user_id")
        if not uid: return "Please specify user_id."
        cur.execute("""
            SELECT mc.id, mc.subject, mc.date, mc.invitee,
                   u_chair.name AS chairman
            FROM meeting_create mc
            LEFT JOIN users u_chair ON u_chair.id = mc.chairman
            WHERE FIND_IN_SET(%s, mc.invitee) AND mc.status = 1
            ORDER BY mc.date DESC
            LIMIT 50
        """, (uid,))
        rows = cur.fetchall()
        if not rows: return f"No meetings found inviting {uid}."
        lines = [f"- {r['subject']} ({r['date']}), Chairman: {r['chairman']}" for r in rows]
        return f"Meetings Inviting {uid}:\n" + "\n".join(lines)

    elif query_id == "MEETING_MOM_SUMMARY":
        cur.execute("""
            SELECT mc.id, mc.subject, mc.date,
                   mc.mom_meeting_agenda, mc.meeting_file_no,
                   u_chair.name AS chairman
            FROM meeting_create mc
            LEFT JOIN users u_chair ON u_chair.id = mc.chairman
            WHERE mc.mom_meeting_agenda IS NOT NULL AND mc.status = 1
            ORDER BY mc.date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No MoM summaries found."
        lines = [f"- {r['subject']} ({r['date']}): {r['mom_meeting_agenda']}" for r in rows]
        return "MoM Summaries:\n" + "\n".join(lines)

    elif query_id == "MEETING_PENDING_AGENDA":
        cur.execute("""
            SELECT ma.id, ma.agenda_title, ma.description, ma.a_status,
                   ma.incharge
            FROM meeting_agenda ma
            WHERE ma.a_status IN (1, 2) AND ma.status = 1 AND ma.office_id = %s
            ORDER BY ma.created_at DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No pending agenda items found."
        lines = [f"- {r['agenda_title']}: {r['description']} (Incharge: {r['incharge']})" for r in rows]
        return "Pending Agenda:\n" + "\n".join(lines)

    elif query_id == "MEETING_STATUS_SUMMARY":
        cur.execute("""
            SELECT mc.m_status,
                   CASE mc.m_status
                     WHEN 0 THEN 'Draft'
                     WHEN 1 THEN 'Pending'
                     WHEN 2 THEN 'Forwarded'
                     WHEN 3 THEN 'Approved'
                   END AS status_label,
                   COUNT(mc.id) AS count
            FROM meeting_create mc
            WHERE mc.status = 1
            GROUP BY mc.m_status
        """)
        rows = cur.fetchall()
        if not rows: return "No meeting status summary found."
        lines = [f"- {r['status_label']}: {r['count']} Meetings" for r in rows]
        return "Meeting Status Summary:\n" + "\n".join(lines)

    elif query_id == "MEETING_BY_SUBJECT":
        kw = p.get("keyword") or p.get("subject")
        if not kw: return "Please specify keyword."
        cur.execute("""
            SELECT mc.id, mc.subject, mc.title, mc.date, mc.m_status,
                   u_creator.name AS created_by
            FROM meeting_create mc
            LEFT JOIN users u_creator ON u_creator.id = mc.creator
            WHERE mc.subject LIKE CONCAT('%%', %s, '%%') AND mc.status = 1
            ORDER BY mc.date DESC
            LIMIT 50
        """, (kw,))
        rows = cur.fetchall()
        if not rows: return f"No meetings found matching '{kw}'."
        lines = [f"- {r['title']} ({r['date']}): {r['subject']}" for r in rows]
        return f"Meetings matching '{kw}':\n" + "\n".join(lines)

    elif query_id == "MEETING_BY_DEPARTMENT":
        cur.execute("""
            SELECT mc.id, mc.subject, mc.date,
                   u_chair.name AS chairman,
                   mc.description
            FROM meeting_create mc
            LEFT JOIN users u_chair ON u_chair.id = mc.chairman
            WHERE mc.status = 1
            ORDER BY mc.date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No department meeting data found."
        lines = [f"- {r['subject']} ({r['date']}), Chairman: {r['chairman']}" for r in rows]
        return "Meetings by Department:\n" + "\n".join(lines)

    elif query_id == "MEETING_MONTHLY_COUNT":
        cur.execute("""
            SELECT YEAR(mc.date) AS yr, MONTH(mc.date) AS mo,
                   MONTHNAME(mc.date) AS month_name,
                   COUNT(mc.id) AS meeting_count
            FROM meeting_create mc
            WHERE mc.status = 1
            GROUP BY YEAR(mc.date), MONTH(mc.date)
            ORDER BY yr DESC, mo DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No monthly meeting data found."
        lines = [f"- {r['month_name']} {r['yr']}: {r['meeting_count']} Meetings" for r in rows]
        return "Monthly Meeting Count:\n" + "\n".join(lines)

    elif query_id == "MEETING_FILES":
        cur.execute("""
            SELECT mc.id, mc.subject, mc.date, mc.meeting_file_no
            FROM meeting_create mc
            WHERE mc.meeting_file_no IS NOT NULL AND mc.status = 1
            ORDER BY mc.date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No meeting files found."
        lines = [f"- {r['subject']} ({r['date']}): File {r['meeting_file_no']}" for r in rows]
        return "Meeting Files:\n" + "\n".join(lines)

    elif query_id == "MEETING_FORWARDED":
        cur.execute("""
            SELECT mc.id, mc.subject, mc.date, mc.m_status,
                   mc.forward_id, fu.name AS forwarded_to,
                   mc.remarks_forward
            FROM meeting_create mc
            LEFT JOIN users fu ON fu.id = mc.forward_id
            WHERE mc.m_status = 2 AND mc.status = 1
            ORDER BY mc.date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No forwarded meetings found."
        lines = [f"- {r['subject']} ({r['date']}): Forwarded to {r['forwarded_to']} (Remarks: {r['remarks_forward']})" for r in rows]
        return "Forwarded Meetings:\n" + "\n".join(lines)

    elif query_id == "MEETING_REMATCH":
        cur.execute("""
            SELECT mc.id, mc.subject, mc.date, mc.re_meeting_id,
                   mc2.subject AS original_meeting
            FROM meeting_create mc
            LEFT JOIN meeting_create mc2 ON mc2.id = mc.re_meeting_id
            WHERE mc.re_meeting_id > 0 AND mc.status = 1
            ORDER BY mc.date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No rematched meetings found."
        lines = [f"- {r['subject']} ({r['date']}): Rematch of {r['original_meeting']}" for r in rows]
        return "Rematched Meetings:\n" + "\n".join(lines)

    elif query_id == "MEETING_ACTION_SUMMARY":
        cur.execute("""
            SELECT ma.id, ma.agenda_title, ma.a_status,
                   CASE ma.a_status
                     WHEN 1 THEN 'Pending'
                     WHEN 2 THEN 'In Progress'
                     WHEN 3 THEN 'Completed'
                     WHEN 4 THEN 'Dropped'
                   END AS status_label,
                   ma.mom_description
            FROM meeting_agenda ma
            WHERE ma.status = 1 AND ma.office_id = %s
            ORDER BY ma.a_status, ma.created_at
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No action summary found."
        lines = [f"- {r['agenda_title']}: {r['status_label']} ({r['mom_description']})" for r in rows]
        return "Meeting Action Summary:\n" + "\n".join(lines)

    elif query_id == "MEETING_MASTER_LIST":
        cur.execute("""
            SELECT mm.id, mm.meeting_name, mm.status, mm.created_at
            FROM meeting_master mm
            WHERE mm.status = 1
            ORDER BY mm.meeting_name
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No meeting master lists found."
        lines = [f"- {r['meeting_name']}" for r in rows]
        return "Meeting Master List:\n" + "\n".join(lines)

    elif query_id == "MEETING_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(id) FROM meeting_create WHERE status=1) AS total_meetings,
              (SELECT COUNT(id) FROM meeting_create WHERE date >= CURDATE() AND status=1) AS upcoming,
              (SELECT COUNT(id) FROM meeting_create WHERE m_status=3 AND status=1) AS completed,
              (SELECT COUNT(id) FROM meeting_agenda WHERE a_status IN(1,2) AND status=1 AND office_id=%s) AS pending_actions,
              (SELECT COUNT(id) FROM meeting_create WHERE date=CURDATE() AND status=1) AS today_meetings
        """, (office_id,))
        r = cur.fetchone()
        if not r: return "Could not generate meeting module summary."
        return (f"Meeting Module Summary:\n"
                f"Total Meetings: {r['total_meetings']}\n"
                f"Upcoming Meetings: {r['upcoming']}\n"
                f"Today's Meetings: {r['today_meetings']}\n"
                f"Completed Meetings: {r['completed']}\n"
                f"Pending Actions: {r['pending_actions']}")

    return None
