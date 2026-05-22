"""Attendance module query templates."""

TEMPLATES = [
    {
        "id": "ATTENDANCE_TOTAL_RECORDS",
        "module": "attendance",
        "description": "Total attendance records",
        "example_questions": ["Total attendance records?", "How many attendance entries?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_COUNT_BY_DATE",
        "module": "attendance",
        "description": "Attendance count by date",
        "example_questions": ["Attendance count by date?", "How many present today?"],
        "required_params": [],
        "optional_params": ["date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_TRAINEE_BY_NAME",
        "module": "attendance",
        "description": "Trainee attendance by name",
        "example_questions": ["Show attendance of trainee?", "Is Mayank present today?"],
        "required_params": [],
        "optional_params": ["user_name", "user_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_COURSE_WISE",
        "module": "attendance",
        "description": "Course-wise attendance",
        "example_questions": ["Course-wise attendance?", "Attendance by course?"],
        "required_params": [],
        "optional_params": ["course_id", "course_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_BATCH_WISE",
        "module": "attendance",
        "description": "Batch-wise attendance",
        "example_questions": ["Batch-wise attendance?", "Attendance by batch?"],
        "required_params": [],
        "optional_params": ["batch_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_ABSENT_TRAINEES",
        "module": "attendance",
        "description": "Absent trainees",
        "example_questions": ["Who is absent today?", "List absent trainees"],
        "required_params": [],
        "optional_params": ["date", "course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_PRESENT_TRAINEES",
        "module": "attendance",
        "description": "Present trainees",
        "example_questions": ["Who is present today?", "List present trainees"],
        "required_params": [],
        "optional_params": ["date", "course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_PERCENTAGE",
        "module": "attendance",
        "description": "Attendance percentage",
        "example_questions": ["What is attendance percentage?", "Show attendance rate"],
        "required_params": [],
        "optional_params": ["course_id", "from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_PUNCH_COUNT",
        "module": "attendance",
        "description": "Punch count",
        "example_questions": ["Total punches today?", "How many punches?"],
        "required_params": [],
        "optional_params": ["date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_TODAY",
        "module": "attendance",
        "description": "Today's attendance",
        "example_questions": ["Today's attendance?", "Who came today?", "Give me today's attendance summary."],
        "required_params": [],
        "optional_params": ["office_id", "course_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_MONTHLY",
        "module": "attendance",
        "description": "Monthly attendance",
        "example_questions": ["Monthly attendance?", "This month attendance?"],
        "required_params": [],
        "optional_params": ["month", "year", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_YEAR_WISE",
        "module": "attendance",
        "description": "Year-wise attendance",
        "example_questions": ["Year-wise attendance?", "Annual attendance?"],
        "required_params": [],
        "optional_params": ["year", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_BY_TRAINEE",
        "module": "attendance",
        "description": "Attendance by trainee",
        "example_questions": ["Show my attendance?", "Attendance of trainee?"],
        "required_params": [],
        "optional_params": ["user_id", "user_name", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "staff", "trainee"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_SUMMARY",
        "module": "attendance",
        "description": "Attendance summary",
        "example_questions": ["Attendance summary?", "Overall attendance stats?"],
        "required_params": [],
        "optional_params": ["from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_BY_DEPARTMENT",
        "module": "attendance",
        "description": "Attendance by department",
        "example_questions": ["Department-wise attendance?", "Attendance by department?"],
        "required_params": [],
        "optional_params": ["department_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_BY_DESIGNATION",
        "module": "attendance",
        "description": "Attendance by designation",
        "example_questions": ["Designation-wise attendance?", "Attendance by designation?"],
        "required_params": [],
        "optional_params": ["designation_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_BY_OFFICE",
        "module": "attendance",
        "description": "Attendance by office",
        "example_questions": ["Office-wise attendance?", "Attendance by office?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "ATTENDANCE_IRREGULAR",
        "module": "attendance",
        "description": "Irregular/late attendance",
        "example_questions": ["Irregular attendance?", "Late comers?"],
        "required_params": [],
        "optional_params": ["from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_DETAILED_LIST",
        "module": "attendance",
        "description": "Detailed attendance list",
        "example_questions": ["Show attendance details?", "Detailed attendance report?"],
        "required_params": [],
        "optional_params": ["from_date", "to_date", "course_id", "office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "ATTENDANCE_MODULE_SUMMARY",
        "module": "attendance",
        "description": "Attendance module summary",
        "example_questions": ["Attendance summary?", "Attendance module overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute attendance queries."""
    p = params or {}
    
    if query_id == "ATTENDANCE_TOTAL_RECORDS":
        cur.execute("SELECT COUNT(*) AS total FROM attendances a JOIN users u ON u.id = a.user_id WHERE u.office_id = %s", (office_id,))
        r = cur.fetchone()
        return f"Total attendance records: {r['total'] if r else 0}"
        
    elif query_id == "ATTENDANCE_COUNT_BY_DATE":
        date = p.get("date")
        if date:
            cur.execute("SELECT COUNT(*) AS total FROM attendances a JOIN users u ON u.id = a.user_id WHERE u.office_id = %s AND DATE(a.punch_time) = %s", (office_id, date))
        else:
            cur.execute("SELECT COUNT(*) AS total FROM attendances a JOIN users u ON u.id = a.user_id WHERE u.office_id = %s AND DATE(a.punch_time) = CURDATE()", (office_id,))
        r = cur.fetchone()
        return f"Attendance count: {r['total'] if r else 0}"

    elif query_id == "ATTENDANCE_TRAINEE_BY_NAME":
        name = p.get("user_name") or p.get("name")
        if not name: return "Please specify a trainee name."
        cur.execute("""
            SELECT a.id, u.name, u.name_hindi, c.course_name, tc.course_batch,
                   a.punch_time, a.punch,  a.status, a.created_at
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE u.name LIKE CONCAT('%%', %s, '%%')
              AND a.status = 1 AND tc.office_id = %s
            ORDER BY a.punch_time DESC
            LIMIT 50
        """, (name, office_id))
        rows = cur.fetchall()
        if not rows: return f"No attendance records found for trainee '{name}'."
        lines = [f"- {r['name']} ({r['course_name']}): {r['punch_time']} - {'Present' if r['punch'] == '4' else 'Absent'}" for r in rows]
        return f"Attendance Records for '{name}':\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_COURSE_WISE":
        cur.execute("""
            SELECT c.course_name, tc.course_batch, tc.from_date, tc.to_date,
                   COUNT(DISTINCT a.user_id) AS total_trainees,
                   SUM(CASE WHEN a.punch = '4' THEN 1 ELSE 0 END) AS present_count,
                   SUM(CASE WHEN a.punch = '5' THEN 1 ELSE 0 END) AS absent_count
            FROM attendances a
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.status = 1 AND tc.office_id = %s
            GROUP BY a.course_id, c.course_name, tc.course_batch, tc.from_date, tc.to_date
            ORDER BY tc.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No course-wise attendance data found."
        lines = [f"- {r['course_name']} ({r['course_batch']}): {r['present_count']} Present, {r['absent_count']} Absent, {r['total_trainees']} Total Trainees" for r in rows]
        return "Course-wise Attendance:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_BATCH_WISE":
        cur.execute("""
            SELECT tc.batch_no, tc.course_batch, tc.from_date, tc.to_date,
                   c.course_name,
                   COUNT(DISTINCT a.user_id) AS total_trainees,
                   COUNT(DISTINCT DATE(a.punch_time)) AS total_days,
                   SUM(CASE WHEN a.punch = '4' THEN 1 ELSE 0 END) AS present_count,
                   SUM(CASE WHEN a.punch = '5' THEN 1 ELSE 0 END) AS absent_count
            FROM attendances a
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.status = 1 AND tc.office_id = %s
            GROUP BY tc.id, tc.batch_no, tc.course_batch, tc.from_date, tc.to_date, c.course_name
            ORDER BY tc.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No batch-wise attendance data found."
        lines = [f"- Batch {r['course_batch']} ({r['course_name']}): {r['total_trainees']} Trainees, {r['total_days']} Days, {r['present_count']} Present, {r['absent_count']} Absent" for r in rows]
        return "Batch-wise Attendance:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_ABSENT_TRAINEES":
        date = p.get("date")
        q = """
            SELECT a.id, u.name, u.name_hindi, u.mobile,
                   c.course_name, tc.course_batch,
                   DATE(a.punch_time) AS attendance_date
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.punch = '5' AND a.status = 1 AND tc.office_id = %s
        """
        params = [office_id]
        if date:
            q += " AND DATE(a.punch_time) = %s"
            params.append(date)
        q += " ORDER BY a.punch_time DESC LIMIT 50"
        cur.execute(q, tuple(params))
        rows = cur.fetchall()
        if not rows: return "No absent trainees found."
        lines = [f"- {r['name']} ({r['course_name']}) on {r['attendance_date']}" for r in rows]
        return "Absent Trainees:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_PRESENT_TRAINEES":
        date = p.get("date")
        q = """
            SELECT a.id, u.name, u.name_hindi, u.mobile,
                   c.course_name, tc.course_batch,
                   DATE(a.punch_time) AS attendance_date
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.punch = '4' AND a.status = 1 AND tc.office_id = %s
        """
        params = [office_id]
        if date:
            q += " AND DATE(a.punch_time) = %s"
            params.append(date)
        q += " ORDER BY a.punch_time DESC LIMIT 50"
        cur.execute(q, tuple(params))
        rows = cur.fetchall()
        if not rows: return "No present trainees found."
        lines = [f"- {r['name']} ({r['course_name']}) on {r['attendance_date']}" for r in rows]
        return "Present Trainees:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_PERCENTAGE":
        cur.execute("""
            SELECT u.name, u.name_hindi, c.course_name, tc.course_batch,
                   COUNT(DISTINCT DATE(a.punch_time)) AS days_present,
                   tc.working_days,
                   ROUND(
                     (COUNT(DISTINCT DATE(a.punch_time)) / NULLIF(tc.working_days, 0)) * 100, 2
                   ) AS attendance_percentage
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.punch = '4' AND a.status = 1 AND tc.office_id = %s
            GROUP BY a.user_id, a.course_id, u.name, u.name_hindi, c.course_name,
                     tc.course_batch, tc.working_days
            ORDER BY attendance_percentage ASC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No attendance percentage data found."
        lines = [f"- {r['name']} ({r['course_name']}): {r['attendance_percentage']}% ({r['days_present']}/{r['working_days']} days)" for r in rows]
        return "Attendance Percentage:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_PUNCH_COUNT":
        cur.execute("""
            SELECT u.name, DATE(a.punch_time) AS att_date,
                   COUNT(a.id) AS punch_count,
                   MIN(a.punch_time) AS first_punch,
                   MAX(a.punch_time) AS last_punch
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            WHERE a.status = 1 AND u.office_id = %s
            GROUP BY a.user_id, DATE(a.punch_time), u.name
            ORDER BY att_date DESC, u.name
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No punch count data found."
        lines = [f"- {r['name']} on {r['att_date']}: {r['punch_count']} punches (First: {r['first_punch']}, Last: {r['last_punch']})" for r in rows]
        return "Attendance Punch Count:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_TODAY":
        cur.execute("""
            SELECT a.id, u.name, u.name_hindi, u.mobile,
                   c.course_name, tc.course_batch,
                   a.punch_time, a.punch, 
                   CASE a.punch WHEN '4' THEN 'Present' WHEN '5' THEN 'Absent' WHEN '1' THEN 'CL' WHEN '2' THEN 'LAP' WHEN '3' THEN 'SL' ELSE 'Absent' END AS status_label
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE DATE(a.punch_time) = CURDATE()
              AND a.status = 1 AND tc.office_id = %s
            ORDER BY a.punch_time DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No attendance records found for today."
        lines = [f"- {r['name']} ({r['course_name']}): {r['status_label']} at {r['punch_time']}" for r in rows]
        return "Today's Attendance:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_MONTHLY":
        cur.execute("""
            SELECT YEAR(a.punch_time) AS yr, MONTH(a.punch_time) AS mo,
                   MONTHNAME(a.punch_time) AS month_name,
                   COUNT(CASE WHEN a.punch = '4' THEN 1 END) AS present_count,
                   COUNT(CASE WHEN a.punch = '5' THEN 1 END) AS absent_count,
                   COUNT(a.id) AS total_records
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            WHERE a.status = 1 AND u.office_id = %s
            GROUP BY YEAR(a.punch_time), MONTH(a.punch_time), MONTHNAME(a.punch_time)
            ORDER BY yr DESC, mo DESC
            LIMIT 24
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No monthly attendance summary found."
        lines = [f"- {r['month_name']} {r['yr']}: {r['present_count']} Present, {r['absent_count']} Absent, {r['total_records']} Total" for r in rows]
        return "Monthly Attendance Summary:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_YEAR_WISE":
        cur.execute("""
            SELECT YEAR(a.punch_time) AS yr,
                   COUNT(DISTINCT a.user_id) AS unique_trainees,
                   COUNT(CASE WHEN a.punch = '4' THEN 1 END) AS present_count,
                   COUNT(CASE WHEN a.punch = '5' THEN 1 END) AS absent_count,
                   COUNT(DISTINCT a.course_id) AS total_courses
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            WHERE a.status = 1 AND u.office_id = %s
            GROUP BY YEAR(a.punch_time)
            ORDER BY yr DESC
            LIMIT 10
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No year-wise attendance summary found."
        lines = [f"- Year {r['yr']}: {r['unique_trainees']} Trainees, {r['present_count']} Present, {r['absent_count']} Absent, {r['total_courses']} Courses" for r in rows]
        return "Year-wise Attendance Summary:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_BY_TRAINEE":
        uid = p.get("user_id")
        if not uid: return "Please specify user_id."
        cur.execute("""
            SELECT DATE(a.punch_time) AS att_date,
                   a.punch_time, a.punch,
                   CASE a.punch WHEN '4' THEN 'Present' WHEN '5' THEN 'Absent' WHEN '1' THEN 'CL' WHEN '2' THEN 'LAP' WHEN '3' THEN 'SL' ELSE 'Absent' END AS att_status,
                   c.course_name, tc.course_batch, a.remarks
            FROM attendances a
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.user_id = %s
              AND a.status = 1 AND tc.office_id = %s
            ORDER BY a.punch_time DESC
            LIMIT 50
        """, (uid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No attendance records found for user ID {uid}."
        lines = [f"- {r['att_date']} ({r['course_name']}): {r['att_status']} at {r['punch_time']}" for r in rows]
        return f"Attendance for Trainee {uid}:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_SUMMARY":
        cur.execute("""
            SELECT COUNT(DISTINCT a.user_id) AS total_trainees,
                   COUNT(DISTINCT a.course_id) AS total_courses,
                   COUNT(a.id) AS total_records,
                   SUM(CASE WHEN a.punch = '4' THEN 1 ELSE 0 END) AS total_present,
                   SUM(CASE WHEN a.punch = '5' THEN 1 ELSE 0 END) AS total_absent,
                   ROUND(SUM(CASE WHEN a.punch = '4' THEN 1 ELSE 0 END) / COUNT(a.id) * 100, 2) AS overall_present_pct
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            WHERE a.status = 1 AND u.office_id = %s
        """, (office_id,))
        r = cur.fetchone()
        if not r or not r.get("total_records"): return "No overall attendance summary found."
        return (f"Overall Attendance Summary:\n"
                f"Total Trainees: {r['total_trainees']}\n"
                f"Total Courses: {r['total_courses']}\n"
                f"Total Records: {r['total_records']}\n"
                f"Present: {r['total_present']} ({r['overall_present_pct']}%)\n"
                f"Absent: {r['total_absent']}")

    elif query_id == "ATTENDANCE_BY_DEPARTMENT":
        cur.execute("""
            SELECT d.department_name,
                   COUNT(DISTINCT a.user_id) AS trainee_count,
                   SUM(CASE WHEN a.punch = '4' THEN 1 ELSE 0 END) AS present_count,
                   SUM(CASE WHEN a.punch = '5' THEN 1 ELSE 0 END) AS absent_count
            FROM attendances a
            JOIN tra_masters tm ON tm.user_id = a.user_id AND tm.course_id = a.course_id
            JOIN departments d ON d.id = tm.dep_id
            WHERE a.status = 1 AND tm.office_id = %s
            GROUP BY d.id, d.department_name
            ORDER BY d.department_name
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No department-wise attendance data found."
        lines = [f"- {r['department_name']}: {r['trainee_count']} Trainees, {r['present_count']} Present, {r['absent_count']} Absent" for r in rows]
        return "Attendance by Department:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_BY_DESIGNATION":
        cur.execute("""
            SELECT desi.desi_name,
                   COUNT(DISTINCT a.user_id) AS trainee_count,
                   SUM(CASE WHEN a.punch = '4' THEN 1 ELSE 0 END) AS present_count,
                   SUM(CASE WHEN a.punch = '5' THEN 1 ELSE 0 END) AS absent_count
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN designations desi ON desi.id = u.desi_id
            WHERE a.status = 1 AND u.office_id = %s
            GROUP BY desi.id, desi.desi_name
            ORDER BY desi.desi_name
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No designation-wise attendance data found."
        lines = [f"- {r['desi_name']}: {r['trainee_count']} Trainees, {r['present_count']} Present, {r['absent_count']} Absent" for r in rows]
        return "Attendance by Designation:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_BY_OFFICE":
        cur.execute("""
            SELECT tc.office_id,
                   COUNT(DISTINCT a.user_id) AS trainee_count,
                   SUM(CASE WHEN a.punch = '4' THEN 1 ELSE 0 END) AS present_count,
                   SUM(CASE WHEN a.punch = '5' THEN 1 ELSE 0 END) AS absent_count
            FROM attendances a
            JOIN training_calendars tc ON tc.id = a.course_id
            WHERE a.status = 1 AND tc.office_id = %s
            GROUP BY tc.office_id
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No office-wise attendance data found."
        lines = [f"- Office {r['office_id']}: {r['trainee_count']} Trainees, {r['present_count']} Present, {r['absent_count']} Absent" for r in rows]
        return "Attendance by Office:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_IRREGULAR":
        cur.execute("""
            SELECT u.name, u.name_hindi, u.mobile,
                   c.course_name, tc.course_batch,
                   COUNT(DISTINCT DATE(a.punch_time)) AS days_present,
                   tc.working_days,
                   ROUND(COUNT(DISTINCT DATE(a.punch_time)) / NULLIF(tc.working_days,0) * 100, 2) AS att_pct
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.punch = '4'
              AND a.status = 1 AND tc.office_id = %s
            GROUP BY a.user_id, a.course_id, u.name, u.name_hindi, u.mobile,
                     c.course_name, tc.course_batch, tc.working_days
            HAVING att_pct < 75
            ORDER BY att_pct ASC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No irregular trainees found (all above 75%)."
        lines = [f"- {r['name']} ({r['course_name']}): {r['att_pct']}% ({r['days_present']}/{r['working_days']} days)" for r in rows]
        return "Irregular Trainees (< 75%):\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_DETAILED_LIST":
        cur.execute("""
            SELECT a.id, u.name, u.name_hindi, u.mobile,
                   desi.desi_name AS designation,
                   c.course_name, tc.course_batch, tc.batch_no,
                   DATE(a.punch_time) AS att_date,
                   TIME(a.punch_time) AS att_time,
                   a.punch,
                   CASE a.punch WHEN '4' THEN 'Present' WHEN '5' THEN 'Absent' WHEN '1' THEN 'CL' WHEN '2' THEN 'LAP' WHEN '3' THEN 'SL' ELSE 'Absent' END AS att_status,
                   a.remarks, a.created_at
            FROM attendances a
            JOIN users u ON u.id = a.user_id
            LEFT JOIN designations desi ON desi.id = u.desi_id
            JOIN training_calendars tc ON tc.id = a.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE a.status = 1 AND tc.office_id = %s
            ORDER BY a.punch_time DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No detailed attendance records found."
        lines = [f"- {r['name']} ({r['course_name']}): {r['att_status']} on {r['att_date']} at {r['att_time']}" for r in rows]
        return "Detailed Attendance List:\n" + "\n".join(lines)

    elif query_id == "ATTENDANCE_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(DISTINCT a.user_id) FROM attendances a JOIN users u ON u.id = a.user_id WHERE a.status=1 AND a.punch='4' AND DATE(a.punch_time)=CURDATE() AND u.office_id=%s) AS present_today,
              (SELECT COUNT(DISTINCT a.user_id) FROM attendances a JOIN users u ON u.id = a.user_id WHERE a.status=1 AND a.punch='5' AND DATE(a.punch_time)=CURDATE() AND u.office_id=%s) AS absent_today,
              (SELECT COUNT(DISTINCT a.user_id) FROM attendances a JOIN users u ON u.id = a.user_id WHERE a.status=1 AND u.office_id=%s) AS total_trainees_tracked,
              (SELECT COUNT(DISTINCT a.course_id) FROM attendances a JOIN users u ON u.id = a.user_id WHERE a.status=1 AND u.office_id=%s) AS total_courses,
              (SELECT COUNT(a.id) FROM attendances a JOIN users u ON u.id = a.user_id WHERE a.status=1 AND DATE(a.punch_time)=CURDATE() AND u.office_id=%s) AS total_punches_today
        """, (office_id, office_id, office_id, office_id, office_id))
        r = cur.fetchone()
        if not r: return "Could not generate attendance module summary."
        return (f"Attendance Module Summary:\n"
                f"Present Today: {r['present_today']}\n"
                f"Absent Today: {r['absent_today']}\n"
                f"Total Trainees Tracked: {r['total_trainees_tracked']}\n"
                f"Total Courses: {r['total_courses']}\n"
                f"Total Punches Today: {r['total_punches_today']}")

    return None
