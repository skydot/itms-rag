import os
import logging
from app.services.db_service import get_connection
from app.services.report_service import generate_report
from app.services.response_mode_service import detect_response_mode


# ── v_status code mapping (vehicle_masters) ──
_V_STATUS_MAP = {0: "Pending", 2: "Approved", 3: "Rejected", 4: "Completed"}


def _build_response(rows: list, question: str, module: str, office_id: int, session_id: str, base_url: str, force_report: bool = False, force_chat: bool = False) -> dict:
    row_count = len(rows)
    if force_report:
        response_mode = "report"
    elif force_chat:
        response_mode = "chat"
    else:
        response_mode = detect_response_mode(question, result_type=module, row_count=row_count)

    if response_mode == "report":
        if row_count == 0:
            return {"type": "text", "message": "No matching records found."}
        report = generate_report(
            module_name=module,
            title="Vehicle Report",
            user_question=question,
            rows=rows,
            office_id=office_id,
            session_id=session_id
        )
        report_url = base_url.rstrip("/") + report["url"]
        ttl = report["ttl_seconds"]
        if ttl < 60:
            exp = f"{ttl} seconds"
        elif ttl < 3600:
            exp = f"{ttl // 60} minute{'s' if ttl // 60 != 1 else ''}"
        else:
            exp = f"{ttl // 3600} hour{'s' if ttl // 3600 != 1 else ''}"

        msg = f"Found {row_count} records for your request.\nOpen full report: {report_url}\nThis report link will expire in {exp}."
        return {
            "type": "text",
            "message": msg,
            "report_url": report_url,
            "row_count": row_count,
            "response_mode": "report"
        }
    else:
        if row_count == 0:
            return {"type": "text", "message": "No matching records found."}
        from app.services.llm_service import format_answer
        formatted_text = ""
        for r in rows:
            for k, v in r.items():
                formatted_text += f"{k}: {v}, "
            formatted_text += "\n"

        answer = format_answer(question, formatted_text)
        return {"type": "text", "message": answer}


