"""Minified attendance schema."""

ATTENDANCE_SCHEMA = """
TRMS Attendance schema.
TRMS Attendance module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- attendances.user_id = users.id
- attendances.course_id = training_calendars.id
- tra_masters.user_id = users.id
- tra_masters.ct_id = training_calendars.id
- training_calendars.ct_id = courses.id
- users.office_id for office filtering
Common question mapping:
- Attendance by date: Filter DATE(attendances.punch_time)
- Present trainees: attendances.punch = '4'
- Absent trainees: attendances.punch = '5'
- On Leave (CL/LAP/SL): attendances.punch IN ('1', '2', '3')
- Punch status meaning: 4=Present, 5=Absent(AB), 1=CL, 2=LAP, 3=SL
- Punch count: Count attendances records
- Course-wise attendance: Group by training_calendars -> courses

Rules:
- attendances.user_id joins with users.id.
- attendances.course_id joins with training_calendars.id.
"""
