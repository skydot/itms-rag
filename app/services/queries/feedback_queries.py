"""Feedback module query templates."""

TEMPLATES = [
    {
        "id": "FEEDBACK_TOTAL",
        "module": "feedback",
        "description": "Total feedback responses",
        "example_questions": ["Total feedback?", "How many feedback responses?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_BY_COURSE",
        "module": "feedback",
        "description": "Feedback by course",
        "example_questions": ["Feedback by course?", "Course-wise feedback?"],
        "required_params": [],
        "optional_params": ["course_id", "course_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_BY_TRAINEE",
        "module": "feedback",
        "description": "Feedback by trainee/user",
        "example_questions": ["Feedback by trainee?", "User's feedback?"],
        "required_params": [],
        "optional_params": ["user_id", "user_name", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_QUESTION_WISE",
        "module": "feedback",
        "description": "Question-wise feedback",
        "example_questions": ["Question-wise feedback?", "Feedback by question?"],
        "required_params": [],
        "optional_params": ["fq_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_SECTION_WISE",
        "module": "feedback",
        "description": "Section-wise feedback",
        "example_questions": ["Section-wise feedback?", "Feedback by section?"],
        "required_params": [],
        "optional_params": ["fs_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_AVERAGE_RATING",
        "module": "feedback",
        "description": "Average rating",
        "example_questions": ["Average rating?", "Overall feedback rating?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_POSITIVE_NEGATIVE",
        "module": "feedback",
        "description": "Positive/negative feedback",
        "example_questions": ["Positive feedback?", "Negative feedback?"],
        "required_params": [],
        "optional_params": ["sentiment", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_PENDING_USERS",
        "module": "feedback",
        "description": "Feedback pending users",
        "example_questions": ["Who hasn't given feedback?", "Pending feedback users?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_SUBMITTED_USERS",
        "module": "feedback",
        "description": "Feedback submitted users",
        "example_questions": ["Who submitted feedback?", "Feedback submitted list?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_COURSE_CONTENT",
        "module": "feedback",
        "description": "Course content feedback",
        "example_questions": ["Course content feedback?", "Content rating?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_FACILITY",
        "module": "feedback",
        "description": "Facility feedback",
        "example_questions": ["Facility feedback?", "Infrastructure feedback?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_VL",
        "module": "feedback",
        "description": "VL feedback",
        "example_questions": ["VL feedback?", "Visiting lecturer feedback?"],
        "required_params": [],
        "optional_params": ["vl_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_BY_YEAR",
        "module": "feedback",
        "description": "Feedback by year",
        "example_questions": ["Feedback by year?", "Annual feedback?"],
        "required_params": [],
        "optional_params": ["year", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_BY_MONTH",
        "module": "feedback",
        "description": "Feedback by month",
        "example_questions": ["Feedback by month?", "Monthly feedback?"],
        "required_params": [],
        "optional_params": ["month", "year", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_COMMENTS",
        "module": "feedback",
        "description": "Feedback comments/list",
        "example_questions": ["Feedback comments?", "Show feedback text?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_TOP_RATED",
        "module": "feedback",
        "description": "Top rated course",
        "example_questions": ["Top rated course?", "Best rated course?"],
        "required_params": [],
        "optional_params": ["office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "ranking",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_LOW_RATED",
        "module": "feedback",
        "description": "Low rated course",
        "example_questions": ["Low rated course?", "Worst rated course?"],
        "required_params": [],
        "optional_params": ["office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "ranking",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_RESPONSE_COUNT",
        "module": "feedback",
        "description": "Feedback response count",
        "example_questions": ["Feedback response count?", "Total responses?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_SUMMARY_BY_QUESTION",
        "module": "feedback",
        "description": "Feedback summary by question",
        "example_questions": ["Question summary?", "Feedback stats by question?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FEEDBACK_MODULE_SUMMARY",
        "module": "feedback",
        "description": "Feedback module summary",
        "example_questions": ["Feedback summary?", "Feedback module overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute feedback queries."""
    p = params or {}
    
    if query_id == "FEEDBACK_TOTAL":
        cur.execute("SELECT COUNT(*) AS total FROM feed_master fm JOIN training_calendars tc ON tc.id = fm.course_id WHERE tc.office_id = %s", (office_id,))
        r = cur.fetchone()
        return f"Total feedback responses: {r['total'] if r else 0}"

    elif query_id == "FEEDBACK_BY_COURSE":
        cur.execute("""
            SELECT fm.course_id, c.course_name, tc.course_batch,
                   COUNT(DISTINCT fm.user_id) AS respondents,
                   ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))), 2) AS avg_rating
            FROM feed_master fm
            JOIN training_calendars tc ON tc.id = fm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE fm.status = 1 AND fm.final_submit = 1 AND tc.office_id = %s
            GROUP BY fm.course_id, c.course_name, tc.course_batch
            ORDER BY avg_rating DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No course feedback found."
        lines = [f"- {r['course_name']} ({r['course_batch']}): {r['avg_rating']} Stars ({r['respondents']} Respondents)" for r in rows]
        return "Feedback by Course:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_BY_TRAINEE":
        uid = p.get("user_id")
        if not uid: return "Please specify user_id."
        cur.execute("""
            SELECT u.name, u.name_hindi, fm.course_id, c.course_name,
                   COUNT(fm.id) AS responses_given,
                   fm.final_submit
            FROM feed_master fm
            JOIN users u ON u.id = fm.user_id
            JOIN training_calendars tc ON tc.id = fm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE fm.user_id = %s AND fm.status = 1 AND tc.office_id = %s
            GROUP BY fm.user_id, fm.course_id, fm.final_submit, u.name, u.name_hindi, c.course_name
            ORDER BY fm.course_id
            LIMIT 50
        """, (uid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No feedback found for trainee {uid}."
        lines = [f"- {r['course_name']}: {r['responses_given']} Responses (Submitted: {'Yes' if r['final_submit']==1 else 'No'})" for r in rows]
        return f"Feedback by {rows[0]['name']}:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_QUESTION_WISE":
        cur.execute("""
            SELECT fq.fq_id, fq.fq_title, fq.fq_code,
                   COUNT(fm.id) AS response_count,
                   ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))), 2) AS avg_score
            FROM feed_que fq
            LEFT JOIN feed_master fm ON fm.fq_id = fq.fq_id AND fm.status = 1
            LEFT JOIN training_calendars tc ON tc.id = fm.course_id
            WHERE fq.status = 1 AND (tc.office_id = %s OR tc.office_id IS NULL)
            GROUP BY fq.fq_id, fq.fq_title, fq.fq_code
            ORDER BY fq.fq_sort
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No question-wise feedback found."
        lines = [f"- {r['fq_code']}: {r['fq_title']} -> Rating: {r['avg_score']} ({r['response_count']} Responses)" for r in rows]
        return "Question-wise Feedback:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_SECTION_WISE":
        cur.execute("""
            SELECT fs.fs_title, fs.fs_code,
                   COUNT(fm.id) AS response_count,
                   ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))), 2) AS avg_score
            FROM feed_section fs
            LEFT JOIN feed_master fm ON fm.fs_id = fs.fs_id AND fm.status = 1
            LEFT JOIN training_calendars tc ON tc.id = fm.course_id
            WHERE fs.status = 1 AND (tc.office_id = %s OR tc.office_id IS NULL)
            GROUP BY fs.fs_id, fs.fs_title, fs.fs_code
            ORDER BY fs.fs_sort
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No section-wise feedback found."
        lines = [f"- {r['fs_title']}: Rating: {r['avg_score']} ({r['response_count']} Responses)" for r in rows]
        return "Section-wise Feedback:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_AVERAGE_RATING":
        cur.execute("""
            SELECT c.course_name, tc.course_batch,
                   ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))), 2) AS avg_rating,
                   COUNT(DISTINCT fm.user_id) AS total_respondents
            FROM feed_master fm
            JOIN training_calendars tc ON tc.id = fm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE fm.status = 1 AND fm.final_submit = 1 AND tc.office_id = %s
            GROUP BY fm.course_id, c.course_name, tc.course_batch
            ORDER BY avg_rating DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No average ratings found."
        lines = [f"- {r['course_name']} ({r['course_batch']}): {r['avg_rating']} Stars ({r['total_respondents']} Respondents)" for r in rows]
        return "Average Course Ratings:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_POSITIVE_NEGATIVE":
        cur.execute("""
            SELECT c.course_name,
                   SUM(CASE WHEN CAST(fm.response AS DECIMAL) >= 3 THEN 1 ELSE 0 END) AS positive,
                   SUM(CASE WHEN CAST(fm.response AS DECIMAL) < 3 THEN 1 ELSE 0 END) AS negative
            FROM feed_master fm
            JOIN training_calendars tc ON tc.id = fm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE fm.status = 1 AND fm.fq_type = 1 AND tc.office_id = %s
            GROUP BY fm.course_id, c.course_name
            ORDER BY positive DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No positive/negative feedback split found."
        lines = [f"- {r['course_name']}: {r['positive']} Positive, {r['negative']} Negative" for r in rows]
        return "Feedback Positive/Negative Split:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_PENDING_USERS":
        cur.execute("""
            SELECT u.id, u.name, u.mobile, c.course_name, tc.course_batch
            FROM tra_masters trm
            JOIN users u ON u.id = trm.user_id
            JOIN training_calendars tc ON tc.id = trm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE trm.is_approved = 1 AND tc.office_id = %s
              AND NOT EXISTS (
                SELECT 1 FROM feed_master fm
                WHERE fm.user_id = trm.user_id
                  AND fm.course_id = trm.course_id
                  AND fm.final_submit = 1
                  AND fm.status = 1
              )
            ORDER BY u.name
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No users with pending feedback found."
        lines = [f"- {r['name']} ({r['mobile']}): Missing feedback for {r['course_name']} ({r['course_batch']})" for r in rows]
        return "Pending Feedback Users:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_SUBMITTED_USERS":
        cur.execute("""
            SELECT DISTINCT u.id, u.name, u.mobile, c.course_name, tc.course_batch,
                   MAX(fm.created_at) AS submitted_at
            FROM feed_master fm
            JOIN users u ON u.id = fm.user_id
            JOIN training_calendars tc ON tc.id = fm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE fm.final_submit = 1 AND fm.status = 1 AND tc.office_id = %s
            GROUP BY u.id, u.name, u.mobile, c.course_name, tc.course_batch
            ORDER BY submitted_at DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No users have submitted feedback."
        lines = [f"- {r['name']}: {r['course_name']} ({r['course_batch']}) submitted at {r['submitted_at']}" for r in rows]
        return "Submitted Feedback Users:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_COURSE_CONTENT":
        cur.execute("""
            SELECT fq.fq_title, fm.course_id, c.course_name,
                   ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))), 2) AS avg_score,
                   COUNT(fm.id) AS count
            FROM feed_master fm
            JOIN feed_que fq ON fq.fq_id = fm.fq_id
            JOIN training_calendars tc ON tc.id = fm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE fm.fs_type = 0 AND fm.status = 1 AND tc.office_id = %s
            GROUP BY fq.fq_id, fq.fq_title, fm.course_id, c.course_name
            ORDER BY avg_score DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No course content feedback found."
        lines = [f"- {r['course_name']} ({r['fq_title']}): Rating {r['avg_score']} ({r['count']} Responses)" for r in rows]
        return "Course Content Feedback:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_FACILITY":
        cur.execute("""
            SELECT fs.fs_title AS section, fq.fq_title AS question,
                   ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))), 2) AS avg_score
            FROM feed_master fm
            JOIN feed_section fs ON fs.fs_id = fm.fs_id
            JOIN feed_que fq ON fq.fq_id = fm.fq_id
            JOIN training_calendars tc ON tc.id = fm.course_id
            WHERE fm.status = 1 AND fm.fq_type = 1 AND tc.office_id = %s
            GROUP BY fs.fs_id, fs.fs_title, fq.fq_id, fq.fq_title
            ORDER BY avg_score DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No facility feedback found."
        lines = [f"- {r['section']} > {r['question']}: Rating {r['avg_score']}" for r in rows]
        return "Facility Feedback:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_VL":
        cur.execute("""
            SELECT vm.subject_name, u.name AS vl_name,
                   COUNT(fm.id) AS feedback_count,
                   ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))), 2) AS avg_rating
            FROM feed_master fm
            JOIN vl_management vm ON vm.id = fm.fs_id AND fm.fs_type = 2
            JOIN users u ON u.id = vm.vl_id
            WHERE fm.status = 1 AND vm.office_id = %s
            GROUP BY vm.id, vm.subject_name, u.name
            ORDER BY avg_rating DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No visiting lecturer feedback found."
        lines = [f"- {r['vl_name']} ({r['subject_name']}): Rating {r['avg_rating']} ({r['feedback_count']} Responses)" for r in rows]
        return "Visiting Lecturer Feedback:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_BY_YEAR":
        cur.execute("""
            SELECT YEAR(fm.created_at) AS yr,
                   COUNT(DISTINCT fm.user_id) AS respondents,
                   COUNT(DISTINCT fm.course_id) AS courses,
                   ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))), 2) AS avg_rating
            FROM feed_master fm
            JOIN training_calendars tc ON tc.id = fm.course_id
            WHERE fm.status = 1 AND fm.final_submit = 1 AND tc.office_id = %s
            GROUP BY YEAR(fm.created_at)
            ORDER BY yr DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No year-wise feedback data found."
        lines = [f"- {r['yr']}: {r['avg_rating']} Stars across {r['courses']} Courses ({r['respondents']} Respondents)" for r in rows]
        return "Feedback by Year:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_BY_MONTH":
        cur.execute("""
            SELECT YEAR(fm.created_at) AS yr, MONTH(fm.created_at) AS mo,
                   MONTHNAME(fm.created_at) AS month_name,
                   COUNT(DISTINCT fm.user_id) AS respondents,
                   ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))), 2) AS avg_rating
            FROM feed_master fm
            JOIN training_calendars tc ON tc.id = fm.course_id
            WHERE fm.status = 1 AND fm.final_submit = 1 AND tc.office_id = %s
            GROUP BY YEAR(fm.created_at), MONTH(fm.created_at), MONTHNAME(fm.created_at)
            ORDER BY yr DESC, mo DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No month-wise feedback data found."
        lines = [f"- {r['month_name']} {r['yr']}: Rating {r['avg_rating']} ({r['respondents']} Respondents)" for r in rows]
        return "Feedback by Month:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_COMMENTS":
        cur.execute("""
            SELECT ff.id, u.name, u.mobile, c.course_name, tc.course_batch,
                   ff.expec, ff.in_depth, ff.hands_on, ff.feed, ff.created_at
            FROM feed_forwards ff
            JOIN users u ON u.id = ff.user_id
            JOIN training_calendars tc ON tc.id = ff.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE ff.status = 1 AND tc.office_id = %s
            ORDER BY ff.created_at DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No feedback comments found."
        lines = [f"- {r['name']} on {r['course_name']}: {r['feed']}" for r in rows]
        return "Feedback Comments:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_TOP_RATED":
        cur.execute("""
            SELECT c.course_name, tc.course_batch,
                   ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))), 2) AS avg_rating,
                   COUNT(DISTINCT fm.user_id) AS respondents
            FROM feed_master fm
            JOIN training_calendars tc ON tc.id = fm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE fm.status = 1 AND fm.final_submit = 1 AND tc.office_id = %s
            GROUP BY fm.course_id, c.course_name, tc.course_batch
            ORDER BY avg_rating DESC
            LIMIT 10
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No top rated courses found."
        lines = [f"- {r['course_name']} ({r['course_batch']}): {r['avg_rating']} Stars ({r['respondents']} Respondents)" for r in rows]
        return "Top 10 Rated Courses:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_LOW_RATED":
        cur.execute("""
            SELECT c.course_name, tc.course_batch,
                   ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))), 2) AS avg_rating,
                   COUNT(DISTINCT fm.user_id) AS respondents
            FROM feed_master fm
            JOIN training_calendars tc ON tc.id = fm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE fm.status = 1 AND fm.final_submit = 1 AND tc.office_id = %s
            GROUP BY fm.course_id, c.course_name, tc.course_batch
            ORDER BY avg_rating ASC
            LIMIT 10
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No lowest rated courses found."
        lines = [f"- {r['course_name']} ({r['course_batch']}): {r['avg_rating']} Stars ({r['respondents']} Respondents)" for r in rows]
        return "Lowest 10 Rated Courses:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_RESPONSE_COUNT":
        cur.execute("""
            SELECT c.course_name, tc.course_batch,
                   COUNT(fm.id) AS total_responses,
                   COUNT(DISTINCT fm.user_id) AS unique_respondents,
                   SUM(fm.final_submit) AS final_submitted
            FROM feed_master fm
            JOIN training_calendars tc ON tc.id = fm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE fm.status = 1 AND tc.office_id = %s
            GROUP BY fm.course_id, c.course_name, tc.course_batch
            ORDER BY total_responses DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No response count data found."
        lines = [f"- {r['course_name']} ({r['course_batch']}): {r['total_responses']} Responses ({r['unique_respondents']} Users)" for r in rows]
        return "Feedback Response Counts:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_SUMMARY_BY_QUESTION":
        cur.execute("""
            SELECT fq.fq_id, fq.fq_code, fq.fq_title,
                   COUNT(fm.id) AS total_responses,
                   ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))), 2) AS avg_score,
                   SUM(CASE WHEN CAST(fm.response AS DECIMAL) = 5 THEN 1 ELSE 0 END) AS score_5,
                   SUM(CASE WHEN CAST(fm.response AS DECIMAL) = 4 THEN 1 ELSE 0 END) AS score_4,
                   SUM(CASE WHEN CAST(fm.response AS DECIMAL) = 3 THEN 1 ELSE 0 END) AS score_3,
                   SUM(CASE WHEN CAST(fm.response AS DECIMAL) <= 2 THEN 1 ELSE 0 END) AS score_low
            FROM feed_que fq
            LEFT JOIN feed_master fm ON fm.fq_id = fq.fq_id AND fm.status = 1
            LEFT JOIN training_calendars tc ON tc.id = fm.course_id
            WHERE fq.status = 1 AND (tc.office_id = %s OR tc.office_id IS NULL)
            GROUP BY fq.fq_id, fq.fq_code, fq.fq_title
            ORDER BY fq.fq_sort
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No question summary found."
        lines = [f"- {r['fq_code']}: Avg {r['avg_score']} ({r['score_5']}x 5s, {r['score_low']}x Low)" for r in rows]
        return "Feedback Summary by Question:\n" + "\n".join(lines)

    elif query_id == "FEEDBACK_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(DISTINCT fm.user_id) FROM feed_master fm JOIN training_calendars tc ON tc.id = fm.course_id WHERE fm.final_submit=1 AND fm.status=1 AND tc.office_id=%s) AS total_submitted,
              (SELECT COUNT(DISTINCT fm.course_id) FROM feed_master fm JOIN training_calendars tc ON tc.id = fm.course_id WHERE fm.status=1 AND tc.office_id=%s) AS courses_with_feedback,
              (SELECT ROUND(AVG(CAST(fm.response AS DECIMAL(5,2))),2) FROM feed_master fm JOIN training_calendars tc ON tc.id = fm.course_id WHERE fm.status=1 AND fm.fq_type=1 AND tc.office_id=%s) AS overall_avg_rating,
              (SELECT COUNT(ff.id) FROM feed_forwards ff JOIN training_calendars tc ON tc.id = ff.course_id WHERE ff.status=1 AND tc.office_id=%s) AS total_comments
        """, (office_id, office_id, office_id, office_id))
        r = cur.fetchone()
        if not r: return "Could not generate feedback module summary."
        return (f"Feedback Module Summary:\n"
                f"Total Submitted Users: {r['total_submitted']}\n"
                f"Courses with Feedback: {r['courses_with_feedback']}\n"
                f"Overall Avg Rating: {r['overall_avg_rating']}\n"
                f"Total Comments: {r['total_comments']}")

    return None