def execute_vehicle_guided_query(flow_id: str, slots: dict, office_id: int, role: str, session_id: str = None, user_question: str = "", base_url: str = os.getenv("API_BASE_URL", "")) -> dict:
    """Route to the correct vehicle executor."""
    try:
        print(f"[Vehicle Guided] Executing: {flow_id}")
        print(f"[Vehicle Guided] Slots: {slots}")
        if flow_id == "vehicle_list":
            return _exec_vehicle_list(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "vehicle_availability":
            return _exec_vehicle_availability(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "vehicle_usage_summary":
            return _exec_vehicle_usage_summary(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "vehicle_register_history":
            return _exec_vehicle_register_history(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "study_tour_vehicle_usage":
            return _exec_study_tour_vehicle_usage(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "field_training_vehicle_usage":
            return _exec_field_training_vehicle_usage(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "vehicle_by_driver":
            return _exec_vehicle_by_driver(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "vehicle_count":
            return _exec_vehicle_count(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "vehicle_maintenance":
            return _exec_vehicle_maintenance(slots, office_id, user_question, session_id, base_url)
        elif flow_id == "recent_vehicle_activity":
            return _exec_recent_vehicle_activity(slots, office_id, user_question, session_id, base_url)
        else:
            return {"type": "text", "message": "Vehicle flow not recognized."}
    except Exception as e:
        logging.error(f"[Vehicle Guided] Error executing {flow_id}: {e}")
        return {"type": "text", "message": f"Error retrieving vehicle data: {str(e)}"}


# ═══════════════════════════════════════════════
# Flow Executors
# ═══════════════════════════════════════════════


def _exec_vehicle_list(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    """List all vehicle bookings from vehicle_masters."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT vm.id, vm.name AS requester_name, vm.from_place, vm.to_place,
                   vm.from_date, vm.to_date, vm.kilometer,
                   vm.booking_for, vm.travel_by, vm.reason,
                   CASE vm.v_status
                       WHEN 0 THEN 'Pending'
                       WHEN 2 THEN 'Approved'
                       WHEN 3 THEN 'Rejected'
                       WHEN 4 THEN 'Completed'
                       ELSE 'Unknown'
                   END AS booking_status
            FROM vehicle_masters vm
            WHERE vm.status = 1
        """
        params = []

        status = slots.get("status")
        if status:
            status_code = {"pending": 0, "approved": 2, "rejected": 3, "completed": 4}.get(status.lower())
            if status_code is not None:
                query += " AND vm.v_status = %s"
                params.append(status_code)

        query += " ORDER BY vm.from_date DESC LIMIT 200"
        cur.execute(query, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "vehicle", office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_vehicle_availability(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    """Check vehicle availability based on bookings for a date."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        # Resolve date
        date_val = slots.get("date") or "today"
        if date_val == "today":
            date_expr = "CURDATE()"
        elif date_val == "tomorrow":
            date_expr = "CURDATE() + INTERVAL 1 DAY"
        elif date_val == "yesterday":
            date_expr = "CURDATE() - INTERVAL 1 DAY"
        else:
            date_expr = "%s"

        # Show bookings for this date with their status
        query = f"""
            SELECT vm.id, vm.name AS requester_name, vm.from_place, vm.to_place,
                   vm.from_date, vm.to_date,
                   vm.booking_for, vm.travel_by,
                   CASE vm.v_status
                       WHEN 0 THEN 'Pending'
                       WHEN 2 THEN 'Approved'
                       WHEN 3 THEN 'Rejected'
                       WHEN 4 THEN 'Completed'
                       ELSE 'Unknown'
                   END AS booking_status
            FROM vehicle_masters vm
            WHERE vm.status = 1
            AND DATE(vm.from_date) <= {date_expr}
            AND (vm.to_date IS NULL OR DATE(vm.to_date) >= {date_expr})
            ORDER BY vm.from_date
        """
        params = []
        if date_val not in ("today", "tomorrow", "yesterday"):
            params = [date_val, date_val]

        cur.execute(query, params)
        rows = cur.fetchall()

        if not rows:
            return {"type": "text", "message": f"No vehicle bookings found for {date_val}. All vehicles may be available."}

        return _build_response(rows, question, "vehicle", office_id, session_id, base_url, force_chat=True)
    except Exception as e:
        logging.error(f"Error in _exec_vehicle_availability: {e}")
        return {"type": "text", "message": "Could not check vehicle availability."}
    finally:
        conn.close()


def _exec_vehicle_usage_summary(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    """Summarize vehicle usage by bus number from vehicle_registers."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT vr.bus_num AS vehicle_number,
                   COUNT(*) AS trip_count,
                   SUM(vr.km_total) AS total_km,
                   SUM(vr.total_trainee) AS total_trainees_transported,
                   MIN(vr.from_date) AS first_trip,
                   MAX(vr.from_date) AS last_trip
            FROM vehicle_registers vr
            WHERE vr.status = 1 AND vr.bus_num IS NOT NULL AND vr.bus_num != ''
            GROUP BY vr.bus_num
            ORDER BY trip_count DESC
        """
        cur.execute(query)
        rows = cur.fetchall()

        # Also add study tour bus usage
        query2 = """
            SELECT st.bus_num AS vehicle_number,
                   COUNT(*) AS trip_count,
                   0 AS total_km,
                   SUM(st.total_trainee) AS total_trainees_transported,
                   MIN(st.from_date) AS first_trip,
                   MAX(st.from_date) AS last_trip
            FROM study_tour st
            WHERE st.status = 1 AND st.bus_num IS NOT NULL AND st.bus_num != ''
            GROUP BY st.bus_num
        """
        cur.execute(query2)
        st_rows = cur.fetchall()

        # Merge
        combined = {}
        for r in rows:
            vn = r["vehicle_number"]
            combined[vn] = r
        for r in st_rows:
            vn = r["vehicle_number"]
            if vn in combined:
                combined[vn]["trip_count"] += r["trip_count"]
                combined[vn]["total_trainees_transported"] = (combined[vn]["total_trainees_transported"] or 0) + (r["total_trainees_transported"] or 0)
            else:
                combined[vn] = r

        result_rows = sorted(combined.values(), key=lambda x: x["trip_count"], reverse=True)
        if not result_rows:
            return {"type": "text", "message": "No vehicle usage records found."}
        return _build_response(result_rows, question, "vehicle", office_id, session_id, base_url, force_chat=True)
    finally:
        conn.close()


def _exec_vehicle_register_history(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    """Show vehicle register/trip history."""
    vehicle_number = slots.get("vehicle_number")
    limit = slots.get("limit") or 50
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT vr.bus_num AS vehicle_number, vr.from_date, vr.return_date,
                   vr.from_where, vr.to_where, vr.driver_name,
                   vr.total_trainee, vr.km_start, vr.km_last, vr.km_total,
                   CASE vr.type WHEN 1 THEN 'Study Tour' WHEN 2 THEN 'Field Training' ELSE 'Other' END AS trip_type
            FROM vehicle_registers vr
            WHERE vr.status = 1
        """
        params = []
        if vehicle_number:
            query += " AND vr.bus_num LIKE %s"
            params.append(f"%{vehicle_number}%")
        query += " ORDER BY vr.from_date DESC LIMIT %s"
        params.append(limit)
        cur.execute(query, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "vehicle", office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_study_tour_vehicle_usage(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    """Show vehicles used in study tours."""
    course_id = slots.get("course_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT st.id AS tour_id, st.from_date, st.return_date,
                   st.from_where, st.to_where, st.bus_num AS vehicle_number,
                   st.total_trainee,
                   st.year AS tour_year
            FROM study_tour st
            WHERE st.status = 1
        """
        params = []
        if course_id:
            query += " AND FIND_IN_SET(%s, st.course_id)"
            params.append(course_id)

        query += " ORDER BY st.from_date DESC LIMIT 100"
        cur.execute(query, params)
        rows = cur.fetchall()

        # Also fetch vehicle_registers tied to study_tours
        query2 = """
            SELECT vr.bus_num AS vehicle_number, vr.from_date, vr.return_date,
                   vr.from_where, vr.to_where, vr.driver_name,
                   vr.total_trainee, vr.km_total,
                   st.from_where AS tour_from, st.to_where AS tour_to
            FROM vehicle_registers vr
            JOIN study_tour st ON vr.study_id = st.id
            WHERE vr.status = 1 AND vr.type = 1
        """
        reg_params = []
        if course_id:
            query2 += " AND FIND_IN_SET(%s, st.course_id)"
            reg_params.append(course_id)
        query2 += " ORDER BY vr.from_date DESC LIMIT 100"
        cur.execute(query2, reg_params)
        reg_rows = cur.fetchall()

        # If we have detailed register entries, prefer those
        if reg_rows:
            return _build_response(reg_rows, question, "vehicle", office_id, session_id, base_url)
        return _build_response(rows, question, "vehicle", office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_field_training_vehicle_usage(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    """Show vehicles used in field training."""
    course_id = slots.get("course_id")
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT ft.id AS training_id, ft.from_date, ft.return_date,
                   ft.car_number AS vehicle_number,
                   ft.total_trainee, ft.remarks,
                   ft.year AS training_year
            FROM field_training ft
            WHERE ft.status = 1
        """
        params = []
        if course_id:
            query += " AND FIND_IN_SET(%s, ft.course_id)"
            params.append(course_id)

        query += " ORDER BY ft.from_date DESC LIMIT 100"
        cur.execute(query, params)
        rows = cur.fetchall()
        return _build_response(rows, question, "vehicle", office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_vehicle_by_driver(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    """Show trips by a specific driver."""
    driver_name = slots.get("driver_name")
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT vr.driver_name, vr.bus_num AS vehicle_number,
                   vr.from_date, vr.return_date,
                   vr.from_where, vr.to_where,
                   vr.total_trainee, vr.km_total,
                   CASE vr.type WHEN 1 THEN 'Study Tour' WHEN 2 THEN 'Field Training' ELSE 'Other' END AS trip_type
            FROM vehicle_registers vr
            WHERE vr.status = 1
        """
        params = []
        if driver_name:
            query += " AND vr.driver_name LIKE %s"
            params.append(f"%{driver_name}%")

        query += " ORDER BY vr.from_date DESC LIMIT 100"
        cur.execute(query, params)
        rows = cur.fetchall()

        if not rows and not driver_name:
            # Show driver-wise summary
            query2 = """
                SELECT vr.driver_name, COUNT(*) AS trip_count,
                       SUM(vr.km_total) AS total_km,
                       MIN(vr.from_date) AS first_trip,
                       MAX(vr.from_date) AS last_trip
                FROM vehicle_registers vr
                WHERE vr.status = 1 AND vr.driver_name IS NOT NULL AND vr.driver_name != ''
                GROUP BY vr.driver_name
                ORDER BY trip_count DESC
            """
            cur.execute(query2)
            rows = cur.fetchall()

        return _build_response(rows, question, "vehicle", office_id, session_id, base_url)
    finally:
        conn.close()


def _exec_vehicle_count(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    """Count vehicle bookings."""
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Count bookings from vehicle_masters
        query = """
            SELECT COUNT(*) AS total_bookings
            FROM vehicle_masters vm
            WHERE vm.status = 1
        """
        params = []
        status = slots.get("status")
        if status:
            status_code = {"pending": 0, "approved": 2, "rejected": 3, "completed": 4}.get(status.lower())
            if status_code is not None:
                query += " AND vm.v_status = %s"
                params.append(status_code)

        cur.execute(query, params)
        bookings = cur.fetchone()["total_bookings"]

        # Count distinct vehicles from registers
        cur.execute("SELECT COUNT(DISTINCT bus_num) AS total_vehicles FROM vehicle_registers WHERE status = 1 AND bus_num IS NOT NULL AND bus_num != ''")
        registered = cur.fetchone()["total_vehicles"]

        # Count study tours
        cur.execute("SELECT COUNT(*) AS total_tours FROM study_tour WHERE status = 1")
        tours = cur.fetchone()["total_tours"]

        # Count field trainings
        cur.execute("SELECT COUNT(*) AS total_trainings FROM field_training WHERE status = 1")
        trainings = cur.fetchone()["total_trainings"]

        status_label = f" ({status})" if status else ""
        msg = (
            f"Vehicle Summary{status_label}:\n"
            f"Total vehicle bookings: {bookings}\n"
            f"Distinct registered vehicles: {registered}\n"
            f"Study tours: {tours}\n"
            f"Field trainings: {trainings}"
        )
        return {"type": "text", "message": msg}
    finally:
        conn.close()


def _exec_vehicle_maintenance(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    """Vehicle maintenance records — not available in current schema."""
    return {"type": "text", "message": "Vehicle maintenance/repair records are not available in the current database schema."}


def _exec_recent_vehicle_activity(slots: dict, office_id: int, question: str, session_id: str, base_url: str) -> dict:
    """Show most recent vehicle activity from registers and study tours."""
    limit = slots.get("limit") or 10
    conn = get_connection()
    try:
        cur = conn.cursor()
        # Get recent register entries
        query = """
            SELECT vr.bus_num AS vehicle_number, vr.from_date, vr.return_date,
                   vr.from_where, vr.to_where, vr.driver_name,
                   vr.total_trainee, vr.km_total,
                   CASE vr.type WHEN 1 THEN 'Study Tour' WHEN 2 THEN 'Field Training' ELSE 'Other' END AS activity_type
            FROM vehicle_registers vr
            WHERE vr.status = 1
            ORDER BY vr.from_date DESC
            LIMIT %s
        """
        cur.execute(query, (limit,))
        reg_rows = cur.fetchall()

        # Also get recent study tours
        query2 = """
            SELECT st.bus_num AS vehicle_number, st.from_date, st.return_date,
                   st.from_where, st.to_where, '' AS driver_name,
                   st.total_trainee, 0 AS km_total,
                   'Study Tour' AS activity_type
            FROM study_tour st
            WHERE st.status = 1
            ORDER BY st.from_date DESC
            LIMIT %s
        """
        cur.execute(query2, (limit,))
        st_rows = cur.fetchall()

        # Combine and sort by date
        combined = reg_rows + st_rows
        combined.sort(key=lambda x: x.get("from_date") or "", reverse=True)
        combined = combined[:limit]

        return _build_response(combined, question, "vehicle", office_id, session_id, base_url)
    finally:
        conn.close()
