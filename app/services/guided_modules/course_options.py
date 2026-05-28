"""Course option resolver — fetches clickable option lists for course guided flows.

All queries use parameterized SQL and enforce office_id filtering.
Never exposes password or sensitive columns.
"""

from datetime import datetime
from typing import List, Dict, Optional
from app.services.db_service import get_connection


def search_courses_by_name(course_name: str, office_id: int, limit: int = 10) -> List[Dict]:
    """Search courses by partial name match. Returns label/value pairs with meta."""
    conn = get_connection()
    try:
        cur = conn.cursor()

        def _execute_search(search_term):
            cur.execute("""
                SELECT tc.id AS course_id, c.course_name, tc.course_batch,
                       tc.from_date, tc.to_date
                FROM training_calendars tc
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                WHERE (LOWER(c.course_name) LIKE LOWER(%s) OR LOWER(tc.course_batch) LIKE LOWER(%s))
                  AND tc.status = 1
                ORDER BY tc.from_date DESC
                LIMIT %s
            """, (office_id, f"%{search_term}%", f"%{search_term}%", limit))
            return cur.fetchall()

        rows = _execute_search(course_name)
        # Fallback: try first token if multi-word search fails
        if not rows and " " in course_name:
            first_token = course_name.split()[0]
            if len(first_token) > 2:
                rows = _execute_search(first_token)

        options = []
        for row in rows:
            batch = f" - Batch {row['course_batch']}" if row.get("course_batch") else ""
            from_dt = f" - {row['from_date']}" if row.get("from_date") else ""
            to_dt = f" to {row['to_date']}" if row.get("to_date") else ""
            options.append({
                "label": f"{row['course_name']}{batch}{from_dt}{to_dt}",
                "value": row["course_id"],
                "meta": {
                    "course_id": row["course_id"],
                    "course_name": row["course_name"],
                },
            })
        return options
    except Exception as e:
        print(f"[Course Options] search_courses_by_name error: {e}")
        return []
    finally:
        conn.close()


def get_recent_courses_for_course_module(office_id: int, limit: int = 10, offset: int = 0) -> List[Dict]:
    """Get recent training calendar courses for course module selection."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT tc.id AS course_id, c.course_name, tc.course_batch,
                   tc.from_date
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE tc.status = 1
            ORDER BY tc.from_date DESC
            LIMIT %s OFFSET %s
        """, (office_id, limit + 1, offset))
        rows = cur.fetchall()

        has_more = len(rows) > limit
        if has_more:
            rows = rows[:limit]

        options = []
        if offset == 0:
            options.append({"label": "All courses", "value": "ALL"})
        if offset > 0:
            options.append({"label": "⬅️ Previous courses", "value": "LOAD_PREV_OPTIONS"})

        for row in rows:
            batch = f" {row['course_batch']}" if row.get("course_batch") else ""
            date_part = f" - {row['from_date']}" if row.get("from_date") else ""
            options.append({
                "label": f"{row['course_name']}{batch}{date_part}",
                "value": row["course_id"],
            })
            
        if has_more:
            options.append({"label": "More courses ➡️", "value": "LOAD_MORE_OPTIONS"})
            
        return options
    except Exception as e:
        print(f"[Course Options] get_recent_courses_for_course_module error: {e}")
        return [{"label": "All courses", "value": "ALL"}]
    finally:
        conn.close()


def get_current_courses(office_id: int) -> List[Dict]:
    """Get currently ongoing courses (from_date <= today AND to_date >= today)."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT tc.id AS course_id, c.course_name, tc.course_batch,
                   tc.from_date, tc.to_date
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE tc.status = 1
              AND tc.from_date <= CURDATE()
              AND tc.to_date >= CURDATE()
            ORDER BY tc.from_date DESC
        """, (office_id,))
        rows = cur.fetchall()

        options = []
        for row in rows:
            batch = f" - Batch {row['course_batch']}" if row.get("course_batch") else ""
            from_dt = f" - {row['from_date']}" if row.get("from_date") else ""
            to_dt = f" to {row['to_date']}" if row.get("to_date") else ""
            options.append({
                "label": f"{row['course_name']}{batch}{from_dt}{to_dt}",
                "value": row["course_id"],
                "meta": {
                    "course_id": row["course_id"],
                    "course_name": row["course_name"],
                },
            })
        return options
    except Exception as e:
        print(f"[Course Options] get_current_courses error: {e}")
        return []
    finally:
        conn.close()


def get_course_status_options() -> List[Dict]:
    """Static course status filter options."""
    return [
        {"label": "Current courses", "value": "current"},
        {"label": "Upcoming courses", "value": "upcoming"},
        {"label": "Completed courses", "value": "completed"},
        {"label": "All courses", "value": "all"},
    ]


def get_course_year_options() -> List[Dict]:
    """Get year selection options for course flows."""
    current_year = datetime.now().year
    return [
        {"label": f"Current year ({current_year})", "value": current_year},
        {"label": f"Previous year ({current_year - 1})", "value": current_year - 1},
        {"label": "All years", "value": "ALL"},
    ]
