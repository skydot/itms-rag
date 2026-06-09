"""Trainee option resolver — fetches clickable option lists for trainee guided flows.

All queries use parameterized SQL and enforce office_id filtering.
Never exposes password or sensitive columns.
"""

from datetime import datetime
from typing import List, Dict
from app.services.db_service import get_connection


def search_trainees_by_name(name: str, office_id: int) -> List[Dict]:
    """Search trainees by partial name match. Returns label/value pairs with meta."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        def _execute_search(search_term):
            cur.execute("""
                SELECT DISTINCT u.id AS user_id, u.name, u.user_code,
                       c.course_name, tc.course_batch, tc.id AS course_id
                FROM users u
                JOIN tra_masters tm ON tm.user_id = u.id AND tm.status = 1
                JOIN training_calendars tc ON tc.id = tm.course_id AND tc.status = 1
                JOIN courses c ON c.id = tc.ct_id
                WHERE LOWER(u.name) LIKE LOWER(%s)
                  AND u.office_id = %s
                  AND u.status = 1
                ORDER BY u.name
                LIMIT 1000
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
        print(f"[Trainee Options] search_trainees_by_name error: {e}")
        return []
    finally:
        conn.close()


def get_recent_trainee_courses(office_id: int, limit: int = 10, offset: int = 0) -> List[Dict]:
    """Get recent training calendar courses for trainee module."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT tc.id AS course_id, c.course_name, tc.course_batch,
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
            options.append({"label": "All recent courses", "value": "ALL"})
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
        print(f"[Trainee Options] get_recent_trainee_courses error: {e}")
        return [{"label": "All recent courses", "value": "ALL"}]
    finally:
        conn.close()


def get_year_options() -> List[Dict]:
    """Get year selection options for trainee flows."""
    current_year = datetime.now().year
    return [
        {"label": f"Current year ({current_year})", "value": current_year},
        {"label": f"Previous year ({current_year - 1})", "value": current_year - 1},
        {"label": "All years", "value": "ALL"},
    ]


def get_courses_for_trainee_module(office_id: int, limit: int = 20, offset: int = 0) -> List[Dict]:
    """Get courses for trainee module selection (not trainee-specific)."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.id AS course_id, c.course_name
            FROM courses c
            WHERE c.office_id = %s AND c.status = 1
            ORDER BY c.course_name
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
            options.append({
                "label": row['course_name'],
                "value": row["course_id"],
            })
            
        if has_more:
            options.append({"label": "More courses ➡️", "value": "LOAD_MORE_OPTIONS"})
            
        return options
    except Exception as e:
        print(f"[Trainee Options] get_courses_for_trainee_module error: {e}")
        return [{"label": "All courses", "value": "ALL"}]
    finally:
        conn.close()
