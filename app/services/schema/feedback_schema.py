"""Minified feedback schema."""

FEEDBACK_SCHEMA = """
TRMS Feedback schema.
TRMS Feedback module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- feed_master.user_id = users.id
- feed_master.course_id = training_calendars.id
- training_calendars.ct_id = courses.id
- feed_master.fq_id = feed_que.fq_id
- feed_master.fs_id = feed_section.fs_id
- feed_que_vls.vl_id = vl_management.id
Common question mapping:
- Total feedback: Count feed_master
- Feedback by course: Group by course_id
- Question-wise feedback: Join feed_master with feed_que
- Average rating: Aggregate feed_master.response
- Feedback pending: Users without feed_master entry
- VL feedback: Query feed_que_vls
"""
