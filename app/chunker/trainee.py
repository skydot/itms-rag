import logging
from app.services.db_service import get_connection

logger = logging.getLogger(__name__)


def get_trainee_chunks():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                u.id AS entity_id,
                u.name AS trainee_name,
                u.office_id,
                u.email,
                u.mobile AS phone,
                u.permanent_address AS address,
                u.birth_date AS dob,
                u.gender,
                u.designation
            FROM users u
            WHERE u.office_id IS NOT NULL
            AND u.name IS NOT NULL
            LIMIT 200
        """)
        rows = cursor.fetchall()
        chunks = []
        for row in rows:
            name = row.get("trainee_name") or "Unknown trainee"
            email = row.get("email") or "N/A"
            phone = row.get("phone") or "N/A"
            address = row.get("address") or "N/A"
            dob = row.get("dob") or "N/A"
            gender = row.get("gender") or "N/A"
            designation = row.get("designation") or "Trainee"
            
            text = f"""Trainee: {name}
Email: {email}
Phone: {phone}
Address: {address}
DOB: {dob}
Gender: {gender}
Designation: {designation}"""
            
            chunks.append({
                "text": text,
                "office_id": row.get("office_id"),
                "module": "trainee",
                "allowed_roles": ["principal", "admin", "hr_staff", "trainer"],
                "entity_id": row.get("entity_id"),
                "entity_type": "trainee",
                "trainee_name": name.lower()
            })
        conn.close()
        return chunks
    except Exception as e:
        logger.warning(f"Trainee sync skipped: {e}")
        return []
