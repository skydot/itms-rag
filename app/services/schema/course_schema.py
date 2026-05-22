"""Minified course schema."""

COURSE_SCHEMA = """
TRMS Course schema.
TRMS Course module schema.
IMPORTANT STATUS RULES:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering.
- courses table stores master course information.

Tables:


Relationships:
- courses.cf_id = course_for.id
- courses.cg_id = course_groups.id
- training_calendars.ct_id = courses.id
- training_calendars.cf_id = course_for.id
- training_calendars.cg_id = course_groups.id
- cs_designs.course_id = courses.id
Office Filtering:
- Prefer courses.office_id = {office_id} for course master queries.
- Prefer training_calendars.office_id = {office_id} for batch/calendar queries.
- Prefer course_for.office_id = {office_id} for category queries.
- Prefer course_groups.office_id = {office_id} for group queries.
- Always enforce office_id from backend/login context, not from user text.
Common Question Mapping:
- total courses: COUNT(*) from courses where status = 1.
- active courses: courses.status = 1.
- course details: courses by course_name or cs_code.
- department/category wise courses: join courses with course_for.
- group wise courses: join courses with course_groups.
- promotion/refresher/initial courses: use course_groups.course_group.
- online exam courses: courses.online_exam = 1.
- certificate courses: courses.certificate = 1.
- course duration: courses.cs_duration and courses.week_days.
- course batch count: join training_calendars with courses and group by course.
- upcoming batches: training_calendars.from_date > CURDATE().
- ongoing batches: training_calendars.from_date <= CURDATE() AND training_calendars.to_date >= CURDATE().
- completed batches: training_calendars.to_date < CURDATE().
- hostel facility courses: join cs_designs and use cs_designs.hostel = 1.
- mess facility courses: join cs_designs and use cs_designs.mess = 1.
- library facility courses: join cs_designs and use cs_designs.library = 1.
- seat capacity: use training_calendars.seat.
- case-insensitive course search: LOWER(courses.course_name) LIKE LOWER('%name%') OR LOWER(courses.cs_code) LIKE LOWER('%name%').
CRITICAL - RECENT/LATEST/CURRENT COURSE RULES:
- "recent course", "latest course", "current course", "recent batch", "latest batch" means the LATEST training_calendars record by from_date DESC.
- DO NOT use YEAR(CURDATE()) for "recent course" - it means latest batch, not current year.
- For "recent/latest course": ORDER BY training_calendars.from_date DESC LIMIT 1.
- For "current course" (ongoing): use training_calendars.from_date <= CURDATE() AND training_calendars.to_date >= CURDATE().
- For "this year" or "2026": then use YEAR(training_calendars.from_date) = 2026.
- For "recent course trainees": join training_calendars with tra_masters, ORDER BY tc.from_date DESC LIMIT 1, count trainees.
Example - "show recent course details":
SELECT tc.course_batch, c.course_name, tc.from_date, tc.to_date, tc.seat
FROM training_calendars tc
JOIN courses c ON c.id = tc.ct_id
WHERE tc.office_id = {office_id} AND tc.status = 1
ORDER BY tc.from_date DESC
LIMIT 1;

Rules:
- courses.office_id is office filter.
- courses.cf_id joins with course_for.id.
- courses.cg_id joins with course_groups.id.
- courses.status = 1 means active course.
- course_for.id joins with courses.cf_id.
- course_for.office_id is office filter.
- course_for.status = 1 means active course category.
- course_groups.id joins with courses.cg_id.
- course_groups.office_id is office filter.
- course_groups.status = 1 means active group.
"""
