"""Minified meeting schema."""

MEETING_SCHEMA = """
TRMS Meeting schema.
TRMS Meeting module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- meet_agenda.meeting_id = meeting_create.id
- mdl_calenders for scheduled meetings
- users for creator, chairman, invitee
Common question mapping:
- Total meetings: Count meeting_create
- Upcoming meetings: Filter by date >= CURDATE()
- Completed meetings: Filter by past dates
- Meeting agenda: Query meet_agenda
- Meetings by chairman: Filter by chairman field
"""
