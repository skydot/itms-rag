"""Minified seminar schema."""

SEMINAR_SCHEMA = """
TRMS Seminar schema.
TRMS Seminar module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:
- seminars: id, sem_date, subject, start_time, end_time, type_id, topic_id, topic_des, judge, main_speaker, vl_id, created_by, forward_id, remarks_forward, topic_remarks, se_status, status, created_at, updated_at
- seminars_topic: id, office_id, sub_topic, status, created_at, updated_at
- topics: id, office_id, topic_name, topic_hours, desi_id, sec_id, short_code, topic_type, topic_description, sort_no, extra, status, created_at, updated_at
- users: id, role_id, office_id, user_code, user_type, desi_id, designation, parent_id, cti, prefix, name, mobile, whatsapp_number, emergency_numbers, office_mobile, emg_mobile_no, email, office_email, aadhar, uan, name_hindi, s_name, father_name, father_name_hindi, controlling_officer, experience_raill, gender, language, birth_date, date_of_appointment, railway_join_date, retire_date, posting_date, blood, pf_no, food, ph, merital, category, country_code, account_office, country, upsc_year, upsc_rank, upsc_state, organization, usefull, qualification, additional_qualification, bank_id, bank_acc, ifsc_code, service_id, grade_id, zone_id, div_id, depo_id, station_id, dep_id, group_id, comp_id, grade_pay, pay_level, pay_basic, posted_at, permanent_address, present_address, permanent_identity, city, resi_address, representative, android_id, photo, signature, password, lang, status, hrms_id, mod_rec, is_approved, ex_is_approved, forced, created_by, created_at, updated_at
- vl_management: id, office_id, vl_id, vl_date, subject_name, description_1, description_2, user_type, status, created_at, updated_at
- subjects: id, office_id, subject_name, subject_code, subject_hours, mark, total_mark, weightage, subject_type, mcq, essay, not_in_exam, status, created_at, updated_at
- departments: id, service_id, office_id, department_name, sort_no, status, created_at, updated_at
"""
