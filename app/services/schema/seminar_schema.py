"""Minified seminar schema."""

SEMINAR_SCHEMA = """
TRMS Seminar schema.
TRMS Seminar module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- seminars.topic_id = topics.id
- seminars_topic for sub-topic details
- vl_management for VL-led seminars
Common question mapping:
- Total seminars: Count seminars
- Upcoming seminars: Filter sem_date >= CURDATE()
- Completed seminars: Filter sem_date < CURDATE()
- Seminar by topic: Join with seminars_topic
- Seminar by speaker: Filter by subject/speaker
"""
