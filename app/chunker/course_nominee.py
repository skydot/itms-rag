import logging
from app.services.db_service import get_connection

logger = logging.getLogger(__name__)


def get_course_nominee_chunks():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                cn.id AS entity_id,
                cn.nominee AS trainee_name,
                cn.office_id,
                cn.ct_id AS course_id,
                cn.created_at AS nomination_date,
                cn.status
            FROM courses_nominee cn
            WHERE cn.office_id IS NOT NULL AND cn.nominee IS NOT NULL
            LIMIT 200
        """)
        rows = cursor.fetchall()
        chunks = []
        for row in rows:
            name = row.get("trainee_name") or "Unknown trainee"
            course_id = row.get("course_id") or "N/A"
            nomination_date = row.get("nomination_date") or "N/A"
            status = row.get("status") or 1
            status_text = "Approved" if status == 1 else "Pending"
            
            text = f"""Trainee: {name}
Course ID: {course_id}
Nomination Date: {nomination_date}
Status: {status_text}"""
            
            chunks.append({
                "text": text,
                "office_id": row.get("office_id"),
                "module": "course_nominee",
                "allowed_roles": ["principal", "admin", "training_staff", "trainer"],
                "entity_id": row.get("entity_id"),
                "entity_type": "course_nominee",
                "trainee_name": name.lower()
            })
        conn.close()
        return chunks
    except Exception as e:
        logger.warning(f"Course nominee sync skipped: {e}")
        return []
