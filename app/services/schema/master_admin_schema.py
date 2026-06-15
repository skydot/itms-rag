"""Minified master_admin schema."""

MASTER_ADMIN_SCHEMA = """
TRMS Master_Admin schema.
TRMS Master Admin module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:
- users: id, role_id, office_id, user_code, user_type, desi_id, designation, parent_id, cti, prefix, name, mobile, whatsapp_number, emergency_numbers, office_mobile, emg_mobile_no, email, office_email, aadhar, uan, name_hindi, s_name, father_name, father_name_hindi, controlling_officer, experience_raill, gender, language, birth_date, date_of_appointment, railway_join_date, retire_date, posting_date, blood, pf_no, food, ph, merital, category, country_code, account_office, country, upsc_year, upsc_rank, upsc_state, organization, usefull, qualification, additional_qualification, bank_id, bank_acc, ifsc_code, service_id, grade_id, zone_id, div_id, depo_id, station_id, dep_id, group_id, comp_id, grade_pay, pay_level, pay_basic, posted_at, permanent_address, present_address, permanent_identity, city, resi_address, representative, android_id, photo, signature, password, lang, status, hrms_id, mod_rec, is_approved, ex_is_approved, forced, created_by, created_at, updated_at
- roles: id, office_id, role_name, status, created_at, updated_at
- permissions: id, permission, type_id, menu, page_link, office_id, sort_no, status, created_at, updated_at
- perm_types: id, type, groups, office_id, type_icon, sort_no, status, created_at, updated_at
- accesses: id, user_id, perm_id, office_id, created_at, updated_at
- services: id, office_id, service_name, service_name_hindi, sort_no, status, created_at, updated_at
- departments: id, service_id, office_id, department_name, sort_no, status, created_at, updated_at
- designations: id, grade_id, desi_name, desi_name_hindi, desi_code, desi_type, lecture, officer, office_id, leave_forward_id, desi_email, desi_phone, desi_fax, sort_no, status, created_at, updated_at
- grades: id, grade, status, sort_no, created_at, updated_at
- grade_pay: id, level_id, basic, status, created_at, updated_at
- pay_level: id, level, g_level, g_pay, commission, sort_no, status, created_at, updated_at
- pay_scale: id, scale, commission, sort_no, status, created_at, updated_at
- rail_zones: id, zone_name, zone_name_hindi, zone_code, type, zrti_type, status, sort_no, created_at, updated_at
- divisions: id, division, div_code, zone_id, sort_no, status, created_at, updated_at
- depots: id, depots, status, created_at, updated_at
- rail_stations: id, st_name, st_code, status, created_at, updated_at
- states: id, state, status, created_at, updated_at
- places: id, office_id, place_name, place_code, address, city, pin, state, phone_no, mobile, status, created_at, updated_at
- company: id, comp_name, status, created_at, updated_at
- bank: id, bank_name, bank_code, office_id, status, created_at, updated_at
- holidays: id, office_id, holiday_date, holiday_name, holiday_type, status, created_at, updated_at
- site_info: id, office_id, site_title, site_title_short, site_title_short_admin, site_logo, fav_icon, site_url, address, email_address, status, created_at, updated_at

Rules:
- rail_zones.zone_code for zone codes like 'NWR', 'WCR'. Use zone_code for filtering by short codes.
"""
