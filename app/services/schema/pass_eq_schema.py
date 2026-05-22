"""Minified pass_eq schema."""

PASS_EQ_SCHEMA = """
TRMS Pass_Eq schema.
TRMS Pass and EQ module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- pass.user_id = users.id
- pass.pass_type = pass_type.id
- eqs.user_id = users.id
- eqs.course_id = training_calendars.id
Common question mapping:
- Total pass requests: Count pass
- Pending pass: Filter by status
- Approved pass: Filter by status
- Pass by type: Join with pass_type
- EQ requests: Count eqs
- EQ by journey date: Filter eqs.journey_date
- Train class summary: Group by train_class
"""
