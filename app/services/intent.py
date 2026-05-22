def detect_intent(message: str) -> str:
    """
    Very simple intent detector for demo.

    Later this can be replaced by Groq/Ollama/LLM.
    For now keyword matching is enough.
    """

    text = message.lower()

    dashboard_words = ["dashboard", "report", "overview", "summary"]
    chart_words = ["chart", "graph", "bar", "line", "pie"]

    if any(word in text for word in dashboard_words):
        return "dashboard"

    if any(word in text for word in chart_words):
        return "chart"

    return "text"
