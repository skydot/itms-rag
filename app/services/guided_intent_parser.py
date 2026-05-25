import json
import logging
from typing import Dict, Any

from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a TRMS guided-flow intent parser.
Return valid JSON only. No markdown. No explanation.
Do not generate SQL. Do not answer the user.
Your job: map a question to one guided flow and extract slots.

Guided flows:

1. exam_marks_by_trainee — marks/score of a specific trainee
Examples: "Mayank marks", "marks of Mayank", "mayank marks in recent exam"
Slots: trainee_name, course_name, exam_filter, exam_type_name, subject_name, year

2. exam_result_by_trainee — did trainee pass or fail
Examples: "Did Mayank pass?", "Mayank pass or fail?", "result of Mayank"
Slots: trainee_name, course_name, exam_filter, year

3. failed_trainees — list/count of failed trainees (NO trainee name needed)
Examples: "Show failed trainees", "How many failed?", "failed students in exam"
Slots: course_name, exam_type_name, subject_name, year

4. failed_trainees_by_subject — which subject has most failures
Examples: "Which subject has highest failed trainees?", "subject wise fail count"
Slots: course_name, exam_type_name, year

5. passed_trainees — list/count of passed trainees
Examples: "Show passed trainees", "How many passed?"
Slots: course_name, exam_type_name, subject_name, year

6. not_appeared_trainees — who did not appear / absent in exam
Examples: "Who did not appear?", "absent in exam", "not appeared trainees"
Slots: course_name, exam_type_name, subject_name, year

7. top_performers — highest marks / topper (NO trainee name needed)
Examples: "Who got highest marks?", "top 5 performers", "exam topper"
Slots: course_name, exam_type_name, subject_name, year, limit

8. lowest_performers — lowest marks (NO trainee name needed)
Examples: "Who got lowest marks?", "bottom 5 performers"
Slots: course_name, exam_type_name, subject_name, year, limit

9. subject_wise_marks_summary — average marks per subject
Examples: "Subject wise average marks", "subject wise performance"
Slots: course_name, exam_type_name, year

10. course_exam_summary — course wise pass/fail summary
Examples: "Course wise exam result", "pass fail summary by course"
Slots: year, course_name

11. re_exam_trainees — trainees in re-exam
Examples: "Show re-exam trainees", "re exam students"
Slots: course_name, year

12. pass_percentage — pass rate / percentage
Examples: "What is pass percentage?", "course pass percentage"
Slots: course_name, exam_type_name, subject_name, year

13. pending_dues_by_person — dues of a person
Slots: trainee_name, dues_type, year

14. hostel_room_of_trainee — room of a person
Slots: trainee_name, stay_filter

15. hostel_availability — available rooms/beds
Slots: building_name

16. attendance_by_trainee — attendance of a person
Slots: trainee_name, course_name, year

17. trainee_profile_by_name — basic details of a specific trainee
Examples: "Show Mayank details", "Mayank trainee profile"
Slots: trainee_name

18. active_trainee_count — count of active trainees
Examples: "How many active trainees are there?", "Active trainees count"
Slots: (none)

19. trainee_joined_by_year — trainees joined in a specific year
Examples: "How many trainees joined in 2025?", "Show trainees joined in 2025"
Slots: year

20. recent_course_trainees — trainees in recent/latest/current course
Examples: "How many students joined recent course?", "Trainees in latest course"
Slots: recent_filter (recent/latest/current/ongoing)

21. course_wise_trainee_count — trainee count per course
Examples: "Show course wise trainee count", "Course wise students"
Slots: (none)

22. batch_wise_trainee_count — trainee count per batch
Examples: "Show batch wise trainee count", "Batch wise students"
Slots: (none)

23. gender_wise_trainee_count — count of male and female trainees
Examples: "Gender wise trainee count", "How many male and female students?"
Slots: (none)

24. approved_trainees — approved trainees
Examples: "Show approved trainees", "How many approved trainees?"
Slots: (none)

25. pending_approval_trainees — trainees pending approval
Examples: "Show pending approval trainees", "How many trainees pending approval?"
Slots: (none)

26. outstay_trainees — trainees overstaying
Examples: "Show outstay trainees", "How many outstay students?"
Slots: (none)

exam_filter values: recent/latest/current/last/all/final/phase_1/phase_2/re_exam

Return JSON:
{"matches_guided_flow":true,"flow_id":"...","confidence":0.9,"slots":{...},"reason":"..."}
If unsure: {"matches_guided_flow":false,"flow_id":null,"confidence":0,"slots":{},"reason":"..."}

JSON only. No markdown.
"""

def parse_guided_intent(message: str) -> Dict[str, Any]:
    default_fallback = {
        "matches_guided_flow": False,
        "flow_id": None,
        "confidence": 0,
        "slots": {},
        "reason": "Not a guided flow question"
    }

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message}
    ]

    try:
        response_text = call_llm(messages, temperature=0, max_tokens=300)
        
        # Clean up possible markdown wrappers
        text = response_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        parsed = json.loads(text)
        print("[Guided Intent Parser] Message:", message)
        print("[Guided Intent Parser] Parsed:", parsed)

        # Handle smaller model quirks
        if "flow_id" in parsed and parsed["flow_id"]:
            if "matches_guided_flow" not in parsed:
                parsed["matches_guided_flow"] = True
            if "confidence" not in parsed:
                parsed["confidence"] = 1.0

        confidence = parsed.get("confidence", 0)
        if not parsed.get("matches_guided_flow") or confidence < 0.70:
            return default_fallback

        return parsed
    except Exception as e:
        logger.error(f"Error parsing guided intent: {e}")
        return default_fallback
