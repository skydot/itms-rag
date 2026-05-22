from app.services.db_service import get_connection


def get_marks_by_trainee(search_name: str, office_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT
                u.name AS trainee_name,
                c.course_name,
                es.subject_name,
                em.mark_obtained,
                em.total_mark,
                em.result
            FROM exam_marks em
            LEFT JOIN users u ON em.user_id = u.id
            LEFT JOIN courses c ON em.course_id = c.id
            LEFT JOIN exam_subject es ON em.sub_id = es.id
            WHERE u.name LIKE %s
              AND em.office_id = %s
            LIMIT 10
            """,
            (f"%{search_name}%", office_id),
        )

        rows = cursor.fetchall()
        sanitized_rows = []

        for row in rows:
            marks = row.get("mark_obtained") or 0
            total = row.get("total_mark") or 0

            sanitized_rows.append(
                {
                    "trainee_name": row.get("trainee_name") or "Unknown trainee",
                    "course_name": row.get("course_name") or "training",
                    "subject_name": row.get("subject_name") or "subject",
                    "marks_text": f"{marks} out of {total}" if total else str(marks),
                    "result": "passed" if row.get("result") == 1 else "failed",
                }
            )

        return sanitized_rows
    finally:
        conn.close()
