"""Hostel option resolver — fetches clickable option lists for hostel guided flows.

All queries use parameterized SQL and enforce office_id filtering.
Never exposes password or sensitive columns.
"""

from typing import List, Dict, Optional
from app.services.db_service import get_connection


def search_hostel_trainees_by_name(name: str, office_id: int) -> List[Dict]:
    """Search trainees by partial name match with hostel context.
    Returns label/value pairs with room/building info.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        def _execute_search(search_term):
            cur.execute("""
                SELECT u.id AS user_id, u.name, u.user_code,
                       hb.building_name, hr.room_name, hm.h_status
                FROM users u
                JOIN hostel_masters hm ON hm.user_id = u.id
                JOIN hostel_buildings hb ON hb.id = hm.building_id
                JOIN hostel_rooms hr ON hr.id = hm.room_id
                WHERE LOWER(u.name) LIKE LOWER(%s)
                  AND hm.office_id = %s
                  AND u.status = 1
                ORDER BY hm.h_status DESC, hm.in_date DESC
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
                room_part = f" - Room {row['room_name']}" if row.get("room_name") else ""
                building_part = f" - {row['building_name']}" if row.get("building_name") else ""
                status_part = " [Active]" if row.get("h_status") == 1 else " [Past]"
                seen[uid] = {
                    "label": f"{row['name']}{code_part}{room_part}{building_part}{status_part}",
                    "value": uid,
                    "meta": {
                        "user_id": uid,
                    },
                }
        return list(seen.values())
    except Exception as e:
        print(f"[Hostel Options] search_hostel_trainees_by_name error: {e}")
        return []
    finally:
        conn.close()


def get_hostel_buildings(office_id: int, hostel_type: Optional[str] = None) -> List[Dict]:
    """Get active hostel buildings for an office.
    If hostel_type is gents/ladies, filter by building name containing that keyword.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        sql = """
            SELECT id AS building_id, building_name, bed_capacity
            FROM hostel_buildings
            WHERE office_id = %s AND status = 1
        """
        params = [office_id]

        if hostel_type:
            if hostel_type == "gents":
                sql += " AND (LOWER(building_name) LIKE %s OR LOWER(building_name) LIKE %s)"
                params.extend(["%gents%", "%boys%"])
            elif hostel_type == "ladies":
                sql += " AND (LOWER(building_name) LIKE %s OR LOWER(building_name) LIKE %s)"
                params.extend(["%ladies%", "%girls%"])

        sql += " ORDER BY building_name"
        cur.execute(sql, params)
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
        print(f"[Hostel Options] get_hostel_buildings error: {e}")
        return [{"label": "All buildings", "value": "ALL"}]
    finally:
        conn.close()


def get_rooms_by_number(room_number: str, office_id: int) -> List[Dict]:
    """Get rooms matching a room number. If same number exists in multiple buildings,
    return options for each.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT hr.id AS room_id, hr.room_name, hr.room_beds,
                   hb.id AS building_id, hb.building_name
            FROM hostel_rooms hr
            JOIN hostel_buildings hb ON hb.id = hr.building_id
            WHERE hr.room_name = %s
              AND hr.office_id = %s
              AND hr.status = 1
            ORDER BY hb.building_name
        """, (room_number, office_id))
        rows = cur.fetchall()

        options = []
        for row in rows:
            options.append({
                "label": f"Room {row['room_name']} - {row['building_name']}",
                "value": row["room_id"],
                "meta": {
                    "room_id": row["room_id"],
                    "building_id": row["building_id"],
                },
            })
        return options
    except Exception as e:
        print(f"[Hostel Options] get_rooms_by_number error: {e}")
        return []
    finally:
        conn.close()


def get_hostel_status_options() -> List[Dict]:
    """Static complaint status options."""
    return [
        {"label": "Pending complaints", "value": "pending"},
        {"label": "Resolved complaints", "value": "resolved"},
        {"label": "All complaints", "value": "all"},
    ]


def get_dues_status_options() -> List[Dict]:
    """Static hostel dues status options."""
    return [
        {"label": "Pending dues", "value": "pending"},
        {"label": "Paid dues", "value": "paid"},
        {"label": "All dues", "value": "all"},
    ]


def get_stay_filter_options() -> List[Dict]:
    """Static stay filter options for trainee room lookup."""
    return [
        {"label": "Current stay", "value": "current"},
        {"label": "All stays", "value": "all"},
    ]
