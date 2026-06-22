"""Course module query handlers."""

import datetime

TEMPLATES = [
    {
        "id": "COURSE_TOTAL_COUNT",
        "module": "course",
        "description": "Total number of active courses",
        "example_questions": [
            "How many courses are there?",
            "How many active courses?",
            "How many courses we have?",
            "How many active courses we have?",
            "Total courses",
            "Show total active courses"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_for", "course_group", "status"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "COURSE_LIST_ACTIVE",
        "module": "course",
        "description": "List active courses",
        "example_questions": [
            "Show all active courses",
            "List courses",
            "Which courses are active?"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_for", "course_group", "limit"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COURSE_DETAILS_BY_NAME",
        "module": "course",
        "description": "Get course details by course name or course code",
        "example_questions": [
            "Show details of induction course",
            "What is HR-LDCE course?",
            "Course details for OS/WI Promotion"
        ],
        "required_params": [],
        "optional_params": ["course_name", "cs_code", "office_id"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "detail",
        "security_level": "low"
    },
    {
        "id": "COURSE_BY_COURSE_FOR",
        "module": "course",
        "description": "List/count courses by course_for/category/department",
        "example_questions": [
            "Show establishment courses",
            "How many transportation courses?",
            "Course list by department"
        ],
        "required_params": [],
        "optional_params": ["course_for", "course_for_id", "office_id"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COURSE_BY_GROUP",
        "module": "course",
        "description": "List/count courses by course group like Promotion, Refresher, Initial",
        "example_questions": [
            "Show promotion courses",
            "How many refresher courses?",
            "List initial courses"
        ],
        "required_params": [],
        "optional_params": ["course_group", "course_group_id", "office_id"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COURSE_FOR_SUMMARY",
        "module": "course",
        "description": "Course count grouped by course_for/category/department",
        "example_questions": [
            "Department wise course count",
            "Course for wise summary",
            "How many courses in each department?"
        ],
        "required_params": [],
        "optional_params": ["office_id", "status"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "COURSE_GROUP_SUMMARY",
        "module": "course",
        "description": "Course count grouped by course group",
        "example_questions": [
            "Group wise course count",
            "Promotion refresher initial course count",
            "Course group summary"
        ],
        "required_params": [],
        "optional_params": ["office_id", "status"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "COURSE_DURATION_SUMMARY",
        "module": "course",
        "description": "Course duration and week days summary",
        "example_questions": [
            "Which course has longest duration?",
            "Show course duration",
            "Course duration wise list"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_name", "course_for", "course_group"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "COURSE_ONLINE_EXAM_ENABLED",
        "module": "course",
        "description": "Courses where online exam is enabled",
        "example_questions": [
            "Which courses have online exam?",
            "Show online exam courses",
            "How many courses have online exam enabled?"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_for", "course_group"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COURSE_CERTIFICATE_ENABLED",
        "module": "course",
        "description": "Courses where certificate is enabled",
        "example_questions": [
            "Which courses provide certificate?",
            "Show certificate courses",
            "How many certificate courses?"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_for", "course_group"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COURSE_WITH_HOSTEL",
        "module": "course",
        "description": "Courses with hostel facility enabled through cs_designs",
        "example_questions": [
            "Which courses have hostel?",
            "Show courses with hostel facility",
            "Course hostel facility list"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_name"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COURSE_WITH_MESS",
        "module": "course",
        "description": "Courses with mess facility enabled through cs_designs",
        "example_questions": [
            "Which courses have mess?",
            "Show courses with mess facility",
            "Course mess facility list"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_name"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COURSE_WITH_LIBRARY",
        "module": "course",
        "description": "Courses with library facility enabled through cs_designs",
        "example_questions": [
            "Which courses have library?",
            "Show courses with library facility",
            "Course library facility list"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_name"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COURSE_FACILITY_SUMMARY",
        "module": "course",
        "description": "Facility summary for courses: hostel, mess, library, sports, store",
        "example_questions": [
            "Show course facility summary",
            "How many courses have hostel mess library?",
            "Facility wise course count"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_for", "course_group"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "COURSE_BATCH_COUNT",
        "module": "course",
        "description": "Count training batches/calendars for courses",
        "example_questions": [
            "How many batches for each course?",
            "Course wise batch count",
            "Show batches of HR-LDCE"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_name", "year", "month"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "COURSE_UPCOMING_BATCHES",
        "module": "course",
        "description": "Upcoming course batches from training_calendars",
        "example_questions": [
            "Upcoming courses",
            "Which course batches are upcoming?",
            "Show upcoming training courses"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_name", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COURSE_ONGOING_BATCHES",
        "module": "course",
        "description": "Ongoing course batches from training_calendars",
        "example_questions": [
            "Ongoing courses",
            "Which courses are running now?",
            "Current training batches"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_name"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COURSE_COMPLETED_BATCHES",
        "module": "course",
        "description": "Completed course batches from training_calendars",
        "example_questions": [
            "Completed courses",
            "Which courses completed this year?",
            "Completed training batches"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_name", "year", "month"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "COURSE_SEAT_SUMMARY",
        "module": "course",
        "description": "Course/batch seat capacity summary using training_calendars.seat",
        "example_questions": [
            "Show seat capacity course wise",
            "Which course has highest seats?",
            "Batch seat summary"
        ],
        "required_params": [],
        "optional_params": ["office_id", "course_name", "year"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "COURSE_MODULE_SUMMARY",
        "module": "course",
        "description": "Overall course module summary including total courses, active courses, groups, categories, batches",
        "example_questions": [
            "Course module summary",
            "Give overview of courses",
            "Course dashboard summary"
        ],
        "required_params": [],
        "optional_params": ["office_id", "year"],
        "allowed_roles": ["principal", "admin", "course_admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute course query by ID."""
    p = params or {}
    
    if query_id == "COURSE_TOTAL_COUNT":
        cur.execute("SELECT COUNT(*) AS total_courses FROM courses WHERE office_id = %s AND status = 1", (office_id,))
        r = cur.fetchone()
        return f"Total active courses: {r['total_courses'] if r else 0}"

    elif query_id == "COURSE_LIST_ACTIVE":
        limit = int(p.get("limit") or 2000)
        cur.execute("""
            SELECT course_name, cs_code, cs_duration, week_days 
            FROM courses 
            WHERE office_id = %s AND status = 1 
            ORDER BY course_name 
            LIMIT %s
        """, (office_id, limit))
        rows = cur.fetchall()
        if not rows:
            return "No active courses found."
        lines = ["Active Courses:"]
        for r in rows:
            lines.append(f"- {r['course_name']} ({r['cs_code']}) - Duration: {r['cs_duration']} {r['week_days']}")
        return "\n".join(lines)

    elif query_id == "COURSE_DETAILS_BY_NAME":
        course_name = p.get("course_name", "")
        cs_code = p.get("cs_code", "")
        if course_name:
            # Strip trailing 'course'/'courses' to improve LIKE matching
            search_term = course_name.lower().replace(" courses", "").replace(" course", "").strip()
            cur.execute("""
                SELECT c.*, cf.course_for, cg.course_group 
                FROM courses c
                LEFT JOIN course_for cf ON cf.id = c.cf_id
                LEFT JOIN course_groups cg ON cg.id = c.cg_id
                WHERE c.office_id = %s AND c.status = 1 
                AND (LOWER(c.course_name) LIKE LOWER(%s) OR LOWER(c.cs_code) LIKE LOWER(%s))
                LIMIT 5
            """, (office_id, f"%{search_term}%", f"%{search_term}%"))
        elif cs_code:
            cur.execute("""
                SELECT c.*, cf.course_for, cg.course_group 
                FROM courses c
                LEFT JOIN course_for cf ON cf.id = c.cf_id
                LEFT JOIN course_groups cg ON cg.id = c.cg_id
                WHERE c.office_id = %s AND c.status = 1 AND c.cs_code = %s
                LIMIT 5
            """, (office_id, cs_code))
        else:
            return None
        rows = cur.fetchall()
        if not rows:
            return "Course not found."

        if len(rows) > 1:
            lines = [f"Multiple courses found. Please select a course:"]
            for r in rows:
                lines.append(f"- {r['course_name']} (Code: {r['cs_code']})")
            return "COURSE_SELECT\n" + "\n".join(lines)

        lines = ["Course Details:"]
        for r in rows:
            lines.append(f"<b>Name:</b> {r['course_name']}")
            lines.append(f"<b>Code:</b> {r['cs_code']}")
            lines.append(f"<b>Duration:</b> {r['cs_duration']} {r['week_days']}")
            lines.append(f"<b>Category:</b> {r.get('course_for', 'N/A')}")
            lines.append(f"<b>Group:</b> {r.get('course_group', 'N/A')}")
            lines.append(f"<b>Online Exam:</b> {'Yes' if r['online_exam'] else 'No'}")
            lines.append(f"<b>Certificate:</b> {'Yes' if r['certificate'] else 'No'}")
        return "<br>".join(lines)

    elif query_id == "COURSE_BY_COURSE_FOR":
        course_for = p.get("course_for", "")
        if not course_for:
            return None
        cur.execute("""
            SELECT c.course_name, c.cs_code, cf.course_for
            FROM courses c
            JOIN course_for cf ON cf.id = c.cf_id
            WHERE c.office_id = %s AND c.status = 1
            AND LOWER(cf.course_for) LIKE LOWER(%s)
            ORDER BY c.course_name
            LIMIT 20
        """, (office_id, f"%{course_for}%"))
        rows = cur.fetchall()
        if not rows:
            return f"No courses found for department: {course_for}"
        lines = [f"Courses in {course_for}:"]
        for r in rows:
            lines.append(f"- {r['course_name']} ({r['cs_code']})")
        return "\n".join(lines)

    elif query_id == "COURSE_BY_GROUP":
        course_group = p.get("course_group", "")
        if not course_group:
            return None
        cur.execute("""
            SELECT c.course_name, c.cs_code, cg.course_group
            FROM courses c
            JOIN course_groups cg ON cg.id = c.cg_id
            WHERE c.office_id = %s AND c.status = 1
            AND LOWER(cg.course_group) LIKE LOWER(%s)
            ORDER BY c.course_name
            LIMIT 20
        """, (office_id, f"%{course_group}%"))
        rows = cur.fetchall()
        if not rows:
            return f"No courses found for group: {course_group}"
        lines = [f"Courses in {course_group} group:"]
        for r in rows:
            lines.append(f"- {r['course_name']} ({r['cs_code']})")
        return "\n".join(lines)

    elif query_id == "COURSE_FOR_SUMMARY":
        cur.execute("""
            SELECT cf.course_for, COUNT(c.id) AS course_count
            FROM course_for cf
            LEFT JOIN courses c ON c.cf_id = cf.id AND c.office_id = %s AND c.status = 1
            WHERE cf.office_id = %s AND cf.status = 1
            GROUP BY cf.course_for
            ORDER BY course_count DESC
        """, (office_id, office_id))
        rows = cur.fetchall()
        if not rows:
            return "No course categories found."
        lines = ["Department-wise Course Count:"]
        for r in rows:
            lines.append(f"- {r['course_for']}: {r['course_count']}")
        return "\n".join(lines)

    elif query_id == "COURSE_GROUP_SUMMARY":
        cur.execute("""
            SELECT cg.course_group, COUNT(c.id) AS course_count
            FROM course_groups cg
            LEFT JOIN courses c ON c.cg_id = cg.id AND c.office_id = %s AND c.status = 1
            WHERE cg.office_id = %s AND cg.status = 1
            GROUP BY cg.course_group
            ORDER BY course_count DESC
        """, (office_id, office_id))
        rows = cur.fetchall()
        if not rows:
            return "No course groups found."
        lines = ["Course Group-wise Count:"]
        for r in rows:
            lines.append(f"- {r['course_group']}: {r['course_count']}")
        return "\n".join(lines)

    elif query_id == "COURSE_ONLINE_EXAM_ENABLED":
        cur.execute("""
            SELECT course_name, cs_code, course_name_hindi
            FROM courses 
            WHERE office_id = %s AND status = 1 AND online_exam = 1
            ORDER BY course_name
            LIMIT 20
        """, (office_id,))
        rows = cur.fetchall()
        if not rows:
            return "No courses with online exam enabled."
        lines = ["Courses with Online Exam:"]
        for r in rows:
            lines.append(f"- {r['course_name']} ({r['cs_code']})")
        return "\n".join(lines)

    elif query_id == "COURSE_CERTIFICATE_ENABLED":
        cur.execute("""
            SELECT course_name, cs_code
            FROM courses 
            WHERE office_id = %s AND status = 1 AND certificate = 1
            ORDER BY course_name
            LIMIT 20
        """, (office_id,))
        rows = cur.fetchall()
        if not rows:
            return "No courses with certificate enabled."
        lines = ["Courses with Certificate:"]
        for r in rows:
            lines.append(f"- {r['course_name']} ({r['cs_code']})")
        return "\n".join(lines)

    elif query_id == "COURSE_WITH_HOSTEL":
        cur.execute("""
            SELECT DISTINCT c.course_name, c.cs_code
            FROM all_dues ad
            JOIN training_calendars tc ON tc.id = ad.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE c.office_id = %s AND c.status = 1 AND ad.status = 1 AND ad.hostel = 1
            ORDER BY c.course_name
            LIMIT 20
        """, (office_id,))
        rows = cur.fetchall()
        if not rows:
            return "No courses with hostel facility."
        lines = ["Courses with Hostel Facility:"]
        for r in rows:
            lines.append(f"- {r['course_name']} ({r['cs_code']})")
        return "\n".join(lines)

    elif query_id == "COURSE_WITH_MESS":
        cur.execute("""
            SELECT DISTINCT c.course_name, c.cs_code
            FROM all_dues ad
            JOIN training_calendars tc ON tc.id = ad.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE c.office_id = %s AND c.status = 1 AND ad.status = 1 AND ad.mess = 1
            ORDER BY c.course_name
            LIMIT 20
        """, (office_id,))
        rows = cur.fetchall()
        if not rows:
            return "No courses with mess facility."
        lines = ["Courses with Mess Facility:"]
        for r in rows:
            lines.append(f"- {r['course_name']} ({r['cs_code']})")
        return "\n".join(lines)

    elif query_id == "COURSE_WITH_LIBRARY":
        cur.execute("""
            SELECT DISTINCT c.course_name, c.cs_code
            FROM all_dues ad
            JOIN training_calendars tc ON tc.id = ad.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE c.office_id = %s AND c.status = 1 AND ad.status = 1 AND ad.library = 1
            ORDER BY c.course_name
            LIMIT 20
        """, (office_id,))
        rows = cur.fetchall()
        if not rows:
            return "No courses with library facility."
        lines = ["Courses with Library Facility:"]
        for r in rows:
            lines.append(f"- {r['course_name']} ({r['cs_code']})")
        return "\n".join(lines)

    elif query_id == "COURSE_FACILITY_SUMMARY":
        cur.execute("""
            SELECT 
                COUNT(DISTINCT CASE WHEN ad.hostel = 1 THEN c.id END) AS hostel_courses,
                COUNT(DISTINCT CASE WHEN ad.mess = 1 THEN c.id END) AS mess_courses,
                COUNT(DISTINCT CASE WHEN ad.library = 1 THEN c.id END) AS library_courses,
                COUNT(DISTINCT CASE WHEN ad.sports = 1 THEN c.id END) AS sports_courses,
                COUNT(DISTINCT CASE WHEN ad.store = 1 THEN c.id END) AS store_courses
            FROM all_dues ad
            JOIN training_calendars tc ON tc.id = ad.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE c.office_id = %s AND c.status = 1 AND ad.status = 1
        """, (office_id,))
        r = cur.fetchone()
        if not r:
            return "No facility data found."
        return f"""Course Facility Summary:
- Hostel: {r['hostel_courses']} courses
- Mess: {r['mess_courses']} courses
- Library: {r['library_courses']} courses
- Sports: {r['sports_courses']} courses
- Store: {r['store_courses']} courses"""

    elif query_id == "COURSE_UPCOMING_BATCHES":
        cur.execute("""
            SELECT tc.course_batch, c.course_name, tc.from_date, tc.to_date, tc.seat
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id
            WHERE tc.office_id = %s AND tc.status = 1 AND tc.from_date > CURDATE()
            ORDER BY tc.from_date
            LIMIT 20
        """, (office_id,))
        rows = cur.fetchall()
        if not rows:
            return "No upcoming course batches."
        lines = ["Upcoming Course Batches:"]
        for r in rows:
            lines.append(f"- {r['course_name']} | Batch: {r['course_batch']} | From: {r['from_date']} | Seats: {r['seat']}")
        return "\n".join(lines)

    elif query_id == "COURSE_ONGOING_BATCHES":
        cur.execute("""
            SELECT tc.course_batch, c.course_name, tc.from_date, tc.to_date, tc.seat
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id
            WHERE tc.office_id = %s AND tc.status = 1 
            AND tc.from_date <= CURDATE() AND tc.to_date >= CURDATE()
            ORDER BY tc.from_date
            LIMIT 20
        """, (office_id,))
        rows = cur.fetchall()
        if not rows:
            return "No ongoing course batches."
        lines = ["Ongoing Course Batches:"]
        for r in rows:
            lines.append(f"- {r['course_name']} | Batch: {r['course_batch']} | From: {r['from_date']} To: {r['to_date']} | Seats: {r['seat']}")
        return "\n".join(lines)

    elif query_id == "COURSE_COMPLETED_BATCHES":
        year = int(p.get("year", datetime.datetime.now().year))
        cur.execute("""
            SELECT tc.course_batch, c.course_name, tc.from_date, tc.to_date
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id
            WHERE tc.office_id = %s AND tc.status = 1 
            AND tc.to_date < CURDATE()
            AND YEAR(tc.to_date) = %s
            ORDER BY tc.to_date DESC
            LIMIT 20
        """, (office_id, year))
        rows = cur.fetchall()
        if not rows:
            return f"No completed course batches in {year}."
        lines = [f"Completed Course Batches in {year}:"]
        for r in rows:
            lines.append(f"- {r['course_name']} | Batch: {r['course_batch']} | Completed: {r['to_date']}")
        return "\n".join(lines)

    elif query_id == "COURSE_BATCH_COUNT":
        cur.execute("""
            SELECT c.course_name, COUNT(tc.id) AS batch_count
            FROM courses c
            LEFT JOIN training_calendars tc ON tc.ct_id = c.id AND tc.office_id = %s AND tc.status = 1
            WHERE c.office_id = %s AND c.status = 1
            GROUP BY c.id, c.course_name
            ORDER BY batch_count DESC
            LIMIT 20
        """, (office_id, office_id))
        rows = cur.fetchall()
        if not rows:
            return "No batch data found."
        lines = ["Course-wise Batch Count:"]
        for r in rows:
            lines.append(f"- {r['course_name']}: {r['batch_count']} batches")
        return "\n".join(lines)

    elif query_id == "COURSE_SEAT_SUMMARY":
        cur.execute("""
            SELECT c.course_name, SUM(tc.seat) AS total_seats, AVG(tc.seat) AS avg_seats
            FROM courses c
            JOIN training_calendars tc ON tc.ct_id = c.id
            WHERE tc.office_id = %s AND tc.status = 1 AND tc.from_date > DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
            GROUP BY c.id, c.course_name
            ORDER BY total_seats DESC
            LIMIT 20
        """, (office_id,))
        rows = cur.fetchall()
        if not rows:
            return "No seat data found."
        lines = ["Course Seat Capacity (Last 1 Year):"]
        for r in rows:
            lines.append(f"- {r['course_name']}: Total {int(r['total_seats'])} seats (Avg: {int(r['avg_seats'])} per batch)")
        return "\n".join(lines)

    elif query_id == "COURSE_DURATION_SUMMARY":
        cur.execute("""
            SELECT course_name, cs_duration, week_days
            FROM courses
            WHERE office_id = %s AND status = 1
            ORDER BY CAST(cs_duration AS UNSIGNED) DESC
            LIMIT 20
        """, (office_id,))
        rows = cur.fetchall()
        if not rows:
            return "No course duration data found."
        lines = ["Course Duration Summary:"]
        for r in rows:
            lines.append(f"- {r['course_name']}: {r['cs_duration']} {r['week_days']}")
        return "\n".join(lines)

    elif query_id == "COURSE_MODULE_SUMMARY":
        # Total courses
        cur.execute("SELECT COUNT(*) AS total FROM courses WHERE office_id = %s AND status = 1", (office_id,))
        total_courses = cur.fetchone()['total']
        
        # Active batches
        cur.execute("SELECT COUNT(*) AS total FROM training_calendars WHERE office_id = %s AND status = 1", (office_id,))
        total_batches = cur.fetchone()['total']
        
        # Categories
        cur.execute("SELECT COUNT(*) AS total FROM course_for WHERE office_id = %s AND status = 1", (office_id,))
        total_categories = cur.fetchone()['total']
        
        # Groups
        cur.execute("SELECT COUNT(*) AS total FROM course_groups WHERE office_id = %s AND status = 1", (office_id,))
        total_groups = cur.fetchone()['total']
        
        # Upcoming batches
        cur.execute("SELECT COUNT(*) AS total FROM training_calendars WHERE office_id = %s AND status = 1 AND from_date > CURDATE()", (office_id,))
        upcoming = cur.fetchone()['total']
        
        # Ongoing batches
        cur.execute("SELECT COUNT(*) AS total FROM training_calendars WHERE office_id = %s AND status = 1 AND from_date <= CURDATE() AND to_date >= CURDATE()", (office_id,))
        ongoing = cur.fetchone()['total']
        
        return f"""<b>Course Module Summary:</b>
<br><b>Total Active Courses:</b> {total_courses}
<br><b>Total Active Batches:</b> {total_batches}
<br><b>Course Categories:</b> {total_categories}
<br><b>Course Groups:</b> {total_groups}
<br><b>Upcoming Batches:</b> {upcoming}
<br><b>Ongoing Batches:</b> {ongoing}"""

    elif query_id == "COURSE_RECENT_TRAINEE_COUNT":
        # Get the most recent course batch and count trainees
        cur.execute("""
            SELECT 
                tc.id,
                tc.course_batch,
                c.course_name,
                tc.from_date,
                tc.to_date,
                COUNT(tm.user_id) AS trainee_count
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id
            LEFT JOIN tra_masters tm ON tm.course_id = tc.id AND tm.status = 1
            WHERE tc.office_id = %s 
              AND tc.status = 1
            GROUP BY tc.id, tc.course_batch, c.course_name, tc.from_date, tc.to_date
            ORDER BY tc.from_date DESC
            LIMIT 1
        """, (office_id,))
        row = cur.fetchone()
        if not row:
            return "No recent course batch found."
        return f"""The latest course batch is <b>{row['course_batch']}</b> / <b>{row['course_name']}</b>.
<br>It started on {row['from_date']} and has <b>{row['trainee_count']}</b> trainees enrolled."""

    return None
