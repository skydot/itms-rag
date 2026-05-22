import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "trms_user"),
    password=os.getenv("DB_PASSWORD", "trms123"),
    database=os.getenv("DB_NAME", "trms_dump")
)

cur = conn.cursor(dictionary=True)

name = "%mayank%"
cur.execute("SELECT id, name, office_id FROM users WHERE LOWER(name) LIKE LOWER(%s)", (name,))
users = cur.fetchall()
print("Users:", users)

for u in users:
    uid = u['id']
    print(f"\n--- Data for user {uid} ({u['name']}) ---")
    
    cur.execute("""
        SELECT tm.id as tm_id, tm.course_id, tm.is_approved, tc.course_batch 
        FROM tra_masters tm
        JOIN training_calendars tc ON tc.id = tm.course_id
        WHERE tm.user_id = %s
    """, (uid,))
    tms = cur.fetchall()
    print("Tra Masters:", tms)
    
    cur.execute("""
        SELECT em.subject_id, em.course_id, em.mark_obtained 
        FROM exam_marks em 
        WHERE em.user_id = %s
    """, (uid,))
    marks = cur.fetchall()
    print("Exam Marks:", marks)

    cur.execute("""
        SELECT s.subject_name, em.mark_obtained, s.total_mark, tc.course_batch, u.name AS trainee_name, ed.status, s.not_in_exam
        FROM et_design ed
        JOIN training_calendars tc ON tc.id = ed.course_id
        JOIN subjects s ON s.id = ed.subject
        JOIN tra_masters tm ON tm.course_id = ed.course_id AND tm.is_approved = 1
        JOIN users u ON u.id = tm.user_id
        LEFT JOIN exam_design ee ON ee.subject_id = ed.subject AND ee.cs_id = tc.ct_id
        LEFT JOIN exam_marks em ON em.user_id = tm.user_id AND em.course_id = tm.course_id AND em.subject_id = ed.subject
        WHERE u.id = %s 
    """, (uid,))
    full_query = cur.fetchall()
    print("Full Query Results:")
    for row in full_query:
        print(row)

cur.close()
conn.close()
