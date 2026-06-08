"""Exam, Re-exam, and Principal-level query handlers."""

TEMPLATES = [
    {
        "id": "TOTAL_EXAM_SCHEDULES",
        "module": "exam",
        "description": "total exam schedules overall (ONLY use if NO time period is mentioned)",
        "example_questions": [
            "Total exam schedules overall (only use if no time period is mentioned)?",
            "Show total exam schedules overall (ONLY use if NO time period is mentioned)"
        ],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "count",
        "security_level": "medium"
    },
    {
        "id": "TOTAL_SUBJECTS",
        "module": "exam",
        "description": "exam subjects / total subjects",
        "example_questions": [
            "Exam subjects?",
            "Show exam subjects"
        ],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "count",
        "security_level": "medium"
    },
    {
        "id": "EXAM_SCHEDULES_BY_TIME",
        "module": "exam",
        "description": "Get count AND list of exam schedules. Can filter by time period (e.g., in 2025, this year, between January and December, last 4 months)",
        "example_questions": [
            "Get count and list of exam schedules. can filter by time period (e.g., in 2025, this year, between january and december, last 4 months).?",
            "Show Get count AND list of exam schedules. Can filter by time period (e.g., in 2025, this year, between January and December, last 4 months)."
        ],
        "required_params": [],
        "optional_params": [
            "limit",
            "offset",
            "year",
            "month",
            "start_month",
            "end_month",
            "last_months",
            "last_years"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "count",
        "security_level": "medium"
    },
    {
        "id": "UPCOMING_EXAMS",
        "module": "exam",
        "description": "upcoming exams",
        "example_questions": [
            "Upcoming exams?",
            "Show upcoming exams"
        ],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "COMPLETED_EXAMS",
        "module": "exam",
        "description": "completed exams",
        "example_questions": [
            "Completed exams?",
            "Show completed exams"
        ],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "TOTAL_MARKS_RECORDS",
        "module": "exam",
        "description": "Total marks records",
        "example_questions": [
            "Total marks records?",
            "Show Total marks records"
        ],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "count",
        "security_level": "medium"
    },
    {
        "id": "MARKS_OF_ONE_TRAINEE",
        "module": "exam",
        "description": "marks of trainee / Marks of one trainee by name or ID",
        "example_questions": [
            "Marks of trainee?",
            "Show marks of trainee",
            "marks of mayank",
            "get marks for trainee John"
        ],
        "required_params": [],
        "optional_params": [
            "trainee_id",
            "search_name",
            "name",
            "user_code"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "MARKS_OF_TRAINEE_IN_ONE_EXAM",
        "module": "exam",
        "description": "Marks of trainee in one exam",
        "example_questions": [
            "Marks of trainee in one exam.?",
            "Show Marks of trainee in one exam."
        ],
        "required_params": [],
        "optional_params": [
            "trainee_id",
            "exam_schedule_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "SUBJECT_WISE_AVERAGE_MARKS",
        "module": "exam",
        "description": "Subject-wise average marks",
        "example_questions": [
            "Subject-wise average marks?",
            "Show Subject-wise average marks"
        ],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "EXAM_TOP_PERFORMERS",
        "module": "exam",
        "description": "Top performers / highest marks.",
        "example_questions": [
            "Who got highest marks?",
            "Show top 5 performers",
            "Top trainees in exam"
        ],
        "required_params": [],
        "optional_params": [
            "office_id",
            "course_name",
            "exam_name",
            "course_id",
            "limit"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "ranking",
        "security_level": "medium"
    },
    {
        "id": "LOWEST_PERFORMERS",
        "module": "exam",
        "description": "lowest students / Lowest performers / lowest marks / bottom trainees",
        "example_questions": [
            "Lowest students?",
            "Show lowest students",
            "bottom 5 trainees",
            "bottom performers"
        ],
        "required_params": [],
        "optional_params": [
            "course_name",
            "Cabinman",
            "course_id",
            "limit"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "ranking",
        "security_level": "medium"
    },
    {
        "id": "FAILED_TRAINEES",
        "module": "exam",
        "description": "failed students / Failed trainees in exam",
        "example_questions": [
            "Failed students?",
            "Show failed students",
            "Who failed in cabinman"
        ],
        "required_params": [],
        "optional_params": [
            "course_name",
            "course_id",
            "passing_marks"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "PASSED_TRAINEES",
        "module": "exam",
        "description": "passed students / Passed trainees in exam / who passed",
        "example_questions": [
            "Passed students?",
            "Show passed students",
            "Who passed the exam",
            "List passed trainees"
        ],
        "required_params": [],
        "optional_params": [
            "course_name",
            "course_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "FAILED_TRAINEES_COUNT",
        "module": "exam",
        "description": "Failed trainees count",
        "example_questions": [
            "Failed trainees count.?",
            "Show Failed trainees count."
        ],
        "required_params": [],
        "optional_params": [
            "passing_marks",
            "exam_schedule_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "count",
        "security_level": "medium"
    },
    {
        "id": "PASS_FAIL_SUMMARY",
        "module": "exam",
        "description": "Pass / fail summary",
        "example_questions": [
            "Pass?",
            "Show Pass"
        ],
        "required_params": [],
        "optional_params": [
            "exam_schedule_id",
            "passing_marks"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "PASS_PERCENTAGE",
        "module": "exam",
        "description": "pass percentage",
        "example_questions": [
            "Pass percentage.?",
            "Show pass percentage."
        ],
        "required_params": [],
        "optional_params": [
            "exam_schedule_id",
            "passing_marks"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "TOTAL_RE_EXAM_TRAINEES",
        "module": "exam",
        "description": "Total re-exam trainees",
        "example_questions": [
            "Total re-exam trainees?",
            "Show Total re-exam trainees"
        ],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "count",
        "security_level": "medium"
    },
    {
        "id": "RE_EXAM_TRAINEE_LIST",
        "module": "exam",
        "description": "re-exam students / Re-exam trainee list",
        "example_questions": [
            "Re-exam students?",
            "Show re-exam students"
        ],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "RE_EXAM_COUNT_BY_EXAM",
        "module": "exam",
        "description": "Re-exam count by exam",
        "example_questions": [
            "Re-exam count by exam?",
            "Show Re-exam count by exam"
        ],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "count",
        "security_level": "medium"
    },
    {
        "id": "TRAINEE_COMPLETE_EXAM_REPORT",
        "module": "exam",
        "description": "Trainee complete exam report",
        "example_questions": [
            "Trainee complete exam report.?",
            "Show Trainee complete exam report."
        ],
        "required_params": [],
        "optional_params": [
            "trainee_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "details",
        "security_level": "medium"
    },
    {
        "id": "TRAINEES_WITH_NO_MARKS",
        "module": "exam",
        "description": "Trainees with no marks",
        "example_questions": [
            "Trainees with no marks?",
            "Show Trainees with no marks"
        ],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "AVERAGE_MARKS_BY_TRAINEE",
        "module": "exam",
        "description": "Average marks by trainee",
        "example_questions": [
            "Average marks by trainee?",
            "Show Average marks by trainee"
        ],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "WEAK_TRAINEES",
        "module": "exam",
        "description": "weak trainees / Weak trainees",
        "example_questions": [
            "Weak trainees?",
            "Show weak trainees"
        ],
        "required_params": [],
        "optional_params": [
            "threshold_marks"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "ACTIVE_EXAM_TYPES",
        "module": "exam",
        "description": "List all active exam types / total exam types / how many exam types / total exam type",
        "example_questions": [
            "List all active exam types?",
            "Show List all active exam types"
        ],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "count",
        "security_level": "medium"
    },
    {
        "id": "EXAM_TYPE_DETAILS_BY_ID",
        "module": "exam",
        "description": "Get exam type details by ID",
        "example_questions": [
            "Get exam type details by id.?",
            "Show Get exam type details by ID."
        ],
        "required_params": [],
        "optional_params": [
            "exam_type_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "details",
        "security_level": "medium"
    },
    {
        "id": "ALL_MARKS_FOR_TRAINEE",
        "module": "exam",
        "description": "Get all marks for a trainee",
        "example_questions": [
            "Get all marks for a trainee.?",
            "Show Get all marks for a trainee."
        ],
        "required_params": [],
        "optional_params": [
            "user_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "ALL_MARKS_FOR_COURSE",
        "module": "exam",
        "description": "Get all marks for a specific course",
        "example_questions": [
            "Get all marks for a specific course.?",
            "Show Get all marks for a specific course."
        ],
        "required_params": [],
        "optional_params": [
            "course_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "MARKS_FOR_TRAINEE_IN_COURSE",
        "module": "exam",
        "description": "Get marks for a trainee in a specific course",
        "example_questions": [
            "Get marks for a trainee in a specific course.?",
            "Show Get marks for a trainee in a specific course."
        ],
        "required_params": [],
        "optional_params": [
            "user_id",
            "course_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "MARKS_BY_EXAM_TYPE_FOR_COURSE",
        "module": "exam",
        "description": "Marks by exam type for a course",
        "example_questions": [
            "Marks by exam type for a course.?",
            "Show Marks by exam type for a course."
        ],
        "required_params": [],
        "optional_params": [
            "course_id",
            "exam_type_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "SUBJECT_WISE_MARKS_FOR_TRAINEE_IN_COURSE",
        "module": "exam",
        "description": "Subject-wise marks for a trainee in a course",
        "example_questions": [
            "Subject-wise marks for a trainee in a course.?",
            "Show Subject-wise marks for a trainee in a course."
        ],
        "required_params": [],
        "optional_params": [
            "user_id",
            "course_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "HIGHEST_SCORERS_IN_COURSE",
        "module": "exam",
        "description": "Highest scorers in a course",
        "example_questions": [
            "Highest scorers in a course.?",
            "Show Highest scorers in a course."
        ],
        "required_params": [],
        "optional_params": [
            "course_name",
            "course_id",
            "exam_type_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "ranking",
        "security_level": "medium"
    },
    {
        "id": "PASS_FAIL_SUMMARY_FOR_COURSE",
        "module": "exam",
        "description": "Pass/fail summary for a course",
        "example_questions": [
            "Pass?",
            "Show Pass"
        ],
        "required_params": [],
        "optional_params": [
            "course_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "ALL_FAILED_TRAINEES_IN_COURSE",
        "module": "exam",
        "description": "All failed trainees in a course",
        "example_questions": [
            "All failed trainees in a course.?",
            "Show All failed trainees in a course."
        ],
        "required_params": [],
        "optional_params": [
            "course_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "DID_TRAINEE_PASS_IN_COURSE",
        "module": "exam",
        "description": "Did a specific trainee pass in a course?",
        "example_questions": [
            "Did a specific trainee pass in a course??",
            "Show Did a specific trainee pass in a course?"
        ],
        "required_params": [],
        "optional_params": [
            "user_id",
            "course_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "OVERALL_PASS_FAIL_COUNT",
        "module": "exam",
        "description": "Overall pass/fail count across all courses",
        "example_questions": [
            "Overall pass?",
            "Show Overall pass"
        ],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "count",
        "security_level": "medium"
    },
    {
        "id": "TRAINEES_APPEARED_IN_RE_EXAM",
        "module": "exam",
        "description": "Trainees who appeared in re-exam",
        "example_questions": [
            "Trainees who appeared in re-exam.?",
            "Show Trainees who appeared in re-exam."
        ],
        "required_params": [],
        "optional_params": [
            "course_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "TRAINEES_FAILED_AFTER_RE_EXAM",
        "module": "exam",
        "description": "Trainees who failed even after re-exam",
        "example_questions": [
            "Trainees who failed even after re-exam.?",
            "Show Trainees who failed even after re-exam."
        ],
        "required_params": [],
        "optional_params": [
            "course_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "EXAM_DESIGN_FOR_COURSE",
        "module": "exam",
        "description": "Exam design for a course",
        "example_questions": [
            "Exam design for a course.?",
            "Show Exam design for a course."
        ],
        "required_params": [],
        "optional_params": [
            "office_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "MIN_PASS_MARKS_PER_EXAM_TYPE",
        "module": "exam",
        "description": "Minimum passing marks per exam type",
        "example_questions": [
            "Minimum passing marks per exam type.?",
            "Show Minimum passing marks per exam type."
        ],
        "required_params": [],
        "optional_params": [
            "office_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "FEEDBACK_SUBMISSIONS_FOR_COURSE",
        "module": "exam",
        "description": "Feedback submissions for a course",
        "example_questions": [
            "Feedback submissions for a course.?",
            "Show Feedback submissions for a course."
        ],
        "required_params": [],
        "optional_params": [
            "course_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "FEEDBACK_SUBMITTED_COUNT_FOR_COURSE",
        "module": "exam",
        "description": "How many trainees submitted feedback for a course?",
        "example_questions": [
            "How many trainees submitted feedback for a course??",
            "Show How many trainees submitted feedback for a course?"
        ],
        "required_params": [],
        "optional_params": [
            "course_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "FEEDBACK_RESPONSES_FOR_QUESTION",
        "module": "exam",
        "description": "Feedback responses for a question",
        "example_questions": [
            "Feedback responses for a question.?",
            "Show Feedback responses for a question."
        ],
        "required_params": [],
        "optional_params": [
            "fq_id",
            "course_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "LIST_ALL_FEEDBACK_QUESTIONS",
        "module": "exam",
        "description": "List all feedback questions",
        "example_questions": [
            "List all feedback questions.?",
            "Show List all feedback questions."
        ],
        "required_params": [],
        "optional_params": [
            "office_id"
        ],
        "allowed_roles": [
            "principal",
            "admin",
            "exam_admin"
        ],
        "result_type": "list",
        "security_level": "medium"
    }
]

def execute(query_id, params, cur, office_id):
    p = params or {}
    print(f"[exam_queries] Executing query_id={query_id}, params={p}, office_id={office_id}")
    
    GENERIC_WORDS = {
        "exam", "exams", "course", "courses", "marks", "mark", "performers",
        "performer", "top", "highest", "lowest", "best", "worst", "recent",
        "latest", "schedule", "schedules", "trainee", "trainees", "student",
        "students", "result", "results", "score", "scores", "all", "total",
        "overall", "general", "any", "the", "in", "for", "of", "a", "an",
        "most", "current", "currently", "completed", "active", "test", "tests",
        "session", "sessions", "term", "terms", "held", "conducted", "last",
        "first", "new", "newest", "old", "oldest", "year", "years", "month",
        "months", "day", "days"
    }
    
    def _clean_course_name(name):
        """Return None if the name is just generic words, otherwise return the cleaned name."""
        if not name:
            return None
        import re
        cleaned = re.sub(r'[?.!,]', '', name.strip().lower())
        # If the entire name consists of only generic/blocked words, discard it
        words = set(cleaned.split())
        if not words or words.issubset(GENERIC_WORDS):
            return None
        return name.strip()
    
    # 3. Exam Master Queries
    if query_id == "TOTAL_EXAM_SCHEDULES":
        cur.execute("SELECT COUNT(*) AS total FROM et_design ed JOIN training_calendars tc ON tc.id = ed.course_id JOIN courses c ON c.id = tc.ct_id WHERE tc.office_id = %s", (office_id,))
        r = cur.fetchone()
        return f"Total exam schedules: {r['total'] if r else 0}"
        
    elif query_id == "TOTAL_SUBJECTS":
        cur.execute("SELECT COUNT(DISTINCT subject) AS total_subjects FROM et_design ed JOIN training_calendars tc ON tc.id = ed.course_id JOIN courses c ON c.id = tc.ct_id WHERE tc.office_id = %s", (office_id,))
        r = cur.fetchone()
        return f"Total subjects: {r['total_subjects'] if r else 0}"
        
    elif query_id == "EXAM_SCHEDULES_BY_TIME":
        limit = int(p.get("limit", 20))
        offset = int(p.get("offset", 0))
        
        last_months = p.get("last_months")
        last_years = p.get("last_years")
        year = p.get("year")
        month = p.get("month")
        start_month = p.get("start_month")
        end_month = p.get("end_month")
        
        base_query = "FROM et_design ed JOIN training_calendars tc ON tc.id = ed.course_id JOIN courses c ON c.id = tc.ct_id WHERE tc.office_id = %s AND ed.status = 1"
        params_db = [office_id]
        time_str_parts = []
        
        if last_months is not None:
            base_query += " AND ed.exam_date >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)"
            params_db.append(int(last_months))
            time_str_parts.append(f"in the last {last_months} months")
        elif last_years is not None:
            import datetime
            target_year = datetime.datetime.now().year - int(last_years)
            base_query += " AND YEAR(ed.exam_date) = %s"
            params_db.append(target_year)
            time_str_parts.append(f"in the last {last_years} year(s) ({target_year})")
        elif start_month and end_month:
            base_query += " AND MONTH(ed.exam_date) BETWEEN %s AND %s"
            params_db.extend([int(start_month), int(end_month)])
            time_str_parts.append(f"between month {start_month} and {end_month}")
            if year:
                base_query += " AND YEAR(ed.exam_date) = %s"
                params_db.append(int(year))
                time_str_parts.append(f"of {year}")
        else:
            if year:
                base_query += " AND YEAR(ed.exam_date) = %s"
                params_db.append(int(year))
                time_str_parts.append(f"in {year}")
            if month:
                base_query += " AND MONTH(ed.exam_date) = %s"
                params_db.append(int(month))
                import datetime
                try:
                    month_name = datetime.date(1900, int(month), 1).strftime('%B')
                    time_str_parts.append(f"month {month_name}")
                except:
                    time_str_parts.append(f"month {month}")
                
        time_str = " ".join(time_str_parts) if time_str_parts else "overall"

        count_query = f"SELECT COUNT(*) AS total {base_query}"
        cur.execute(count_query, tuple(params_db))
        r = cur.fetchone()
        total_count = r['total'] if r else 0
        
        if total_count == 0:
            return f"No exam schedules found {time_str}."

        list_query = f"SELECT ed.*, c.course_name {base_query} ORDER BY ed.exam_date DESC LIMIT %s OFFSET %s"
        params_db.extend([limit, offset])
        cur.execute(list_query, tuple(params_db))
        rows = cur.fetchall()
        
        lines = [f"- {row.get('subject')} ({row.get('course_name')}): Date {row.get('exam_date')}" for row in rows]
        
        return f"Total exam schedules {time_str}: {total_count}\n\nList (showing up to {limit}):\n" + "\n".join(lines)
        
    elif query_id == "UPCOMING_EXAMS":
        cur.execute("SELECT ed.*, c.course_name FROM et_design ed JOIN training_calendars tc ON tc.id = ed.course_id JOIN courses c ON c.id = tc.ct_id WHERE tc.office_id = %s AND ed.exam_date >= CURDATE() ORDER BY ed.exam_date ASC", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No upcoming exams found."
        lines = [f"- {r.get('subject')} ({r.get('course_name')}): Date {r.get('exam_date')}" for r in rows]
        return "Upcoming Exams:\n" + "\n".join(lines)
        
    elif query_id == "COMPLETED_EXAMS":
        cur.execute("SELECT ed.*, c.course_name FROM et_design ed JOIN training_calendars tc ON tc.id = ed.course_id JOIN courses c ON c.id = tc.ct_id WHERE tc.office_id = %s AND ed.exam_date < CURDATE() ORDER BY ed.exam_date DESC", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No completed exams found."
        lines = [f"- {r.get('subject')} ({r.get('course_name')}): Date {r.get('exam_date')}" for r in rows]
        return "Completed Exams:\n" + "\n".join(lines)
        
    # 4. Exam Marks Queries
    elif query_id == "TOTAL_MARKS_RECORDS":
        cur.execute("SELECT COUNT(*) AS total FROM exam_marks em JOIN training_calendars tc ON tc.id = em.course_id JOIN courses c ON c.id = tc.ct_id WHERE tc.office_id = %s", (office_id,))
        r = cur.fetchone()
        return f"Total marks records: {r['total'] if r else 0}"
        
    elif query_id == "MARKS_OF_ONE_TRAINEE":
        uid = p.get("trainee_id") or p.get("user_id")
        name = p.get("search_name") or p.get("name")
        user_code = p.get("user_code")
        
        # If user_code provided, lookup the user ID first
        if user_code:
            cur.execute("SELECT id FROM users WHERE user_code = %s AND office_id = %s", (user_code.upper(), office_id))
            row = cur.fetchone()
            if row:
                uid = row['id']
            else:
                return f"No trainee found with code '{user_code}' in your office."
        
        if not uid and not name: return "Please specify a trainee_id, user_id, name, or user_code."
        
        # Clean up name (remove quotes, extra spaces)
        if name:
            import re
            name = re.sub(r'[^a-zA-Z0-9\s]', '', name).strip()
        
        # If no trainee_id, first search for matching users by name
        if not uid:
            cur.execute(
                "SELECT id, name, user_code FROM users WHERE LOWER(name) LIKE LOWER(%s) AND office_id = %s AND EXISTS (SELECT 1 FROM exam_marks em WHERE em.user_id = users.id) LIMIT 20",
                (f"%{name}%", office_id)
            )
            matches = cur.fetchall()
            import logging
            logging.info(f"[MARKS_OF_ONE_TRAINEE] Searching for name='{name}', office_id={office_id}, found {len(matches)} matches: {matches}")
            if not matches:
                return f"No trainee found with name '{name}' in your office."
            if len(matches) == 1:
                uid = matches[0]['id']
            else:
                # Multiple matches — return list for user to pick
                lines = [f"- {m['name']} (Code: {m.get('user_code', 'N/A')})" for m in matches]
                return f"TRAINEE_SELECT\nMultiple trainees found matching '{name}'. Please select one:\n" + "\n".join(lines)
        
        # Fetch marks for the specific trainee using exam_marks
        cur.execute("""
            SELECT s.subject_name, em.mark_obtained, s.total_mark, c.course_name, u.name AS trainee_name, u.user_code
            FROM exam_marks em
            JOIN subjects s ON s.id = em.subject_id
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id
            JOIN users u ON u.id = em.user_id
            WHERE em.user_id = %s AND tc.office_id = %s
            ORDER BY em.id DESC
        """, (uid, office_id))
        rows = cur.fetchall()
        if not rows:
            # Get the trainee name and code even if no marks
            cur.execute("SELECT name, user_code FROM users WHERE id = %s", (uid,))
            user_row = cur.fetchone()
            trainee_display = user_row['name'] if user_row else uid
            user_code_display = user_row['user_code'] if user_row and user_row['user_code'] else 'N/A'
            return f"{trainee_display} (Code: {user_code_display}) has not appeared in any exam yet."
        
        trainee_display = rows[0]['trainee_name']
        user_code_display = rows[0]['user_code'] if rows[0].get('user_code') else 'N/A'
        
        # Build card-based layout for better display in narrow chat
        cards = []
        for r in rows:
            mark = r['mark_obtained'] if r['mark_obtained'] is not None else 'N/A'
            cards.append(f"""
<div style="background: #2d3748; border-radius: 8px; padding: 12px; margin: 8px 0; color: white;">
    <div style="font-weight: bold; font-size: 15px; margin-bottom: 6px;">{r['subject_name']}</div>
    <div style="font-size: 13px; color: #a0aec0; margin-bottom: 4px;">{r['course_name']}</div>
    <div style="font-size: 16px; font-weight: bold; color: #68d391;">{mark}/{r['total_mark']}</div>
</div>""")
        
        result_html = f"""<b>Marks for {trainee_display} (Code: {user_code_display}):</b><br>
{''.join(cards)}"""
        return result_html
        
    elif query_id == "MARKS_OF_TRAINEE_IN_ONE_EXAM":
        uid = p.get("trainee_id") or p.get("user_id")
        cid = p.get("course_id") or p.get("exam_schedule_id")
        if not uid or not cid: return "Please specify trainee_id and course_id."
        cur.execute("""
            SELECT s.subject_name, em.mark_obtained, s.total_mark
            FROM exam_marks em
            JOIN subjects s ON s.id = em.subject_id
            JOIN training_calendars tc ON tc.id = em.course_id
            WHERE em.user_id = %s AND em.course_id = %s AND tc.office_id = %s
        """, (uid, cid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No marks found for trainee {uid} in course {cid}."
        lines = [f"- {r['subject_name']}: {r['mark_obtained']}/{r['total_mark']}" for r in rows]
        return f"Marks for Trainee {uid} in Course {cid}:\n" + "\n".join(lines)
        
    elif query_id == "SUBJECT_WISE_AVERAGE_MARKS":
        cur.execute("""
            SELECT s.subject_name, AVG(em.mark_obtained) AS avg_marks, AVG(s.total_mark) AS total_mark
            FROM exam_marks em
            JOIN subjects s ON s.id = em.subject_id
            JOIN training_calendars tc ON tc.id = em.course_id
            WHERE tc.office_id = %s
            GROUP BY s.id
            ORDER BY avg_marks DESC
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No average marks data found."
        lines = [f"- {r['subject_name']}: Avg {round(r['avg_marks'], 2)} / {r['total_mark']}" for r in rows]
        return "Subject-wise Average Marks:\n" + "\n".join(lines)
        
    elif query_id == "EXAM_TOP_PERFORMERS":
        cid = p.get("course_id")
        course_name = _clean_course_name(p.get("course_name") or p.get("exam_name"))
        limit = int(p.get("limit", 10))
        
        # Resolve course_name to course_id if name is provided
        if not cid and course_name:
            cur.execute(
                """SELECT tc.id, tc.course_batch FROM training_calendars tc 
                   JOIN courses c ON c.id = tc.ct_id 
                   WHERE LOWER(c.course_name) LIKE LOWER(%s) AND tc.office_id = %s 
                   AND EXISTS (SELECT 1 FROM exam_marks em WHERE em.course_id = tc.id)
                   ORDER BY tc.from_date DESC LIMIT 1""",
                (f"%{course_name}%", office_id)
            )
            match = cur.fetchone()
            if match:
                cid = match['id']
            else:
                return f"No exam marks data found for any '{course_name}' course."
        
        if not cid:
            cur.execute(
                """SELECT tc.id FROM training_calendars tc 
                   WHERE tc.office_id = %s 
                   AND EXISTS (SELECT 1 FROM exam_marks em WHERE em.course_id = tc.id)
                   ORDER BY tc.from_date DESC LIMIT 1""", 
                (office_id,)
            )
            row = cur.fetchone()
            if not row: return "No exam marks data available yet."
            cid = row['id']
        cur.execute("""
            SELECT u.name, SUM(em.mark_obtained) AS total_marks, SUM(s.total_mark) AS max_marks, c.course_name, tc.course_batch
            FROM exam_marks em
            JOIN users u ON u.id = em.user_id
            JOIN subjects s ON s.id = em.subject_id
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE em.course_id = %s AND tc.office_id = %s
            GROUP BY em.user_id, c.course_name, tc.course_batch
            ORDER BY total_marks DESC
            LIMIT %s
        """, (cid, office_id, limit))
        rows = cur.fetchall()
        if not rows: return f"No performers found for course {cid}."
        
        display_name = f"{rows[0]['course_name']} ({rows[0]['course_batch']})"
        lines = [f"- {r['name']}: {r['total_marks']}/{r['max_marks']}" for r in rows]
        return f"Top Performers in {display_name}:\n" + "\n".join(lines)
        
    elif query_id == "LOWEST_PERFORMERS":
        cid = p.get("course_id")
        course_name = _clean_course_name(p.get("course_name") or p.get("exam_name"))
        limit = int(p.get("limit", 10))
        
        # Resolve course_name to course_id if name is provided
        if not cid and course_name:
            cur.execute(
                """SELECT tc.id, tc.course_batch FROM training_calendars tc 
                   JOIN courses c ON c.id = tc.ct_id 
                   WHERE LOWER(c.course_name) LIKE LOWER(%s) AND tc.office_id = %s 
                   AND EXISTS (SELECT 1 FROM exam_marks em WHERE em.course_id = tc.id)
                   ORDER BY tc.from_date DESC LIMIT 1""",
                (f"%{course_name}%", office_id)
            )
            match = cur.fetchone()
            if match:
                cid = match['id']
            else:
                return f"No exam marks data found for any '{course_name}' course."
        
        if not cid:
            cur.execute(
                """SELECT tc.id FROM training_calendars tc 
                   WHERE tc.office_id = %s 
                   AND EXISTS (SELECT 1 FROM exam_marks em WHERE em.course_id = tc.id)
                   ORDER BY tc.from_date DESC LIMIT 1""", 
                (office_id,)
            )
            row = cur.fetchone()
            if not row: return "No exam marks data available yet."
            cid = row['id']
        cur.execute("""
            SELECT u.name, SUM(em.mark_obtained) AS total_marks, SUM(s.total_mark) AS max_marks, c.course_name, tc.course_batch
            FROM exam_marks em
            JOIN users u ON u.id = em.user_id
            JOIN subjects s ON s.id = em.subject_id
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE em.course_id = %s AND tc.office_id = %s
            GROUP BY em.user_id, c.course_name, tc.course_batch
            ORDER BY total_marks ASC
            LIMIT %s
        """, (cid, office_id, limit))
        rows = cur.fetchall()
        if not rows: return f"No lowest performers found for course {cid}."
        
        display_name = f"{rows[0]['course_name']} ({rows[0]['course_batch']})"
        lines = [f"- {r['name']}: {r['total_marks']}/{r['max_marks']}" for r in rows]
        return f"Lowest Performers in {display_name}:\n" + "\n".join(lines)
        
    elif query_id == "FAILED_TRAINEES":
        cid = p.get("course_id")
        course_name = _clean_course_name(p.get("course_name") or p.get("exam_name"))
        
        # Resolve course_name to course_id if name is provided
        if not cid and course_name:
            cur.execute(
                """SELECT tc.id, tc.course_batch FROM training_calendars tc 
                   JOIN courses c ON c.id = tc.ct_id 
                   WHERE LOWER(c.course_name) LIKE LOWER(%s) AND tc.office_id = %s 
                   AND EXISTS (SELECT 1 FROM exam_marks em WHERE em.course_id = tc.id)
                   ORDER BY tc.from_date DESC LIMIT 1""",
                (f"%{course_name}%", office_id)
            )
            match = cur.fetchone()
            if match:
                cid = match['id']
            else:
                return f"No exam marks data found for any '{course_name}' course."
        
        if not cid:
            cur.execute("SELECT id FROM training_calendars WHERE office_id = %s ORDER BY id DESC LIMIT 1", (office_id,))
            row = cur.fetchone()
            if not row: return "No courses available."
            cid = row['id']
        cur.execute("""
            SELECT u.name, u.user_code, s.subject_name, em.mark_obtained, s.total_mark, c.course_name, tc.course_batch
            FROM exam_marks em
            JOIN users u ON u.id = em.user_id
            JOIN subjects s ON s.id = em.subject_id
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE em.course_id = %s AND em.result = 2 AND tc.office_id = %s
            ORDER BY em.mark_obtained ASC
        """, (cid, office_id))
        rows = cur.fetchall()
        if not rows: 
            # Get course name for message
            cur.execute("SELECT c.course_name, tc.course_batch FROM training_calendars tc JOIN courses c ON c.id = tc.ct_id WHERE tc.id = %s", (cid,))
            cname_row = cur.fetchone()
            cname = f"{cname_row['course_name']} ({cname_row['course_batch']})" if cname_row else f"Course {cid}"
            return f"No failed trainees in {cname}."
        display_name = f"{rows[0]['course_name']} ({rows[0]['course_batch']})"
        lines = [f"- {r['name']} (Code: {r['user_code']}): {r['subject_name']} - {r['mark_obtained']}/{r['total_mark']}" for r in rows[:50]]
        return f"Failed Trainees in {display_name} (result=2, showing up to 50):\n" + "\n".join(lines)
        
    elif query_id == "PASSED_TRAINEES":
        cid = p.get("course_id")
        course_name = _clean_course_name(p.get("course_name") or p.get("exam_name"))
        
        # Resolve course_name to course_id if name is provided
        if not cid and course_name:
            cur.execute(
                """SELECT tc.id, tc.course_batch FROM training_calendars tc 
                   JOIN courses c ON c.id = tc.ct_id 
                   WHERE LOWER(c.course_name) LIKE LOWER(%s) AND tc.office_id = %s 
                   AND EXISTS (SELECT 1 FROM exam_marks em WHERE em.course_id = tc.id)
                   ORDER BY tc.from_date DESC LIMIT 1""",
                (f"%{course_name}%", office_id)
            )
            match = cur.fetchone()
            if match:
                cid = match['id']
            else:
                return f"No exam marks data found for any '{course_name}' course."
        
        if not cid:
            cur.execute("SELECT id FROM training_calendars WHERE office_id = %s ORDER BY id DESC LIMIT 1", (office_id,))
            row = cur.fetchone()
            if not row: return "No courses available."
            cid = row['id']
        cur.execute("""
            SELECT u.name, u.user_code, s.subject_name, em.mark_obtained, s.total_mark, c.course_name, tc.course_batch
            FROM exam_marks em
            JOIN users u ON u.id = em.user_id
            JOIN subjects s ON s.id = em.subject_id
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE em.course_id = %s AND em.result = 1 AND tc.office_id = %s
            ORDER BY em.mark_obtained DESC
        """, (cid, office_id))
        rows = cur.fetchall()
        if not rows: 
            cur.execute("SELECT c.course_name, tc.course_batch FROM training_calendars tc JOIN courses c ON c.id = tc.ct_id WHERE tc.id = %s", (cid,))
            cname_row = cur.fetchone()
            cname = f"{cname_row['course_name']} ({cname_row['course_batch']})" if cname_row else f"Course {cid}"
            return f"No passed trainees in {cname}."
        display_name = f"{rows[0]['course_name']} ({rows[0]['course_batch']})"
        lines = [f"- {r['name']} (Code: {r['user_code']}): {r['subject_name']} - {r['mark_obtained']}/{r['total_mark']}" for r in rows[:50]]
        return f"Passed Trainees in {display_name} (result=1, showing up to 50):\n" + "\n".join(lines)
        
    elif query_id == "FAILED_TRAINEES_COUNT":
        cid = p.get("course_id")
        course_name = _clean_course_name(p.get("course_name") or p.get("exam_name"))
        
        # Resolve course_name to course_id if name is provided
        if not cid and course_name:
            cur.execute(
                """SELECT tc.id, tc.course_batch FROM training_calendars tc 
                   JOIN courses c ON c.id = tc.ct_id 
                   WHERE LOWER(c.course_name) LIKE LOWER(%s) AND tc.office_id = %s 
                   AND EXISTS (SELECT 1 FROM exam_marks em WHERE em.course_id = tc.id)
                   ORDER BY tc.from_date DESC LIMIT 1""",
                (f"%{course_name}%", office_id)
            )
            match = cur.fetchone()
            if match:
                cid = match['id']
            else:
                return f"No exam marks data found for any '{course_name}' course."
        
        if not cid:
            cur.execute("SELECT id FROM training_calendars WHERE office_id = %s ORDER BY id DESC LIMIT 1", (office_id,))
            row = cur.fetchone()
            if not row: return "No courses available."
            cid = row['id']
        cur.execute("""
            SELECT COUNT(DISTINCT em.user_id) AS failed_trainees, c.course_name, tc.course_batch
            FROM exam_marks em
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE em.course_id = %s AND em.result = 2 AND tc.office_id = %s
        """, (cid, office_id))
        r = cur.fetchone()
        display_name = f"{r['course_name']} ({r['course_batch']})" if r and r['course_name'] else f"Course {cid}"
        return f"Failed trainees count in {display_name} (result=2): {r['failed_trainees'] if r else 0}"
        
    elif query_id == "PASS_FAIL_SUMMARY":
        cid = p.get("course_id")
        course_name = _clean_course_name(p.get("course_name") or p.get("exam_name"))
        
        # Resolve course_name to course_id if name is provided
        if not cid and course_name:
            cur.execute(
                """SELECT tc.id, tc.course_batch FROM training_calendars tc 
                   JOIN courses c ON c.id = tc.ct_id 
                   WHERE LOWER(c.course_name) LIKE LOWER(%s) AND tc.office_id = %s 
                   AND EXISTS (SELECT 1 FROM exam_marks em WHERE em.course_id = tc.id)
                   ORDER BY tc.from_date DESC LIMIT 1""",
                (f"%{course_name}%", office_id)
            )
            match = cur.fetchone()
            if match:
                cid = match['id']
            else:
                return f"No exam marks data found for any '{course_name}' course."
        
        if not cid:
            cur.execute("SELECT id FROM training_calendars WHERE office_id = %s ORDER BY id DESC LIMIT 1", (office_id,))
            row = cur.fetchone()
            if not row: return "No courses available."
            cid = row['id']
        cur.execute("""
            SELECT 
                COUNT(DISTINCT CASE WHEN em.result = 1 THEN em.user_id END) AS passed,
                COUNT(DISTINCT CASE WHEN em.result = 2 THEN em.user_id END) AS failed,
                c.course_name, tc.course_batch
            FROM exam_marks em
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE em.course_id = %s AND tc.office_id = %s
        """, (cid, office_id))
        r = cur.fetchone()
        display_name = f"{r['course_name']} ({r['course_batch']})" if r and r['course_name'] else f"Course {cid}"
        return f"Pass / Fail Summary for {display_name}:\nPassed (result=1): {r['passed']}\nFailed (result=2): {r['failed']}"
        
    elif query_id == "PASS_PERCENTAGE":
        cid = p.get("course_id")
        pm = float(p.get("passing_marks", 40))
        if not cid:
            cur.execute("SELECT id FROM training_calendars WHERE office_id = %s ORDER BY id DESC LIMIT 1", (office_id,))
            row = cur.fetchone()
            if not row: return "No courses available."
            cid = row['id']
        cur.execute("""
            SELECT ROUND(COUNT(DISTINCT CASE WHEN em.mark_obtained >= %s THEN em.user_id END) * 100.0 / NULLIF(COUNT(DISTINCT em.user_id), 0), 2) AS pass_percentage
            FROM exam_marks em
            JOIN training_calendars tc ON tc.id = em.course_id
            WHERE em.course_id = %s AND tc.office_id = %s
        """, (pm, cid, office_id))
        r = cur.fetchone()
        return f"Pass Percentage for Course {cid}: {r['pass_percentage'] if r else 0}%"
        
    # 5. Re-exam Queries
    elif query_id == "TOTAL_RE_EXAM_TRAINEES":
        cur.execute("SELECT COUNT(*) AS total_re_exam_trainees FROM re_exam_trainee WHERE office_id = %s", (office_id,))
        r = cur.fetchone()
        return f"Total re-exam trainees: {r['total_re_exam_trainees'] if r else 0}"
        
    elif query_id == "RE_EXAM_TRAINEE_LIST":
        cur.execute("SELECT * FROM re_exam_trainee WHERE office_id = %s ORDER BY id DESC", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No re-exam trainees found."
        lines = [f"- Re-exam ID {r.get('id')} for Trainee {r.get('trainee_id')}" for r in rows[:50]]
        return "Re-exam Trainees List (showing up to 50):\n" + "\n".join(lines)
        
    elif query_id == "RE_EXAM_COUNT_BY_EXAM":
        cur.execute("SELECT exam_schedule_id, COUNT(*) AS total_re_exam FROM re_exam_trainee WHERE office_id = %s GROUP BY exam_schedule_id ORDER BY total_re_exam DESC", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No re-exam counts found."
        lines = [f"- Exam {r['exam_schedule_id']}: {r['total_re_exam']} re-exams" for r in rows]
        return "Re-exam Count by Exam:\n" + "\n".join(lines)
        
    # 6. Principal-Level Combined Questions
    elif query_id == "TRAINEE_COMPLETE_EXAM_REPORT":
        tid = p.get("trainee_id")
        if not tid: return "Please specify a trainee_id."
        cur.execute("SELECT tm.id AS trainee_id, tm.trainee_name, em.exam_schedule_id, em.subject_id, em.marks FROM tra_masters tm LEFT JOIN exam_marks em ON em.trainee_id = tm.id AND em.office_id = tm.office_id WHERE tm.office_id = %s AND tm.id = %s", (office_id, tid))
        rows = cur.fetchall()
        if not rows: return f"No exam report found for trainee ID {tid}."
        t_name = rows[0].get('trainee_name', f'ID {tid}')
        lines = [f"- Exam {r['exam_schedule_id']}, Subject {r['subject_id']}: {r['marks']} marks" for r in rows if r['exam_schedule_id']]
        return f"Complete Exam Report for {t_name}:\n" + ("\n".join(lines) if lines else "No marks recorded.")
        
    elif query_id == "TRAINEES_WITH_NO_MARKS":
        cur.execute("SELECT tm.id, tm.trainee_name FROM tra_masters tm LEFT JOIN exam_marks em ON em.trainee_id = tm.id AND em.office_id = tm.office_id WHERE tm.office_id = %s AND em.id IS NULL", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No trainees without marks found."
        lines = [f"- {r.get('trainee_name')} (ID: {r.get('id')})" for r in rows[:50]]
        return "Trainees with No Marks (showing up to 50):\n" + "\n".join(lines)
        
    elif query_id == "AVERAGE_MARKS_BY_TRAINEE":
        cur.execute("SELECT tm.id AS trainee_id, tm.trainee_name, AVG(em.marks) AS average_marks FROM tra_masters tm JOIN exam_marks em ON em.trainee_id = tm.id AND em.office_id = tm.office_id WHERE tm.office_id = %s GROUP BY tm.id, tm.trainee_name ORDER BY average_marks DESC", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No average marks data found."
        lines = [f"- {r.get('trainee_name')}: {round(r['average_marks'] or 0, 2)} avg" for r in rows[:50]]
        return "Average Marks by Trainee (showing top 50):\n" + "\n".join(lines)
        
    elif query_id == "WEAK_TRAINEES":
        th = float(p.get("threshold_marks", 50))
        cur.execute("SELECT tm.id AS trainee_id, tm.trainee_name, AVG(em.marks) AS average_marks FROM tra_masters tm JOIN exam_marks em ON em.trainee_id = tm.id AND em.office_id = tm.office_id WHERE tm.office_id = %s GROUP BY tm.id, tm.trainee_name HAVING AVG(em.marks) < %s ORDER BY average_marks ASC", (office_id, th))
        rows = cur.fetchall()
        if not rows: return f"No weak trainees found (avg marks < {th})."
        lines = [f"- {r.get('trainee_name')}: {round(r['average_marks'] or 0, 2)} avg" for r in rows[:50]]
        return f"Weak Trainees (avg < {th}):\n" + "\n".join(lines)

    # 20 New Queries
    elif query_id == "ACTIVE_EXAM_TYPES":
        cur.execute("SELECT id, title, title_hindi, total_mark, weightage FROM exam_type WHERE status = 1 ORDER BY title")
        rows = cur.fetchall()
        if not rows: return "No active exam types found."
        count = len(rows)
        lines = [f"- {r.get('title')} (ID: {r.get('id')}), Total Marks: {r.get('total_mark')}" for r in rows]
        return f"Total active exam types: {count}\n" + "\n".join(lines)
        
    elif query_id == "EXAM_TYPE_DETAILS_BY_ID":
        et_id = p.get("exam_type_id")
        if not et_id: return "Please specify an exam_type_id."
        cur.execute("SELECT id, title, title_hindi, total_mark, weightage, CASE status WHEN 1 THEN 'Active' ELSE 'Inactive' END AS status FROM exam_type WHERE id = %s", (et_id,))
        r = cur.fetchone()
        if not r: return f"Exam type {et_id} not found."
        return f"Exam Type {et_id}: {r.get('title')} - Status: {r.get('status')}, Total Marks: {r.get('total_mark')}"

    elif query_id == "ALL_MARKS_FOR_TRAINEE":
        uid = p.get("user_id")
        if not uid: return "Please specify a user_id."
        cur.execute("SELECT em.id, c.course_name, et.title AS exam_type, s.subject_name, em.mark_obtained, em.total_mark, em.re_exam_mark, CASE em.result WHEN 1 THEN 'Pass' WHEN 2 THEN 'Fail' ELSE 'Pending' END AS result, CASE em.re_exam_result WHEN 1 THEN 'Pass' WHEN 2 THEN 'Fail' ELSE '-' END AS re_exam_result FROM exam_marks em JOIN training_calendars tc ON tc.id = em.course_id JOIN courses c ON c.id = tc.ct_id JOIN exam_type et ON et.id = em.exam_type_id LEFT JOIN subjects s ON s.id = em.subject_id WHERE em.user_id = %s AND em.status = 1 ORDER BY em.created_at DESC", (uid,))
        rows = cur.fetchall()
        if not rows: return f"I could not find any exam records for trainee ID {uid} in your office."
        lines = [f"- {r.get('course_name')} ({r.get('exam_type')}): {r.get('mark_obtained')}/{r.get('total_mark')} - {r.get('result')}" for r in rows[:50]]
        return f"Marks for User {uid}:\n" + "\n".join(lines)

    elif query_id == "ALL_MARKS_FOR_COURSE":
        cid = p.get("course_id")
        if not cid: return "Please specify a course_id."
        cur.execute("SELECT u.name, u.user_code, et.title AS exam_type, s.subject_name, em.mark_obtained, em.total_mark, CASE em.result WHEN 1 THEN 'Pass' WHEN 2 THEN 'Fail' ELSE 'Pending' END AS result FROM exam_marks em JOIN users u ON u.id = em.user_id JOIN exam_type et ON et.id = em.exam_type_id LEFT JOIN subjects s ON s.id = em.subject_id WHERE em.course_id = %s AND em.status = 1 ORDER BY u.name, et.title", (cid,))
        rows = cur.fetchall()
        if not rows: return f"No marks found for course {cid}."
        lines = [f"- {r.get('name')} ({r.get('exam_type')}): {r.get('mark_obtained')}/{r.get('total_mark')} - {r.get('result')}" for r in rows[:50]]
        return f"Marks for Course {cid}:\n" + "\n".join(lines)

    elif query_id == "MARKS_FOR_TRAINEE_IN_COURSE":
        uid = p.get("user_id")
        cid = p.get("course_id")
        if not uid or not cid: return "Please specify user_id and course_id."
        cur.execute("SELECT et.title AS exam_type, s.subject_name, em.mark_obtained, em.total_mark, em.re_exam_mark, CASE em.result WHEN 1 THEN 'Pass' WHEN 2 THEN 'Fail' ELSE 'Pending' END AS result, CASE em.re_exam_result WHEN 1 THEN 'Pass' WHEN 2 THEN 'Fail' ELSE '-' END AS re_exam_result, em.created_at FROM exam_marks em JOIN exam_type et ON et.id = em.exam_type_id LEFT JOIN subjects s ON s.id = em.subject_id WHERE em.user_id = %s AND em.course_id = %s AND em.status = 1 ORDER BY et.title", (uid, cid))
        rows = cur.fetchall()
        if not rows: return f"No marks found for user {uid} in course {cid}."
        lines = [f"- {r.get('exam_type')} ({r.get('subject_name')}): {r.get('mark_obtained')}/{r.get('total_mark')} - {r.get('result')}" for r in rows]
        return f"Marks for User {uid} in Course {cid}:\n" + "\n".join(lines)

    elif query_id == "MARKS_BY_EXAM_TYPE_FOR_COURSE":
        cid = p.get("course_id")
        et_id = p.get("exam_type_id")
        if not cid or not et_id: return "Please specify course_id and exam_type_id."
        cur.execute("SELECT u.name, u.user_code, u.designation, em.mark_obtained, em.total_mark, ROUND(em.mark_obtained * 100.0 / NULLIF(em.total_mark,0), 1) AS percentage, CASE em.result WHEN 1 THEN 'Pass' WHEN 2 THEN 'Fail' ELSE 'Pending' END AS result FROM exam_marks em JOIN users u ON u.id = em.user_id WHERE em.course_id = %s AND em.exam_type_id = %s AND em.status = 1 ORDER BY CAST(em.mark_obtained AS UNSIGNED) DESC", (cid, et_id))
        rows = cur.fetchall()
        if not rows: return f"No marks found for course {cid} and exam type {et_id}."
        lines = [f"- {r.get('name')}: {r.get('mark_obtained')}/{r.get('total_mark')} ({r.get('percentage')}%) - {r.get('result')}" for r in rows[:50]]
        return f"Marks for Course {cid}, Exam Type {et_id}:\n" + "\n".join(lines)

    elif query_id == "SUBJECT_WISE_MARKS_FOR_TRAINEE_IN_COURSE":
        uid = p.get("user_id")
        cid = p.get("course_id")
        if not uid or not cid: return "Please specify user_id and course_id."
        cur.execute("SELECT s.subject_name, s.subject_code, et.title AS exam_type, em.mark_obtained, em.total_mark, ROUND(em.mark_obtained * 100.0 / NULLIF(em.total_mark,0), 1) AS pct, CASE em.result WHEN 1 THEN 'Pass' WHEN 2 THEN 'Fail' ELSE '-' END AS result FROM exam_marks em JOIN subjects s ON s.id = em.subject_id JOIN exam_type et ON et.id = em.exam_type_id WHERE em.user_id = %s AND em.course_id = %s AND em.status = 1 ORDER BY s.subject_name", (uid, cid))
        rows = cur.fetchall()
        if not rows: return f"No marks found for user {uid} in course {cid}."
        lines = [f"- {r.get('subject_name')} ({r.get('exam_type')}): {r.get('mark_obtained')}/{r.get('total_mark')} - {r.get('result')}" for r in rows]
        return f"Subject Marks for User {uid} in Course {cid}:\n" + "\n".join(lines)

    elif query_id == "HIGHEST_SCORERS_IN_COURSE":
        cid = p.get("course_id")
        course_name = _clean_course_name(p.get("course_name") or p.get("exam_name"))
        et_id = p.get("exam_type_id")
        
        # Resolve course_name to course_id if name is provided
        if not cid and course_name:
            cur.execute(
                """SELECT tc.id, tc.course_batch FROM training_calendars tc 
                   JOIN courses c ON c.id = tc.ct_id 
                   WHERE LOWER(c.course_name) LIKE LOWER(%s) AND tc.office_id = %s 
                   AND EXISTS (SELECT 1 FROM exam_marks em WHERE em.course_id = tc.id)
                   ORDER BY tc.from_date DESC LIMIT 1""",
                (f"%{course_name}%", office_id)
            )
            match = cur.fetchone()
            if match:
                cid = match['id']
            else:
                return f"No exam marks data found for any '{course_name}' course."
        
        if not cid:
            cur.execute(
                """SELECT tc.id FROM training_calendars tc 
                   WHERE tc.office_id = %s 
                   AND EXISTS (SELECT 1 FROM exam_marks em WHERE em.course_id = tc.id)
                   ORDER BY tc.from_date DESC LIMIT 1""", 
                (office_id,)
            )
            row = cur.fetchone()
            if not row: return "No exam marks data available yet."
            cid = row['id']
        if not et_id:
            cur.execute("SELECT id FROM exam_type WHERE office_id = %s ORDER BY id ASC LIMIT 1", (office_id,))
            row = cur.fetchone()
            if not row: return "No exam types available."
            et_id = row['id']
        cur.execute("SELECT u.name, u.user_code, u.designation, em.mark_obtained, em.total_mark, ROUND(em.mark_obtained * 100.0 / NULLIF(em.total_mark,0), 1) AS percentage, c.course_name, tc.course_batch, et.title AS exam_type_name FROM exam_marks em JOIN users u ON u.id = em.user_id JOIN training_calendars tc ON tc.id = em.course_id JOIN courses c ON c.id = tc.ct_id JOIN exam_type et ON et.id = em.exam_type_id WHERE em.course_id = %s AND em.exam_type_id = %s AND em.status = 1 ORDER BY CAST(em.mark_obtained AS UNSIGNED) DESC LIMIT 10", (cid, et_id))
        rows = cur.fetchall()
        if not rows: return f"No highest scorers found for course {cid} and exam type {et_id}."
        
        display_name = f"{rows[0]['course_name']} ({rows[0]['course_batch']})"
        et_name = rows[0]['exam_type_name']
        lines = [f"- {r.get('name')}: {r.get('mark_obtained')}/{r.get('total_mark')} ({r.get('percentage')}%)" for r in rows]
        return f"Top Scorers for {display_name}, Exam Type: {et_name}:\n" + "\n".join(lines)

    elif query_id == "PASS_FAIL_SUMMARY_FOR_COURSE":
        cid = p.get("course_id")
        if not cid: return "Please specify a course_id."
        cur.execute("SELECT et.title AS exam_type, COUNT(*) AS total, SUM(IF(em.result=1,1,0)) AS passed, SUM(IF(em.result=2,1,0)) AS failed, SUM(IF(em.result=0,1,0)) AS pending, ROUND(SUM(IF(em.result=1,1,0))*100.0/COUNT(*),1) AS pass_pct FROM exam_marks em JOIN exam_type et ON et.id = em.exam_type_id WHERE em.course_id = %s AND em.status = 1 GROUP BY em.exam_type_id, et.title ORDER BY et.title", (cid,))
        rows = cur.fetchall()
        if not rows: return f"No pass/fail summary for course {cid}."
        lines = [f"- {r.get('exam_type')}: Pass {r.get('passed')}, Fail {r.get('failed')}, Pending {r.get('pending')} (Pass {r.get('pass_pct')}%)" for r in rows]
        return f"Pass/Fail Summary for Course {cid}:\n" + "\n".join(lines)

    elif query_id == "ALL_FAILED_TRAINEES_IN_COURSE":
        cid = p.get("course_id")
        if not cid:
            cur.execute("SELECT id FROM courses WHERE office_id = %s ORDER BY id DESC LIMIT 1", (office_id,))
            row = cur.fetchone()
            if not row: return "No courses available."
            cid = row['id']
        cur.execute("SELECT u.name, u.user_code, u.mobile, et.title AS exam_type, em.mark_obtained, em.total_mark, em.re_exam_mark, CASE em.re_exam_result WHEN 1 THEN 'Pass' WHEN 2 THEN 'Still Fail' ELSE 'Not Given' END AS re_exam FROM exam_marks em JOIN users u ON u.id = em.user_id JOIN exam_type et ON et.id = em.exam_type_id WHERE em.course_id = %s AND em.result = 2 AND em.status = 1 ORDER BY et.title, u.name", (cid,))
        rows = cur.fetchall()
        if not rows: return f"No failed trainees found for course {cid}."
        lines = [f"- {r.get('name')} in {r.get('exam_type')}: {r.get('mark_obtained')}/{r.get('total_mark')} (Re-exam: {r.get('re_exam')})" for r in rows[:50]]
        return f"Failed Trainees in Course {cid}:\n" + "\n".join(lines)

    elif query_id == "DID_TRAINEE_PASS_IN_COURSE":
        uid = p.get("user_id")
        cid = p.get("course_id")
        if not uid or not cid: return "Please specify user_id and course_id."
        cur.execute("SELECT et.title AS exam_type, em.mark_obtained, em.total_mark, CASE em.result WHEN 1 THEN 'Pass' WHEN 2 THEN 'Fail' ELSE 'Pending' END AS result, em.re_exam_mark, CASE em.re_exam_result WHEN 1 THEN 'Pass' WHEN 2 THEN 'Fail' ELSE 'N/A' END AS re_exam_result FROM exam_marks em JOIN exam_type et ON et.id = em.exam_type_id WHERE em.user_id = %s AND em.course_id = %s AND em.status = 1", (uid, cid))
        rows = cur.fetchall()
        if not rows: return f"No pass/fail records found for user {uid} in course {cid}."
        lines = [f"- {r.get('exam_type')}: {r.get('result')} (Marks: {r.get('mark_obtained')}/{r.get('total_mark')})" for r in rows]
        return f"Pass/Fail Status for User {uid} in Course {cid}:\n" + "\n".join(lines)

    elif query_id == "OVERALL_PASS_FAIL_COUNT":
        cur.execute("SELECT c.course_name, COUNT(DISTINCT em.user_id) AS trainees, SUM(IF(em.result=1,1,0)) AS pass_count, SUM(IF(em.result=2,1,0)) AS fail_count, ROUND(SUM(IF(em.result=1,1,0))*100.0/NULLIF(COUNT(*),0),1) AS pass_pct FROM exam_marks em JOIN training_calendars tc ON tc.id = em.course_id JOIN courses c ON c.id = tc.ct_id WHERE tc.office_id = %s AND em.status = 1 GROUP BY em.course_id, c.course_name ORDER BY trainees DESC", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No overall pass/fail data found."
        lines = [f"- {r.get('course_name')}: Trainees {r.get('trainees')}, Pass {r.get('pass_count')}, Fail {r.get('fail_count')} (Pass {r.get('pass_pct')}%)" for r in rows[:50]]
        return "Overall Pass/Fail Count:\n" + "\n".join(lines)

    elif query_id == "TRAINEES_APPEARED_IN_RE_EXAM":
        cid = p.get("course_id")
        if not cid: return "Please specify a course_id."
        cur.execute("SELECT u.name, u.user_code, et.title AS exam_type, em.mark_obtained AS original_mark, em.re_exam_mark, CASE em.re_exam_result WHEN 1 THEN 'Pass' WHEN 2 THEN 'Fail' ELSE 'Not Given' END AS re_exam_result FROM exam_marks em JOIN users u ON u.id = em.user_id JOIN exam_type et ON et.id = em.exam_type_id WHERE em.course_id = %s AND em.result = 2 AND em.re_exam_mark > 0 AND em.status = 1 ORDER BY u.name", (cid,))
        rows = cur.fetchall()
        if not rows: return f"No re-exam data found for course {cid}."
        lines = [f"- {r.get('name')} in {r.get('exam_type')}: Re-exam {r.get('re_exam_result')} (Mark: {r.get('re_exam_mark')})" for r in rows[:50]]
        return f"Re-exam Trainees in Course {cid}:\n" + "\n".join(lines)

    elif query_id == "TRAINEES_FAILED_AFTER_RE_EXAM":
        cid = p.get("course_id")
        if not cid: return "Please specify a course_id."
        cur.execute("SELECT u.name, u.user_code, u.mobile, et.title AS exam_type, em.mark_obtained AS original_mark, em.re_exam_mark FROM exam_marks em JOIN users u ON u.id = em.user_id JOIN exam_type et ON et.id = em.exam_type_id WHERE em.course_id = %s AND em.result = 2 AND em.re_exam_result = 2 AND em.status = 1 ORDER BY u.name", (cid,))
        rows = cur.fetchall()
        if not rows: return f"No trainees failed after re-exam in course {cid}."
        lines = [f"- {r.get('name')} in {r.get('exam_type')}: Re-exam Mark {r.get('re_exam_mark')}" for r in rows[:50]]
        return f"Failed After Re-exam in Course {cid}:\n" + "\n".join(lines)

    elif query_id == "EXAM_DESIGN_FOR_COURSE":
        cur.execute("SELECT et.title AS exam_type, s.subject_name, ed.total_marks, ed.minimum_marks, ed.mcq, ed.essay, ed.type_sort, CASE ed.status WHEN 1 THEN 'Active' ELSE 'Inactive' END AS status FROM exam_design ed JOIN exam_type et ON et.id = ed.cs_id LEFT JOIN subjects s ON s.id = ed.subject_id WHERE ed.office_id = %s AND ed.status = 1 ORDER BY ed.type_sort", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No exam design data found."
        lines = [f"- {r.get('exam_type')}: Total {r.get('total_marks')}, Min {r.get('minimum_marks')}" for r in rows[:50]]
        return "Exam Design:\n" + "\n".join(lines)

    elif query_id == "MIN_PASS_MARKS_PER_EXAM_TYPE":
        cur.execute("SELECT et.title AS exam_type, ed.total_marks, ed.minimum_marks, ROUND(ed.minimum_marks*100.0/NULLIF(ed.total_marks,0),1) AS min_pass_pct, ed.mcq AS mcq_questions, ed.essay AS essay_questions FROM exam_design ed JOIN exam_type et ON et.id = ed.cs_id WHERE ed.office_id = %s AND ed.status = 1 ORDER BY et.title", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No min pass marks data found."
        lines = [f"- {r.get('exam_type')}: Min {r.get('minimum_marks')}/{r.get('total_marks')} ({r.get('min_pass_pct')}%)" for r in rows[:50]]
        return "Minimum Passing Marks by Exam Type:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_SUBMISSIONS_FOR_COURSE":
        cid = p.get("course_id")
        if not cid: return "Please specify a course_id."
        cur.execute("SELECT u.name, u.user_code, fs.fs_title AS section, fm.final_submit, fm.created_at AS submitted_at FROM feed_master fm JOIN users u ON u.id = fm.user_id JOIN feed_section fs ON fs.fs_id = fm.fs_id WHERE fm.course_id = %s AND fm.status = 1 ORDER BY fm.created_at DESC", (cid,))
        rows = cur.fetchall()
        if not rows: return f"No feedback submissions found for course {cid}."
        lines = [f"- {r.get('name')} in {r.get('section')}: {'Final' if r.get('final_submit') else 'Draft'}" for r in rows[:50]]
        return f"Feedback Submissions for Course {cid}:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_SUBMITTED_COUNT_FOR_COURSE":
        cid = p.get("course_id")
        if not cid: return "Please specify a course_id."
        cur.execute("SELECT COUNT(DISTINCT user_id) AS submitted_count, SUM(IF(final_submit=1,1,0)) AS final_submitted, SUM(IF(final_submit=0,1,0)) AS draft_only FROM feed_master WHERE course_id = %s AND status = 1", (cid,))
        r = cur.fetchone()
        if not r: return f"No feedback stats found for course {cid}."
        return f"Feedback Stats for Course {cid}:\nTotal Trainees: {r.get('submitted_count')}\nFinal: {r.get('final_submitted')}\nDraft: {r.get('draft_only')}"

    elif query_id == "FEEDBACK_RESPONSES_FOR_QUESTION":
        fq_id = p.get("fq_id")
        cid = p.get("course_id")
        if not fq_id or not cid: return "Please specify fq_id and course_id."
        cur.execute("SELECT u.name, u.user_code, fm.response, fm.created_at FROM feed_master fm JOIN users u ON u.id = fm.user_id WHERE fm.fq_id = %s AND fm.course_id = %s AND fm.status = 1 ORDER BY fm.created_at", (fq_id, cid))
        rows = cur.fetchall()
        if not rows: return f"No feedback responses found for question {fq_id} in course {cid}."
        lines = [f"- {r.get('name')}: {r.get('response')}" for r in rows[:50]]
        return f"Feedback Responses for Question {fq_id}, Course {cid}:\n" + "\n".join(lines)

    elif query_id == "LIST_ALL_FEEDBACK_QUESTIONS":
        cur.execute("SELECT fq.fq_code, fq.fq_title, fs.fs_title AS section, fq.fq_type, fq.fq_sort, CASE fq.status WHEN 1 THEN 'Active' ELSE 'Inactive' END AS status FROM feed_que fq JOIN feed_section fs ON fs.fs_id = fq.fs_id WHERE fq.office_id = %s ORDER BY fq.fq_sort", (office_id,))
        rows = cur.fetchall()
        if not rows: return "No feedback questions found."
        lines = [f"- {r.get('fq_title')} ({r.get('section')}): {r.get('status')}" for r in rows[:50]]
        return "Feedback Questions:\n" + "\n".join(lines)
        
    return None
