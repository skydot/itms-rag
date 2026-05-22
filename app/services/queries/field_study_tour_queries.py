"""Field Training and Study Tour module query templates."""

TEMPLATES = [
    {
        "id": "FST_TOTAL_FIELD_TRAINING",
        "module": "field_study_tour",
        "description": "Total field trainings",
        "example_questions": ["Total field trainings?", "How many field trainings?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "FST_TOTAL_STUDY_TOURS",
        "module": "field_study_tour",
        "description": "Total study tours",
        "example_questions": ["Total study tours?", "How many study tours?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "FST_UPCOMING_FIELD_TRAINING",
        "module": "field_study_tour",
        "description": "Upcoming field trainings",
        "example_questions": ["Upcoming field trainings?", "Future trainings?"],
        "required_params": [],
        "optional_params": ["office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FST_COMPLETED_FIELD_TRAINING",
        "module": "field_study_tour",
        "description": "Completed field trainings",
        "example_questions": ["Completed field trainings?", "Past trainings?"],
        "required_params": [],
        "optional_params": ["office_id", "year"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FST_UPCOMING_STUDY_TOURS",
        "module": "field_study_tour",
        "description": "Upcoming study tours",
        "example_questions": ["Upcoming study tours?", "Future tours?"],
        "required_params": [],
        "optional_params": ["office_id", "limit"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FST_COMPLETED_STUDY_TOURS",
        "module": "field_study_tour",
        "description": "Completed study tours",
        "example_questions": ["Completed study tours?", "Past tours?"],
        "required_params": [],
        "optional_params": ["office_id", "year"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FST_COURSE_WISE_TOURS",
        "module": "field_study_tour",
        "description": "Course-wise tours",
        "example_questions": ["Tours by course?", "Course-wise study tours?"],
        "required_params": [],
        "optional_params": ["course_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FST_YEAR_WISE_TOURS",
        "module": "field_study_tour",
        "description": "Year-wise tours",
        "example_questions": ["Tours by year?", "Year-wise study tours?"],
        "required_params": [],
        "optional_params": ["year", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FST_TRAINEE_COUNT_TOUR",
        "module": "field_study_tour",
        "description": "Trainee count in tour",
        "example_questions": ["Trainees in tour?", "How many trainees?"],
        "required_params": [],
        "optional_params": ["tour_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "FST_STAFF_ASSIGNED",
        "module": "field_study_tour",
        "description": "Staff assigned",
        "example_questions": ["Staff assigned?", "Who is assigned?"],
        "required_params": [],
        "optional_params": ["tour_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FST_VEHICLE_ASSIGNED",
        "module": "field_study_tour",
        "description": "Vehicle assigned",
        "example_questions": ["Vehicle assigned?", "Transport assigned?"],
        "required_params": [],
        "optional_params": ["tour_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FST_ROUTE_SUMMARY",
        "module": "field_study_tour",
        "description": "Route summary",
        "example_questions": ["Route summary?", "Tour routes?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FST_DATE_RANGE_TOURS",
        "module": "field_study_tour",
        "description": "Date range tours",
        "example_questions": ["Tours in date range?", "Between dates?"],
        "required_params": [],
        "optional_params": ["from_date", "to_date", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FST_BUS_NUMBER_SUMMARY",
        "module": "field_study_tour",
        "description": "Bus number summary",
        "example_questions": ["Bus summary?", "Which buses used?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FST_TOUR_STATUS_SUMMARY",
        "module": "field_study_tour",
        "description": "Tour status summary",
        "example_questions": ["Tour status?", "Study tour status?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FST_FIELD_TRAINING_STATUS",
        "module": "field_study_tour",
        "description": "Field training status summary",
        "example_questions": ["Field training status?", "Training status?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "summary",
        "security_level": "low"
    },
    {
        "id": "FST_FILLED_TRAINING_DATA",
        "module": "field_study_tour",
        "description": "Filled training data",
        "example_questions": ["Filled training data?", "Training details?"],
        "required_params": [],
        "optional_params": ["training_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FST_ZONE_DIVISION_WISE",
        "module": "field_study_tour",
        "description": "Zone/division-wise training",
        "example_questions": ["Training by zone?", "Division-wise training?"],
        "required_params": [],
        "optional_params": ["zone_id", "division_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FST_STAFF_WISE_TOURS",
        "module": "field_study_tour",
        "description": "Staff-wise tours",
        "example_questions": ["Tours by staff?", "Staff tour assignments?"],
        "required_params": [],
        "optional_params": ["staff_id", "office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "FST_MODULE_SUMMARY",
        "module": "field_study_tour",
        "description": "Field/study tour module summary",
        "example_questions": ["Field study tour summary?", "Module overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute field study tour queries."""
    p = params or {}
    
    if query_id == "FST_TOTAL_FIELD_TRAINING":
        cur.execute("SELECT COUNT(*) AS total FROM field_training ft JOIN training_calendars tc ON tc.id = ft.course_id WHERE tc.office_id = %s", (office_id,))
        r = cur.fetchone()
        return f"Total field trainings: {r['total'] if r else 0}"

    elif query_id == "FST_TOTAL_STUDY_TOURS":
        cur.execute("SELECT COUNT(id) AS total_study_tours FROM study_tour WHERE status = 1")
        r = cur.fetchone()
        return f"Total study tours: {r['total_study_tours'] if r else 0}"

    elif query_id == "FST_UPCOMING_FIELD_TRAINING":
        cur.execute("""
            SELECT ft.id, ft.year, ft.from_date, ft.start_from_date,
                   ft.return_date, ft.end_return_date, ft.total_trainee,
                   ft.car_number, ft.remarks, ft.f_status,
                   u.name AS staff_name, desi.desi_name AS staff_designation
            FROM field_training ft
            LEFT JOIN users u ON u.id = ft.staff_id
            LEFT JOIN designations desi ON desi.id = ft.staff_desi_id
            WHERE ft.from_date >= CURDATE() AND ft.status = 1
            ORDER BY ft.from_date ASC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No upcoming field trainings found."
        lines = [f"- {r['from_date']} to {r['return_date']}: Staff {r['staff_name']} ({r['total_trainee']} Trainees)" for r in rows]
        return "Upcoming Field Trainings:\n" + "\n".join(lines)

    elif query_id == "FST_COMPLETED_FIELD_TRAINING":
        cur.execute("""
            SELECT ft.id, ft.year, ft.from_date, ft.return_date,
                   ft.total_trainee, ft.car_number, ft.remarks,
                   u.name AS staff_name
            FROM field_training ft
            LEFT JOIN users u ON u.id = ft.staff_id
            WHERE ft.return_date < CURDATE() AND ft.status = 1
            ORDER BY ft.return_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No completed field trainings found."
        lines = [f"- {r['from_date']} to {r['return_date']}: Staff {r['staff_name']} ({r['total_trainee']} Trainees)" for r in rows]
        return "Completed Field Trainings:\n" + "\n".join(lines)

    elif query_id == "FST_UPCOMING_STUDY_TOURS":
        cur.execute("""
            SELECT st.id, st.year, st.from_date, st.return_date,
                   st.total_trainee, st.bus_num, st.from_where, st.to_where,
                   st.remarks, st.s_status
            FROM study_tour st
            WHERE st.from_date >= CURDATE() AND st.status = 1
            ORDER BY st.from_date ASC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No upcoming study tours found."
        lines = [f"- {r['from_date']} to {r['return_date']}: {r['from_where']} -> {r['to_where']} ({r['total_trainee']} Trainees)" for r in rows]
        return "Upcoming Study Tours:\n" + "\n".join(lines)

    elif query_id == "FST_COMPLETED_STUDY_TOURS":
        cur.execute("""
            SELECT st.id, st.year, st.from_date, st.return_date,
                   st.total_trainee, st.bus_num, st.from_where, st.to_where, st.remarks
            FROM study_tour st
            WHERE st.return_date < CURDATE() AND st.status = 1
            ORDER BY st.return_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No completed study tours found."
        lines = [f"- {r['from_date']} to {r['return_date']}: {r['from_where']} -> {r['to_where']} ({r['total_trainee']} Trainees)" for r in rows]
        return "Completed Study Tours:\n" + "\n".join(lines)

    elif query_id == "FST_COURSE_WISE_TOURS":
        cur.execute("""
            SELECT st.course_id, st.year,
                   COUNT(st.id) AS total_tours,
                   SUM(st.total_trainee) AS total_trainees
            FROM study_tour st
            WHERE st.status = 1
            GROUP BY st.course_id, st.year
            ORDER BY st.year DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No course-wise tours found."
        lines = [f"- Course {r['course_id']} ({r['year']}): {r['total_tours']} Tours, {r['total_trainees']} Trainees" for r in rows]
        return "Course-wise Study Tours:\n" + "\n".join(lines)

    elif query_id == "FST_YEAR_WISE_TOURS":
        cur.execute("""
            SELECT st.year,
                   COUNT(st.id) AS total_study_tours,
                   SUM(st.total_trainee) AS total_trainees
            FROM study_tour st
            WHERE st.status = 1
            GROUP BY st.year
            ORDER BY st.year DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No year-wise tours found."
        lines = [f"- {r['year']}: {r['total_study_tours']} Tours, {r['total_trainees']} Trainees" for r in rows]
        return "Year-wise Study Tours:\n" + "\n".join(lines)

    elif query_id == "FST_TRAINEE_COUNT_TOUR":
        cur.execute("""
            SELECT st.id, st.from_date, st.return_date,
                   st.from_where, st.to_where, st.total_trainee
            FROM study_tour st
            WHERE st.status = 1
            ORDER BY st.from_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No trainee count data found."
        lines = [f"- {r['from_where']} -> {r['to_where']} ({r['from_date']} to {r['return_date']}): {r['total_trainee']} Trainees" for r in rows]
        return "Trainees in Study Tours:\n" + "\n".join(lines)

    elif query_id == "FST_STAFF_ASSIGNED":
        cur.execute("""
            SELECT ft.id, ft.from_date, ft.return_date,
                   u.name AS staff_name, u.mobile AS staff_mobile,
                   desi.desi_name AS designation, ft.total_trainee
            FROM field_training ft
            JOIN users u ON u.id = ft.staff_id
            JOIN designations desi ON desi.id = ft.staff_desi_id
            WHERE ft.status = 1
            ORDER BY ft.from_date DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No staff assignment data found."
        lines = [f"- {r['staff_name']} ({r['designation']}): {r['from_date']} to {r['return_date']} ({r['total_trainee']} Trainees)" for r in rows]
        return "Staff Assigned to Field Training:\n" + "\n".join(lines)

    elif query_id == "FST_VEHICLE_ASSIGNED":
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
        if not rows: return "No vehicle assignment data found."
        lines = [f"- Bus {r['bus_num']} (Driver {r['driver_name']}): {r['from_where']} to {r['to_where']} ({r['from_date']} to {r['return_date']})" for r in rows]
        return "Vehicles Assigned:\n" + "\n".join(lines)

    elif query_id == "FST_ROUTE_SUMMARY":
        cur.execute("""
            SELECT st.from_where, st.to_where,
                   COUNT(st.id) AS tour_count,
                   SUM(st.total_trainee) AS total_trainees
            FROM study_tour st
            WHERE st.status = 1
            GROUP BY st.from_where, st.to_where
            ORDER BY tour_count DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No route summary found."
        lines = [f"- {r['from_where']} -> {r['to_where']}: {r['tour_count']} Tours ({r['total_trainees']} Trainees)" for r in rows]
        return "Study Tour Route Summary:\n" + "\n".join(lines)

    elif query_id == "FST_DATE_RANGE_TOURS":
        fdate = p.get("from_date")
        tdate = p.get("to_date")
        if not fdate or not tdate: return "Please specify from_date and to_date."
        cur.execute("""
            SELECT st.id, st.from_date, st.return_date,
                   st.total_trainee, st.from_where, st.to_where, st.bus_num
            FROM study_tour st
            WHERE st.from_date BETWEEN %s AND %s AND st.status = 1
            ORDER BY st.from_date
            LIMIT 50
        """, (fdate, tdate))
        rows = cur.fetchall()
        if not rows: return "No tours found in this date range."
        lines = [f"- {r['from_date']} to {r['return_date']}: {r['from_where']} -> {r['to_where']} (Bus {r['bus_num']})" for r in rows]
        return f"Study Tours from {fdate} to {tdate}:\n" + "\n".join(lines)

    elif query_id == "FST_BUS_NUMBER_SUMMARY":
        cur.execute("""
            SELECT st.bus_num,
                   COUNT(st.id) AS total_trips,
                   SUM(st.total_trainee) AS total_trainees
            FROM study_tour st
            WHERE st.bus_num IS NOT NULL AND st.status = 1
            GROUP BY st.bus_num
            ORDER BY total_trips DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No bus number summary found."
        lines = [f"- Bus {r['bus_num']}: {r['total_trips']} Trips ({r['total_trainees']} Trainees)" for r in rows]
        return "Bus Number Summary:\n" + "\n".join(lines)

    elif query_id == "FST_TOUR_STATUS_SUMMARY":
        cur.execute("""
            SELECT st.s_status,
                   CASE st.s_status
                     WHEN 0 THEN 'Draft'
                     WHEN 1 THEN 'Pending'
                     WHEN 2 THEN 'Approved'
                     WHEN 3 THEN 'Completed'
                   END AS status_label,
                   COUNT(st.id) AS count
            FROM study_tour st
            WHERE st.status = 1
            GROUP BY st.s_status
        """)
        rows = cur.fetchall()
        if not rows: return "No tour status summary found."
        lines = [f"- {r['status_label']}: {r['count']} Tours" for r in rows]
        return "Study Tour Status Summary:\n" + "\n".join(lines)

    elif query_id == "FST_FIELD_TRAINING_STATUS":
        cur.execute("""
            SELECT ft.f_status,
                   CASE ft.f_status
                     WHEN 0 THEN 'Draft'
                     WHEN 1 THEN 'Pending'
                     WHEN 2 THEN 'Rejected'
                     WHEN 3 THEN 'Approved'
                   END AS status_label,
                   COUNT(ft.id) AS count
            FROM field_training ft
            WHERE ft.status = 1
            GROUP BY ft.f_status
        """)
        rows = cur.fetchall()
        if not rows: return "No field training status found."
        lines = [f"- {r['status_label']}: {r['count']} Trainings" for r in rows]
        return "Field Training Status Summary:\n" + "\n".join(lines)

    elif query_id == "FST_FILLED_TRAINING_DATA":
        cur.execute("""
            SELECT fd.id, fd.filled_id, fd.trainee,
                   rz.zone AS zone_name,
                   d.division AS division_name
            FROM filled_training_data fd
            LEFT JOIN rail_zones rz ON rz.id = fd.zone_id
            LEFT JOIN divisions d ON d.id = fd.div_id
            WHERE fd.status = 1
            ORDER BY fd.filled_id
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No filled training data found."
        lines = [f"- Zone {r['zone_name']}, Div {r['division_name']}: {r['trainee']} Trainees" for r in rows]
        return "Filled Training Data:\n" + "\n".join(lines)

    elif query_id == "FST_ZONE_DIVISION_WISE":
        cur.execute("""
            SELECT rz.zone AS zone_name, d.division AS division_name,
                   SUM(fd.trainee) AS total_trainees,
                   COUNT(fd.id) AS record_count
            FROM filled_training_data fd
            JOIN rail_zones rz ON rz.id = fd.zone_id
            JOIN divisions d ON d.id = fd.div_id
            WHERE fd.status = 1
            GROUP BY rz.id, d.id, rz.zone, d.division
            ORDER BY total_trainees DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No zone/division training data found."
        lines = [f"- {r['zone_name']} > {r['division_name']}: {r['total_trainees']} Trainees ({r['record_count']} Records)" for r in rows]
        return "Zone & Division-wise Training:\n" + "\n".join(lines)

    elif query_id == "FST_STAFF_WISE_TOURS":
        cur.execute("""
            SELECT u.name AS staff_name, desi.desi_name AS designation,
                   COUNT(ft.id) AS total_field_trainings,
                   SUM(ft.total_trainee) AS total_trainees_handled
            FROM field_training ft
            JOIN users u ON u.id = ft.staff_id
            JOIN designations desi ON desi.id = ft.staff_desi_id
            WHERE ft.status = 1
            GROUP BY u.id, u.name, desi.desi_name
            ORDER BY total_field_trainings DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No staff-wise tours found."
        lines = [f"- {r['staff_name']} ({r['designation']}): {r['total_field_trainings']} Trainings, {r['total_trainees_handled']} Trainees Handled" for r in rows]
        return "Staff-wise Field Trainings:\n" + "\n".join(lines)

    elif query_id == "FST_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(id) FROM study_tour WHERE status=1) AS total_study_tours,
              (SELECT COUNT(id) FROM field_training WHERE status=1) AS total_field_trainings,
              (SELECT SUM(total_trainee) FROM study_tour WHERE status=1) AS trainees_in_study_tours,
              (SELECT SUM(total_trainee) FROM field_training WHERE status=1) AS trainees_in_field_training,
              (SELECT COUNT(id) FROM study_tour WHERE from_date >= CURDATE() AND status=1) AS upcoming_tours
        """)
        r = cur.fetchone()
        if not r: return "Could not generate field study tour module summary."
        return (f"Field Study Tour Module Summary:\n"
                f"Total Study Tours: {r['total_study_tours']}\n"
                f"Total Field Trainings: {r['total_field_trainings']}\n"
                f"Trainees in Study Tours: {r['trainees_in_study_tours']}\n"
                f"Trainees in Field Training: {r['trainees_in_field_training']}\n"
                f"Upcoming Tours: {r['upcoming_tours']}")

    return None
