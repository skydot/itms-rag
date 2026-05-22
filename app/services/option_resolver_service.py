"""Option resolver — fetches clickable option lists from MySQL for guided flows.

All queries use parameterized SQL and enforce office_id filtering.
Never exposes password or sensitive columns.
"""

from typing import List, Dict
from app.services.db_service import get_connection


def search_trainees_by_name(name: str, office_id: int) -> List[Dict]:
    """Search trainees by partial name match. Returns label/value pairs."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT u.id AS user_id, u.name, u.user_code,
                   c.course_name, tc.course_batch
            FROM users u
            JOIN tra_masters tm ON tm.user_id = u.id AND tm.status = 1
            JOIN training_calendars tc ON tc.id = tm.course_id AND tc.status = 1
            JOIN courses c ON c.id = tc.ct_id
            WHERE LOWER(u.name) LIKE LOWER(%s)
              AND u.office_id = %s
              AND u.status = 1
            ORDER BY u.name
            LIMIT 20
        """, (f"%{name}%", office_id))
        rows = cur.fetchall()

        # Deduplicate by user_id (a trainee may appear in multiple courses)
        seen = {}
        for row in rows:
            uid = row["user_id"]
            if uid not in seen:
                code_part = f" ({row['user_code']})" if row.get("user_code") else ""
                course_part = f" - {row['course_name']}" if row.get("course_name") else ""
                batch_part = f" Batch {row['course_batch']}" if row.get("course_batch") else ""
                seen[uid] = {
                    "label": f"{row['name']}{code_part}{course_part}{batch_part}",
                    "value": uid,
                }
        return list(seen.values())
    except Exception as e:
        print(f"[OptionResolver] search_trainees_by_name error: {e}")
        return []
    finally:
        conn.close()


def get_courses_for_trainee(user_id: int, office_id: int) -> List[Dict]:
    """Get courses/batches a trainee is enrolled in."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT tc.id AS course_id, c.course_name, tc.course_batch,
                   tc.from_date, tc.to_date
            FROM tra_masters tm
            JOIN training_calendars tc ON tc.id = tm.course_id AND tc.status = 1
            JOIN courses c ON c.id = tc.ct_id
            WHERE tm.user_id = %s
              AND tm.office_id = %s
              AND tm.status = 1
            ORDER BY tc.from_date DESC
        """, (user_id, office_id))
        rows = cur.fetchall()

        options = [{"label": "All courses", "value": "ALL"}]
        for row in rows:
            batch = f" (Batch {row['course_batch']})" if row.get("course_batch") else ""
            options.append({
                "label": f"{row['course_name']}{batch}",
                "value": row["course_id"],
            })
        return options
    except Exception as e:
        print(f"[OptionResolver] get_courses_for_trainee error: {e}")
        return [{"label": "All courses", "value": "ALL"}]
    finally:
        conn.close()


def get_exam_types_for_trainee_course(user_id: int, course_id, office_id: int) -> List[Dict]:
    """Get exam types for a trainee's course."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        if course_id == "ALL":
            cur.execute("""
                SELECT DISTINCT et.id AS exam_type_id, et.title
                FROM exam_marks em
                JOIN exam_type et ON et.id = em.exam_type_id AND et.status = 1
                JOIN training_calendars tc ON tc.id = em.course_id
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                WHERE em.user_id = %s AND em.status = 1
                ORDER BY et.title
            """, (office_id, user_id))
        else:
            cur.execute("""
                SELECT DISTINCT et.id AS exam_type_id, et.title
                FROM exam_marks em
                JOIN exam_type et ON et.id = em.exam_type_id AND et.status = 1
                JOIN training_calendars tc ON tc.id = em.course_id
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                WHERE em.user_id = %s AND em.course_id = %s AND em.status = 1
                ORDER BY et.title
            """, (office_id, user_id, course_id))
        rows = cur.fetchall()

        if len(rows) <= 1:
            return []  # No need to ask if only 0 or 1 exam type

        options = [{"label": "All exams", "value": "ALL"}]
        for row in rows:
            options.append({
                "label": row["title"],
                "value": row["exam_type_id"],
            })
        return options
    except Exception as e:
        print(f"[OptionResolver] get_exam_types_for_trainee_course error: {e}")
        return []
    finally:
        conn.close()


def get_recent_courses_for_exam(office_id: int, limit: int = 10) -> List[Dict]:
    """Get recent courses/batches that have exam marks. For non-trainee exam flows."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT tc.id AS course_id, c.course_name, tc.course_batch,
                   tc.from_date
            FROM exam_marks em
            JOIN training_calendars tc ON tc.id = em.course_id AND tc.status = 1
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE em.status = 1
            ORDER BY tc.from_date DESC
            LIMIT %s
        """, (office_id, limit))
        rows = cur.fetchall()

        options = [{"label": "All courses", "value": "ALL"}]
        for row in rows:
            batch = f" (Batch {row['course_batch']})" if row.get("course_batch") else ""
            options.append({
                "label": f"{row['course_name']}{batch}",
                "value": row["course_id"],
            })
        return options
    except Exception as e:
        print(f"[OptionResolver] get_recent_courses_for_exam error: {e}")
        return [{"label": "All courses", "value": "ALL"}]
    finally:
        conn.close()


def get_exam_types_for_course(course_id, office_id: int) -> List[Dict]:
    """Get exam types for a specific course (not trainee-specific)."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        if course_id == "ALL":
            cur.execute("""
                SELECT DISTINCT et.id AS exam_type_id, et.title
                FROM exam_marks em
                JOIN exam_type et ON et.id = em.exam_type_id AND et.status = 1
                JOIN training_calendars tc ON tc.id = em.course_id
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                WHERE em.status = 1
                ORDER BY et.title
            """, (office_id,))
        else:
            cur.execute("""
                SELECT DISTINCT et.id AS exam_type_id, et.title
                FROM exam_marks em
                JOIN exam_type et ON et.id = em.exam_type_id AND et.status = 1
                JOIN training_calendars tc ON tc.id = em.course_id
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                WHERE em.course_id = %s AND em.status = 1
                ORDER BY et.title
            """, (office_id, course_id))
        rows = cur.fetchall()

        if len(rows) <= 1:
            return []

        options = [{"label": "All exams", "value": "ALL"}]
        for row in rows:
            options.append({
                "label": row["title"],
                "value": row["exam_type_id"],
            })
        return options
    except Exception as e:
        print(f"[OptionResolver] get_exam_types_for_course error: {e}")
        return []
    finally:
        conn.close()


