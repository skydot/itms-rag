"""Minified faculty_vl schema."""

FACULTY_VL_SCHEMA = """
TRMS Faculty_Vl schema.
TRMS Faculty and Visiting Lecturer (VL) module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- vl_management.id = vl_description.vlm_id
- vl_management joins with courses via vl_description
- feed_que_vls.vl_id -> vl_management.id
- users.id for faculty information
- subjects for subject details
Common question mapping:
- Total VLs: Count vl_management records
- VL by date: Filter vl_management.vl_date
- VL by subject: Filter vl_management.subject_name
- VL by course: Join with vl_description -> courses
- Faculty lecture schedule: Query vl_description
- VL payment: Sum vl_description.price
"""
