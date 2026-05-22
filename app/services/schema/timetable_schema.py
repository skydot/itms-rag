"""Minified timetable schema."""

TIMETABLE_SCHEMA = """
TRMS Timetable schema.
TRMS Timetable module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- time_masters.course_id -> training_calendars.id
- tt_designs.course_id -> training_calendars.id
- tt_designs_daywise.tt_design_id -> tt_designs.id
- tt_designs_daywise.course_id -> training_calendars.id
- tt_designs_daywise.subject_id -> subjects.id
- tt_designs_daywise.class_room_id -> class_rooms.id
- training_calendars.ct_id -> courses.id
- vl_management for visiting lecturer sessions
Common question mapping:
- Today's timetable: Filter by current date on tt_designs_daywise
- Weekly timetable: Group by day of week
- Course timetable: Filter by course_id
- Faculty timetable: Join with users/faculty
- VL lectures: Query vl_management
- Classroom usage: Query class_rooms with timetable
"""
