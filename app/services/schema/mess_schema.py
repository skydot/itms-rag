"""Minified mess schema."""

MESS_SCHEMA = """
TRMS Mess schema.
TRMS Mess module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:
- bills: id, bill_no, bill_date, user_id, role_id, ct_id, course_id, hostel_id, c_d_o, remark, bill_lock, status, created_at, updated_at
- bill_details: id, bill_id, item_id, qty, rate, taxable, gst_rate, gst_amt, amount, from_date, to_date, item_remark, bd_type, status, sort_no, created_at, updated_at
- bill_receipts: id, bill_id, user_id, course_id, user_name, role_id, pay_by, amount, receipt_no, receipt_date, from_date, to_date, days, price, overhead, due, txn_no, status, remarks, online_log, created_at, updated_at
- bill_receipts_refund: id, bill_id, user_id, role_id, pay_by, amount, receipt_no, receipt_date, due, txn_no, status, remarks, online_log, created_at, updated_at
- mess_bill_format: id, office_id, company_name, bill_prefix, gst_no, bank_name, bank_acc, ifsc_code, upi_code, fssai_license_no, term_condi, signature, effective_date, status, created_at, updated_at
- mess_material: id, item_name, units, status, created_at, updated_at
- items: id, office_id, item_name, type, status, created_at, updated_at
- item_prices: id, office_id, item_id, price, gst_rate, effect_date, status, created_at, updated_at
- partys: id, office_id, p_name, p_email, p_mobile, status, created_at, updated_at
- users: id, role_id, office_id, user_code, user_type, desi_id, designation, parent_id, cti, prefix, name, mobile, whatsapp_number, emergency_numbers, office_mobile, emg_mobile_no, email, office_email, aadhar, uan, name_hindi, s_name, father_name, father_name_hindi, controlling_officer, experience_raill, gender, language, birth_date, date_of_appointment, railway_join_date, retire_date, posting_date, blood, pf_no, food, ph, merital, category, country_code, account_office, country, upsc_year, upsc_rank, upsc_state, organization, usefull, qualification, additional_qualification, bank_id, bank_acc, ifsc_code, service_id, grade_id, zone_id, div_id, depo_id, station_id, dep_id, group_id, comp_id, grade_pay, pay_level, pay_basic, posted_at, permanent_address, present_address, permanent_identity, city, resi_address, representative, android_id, photo, signature, password, lang, status, hrms_id, mod_rec, is_approved, ex_is_approved, forced, created_by, created_at, updated_at
- courses: id, cf_id, cg_id, office_id, course_name, course_name_hindi, cs_code, cs_description, cs_duration, week_days, certificate, feed_type, online_exam, sort_no, status, created_at, updated_at
- training_calendars: id, cf_id, ct_id, cg_id, office_id, course_code, batch_no, course_batch, program_name, program_name_hindi, class_id, from_date, to_date, extended_date, seat, exam_note, working_days, file_no, course_director, examiner, cd, cd_user_id, ccd, dir_desi_id, dir_user_id, ati, modes, mcdo, feedback, feedback_vl, place, short_code, cancel, reason, copy_by, fail_status, status, created_at, updated_at
- hostel_masters: id, user_id, role_id, office_id, proom_type, person, amount, ct_id, course_id, train_no, ph, receipt_no, building_id, room_id, beds, food, in_date, out_date, days, item_id, mess, plusbed, remark, charge, total_charges, extra_room, preference, tour, hostel_dues, room_log, h_status, created_at, updated_at
"""
