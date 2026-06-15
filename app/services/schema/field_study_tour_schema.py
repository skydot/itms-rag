"""Minified field_study_tour schema."""

FIELD_STUDY_TOUR_SCHEMA = """
TRMS Field_Study_Tour schema.
TRMS Field Training and Study Tour module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:
- field_training: id, year, course_id, from_date, start_from_date, return_date, end_return_date, total_trainee, staff_id, staff_desi_id, type, car_number, remarks, created_by, forward_id, remarks_forward, f_status, status, created_at, updated_at
- filled_training_data: id, filled_id, zone_id, div_id, trainee, status, created_at, updated_at
- study_tour: id, year, course_id, from_date, return_date, total_trainee, staff_id, staff_desi_id, type, bus_num, from_time, return_time, from_where, to_where, remarks, created_by, forward_id, remarks_forward, s_status, status, created_at, updated_at
- vehicle_registers: id, study_id, from_date, return_date, bus_num, from_time, return_time, total_trainee, type, from_where, to_where, driver_name, d_mobile, km_start, km_last, km_total, status, created_at, updated_at
- users: id, role_id, office_id, user_code, user_type, desi_id, designation, parent_id, cti, prefix, name, mobile, whatsapp_number, emergency_numbers, office_mobile, emg_mobile_no, email, office_email, aadhar, uan, name_hindi, s_name, father_name, father_name_hindi, controlling_officer, experience_raill, gender, language, birth_date, date_of_appointment, railway_join_date, retire_date, posting_date, blood, pf_no, food, ph, merital, category, country_code, account_office, country, upsc_year, upsc_rank, upsc_state, organization, usefull, qualification, additional_qualification, bank_id, bank_acc, ifsc_code, service_id, grade_id, zone_id, div_id, depo_id, station_id, dep_id, group_id, comp_id, grade_pay, pay_level, pay_basic, posted_at, permanent_address, present_address, permanent_identity, city, resi_address, representative, android_id, photo, signature, password, lang, status, hrms_id, mod_rec, is_approved, ex_is_approved, forced, created_by, created_at, updated_at
- courses: id, cf_id, cg_id, office_id, course_name, course_name_hindi, cs_code, cs_description, cs_duration, week_days, certificate, feed_type, online_exam, sort_no, status, created_at, updated_at
- training_calendars: id, cf_id, ct_id, cg_id, office_id, course_code, batch_no, course_batch, program_name, program_name_hindi, class_id, from_date, to_date, extended_date, seat, exam_note, working_days, file_no, course_director, examiner, cd, cd_user_id, ccd, dir_desi_id, dir_user_id, ati, modes, mcdo, feedback, feedback_vl, place, short_code, cancel, reason, copy_by, fail_status, status, created_at, updated_at
- tra_masters: id, user_id, ct_id, course_id, office_id, email, course_code, role, desi_id, service_id, grade_id, application_id, controlling_officer, zone_id, div_id, depo_id, station_id, dep_id, group_id, posted_at, certy_no, certy_approve, certi_ap_user, certi_ap_desi, representative, remarks, user_log, pass_file, nomination_letter, rank, local_trainee, status, out_stay, pass_status, is_approved, is_approved_date, created_at, updated_at
- rail_zones: id, zone_name, zone_name_hindi, zone_code, type, zrti_type, status, sort_no, created_at, updated_at
- divisions: id, division, div_code, zone_id, sort_no, status, created_at, updated_at
"""
