"""Minified complaint schema."""

COMPLAINT_SCHEMA = """
TRMS Complaint schema.
TRMS Complaint module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce complaints.office_id = {office_id}.

Tables:
- complaints: id, office_id, cm_no, building_id, ctype_id, ctype_sub_id, user_id, forwarded_to, description, remarks, remarks_log, rating, review, attachment, cm_status, status, created_at, updated_at
- complaints_files: id, cm_id, attachment, status, created_at, updated_at
- complaint_cat: id, comp_name, cat_id, agent_id, sort, status, created_at, updated_at
- complaint_subcat: id, cat_id, subcat_name, status, created_at, updated_at
- comp_categories: id, parent_id, agent_id, category, status, created_at, updated_at
- users: id, role_id, office_id, user_code, user_type, desi_id, designation, parent_id, cti, prefix, name, mobile, whatsapp_number, emergency_numbers, office_mobile, emg_mobile_no, email, office_email, aadhar, uan, name_hindi, s_name, father_name, father_name_hindi, controlling_officer, experience_raill, gender, language, birth_date, date_of_appointment, railway_join_date, retire_date, posting_date, blood, pf_no, food, ph, merital, category, country_code, account_office, country, upsc_year, upsc_rank, upsc_state, organization, usefull, qualification, additional_qualification, bank_id, bank_acc, ifsc_code, service_id, grade_id, zone_id, div_id, depo_id, station_id, dep_id, group_id, comp_id, grade_pay, pay_level, pay_basic, posted_at, permanent_address, present_address, permanent_identity, city, resi_address, representative, android_id, photo, signature, password, lang, status, hrms_id, mod_rec, is_approved, ex_is_approved, forced, created_by, created_at, updated_at
- hostel_buildings: id, office_id, building_name, bed_capacity, location, desi_id, sort_no, status, created_at, updated_at
- departments: id, service_id, office_id, department_name, sort_no, status, created_at, updated_at
- designations: id, grade_id, desi_name, desi_name_hindi, desi_code, desi_type, lecture, officer, office_id, leave_forward_id, desi_email, desi_phone, desi_fax, sort_no, status, created_at, updated_at
Columns:
- id
- office_id
- cm_no (Complaint number)
- building_id (joins with hostel_buildings.id)
- ctype_id (joins with complaint_cat.id)
- ctype_sub_id (joins with complaint_subcat.id)
- user_id (joins with users.id)
- description
- remarks
- cm_status (Complaint status: 0=Pending, 1=Forwarded, 2=Resolved, 3=Closed, etc.)
- status (1=active)
- created_at
- updated_at

Table: complaint_cat
Columns:
- id
- comp_name (Category name)
- status (1=active)

Table: complaint_subcat
Columns:
- id
- cat_id (joins with complaint_cat.id)
- subcat_name (Sub-category name)
- status (1=active)

Table: complaints_files
Columns:
- id
- cm_id (joins with complaints.id)
- file_name

Relationships:
- complaints.building_id = hostel_buildings.id
- complaints.ctype_id = complaint_cat.id
- complaints.ctype_sub_id = complaint_subcat.id
- complaints_files.cm_id = complaints.id
- complaint_subcat.cat_id = complaint_cat.id
- complaints.user_id = users.id

Common question mapping:
- Total complaints: Count complaints
- Pending complaints: Filter by cm_status (e.g. cm_status = 0 or cm_status = 1 depending on system, fallback to checking cm_status != 2 AND cm_status != 3)
- Complaint by category: Join with complaint_cat (c.ctype_id = cc.id) and select cc.comp_name
- Complaint by building: Join with hostel_buildings (c.building_id = hb.id) and select hb.building_name
- Complaint attachments: Query complaints_files
"""
