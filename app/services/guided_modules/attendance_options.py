"""Attendance option resolver — fetches clickable option lists for attendance guided flows.

All queries use parameterized SQL and enforce office_id filtering.
Never exposes password or sensitive columns.
"""

from typing import List, Dict
from app.services.db_service import get_connection


def search_attendance_trainees_by_name(name: str, office_id: int) -> List[Dict]:
    """Search trainees by partial name match — only those who HAVE attendance records.
    Returns label/value pairs with course info.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        def _execute_search(search_term):
            cur.execute("""
                SELECT u.id AS user_id, u.name, u.user_code,
                       c.course_name, tc.course_batch, a.course_id,
                       MAX(tc.from_date) AS latest_from
                FROM attendances a
                JOIN users u ON u.id = a.user_id
                JOIN training_calendars tc ON tc.id = a.course_id AND tc.status = 1
                JOIN courses c ON c.id = tc.ct_id
                WHERE LOWER(u.name) LIKE LOWER(%s)
                  AND u.office_id = %s
                  AND u.status = 1
                  AND a.status = 1
                GROUP BY u.id, u.name, u.user_code, c.course_name, tc.course_batch, a.course_id
                ORDER BY latest_from DESC, u.name
                LIMIT 20
            """, (f"%{search_term}%", office_id))
            return cur.fetchall()

        rows = _execute_search(name)
        if not rows and " " in name:
            first_token = name.split()[0]
            if len(first_token) > 2:
                rows = _execute_search(first_token)

        seen = {}
        for row in rows:
            uid = row["user_id"]
            if uid not in seen:
                code_part = f" ({row['user_code']})" if row.get("user_code") else ""
                course_part = f" - {row['course_name']}" if row.get("course_name") else ""
                batch_part = f" {row['course_batch']}" if row.get("course_batch") else ""
                seen[uid] = {
                    "label": f"{row['name']}{code_part}{course_part}{batch_part}",
                    "value": uid,
                    "meta": {
                        "user_id": uid,
                        "course_id": row.get("course_id"),
                    },
                }
        return list(seen.values())
    except Exception as e:
        print(f"[Attendance Options] search_attendance_trainees_by_name error: {e}")
        return []
    finally:
        conn.close()


def get_attendance_courses_for_trainee(user_id: int, office_id: int) -> List[Dict]:
    """Get courses for which a trainee has attendance records.
    Returns [All courses] + course options.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT tc.id AS course_id, c.course_name, tc.course_batch,
                   tc.from_date
            FROM attendances a
            JOIN training_calendars tc ON tc.id = a.course_id AND tc.status = 1
            JOIN courses c ON c.id = tc.ct_id
            JOIN users u ON u.id = a.user_id
            WHERE a.user_id = %s
              AND u.office_id = %s
              AND a.status = 1
            ORDER BY tc.from_date DESC
            LIMIT 20
        """, (user_id, office_id))
        rows = cur.fetchall()

        options = [{"label": "All courses", "value": "ALL"}]
        for row in rows:
            batch = f" {row['course_batch']}" if row.get("course_batch") else ""
            date_part = f" - {row['from_date']}" if row.get("from_date") else ""
            options.append({
                "label": f"{row['course_name']}{batch}{date_part}",
                "value": row["course_id"],
            })
        return options
    except Exception as e:
        print(f"[Attendance Options] get_attendance_courses_for_trainee error: {e}")
        return [{"label": "All courses", "value": "ALL"}]
    finally:
        conn.close()


def get_recent_attendance_courses(office_id: int, limit: int = 10) -> List[Dict]:
    """Get recent training calendar courses that have attendance records.
    Returns [All courses] + course options.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT tc.id AS course_id, c.course_name, tc.course_batch,
                   tc.from_date
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            JOIN attendances a ON a.course_id = tc.id AND a.status = 1
            WHERE tc.status = 1
            ORDER BY tc.from_date DESC
            LIMIT %s
        """, (office_id, limit))
        rows = cur.fetchall()

        options = [{"label": "All courses", "value": "ALL"}]
        for row in rows:
            batch = f" {row['course_batch']}" if row.get("course_batch") else ""
            date_part = f" - {row['from_date']}" if row.get("from_date") else ""
            options.append({
                "label": f"{row['course_name']}{batch}{date_part}",
                "value": row["course_id"],
            })
        return options
    except Exception as e:
        print(f"[Attendance Options] get_recent_attendance_courses error: {e}")
        return [{"label": "All courses", "value": "ALL"}]
    finally:
        conn.close()


def get_attendance_threshold_options() -> List[Dict]:
    """Static threshold options for low attendance detection."""
    return [
        {"label": "Below 75%", "value": 75},
        {"label": "Below 80%", "value": 80},
        {"label": "Below 90%", "value": 90},
    ]


def get_date_range_options() -> List[Dict]:
    """Static date range options."""
    return [
        {"label": "Today", "value": "today"},
        {"label": "Yesterday", "value": "yesterday"},
        {"label": "Last 7 days", "value": "last_7_days"},
        {"label": "Last 30 days", "value": "last_30_days"},
        {"label": "All available records", "value": "ALL"},
    ]
