"""Minified sports schema."""

SPORTS_SCHEMA = """
TRMS Sports schema.
TRMS Sports module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- sport_team.program_id = sport.id
- particpants.program_id = sport.id
- particpants.team_id = sport_team.id
- sportitem_issue links to sport_item
- sport_material.party_id = partys.id
- sports_photos.sport_id = sport.id
Common question mapping:
- Total sports: Count sport
- Upcoming sports: Filter from_date >= CURDATE()
- Sports teams: Query sport_team
- Participants: Count particpants
- Sport items: Query sport_item
- Equipment issued: Query sportitem_issue
"""
