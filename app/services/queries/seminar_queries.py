"""Seminar module query templates."""

TEMPLATES = [
    {
        "id": "SEMINAR_TOTAL",
        "module": "seminar",
        "description": "Total seminars",
        "example_questions": ["Total seminars?", "How many seminars?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_UPCOMING",
        "module": "seminar",
        "description": "Upcoming seminars",
        "example_questions": ["Upcoming seminars?", "Future seminars?"],
        "required_params": [],
        "optional_params": ["office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_COMPLETED",
        "module": "seminar",
        "description": "Completed seminars",
        "example_questions": ["Completed seminars?", "Past seminars?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_BY_DATE",
        "module": "seminar",
        "description": "Seminar by date",
        "example_questions": ["Seminars on date?", "Date-wise seminars?"],
        "required_params": [],
        "optional_params": ["date", "from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_BY_TOPIC",
        "module": "seminar",
        "description": "Seminar by topic",
        "example_questions": ["Seminars by topic?", "Topic-wise seminars?"],
        "required_params": [],
        "optional_params": ["topic_id", "topic_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_BY_SPEAKER",
        "module": "seminar",
        "description": "Seminar by main speaker",
        "example_questions": ["Seminars by speaker?", "Speaker-wise seminars?"],
        "required_params": [],
        "optional_params": ["speaker_id", "speaker_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_BY_JUDGE",
        "module": "seminar",
        "description": "Seminar by judge",
        "example_questions": ["Seminars by judge?", "Judge-wise seminars?"],
        "required_params": [],
        "optional_params": ["judge_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_TOPIC_LIST",
        "module": "seminar",
        "description": "Seminar topic list",
        "example_questions": ["Seminar topics?", "List topics?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_DURATION",
        "module": "seminar",
        "description": "Seminar duration",
        "example_questions": ["Seminar duration?", "How long was seminar?"],
        "required_params": [],
        "optional_params": ["seminar_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_BY_TYPE",
        "module": "seminar",
        "description": "Seminar by type",
        "example_questions": ["Seminars by type?", "Type-wise seminars?"],
        "required_params": [],
        "optional_params": ["type_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_BY_VL",
        "module": "seminar",
        "description": "Seminar by VL",
        "example_questions": ["VL seminars?", "Seminars by visiting lecturer?"],
        "required_params": [],
        "optional_params": ["vl_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_MONTHLY_COUNT",
        "module": "seminar",
        "description": "Monthly seminar count",
        "example_questions": ["Monthly seminars?", "Seminars this month?"],
        "required_params": [],
        "optional_params": ["month", "year", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_ATTENDANCE",
        "module": "seminar",
        "description": "Seminar attendance",
        "example_questions": ["Seminar attendance?", "Who attended seminar?"],
        "required_params": [],
        "optional_params": ["seminar_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_REMARKS",
        "module": "seminar",
        "description": "Seminar remarks",
        "example_questions": ["Seminar remarks?", "Feedback on seminar?"],
        "required_params": [],
        "optional_params": ["seminar_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_STATUS_SUMMARY",
        "module": "seminar",
        "description": "Seminar status summary",
        "example_questions": ["Seminar status?", "Status summary?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_SUBJECT_SUMMARY",
        "module": "seminar",
        "description": "Seminar subject summary",
        "example_questions": ["Subject-wise seminar?", "Seminar by subject?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_TOPIC_SUMMARY",
        "module": "seminar",
        "description": "Seminar topic summary",
        "example_questions": ["Topic-wise seminar?", "Seminar topics count?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_OFFICE_SUMMARY",
        "module": "seminar",
        "description": "Seminar office summary",
        "example_questions": ["Office seminar summary?", "Office-wise seminars?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_DATE_RANGE",
        "module": "seminar",
        "description": "Seminar date range",
        "example_questions": ["Seminars in range?", "Date range seminars?"],
        "required_params": [],
        "optional_params": ["from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "SEMINAR_MODULE_SUMMARY",
        "module": "seminar",
        "description": "Seminar module summary",
        "example_questions": ["Seminar summary?", "Seminar module overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute seminar queries."""
    p = params or {}
    
    if query_id == "SEMINAR_UPCOMING":
        cur.execute("""
            SELECT s.id, s.sem_date, s.subject, s.start_time, s.end_time,
                   s.type_id, s.judge, s.main_speaker, s.se_status
            FROM seminars s
            WHERE s.sem_date >= CURDATE() AND s.status = 1
            ORDER BY s.sem_date ASC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No upcoming seminars found."
        lines = [f"- {r['subject']} ({r['sem_date']} {r['start_time']}): Speaker {r['main_speaker']} (Judge: {r['judge']})" for r in rows]
        return "Upcoming Seminars:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_COMPLETED":
        cur.execute("""
            SELECT s.id, s.sem_date, s.subject, s.start_time, s.end_time,
                   s.topic_remarks, s.se_status
            FROM seminars s
            WHERE s.sem_date < CURDATE() AND s.status = 1
            ORDER BY s.sem_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No completed seminars found."
        lines = [f"- {r['subject']} ({r['sem_date']}): {r['topic_remarks']}" for r in rows]
        return "Completed Seminars:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_BY_DATE":
        import calendar
        from app.services.date_parser import parse_loose_date

        raw_date_input = p.get("from_date") or p.get("sem_date") or p.get("date") or ""
        fdate = parse_loose_date(raw_date_input)
        explicit_tdate = parse_loose_date(p.get("to_date")) if p.get("to_date") else None
        tdate = explicit_tdate or fdate

        if not fdate or not tdate:
            return "Please specify from_date and to_date."

        # If user gave only a month name (no explicit to_date and no specific day),
        # check if it's purely a month string without a year.
        months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december", "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        is_only_month = not explicit_tdate and raw_date_input.strip().lower() in months

        if is_only_month:
            # User only provided a month. Query all years for that month to avoid 'guessed year' misses.
            try:
                mo = int(fdate.split("-")[1])
                cur.execute("""
                    SELECT s.id, s.sem_date, s.subject, s.start_time, s.end_time,
                           s.judge, s.main_speaker
                    FROM seminars s
                    WHERE MONTH(s.sem_date) = %s AND s.status = 1
                    ORDER BY s.sem_date DESC, s.start_time
                    LIMIT 50
                """, (mo,))
                rows = cur.fetchall()
                if not rows: return f"No seminars found in {raw_date_input.capitalize()}."
                lines = [f"- {r['subject']} ({r['sem_date']}) at {r['start_time']} (Speaker: {r['main_speaker']})" for r in rows]
                return f"Seminars in {raw_date_input.capitalize()}:\n" + "\n".join(lines)
            except Exception:
                pass  # Fall back to range query if something goes wrong

        if not explicit_tdate and fdate and fdate.endswith("-01"):
            try:
                parts = fdate.split("-")
                yr, mo = int(parts[0]), int(parts[1])
                last_day = calendar.monthrange(yr, mo)[1]
                tdate = f"{yr}-{mo:02d}-{last_day:02d}"
            except Exception:
                pass  # fall back to single-day range

        cur.execute("""
            SELECT s.id, s.sem_date, s.subject, s.start_time, s.end_time,
                   s.judge, s.main_speaker
            FROM seminars s
            WHERE DATE(s.sem_date) BETWEEN %s AND %s AND s.status = 1
            ORDER BY s.start_time
            LIMIT 50
        """, (fdate, tdate))
        rows = cur.fetchall()
        if not rows: return f"No seminars found in this date range ({fdate} to {tdate})."
        lines = [f"- {r['subject']} at {r['start_time']} (Speaker: {r['main_speaker']})" for r in rows]
        return f"Seminars from {fdate} to {tdate}:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_BY_TOPIC":
        tid = p.get("topic_id")
        if not tid: return "Please specify topic_id."
        cur.execute("""
            SELECT s.id, s.sem_date, s.subject,
                   st.sub_topic AS topic
            FROM seminars s
            JOIN seminars_topic st ON FIND_IN_SET(st.id, s.topic_id)
            WHERE st.id = %s AND s.status = 1 AND st.office_id = %s
            ORDER BY s.sem_date DESC
            LIMIT 50
        """, (tid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No seminars found for topic ID {tid}."
        lines = [f"- {r['subject']} ({r['sem_date']}) - Topic: {r['topic']}" for r in rows]
        return f"Seminars for Topic:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_BY_SPEAKER":
        speaker = p.get("speaker_name") or p.get("speaker")
        if not speaker: return "Please specify speaker_name."
        cur.execute("""
            SELECT s.id, s.sem_date, s.subject, s.main_speaker,
                   s.start_time, s.end_time
            FROM seminars s
            WHERE s.main_speaker LIKE CONCAT('%%', %s, '%%') AND s.status = 1
            ORDER BY s.sem_date DESC
            LIMIT 50
        """, (speaker,))
        rows = cur.fetchall()
        if not rows: return f"No seminars found for speaker '{speaker}'."
        lines = [f"- {r['subject']} ({r['sem_date']}) by {r['main_speaker']}" for r in rows]
        return f"Seminars by Speaker:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_BY_JUDGE":
        judge = p.get("judge_name") or p.get("judge")
        if not judge: return "Please specify judge_name."
        cur.execute("""
            SELECT s.id, s.sem_date, s.subject, s.judge,
                   s.start_time, s.end_time
            FROM seminars s
            WHERE s.judge LIKE CONCAT('%%', %s, '%%') AND s.status = 1
            ORDER BY s.sem_date DESC
            LIMIT 50
        """, (judge,))
        rows = cur.fetchall()
        if not rows: return f"No seminars found with judge '{judge}'."
        lines = [f"- {r['subject']} ({r['sem_date']}), Judge: {r['judge']}" for r in rows]
        return f"Seminars by Judge:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_TOPIC_LIST":
        cur.execute("""
            SELECT st.id, st.sub_topic, st.office_id, st.status, st.created_at
            FROM seminars_topic st
            WHERE st.status = 1 AND st.office_id = %s
            ORDER BY st.sub_topic
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No seminar topics found."
        lines = [f"- {r['sub_topic']}" for r in rows]
        return "Seminar Topics:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_DURATION":
        cur.execute("""
            SELECT s.id, s.sem_date, s.subject,
                   s.start_time, s.end_time,
                   TIMEDIFF(s.end_time, s.start_time) AS duration
            FROM seminars s
            WHERE s.status = 1
            ORDER BY s.sem_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No seminar duration data found."
        lines = [f"- {r['subject']} ({r['sem_date']}): {r['duration']} hours" for r in rows]
        return "Seminar Durations:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_BY_TYPE":
        cur.execute("""
            SELECT s.type_id, COUNT(s.id) AS count
            FROM seminars s
            WHERE s.status = 1
            GROUP BY s.type_id
            ORDER BY count DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No seminar types found."
        lines = [f"- Type {r['type_id']}: {r['count']} Seminars" for r in rows]
        return "Seminars by Type:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_BY_VL":
        cur.execute("""
            SELECT s.id, s.sem_date, s.subject, vm.subject_name AS vl_subject,
                   u.name AS vl_name
            FROM seminars s
            JOIN vl_management vm ON vm.id = s.vl_id
            JOIN users u ON u.id = vm.vl_id
            WHERE s.vl_id > 0 AND s.status = 1 AND u.office_id = %s
            ORDER BY s.sem_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No VL seminars found."
        lines = [f"- {r['subject']} ({r['sem_date']}) - VL: {r['vl_name']} ({r['vl_subject']})" for r in rows]
        return "Seminars by Visiting Lecturers:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_MONTHLY_COUNT":
        cur.execute("""
            SELECT YEAR(s.sem_date) AS yr, MONTH(s.sem_date) AS mo,
                   MONTHNAME(s.sem_date) AS month_name,
                   COUNT(s.id) AS seminar_count
            FROM seminars s
            WHERE s.status = 1
            GROUP BY YEAR(s.sem_date), MONTH(s.sem_date), MONTHNAME(s.sem_date)
            ORDER BY yr DESC, mo DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No monthly seminar data found."
        lines = [f"- {r['month_name']} {r['yr']}: {r['seminar_count']} Seminars" for r in rows]
        return "Monthly Seminar Count:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_ATTENDANCE":
        cur.execute("""
            SELECT s.id, s.sem_date, s.subject, s.topic_des
            FROM seminars s
            WHERE s.status = 1
            ORDER BY s.sem_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No seminar attendance data found."
        lines = [f"- {r['subject']} ({r['sem_date']}): {r['topic_des']}" for r in rows]
        return "Seminar Attendance/Topic Desc:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_REMARKS":
        cur.execute("""
            SELECT s.id, s.sem_date, s.subject, s.topic_remarks, s.remarks_forward
            FROM seminars s
            WHERE s.topic_remarks IS NOT NULL AND s.status = 1
            ORDER BY s.sem_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No seminar remarks found."
        lines = [f"- {r['subject']} ({r['sem_date']}): {r['topic_remarks']}" for r in rows]
        return "Seminar Remarks:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_STATUS_SUMMARY":
        cur.execute("""
            SELECT s.se_status,
                   CASE s.se_status
                     WHEN 0 THEN 'Draft'
                     WHEN 1 THEN 'Pending'
                     WHEN 2 THEN 'Forwarded'
                     WHEN 3 THEN 'Approved'
                   END AS status_label,
                   COUNT(s.id) AS count
            FROM seminars s
            WHERE s.status = 1
            GROUP BY s.se_status
        """)
        rows = cur.fetchall()
        if not rows: return "No seminar status summary found."
        lines = [f"- {r['status_label']}: {r['count']} Seminars" for r in rows]
        return "Seminar Status Summary:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_SUBJECT_SUMMARY":
        cur.execute("""
            SELECT s.subject, COUNT(s.id) AS seminar_count
            FROM seminars s
            WHERE s.status = 1 AND s.subject IS NOT NULL
            GROUP BY s.subject
            ORDER BY seminar_count DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No subject summary found."
        lines = [f"- {r['subject']}: {r['seminar_count']} Seminars" for r in rows]
        return "Seminar Subject Summary:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_TOPIC_SUMMARY":
        cur.execute("""
            SELECT st.sub_topic,
                   COUNT(DISTINCT s.id) AS seminar_count
            FROM seminars_topic st
            LEFT JOIN seminars s ON FIND_IN_SET(st.id, s.topic_id) AND s.status = 1
            WHERE st.status = 1 AND st.office_id = %s
            GROUP BY st.id, st.sub_topic
            ORDER BY seminar_count DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No topic summary found."
        lines = [f"- {r['sub_topic']}: {r['seminar_count']} Seminars" for r in rows]
        return "Seminar Topic Summary:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_OFFICE_SUMMARY":
        cur.execute("""
            SELECT st.office_id, COUNT(st.id) AS topic_count
            FROM seminars_topic st
            WHERE st.status = 1 AND st.office_id = %s
            GROUP BY st.office_id
        """, (office_id,))
        r = cur.fetchone()
        if not r: return "No office summary found."
        return f"Seminar Office Summary: {r['topic_count']} topics for office {r['office_id']}"

    elif query_id == "SEMINAR_DATE_RANGE":
        fdate = p.get("from_date")
        tdate = p.get("to_date")
        if not fdate or not tdate: return "Please specify from_date and to_date."
        cur.execute("""
            SELECT s.id, s.sem_date, s.subject, s.start_time, s.end_time,
                   s.judge, s.main_speaker, s.se_status
            FROM seminars s
            WHERE s.sem_date BETWEEN %s AND %s AND s.status = 1
            ORDER BY s.sem_date
            LIMIT 50
        """, (fdate, tdate))
        rows = cur.fetchall()
        if not rows: return "No seminars found in date range."
        lines = [f"- {r['subject']} ({r['sem_date']}): Speaker {r['main_speaker']}" for r in rows]
        return f"Seminars from {fdate} to {tdate}:\n" + "\n".join(lines)

    elif query_id == "SEMINAR_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(id) FROM seminars WHERE status=1) AS total_seminars,
              (SELECT COUNT(id) FROM seminars WHERE sem_date >= CURDATE() AND status=1) AS upcoming,
              (SELECT COUNT(id) FROM seminars WHERE sem_date < CURDATE() AND status=1) AS completed,
              (SELECT COUNT(id) FROM seminars_topic WHERE status=1 AND office_id=%s) AS total_topics
        """, (office_id,))
        r = cur.fetchone()
        if not r: return "Could not generate seminar module summary."
        return (f"Seminar Module Summary:\n"
                f"Total Seminars: {r['total_seminars']}\n"
                f"Upcoming Seminars: {r['upcoming']}\n"
                f"Completed Seminars: {r['completed']}\n"
                f"Total Topics: {r['total_topics']}")

    return None
