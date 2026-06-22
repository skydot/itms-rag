"""Complaint module query templates."""

TEMPLATES = [
    {
        "id": "COMPLAINT_TOTAL",
        "module": "complaint",
        "description": "Total complaints",
        "example_questions": ["Total complaints?", "How many complaints?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_PENDING",
        "module": "complaint",
        "description": "Pending complaints",
        "example_questions": ["Pending complaints?", "Unsolved complaints?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "COMPLAINT_COMPLETED",
        "module": "complaint",
        "description": "Completed/closed complaints",
        "example_questions": ["Completed complaints?", "Resolved complaints?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_BY_STATUS",
        "module": "complaint",
        "description": "Complaint by status",
        "example_questions": ["Complaints by status?", "Status-wise complaints?"],
        "required_params": [],
        "optional_params": ["status", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_BY_CATEGORY",
        "module": "complaint",
        "description": "Complaint by category",
        "example_questions": ["Complaints by category?", "Category-wise complaints?"],
        "required_params": [],
        "optional_params": ["category_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_BY_SUBCATEGORY",
        "module": "complaint",
        "description": "Complaint by subcategory",
        "example_questions": ["Complaints by subcategory?", "Subcategory-wise complaints?"],
        "required_params": [],
        "optional_params": ["subcategory_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_BY_USER",
        "module": "complaint",
        "description": "Complaint by user",
        "example_questions": ["Complaints by user?", "User's complaints?"],
        "required_params": [],
        "optional_params": ["user_id", "user_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "COMPLAINT_BY_BUILDING",
        "module": "complaint",
        "description": "Complaint by building/hostel",
        "example_questions": ["Hostel complaints?", "Building-wise complaints?"],
        "required_params": [],
        "optional_params": ["building_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_BY_DATE",
        "module": "complaint",
        "description": "Complaint by date",
        "example_questions": ["Complaints on date?", "Today's complaints?"],
        "required_params": [],
        "optional_params": ["date", "from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_MONTHLY",
        "module": "complaint",
        "description": "Monthly complaints",
        "example_questions": ["Monthly complaints?", "This month complaints?"],
        "required_params": [],
        "optional_params": ["month", "year", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_RATING",
        "module": "complaint",
        "description": "Complaint rating/review",
        "example_questions": ["Complaint ratings?", "Complaint reviews?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_FORWARDED",
        "module": "complaint",
        "description": "Forwarded complaints",
        "example_questions": ["Forwarded complaints?", "Escalated complaints?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_ATTACHMENTS",
        "module": "complaint",
        "description": "Complaint attachments",
        "example_questions": ["Complaint attachments?", "Files attached to complaints?"],
        "required_params": [],
        "optional_params": ["complaint_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_URGENT",
        "module": "complaint",
        "description": "Urgent complaints",
        "example_questions": ["Urgent complaints?", "High priority complaints?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "COMPLAINT_RESOLVED_COUNT",
        "module": "complaint",
        "description": "Count of resolved or completed complaints",
        "example_questions": ["Resolved complaints count?", "How many complaints resolved?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_UNRESOLVED_COUNT",
        "module": "complaint",
        "description": "Count of unresolved, pending, or not resolved complaints",
        "example_questions": ["Unresolved complaints count?", "How many complaints pending?", "How many complaints not resolved?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_OFFICE_SUMMARY",
        "module": "complaint",
        "description": "Complaint office summary",
        "example_questions": ["Office complaint summary?", "Complaint statistics?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_CATEGORY_SUMMARY",
        "module": "complaint",
        "description": "Complaint category summary",
        "example_questions": ["Category summary?", "Complaints by category count?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "COMPLAINT_DETAILED_LIST",
        "module": "complaint",
        "description": "Detailed complaint list",
        "example_questions": ["Show complaint details?", "Detailed complaints?"],
        "required_params": [],
        "optional_params": ["office_id", "status", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "COMPLAINT_MODULE_SUMMARY",
        "module": "complaint",
        "description": "Complaint module summary",
        "example_questions": ["Complaint summary?", "Complaint module overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute complaint queries."""
    p = params or {}
    
    if query_id == "COMPLAINT_TOTAL":
        cur.execute("SELECT COUNT(*) AS total FROM complaints WHERE office_id = %s", (office_id,))
        r = cur.fetchone()
        return f"Total complaints: {r['total'] if r else 0}"
        
    elif query_id == "COMPLAINT_PENDING":
        cur.execute("""
            SELECT c.id, c.cm_no, c.description, c.created_at,
                   cc.comp_name AS category,
                   u.name AS raised_by,
                   hb.building_name
            FROM complaints c
            JOIN complaint_cat cc ON cc.id = c.ctype_id
            JOIN users u ON u.id = c.user_id
            LEFT JOIN hostel_buildings hb ON hb.id = c.building_id
            WHERE c.cm_status = 1
              AND c.status = 1 AND c.office_id = %s
            ORDER BY c.created_at DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No pending complaints found."
        lines = [f"- #{r['cm_no']} ({r['category']}): {r['description']} by {r['raised_by']} at {r['building_name'] or 'Unknown'}" for r in rows]
        return "Pending Complaints:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_COMPLETED":
        cur.execute("""
            SELECT c.id, c.cm_no, c.description, c.remarks, c.rating, c.review,
                   c.created_at, c.updated_at,
                   cc.comp_name AS category,
                   u.name AS raised_by
            FROM complaints c
            JOIN complaint_cat cc ON cc.id = c.ctype_id
            JOIN users u ON u.id = c.user_id
            WHERE c.cm_status = 3
              AND c.status = 1 AND c.office_id = %s
            ORDER BY c.updated_at DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No completed complaints found."
        lines = [f"- #{r['cm_no']} ({r['category']}): {r['description']} by {r['raised_by']} (Rating: {r['rating']})" for r in rows]
        return "Completed Complaints:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_BY_STATUS":
        status_val = p.get("status") or p.get("cm_status")
        if not status_val: return "Please specify a status."
        cur.execute("""
            SELECT c.id, c.cm_no, c.description, c.remarks, c.cm_status,
                   c.created_at, c.updated_at,
                   cc.comp_name AS category,
                   u.name AS raised_by,
                   CASE c.cm_status
                     WHEN 1 THEN 'Pending'
                     WHEN 2 THEN 'In Progress'
                     WHEN 3 THEN 'Completed'
                     WHEN 4 THEN 'Forwarded'
                     WHEN 5 THEN 'Closed'
                     ELSE 'Unknown'
                   END AS status_label
            FROM complaints c
            JOIN complaint_cat cc ON cc.id = c.ctype_id
            JOIN users u ON u.id = c.user_id
            WHERE c.cm_status = %s
              AND c.status = 1 AND c.office_id = %s
            ORDER BY c.created_at DESC
            LIMIT 50
        """, (status_val, office_id))
        rows = cur.fetchall()
        if not rows: return f"No complaints found with status {status_val}."
        lines = [f"- #{r['cm_no']} ({r['category']}): [{r['status_label']}] {r['description']} by {r['raised_by']}" for r in rows]
        return f"Complaints (Status: {status_val}):\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_BY_CATEGORY":
        cur.execute("""
            SELECT cc.id AS cat_id, cc.comp_name AS category,
                   COUNT(c.id) AS total_complaints,
                   SUM(CASE WHEN c.cm_status = 1 THEN 1 ELSE 0 END) AS pending,
                   SUM(CASE WHEN c.cm_status = 3 THEN 1 ELSE 0 END) AS completed,
                   SUM(CASE WHEN c.cm_status = 5 THEN 1 ELSE 0 END) AS closed,
                   ROUND(AVG(c.rating), 2) AS avg_rating
            FROM complaint_cat cc
            LEFT JOIN complaints c ON c.ctype_id = cc.id AND c.status = 1 AND c.office_id = %s
            WHERE cc.cat_id = 0
              AND cc.status = 1 AND cc.office_id = %s
            GROUP BY cc.id, cc.comp_name
            ORDER BY total_complaints DESC
            LIMIT 50
        """, (office_id, office_id))
        rows = cur.fetchall()
        if not rows: return "No category-wise complaints found."
        lines = [f"- {r['category']}: {r['total_complaints']} Total ({r['pending']} Pending, {r['completed']} Completed, {r['closed']} Closed, Avg Rating: {r['avg_rating'] if r['avg_rating'] is not None else 0})" for r in rows]
        return "Complaints by Category:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_BY_SUBCATEGORY":
        cur.execute("""
            SELECT cc.comp_name AS category,
                   cs.subcat_name AS sub_category,
                   COUNT(c.id) AS total_complaints,
                   SUM(CASE WHEN c.cm_status = 1 THEN 1 ELSE 0 END) AS pending,
                   SUM(CASE WHEN c.cm_status = 3 THEN 1 ELSE 0 END) AS completed
            FROM complaint_subcat cs
            JOIN complaint_cat cc ON cc.id = cs.cat_id
            LEFT JOIN complaints c ON c.ctype_sub_id = cs.id AND c.status = 1 AND c.office_id = %s
            WHERE cs.status = 1 AND cs.office_id = %s
            GROUP BY cs.id, cc.comp_name, cs.subcat_name
            ORDER BY total_complaints DESC
            LIMIT 50
        """, (office_id, office_id))
        rows = cur.fetchall()
        if not rows: return "No subcategory-wise complaints found."
        lines = [f"- {r['category']} > {r['sub_category']}: {r['total_complaints']} Total ({r['pending']} Pending)" for r in rows]
        return "Complaints by Subcategory:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_BY_USER":
        uid = p.get("user_id")
        if not uid: return "Please specify a user_id."
        cur.execute("""
            SELECT c.id, c.cm_no, c.description, c.remarks, c.rating, c.review,
                   c.cm_status, c.created_at,
                   cc.comp_name AS category,
                   CASE c.cm_status
                     WHEN 1 THEN 'Pending'
                     WHEN 3 THEN 'Completed'
                     WHEN 5 THEN 'Closed'
                     ELSE 'Other'
                   END AS status_label
            FROM complaints c
            JOIN complaint_cat cc ON cc.id = c.ctype_id
            WHERE c.user_id = %s
              AND c.status = 1 AND c.office_id = %s
            ORDER BY c.created_at DESC
            LIMIT 50
        """, (uid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No complaints found for user {uid}."
        lines = [f"- #{r['cm_no']} ({r['category']}): [{r['status_label']}] {r['description']}" for r in rows]
        return f"Complaints by User {uid}:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_BY_BUILDING":
        bid = p.get("building_id")
        if not bid: return "Please specify a building_id."
        cur.execute("""
            SELECT c.id, c.cm_no, c.description, c.cm_status,
                   hb.building_name,
                   cc.comp_name AS category,
                   u.name AS raised_by,
                   c.created_at
            FROM complaints c
            JOIN hostel_buildings hb ON hb.id = c.building_id
            JOIN complaint_cat cc ON cc.id = c.ctype_id
            JOIN users u ON u.id = c.user_id
            WHERE c.building_id = %s
              AND c.status = 1 AND c.office_id = %s
            ORDER BY c.created_at DESC
            LIMIT 50
        """, (bid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No complaints found for building {bid}."
        lines = [f"- #{r['cm_no']} at {r['building_name']}: {r['description']} by {r['raised_by']}" for r in rows]
        return f"Complaints for Building {bid}:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_BY_DATE":
        fdate = p.get("from_date") or p.get("date")
        tdate = p.get("to_date") or fdate
        if not fdate or not tdate: return "Please specify from_date and to_date."
        cur.execute("""
            SELECT c.id, c.cm_no, c.description, c.cm_status,
                   cc.comp_name AS category,
                   u.name AS raised_by,
                   c.created_at
            FROM complaints c
            JOIN complaint_cat cc ON cc.id = c.ctype_id
            JOIN users u ON u.id = c.user_id
            WHERE DATE(c.created_at) BETWEEN %s AND %s
              AND c.status = 1 AND c.office_id = %s
            ORDER BY c.created_at DESC
            LIMIT 50
        """, (fdate, tdate, office_id))
        rows = cur.fetchall()
        if not rows: return "No complaints found in this date range."
        lines = [f"- #{r['cm_no']} ({r['category']}): {r['description']} by {r['raised_by']}" for r in rows]
        return f"Complaints between {fdate} and {tdate}:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_MONTHLY":
        cur.execute("""
            SELECT YEAR(c.created_at) AS yr,
                   MONTH(c.created_at) AS mo,
                   MONTHNAME(c.created_at) AS month_name,
                   COUNT(c.id) AS total,
                   SUM(CASE WHEN c.cm_status = 1 THEN 1 ELSE 0 END) AS pending,
                   SUM(CASE WHEN c.cm_status = 3 THEN 1 ELSE 0 END) AS completed
            FROM complaints c
            WHERE c.status = 1 AND c.office_id = %s
            GROUP BY YEAR(c.created_at), MONTH(c.created_at), MONTHNAME(c.created_at)
            ORDER BY yr DESC, mo DESC
            LIMIT 24
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No monthly complaints data found."
        lines = [f"- {r['month_name']} {r['yr']}: {r['total']} Total ({r['pending']} Pending, {r['completed']} Completed)" for r in rows]
        return "Monthly Complaints:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_RATING":
        cur.execute("""
            SELECT c.id, c.cm_no, c.rating, c.review,
                   cc.comp_name AS category,
                   u.name AS raised_by,
                   c.updated_at AS resolved_at
            FROM complaints c
            JOIN complaint_cat cc ON cc.id = c.ctype_id
            JOIN users u ON u.id = c.user_id
            WHERE c.rating IS NOT NULL
              AND c.status = 1 AND c.office_id = %s
            ORDER BY c.rating DESC, c.updated_at DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No rated complaints found."
        lines = [f"- #{r['cm_no']} ({r['category']}): {r['rating']} Stars - {r['review']} (by {r['raised_by']})" for r in rows]
        return "Complaint Ratings:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_FORWARDED":
        cur.execute("""
            SELECT c.id, c.cm_no, c.description, c.forwarded_to,
                   fu.name AS forwarded_to_user,
                   cc.comp_name AS category,
                   u.name AS raised_by,
                   c.created_at
            FROM complaints c
            JOIN complaint_cat cc ON cc.id = c.ctype_id
            JOIN users u ON u.id = c.user_id
            LEFT JOIN users fu ON fu.id = c.forwarded_to
            WHERE c.forwarded_to > 0
              AND c.status = 1 AND c.office_id = %s
            ORDER BY c.created_at DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No forwarded complaints found."
        lines = [f"- #{r['cm_no']} ({r['category']}): Forwarded to {r['forwarded_to_user']} (Raised by {r['raised_by']})" for r in rows]
        return "Forwarded Complaints:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_ATTACHMENTS":
        cur.execute("""
            SELECT c.id, c.cm_no, cf.attachment, cf.created_at AS attachment_date,
                   cc.comp_name AS category,
                   u.name AS raised_by
            FROM complaints_files cf
            JOIN complaints c ON c.id = cf.cm_id
            JOIN complaint_cat cc ON cc.id = c.ctype_id
            JOIN users u ON u.id = c.user_id
            WHERE cf.status = 1
              AND c.status = 1 AND c.office_id = %s
            ORDER BY cf.created_at DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No attachments found for complaints."
        lines = [f"- #{r['cm_no']} ({r['category']}): {r['attachment']} (by {r['raised_by']})" for r in rows]
        return "Complaints with Attachments:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_URGENT":
        cur.execute("""
            SELECT c.id, c.cm_no, c.description, c.cm_status,
                   cc.comp_name AS category,
                   u.name AS raised_by,
                   c.created_at,
                   DATEDIFF(NOW(), c.created_at) AS days_pending
            FROM complaints c
            JOIN complaint_cat cc ON cc.id = c.ctype_id
            JOIN users u ON u.id = c.user_id
            WHERE c.cm_status = 1
              AND c.status = 1 AND c.office_id = %s
              AND DATEDIFF(NOW(), c.created_at) >= 3
            ORDER BY days_pending DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No urgent pending complaints found."
        lines = [f"- #{r['cm_no']} ({r['category']}): Pending for {r['days_pending']} days by {r['raised_by']}" for r in rows]
        return "Urgent Complaints:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_RESOLVED_COUNT":
        cur.execute("""
            SELECT COUNT(id) AS resolved_count
            FROM complaints
            WHERE cm_status = 3
              AND status = 1 AND office_id = %s
        """, (office_id,))
        r = cur.fetchone()
        return f"Resolved complaints count: {r['resolved_count'] if r else 0}"

    elif query_id == "COMPLAINT_UNRESOLVED_COUNT":
        cur.execute("""
            SELECT COUNT(id) AS unresolved_count
            FROM complaints
            WHERE cm_status IN (1, 2, 4)
              AND status = 1 AND office_id = %s
        """, (office_id,))
        r = cur.fetchone()
        return f"Unresolved complaints count: {r['unresolved_count'] if r else 0}"

    elif query_id == "COMPLAINT_OFFICE_SUMMARY":
        cur.execute("""
            SELECT c.office_id,
                   COUNT(c.id) AS total,
                   SUM(CASE WHEN c.cm_status = 1 THEN 1 ELSE 0 END) AS pending,
                   SUM(CASE WHEN c.cm_status = 3 THEN 1 ELSE 0 END) AS completed,
                   ROUND(AVG(c.rating), 2) AS avg_rating
            FROM complaints c
            WHERE c.status = 1 AND c.office_id = %s
            GROUP BY c.office_id
        """, (office_id,))
        r = cur.fetchone()
        if not r: return "No office summary data available."
        return f"Office {office_id} Summary: {r['total']} Total, {r['pending']} Pending, {r['completed']} Completed, Avg Rating: {r['avg_rating']}"

    elif query_id == "COMPLAINT_CATEGORY_SUMMARY":
        cur.execute("""
            SELECT cc.comp_name AS category,
                   COUNT(c.id) AS total,
                   SUM(CASE WHEN c.cm_status = 1 THEN 1 ELSE 0 END) AS pending,
                   SUM(CASE WHEN c.cm_status = 3 THEN 1 ELSE 0 END) AS completed,
                   SUM(CASE WHEN c.cm_status = 5 THEN 1 ELSE 0 END) AS closed,
                   ROUND(AVG(c.rating), 2) AS avg_rating
            FROM complaint_cat cc
            LEFT JOIN complaints c ON c.ctype_id = cc.id AND c.status = 1 AND c.office_id = %s
            WHERE cc.status = 1 AND cc.office_id = %s
            GROUP BY cc.id, cc.comp_name
            ORDER BY total DESC
            LIMIT 50
        """, (office_id, office_id))
        rows = cur.fetchall()
        if not rows: return "No category summary data available."
        lines = [f"- {r['category']}: {r['total']} Total ({r['pending']} Pending, {r['completed']} Completed, {r['closed']} Closed, Avg Rating: {r['avg_rating'] if r['avg_rating'] is not None else 0})" for r in rows]
        return "Complaint Category Summary:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_DETAILED_LIST":
        cur.execute("""
            SELECT c.id, c.cm_no, c.description, c.remarks,
                   c.rating, c.review, c.cm_status,
                   CASE c.cm_status
                     WHEN 1 THEN 'Pending'
                     WHEN 2 THEN 'In Progress'
                     WHEN 3 THEN 'Completed'
                     WHEN 4 THEN 'Forwarded'
                     WHEN 5 THEN 'Closed'
                   END AS status_label,
                   cc.comp_name AS category,
                   cs.subcat_name AS sub_category,
                   u.name AS raised_by,
                   u.mobile,
                   hb.building_name,
                   c.created_at, c.updated_at
            FROM complaints c
            JOIN complaint_cat cc ON cc.id = c.ctype_id
            LEFT JOIN complaint_subcat cs ON cs.id = c.ctype_sub_id
            JOIN users u ON u.id = c.user_id
            LEFT JOIN hostel_buildings hb ON hb.id = c.building_id
            WHERE c.status = 1 AND c.office_id = %s
            ORDER BY c.created_at DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No detailed complaints list found."
        lines = [f"- #{r['cm_no']} ({r['status_label']}): {r['category']} - {r['description']} (by {r['raised_by']})" for r in rows]
        return "Detailed Complaints List:\n" + "\n".join(lines)

    elif query_id == "COMPLAINT_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(id) FROM complaints WHERE status=1 AND office_id=%s) AS total_complaints,
              (SELECT COUNT(id) FROM complaints WHERE cm_status=1 AND status=1 AND office_id=%s) AS pending,
              (SELECT COUNT(id) FROM complaints WHERE cm_status=3 AND status=1 AND office_id=%s) AS completed,
              (SELECT COUNT(id) FROM complaints WHERE cm_status=5 AND status=1 AND office_id=%s) AS closed,
              (SELECT ROUND(AVG(rating),2) FROM complaints WHERE rating IS NOT NULL AND status=1 AND office_id=%s) AS avg_rating,
              (SELECT COUNT(id) FROM complaints WHERE DATE(created_at)=CURDATE() AND status=1 AND office_id=%s) AS today_complaints
        """, (office_id, office_id, office_id, office_id, office_id, office_id))
        r = cur.fetchone()
        if not r: return "Could not generate complaint module summary."
        return (f"Complaint Module Summary:\n"
                f"Total Complaints: {r['total_complaints']}\n"
                f"Pending: {r['pending']}\n"
                f"Completed: {r['completed']}\n"
                f"Closed: {r['closed']}\n"
                f"Average Rating: {r['avg_rating']}\n"
                f"Today's Complaints: {r['today_complaints']}")

    return None
