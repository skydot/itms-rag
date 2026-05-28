"""Faculty / VL option resolver — fetches clickable option lists for faculty guided flows.

All queries use parameterized SQL and enforce office_id filtering.
"""

from typing import List, Dict, Optional
from app.services.db_service import get_connection


def search_faculty_by_name(name: str, office_id: int, limit: int = 10) -> List[Dict]:
    """Search internal faculty (users with instructor/lecturer designations)."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.id AS faculty_id, u.name, u.user_code, desi.desi_name
            FROM users u
            LEFT JOIN designations desi ON desi.id = u.desi_id
            WHERE LOWER(u.name) LIKE LOWER(%s) AND u.office_id = %s AND u.status = 1
            ORDER BY u.name ASC
            LIMIT %s
        """, (f"%{name}%", office_id, limit))
        rows = cur.fetchall()

        options = []
        for row in rows:
            desi = f" - {row['desi_name']}" if row.get("desi_name") else ""
            options.append({
                "label": f"{row['name']}{desi}",
                "value": row["faculty_id"],
                "meta": {"faculty_id": row["faculty_id"], "faculty_type": "internal"}
            })
        return options
    finally:
        conn.close()


def search_vl_by_name(name: str, office_id: int, limit: int = 10) -> List[Dict]:
    """Search visiting lecturers by name."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT vm.id AS vl_mgmt_id, u.id AS user_id, u.name, vm.subject_name
            FROM vl_management vm
            JOIN users u ON u.id = vm.vl_id
            WHERE LOWER(u.name) LIKE LOWER(%s) AND vm.office_id = %s AND vm.status = 1
            ORDER BY u.name ASC
            LIMIT %s
        """, (f"%{name}%", office_id, limit))
        rows = cur.fetchall()

        options = []
        for row in rows:
            subj = f" - {row['subject_name']}" if row.get("subject_name") else ""
            options.append({
                "label": f"{row['name']} (VL){subj}",
                "value": row["user_id"],
                "meta": {"faculty_id": row["user_id"], "vl_mgmt_id": row["vl_mgmt_id"], "faculty_type": "vl"}
            })
        return options
    finally:
        conn.close()


def search_faculty_all(name: str, office_id: int, limit: int = 10) -> List[Dict]:
    """Search both internal faculty and VL by name."""
    internal = search_faculty_by_name(name, office_id, limit)
    vl = search_vl_by_name(name, office_id, limit)
    combined = internal + vl
    return combined[:limit]


def search_faculty_courses(course_name: str, office_id: int, limit: int = 10) -> List[Dict]:
    """Search courses for faculty assignment queries."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT tc.id AS course_id, c.course_name, tc.course_batch, tc.from_date, tc.to_date
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE (LOWER(c.course_name) LIKE LOWER(%s) OR LOWER(tc.course_batch) LIKE LOWER(%s))
              AND tc.status = 1
            ORDER BY tc.from_date DESC
            LIMIT %s
        """, (office_id, f"%{course_name}%", f"%{course_name}%", limit))
        rows = cur.fetchall()

        options = []
        for row in rows:
            batch = f" - Batch {row['course_batch']}" if row.get("course_batch") else ""
            options.append({
                "label": f"{row['course_name']}{batch} ({row['from_date']} to {row['to_date']})",
                "value": row["course_id"],
                "meta": {"course_id": row["course_id"], "course_name": row["course_name"]}
            })
        return options
    finally:
        conn.close()


def search_faculty_subjects(subject_name: str, office_id: int, limit: int = 10) -> List[Dict]:
    """Search subjects for faculty queries."""
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
            options.append({"label": row["subject_name"], "value": row["id"]})
        return options
    finally:
        conn.close()


def get_faculty_type_options() -> List[Dict]:
    """Return faculty type filter options."""
    return [
        {"label": "All faculty", "value": "all"},
        {"label": "Internal faculty", "value": "internal"},
        {"label": "Visiting lecturers", "value": "vl"},
    ]


def get_faculty_date_options() -> List[Dict]:
    """Return common date options."""
    return [
        {"label": "Today", "value": "today"},
        {"label": "Tomorrow", "value": "tomorrow"},
        {"label": "Yesterday", "value": "yesterday"},
        {"label": "Last 7 days", "value": "last_7_days"},
        {"label": "All available records", "value": "ALL"},
    ]


def get_recent_faculty_courses(office_id: int, limit: int = 10) -> List[Dict]:
    """Return recent courses for faculty lookup."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT tc.id AS course_id, c.course_name, tc.course_batch, tc.from_date, tc.to_date
            FROM training_calendars tc
            JOIN courses c ON c.id = tc.ct_id AND c.office_id = %s
            WHERE tc.status = 1
            ORDER BY tc.from_date DESC
            LIMIT %s
        """, (office_id, limit))
        rows = cur.fetchall()

        options = [{"label": "All courses", "value": "ALL"}]
        for row in rows:
            batch = f" - Batch {row['course_batch']}" if row.get("course_batch") else ""
            options.append({
                "label": f"{row['course_name']}{batch} ({row['from_date']})",
                "value": row["course_id"],
                "meta": {"course_id": row["course_id"], "course_name": row["course_name"]}
            })
        return options
    finally:
        conn.close()
