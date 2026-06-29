"""Timetable option resolver — fetches clickable option lists for timetable guided flows.

All queries use parameterized SQL and enforce office_id filtering.
"""

from typing import List, Dict, Optional
from datetime import datetime
from app.services.db_service import get_connection


def search_timetable_courses(course_name: str, office_id: int, limit: int = 10) -> List[Dict]:
    """Search for a course for timetable queries. Only shows courses with timetable data."""
    conn = get_connection()
    try:
        cur = conn.cursor()

        def _execute_search(search_term):
            cur.execute("""
                SELECT tc.id AS course_id, c.course_name, tc.course_batch, tc.from_date, tc.to_date
                FROM training_calendars tc
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                WHERE (LOWER(c.course_name) LIKE LOWER(%s) OR LOWER(tc.course_batch) LIKE LOWER(%s))
                  AND tc.status = 1
                  AND EXISTS (
                      SELECT 1 FROM time_masters tm
                      WHERE tm.course_id = tc.id AND tm.office_id = %s AND tm.status = 1
                  )
                ORDER BY tc.from_date DESC
                LIMIT %s
            """, (office_id, f"%{search_term}%", f"%{search_term}%", office_id, limit))
            return cur.fetchall()

        rows = _execute_search(course_name)
        if not rows and " " in course_name:
            first_token = course_name.split()[0]
            if len(first_token) > 2:
                rows = _execute_search(first_token)

        options = [{"label": "📋 All courses (combined)", "value": "ALL"}]
        for row in rows:
            batch = row.get("course_batch", "")
            batch_str = f" - Batch {batch}" if batch else ""
            d_str = f" ({row['from_date']} to {row['to_date']})"
            options.append({
                "label": f"{row['course_name']}{batch_str}{d_str}",
                "value": row["course_id"],
                "meta": {
                    "course_id": row["course_id"],
                    "course_name": row["course_name"]
                }
            })
        return options
    finally:
        conn.close()


def search_faculty_by_name(name: str, office_id: int, limit: int = 10) -> List[Dict]:
    """Search for faculty members by name."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.id AS user_id, u.name, desi.desi_name
            FROM users u
            LEFT JOIN designations desi ON desi.id = u.desi_id
            WHERE LOWER(u.name) LIKE LOWER(%s) AND u.office_id = %s AND u.status = 1
            ORDER BY u.name ASC
            LIMIT %s
        """, (f"%{name}%", office_id, limit))
        rows = cur.fetchall()

        options = []
        for row in rows:
            desi = f" - {row['desi_name']}" if row['desi_name'] else ""
            options.append({
                "label": f"{row['name']}{desi}",
                "value": row["user_id"]
            })
        return options
    finally:
        conn.close()


def search_subjects_by_name(subject_name: str, office_id: int, limit: int = 10) -> List[Dict]:
    """Search for subjects."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, subject_name
            FROM subjects
            WHERE LOWER(subject_name) LIKE LOWER(%s) AND office_id = %s AND status = 1
            ORDER BY subject_name ASC
            LIMIT %s
        """, (f"%{subject_name}%", office_id, limit))
        rows = cur.fetchall()

        options = []
        for row in rows:
            options.append({
                "label": row["subject_name"],
                "value": row["id"]
            })
        return options
    finally:
        conn.close()


def search_classrooms_by_name(classroom_name: str, office_id: int, limit: int = 10) -> List[Dict]:
    """Search for classrooms."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, class_name
            FROM class_rooms
            WHERE (LOWER(class_name) LIKE LOWER(%s) OR id = %s) AND office_id = %s AND status = 1
            ORDER BY class_name ASC
            LIMIT %s
        """, (f"%{classroom_name}%", classroom_name if classroom_name.isdigit() else 0, office_id, limit))
        rows = cur.fetchall()

        options = []
        for row in rows:
            options.append({
                "label": row["class_name"],
                "value": row["id"]
            })
        return options
    finally:
        conn.close()


def get_sessions(office_id: int) -> List[Dict]:
    """Get predefined session options."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, session AS session_name
            FROM sessions
            WHERE office_id = %s AND status = 1
            ORDER BY id ASC
        """, (office_id,))
        rows = cur.fetchall()

        options = [{"label": "All Sessions", "value": "ALL"}]
        for row in rows:
            options.append({
                "label": row["session_name"],
                "value": row["id"]
            })
        return options
    except:
        return [{"label": "All Sessions", "value": "ALL"}]
    finally:
        conn.close()


def get_recent_timetable_courses(office_id: int, limit: int = 10, offset: int = 0) -> List[Dict]:
    """Get the most recent courses that have timetable data."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT tc.id AS course_id, c.course_name, tc.course_batch, tc.from_date, tc.to_date
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE tc.status = 1
              AND EXISTS (
                  SELECT 1 FROM time_masters tm
                  WHERE tm.course_id = tc.id AND tm.office_id = %s AND tm.status = 1
              )
            ORDER BY tc.from_date DESC
            LIMIT %s OFFSET %s
        """, (office_id, office_id, limit + 1, offset))
        rows = cur.fetchall()

        has_more = len(rows) > limit
        if has_more:
            rows = rows[:limit]

        options = []
        if offset == 0:
            options.append({"label": "📋 All courses (combined)", "value": "ALL"})
        if offset > 0:
            options.append({"label": "⬅️ Previous courses", "value": "LOAD_PREV_OPTIONS"})

        for row in rows:
            batch = row.get("course_batch", "")
            batch_str = f" - Batch {batch}" if batch else ""
            d_str = f" ({row['from_date']} to {row['to_date']})"
            options.append({
                "label": f"{row['course_name']}{batch_str}{d_str}",
                "value": row["course_id"],
                "meta": {
                    "course_id": row["course_id"],
                    "course_name": row["course_name"]
                }
            })

        if has_more:
            options.append({"label": "More courses ➡️", "value": "LOAD_MORE_OPTIONS"})

        return options
    finally:
        conn.close()


def get_timetable_date_options() -> List[Dict]:
    """Get common date selection options."""
    return [
        {"label": "Today", "value": "today"},
        {"label": "Tomorrow", "value": "tomorrow"},
        {"label": "Yesterday", "value": "yesterday"},
        {"label": "Last 7 days", "value": "last_7_days"},
        {"label": "All available records", "value": "ALL"}
    ]
