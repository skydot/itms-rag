"""Minified sports schema."""

SPORTS_SCHEMA = """
TRMS Sports schema.
TRMS Sports module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:
- sport: id, program, from_date, to_date, start_timing, end_timing, team, coordinator, status, created_at, updated_at
- sport_team: id, program_id, team_name, status, created_at, updated_at
- sport_item: id, office_id, sport_item, status, created_at, updated_at
- sportitem_issue: id, office_id, user_id, sitem_id, qty, issue_date, return_date, fine, status, created_at, updated_at
- sport_material: id, office_id, party_id, type, item_id, purchase_date, qty, item_price, total_price, status, created_at, updated_at
- sports_photos: id, sport_id, sport_photo, status, created_at, updated_at
- srec_sport: id, office_id, type_id, name, payment_by, utr_no, course_id, receipt_no, days, trainee, amount, total, receipt_date, remarks, status, created_at, updated_at
- particpants: id, program_id, participant_id, team_id, status, created_at, updated_at
- partys: id, office_id, p_name, p_email, p_mobile, status, created_at, updated_at
- users: id, role_id, office_id, user_code, user_type, desi_id, designation, parent_id, cti, prefix, name, mobile, whatsapp_number, emergency_numbers, office_mobile, emg_mobile_no, email, office_email, aadhar, uan, name_hindi, s_name, father_name, father_name_hindi, controlling_officer, experience_raill, gender, language, birth_date, date_of_appointment, railway_join_date, retire_date, posting_date, blood, pf_no, food, ph, merital, category, country_code, account_office, country, upsc_year, upsc_rank, upsc_state, organization, usefull, qualification, additional_qualification, bank_id, bank_acc, ifsc_code, service_id, grade_id, zone_id, div_id, depo_id, station_id, dep_id, group_id, comp_id, grade_pay, pay_level, pay_basic, posted_at, permanent_address, present_address, permanent_identity, city, resi_address, representative, android_id, photo, signature, password, lang, status, hrms_id, mod_rec, is_approved, ex_is_approved, forced, created_by, created_at, updated_at
- courses: id, cf_id, cg_id, office_id, course_name, course_name_hindi, cs_code, cs_description, cs_duration, week_days, certificate, feed_type, online_exam, sort_no, status, created_at, updated_at
- training_calendars: id, cf_id, ct_id, cg_id, office_id, course_code, batch_no, course_batch, program_name, program_name_hindi, class_id, from_date, to_date, extended_date, seat, exam_note, working_days, file_no, course_director, examiner, cd, cd_user_id, ccd, dir_desi_id, dir_user_id, ati, modes, mcdo, feedback, feedback_vl, place, short_code, cancel, reason, copy_by, fail_status, status, created_at, updated_at
"""
