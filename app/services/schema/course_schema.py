"""Minified course schema."""

COURSE_SCHEMA = """
TRMS Course schema.
TRMS Course module schema.
IMPORTANT STATUS RULES:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering.
- courses table stores master course information.

Tables:
- courses: id, cf_id, cg_id, office_id, course_name, course_name_hindi, cs_code, cs_description, cs_duration, week_days, certificate, feed_type, online_exam, sort_no, status, created_at, updated_at
- course_for: id, office_id, course_for, types, types_name, status, sort_no, created_at, updated_at
- course_groups: id, cf_id, office_id, course_group, types, status, sort_no, created_at, updated_at
- training_calendars: id, cf_id, ct_id, cg_id, office_id, course_code, batch_no, course_batch, program_name, program_name_hindi, class_id, from_date, to_date, extended_date, seat, exam_note, working_days, file_no, course_director, examiner, cd, cd_user_id, ccd, dir_desi_id, dir_user_id, ati, modes, mcdo, feedback, feedback_vl, place, short_code, cancel, reason, copy_by, fail_status, status, created_at, updated_at
- cs_designs: id, cs_id, sub_id, office_id, topic_id, hours, desi_id, sec_id, topics_sort, subjects_sort, status, created_at, updated_at
- all_dues: id, course_id, zone_id, library, mess, hostel, sports, store, status, created_at, updated_at
- degree: id, degree, status, created_at, updated_at
- departments: id, service_id, office_id, department_name, sort_no, status, created_at, updated_at

Relationships:
- courses.cf_id = course_for.id
- courses.cg_id = course_groups.id
- training_calendars.ct_id = courses.id
- training_calendars.cf_id = course_for.id
- training_calendars.cg_id = course_groups.id
- cs_designs.cs_id = courses.id
- all_dues.course_id = training_calendars.id (facility flags per batch)
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
- hostel facility courses: join all_dues with training_calendars and courses, use all_dues.hostel = 1.
- mess facility courses: join all_dues with training_calendars and courses, use all_dues.mess = 1.
- library facility courses: join all_dues with training_calendars and courses, use all_dues.library = 1.
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
- IMPORTANT: DO NOT use course_for.status = 1 unless you explicitly JOIN course_for in the query.
- IMPORTANT: DO NOT use course_groups.status = 1 unless you explicitly JOIN course_groups in the query.
- IMPORTANT: DO NOT use training_calendars.status = 1 unless you explicitly JOIN training_calendars in the query.
- course_for.id joins with courses.cf_id.
- course_groups.id joins with courses.cg_id.
"""
