import json
import logging
from typing import Dict, Any, Tuple, List
from app.services.smart_query_service import QUERY_TEMPLATES
from app.services.llm_service import call_llm
from app.services.smart_query_service import get_relevant_templates

logger = logging.getLogger(__name__)

def select_query_and_extract_params(question: str, module_hint: str = "", history: list = None) -> Tuple[str, Dict[str, Any], float]:
    """
    Step 1 & 2: Query Selection and Parameter Extraction.
    Returns (query_id, params, confidence)
    """
    # Get relevant templates to limit context
    allowed_templates = get_relevant_templates(question)
    
    # If no templates found from keyword heuristic, we can fallback to all module templates if we have a hint
    if not allowed_templates and module_hint:
        allowed_templates = [t for t in QUERY_TEMPLATES if t.get("module") == module_hint]

    if not allowed_templates:
        # If absolutely no templates, we have no query to select
        return "NONE", {}, 0.0

    template_summaries = []
    for t in allowed_templates:
        summary = {
            "id": t["id"],
            "description": t["description"],
            "required_params": t.get("required_params", []),
            "optional_params": t.get("optional_params", [])
        }
        template_summaries.append(summary)

    history_context = ""
    if history:
        history_lines = []
        for h in history:
            history_lines.append(f"User: {h.get('question', '')}")
            ans = h.get('answer', '')
            history_lines.append(f"Assistant: {ans[:150]}..." if len(ans) > 150 else f"Assistant: {ans}")
        history_context = "\nConversation History:\n" + "\n".join(history_lines) + "\n"

    prompt = f"""You are a strict Query Selection and Parameter Extraction agent for a TRMS system.
Your task is to map the user's question to exactly ONE predefined query_id from the Allowed Queries list.
You must ALSO extract ALL required and optional parameters for that query from the user's question and conversation history.

Allowed Queries:
{json.dumps(template_summaries, indent=2)}

{history_context}
User Question: {question}

Return STRICT JSON ONLY with the following schema:
{{
  "query_id": "THE_SELECTED_ID_OR_NONE",
  "parameters": {{
    "param_name": "extracted_value"
  }},
  "confidence": 0.95
}}

Extraction Rules:
- Do NOT hallucinate parameters. If a parameter is not mentioned, do NOT include it.
- Ensure the query_id perfectly matches what the user is asking. If it doesn't match well, set query_id to "NONE" and confidence to 0.0.
- date: Extract date in YYYY-MM-DD format if explicitly given or calculable.
- month: Extract month number (1-12) ONLY if a TEXT NAME of a month (like January, December) is explicitly used. NEVER extract this if the user says "last 12 months" or similar.
- year: Extract any 4-digit year mentioned.
- limit: Extract count if user says "top 5" or "top 20" etc.
- search_name: Extract person name if mentioned.
- building_name: Extract building/hostel name if mentioned.
- room_name: Extract room number if mentioned.
- gender: Extract "male" or "female" if mentioned.
- course_name: Extract actual training course or program name if mentioned.
"""

    messages = [
        {"role": "system", "content": "You are a strict JSON generator. Output valid JSON only. No markdown formatting."},
        {"role": "user", "content": prompt}
    ]

    try:
        content = call_llm(messages=messages, temperature=0.0, max_tokens=300)
        if not content:
            return "NONE", {}, 0.0
        content = content.replace("```json", "").replace("```", "").strip()
        data = json.loads(content)
        query_id = data.get("query_id", "NONE")
        params = data.get("parameters", {})
        confidence = float(data.get("confidence", 0.0))
        
        logger.info(f"[QUERY REGISTRY] Selected {query_id} with confidence {confidence}. Params: {params}")
        return query_id, params, confidence
    except Exception as e:
        logger.error(f"[QUERY REGISTRY] Error extracting query: {e}")
        return "NONE", {}, 0.0

def validate_parameters(query_id: str, params: Dict[str, Any]) -> List[str]:
    """
    Step 3: Validate required parameters.
    Returns a list of missing parameters.
    """
    template = next((t for t in QUERY_TEMPLATES if t.get("id") == query_id), None)
    if not template:
        return []
    
    missing = []
    for req in template.get("required_params", []):
        if req not in params or not str(params[req]).strip():
            missing.append(req)
    return missing
