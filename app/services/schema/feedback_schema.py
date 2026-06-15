"""Minified feedback schema."""

FEEDBACK_SCHEMA = """
TRMS Feedback schema.
TRMS Feedback module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:
- feed_master: id, user_id, course_id, fs_id, fs_type, fq_id, fq_type, response, final_submit, status, created_at, updated_at
- feed_que: fq_id, fs_id, office_id, fq_code, fq_title, fq_desc, fq_type, fq_data, fq_sort, status, created_at, updated_at
- feed_section: fs_id, office_id, fs_code, fs_title, fs_desc, fs_sort, type, status, created_at, updated_at
- feed_forwards: id, user_id, course_id, expec, in_depth, hands_on, feed, status, created_at, updated_at
- feed_que_vls: id, office_id, vl_id, subject, year, course_id, status, created_at, updated_at
- users: id, role_id, office_id, user_code, user_type, desi_id, designation, parent_id, cti, prefix, name, mobile, whatsapp_number, emergency_numbers, office_mobile, emg_mobile_no, email, office_email, aadhar, uan, name_hindi, s_name, father_name, father_name_hindi, controlling_officer, experience_raill, gender, language, birth_date, date_of_appointment, railway_join_date, retire_date, posting_date, blood, pf_no, food, ph, merital, category, country_code, account_office, country, upsc_year, upsc_rank, upsc_state, organization, usefull, qualification, additional_qualification, bank_id, bank_acc, ifsc_code, service_id, grade_id, zone_id, div_id, depo_id, station_id, dep_id, group_id, comp_id, grade_pay, pay_level, pay_basic, posted_at, permanent_address, present_address, permanent_identity, city, resi_address, representative, android_id, photo, signature, password, lang, status, hrms_id, mod_rec, is_approved, ex_is_approved, forced, created_by, created_at, updated_at
- courses: id, cf_id, cg_id, office_id, course_name, course_name_hindi, cs_code, cs_description, cs_duration, week_days, certificate, feed_type, online_exam, sort_no, status, created_at, updated_at
- training_calendars: id, cf_id, ct_id, cg_id, office_id, course_code, batch_no, course_batch, program_name, program_name_hindi, class_id, from_date, to_date, extended_date, seat, exam_note, working_days, file_no, course_director, examiner, cd, cd_user_id, ccd, dir_desi_id, dir_user_id, ati, modes, mcdo, feedback, feedback_vl, place, short_code, cancel, reason, copy_by, fail_status, status, created_at, updated_at
- subjects: id, office_id, subject_name, subject_code, subject_hours, mark, total_mark, weightage, subject_type, mcq, essay, not_in_exam, status, created_at, updated_at
- vl_management: id, office_id, vl_id, vl_date, subject_name, description_1, description_2, user_type, status, created_at, updated_at
"""
