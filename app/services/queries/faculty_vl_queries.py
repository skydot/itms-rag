"""Faculty and Visiting Lecturer module query templates."""

TEMPLATES = [
    {
        "id": "FACULTY_VL_TOTAL",
        "module": "faculty_vl",
        "description": "Total visiting lecturers",
        "example_questions": ["Total visiting lecturers?", "How many VLs?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_BY_DATE",
        "module": "faculty_vl",
        "description": "VL by date",
        "example_questions": ["VL on date?", "Visiting lecturer schedule?"],
        "required_params": [],
        "optional_params": ["date", "from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_BY_SUBJECT",
        "module": "faculty_vl",
        "description": "VL by subject",
        "example_questions": ["VL by subject?", "Subject-wise VL?"],
        "required_params": [],
        "optional_params": ["subject_name", "subject_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_BY_COURSE",
        "module": "faculty_vl",
        "description": "VL by course",
        "example_questions": ["VL by course?", "Course-wise visiting lecturers?"],
        "required_params": [],
        "optional_params": ["course_id", "course_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_LECTURE_COUNT",
        "module": "faculty_vl",
        "description": "VL lecture count",
        "example_questions": ["VL lecture count?", "How many VL lectures?"],
        "required_params": [],
        "optional_params": ["vl_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_PAYMENT",
        "module": "faculty_vl",
        "description": "VL payment/price summary",
        "example_questions": ["VL payments?", "Visiting lecturer fees?"],
        "required_params": [],
        "optional_params": ["vl_id", "from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "medium"
    },
    {
        "id": "FACULTY_LECTURE_SCHEDULE",
        "module": "faculty_vl",
        "description": "Faculty lecture schedule",
        "example_questions": ["Faculty schedule?", "Lecture schedule?"],
        "required_params": [],
        "optional_params": ["faculty_id", "from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FACULTY_BY_DEPARTMENT",
        "module": "faculty_vl",
        "description": "Faculty by department",
        "example_questions": ["Faculty by department?", "Dept-wise faculty?"],
        "required_params": [],
        "optional_params": ["department_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FACULTY_BY_DESIGNATION",
        "module": "faculty_vl",
        "description": "Faculty by designation",
        "example_questions": ["Faculty by designation?", "Designation-wise faculty?"],
        "required_params": [],
        "optional_params": ["designation_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FACULTY_ASSIGNED_COURSE",
        "module": "faculty_vl",
        "description": "Faculty assigned to course",
        "example_questions": ["Faculty assigned to course?", "Course faculty?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_TOP",
        "module": "faculty_vl",
        "description": "Top VL by lectures",
        "example_questions": ["Top visiting lecturers?", "Most active VL?"],
        "required_params": [],
        "optional_params": ["office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "ranking",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_FEEDBACK",
        "module": "faculty_vl",
        "description": "VL feedback summary",
        "example_questions": ["VL feedback?", "Visiting lecturer ratings?"],
        "required_params": [],
        "optional_params": ["vl_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_DATE_RANGE",
        "module": "faculty_vl",
        "description": "VL date range",
        "example_questions": ["VL in date range?", "Visiting lecturers between dates?"],
        "required_params": [],
        "optional_params": ["from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_SUBJECT_SUMMARY",
        "module": "faculty_vl",
        "description": "VL subject-wise summary",
        "example_questions": ["VL subject summary?", "Subject-wise VL count?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_COURSE_SUMMARY",
        "module": "faculty_vl",
        "description": "VL course-wise summary",
        "example_questions": ["VL course summary?", "Course-wise VL count?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FACULTY_AVAILABILITY",
        "module": "faculty_vl",
        "description": "Faculty availability",
        "example_questions": ["Faculty availability?", "When is faculty free?"],
        "required_params": [],
        "optional_params": ["faculty_id", "date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_DAILY",
        "module": "faculty_vl",
        "description": "Daily VL schedule",
        "example_questions": ["Daily VL schedule?", "Today's VL?"],
        "required_params": [],
        "optional_params": ["date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_UPCOMING",
        "module": "faculty_vl",
        "description": "Upcoming VL lectures",
        "example_questions": ["Upcoming VL?", "Next VL sessions?"],
        "required_params": [],
        "optional_params": ["office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_COMPLETED",
        "module": "faculty_vl",
        "description": "Completed VL lectures",
        "example_questions": ["Completed VL?", "Past VL sessions?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FACULTY_VL_MODULE_SUMMARY",
        "module": "faculty_vl",
        "description": "Faculty/VL module summary",
        "example_questions": ["Faculty summary?", "VL module overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute faculty VL queries."""
    p = params or {}
    
    if query_id == "FACULTY_VL_TOTAL":
        cur.execute("SELECT COUNT(*) AS total FROM vl_management WHERE office_id = %s", (office_id,))
        r = cur.fetchone()
        return f"Total visiting lecturers: {r['total'] if r else 0}"
        
    elif query_id == "FACULTY_VL_BY_DATE":
        vdate = p.get("date") or p.get("vl_date")
        if not vdate: return "Please specify a date."
        cur.execute("""
            SELECT vm.id, vm.vl_date, vm.subject_name,
                   u.name AS vl_name, desi.desi_name AS designation,
                   vm.description_1, vm.description_2, vm.user_type
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            LEFT JOIN designations desi ON desi.id = u.desi_id
            WHERE vm.vl_date = %s
              AND vm.status = 1 AND vm.office_id = %s
            ORDER BY vm.vl_date DESC
            LIMIT 50
        """, (vdate, office_id))
        rows = cur.fetchall()
        if not rows: return f"No visiting lecturers found for {vdate}."
        lines = [f"- {r['vl_name']} ({r['designation']}): {r['subject_name']}" for r in rows]
        return f"Visiting Lecturers on {vdate}:\n" + "\n".join(lines)

    elif query_id == "FACULTY_VL_BY_SUBJECT":
        sname = p.get("subject_name")
        if not sname: return "Please specify a subject_name."
        cur.execute("""
            SELECT vm.id, vm.vl_date, vm.subject_name,
                   u.name AS vl_name, desi.desi_name AS designation,
                   vm.description_1, vm.description_2
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            LEFT JOIN designations desi ON desi.id = u.desi_id
            WHERE vm.subject_name LIKE CONCAT('%%', %s, '%%')
              AND vm.status = 1 AND vm.office_id = %s
            ORDER BY vm.vl_date DESC
            LIMIT 50
        """, (sname, office_id))
        rows = cur.fetchall()
        if not rows: return f"No VLs found for subject '{sname}'."
        lines = [f"- {r['vl_name']} on {r['vl_date']} (Subject: {r['subject_name']})" for r in rows]
        return f"Visiting Lecturers for Subject '{sname}':\n" + "\n".join(lines)

    elif query_id == "FACULTY_VL_BY_COURSE":
        cid = p.get("ct_id") or p.get("course_id")
        if not cid: return "Please specify a course_id."
        cur.execute("""
            SELECT vm.id, vm.vl_date, vm.subject_name,
                   u.name AS vl_name,
                   c.course_name,
                   tc.course_batch, tc.from_date, tc.to_date,
                   vd.lecture_date, vd.price
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            JOIN vl_description vd ON vd.vlm_id = vm.id
            JOIN training_calendars tc ON tc.id = vd.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE tc.ct_id = %s
              AND vm.status = 1 AND vm.office_id = %s
            ORDER BY vd.lecture_date DESC
            LIMIT 50
        """, (cid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No visiting lecturers found for course {cid}."
        lines = [f"- {r['vl_name']} on {r['lecture_date']} (Subject: {r['subject_name']})" for r in rows]
        return f"Visiting Lecturers for Course {cid}:\n" + "\n".join(lines)

    elif query_id == "FACULTY_VL_LECTURE_COUNT":
        cur.execute("""
            SELECT u.id, u.name, u.name_hindi,
                   desi.desi_name AS designation,
                   COUNT(vm.id) AS total_lectures,
                   COUNT(DISTINCT vd.lecture_date) AS lecture_days
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            LEFT JOIN designations desi ON desi.id = u.desi_id
            JOIN vl_description vd ON vd.vlm_id = vm.id
            WHERE vm.status = 1 AND vm.office_id = %s
            GROUP BY u.id, u.name, u.name_hindi, desi.desi_name
            ORDER BY total_lectures DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No lecture counts found."
        lines = [f"- {r['name']} ({r['designation']}): {r['total_lectures']} Lectures over {r['lecture_days']} Days" for r in rows]
        return "Visiting Lecturer Lecture Counts:\n" + "\n".join(lines)

    elif query_id == "FACULTY_VL_PAYMENT":
        cur.execute("""
            SELECT vm.id, vm.vl_date, vm.subject_name,
                   u.name AS vl_name, desi.desi_name AS designation,
                   vd.lecture_date, vd.price,
                   c.course_name, tc.course_batch
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            LEFT JOIN designations desi ON desi.id = u.desi_id
            JOIN vl_description vd ON vd.vlm_id = vm.id
            JOIN training_calendars tc ON tc.id = vd.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE vm.status = 1 AND vm.office_id = %s
            ORDER BY vd.lecture_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No payment details found."
        lines = [f"- {r['vl_name']} on {r['lecture_date']}: Amount {r['price']} (Course: {r['course_name']})" for r in rows]
        return "Visiting Lecturer Payments:\n" + "\n".join(lines)

    elif query_id == "FACULTY_LECTURE_SCHEDULE":
        cur.execute("""
            SELECT tm.tm_date, tm.start_time, tm.end_time,
                   u.name AS faculty_name, desi.desi_name AS designation,
                   t.topic_name, c.course_name, tc.course_batch,
                   s.subject_name
            FROM time_masters tm
            JOIN users u ON u.id = tm.desi_user_id
            LEFT JOIN designations desi ON desi.id = tm.desi_id
            LEFT JOIN topics t ON t.id = tm.topic_id
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            LEFT JOIN subjects s ON s.id = tm.cs_id
            WHERE tm.status = 1 AND tm.office_id = %s
            ORDER BY tm.tm_date DESC, tm.start_time
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No faculty lecture schedule found."
        lines = [f"- {r['faculty_name']} on {r['tm_date']} ({r['start_time']} - {r['end_time']}): {r['subject_name'] or r['topic_name']} ({r['course_name']})" for r in rows]
        return "Faculty Lecture Schedule:\n" + "\n".join(lines)

    elif query_id == "FACULTY_BY_DEPARTMENT":
        cur.execute("""
            SELECT d.department_name,
                   COUNT(u.id) AS faculty_count
            FROM users u
            JOIN designations desi ON desi.id = u.desi_id
            LEFT JOIN departments d ON d.id = u.desi_id
            WHERE desi.lecture = 1
              AND u.status = 1 AND u.office_id = %s
            GROUP BY d.id, d.department_name
            ORDER BY faculty_count DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No department-wise faculty data found."
        lines = [f"- {r['department_name']}: {r['faculty_count']} Faculty" for r in rows]
        return "Faculty by Department:\n" + "\n".join(lines)

    elif query_id == "FACULTY_BY_DESIGNATION":
        cur.execute("""
            SELECT desi.desi_name,
                   COUNT(u.id) AS faculty_count,
                   GROUP_CONCAT(u.name ORDER BY u.name SEPARATOR ', ') AS faculty_names
            FROM users u
            JOIN designations desi ON desi.id = u.desi_id
            WHERE desi.lecture = 1
              AND u.status = 1 AND u.office_id = %s
            GROUP BY desi.id, desi.desi_name
            ORDER BY faculty_count DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No designation-wise faculty data found."
        lines = [f"- {r['desi_name']}: {r['faculty_count']} ({r['faculty_names']})" for r in rows]
        return "Faculty by Designation:\n" + "\n".join(lines)

    elif query_id == "FACULTY_ASSIGNED_COURSE":
        cur.execute("""
            SELECT c.course_name, tc.course_batch,
                   u.name AS faculty_name, desi.desi_name AS designation,
                   COUNT(tm.id) AS session_count
            FROM time_masters tm
            JOIN users u ON u.id = tm.desi_user_id
            LEFT JOIN designations desi ON desi.id = tm.desi_id
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE tm.status = 1 AND tm.office_id = %s
            GROUP BY c.id, tc.id, u.id, c.course_name, tc.course_batch, u.name, desi.desi_name
            ORDER BY c.course_name, u.name
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No course assignment data found for faculty."
        lines = [f"- {r['faculty_name']} in {r['course_name']} ({r['course_batch']}): {r['session_count']} Sessions" for r in rows]
        return "Faculty Course Assignments:\n" + "\n".join(lines)

    elif query_id == "FACULTY_VL_TOP":
        cur.execute("""
            SELECT u.name, u.name_hindi,
                   desi.desi_name AS designation,
                   COUNT(vm.id) AS total_lectures,
                   SUM(vd.price) AS total_payment
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            LEFT JOIN designations desi ON desi.id = u.desi_id
            JOIN vl_description vd ON vd.vlm_id = vm.id
            WHERE vm.status = 1 AND vm.office_id = %s
            GROUP BY u.id, u.name, u.name_hindi, desi.desi_name
            ORDER BY total_lectures DESC
            LIMIT 10
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No top visiting lecturers found."
        lines = [f"- {r['name']} ({r['designation']}): {r['total_lectures']} Lectures, Total Payment: {r['total_payment']}" for r in rows]
        return "Top 10 Visiting Lecturers:\n" + "\n".join(lines)

    elif query_id == "FACULTY_VL_FEEDBACK":
        cur.execute("""
            SELECT vm.id, vm.vl_date, vm.subject_name,
                   u.name AS vl_name,
                   COUNT(fm.id) AS feedback_count,
                   ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))), 2) AS avg_rating
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            JOIN vl_description vd ON vd.vlm_id = vm.id
            JOIN feed_master fm ON fm.course_id = vd.course_id AND fm.fs_type = 2
            WHERE vm.status = 1 AND vm.office_id = %s
            GROUP BY vm.id, vm.vl_date, vm.subject_name, u.name
            ORDER BY avg_rating DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No feedback found for visiting lecturers."
        lines = [f"- {r['vl_name']} (Subject: {r['subject_name']}): Rating {r['avg_rating']} ({r['feedback_count']} Responses)" for r in rows]
        return "Visiting Lecturer Feedback:\n" + "\n".join(lines)

    elif query_id == "FACULTY_VL_DATE_RANGE":
        fdate = p.get("from_date")
        tdate = p.get("to_date")
        if not fdate or not tdate: return "Please specify from_date and to_date."
        cur.execute("""
            SELECT vm.id, vm.vl_date, vm.subject_name,
                   u.name AS vl_name, desi.desi_name AS designation,
                   vd.lecture_date, vd.price,
                   c.course_name, tc.course_batch
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            LEFT JOIN designations desi ON desi.id = u.desi_id
            JOIN vl_description vd ON vd.vlm_id = vm.id
            JOIN training_calendars tc ON tc.id = vd.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE vd.lecture_date BETWEEN %s AND %s
              AND vm.status = 1 AND vm.office_id = %s
            ORDER BY vd.lecture_date
            LIMIT 50
        """, (fdate, tdate, office_id))
        rows = cur.fetchall()
        if not rows: return "No visiting lectures found in date range."
        lines = [f"- {r['vl_name']} on {r['lecture_date']} ({r['subject_name']}) - {r['course_name']}" for r in rows]
        return f"Visiting Lectures ({fdate} to {tdate}):\n" + "\n".join(lines)

    elif query_id == "FACULTY_VL_SUBJECT_SUMMARY":
        cur.execute("""
            SELECT vm.subject_name,
                   COUNT(vm.id) AS total_lectures,
                   COUNT(DISTINCT vm.vl_id) AS unique_lecturers,
                   SUM(vd.price) AS total_payment
            FROM vl_management vm
            JOIN vl_description vd ON vd.vlm_id = vm.id
            WHERE vm.status = 1 AND vm.office_id = %s
            GROUP BY vm.subject_name
            ORDER BY total_lectures DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No subject summary data found."
        lines = [f"- {r['subject_name']}: {r['total_lectures']} Lectures, {r['unique_lecturers']} VLs, Payment: {r['total_payment']}" for r in rows]
        return "Visiting Lecturer Subject Summary:\n" + "\n".join(lines)

    elif query_id == "FACULTY_VL_COURSE_SUMMARY":
        cur.execute("""
            SELECT c.course_name, tc.course_batch,
                   COUNT(vm.id) AS total_vl_lectures,
                   COUNT(DISTINCT vm.vl_id) AS unique_vl_count,
                   SUM(vd.price) AS total_payment
            FROM vl_description vd
            JOIN vl_management vm ON vm.id = vd.vlm_id
            JOIN training_calendars tc ON tc.id = vd.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE vm.status = 1 AND vm.office_id = %s
            GROUP BY c.id, tc.id, c.course_name, tc.course_batch
            ORDER BY total_vl_lectures DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No course summary data found."
        lines = [f"- {r['course_name']} ({r['course_batch']}): {r['total_vl_lectures']} VL Lectures, {r['unique_vl_count']} VLs, Payment: {r['total_payment']}" for r in rows]
        return "Visiting Lecturer Course Summary:\n" + "\n".join(lines)

    elif query_id == "FACULTY_AVAILABILITY":
        cur.execute("""
            SELECT u.id, u.name, u.name_hindi, u.mobile, u.email,
                   desi.desi_name AS designation, desi.desi_code
            FROM users u
            JOIN designations desi ON desi.id = u.desi_id
            WHERE desi.lecture = 1
              AND u.status = 1 AND u.office_id = %s
            ORDER BY u.name
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No available faculty found."
        lines = [f"- {r['name']} ({r['designation']}): {r['mobile'] or 'N/A'}" for r in rows]
        return "Faculty Availability List:\n" + "\n".join(lines)

    elif query_id == "FACULTY_VL_DAILY":
        cur.execute("""
            SELECT vm.vl_date, vm.subject_name,
                   u.name AS vl_name, desi.desi_name AS designation,
                   vd.lecture_date, vd.price,
                   c.course_name, tc.course_batch
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            LEFT JOIN designations desi ON desi.id = u.desi_id
            JOIN vl_description vd ON vd.vlm_id = vm.id
            JOIN training_calendars tc ON tc.id = vd.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE vd.lecture_date = CURDATE()
              AND vm.status = 1 AND vm.office_id = %s
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No visiting lectures scheduled for today."
        lines = [f"- {r['vl_name']} ({r['designation']}): {r['subject_name']} for {r['course_name']}" for r in rows]
        return "Today's Visiting Lectures:\n" + "\n".join(lines)

    elif query_id == "FACULTY_VL_UPCOMING":
        cur.execute("""
            SELECT vm.vl_date, vm.subject_name,
                   u.name AS vl_name,
                   vd.lecture_date, vd.price,
                   c.course_name, tc.course_batch
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            JOIN vl_description vd ON vd.vlm_id = vm.id
            JOIN training_calendars tc ON tc.id = vd.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE vd.lecture_date > CURDATE()
              AND vm.status = 1 AND vm.office_id = %s
            ORDER BY vd.lecture_date ASC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No upcoming visiting lectures found."
        lines = [f"- {r['lecture_date']}: {r['vl_name']} ({r['subject_name']}) - {r['course_name']}" for r in rows]
        return "Upcoming Visiting Lectures:\n" + "\n".join(lines)

    elif query_id == "FACULTY_VL_COMPLETED":
        cur.execute("""
            SELECT vm.vl_date, vm.subject_name,
                   u.name AS vl_name,
                   vd.lecture_date, vd.price,
                   c.course_name, tc.course_batch
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            JOIN vl_description vd ON vd.vlm_id = vm.id
            JOIN training_calendars tc ON tc.id = vd.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE vd.lecture_date < CURDATE()
              AND vm.status = 1 AND vm.office_id = %s
            ORDER BY vd.lecture_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No completed visiting lectures found."
        lines = [f"- {r['lecture_date']}: {r['vl_name']} ({r['subject_name']}) - {r['course_name']}" for r in rows]
        return "Completed Visiting Lectures:\n" + "\n".join(lines)

    elif query_id == "FACULTY_VL_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(id) FROM vl_management WHERE status=1 AND office_id=%s) AS total_vl_entries,
              (SELECT COUNT(id) FROM vl_description WHERE status=1 AND office_id=%s) AS total_lecture_slots,
              (SELECT SUM(price) FROM vl_description WHERE status=1 AND office_id=%s) AS total_payment_amount,
              (SELECT COUNT(DISTINCT vl_id) FROM vl_management WHERE status=1 AND office_id=%s) AS unique_vl_count,
              (SELECT COUNT(id) FROM vl_description WHERE lecture_date = CURDATE() AND status=1 AND office_id=%s) AS todays_lectures
        """, (office_id, office_id, office_id, office_id, office_id))
        r = cur.fetchone()
        if not r: return "Could not generate VL module summary."
        return (f"Faculty & VL Module Summary:\n"
                f"Total VL Entries: {r['total_vl_entries']}\n"
                f"Total Lecture Slots: {r['total_lecture_slots']}\n"
                f"Total Payment Amount: {r['total_payment_amount']}\n"
                f"Unique Visiting Lecturers: {r['unique_vl_count']}\n"
                f"Today's Lectures: {r['todays_lectures']}")

    return None
