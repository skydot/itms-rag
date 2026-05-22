"""Minified vehicle schema."""

VEHICLE_SCHEMA = """
TRMS Vehicle schema.
TRMS Vehicle module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- vehicle_masters.user_id = users.id
- vehicle_masters.course_id = training_calendars.id
- vehicle_registers.study_id = study_tour.id
- study_tour.course_id = training_calendars.id
- field_training.course_id = training_calendars.id
Common question mapping:
- Vehicle bookings: Count vehicle_masters
- Upcoming trips: Filter by from_date > CURDATE()
- Completed trips: Filter by return_date < CURDATE()
- Vehicle by study tour: Join vehicle_registers with study_tour
- Vehicle by field training: Join with field_training
- KM summary: Aggregate distance if available
"""