def get_subjects_for_course(course_id, office_id: int) -> List[Dict]:
    """Get subjects that have exam marks for a course."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        if course_id == "ALL":
            cur.execute("""
                SELECT DISTINCT s.id AS subject_id, s.subject_name
                FROM exam_marks em
                JOIN subjects s ON s.id = em.subject_id AND s.status = 1
                JOIN training_calendars tc ON tc.id = em.course_id
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                WHERE em.status = 1
                ORDER BY s.subject_name
            """, (office_id,))
        else:
            cur.execute("""
                SELECT DISTINCT s.id AS subject_id, s.subject_name
                FROM exam_marks em
                JOIN subjects s ON s.id = em.subject_id AND s.status = 1
                JOIN training_calendars tc ON tc.id = em.course_id
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                WHERE em.course_id = %s AND em.status = 1
                ORDER BY s.subject_name
            """, (office_id, course_id))
        rows = cur.fetchall()

        if len(rows) <= 1:
            return []

        options = [{"label": "All subjects", "value": "ALL"}]
        for row in rows:
            options.append({
                "label": row["subject_name"],
                "value": row["subject_id"],
            })
        return options
    except Exception as e:
        print(f"[OptionResolver] get_subjects_for_course error: {e}")
        return []
    finally:
        conn.close()


def resolve_latest_exam_type(user_id: int = None, course_id=None, office_id: int = 1):
    """Resolve the latest exam_type_id based on most recent exam_marks."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT em.exam_type_id, et.title, MAX(em.created_at) AS latest
            FROM exam_marks em
            JOIN exam_type et ON et.id = em.exam_type_id AND et.status = 1
            JOIN training_calendars tc ON tc.id = em.course_id
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE em.status = 1
        """
        params = [office_id]
        if user_id:
            sql += " AND em.user_id = %s"
            params.append(user_id)
        if course_id and course_id != "ALL":
            sql += " AND em.course_id = %s"
            params.append(course_id)
        sql += " GROUP BY em.exam_type_id, et.title ORDER BY latest DESC LIMIT 1"
        cur.execute(sql, params)
        row = cur.fetchone()
        if row:
            return row["exam_type_id"]
        return None
    except Exception as e:
        print(f"[OptionResolver] resolve_latest_exam_type error: {e}")
        return None
    finally:
        conn.close()


def get_dues_type_options() -> List[Dict]:
    """Static dues type options."""
    return [
        {"label": "All pending dues", "value": "ALL"},
        {"label": "Hostel dues", "value": "hostel"},
        {"label": "Mess dues", "value": "mess"},
        {"label": "Library dues", "value": "library"},
    ]


def get_hostel_records_for_trainee(user_id: int, office_id: int) -> List[Dict]:
    """Get hostel stay records for a trainee."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT hm.id, hb.building_name, hr.room_name, hm.in_date, hm.out_date,
                   hm.h_status
            FROM hostel_masters hm
            JOIN hostel_buildings hb ON hb.id = hm.building_id
            JOIN hostel_rooms hr ON hr.id = hm.room_id
            WHERE hm.user_id = %s
              AND hm.office_id = %s
              AND hm.status = 1
            ORDER BY hm.in_date DESC
            LIMIT 10
        """, (user_id, office_id))
        rows = cur.fetchall()

        options = []
        current_count = 0
        for row in rows:
            is_current = (row.get("h_status") == 1 or str(row.get("h_status")) == "1")
            if is_current:
                current_count += 1

        if current_count >= 1 and len(rows) > 1:
            options.append({"label": "Current stay", "value": "current"})
            options.append({"label": "All stays", "value": "ALL"})
        return options
    except Exception as e:
        print(f"[OptionResolver] get_hostel_records_for_trainee error: {e}")
        return []
    finally:
        conn.close()


def get_buildings(office_id: int) -> List[Dict]:
    """Get active hostel buildings for an office."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id AS building_id, building_name, bed_capacity
            FROM hostel_buildings
            WHERE office_id = %s AND status = 1
            ORDER BY building_name
        """, (office_id,))
        rows = cur.fetchall()

        options = [{"label": "All buildings", "value": "ALL"}]
        for row in rows:
            cap = f" ({row['bed_capacity']} beds)" if row.get("bed_capacity") else ""
            options.append({
                "label": f"{row['building_name']}{cap}",
                "value": row["building_id"],
            })
        return options
    except Exception as e:
        print(f"[OptionResolver] get_buildings error: {e}")
        return [{"label": "All buildings", "value": "ALL"}]
    finally:
        conn.close()
