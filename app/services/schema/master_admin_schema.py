"""Minified master_admin schema."""

MASTER_ADMIN_SCHEMA = """
TRMS Master_Admin schema.
TRMS Master Admin module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- users.role_id = roles.id
- accesses.user_id = users.id
- accesses.perm_id = permissions.id
- departments.service_id = services.id
- designations.grade_id = grades.id
- grade_pay.level_id = pay_level.id
Common question mapping:
- Total users: Count users
- Role-wise users: Group by roles
- Departments list: Query departments
- Designations list: Query designations
- Zones/Divisions: Query rail_zones, divisions
- Active users: Filter by status

Rules:
- rail_zones.zone_code for zone codes like 'NWR', 'WCR'. Use zone_code for filtering by short codes.
"""
