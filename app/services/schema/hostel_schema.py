"""Minified hostel schema."""

HOSTEL_SCHEMA = """
TRMS Hostel schema.
TRMS Hostel module schema.
IMPORTANT STATUS RULES:
status = 1 means active record where applicable.
office_id is used for office-wise filtering.
hostel_buildings stores hostel/building capacity.

Tables:
- hostel_buildings: id, office_id, building_name, bed_capacity, location, desi_id, sort_no, status, created_at, updated_at
- hostel_rooms: id, building_id, office_id, room_name, room_beds, r_category, floor, ac, toilet, remarks, sort_no, status, created_at, updated_at, direction
- hostel_masters: id, user_id, role_id, office_id, room_type, person, amount, ct_id, course_id, train_no, ph, receipt_no, building_id, room_id, beds, food, in_date, out_date, days, item_id, mess, plusbed, remark, charge, total_charges, extra_room, preference, tour, hostel_dues, room_log, h_status, status, created_at, updated_at
- all_dues: id, course_id, zone_id, library, mess, hostel, sports, store, status, created_at, updated_at
- complaints: id, office_id, cm_no, building_id, ctype_id, ctype_sub_id, user_id, forwarded_to, description, remarks, remarks_log, rating, review, attachment, cm_status, status, created_at, updated_at
- users: id, office_id, name, mobile, email, status
- tra_masters: user_id, course_id, office_id, status
- training_calendars: id, ct_id, office_id, course_batch, from_date, to_date, status
- courses: id, office_id, course_name, status

Relationships:
hostel_rooms.building_id = hostel_buildings.id
hostel_masters.building_id = hostel_buildings.id
hostel_masters.room_id = hostel_rooms.id
hostel_masters.user_id = users.id
complaints.building_id = hostel_buildings.id
complaints.user_id = users.id
hostel_masters.course_id = training_calendars.id
tra_masters.course_id = training_calendars.id
training_calendars.ct_id = courses.id
tra_masters.user_id = users.id
Office Filtering:
Prefer hostel_buildings.office_id = {office_id} for building queries.
Prefer hostel_rooms.office_id = {office_id} for room queries.
Prefer hostel_masters.office_id = {office_id} for allotment/occupancy queries.
Prefer complaints.office_id = {office_id} for complaint queries.
Always enforce office_id from backend/login context, not from user text.
Common Question Mapping:
total hostel buildings: COUNT(*) from hostel_buildings where status = 1.
total rooms: COUNT(*) from hostel_rooms where status = 1.
total beds: SUM(hostel_rooms.room_beds) or SUM(hostel_buildings.bed_capacity), depending question.
occupied/booked beds: SUM(hostel_masters.beds) for active/current allotments.
current occupancy: hostel_masters.in_date <= CURDATE() AND (hostel_masters.out_date IS NULL OR hostel_masters.out_date >= CURDATE()).
available beds: total room beds - occupied/current booked beds.
room-wise occupancy: group by hostel_rooms.room_name.
building-wise occupancy: group by hostel_buildings.building_name.
trainee hostel details: join hostel_masters with users and hostel_rooms/buildings.
hostel complaints: use complaints joined with hostel_buildings where building_id exists.
complaint status summary: group by complaints.cm_status.

Rules:
hostel_buildings.office_id is office filter.
status = 1 means active building.
hostel_rooms.building_id joins with hostel_buildings.id.
hostel_rooms.office_id is office filter.
status = 1 means active room.
hostel_masters.user_id joins with users.id.
hostel_masters.building_id joins with hostel_buildings.id.
hostel_masters.room_id joins with hostel_rooms.id.
hostel_masters.course_id joins with training_calendars.id (NOT courses.id directly).
hostel_masters.office_id is office filter.
"""
