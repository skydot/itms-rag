"""Vehicle module query templates."""

TEMPLATES = [
    {
        "id": "VEHICLE_BOOKING_COUNT",
        "module": "vehicle",
        "description": "Vehicle booking count",
        "example_questions": ["Total vehicle bookings?", "How many bookings?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_BOOKINGS_BY_DATE",
        "module": "vehicle",
        "description": "Vehicle bookings by date",
        "example_questions": ["Bookings on date?", "Date-wise bookings?"],
        "required_params": [],
        "optional_params": ["date", "from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_UPCOMING",
        "module": "vehicle",
        "description": "Upcoming vehicle bookings",
        "example_questions": ["Upcoming bookings?", "Future vehicle trips?"],
        "required_params": [],
        "optional_params": ["office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_COMPLETED",
        "module": "vehicle",
        "description": "Completed vehicle bookings",
        "example_questions": ["Completed trips?", "Past bookings?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_REGISTER_LIST",
        "module": "vehicle",
        "description": "Vehicle register list",
        "example_questions": ["Vehicle list?", "Registered vehicles?"],
        "required_params": [],
        "optional_params": ["office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_BY_COURSE",
        "module": "vehicle",
        "description": "Vehicle by course",
        "example_questions": ["Vehicle by course?", "Course-wise bookings?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_BY_STUDY_TOUR",
        "module": "vehicle",
        "description": "Vehicle by study tour",
        "example_questions": ["Vehicle for study tour?", "Tour vehicles?"],
        "required_params": [],
        "optional_params": ["study_tour_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_BY_FIELD_TRAINING",
        "module": "vehicle",
        "description": "Vehicle by field training",
        "example_questions": ["Vehicle for field training?", "Training vehicles?"],
        "required_params": [],
        "optional_params": ["field_training_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_TRAINEE_COUNT",
        "module": "vehicle",
        "description": "Total trainees in vehicle trips",
        "example_questions": ["Trainees in vehicles?", "Passenger count?"],
        "required_params": [],
        "optional_params": ["office_id", "trip_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_KM_SUMMARY",
        "module": "vehicle",
        "description": "KM summary",
        "example_questions": ["Total KM?", "Kilometer summary?"],
        "required_params": [],
        "optional_params": ["office_id", "from_date", "to_date"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_ROUTE_SUMMARY",
        "module": "vehicle",
        "description": "Route/from-to summary",
        "example_questions": ["Route summary?", "Popular routes?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_STATUS_SUMMARY",
        "module": "vehicle",
        "description": "Vehicle status summary",
        "example_questions": ["Vehicle status?", "Booking status?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_PENDING",
        "module": "vehicle",
        "description": "Pending bookings",
        "example_questions": ["Pending bookings?", "Awaiting approval?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_APPROVED",
        "module": "vehicle",
        "description": "Approved bookings",
        "example_questions": ["Approved bookings?", "Confirmed trips?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_CANCELLED",
        "module": "vehicle",
        "description": "Cancelled bookings",
        "example_questions": ["Cancelled bookings?", "Rejected trips?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_TWO_WAY",
        "module": "vehicle",
        "description": "Two-way bookings",
        "example_questions": ["Two-way bookings?", "Round trips?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_TRAIN_PNR",
        "module": "vehicle",
        "description": "Train/PNR booking info",
        "example_questions": ["Train bookings?", "PNR details?"],
        "required_params": [],
        "optional_params": ["office_id", "pnr_number"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "VEHICLE_USAGE_MONTHLY",
        "module": "vehicle",
        "description": "Vehicle usage by month",
        "example_questions": ["Monthly usage?", "Vehicle by month?"],
        "required_params": [],
        "optional_params": ["month", "year", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_DRIVER_DETAILS",
        "module": "vehicle",
        "description": "Driver details",
        "example_questions": ["Driver details?", "Driver assignments?"],
        "required_params": [],
        "optional_params": ["office_id", "vehicle_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "VEHICLE_MODULE_SUMMARY",
        "module": "vehicle",
        "description": "Vehicle module summary",
        "example_questions": ["Vehicle summary?", "Vehicle module overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute vehicle queries."""
    p = params or {}
    
    if query_id == "VEHICLE_BOOKINGS_BY_DATE":
        fdate = p.get("from_date") or p.get("date")
        if not fdate: return "Please specify from_date."
        cur.execute("""
            SELECT vm.id, vm.name, vm.from_place, vm.to_place,
                   vm.from_date, vm.to_date, vm.adult, vm.child,
                   vm.booking_for, vm.two_way
            FROM vehicle_masters vm
            LEFT JOIN training_calendars tc ON tc.id = vm.course_id
            WHERE DATE(vm.from_date) = %s AND vm.status = 1 AND (tc.office_id = %s OR tc.id IS NULL)
            ORDER BY vm.from_date
            LIMIT 50
        """, (fdate, office_id))
        rows = cur.fetchall()
        if not rows: return f"No vehicle bookings on {fdate}."
        lines = [f"- {r['name']} ({r['from_place']} to {r['to_place']}): {r['booking_for']}" for r in rows]
        return f"Vehicle Bookings on {fdate}:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_UPCOMING":
        cur.execute("""
            SELECT vm.id, vm.name, vm.from_place, vm.to_place,
                   vm.from_date, vm.to_date, vm.booking_for, vm.two_way
            FROM vehicle_masters vm
            LEFT JOIN training_calendars tc ON tc.id = vm.course_id
            WHERE vm.from_date >= NOW() AND vm.status = 1 AND (tc.office_id = %s OR tc.id IS NULL)
            ORDER BY vm.from_date ASC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No upcoming vehicle bookings."
        lines = [f"- {r['name']} ({r['from_date']}): {r['from_place']} to {r['to_place']}" for r in rows]
        return "Upcoming Vehicle Bookings:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_COMPLETED":
        cur.execute("""
            SELECT vm.id, vm.name, vm.from_place, vm.to_place,
                   vm.from_date, vm.to_date, vm.kilometer
            FROM vehicle_masters vm
            LEFT JOIN training_calendars tc ON tc.id = vm.course_id
            WHERE vm.to_date < NOW() AND vm.status = 1 AND (tc.office_id = %s OR tc.id IS NULL)
            ORDER BY vm.to_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No completed vehicle bookings."
        lines = [f"- {r['name']} ({r['from_date']} to {r['to_date']}): {r['kilometer']}km" for r in rows]
        return "Completed Vehicle Bookings:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_REGISTER_LIST":
        cur.execute("""
            SELECT vr.id, vr.from_date, vr.return_date, vr.bus_num,
                   vr.from_where, vr.to_where, vr.total_trainee,
                   vr.driver_name, vr.d_mobile,
                   vr.km_start, vr.km_last, vr.km_total
            FROM vehicle_registers vr
            WHERE vr.status = 1
            ORDER BY vr.from_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No vehicle registers found."
        lines = [f"- Bus {r['bus_num']} ({r['from_date']}): {r['from_where']} to {r['to_where']} ({r['km_total']}km)" for r in rows]
        return "Vehicle Register:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_BY_COURSE":
        cid = p.get("course_id")
        if not cid: return "Please specify course_id."
        cur.execute("""
            SELECT vm.id, vm.name, vm.from_place, vm.to_place, vm.from_date,
                   tc.course_batch, c.course_name
            FROM vehicle_masters vm
            JOIN training_calendars tc ON tc.id = vm.course_id
            JOIN courses c ON c.id = tc.ct_id
            WHERE vm.course_id = %s AND vm.status = 1 AND tc.office_id = %s
            ORDER BY vm.from_date DESC
            LIMIT 50
        """, (cid, office_id))
        rows = cur.fetchall()
        if not rows: return f"No vehicles booked for course {cid}."
        lines = [f"- {r['name']} ({r['from_date']}): {r['from_place']} to {r['to_place']}" for r in rows]
        return f"Vehicle Bookings for Course {cid}:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_BY_STUDY_TOUR":
        sid = p.get("study_id")
        if not sid: return "Please specify study_id."
        cur.execute("""
            SELECT vr.id, vr.from_date, vr.return_date, vr.bus_num,
                   vr.from_where, vr.to_where, vr.total_trainee,
                   st.remarks AS tour_remarks
            FROM vehicle_registers vr
            JOIN study_tour st ON st.id = vr.study_id
            WHERE vr.study_id = %s AND vr.status = 1
            ORDER BY vr.from_date
            LIMIT 50
        """, (sid,))
        rows = cur.fetchall()
        if not rows: return f"No vehicles registered for study tour {sid}."
        lines = [f"- Bus {r['bus_num']} ({r['from_date']}): {r['from_where']} to {r['to_where']}" for r in rows]
        return f"Vehicles for Study Tour {sid}:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_BY_FIELD_TRAINING":
        cur.execute("""
            SELECT vm.id, vm.name, vm.from_place, vm.to_place,
                   vm.from_date, vm.to_date, vm.booking_for
            FROM vehicle_masters vm
            LEFT JOIN training_calendars tc ON tc.id = vm.course_id
            WHERE vm.booking_for = 'field_training' AND vm.status = 1 AND (tc.office_id = %s OR tc.id IS NULL)
            ORDER BY vm.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No vehicles for field training found."
        lines = [f"- {r['name']} ({r['from_date']}): {r['from_place']} to {r['to_place']}" for r in rows]
        return "Vehicles for Field Training:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_TRAINEE_COUNT":
        cur.execute("""
            SELECT vm.id, vm.from_place, vm.to_place, vm.from_date,
                   vm.adult + vm.child AS total_passengers
            FROM vehicle_masters vm
            LEFT JOIN training_calendars tc ON tc.id = vm.course_id
            WHERE vm.status = 1 AND (tc.office_id = %s OR tc.id IS NULL)
            ORDER BY vm.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No vehicle passenger data found."
        lines = [f"- {r['from_place']} to {r['to_place']} ({r['from_date']}): {r['total_passengers']} Passengers" for r in rows]
        return "Vehicle Passenger Counts:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_KM_SUMMARY":
        cur.execute("""
            SELECT SUM(vr.km_total) AS total_km,
                   AVG(vr.km_total) AS avg_km_per_trip,
                   COUNT(vr.id) AS total_trips
            FROM vehicle_registers vr
            WHERE vr.status = 1
        """)
        r = cur.fetchone()
        return f"Vehicle KM Summary: {r['total_km']} Total KM, {r['total_trips']} Trips (Avg {r['avg_km_per_trip']:.1f} KM/trip)" if r and r['total_trips'] else "No KM summary found."

    elif query_id == "VEHICLE_ROUTE_SUMMARY":
        cur.execute("""
            SELECT vr.from_where, vr.to_where,
                   COUNT(vr.id) AS trip_count,
                   SUM(vr.total_trainee) AS total_trainees,
                   SUM(vr.km_total) AS total_km
            FROM vehicle_registers vr
            WHERE vr.status = 1
            GROUP BY vr.from_where, vr.to_where
            ORDER BY trip_count DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No route summary found."
        lines = [f"- {r['from_where']} to {r['to_where']}: {r['trip_count']} Trips, {r['total_km']}km ({r['total_trainees']} Trainees)" for r in rows]
        return "Vehicle Route Summary:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_STATUS_SUMMARY":
        cur.execute("""
            SELECT vm.v_status_id,
                   COUNT(vm.id) AS count
            FROM vehicle_masters vm
            LEFT JOIN training_calendars tc ON tc.id = vm.course_id
            WHERE vm.status = 1 AND (tc.office_id = %s OR tc.id IS NULL)
            GROUP BY vm.v_status_id
            ORDER BY count DESC
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No status summary found."
        lines = [f"- Status {r['v_status_id']}: {r['count']} Bookings" for r in rows]
        return "Vehicle Status Summary:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_PENDING":
        cur.execute("""
            SELECT vm.id, vm.name, vm.from_place, vm.to_place,
                   vm.from_date, vm.to_date, vm.v_status_id
            FROM vehicle_masters vm
            LEFT JOIN training_calendars tc ON tc.id = vm.course_id
            WHERE vm.v_status_id = 1 AND vm.status = 1 AND (tc.office_id = %s OR tc.id IS NULL)
            ORDER BY vm.from_date
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No pending bookings found."
        lines = [f"- {r['name']} ({r['from_date']}): {r['from_place']} to {r['to_place']}" for r in rows]
        return "Pending Vehicle Bookings:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_APPROVED":
        cur.execute("""
            SELECT vm.id, vm.name, vm.from_place, vm.to_place,
                   vm.from_date, vm.to_date
            FROM vehicle_masters vm
            LEFT JOIN training_calendars tc ON tc.id = vm.course_id
            WHERE vm.v_status_id = 3 AND vm.status = 1 AND (tc.office_id = %s OR tc.id IS NULL)
            ORDER BY vm.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No approved bookings found."
        lines = [f"- {r['name']} ({r['from_date']}): {r['from_place']} to {r['to_place']}" for r in rows]
        return "Approved Vehicle Bookings:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_CANCELLED":
        cur.execute("""
            SELECT vm.id, vm.name, vm.from_place, vm.to_place,
                   vm.from_date, vm.to_date
            FROM vehicle_masters vm
            LEFT JOIN training_calendars tc ON tc.id = vm.course_id
            WHERE vm.v_status_id = 4 AND vm.status = 1 AND (tc.office_id = %s OR tc.id IS NULL)
            ORDER BY vm.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No cancelled bookings found."
        lines = [f"- {r['name']} ({r['from_date']}): {r['from_place']} to {r['to_place']}" for r in rows]
        return "Cancelled Vehicle Bookings:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_TWO_WAY":
        cur.execute("""
            SELECT vm.id, vm.name, vm.from_place, vm.to_place,
                   vm.from_date, vm.to_date, vm.two_way
            FROM vehicle_masters vm
            LEFT JOIN training_calendars tc ON tc.id = vm.course_id
            WHERE vm.two_way = 1 AND vm.status = 1 AND (tc.office_id = %s OR tc.id IS NULL)
            ORDER BY vm.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No two-way bookings found."
        lines = [f"- {r['name']} ({r['from_date']}): {r['from_place']} <-> {r['to_place']}" for r in rows]
        return "Two-Way Vehicle Bookings:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_TRAIN_PNR":
        cur.execute("""
            SELECT vm.id, vm.name, vm.train_no, vm.from_place, vm.to_place,
                   vm.from_date
            FROM vehicle_masters vm
            LEFT JOIN training_calendars tc ON tc.id = vm.course_id
            WHERE vm.train_no IS NOT NULL AND vm.status = 1 AND (tc.office_id = %s OR tc.id IS NULL)
            ORDER BY vm.from_date DESC
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No train PNR links found."
        lines = [f"- {r['name']} ({r['from_date']}): Train {r['train_no']}" for r in rows]
        return "Vehicle Train PNR Links:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_USAGE_MONTHLY":
        cur.execute("""
            SELECT YEAR(vr.from_date) AS yr, MONTH(vr.from_date) AS mo,
                   MONTHNAME(vr.from_date) AS month_name,
                   COUNT(vr.id) AS trips,
                   SUM(vr.km_total) AS total_km,
                   SUM(vr.total_trainee) AS total_trainees
            FROM vehicle_registers vr
            WHERE vr.status = 1
            GROUP BY YEAR(vr.from_date), MONTH(vr.from_date)
            ORDER BY yr DESC, mo DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No monthly usage found."
        lines = [f"- {r['month_name']} {r['yr']}: {r['trips']} Trips, {r['total_km']}km ({r['total_trainees']} Trainees)" for r in rows]
        return "Monthly Vehicle Usage:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_DRIVER_DETAILS":
        cur.execute("""
            SELECT vr.driver_name, vr.d_mobile,
                   COUNT(vr.id) AS trips,
                   SUM(vr.km_total) AS total_km
            FROM vehicle_registers vr
            WHERE vr.driver_name IS NOT NULL AND vr.status = 1
            GROUP BY vr.driver_name, vr.d_mobile
            ORDER BY trips DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No driver details found."
        lines = [f"- Driver {r['driver_name']} ({r['d_mobile']}): {r['trips']} Trips, {r['total_km']}km" for r in rows]
        return "Vehicle Drivers:\n" + "\n".join(lines)

    elif query_id == "VEHICLE_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(vm.id) FROM vehicle_masters vm LEFT JOIN training_calendars tc ON tc.id=vm.course_id WHERE vm.status=1 AND (tc.office_id=%s OR tc.id IS NULL)) AS total_bookings,
              (SELECT COUNT(vm.id) FROM vehicle_masters vm LEFT JOIN training_calendars tc ON tc.id=vm.course_id WHERE vm.from_date >= NOW() AND vm.status=1 AND (tc.office_id=%s OR tc.id IS NULL)) AS upcoming,
              (SELECT COUNT(vr.id) FROM vehicle_registers vr WHERE vr.status=1) AS total_trips_registered,
              (SELECT SUM(vr.km_total) FROM vehicle_registers vr WHERE vr.status=1) AS total_km_covered,
              (SELECT COUNT(vm.id) FROM vehicle_masters vm LEFT JOIN training_calendars tc ON tc.id=vm.course_id WHERE vm.v_status_id=1 AND vm.status=1 AND (tc.office_id=%s OR tc.id IS NULL)) AS pending_approvals
        """, (office_id, office_id, office_id))
        r = cur.fetchone()
        if not r: return "Could not generate vehicle module summary."
        return (f"Vehicle Module Summary:\n"
                f"Total Bookings: {r['total_bookings']}\n"
                f"Upcoming Bookings: {r['upcoming']}\n"
                f"Total Trips Registered: {r['total_trips_registered']}\n"
                f"Total KM Covered: {r['total_km_covered']}\n"
                f"Pending Approvals: {r['pending_approvals']}")

    return None
