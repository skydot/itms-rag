import json
import logging
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Any, Literal

from app.services.llm_service import call_llm

logger = logging.getLogger(__name__)

class IntentResponse(BaseModel):
    intent_type: Literal["casual_chat", "procedural_help", "guided_query", "report_query", "action_query", "unclear"] = Field(
        ..., description="casual_chat | procedural_help | guided_query | report_query | action_query | unclear"
    )
    module: str = Field(default="", description="The module the query relates to")
    operation: str = Field(default="", description="The operation requested")
    slots: Dict[str, Any] = Field(default_factory=dict, description="Extracted slots")
    confidence: float = Field(default=0.0, description="Confidence score between 0.0 and 1.0")

def route_intent(question: str, history: list = None) -> IntentResponse:
    history_context = ""
    if history:
        history_lines = []
        for h in history:
            history_lines.append(f"User: {h.get('question', '')}")
            ans = h.get('answer', '')
            history_lines.append(f"Assistant: {ans[:150]}..." if len(ans) > 150 else f"Assistant: {ans}")
        history_context = "\nConversation History:\n" + "\n".join(history_lines) + "\n"

    prompt = f"""You are an Intent Router for a TRMS (Training Resource Management System) chatbot.
Classify the user's question into one of the following intent types and extract relevant structure.
If the user's question is a short follow-up (e.g. "what about mechanical?"), use the conversation history to infer the full intent.

Intent definitions:
- casual_chat: greetings, thanks, small talk, AND ALSO: random characters, numbers, math expressions (e.g. "1+1", "1-1"), special characters, gibberish words, meaningless text, anything that is NOT a clear TRMS-related question
- procedural_help: how to do something, process explanation, SOP questions, workflow guidance
- guided_query: information lookup, trainee details, hostel details, attendance details, leave details, complaints, inspections
- report_query: reports, statistics, counts, summaries, dashboards, analytics
- action_query: create, update, approve, reject, submit, workflow actions
- unclear: insufficient information, low confidence

IMPORTANT CLASSIFICATION RULES:
- If the message contains ONLY numbers, operators, or special characters (like "1-1", "2+2", "!!@@", "123"), classify as casual_chat.
- If the message is a random word or gibberish with no TRMS relevance (like "doo", "abc", "asdf", "lol"), classify as casual_chat.
- ONLY classify as guided_query or report_query if the message clearly mentions TRMS entities (trainees, exams, hostel, attendance, courses, etc.)

Modules mapping guide:
- exam: exam marks, exam results, passed/failed trainees, grades, performers, toppers, exam schedules, re-exam
- trainee: trainee profiles, trainee count, joined trainees, trainee approvals
- hostel: room allotment, building/room availability, occupancy, hostel buildings, empty rooms
- attendance: daily attendance, present, absent, biometric, punch time, attendance status/percentage
- course: course details, training calendars, batch, syllabus
- complaint: trainee complaints, resolver status, grievances
- timetable: class schedule, faculty timetable, class times
- faculty_vl: faculty details, faculty list, trainers
- library: books search, issued books, book availability, library card
- mess: mess dues, bill summary, food menu, mess receipts/refunds
- vehicle: vehicles list, vehicle availability, study tour transport
- meeting: committee meetings, agenda, minutes, schedules
- seminar: seminar topics, upcoming seminars, seminar count
- inspection: inspections, quality checks, inspectors
- sports: sports events, participants, team details, sports winners
- pass_eq: pass/equipment issue
- field_study_tour: field training, study tours
- master_admin: administrative master tables, system admin settings

Return strictly valid JSON only. No markdown formatting, no explanations.
Expected JSON format:
{{
  "intent_type": "casual_chat | procedural_help | guided_query | report_query | action_query | unclear",
  "module": "module name if applicable (must be one of: exam, trainee, hostel, course, attendance, timetable, faculty_vl, feedback, complaint, library, mess, vehicle, meeting, seminar, inspection, sports, pass_eq, field_study_tour, master_admin), else empty string",
  "operation": "operation name if applicable, else empty string",
  "slots": {{}},
  "confidence": 0.0
}}
{history_context}
User Question: {question}
"""
    
    def _call_and_parse(error_msg: str = ""):
        messages = [
            {"role": "system", "content": "You are a strict JSON router. Output valid JSON only."}
        ]
        if error_msg:
            messages.append({"role": "user", "content": prompt})
            messages.append({"role": "assistant", "content": "invalid json response"})
            messages.append({"role": "user", "content": f"The previous response failed validation: {error_msg}. Please fix it and return strictly valid JSON conforming to the schema."})
        else:
            messages.append({"role": "user", "content": prompt})
            
        try:
            content = call_llm(messages=messages, temperature=0.0, max_tokens=300)
            if not content:
                return "Empty response from LLM"
            content = content.replace("```json", "").replace("```", "").strip()
        except Exception as e:
            return f"LLM Call Error: {str(e)}"
        
        try:
            data = json.loads(content)
            return IntentResponse(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            return str(e)
            
    result = _call_and_parse()
    if isinstance(result, str):
        # Retry once
        retry_result = _call_and_parse(error_msg=result)
        if isinstance(retry_result, str):
            # Still failed
            intent = IntentResponse(intent_type="unclear", confidence=0.0)
        else:
            intent = retry_result
    else:
        intent = result
        
    log_msg = f"[ROUTER]\nquestion={question}\nintent={intent.intent_type}\nmodule={intent.module}\noperation={intent.operation}\nconfidence={intent.confidence}"
    logger.info(log_msg)
    print(log_msg)
    
    return intent
