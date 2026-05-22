"""Minified field_study_tour schema."""

FIELD_STUDY_TOUR_SCHEMA = """
TRMS Field_Study_Tour schema.
TRMS Field Training and Study Tour module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- field_training.course_id = training_calendars.id
- study_tour.course_id = training_calendars.id
- filled_training_data.filled_id = field_training.id
- vehicle_registers.study_id = study_tour.id
- filled_training_data.zone_id = rail_zones.id
- filled_training_data.div_id = divisions.id
Common question mapping:
- Field trainings: Count field_training
- Study tours: Count study_tour
- Upcoming tours: Filter by year/current date
- Vehicle assigned: Join with vehicle_registers
- Trainee count: Count filled_training_data
- Zone-wise: Group by rail_zones
"""
