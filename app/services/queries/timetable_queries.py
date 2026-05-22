"""Timetable module query templates."""

TEMPLATES = [
    {
        "id": "TIMETABLE_TODAY",
        "module": "timetable",
        "description": "Today's timetable",
        "example_questions": ["Today's timetable?", "What lectures today?"],
        "required_params": [],
        "optional_params": ["office_id", "course_id"],
        "allowed_roles": ["principal", "admin", "staff", "trainee"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_TOMORROW",
        "module": "timetable",
        "description": "Tomorrow's timetable",
        "example_questions": ["Tomorrow's timetable?", "What lectures tomorrow?"],
        "required_params": [],
        "optional_params": ["office_id", "course_id"],
        "allowed_roles": ["principal", "admin", "staff", "trainee"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_WEEKLY",
        "module": "timetable",
        "description": "Weekly timetable",
        "example_questions": ["Weekly timetable?", "This week lectures?"],
        "required_params": [],
        "optional_params": ["office_id", "course_id", "week_start"],
        "allowed_roles": ["principal", "admin", "staff", "trainee"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_COURSE",
        "module": "timetable",
        "description": "Course timetable",
        "example_questions": ["Course timetable?", "Batch timetable?"],
        "required_params": [],
        "optional_params": ["course_id", "course_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff", "trainee"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_BATCH",
        "module": "timetable",
        "description": "Batch timetable",
        "example_questions": ["Batch timetable?", "Specific batch schedule?"],
        "required_params": [],
        "optional_params": ["batch_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff", "trainee"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_SUBJECT_WISE",
        "module": "timetable",
        "description": "Subject-wise timetable",
        "example_questions": ["Subject-wise timetable?", "Lectures for subject?"],
        "required_params": [],
        "optional_params": ["subject_id", "subject_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_FACULTY_WISE",
        "module": "timetable",
        "description": "Faculty-wise timetable",
        "example_questions": ["Faculty timetable?", "Teacher's schedule?"],
        "required_params": [],
        "optional_params": ["faculty_id", "faculty_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_CLASSROOM",
        "module": "timetable",
        "description": "Classroom timetable",
        "example_questions": ["Classroom schedule?", "Room booking?"],
        "required_params": [],
        "optional_params": ["classroom_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_SESSION",
        "module": "timetable",
        "description": "Session-wise timetable",
        "example_questions": ["Session timetable?", "Period schedule?"],
        "required_params": [],
        "optional_params": ["session_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_TOPIC",
        "module": "timetable",
        "description": "Topic-wise timetable",
        "example_questions": ["Topic schedule?", "When is topic covered?"],
        "required_params": [],
        "optional_params": ["topic_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_BY_DATE",
        "module": "timetable",
        "description": "Timetable by date",
        "example_questions": ["Timetable on date?", "Schedule for date?"],
        "required_params": [],
        "optional_params": ["date", "office_id", "course_id"],
        "allowed_roles": ["principal", "admin", "staff", "trainee"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_UPCOMING",
        "module": "timetable",
        "description": "Upcoming lectures",
        "example_questions": ["Upcoming lectures?", "Next lectures?"],
        "required_params": [],
        "optional_params": ["office_id", "course_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff", "trainee"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_COMPLETED",
        "module": "timetable",
        "description": "Completed lectures",
        "example_questions": ["Completed lectures?", "Past lectures?"],
        "required_params": [],
        "optional_params": ["office_id", "course_id", "from_date"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_VL",
        "module": "timetable",
        "description": "VL lectures",
        "example_questions": ["VL lectures?", "Visiting lecturer schedule?"],
        "required_params": [],
        "optional_params": ["vl_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_DEPT_WISE",
        "module": "timetable",
        "description": "Department-wise timetable",
        "example_questions": ["Department timetable?", "Dept schedule?"],
        "required_params": [],
        "optional_params": ["department_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_COUNT",
        "module": "timetable",
        "description": "Timetable count",
        "example_questions": ["Total timetable entries?", "How many lectures?"],
        "required_params": [],
        "optional_params": ["office_id", "course_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_HOURS_SUMMARY",
        "module": "timetable",
        "description": "Timetable hours summary",
        "example_questions": ["Total lecture hours?", "Hours per subject?"],
        "required_params": [],
        "optional_params": ["office_id", "course_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_COURSE_PLAN",
        "module": "timetable",
        "description": "Course lecture plan",
        "example_questions": ["Course plan?", "Lecture plan?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "TIMETABLE_MODULE_SUMMARY",
        "module": "timetable",
        "description": "Timetable module summary",
        "example_questions": ["Timetable summary?", "Timetable overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute timetable queries."""
    p = params or {}
    
    if query_id == "TIMETABLE_TOMORROW":
        cur.execute("""
            SELECT tm.tm_date, tm.start_time, tm.end_time,
                   c.course_name, tc.course_batch,
                   u.name AS faculty_name, desi.desi_name AS designation,
                   t.topic_name, s.subject_name
            FROM time_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            LEFT JOIN users u ON u.id = tm.desi_user_id
            LEFT JOIN designations desi ON desi.id = tm.desi_id
            LEFT JOIN topics t ON t.id = tm.topic_id
            LEFT JOIN subjects s ON s.id = tm.cs_id
            WHERE tm.tm_date = DATE_ADD(CURDATE(), INTERVAL 1 DAY)
              AND tm.status = 1 AND tc.office_id = %s
            ORDER BY tm.start_time
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No timetable entries found for tomorrow."
        lines = [f"- {r['start_time']} to {r['end_time']} ({r['course_name']}): {r['topic_name']} by {r['faculty_name']}" for r in rows]
        return "Timetable Tomorrow:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_WEEKLY":
        cur.execute("""
            SELECT tm.tm_date, tm.start_time, tm.end_time,
                   c.course_name, tc.course_batch,
                   u.name AS faculty_name, t.topic_name
            FROM time_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            LEFT JOIN users u ON u.id = tm.desi_user_id
            LEFT JOIN topics t ON t.id = tm.topic_id
            WHERE tm.tm_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
              AND tm.status = 1 AND tc.office_id = %s
            ORDER BY tm.tm_date, tm.start_time
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No weekly timetable found."
        lines = [f"- {r['tm_date']} {r['start_time']} ({r['course_name']}): {r['topic_name']} by {r['faculty_name']}" for r in rows]
        return "Weekly Timetable:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_COURSE":
        cid = p.get("course_id")
        if not cid: return "Please specify course_id."
        cur.execute("""
            SELECT tm.tm_date, tm.start_time, tm.end_time,
                   u.name AS faculty_name, desi.desi_name AS designation,
                   t.topic_name, s.subject_name
            FROM time_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            LEFT JOIN users u ON u.id = tm.desi_user_id
            LEFT JOIN designations desi ON desi.id = tm.desi_id
            LEFT JOIN topics t ON t.id = tm.topic_id
            LEFT JOIN subjects s ON s.id = tm.cs_id
            WHERE tm.course_id = %s AND tm.status = 1 AND tc.office_id = %s
            ORDER BY tm.tm_date, tm.start_time
            LIMIT 50
        """, (cid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No timetable found for course {cid}."
        lines = [f"- {r['tm_date']} {r['start_time']}: {r['topic_name']} by {r['faculty_name']}" for r in rows]
        return f"Timetable for Course {cid}:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_BATCH":
        batch = p.get("batch_no")
        if not batch: return "Please specify batch_no."
        cur.execute("""
            SELECT tm.tm_date, tm.start_time, tm.end_time,
                   tc.course_batch, c.course_name,
                   u.name AS faculty_name, t.topic_name
            FROM time_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            LEFT JOIN users u ON u.id = tm.desi_user_id
            LEFT JOIN topics t ON t.id = tm.topic_id
            WHERE tc.batch_no = %s AND tm.status = 1 AND tc.office_id = %s
            ORDER BY tm.tm_date, tm.start_time
            LIMIT 50
        """, (batch, office_id))
        rows = cur.fetchall()
        if not rows: return f"No timetable found for batch {batch}."
        lines = [f"- {r['tm_date']} {r['start_time']}: {r['topic_name']} by {r['faculty_name']}" for r in rows]
        return f"Timetable for Batch {batch}:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_SUBJECT_WISE":
        cur.execute("""
            SELECT s.subject_name, COUNT(tm.id) AS session_count,
                   SUM(TIMESTAMPDIFF(MINUTE, tm.start_time, tm.end_time))/60 AS total_hours
            FROM time_masters tm
            JOIN subjects s ON s.id = tm.cs_id
            JOIN training_calendars tc ON tc.id = tm.course_id
            WHERE tm.status = 1 AND tc.office_id = %s
            GROUP BY s.id, s.subject_name
            ORDER BY session_count DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No subject-wise timetable found."
        lines = [f"- {r['subject_name']}: {r['session_count']} Sessions, {r['total_hours']:.1f} Hours" for r in rows]
        return "Subject-wise Timetable:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_FACULTY_WISE":
        cur.execute("""
            SELECT u.name AS faculty_name, desi.desi_name AS designation,
                   COUNT(tm.id) AS sessions,
                   SUM(TIMESTAMPDIFF(MINUTE, tm.start_time, tm.end_time))/60 AS total_hours
            FROM time_masters tm
            JOIN users u ON u.id = tm.desi_user_id
            JOIN training_calendars tc ON tc.id = tm.course_id
            LEFT JOIN designations desi ON desi.id = tm.desi_id
            WHERE tm.status = 1 AND tc.office_id = %s
            GROUP BY u.id, u.name, desi.desi_name
            ORDER BY sessions DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No faculty-wise timetable found."
        lines = [f"- {r['faculty_name']}: {r['sessions']} Sessions, {r['total_hours']:.1f} Hours" for r in rows]
        return "Faculty-wise Timetable:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_CLASSROOM":
        class_id = p.get("class_id")
        if not class_id: return "Please specify class_id."
        cur.execute("""
            SELECT tm.tm_date, tm.start_time, tm.end_time, tm.class_id,
                   cr.class_name, c.course_name, tc.course_batch,
                   u.name AS faculty_name
            FROM time_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            LEFT JOIN class_rooms cr ON cr.id = tm.class_id
            LEFT JOIN users u ON u.id = tm.desi_user_id
            WHERE tm.class_id = %s AND tm.status = 1 AND tc.office_id = %s
            ORDER BY tm.tm_date, tm.start_time
            LIMIT 50
        """, (class_id, office_id))
        rows = cur.fetchall()
        if not rows: return f"No timetable found for classroom {class_id}."
        lines = [f"- {r['tm_date']} {r['start_time']} ({r['course_name']}): {r['faculty_name']}" for r in rows]
        return f"Timetable for Classroom {class_id}:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_SESSION":
        cur.execute("""
            SELECT ses.id, ses.session_name,
                   COUNT(tm.id) AS usage_count
            FROM sessions ses
            LEFT JOIN time_masters tm ON tm.session_id = ses.id AND tm.status = 1
            LEFT JOIN training_calendars tc ON tc.id = tm.course_id AND tc.office_id = %s
            WHERE ses.status = 1
            GROUP BY ses.id, ses.session_name
            ORDER BY usage_count DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No session data found."
        lines = [f"- {r['session_name']}: {r['usage_count']} Uses" for r in rows]
        return "Timetable Session Usage:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_TOPIC":
        cur.execute("""
            SELECT t.topic_name, COUNT(tm.id) AS sessions,
                   SUM(TIMESTAMPDIFF(MINUTE, tm.start_time, tm.end_time))/60 AS total_hours
            FROM time_masters tm
            JOIN topics t ON t.id = tm.topic_id
            JOIN training_calendars tc ON tc.id = tm.course_id
            WHERE tm.status = 1 AND tc.office_id = %s
            GROUP BY t.id, t.topic_name
            ORDER BY sessions DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No topic data found."
        lines = [f"- {r['topic_name']}: {r['sessions']} Sessions, {r['total_hours']:.1f} Hours" for r in rows]
        return "Timetable Topic Summary:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_BY_DATE" or query_id == "TIMETABLE_TODAY":
        d = p.get("date") if query_id == "TIMETABLE_BY_DATE" else "CURDATE()"
        query = f"""
            SELECT tm.tm_date, tm.start_time, tm.end_time,
                   c.course_name, tc.course_batch,
                   u.name AS faculty_name, t.topic_name
            FROM time_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            LEFT JOIN users u ON u.id = tm.desi_user_id
            LEFT JOIN topics t ON t.id = tm.topic_id
            WHERE tm.tm_date = {d if d == 'CURDATE()' else '%s'} AND tm.status = 1 AND tc.office_id = %s
            ORDER BY tm.start_time
            LIMIT 50
        """
        if d == 'CURDATE()':
            cur.execute(query, (office_id,))
        else:
            cur.execute(query, (d, office_id))
            
        rows = cur.fetchall()
        if not rows: return f"No timetable found for {d}."
        lines = [f"- {r['start_time']} to {r['end_time']} ({r['course_name']}): {r['topic_name']} by {r['faculty_name']}" for r in rows]
        return f"Timetable for {d}:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_UPCOMING":
        cur.execute("""
            SELECT tm.tm_date, tm.start_time, c.course_name, tc.course_batch,
                   u.name AS faculty_name, t.topic_name
            FROM time_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            LEFT JOIN users u ON u.id = tm.desi_user_id
            LEFT JOIN topics t ON t.id = tm.topic_id
            WHERE tm.tm_date >= CURDATE() AND tm.status = 1 AND tc.office_id = %s
            ORDER BY tm.tm_date, tm.start_time
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No upcoming timetable found."
        lines = [f"- {r['tm_date']} {r['start_time']} ({r['course_name']}): {r['topic_name']} by {r['faculty_name']}" for r in rows]
        return "Upcoming Timetable:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_COMPLETED":
        cur.execute("""
            SELECT tm.tm_date, tm.start_time, tm.end_time,
                   c.course_name, tc.course_batch,
                   u.name AS faculty_name, t.topic_name
            FROM time_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            LEFT JOIN users u ON u.id = tm.desi_user_id
            LEFT JOIN topics t ON t.id = tm.topic_id
            WHERE tm.tm_date < CURDATE() AND tm.status = 1 AND tc.office_id = %s
            ORDER BY tm.tm_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No completed timetable found."
        lines = [f"- {r['tm_date']} ({r['course_name']}): {r['topic_name']} by {r['faculty_name']}" for r in rows]
        return "Completed Timetable:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_VL":
        cur.execute("""
            SELECT tm.tm_date, tm.start_time, tm.end_time,
                   vm.subject_name AS vl_subject, u_vl.name AS vl_name,
                   c.course_name, tc.course_batch
            FROM time_masters tm
            JOIN vl_management vm ON vm.id = tm.vl_id
            JOIN users u_vl ON u_vl.id = vm.vl_id
            JOIN training_calendars tc ON tc.id = tm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE tm.vl_id > 0 AND tm.status = 1 AND tc.office_id = %s
            ORDER BY tm.tm_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No VL timetable found."
        lines = [f"- {r['tm_date']} ({r['course_name']}): {r['vl_subject']} by {r['vl_name']}" for r in rows]
        return "Timetable for Visiting Lecturers:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_DEPT_WISE":
        cur.execute("""
            SELECT d.department_name, COUNT(tm.id) AS session_count
            FROM time_masters tm
            JOIN users u ON u.id = tm.desi_user_id
            JOIN departments d ON d.id = u.desi_id
            JOIN training_calendars tc ON tc.id = tm.course_id
            WHERE tm.status = 1 AND tc.office_id = %s
            GROUP BY d.id, d.department_name
            ORDER BY session_count DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No department-wise timetable found."
        lines = [f"- {r['department_name']}: {r['session_count']} Sessions" for r in rows]
        return "Department-wise Timetable:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_COUNT":
        cur.execute("SELECT COUNT(tm.id) AS total_sessions FROM time_masters tm JOIN training_calendars tc ON tc.id=tm.course_id WHERE tm.status = 1 AND tc.office_id = %s", (office_id,))
        r = cur.fetchone()
        return f"Total sessions: {r['total_sessions'] if r else 0}"

    elif query_id == "TIMETABLE_HOURS_SUMMARY":
        cur.execute("""
            SELECT YEAR(tm.tm_date) AS yr, MONTH(tm.tm_date) AS mo,
                   MONTHNAME(tm.tm_date) AS month_name,
                   COUNT(tm.id) AS sessions,
                   ROUND(SUM(TIMESTAMPDIFF(MINUTE, tm.start_time, tm.end_time))/60, 2) AS total_hours
            FROM time_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id
            WHERE tm.status = 1 AND tc.office_id = %s
            GROUP BY YEAR(tm.tm_date), MONTH(tm.tm_date)
            ORDER BY yr DESC, mo DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No hours summary found."
        lines = [f"- {r['month_name']} {r['yr']}: {r['sessions']} Sessions, {r['total_hours']} Hours" for r in rows]
        return "Timetable Hours Summary:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_COURSE_PLAN":
        cur.execute("""
            SELECT tt.id, tt.course_id, c.course_name,
                   tt.month, tt.year, tt.faculties, tt.type
            FROM tt_designs tt
            JOIN training_calendars tc ON tc.id = tt.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE tt.status = 1 AND tc.office_id = %s
            ORDER BY tt.year DESC, tt.month DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No course plan found."
        lines = [f"- {r['course_name']} ({r['month']}/{r['year']}): Type {r['type']}" for r in rows]
        return "Course Plan:\n" + "\n".join(lines)

    elif query_id == "TIMETABLE_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(tm.id) FROM time_masters tm JOIN training_calendars tc ON tc.id=tm.course_id WHERE tm.status=1 AND tc.office_id=%s) AS total_sessions,
              (SELECT COUNT(tm.id) FROM time_masters tm JOIN training_calendars tc ON tc.id=tm.course_id WHERE tm.tm_date = CURDATE() AND tm.status=1 AND tc.office_id=%s) AS todays_sessions,
              (SELECT COUNT(tm.id) FROM time_masters tm JOIN training_calendars tc ON tc.id=tm.course_id WHERE tm.tm_date = DATE_ADD(CURDATE(),INTERVAL 1 DAY) AND tm.status=1 AND tc.office_id=%s) AS tomorrow_sessions,
              (SELECT COUNT(DISTINCT tm.desi_user_id) FROM time_masters tm JOIN training_calendars tc ON tc.id=tm.course_id WHERE tm.status=1 AND tc.office_id=%s) AS active_faculty,
              (SELECT COUNT(DISTINCT tm.course_id) FROM time_masters tm JOIN training_calendars tc ON tc.id=tm.course_id WHERE tm.status=1 AND tc.office_id=%s) AS courses_with_timetable
        """, (office_id, office_id, office_id, office_id, office_id))
        r = cur.fetchone()
        if not r: return "Could not generate timetable module summary."
        return (f"Timetable Module Summary:\n"
                f"Total Sessions: {r['total_sessions']}\n"
                f"Today's Sessions: {r['todays_sessions']}\n"
                f"Tomorrow's Sessions: {r['tomorrow_sessions']}\n"
                f"Active Faculty: {r['active_faculty']}\n"
                f"Courses w/ Timetable: {r['courses_with_timetable']}")

    return None
