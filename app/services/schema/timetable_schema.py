"""Minified timetable schema."""

TIMETABLE_SCHEMA = """
TRMS Timetable schema.
TRMS Timetable module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:
- time_masters: id, course_id, cs_id, office_id, tm_date, class_id, session_id, start_time, end_time, desi_id, desi_user_id, sec_id, sec_user_id, desi_id_three, desi_id_four, desi_id_five, vl_id, topic_id, topic_type, topic_name, note, hours, outside, status, approve, tmp, created_at, updated_at
- tt_designs: id, course_id, session_id, month, year, faculties, type, vl_id, departments, merge_from, merge_to, status, created_at, updated_at
- tt_designs_daywise: id, tt_design_id, course_id, session_id, date, faculties, type, vl_id, departments, subject_id, class_room_id, merge_from, merge_to, status, created_at, updated_at
- training_calendars: id, cf_id, ct_id, cg_id, office_id, course_code, batch_no, course_batch, program_name, program_name_hindi, class_id, from_date, to_date, extended_date, seat, exam_note, working_days, file_no, course_director, examiner, cd, cd_user_id, ccd, dir_desi_id, dir_user_id, ati, modes, mcdo, feedback, feedback_vl, place, short_code, cancel, reason, copy_by, fail_status, status, created_at, updated_at
- courses: id, cf_id, cg_id, office_id, course_name, course_name_hindi, cs_code, cs_description, cs_duration, week_days, certificate, feed_type, online_exam, sort_no, status, created_at, updated_at
- subjects: id, office_id, subject_name, subject_code, subject_hours, mark, total_mark, weightage, subject_type, mcq, essay, not_in_exam, status, created_at, updated_at
- topics: id, office_id, topic_name, topic_hours, desi_id, sec_id, short_code, topic_type, topic_description, sort_no, extra, status, created_at, updated_at
- sessions: id, office_id, session, start_time, end_time, total_time, status, created_at, updated_at
- class_rooms: id, office_id, class_name, capacity, location, features, sort_no, status, created_at, updated_at
- users: id, role_id, office_id, user_code, user_type, desi_id, designation, parent_id, cti, prefix, name, mobile, whatsapp_number, emergency_numbers, office_mobile, emg_mobile_no, email, office_email, aadhar, uan, name_hindi, s_name, father_name, father_name_hindi, controlling_officer, experience_raill, gender, language, birth_date, date_of_appointment, railway_join_date, retire_date, posting_date, blood, pf_no, food, ph, merital, category, country_code, account_office, country, upsc_year, upsc_rank, upsc_state, organization, usefull, qualification, additional_qualification, bank_id, bank_acc, ifsc_code, service_id, grade_id, zone_id, div_id, depo_id, station_id, dep_id, group_id, comp_id, grade_pay, pay_level, pay_basic, posted_at, permanent_address, present_address, permanent_identity, city, resi_address, representative, android_id, photo, signature, password, lang, status, hrms_id, mod_rec, is_approved, ex_is_approved, forced, created_by, created_at, updated_at
- designations: id, grade_id, desi_name, desi_name_hindi, desi_code, desi_type, lecture, officer, office_id, leave_forward_id, desi_email, desi_phone, desi_fax, sort_no, status, created_at, updated_at
- vl_management: id, office_id, vl_id, vl_date, subject_name, description_1, description_2, user_type, status, created_at, updated_at
"""
