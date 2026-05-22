import logging
from app.services.db_service import get_connection

logger = logging.getLogger(__name__)


def get_attendance_chunks():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                a.id AS entity_id,
                u.name AS trainee_name,
                a.office_id,
                c.course_name,
                a.punch_time,
                a.punch,
                a.attendance_type,
                a.status,
                a.remarks
            FROM attendances a
            LEFT JOIN users u ON a.user_id = u.id
            LEFT JOIN courses c ON a.course_id = c.id
            WHERE a.office_id IS NOT NULL
            AND a.user_id IS NOT NULL
            LIMIT 200
        """)

        rows = cursor.fetchall()
        chunks = []

        for row in rows:
            name = row.get("trainee_name") or "Unknown trainee"
            course = row.get("course_name") or "training"
            punch_time = row.get("punch_time") or "N/A"
            punch = row.get("punch") or ""
            attendance_type = row.get("attendance_type") or "1"
            status = row.get("status") or "1"
            remarks = row.get("remarks") or ""

            status_text = "Present" if status == 1 else "Absent" if status == 0 else str(status)
            type_text = "Check In" if attendance_type == 1 else "Check Out" if attendance_type == 2 else str(attendance_type)

            text = f"""
Trainee: {name}
Course: {course}
Punch Time: {punch_time}
Type: {type_text}
Status: {status_text}
Punch: {punch}
Remarks: {remarks}
"""

            chunks.append({
                "text": text,
                "office_id": row.get("office_id"),
                "module": "attendance",
                "allowed_roles": ["principal", "admin", "attendance_staff", "trainer"],
                "entity_id": row.get("entity_id"),
                "entity_type": "attendance",
                "trainee_name": name.lower()
            })

        conn.close()
        return chunks
    except Exception as e:
        logger.warning(f"Attendance sync skipped: {e}")
        return []
