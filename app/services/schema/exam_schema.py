"""Exam module schema for LLM SQL generation. Only table/column names — no credentials."""

EXAM_SCHEMA = """
TRMS Exam schema.
status=1 means active. office_id filters by office. result: 1=Pass, 2=Fail.

Tables:
- courses: id, office_id, course_name, status
- et_design: id, course_id, subject, exam_date, status
- exam_design: id, cs_id, subject_id, total_marks, minimum_marks, office_id, status
- exam_marks: id, user_id, course_id, exam_type_id, subject_id, mark_obtained, total_mark, result, status
- exam_type: id, office_id, title, status
- subjects: id, subject_name, status
- users: id, office_id, name, mobile, email, status
- training_calendars: id, ct_id, office_id, course_batch, from_date, to_date, status

Relationships:
exam_marks.user_id = users.id
exam_marks.course_id = training_calendars.id
training_calendars.ct_id = courses.id
exam_marks.subject_id = subjects.id
exam_marks.exam_type_id = exam_type.id

Mapping rules:
- filter by office: exam_marks.office_id = {office_id} or courses.office_id = {office_id}
- pass/fail: exam_marks.result = 1 (Pass) or 2 (Fail)
- recent exam: ORDER BY exam_marks.created_at DESC LIMIT 1
- top/highest marks: ORDER BY exam_marks.mark_obtained DESC LIMIT 1
"""
