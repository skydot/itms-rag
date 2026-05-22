import logging
from app.services.db_service import get_connection

logger = logging.getLogger(__name__)


def get_exam_chunks():
    chunks = []
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. exam_marks - main exam data
        cursor.execute("""
            SELECT 
                em.id,
                u.name AS trainee_name,
                u.email,
                c.course_name,
                es.subject_name,
                em.office_id,
                em.mark_obtained,
                em.total_mark,
                em.result
            FROM exam_marks em
            LEFT JOIN users u ON em.user_id = u.id
            LEFT JOIN courses c ON em.course_id = c.id
            LEFT JOIN exam_subject es ON em.sub_id = es.id
            WHERE em.office_id = 2
        """)
        marks_rows = cursor.fetchall()

        for row in marks_rows:
            name = row.get("trainee_name") or "Unknown trainee"
            email = row.get("email") or "N/A"
            course = row.get("course_name") or "Unknown course"
            subject = row.get("subject_name") or "Unknown subject"
            marks = row.get("mark_obtained") or 0
            total = row.get("total_mark") or 0
            result = "PASSED" if row.get("result") == 1 else "FAILED"
            percentage = round((marks/total)*100, 2) if total > 0 else 0

            text = f"""EXAM MARKS RECORD
Trainee: {name}
Email: {email}
Course: {course}
Subject: {subject}
Marks: {marks} out of {total}
Percentage: {percentage}%
Result: {result}
Record ID: {row.get('id')}"""
            
            chunks.append({
                "text": text,
                "trainee_name": name.lower(),
                "trainee_email": email.lower(),
                "course": course.lower(),
                "subject": subject.lower(),
                "office_id": 2,
                "module": "exam",
                "allowed_roles": ["principal", "admin", "exam_staff"],
                "marks": marks,
                "total": total,
                "result": result.lower()
            })

        # 2. exam_subject
        try:
            cursor.execute("SELECT * FROM exam_subject WHERE office_id = 2")
            for row in cursor.fetchall():
                text = f"""EXAM SUBJECT
Subject Name: {row.get('subject_name')}
Subject Code: {row.get('subject_code') or 'N/A'}
Description: {row.get('description') or 'N/A'}
Office ID: {row.get('office_id')}"""
                
                chunks.append({
                    "text": text,
                    "subject_name": row.get('subject_name', '').lower(),
                    "subject_code": row.get('subject_code', '').lower() if row.get('subject_code') else '',
                    "office_id": 2,
                    "module": "exam",
                    "allowed_roles": ["principal", "admin", "exam_staff"]
                })
        except Exception as e:
            logger.warning(f"exam_subject table error: {e}")

        # 3. exam_schedule
        try:
            cursor.execute("SELECT * FROM exam_schedule WHERE office_id = 2")
            for row in cursor.fetchall():
                text = f"""EXAM SCHEDULE
Schedule ID: {row.get('id')}
Exam Date: {row.get('exam_date') or 'TBD'}
Start Time: {row.get('start_time') or 'TBD'}
End Time: {row.get('end_time') or 'TBD'}
Duration: {row.get('duration') or 'N/A'} minutes
Venue: {row.get('venue') or 'TBD'}
Office ID: {row.get('office_id')}"""
                
                chunks.append({
                    "text": text,
                    "office_id": 2,
                    "module": "exam",
                    "allowed_roles": ["principal", "admin", "exam_staff"]
                })
        except Exception as e:
            logger.warning(f"exam_schedule table error: {e}")

        # 4. exam_type
        try:
            cursor.execute("SELECT * FROM exam_type WHERE office_id = 2")
            for row in cursor.fetchall():
                text = f"""EXAM TYPE
Type ID: {row.get('id')}
Type Name: {row.get('type_name')}
Description: {row.get('description') or 'N/A'}
Office ID: {row.get('office_id')}"""
                
                chunks.append({
                    "text": text,
                    "type_name": row.get('type_name', '').lower(),
                    "office_id": 2,
                    "module": "exam",
                    "allowed_roles": ["principal", "admin", "exam_staff"]
                })
        except Exception as e:
            logger.warning(f"exam_type table error: {e}")

        # 5. re_exam_trainee
        try:
            cursor.execute("SELECT * FROM re_exam_trainee WHERE office_id = 2")
            for row in cursor.fetchall():
                text = f"""RE-EXAM RECORD
Record ID: {row.get('id')}
User ID: {row.get('user_id')}
Exam Mark ID: {row.get('exam_mark_id')}
Status: {row.get('status') or 'Pending'}
Reason: {row.get('reason') or 'N/A'}
Applied Date: {row.get('created_at') or 'N/A'}
Office ID: {row.get('office_id')}"""
                
                chunks.append({
                    "text": text,
                    "office_id": 2,
                    "module": "exam",
                    "allowed_roles": ["principal", "admin", "exam_staff"]
                })
        except Exception as e:
            logger.warning(f"re_exam_trainee table error: {e}")

        # Summary
        summary = f"""EXAM MODULE SUMMARY - Office 2
Total Exam Mark Records: {len(marks_rows)}
All exam data available including marks, subjects, schedules, types, and re-exam records."""

        chunks.append({
            "text": summary,
            "trainee_name": "",
            "office_id": 2,
            "module": "exam",
            "allowed_roles": ["principal", "admin", "exam_staff"]
        })

        conn.close()
    except Exception as e:
        logger.error(f"Exam chunker error: {e}")
        if conn:
            conn.close()

    return chunks