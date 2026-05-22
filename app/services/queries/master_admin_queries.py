"""Master Admin module query templates."""

TEMPLATES = [
    {
        "id": "MASTER_TOTAL_USERS",
        "module": "master_admin",
        "description": "Total users",
        "example_questions": ["Total users?", "How many users?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "super_admin"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "MASTER_TOTAL_ROLES",
        "module": "master_admin",
        "description": "Total roles",
        "example_questions": ["Total roles?", "How many roles?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "super_admin"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "MASTER_ROLE_WISE_USERS",
        "module": "master_admin",
        "description": "Role-wise users",
        "example_questions": ["Role-wise users?", "Users by role?"],
        "required_params": [],
        "optional_params": ["role_id", "office_id"],
        "allowed_roles": ["principal", "admin", "super_admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_PERMISSION_LIST",
        "module": "master_admin",
        "description": "Permission list",
        "example_questions": ["List permissions?", "What permissions?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "super_admin"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_USER_ACCESS_LIST",
        "module": "master_admin",
        "description": "User access list",
        "example_questions": ["User access?", "Who has access?"],
        "required_params": [],
        "optional_params": ["user_id", "office_id"],
        "allowed_roles": ["principal", "admin", "super_admin"],
        "result_type": "list",
        "security_level": "medium"
    },
    {
        "id": "MASTER_DEPARTMENTS_LIST",
        "module": "master_admin",
        "description": "Departments list",
        "example_questions": ["List departments?", "What departments?"],
        "required_params": [],
        "optional_params": ["office_id", "service_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_DESIGNATIONS_LIST",
        "module": "master_admin",
        "description": "Designations list",
        "example_questions": ["List designations?", "What designations?"],
        "required_params": [],
        "optional_params": ["office_id", "grade_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_GRADES_LIST",
        "module": "master_admin",
        "description": "Grades list",
        "example_questions": ["List grades?", "What grades?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_SERVICES_LIST",
        "module": "master_admin",
        "description": "Services list",
        "example_questions": ["List services?", "What services?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_ZONES_LIST",
        "module": "master_admin",
        "description": "Zones list",
        "example_questions": ["List zones?", "What zones?"],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_DIVISIONS_LIST",
        "module": "master_admin",
        "description": "Divisions list",
        "example_questions": ["List divisions?", "What divisions?"],
        "required_params": [],
        "optional_params": ["zone_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_DEPOTS_LIST",
        "module": "master_admin",
        "description": "Depots list",
        "example_questions": ["List depots?", "What depots?"],
        "required_params": [],
        "optional_params": ["division_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_RAIL_STATIONS_LIST",
        "module": "master_admin",
        "description": "Rail stations list",
        "example_questions": ["List stations?", "Rail stations?"],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_HOLIDAYS_LIST",
        "module": "master_admin",
        "description": "Holidays list",
        "example_questions": ["List holidays?", "What holidays?"],
        "required_params": [],
        "optional_params": ["office_id", "year"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_BANKS_LIST",
        "module": "master_admin",
        "description": "Banks list",
        "example_questions": ["List banks?", "What banks?"],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_COMPANIES_LIST",
        "module": "master_admin",
        "description": "Companies list",
        "example_questions": ["List companies?", "What companies?"],
        "required_params": [],
        "optional_params": [],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_PLACES_LIST",
        "module": "master_admin",
        "description": "Places list",
        "example_questions": ["List places?", "What places?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "staff"],
        "result_type": "list",
        "security_level": "low"
    },
    {
        "id": "MASTER_ACTIVE_USERS",
        "module": "master_admin",
        "description": "Active users",
        "example_questions": ["Active users?", "How many active?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "super_admin"],
        "result_type": "count",
        "security_level": "low"
    },
    {
        "id": "MASTER_INACTIVE_USERS",
        "module": "master_admin",
        "description": "Inactive users",
        "example_questions": ["Inactive users?", "How many inactive?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "super_admin"],
        "result_type": "count",
        "security_level": "medium"
    },
    {
        "id": "MASTER_MODULE_SUMMARY",
        "module": "master_admin",
        "description": "Master admin summary",
        "example_questions": ["Master admin summary?", "Master overview?"],
        "required_params": [],
        "optional_params": ["office_id"],
        "allowed_roles": ["principal", "admin", "super_admin"],
        "result_type": "summary",
        "security_level": "low"
    }
]


def execute(query_id, params, cur, office_id):
    """Execute master admin queries."""
    p = params or {}
    
    if query_id == "MASTER_TOTAL_ROLES":
        cur.execute("SELECT COUNT(id) AS total_roles FROM roles WHERE status = 1")
        r = cur.fetchone()
        return f"Total roles: {r['total_roles'] if r else 0}"

    elif query_id == "MASTER_ROLE_WISE_USERS":
        cur.execute("""
            SELECT r.role_name, COUNT(u.id) AS user_count
            FROM roles r
            LEFT JOIN users u ON u.role_id = r.id AND u.status = 1
            WHERE r.status = 1
            GROUP BY r.id, r.role_name
            ORDER BY user_count DESC
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No role-wise user data found."
        lines = [f"- {r['role_name']}: {r['user_count']} Users" for r in rows]
        return "Role-wise Users:\n" + "\n".join(lines)

    elif query_id == "MASTER_PERMISSION_LIST":
        cur.execute("""
            SELECT p.id, p.permission, p.page_link, p.menu, p.sort_no,
                   pt.perm_type
            FROM permissions p
            LEFT JOIN perm_types pt ON pt.id = p.type_id
            WHERE p.status = 1
            ORDER BY p.sort_no
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No permissions found."
        lines = [f"- {r['permission']} ({r['perm_type']}): {r['page_link']}" for r in rows]
        return "Permissions List:\n" + "\n".join(lines)

    elif query_id == "MASTER_USER_ACCESS_LIST":
        cur.execute("""
            SELECT u.name, u.email, p.permission, p.page_link
            FROM accesses a
            JOIN users u ON u.id = a.user_id
            JOIN permissions p ON p.id = a.perm_id
            WHERE u.status = 1 AND p.status = 1 AND u.office_id = %s
            ORDER BY u.name, p.sort_no
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No user accesses found."
        lines = [f"- {r['name']} ({r['email']}): {r['permission']}" for r in rows]
        return "User Access List:\n" + "\n".join(lines)

    elif query_id == "MASTER_DEPARTMENTS_LIST":
        cur.execute("""
            SELECT d.id, d.department_name, d.sort_no, d.status, d.created_at
            FROM departments d
            WHERE d.status = 1
            ORDER BY d.sort_no, d.department_name
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No departments found."
        lines = [f"- {r['department_name']}" for r in rows]
        return "Departments:\n" + "\n".join(lines)

    elif query_id == "MASTER_DESIGNATIONS_LIST":
        cur.execute("""
            SELECT desi.id, desi.desi_name, desi.desi_code, desi.desi_type,
                   desi.lecture, desi.officer, desi.sort_no
            FROM designations desi
            WHERE desi.status = 1
            ORDER BY desi.sort_no, desi.desi_name
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No designations found."
        lines = [f"- {r['desi_name']} ({r['desi_code']})" for r in rows]
        return "Designations:\n" + "\n".join(lines)

    elif query_id == "MASTER_GRADES_LIST":
        cur.execute("""
            SELECT g.id, g.grade_name, g.sort_no, g.status
            FROM grades g
            WHERE g.status = 1
            ORDER BY g.sort_no
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No grades found."
        lines = [f"- {r['grade_name']}" for r in rows]
        return "Grades:\n" + "\n".join(lines)

    elif query_id == "MASTER_SERVICES_LIST":
        cur.execute("""
            SELECT s.id, s.service_name, s.sort_no, s.status
            FROM services s
            WHERE s.status = 1
            ORDER BY s.sort_no, s.service_name
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No services found."
        lines = [f"- {r['service_name']}" for r in rows]
        return "Services:\n" + "\n".join(lines)

    elif query_id == "MASTER_ZONES_LIST":
        cur.execute("""
            SELECT rz.id, rz.zone, rz.zone_code, rz.sort_no, rz.status
            FROM rail_zones rz
            WHERE rz.status = 1
            ORDER BY rz.sort_no, rz.zone
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No rail zones found."
        lines = [f"- {r['zone']} ({r['zone_code']})" for r in rows]
        return "Rail Zones:\n" + "\n".join(lines)

    elif query_id == "MASTER_DIVISIONS_LIST":
        cur.execute("""
            SELECT d.id, d.division, d.div_code, rz.zone AS zone_name, d.sort_no
            FROM divisions d
            LEFT JOIN rail_zones rz ON rz.id = d.zone_id
            WHERE d.status = 1
            ORDER BY rz.zone, d.division
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No divisions found."
        lines = [f"- {r['division']} ({r['div_code']}) - Zone: {r['zone_name']}" for r in rows]
        return "Divisions:\n" + "\n".join(lines)

    elif query_id == "MASTER_DEPOTS_LIST":
        cur.execute("""
            SELECT dep.id, dep.depot_name, dep.depot_code, d.division AS division_name
            FROM depots dep
            LEFT JOIN divisions d ON d.id = dep.div_id
            WHERE dep.status = 1
            ORDER BY dep.depot_name
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No depots found."
        lines = [f"- {r['depot_name']} ({r['depot_code']}) - Div: {r['division_name']}" for r in rows]
        return "Depots:\n" + "\n".join(lines)

    elif query_id == "MASTER_RAIL_STATIONS_LIST":
        cur.execute("""
            SELECT rs.id, rs.station_name, rs.station_code, rz.zone AS zone_name
            FROM rail_stations rs
            LEFT JOIN rail_zones rz ON rz.id = rs.zone_id
            WHERE rs.status = 1
            ORDER BY rs.station_name
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No rail stations found."
        lines = [f"- {r['station_name']} ({r['station_code']}) - Zone: {r['zone_name']}" for r in rows]
        return "Rail Stations:\n" + "\n".join(lines)

    elif query_id == "MASTER_HOLIDAYS_LIST":
        cur.execute("""
            SELECT h.id, h.holiday_name, h.holiday_date, h.holiday_type
            FROM holidays h
            WHERE h.status = 1
            ORDER BY h.holiday_date
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No holidays found."
        lines = [f"- {r['holiday_name']} on {r['holiday_date']} ({r['holiday_type']})" for r in rows]
        return "Holidays:\n" + "\n".join(lines)

    elif query_id == "MASTER_BANKS_LIST":
        cur.execute("""
            SELECT b.id, b.bank_name
            FROM bank b
            WHERE b.status = 1
            ORDER BY b.bank_name
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No banks found."
        lines = [f"- {r['bank_name']}" for r in rows]
        return "Banks:\n" + "\n".join(lines)

    elif query_id == "MASTER_COMPANIES_LIST":
        cur.execute("""
            SELECT c.id, c.company_name
            FROM company c
            WHERE c.status = 1
            ORDER BY c.company_name
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No companies found."
        lines = [f"- {r['company_name']}" for r in rows]
        return "Companies:\n" + "\n".join(lines)

    elif query_id == "MASTER_PLACES_LIST":
        cur.execute("""
            SELECT p.id, p.place_name
            FROM places p
            WHERE p.status = 1
            ORDER BY p.place_name
            LIMIT 50
        """)
        rows = cur.fetchall()
        if not rows: return "No places found."
        lines = [f"- {r['place_name']}" for r in rows]
        return "Places:\n" + "\n".join(lines)

    elif query_id == "MASTER_ACTIVE_USERS":
        cur.execute("""
            SELECT u.id, u.name, u.email, u.mobile, r.role_name,
                   desi.desi_name AS designation, u.status
            FROM users u
            LEFT JOIN roles r ON r.id = u.role_id
            LEFT JOIN designations desi ON desi.id = u.desi_id
            WHERE u.status = 1 AND u.office_id = %s
            ORDER BY u.name
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No active users found."
        lines = [f"- {r['name']} ({r['email']}): {r['role_name']}, {r['designation']}" for r in rows]
        return "Active Users:\n" + "\n".join(lines)

    elif query_id == "MASTER_INACTIVE_USERS":
        cur.execute("""
            SELECT u.id, u.name, u.email, u.mobile, r.role_name
            FROM users u
            LEFT JOIN roles r ON r.id = u.role_id
            WHERE u.status = 2 AND u.office_id = %s
            ORDER BY u.name
            LIMIT 50
        """, (office_id,))
        rows = cur.fetchall()
        if not rows: return "No inactive users found."
        lines = [f"- {r['name']} ({r['email']}): {r['role_name']}" for r in rows]
        return "Inactive Users:\n" + "\n".join(lines)

    elif query_id == "MASTER_MODULE_SUMMARY":
        cur.execute("""
            SELECT
              (SELECT COUNT(id) FROM users WHERE status=1 AND office_id=%s) AS active_users,
              (SELECT COUNT(id) FROM roles WHERE status=1) AS total_roles,
              (SELECT COUNT(id) FROM departments WHERE status=1) AS total_departments,
              (SELECT COUNT(id) FROM designations WHERE status=1) AS total_designations,
              (SELECT COUNT(id) FROM courses WHERE status=1) AS active_courses,
              (SELECT COUNT(id) FROM permissions WHERE status=1) AS total_permissions
        """, (office_id,))
        r = cur.fetchone()
        if not r: return "Could not generate master module summary."
        return (f"Master Module Summary:\n"
                f"Active Users: {r['active_users']}\n"
                f"Total Roles: {r['total_roles']}\n"
                f"Total Departments: {r['total_departments']}\n"
                f"Total Designations: {r['total_designations']}\n"
                f"Active Courses: {r['active_courses']}\n"
                f"Total Permissions: {r['total_permissions']}")

    return None
