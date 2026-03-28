import re

from rag_modules.intake_graph import run_intake_graph


STATE_HINTS = [
    "rajasthan",
    "maharashtra",
    "uttar pradesh",
    "up",
    "bihar",
    "gujarat",
    "karnataka",
    "tamil nadu",
    "madhya pradesh",
    "mp",
    "odisha",
    "west bengal",
    "wb",
]

CATEGORY_HINTS = ["sc", "st", "obc", "general", "ews"]


def _extract_age(query):
    # Strict capture: only treat age as known when user explicitly states own age.
    match = re.search(r"\b(?:my age is|i am)\s*(\d{1,3})\s*(?:years|yrs|year|yo|years old)?\b", query.lower())
    if not match:
        return ""
    age = int(match.group(1))
    if 0 < age < 120:
        return str(age)
    return ""


def _extract_first_match(query, values):
    q = query.lower()
    for value in values:
        if value in q:
            return value
    return ""


def _infer_intent(query):
    q = query.lower()
    if any(word in q for word in ["apply", "application", "form", "document", "eligibility"]):
        return "application_guidance"
    if any(word in q for word in ["camp", "ngo", "clinic", "community", "event"]):
        return "community_support"
    return "scheme_search"


def intake_agent(query):
    profile = {
        "language": "english",
        "intent": _infer_intent(query),
        "state": "",
        "category": "",
        "age": "",
        "occupation": "",
        "follow_up_questions": [],
    }

    q = query.lower()

    if any(word in q for word in ["yojana", "yojna", "yoj", "hai kya", "kaise"]):
        profile["language"] = "hinglish"
    if any(word in q for word in ["मैं", "हिंदी", "कृपया", "बताइए", "योजना", "पात्रता"]):
        profile["language"] = "hindi"

    profile["state"] = _extract_first_match(q, STATE_HINTS)
    profile["category"] = _extract_first_match(q, CATEGORY_HINTS)
    profile["age"] = _extract_age(query)

    if "farmer" in q or "kisan" in q:
        profile["occupation"] = "farmer"
    elif "widow" in q:
        profile["occupation"] = "widow"
    elif "student" in q:
        profile["occupation"] = "student"
    elif "labour" in q or "worker" in q:
        profile["occupation"] = "worker"

    questions = []
    if not profile["state"]:
        questions.append("Which state are you currently residing in?")
    if not profile["category"]:
        questions.append("What is your social category (General/OBC/SC/ST/EWS)?")
    if not profile["age"]:
        questions.append("What is your age?")
    if not profile["occupation"]:
        questions.append("What is your occupation or life situation (farmer/student/widow/worker)?")

    profile["follow_up_questions"] = questions[:4]

    return profile


def intake_agent_graph(query, session_id, existing_profile=None):
    return run_intake_graph(query, session_id, existing_profile)