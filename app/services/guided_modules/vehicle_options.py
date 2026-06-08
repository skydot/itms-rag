from app.services.db_service import get_connection


def search_vehicles_by_number(vehicle_number: str, office_id: int, limit: int = 10) -> list[dict]:
    """Search vehicle_registers by bus_num, study_tour by bus_num, field_training by car_number."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        like_num = f"%{vehicle_number}%"
        # Search in vehicle_registers
        query = """
            SELECT DISTINCT vr.bus_num AS vehicle_number, 'register' AS source, vr.id
            FROM vehicle_registers vr
            WHERE vr.status = 1 AND vr.bus_num LIKE %s
            LIMIT %s
        """
        cur.execute(query, (like_num, limit))
        rows = cur.fetchall()

        options = []
        seen = set()
        for r in rows:
            vnum = r["vehicle_number"]
            if vnum and vnum not in seen:
                seen.add(vnum)
                options.append({
                    "label": f"{vnum} (Register)",
                    "value": r["id"],
                    "meta": {"vehicle_number": vnum, "source": "register"}
                })

        # Also search study_tour bus_num
        query2 = """
            SELECT DISTINCT st.bus_num AS vehicle_number, st.id
            FROM study_tour st
            WHERE st.status = 1 AND st.bus_num LIKE %s AND st.bus_num != ''
            LIMIT %s
        """
        cur.execute(query2, (like_num, limit))
        for r in cur.fetchall():
            vnum = r["vehicle_number"]
            if vnum and vnum not in seen:
                seen.add(vnum)
                options.append({
                    "label": f"{vnum} (Study Tour)",
                    "value": r["id"],
                    "meta": {"vehicle_number": vnum, "source": "study_tour"}
                })

        # Also search field_training car_number
        query3 = """
            SELECT DISTINCT ft.car_number AS vehicle_number, ft.id
            FROM field_training ft
            WHERE ft.status = 1 AND ft.car_number LIKE %s AND ft.car_number != ''
            LIMIT %s
        """
        cur.execute(query3, (like_num, limit))
        for r in cur.fetchall():
            vnum = r["vehicle_number"]
            if vnum and vnum not in seen:
                seen.add(vnum)
                options.append({
                    "label": f"{vnum} (Field Training)",
                    "value": r["id"],
                    "meta": {"vehicle_number": vnum, "source": "field_training"}
                })

        return options[:limit]
    finally:
        conn.close()


def search_vehicle_drivers(driver_name: str, office_id: int, limit: int = 10) -> list[dict]:
    """Search unique driver names from vehicle_registers."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        like_name = f"%{driver_name}%"
        query = """
            SELECT DISTINCT vr.driver_name
            FROM vehicle_registers vr
            WHERE vr.status = 1 AND vr.driver_name LIKE %s AND vr.driver_name != ''
            LIMIT %s
        """
        cur.execute(query, (like_name, limit))
        rows = cur.fetchall()

        options = []
        for i, r in enumerate(rows, 1):
            dname = r["driver_name"]
            options.append({
                "label": dname,
                "value": dname,
                "meta": {"driver_name": dname}
            })
        return options
    finally:
        conn.close()


def search_vehicle_courses(course_name: str, office_id: int, limit: int = 10) -> list[dict]:
    """Search courses that have study_tour or field_training records."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        like_name = f"%{course_name}%"
        query = """
            SELECT tc.id, tc.course_batch
            FROM training_calendars tc
            WHERE tc.status = 1 AND tc.course_batch LIKE %s
            AND (
                EXISTS (SELECT 1 FROM study_tour st WHERE FIND_IN_SET(tc.id, st.course_id) AND st.status = 1)
                OR EXISTS (SELECT 1 FROM field_training ft WHERE FIND_IN_SET(tc.id, ft.course_id) AND ft.status = 1)
            )
            LIMIT %s
        """
        cur.execute(query, (like_name, limit))
        rows = cur.fetchall()

        options = []
        for r in rows:
            options.append({
                "label": r["course_batch"],
                "value": r["id"],
                "meta": {"course_id": r["id"]}
            })
        return options
    finally:
        conn.close()


def search_study_tours(tour_name: str, office_id: int, limit: int = 10) -> list[dict]:
    """Search study tours."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT st.id, st.from_where, st.to_where, st.from_date, st.return_date
            FROM study_tour st
            WHERE st.status = 1
            ORDER BY st.from_date DESC
            LIMIT %s
        """
        cur.execute(query, (limit,))
        rows = cur.fetchall()

        options = []
        for r in rows:
            from_place = r["from_where"] or "?"
            to_place = r["to_where"] or "?"
            from_date = r["from_date"].strftime("%Y-%m-%d") if r["from_date"] else "?"
            label = f"{from_place} → {to_place} ({from_date})"
            options.append({
                "label": label,
                "value": r["id"],
                "meta": {"tour_id": r["id"]}
            })
        return options
    finally:
        conn.close()


def get_vehicle_type_options(office_id: int) -> list[dict]:
    """Return static vehicle type options (no lookup table exists)."""
    return [
        {"label": "Bus", "value": "bus", "meta": {"vehicle_type": "bus"}},
        {"label": "Car", "value": "car", "meta": {"vehicle_type": "car"}},
        {"label": "Jeep", "value": "jeep", "meta": {"vehicle_type": "jeep"}},
        {"label": "Van", "value": "van", "meta": {"vehicle_type": "van"}},
        {"label": "Truck", "value": "truck", "meta": {"vehicle_type": "truck"}},
    ]


def get_vehicle_status_options() -> list[dict]:
    """Return vehicle booking status options (v_status codes)."""
    return [
        {"label": "Pending", "value": "pending", "meta": {"status": "pending"}},
        {"label": "Approved", "value": "approved", "meta": {"status": "approved"}},
        {"label": "Completed", "value": "completed", "meta": {"status": "completed"}},
        {"label": "Rejected", "value": "rejected", "meta": {"status": "rejected"}},
    ]
