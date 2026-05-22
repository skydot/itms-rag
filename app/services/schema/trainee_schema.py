"""Trainee module schema for LLM SQL generation. Only table/column names — no credentials."""

TRAINEE_SCHEMA = """
TRMS Trainee schema.
status=1 means active. is_approved=1 means approved. office_id filters by office.
users table: trainee profile (name, mobile). tra_masters: enrollment info. training_calendars: batch dates. courses: course details.

Tables:
- tra_masters: user_id, course_id, office_id, email, role, zone_id, div_id, depo_id, status, is_approved, created_at
- users: id, role_id, office_id, name, mobile, email, gender, status
- training_calendars: id, ct_id, office_id, course_batch, from_date, to_date, status
- courses: id, office_id, course_name, status
- hostel_buildings: id, office_id, building_name, status
- hostel_masters: id, user_id, office_id, building_id, room_id, course_id, in_date, out_date, h_status
- rail_zones: id, zone_code, zone_name
- divisions: id, division, zone_id

Relationships:
tra_masters.user_id = users.id
tra_masters.course_id = training_calendars.id
training_calendars.ct_id = courses.id

Mapping rules:
- filter by office: tra_masters.office_id = {office_id}
- by name: LOWER(users.name) LIKE LOWER('%name%')
- zone code: rail_zones.zone_code (e.g. 'NWR')
- hostel building: hostel_buildings.building_name LIKE '%Geetanjali%'
- recent/latest course: ORDER BY training_calendars.from_date DESC LIMIT 1
- ongoing: training_calendars.from_date <= CURDATE() AND training_calendars.to_date >= CURDATE()
"""
