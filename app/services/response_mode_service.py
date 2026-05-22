"""
Response Mode Detection Service

Determines whether a chatbot response should be:
- "chat": Direct text answer in chat
- "report": Generate HTML report with link
"""

import re


def detect_response_mode(
    user_question: str,
    result_type: str = None,
    row_count: int = 0
) -> str:
    """
    Detect whether response should be chat or report mode.
    
    Args:
        user_question: The user's original question
        result_type: Type of result (e.g., "list", "detail", "count", "summary")
        row_count: Number of rows in the result
        
    Returns:
        "chat" or "report"
    """
    text = user_question.lower().strip()
    
    # Keywords that indicate chat mode (count/KPI questions)
    CHAT_KEYWORDS = [
        "how many", "how much", "count", "total", "percentage", "average",
        "highest", "lowest", "max", "min", "mean", "avg"
    ]
    
    # Check for chat keywords first (high priority)
    for keyword in CHAT_KEYWORDS:
        if keyword in text:
            return "chat"
    
    # Keywords that indicate report mode (list/detail questions)
    REPORT_KEYWORDS = [
        "show", "list", "details", "detail", "all", "report", "records",
        "download", "export", "give me list", "show me", "display",
        "view", "get", "find", "search", "fetch", "retrieve"
    ]
    
    # Check for report keywords
    for keyword in REPORT_KEYWORDS:
        if keyword in text:
            return "report"
    
    # Check result_type indicators
    if result_type:
        result_type_lower = result_type.lower()
        if result_type_lower in ["list", "detail", "details", "records"]:
            return "report"
        if result_type_lower in ["count", "summary", "single", "one"]:
            return "chat"
    
    # If row count is high, prefer report mode
    if row_count > 10:
        # But double-check for chat keywords (override)
        for keyword in ["how many", "count", "total"]:
            if keyword in text:
                return "chat"
        return "report"
    
    # Default to chat for small results
    return "chat"


def should_generate_report(
    user_question: str,
    result_type: str = None,
    row_count: int = 0
) -> bool:
    """
    Convenience function to check if report should be generated.
    
    Returns True if mode is "report", False otherwise.
    """
    return detect_response_mode(user_question, result_type, row_count) == "report"
