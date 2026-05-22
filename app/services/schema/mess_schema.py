"""Minified mess schema."""

MESS_SCHEMA = """
TRMS Mess schema.
TRMS Mess module schema.
Important rules:
- status = 1 means active record where applicable.
- office_id is used for office-wise filtering where available.
- Always enforce office_id from backend/login context.

Tables:


Relationships:
- bill_details.bill_id = bills.id
- bill_receipts.bill_id = bills.id
- bill_receipts_refund.bill_id = bills.id
- mess_material for item details
Common question mapping:
- Total bills: Count bills
- Bill amount: Sum bill_details
- Pending dues: Sum bill_receipts_refund.due
- Receipts: Query bill_receipts
- Refunds: Query bill_receipts_refund
- Mess materials: Query mess_material
"""
