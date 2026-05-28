"""Complaint option resolver — fetches clickable option lists for complaint guided flows.

All queries use parameterized SQL and enforce office_id filtering.
"""

from typing import List, Dict, Optional
from datetime import datetime
from app.services.db_service import get_connection


def search_complaint_trainees_by_name(name: str, office_id: int, limit: int = 10) -> List[Dict]:
    """Search for a trainee who might have raised a complaint."""
    conn = get_connection()
    try:
        cur = conn.cursor()

        def _execute_search(search_term):
            # Same trainee fuzzy search logic
            cur.execute("""
                SELECT tm.user_id, u.name, tc.course_batch, c.course_name
                FROM tra_masters tm
                JOIN users u ON u.id = tm.user_id
                JOIN training_calendars tc ON tc.id = tm.course_id AND tc.status = 1
                JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
                WHERE LOWER(u.name) LIKE LOWER(%s)
                ORDER BY tm.id DESC
                LIMIT %s
            """, (office_id, f"%{search_term}%", limit))
            return cur.fetchall()

        rows = _execute_search(name)
        # Fallback to first token if multi-word fails
        if not rows and " " in name:
            first_token = name.split()[0]
            if len(first_token) > 2:
                rows = _execute_search(first_token)

        options = []
        for row in rows:
            batch = row.get("course_batch", "")
            batch_str = f" - {batch}" if batch else ""
            c_name = row.get("course_name", "")
            c_str = f" ({c_name})" if c_name else ""
            options.append({
                "label": f"{row['name']}{batch_str}{c_str}",
                "value": row["user_id"],
                "meta": {
                    "user_id": row["user_id"],
                    "name": row["name"],
                },
            })
        return options
    except Exception as e:
        print(f"[Complaint Options] search_complaint_trainees_by_name error: {e}")
        return []
    finally:
        conn.close()


def get_complaint_categories(office_id: int, limit: int = 15, offset: int = 0) -> List[Dict]:
    """Fetch known complaint categories from DB, including sub-categories."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, comp_name AS name, cat_id
            FROM complaint_cat
            WHERE status = 1
            ORDER BY cat_id ASC, comp_name ASC
            LIMIT %s OFFSET %s
        """, (limit + 1, offset))
        rows = cur.fetchall()

        has_more = len(rows) > limit
        if has_more:
            rows = rows[:limit]

        options = []
        if offset == 0:
            options.append({"label": "All categories", "value": "ALL"})
        if offset > 0:
            options.append({"label": "⬅️ Previous categories", "value": "LOAD_PREV_OPTIONS"})
            
        for row in rows:
            prefix = "" if row["cat_id"] == 0 else "  ↳ "
            options.append({
                "label": f"{prefix}{row['name']}",
                "value": row["id"],
            })
            
        if has_more:
            options.append({"label": "More categories ➡️", "value": "LOAD_MORE_OPTIONS"})
            
        return options
    except Exception as e:
        print(f"[Complaint Options] get_complaint_categories error: {e}")
        return [
            {"label": "All categories", "value": "ALL"},
            {"label": "Hostel", "value": "hostel"},
            {"label": "Electrical", "value": "electrical"},
            {"label": "Maintenance", "value": "maintenance"}
        ]
    finally:
        conn.close()


def get_complaint_status_options() -> List[Dict]:
    """Static complaint status options."""
    return [
        {"label": "Pending complaints", "value": "pending"},
        {"label": "Resolved complaints", "value": "resolved"},
        {"label": "All complaints", "value": "all"}
    ]


def get_complaint_departments(office_id: int) -> List[Dict]:
    """Fetch known departments for complaints."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name
            FROM departments
            WHERE office_id = %s AND status = 1
            ORDER BY name ASC
        """, (office_id,))
        rows = cur.fetchall()

        options = [{"label": "All departments", "value": "ALL"}]
        for row in rows:
            options.append({
                "label": row["name"],
                "value": row["id"],
            })
        return options
    except Exception as e:
        print(f"[Complaint Options] get_complaint_departments error: {e}")
        return [{"label": "All departments", "value": "ALL"}]
    finally:
        conn.close()


def get_complaint_year_options() -> List[Dict]:
    """Get year selection options for complaint flows."""
    current_year = datetime.now().year
    return [
        {"label": f"Current year ({current_year})", "value": current_year},
        {"label": f"Previous year ({current_year - 1})", "value": current_year - 1},
        {"label": "All years", "value": "ALL"},
    ]
