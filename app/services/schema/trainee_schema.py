"""Trainee module schema for LLM SQL generation. Only table/column names — no credentials."""

TRAINEE_SCHEMA = """
TRMS Trainee schema.
status=1 means active. is_approved=1 means approved. office_id filters by office.
users table: trainee profile (name, mobile). tra_masters: enrollment info. training_calendars: batch dates. courses: course details.

Tables:
- tra_masters: id, user_id, ct_id, course_id, office_id, email, course_code, role, desi_id, service_id, grade_id, application_id, controlling_officer, zone_id, div_id, depo_id, station_id, dep_id, group_id, posted_at, certy_no, certy_approve, certi_ap_user, certi_ap_desi, representative, remarks, user_log, pass_file, nomination_letter, rank, local_trainee, status, out_stay, pass_status, is_approved, is_approved_date, created_at, updated_at
- users: id, role_id, office_id, user_code, user_type, desi_id, designation, parent_id, cti, prefix, name, mobile, whatsapp_number, emergency_numbers, office_mobile, emg_mobile_no, email, office_email, aadhar, uan, name_hindi, s_name, father_name, father_name_hindi, controlling_officer, experience_raill, gender, language, birth_date, date_of_appointment, railway_join_date, retire_date, posting_date, blood, pf_no, food, ph, merital, category, country_code, account_office, country, upsc_year, upsc_rank, upsc_state, organization, usefull, qualification, additional_qualification, bank_id, bank_acc, ifsc_code, service_id, grade_id, zone_id, div_id, depo_id, station_id, dep_id, group_id, comp_id, grade_pay, pay_level, pay_basic, posted_at, permanent_address, present_address, permanent_identity, city, resi_address, representative, android_id, photo, signature, password, lang, status, hrms_id, mod_rec, is_approved, ex_is_approved, forced, created_by, created_at, updated_at
- training_calendars: id, cf_id, ct_id, cg_id, office_id, course_code, batch_no, course_batch, program_name, program_name_hindi, class_id, from_date, to_date, extended_date, seat, exam_note, working_days, file_no, course_director, examiner, cd, cd_user_id, ccd, dir_desi_id, dir_user_id, ati, modes, mcdo, feedback, feedback_vl, place, short_code, cancel, reason, copy_by, fail_status, status, created_at, updated_at
- rail_zones: id, zone_name, zone_name_hindi, zone_code, type, zrti_type, status, sort_no, created_at, updated_at
- divisions: id, division, div_code, zone_id, sort_no, status, created_at, updated_at
- depots: id, depots, status, created_at, updated_at
- courses: id, cf_id, cg_id, office_id, course_name, course_name_hindi, cs_code, cs_description, cs_duration, week_days, certificate, feed_type, online_exam, sort_no, status, created_at, updated_at
- course_for: id, office_id, course_for, types, types_name, status, sort_no, created_at, updated_at
- cs_designs: id, cs_id, sub_id, office_id, topic_id, hours, desi_id, sec_id, topics_sort, subjects_sort, status, created_at, updated_at
- hostel_buildings: id, office_id, building_name, bed_capacity, location, desi_id, sort_no, status, created_at, updated_at
- hostel_masters: id, user_id, role_id, office_id, proom_type, person, amount, ct_id, course_id, train_no, ph, receipt_no, building_id, room_id, beds, food, in_date, out_date, days, item_id, mess, plusbed, remark, charge, total_charges, extra_room, preference, tour, hostel_dues, room_log, h_status, created_at, updated_at
- hostel_rooms: id, building_id, office_id, room_name, room_beds, r_category, floor, ac, toilet, remarks, sort_no, status, created_at, updated_at, direction

Relationships:
tra_masters.user_id = users.id
tra_masters.course_id = training_calendars.id
training_calendars.ct_id = courses.id

Mapping rules:
- filter by office: tra_masters.office_id = {office_id}
- by name: LOWER(users.name) LIKE LOWER('%name%')
- zone code: rail_zones.zone_code (e.g. 'NWR')
- hostel building: hostel_buildings.building_name LIKE '%Geetanjali%'
- recent/latest course: ORDER BY training_calendars.from_date DESC LIMIT 1
- ongoing: training_calendars.from_date <= CURDATE() AND training_calendars.to_date >= CURDATE()
- for only trainee use role_id=1 and for faculty use role_id=2 and and for Visiting Lecturer use role_id=3 for Guest use role_id=4 and for Zone User use role_id=5 and for Division User use role_id=6 and for Department User use role_id=7 
"""
