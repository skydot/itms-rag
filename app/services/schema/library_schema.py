"""Minified library schema."""

LIBRARY_SCHEMA = """
TRMS Library schema.
TRMS Library module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- book_issue links to users and books
- books may link to book_type
Common question mapping:
- Total books: Count books
- Issued books: Count book_issue where not returned
- Overdue books: book_issue with due date passed
- Books by type: Group by book_type
- Books issued to trainee: Filter by user_id
"""
