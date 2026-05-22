"""Inspection module query templates."""

TEMPLATES = [
    {
        "id": "INSPECTION_TOTAL",
        "module": "inspection",
        "description": "Total inspection notes",
        "example_questions": ["Total inspections?", "How many inspections?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_BY_DATE",
        "module": "inspection",
        "description": "Inspection by date",
        "example_questions": ["Inspections on date?", "Date-wise inspections?"],
        "required_params": [],
        "optional_params": ["date", "from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_DESCRIPTIONS",
        "module": "inspection",
        "description": "Inspection descriptions",
        "example_questions": ["Inspection descriptions?", "Inspection details?"],
        "required_params": [],
        "optional_params": ["inspection_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_BY_FACULTY",
        "module": "inspection",
        "description": "Inspection by faculty/user",
        "example_questions": ["Inspections by faculty?", "Faculty inspections?"],
        "required_params": [],
        "optional_params": ["faculty_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_STATUS_SUMMARY",
        "module": "inspection",
        "description": "Inspection status summary",
        "example_questions": ["Inspection status?", "Status summary?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_PENDING",
        "module": "inspection",
        "description": "Pending inspections",
        "example_questions": ["Pending inspections?", "Awaiting inspection?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_COMPLETED",
        "module": "inspection",
        "description": "Completed inspections",
        "example_questions": ["Completed inspections?", "Done inspections?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_REMARKS",
        "module": "inspection",
        "description": "Inspection remarks",
        "example_questions": ["Inspection remarks?", "Comments on inspection?"],
        "required_params": [],
        "optional_params": ["inspection_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_BY_OFFICE",
        "module": "inspection",
        "description": "Inspection by office",
        "example_questions": ["Office inspections?", "Office-wise inspections?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_FILES",
        "module": "inspection",
        "description": "Inspection file uploads",
        "example_questions": ["Inspection files?", "Uploaded documents?"],
        "required_params": [],
        "optional_params": ["inspection_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_BY_TYPE",
        "module": "inspection",
        "description": "Inspection by type",
        "example_questions": ["Inspections by type?", "Type-wise inspections?"],
        "required_params": [],
        "optional_params": ["type_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_ACTION_NOTES",
        "module": "inspection",
        "description": "Inspection action notes",
        "example_questions": ["Action notes?", "Inspection actions?"],
        "required_params": [],
        "optional_params": ["inspection_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_DATE_RANGE",
        "module": "inspection",
        "description": "Inspection date range",
        "example_questions": ["Inspections in range?", "Date range inspections?"],
        "required_params": [],
        "optional_params": ["from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_MONTHLY_COUNT",
        "module": "inspection",
        "description": "Monthly inspection count",
        "example_questions": ["Monthly inspections?", "Inspections this month?"],
        "required_params": [],
        "optional_params": ["month", "year", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_TITLE_SEARCH",
        "module": "inspection",
        "description": "Inspection title search",
        "example_questions": ["Find inspection by title?", "Search inspection?"],
        "required_params": [],
        "optional_params": ["title", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_DESC_SEARCH",
        "module": "inspection",
        "description": "Inspection description search",
        "example_questions": ["Search inspection description?", "Find in inspection?"],
        "required_params": [],
        "optional_params": ["keyword", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_COPY_TO_SUMMARY",
        "module": "inspection",
        "description": "Inspection copy_to summary",
        "example_questions": ["Inspection copies?", "Shared with whom?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_DEPT_SUMMARY",
        "module": "inspection",
        "description": "Inspection department summary",
        "example_questions": ["Dept-wise inspections?", "Inspection by department?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_LATEST",
        "module": "inspection",
        "description": "Inspection latest notes",
        "example_questions": ["Latest inspections?", "Recent inspections?"],
        "required_params": [],
        "optional_params": ["office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "INSPECTION_MODULE_SUMMARY",
        "module": "inspection",
        "description": "Inspection module summary",
        "example_questions": ["Inspection summary?", "Inspection module overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute inspection queries."""
    p = params or {}
    
    if query_id == "INSPECTION_TOTAL":
        cur.execute("SELECT COUNT(*) AS total FROM inspection_notes WHERE office_id = %s AND status = 1", (office_id,))
        r = cur.fetchone()
        return f"Total inspection notes: {r['total'] if r else 0}"

    elif query_id == "INSPECTION_BY_DATE":
        fdate = p.get("from_date") or p.get("date")
        if not fdate: return "Please specify from_date."
        cur.execute("""
            SELECT ins.id, ins.title, ins.from_date, ins.to_date,
                   ins.ins_date, ins.short_desc, ins.file_no
            FROM inspection_notes ins
            WHERE ins.from_date = %s AND ins.status = 1 AND ins.office_id = %s
            ORDER BY ins.created_at DESC
            LIMIT 50
        """, (fdate, office_id))
        rows = cur.fetchall()
        if not rows: return f"No inspections found for date {fdate}."
        lines = [f"- {r['title']} ({r['from_date']} to {r['to_date']}): {r['short_desc']}" for r in rows]
        return f"Inspections on {fdate}:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_DESCRIPTIONS":
        cur.execute("""
            SELECT ind.id, ind.description, ind.in_type, ind.i_status,
                   ind.remarks, ind.remarks_log,
                   ins.title AS inspection_title, ins.from_date, ins.to_date
            FROM inspection_description ind
            JOIN inspection_notes ins ON ins.id = ind.insp_id
            WHERE ind.status = 1 AND ins.office_id = %s
            ORDER BY ind.created_at DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No inspection descriptions found."
        lines = [f"- {r['inspection_title']} ({r['in_type']}): {r['description']}" for r in rows]
        return "Inspection Descriptions:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_BY_FACULTY":
        uid = p.get("user_id") or p.get("faculty_id")
        if not uid: return "Please specify user_id."
        cur.execute("""
            SELECT ind.id, ind.description, ind.in_type, ind.faculty_id,
                   ins.title, ins.from_date
            FROM inspection_description ind
            JOIN inspection_notes ins ON ins.id = ind.insp_id
            WHERE FIND_IN_SET(%s, ind.faculty_id)
              AND ind.status = 1 AND ins.office_id = %s
            ORDER BY ins.from_date DESC
            LIMIT 50
        """, (uid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No inspections found for faculty {uid}."
        lines = [f"- {r['title']} ({r['from_date']}): {r['description']}" for r in rows]
        return f"Inspections for Faculty {uid}:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_STATUS_SUMMARY":
        cur.execute("""
            SELECT ind.i_status,
                   CASE ind.i_status
                     WHEN 0 THEN 'Pending'
                     WHEN 1 THEN 'In Progress'
                     WHEN 2 THEN 'Completed'
                     WHEN 3 THEN 'Closed'
                   END AS status_label,
                   COUNT(ind.id) AS count
            FROM inspection_description ind
            JOIN inspection_notes ins ON ins.id = ind.insp_id
            WHERE ind.status = 1 AND ins.office_id = %s
            GROUP BY ind.i_status
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No status summary found."
        lines = [f"- {r['status_label']}: {r['count']} Items" for r in rows]
        return "Inspection Status Summary:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_PENDING":
        cur.execute("""
            SELECT ind.id, ind.description, ind.in_type,
                   ins.title, ins.from_date, ins.to_date, ins.short_desc
            FROM inspection_description ind
            JOIN inspection_notes ins ON ins.id = ind.insp_id
            WHERE ind.i_status = 0 AND ind.status = 1 AND ins.office_id = %s
            ORDER BY ins.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No pending inspections found."
        lines = [f"- {r['title']}: {r['description']}" for r in rows]
        return "Pending Inspections:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_COMPLETED":
        cur.execute("""
            SELECT ind.id, ind.description, ind.in_type,
                   ind.remarks, ins.title, ins.from_date
            FROM inspection_description ind
            JOIN inspection_notes ins ON ins.id = ind.insp_id
            WHERE ind.i_status = 2 AND ind.status = 1 AND ins.office_id = %s
            ORDER BY ins.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No completed inspections found."
        lines = [f"- {r['title']} ({r['from_date']}): {r['description']} (Remarks: {r['remarks']})" for r in rows]
        return "Completed Inspections:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_REMARKS":
        cur.execute("""
            SELECT ind.id, ind.remarks, ind.remarks_log,
                   ins.title, ins.from_date
            FROM inspection_description ind
            JOIN inspection_notes ins ON ins.id = ind.insp_id
            WHERE ind.remarks IS NOT NULL AND ind.status = 1 AND ins.office_id = %s
            ORDER BY ins.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No remarks found."
        lines = [f"- {r['title']}: {r['remarks']}" for r in rows]
        return "Inspection Remarks:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_BY_OFFICE":
        cur.execute("""
            SELECT ins.id, ins.title, ins.from_date, ins.to_date,
                   ins.short_desc, ins.office_id, COUNT(ind.id) AS description_count
            FROM inspection_notes ins
            LEFT JOIN inspection_description ind ON ind.insp_id = ins.id AND ind.status = 1
            WHERE ins.office_id = %s AND ins.status = 1
            GROUP BY ins.id, ins.title, ins.from_date, ins.to_date, ins.short_desc, ins.office_id
            ORDER BY ins.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return f"No inspections found for office {office_id}."
        lines = [f"- {r['title']} ({r['from_date']}): {r['description_count']} Items" for r in rows]
        return f"Inspections for Office {office_id}:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_FILES":
        cur.execute("""
            SELECT ins.id, ins.title, ins.file_upload, ins.from_date
            FROM inspection_notes ins
            WHERE ins.file_upload IS NOT NULL AND ins.status = 1 AND ins.office_id = %s
            ORDER BY ins.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No inspection files found."
        lines = [f"- {r['title']} ({r['from_date']}): File {r['file_upload']}" for r in rows]
        return "Inspection Files:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_BY_TYPE":
        cur.execute("""
            SELECT ind.in_type, COUNT(ind.id) AS count
            FROM inspection_description ind
            JOIN inspection_notes ins ON ins.id = ind.insp_id
            WHERE ind.status = 1 AND ins.office_id = %s
            GROUP BY ind.in_type
            ORDER BY count DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No inspection types found."
        lines = [f"- Type {r['in_type']}: {r['count']} Items" for r in rows]
        return "Inspections by Type:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_ACTION_NOTES":
        cur.execute("""
            SELECT ind.id, ind.description, ind.in_type,
                   ind.remarks_log, ind.remarks, ind.i_status,
                   ins.title, ins.from_date
            FROM inspection_description ind
            JOIN inspection_notes ins ON ins.id = ind.insp_id
            WHERE ind.remarks_log IS NOT NULL AND ind.status = 1 AND ins.office_id = %s
            ORDER BY ind.updated_at DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No action notes found."
        lines = [f"- {r['title']}: {r['description']} -> {r['remarks_log']}" for r in rows]
        return "Inspection Action Notes:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_DATE_RANGE":
        fdate = p.get("from_date")
        tdate = p.get("to_date")
        if not fdate or not tdate: return "Please specify from_date and to_date."
        cur.execute("""
            SELECT ins.id, ins.title, ins.from_date, ins.to_date,
                   ins.short_desc, COUNT(ind.id) AS description_count
            FROM inspection_notes ins
            LEFT JOIN inspection_description ind ON ind.insp_id = ins.id AND ind.status = 1
            WHERE ins.from_date BETWEEN %s AND %s AND ins.status = 1 AND ins.office_id = %s
            GROUP BY ins.id, ins.title, ins.from_date, ins.to_date, ins.short_desc
            ORDER BY ins.from_date
            LIMIT 50
        """, (fdate, tdate, office_id))
        rows = cur.fetchall()
        if not rows: return "No inspections found in date range."
        lines = [f"- {r['title']} ({r['from_date']} to {r['to_date']}): {r['description_count']} Items" for r in rows]
        return f"Inspections ({fdate} to {tdate}):\n" + "\n".join(lines)

    elif query_id == "INSPECTION_MONTHLY_COUNT":
        cur.execute("""
            SELECT YEAR(ins.created_at) AS yr, MONTH(ins.created_at) AS mo,
                   MONTHNAME(ins.created_at) AS month_name,
                   COUNT(ins.id) AS inspection_count
            FROM inspection_notes ins
            WHERE ins.status = 1 AND ins.office_id = %s
            GROUP BY YEAR(ins.created_at), MONTH(ins.created_at), MONTHNAME(ins.created_at)
            ORDER BY yr DESC, mo DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No monthly counts found."
        lines = [f"- {r['month_name']} {r['yr']}: {r['inspection_count']} Inspections" for r in rows]
        return "Monthly Inspection Count:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_TITLE_SEARCH":
        kw = p.get("title") or p.get("keyword")
        if not kw: return "Please specify title keyword."
        cur.execute("""
            SELECT ins.id, ins.title, ins.from_date, ins.to_date,
                   ins.short_desc, ins.file_no
            FROM inspection_notes ins
            WHERE ins.title LIKE CONCAT('%%', %s, '%%') AND ins.status = 1 AND ins.office_id = %s
            ORDER BY ins.from_date DESC
            LIMIT 50
        """, (kw, office_id))
        rows = cur.fetchall()
        if not rows: return f"No inspections matching '{kw}' found."
        lines = [f"- {r['title']} ({r['from_date']}): {r['short_desc']}" for r in rows]
        return f"Search Results for '{kw}':\n" + "\n".join(lines)

    elif query_id == "INSPECTION_DESC_SEARCH":
        kw = p.get("keyword")
        if not kw: return "Please specify keyword."
        cur.execute("""
            SELECT ind.id, ind.description, ind.in_type,
                   ins.title, ins.from_date
            FROM inspection_description ind
            JOIN inspection_notes ins ON ins.id = ind.insp_id
            WHERE ind.description LIKE CONCAT('%%', %s, '%%') AND ind.status = 1 AND ins.office_id = %s
            ORDER BY ins.from_date DESC
            LIMIT 50
        """, (kw, office_id))
        rows = cur.fetchall()
        if not rows: return f"No descriptions matching '{kw}' found."
        lines = [f"- {r['title']}: {r['description']}" for r in rows]
        return f"Description Search Results for '{kw}':\n" + "\n".join(lines)

    elif query_id == "INSPECTION_COPY_TO_SUMMARY":
        cur.execute("""
            SELECT ins.id, ins.title, ins.copy_to, ins.from_date
            FROM inspection_notes ins
            WHERE ins.copy_to IS NOT NULL AND ins.status = 1 AND ins.office_id = %s
            ORDER BY ins.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No copy_to data found."
        lines = [f"- {r['title']}: Copied to {r['copy_to']}" for r in rows]
        return "Inspection Copies:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_DEPT_SUMMARY":
        cur.execute("""
            SELECT ind.in_type AS department_type,
                   COUNT(ind.id) AS total,
                   SUM(CASE WHEN ind.i_status = 2 THEN 1 ELSE 0 END) AS completed,
                   SUM(CASE WHEN ind.i_status = 0 THEN 1 ELSE 0 END) AS pending
            FROM inspection_description ind
            JOIN inspection_notes ins ON ins.id = ind.insp_id
            WHERE ind.status = 1 AND ins.office_id = %s
            GROUP BY ind.in_type
            ORDER BY total DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No department summary found."
        lines = [f"- Dept {r['department_type']}: {r['total']} Total ({r['completed']} Completed, {r['pending']} Pending)" for r in rows]
        return "Inspection Department Summary:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_LATEST":
        cur.execute("""
            SELECT ins.id, ins.title, ins.from_date, ins.to_date,
                   ins.short_desc, ins.created_at
            FROM inspection_notes ins
            WHERE ins.status = 1 AND ins.office_id = %s
            ORDER BY ins.created_at DESC
            LIMIT 10
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No recent inspections found."
        lines = [f"- {r['title']} ({r['from_date']}): {r['short_desc']}" for r in rows]
        return "Latest 10 Inspections:\n" + "\n".join(lines)

    elif query_id == "INSPECTION_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(id) FROM inspection_notes WHERE status=1 AND office_id=%s) AS total_inspections,
              (SELECT COUNT(ind.id) FROM inspection_description ind JOIN inspection_notes ins ON ins.id=ind.insp_id WHERE ind.status=1 AND ins.office_id=%s) AS total_descriptions,
              (SELECT COUNT(ind.id) FROM inspection_description ind JOIN inspection_notes ins ON ins.id=ind.insp_id WHERE ind.i_status=0 AND ind.status=1 AND ins.office_id=%s) AS pending_actions,
              (SELECT COUNT(ind.id) FROM inspection_description ind JOIN inspection_notes ins ON ins.id=ind.insp_id WHERE ind.i_status=2 AND ind.status=1 AND ins.office_id=%s) AS completed_actions
        """, (office_id, office_id, office_id, office_id))
        r = cur.fetchone()
        if not r: return "Could not generate inspection module summary."
        return (f"Inspection Module Summary:\n"
                f"Total Inspections: {r['total_inspections']}\n"
                f"Total Descriptions/Items: {r['total_descriptions']}\n"
                f"Pending Actions: {r['pending_actions']}\n"
                f"Completed Actions: {r['completed_actions']}")

    return None
