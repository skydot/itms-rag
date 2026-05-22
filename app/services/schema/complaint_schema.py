"""Minified complaint schema."""

COMPLAINT_SCHEMA = """
TRMS Complaint schema.
TRMS Complaint module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- complaints.building_id = hostel_buildings.id
- complaints_files.cm_id = complaints.id
- complaint_subcat.cat_id = complaint_cat.id
Common question mapping:
- Total complaints: Count complaints
- Pending complaints: Filter by status
- Complaint by category: Join with complaint_cat
- Complaint by building: Join with hostel_buildings
- Complaint attachments: Query complaints_files
"""
