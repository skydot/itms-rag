"""Exam module schema for LLM SQL generation. Only table/column names — no credentials."""

EXAM_SCHEMA = """
TRMS Exam schema.
status=1 means active. office_id filters by office. result: 1=Pass, 2=Fail.

Tables:
- courses: id, cf_id, cg_id, office_id, course_name, course_name_hindi, cs_code, cs_description, cs_duration, week_days, certificate, feed_type, online_exam, sort_no, status, created_at, updated_at
- et_design: id, course_id, subject, exam_date, start_time, end_time, faculty, class_id, examiner, status, created_at, updated_at
- exam_design: id, cs_id, subject_id, total_marks, minimum_marks, mcq, essay, office_id, desi_id, type_sort, status, created_at, updated_at
- exam_marks: id, user_id, course_id, exam_type_id, subject_id, mark_obtained, re_exam_mark, total_mark, result, re_exam_result, status, created_at, updated_at
- exam_type: id, title, title_hindi, total_mark, weightage, status, created_at, updated_at
- subjects: id, office_id, subject_name, subject_code, subject_hours, mark, total_mark, weightage, subject_type, mcq, essay, not_in_exam, status, created_at, updated_at
- users: id, role_id, office_id, user_code, user_type, desi_id, designation, parent_id, cti, prefix, name, mobile, whatsapp_number, emergency_numbers, office_mobile, emg_mobile_no, email, office_email, aadhar, uan, name_hindi, s_name, father_name, father_name_hindi, controlling_officer, experience_raill, gender, language, birth_date, date_of_appointment, railway_join_date, retire_date, posting_date, blood, pf_no, food, ph, merital, category, country_code, account_office, country, upsc_year, upsc_rank, upsc_state, organization, usefull, qualification, additional_qualification, bank_id, bank_acc, ifsc_code, service_id, grade_id, zone_id, div_id, depo_id, station_id, dep_id, group_id, comp_id, grade_pay, pay_level, pay_basic, posted_at, permanent_address, present_address, permanent_identity, city, resi_address, representative, android_id, photo, signature, password, lang, status, hrms_id, mod_rec, is_approved, ex_is_approved, forced, created_by, created_at, updated_at
- training_calendars: id, cf_id, ct_id, cg_id, office_id, course_code, batch_no, course_batch, program_name, program_name_hindi, class_id, from_date, to_date, extended_date, seat, exam_note, working_days, file_no, course_director, examiner, cd, cd_user_id, ccd, dir_desi_id, dir_user_id, ati, modes, mcdo, feedback, feedback_vl, place, short_code, cancel, reason, copy_by, fail_status, status, created_at, updated_at

Relationships:
exam_marks.user_id = users.id
exam_marks.course_id = training_calendars.id
training_calendars.ct_id = courses.id
exam_marks.subject_id = subjects.id
exam_marks.exam_type_id = exam_type.id

Mapping rules:
- filter by office: exam_marks.office_id = {office_id} or courses.office_id = {office_id}
- pass/fail: exam_marks.result = 1 (Pass) or 2 (Fail)
- recent exam: ORDER BY exam_marks.created_at DESC LIMIT 1
- top/highest marks: ORDER BY exam_marks.mark_obtained DESC LIMIT 1
"""
