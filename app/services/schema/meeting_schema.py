"""Minified meeting schema."""

MEETING_SCHEMA = """
TRMS Meeting schema.
TRMS Meeting module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:
- meeting_create: id, subject, title, start_time, end_time, description, date, creator, chairman, invitee, meet_description, meeting_file_no, mom_meeting_agenda, re_meeting_id, meeting_app_date, created_by, forward_id, remarks_forward, m_status, mom_for_id, mom_remarks_for, ag_status, status, created_at, updated_at
- meeting_master: id, meeting_name, status, created_at, updated_at
- meet_agenda: id, office_id, meeting_id, agenda_id, type_agenda, status, created_at, updated_at
- mdl_calenders: ct_id, id, office_id, no, agenda_title, description, incharge, mom_description, a_status, status, created_at, updated_at
- users: id, role_id, office_id, user_code, user_type, desi_id, designation, parent_id, cti, prefix, name, mobile, whatsapp_number, emergency_numbers, office_mobile, emg_mobile_no, email, office_email, aadhar, uan, name_hindi, s_name, father_name, father_name_hindi, controlling_officer, experience_raill, gender, language, birth_date, date_of_appointment, railway_join_date, retire_date, posting_date, blood, pf_no, food, ph, merital, category, country_code, account_office, country, upsc_year, upsc_rank, upsc_state, organization, usefull, qualification, additional_qualification, bank_id, bank_acc, ifsc_code, service_id, grade_id, zone_id, div_id, depo_id, station_id, dep_id, group_id, comp_id, grade_pay, pay_level, pay_basic, posted_at, permanent_address, present_address, permanent_identity, city, resi_address, representative, android_id, photo, signature, password, lang, status, hrms_id, mod_rec, is_approved, ex_is_approved, forced, created_by, created_at, updated_at
- departments: id, service_id, office_id, department_name, sort_no, status, created_at, updated_at
- designations: id, grade_id, desi_name, desi_name_hindi, desi_code, desi_type, lecture, officer, office_id, leave_forward_id, desi_email, desi_phone, desi_fax, sort_no, status, created_at, updated_at
"""
