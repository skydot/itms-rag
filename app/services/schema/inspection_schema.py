"""Minified inspection schema."""

INSPECTION_SCHEMA = """
TRMS Inspection schema.
TRMS Inspection module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- inspection_description.insp_id = inspection_notes.id
- inspection_notes.created_by = users.id
- inspection_description.faculty_id = users.id
Common question mapping:
- Total inspections: Count inspection_notes
- Inspection by date: Filter from_date/to_date
- Inspection descriptions: Query inspection_description
- Inspection by faculty: Filter by created_by/faculty_id
"""
