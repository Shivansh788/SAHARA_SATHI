import re
from typing import Dict, List, Literal, TypedDict

from langgraph.graph import END, StateGraph  # pyright: ignore[reportMissingImports]


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

FACT_ORDER = ["state", "category", "age", "occupation"]

QUESTION_MAP = {
    "state": "Which state are you currently residing in?",
    "category": "What is your social category (General/OBC/SC/ST/EWS)?",
    "age": "What is your age?",
    "occupation": "What is your occupation or life situation (farmer/student/widow/worker)?",
}


class IntakeProfile(TypedDict):
    language: str
    intent: str
    state: str
    category: str
    age: str
    occupation: str
    follow_up_questions: List[str]


class IntakeState(TypedDict):
    query: str
    session_id: str
    messages: List[Dict[str, str]]
    profile: IntakeProfile
    pending_questions: List[str]
    turn_count: int


def _extract_age(query: str) -> str:
    match = re.search(r"\b(?:my age is|i am)\s*(\d{1,3})\s*(?:years|yrs|year|yo|years old)?\b", query.lower())
    if not match:
        return ""
    age = int(match.group(1))
    if 0 < age < 120:
        return str(age)
    return ""


def _extract_first_match(query: str, values: List[str]) -> str:
    q = query.lower()
    for value in values:
        if value in q:
            return value
    return ""


def _infer_intent(query: str) -> str:
    q = query.lower()
    if any(word in q for word in ["apply", "application", "form", "document", "eligibility"]):
        return "application_guidance"
    if any(word in q for word in ["camp", "ngo", "clinic", "community", "event"]):
        return "community_support"
    return "scheme_search"


def _infer_language(query: str) -> str:
    q = query.lower()
    if any(word in q for word in ["yojana", "yojna", "yoj", "hai kya", "kaise"]):
        return "hinglish"
    if any(word in q for word in ["मैं", "हिंदी", "कृपया", "बताइए", "योजना", "पात्रता"]):
        return "hindi"
    return "english"


def _infer_occupation(query: str) -> str:
    q = query.lower()
    if "farmer" in q or "kisan" in q:
        return "farmer"
    if "widow" in q:
        return "widow"
    if "student" in q:
        return "student"
    if "labour" in q or "worker" in q:
        return "worker"
    return ""


def _normalize_existing_profile(existing_profile: Dict[str, str] | None) -> IntakeProfile:
    existing_profile = existing_profile or {}
    return {
        "language": str(existing_profile.get("language", "english") or "english"),
        "intent": str(existing_profile.get("intent", "scheme_search") or "scheme_search"),
        "state": str(existing_profile.get("state", "") or ""),
        "category": str(existing_profile.get("category", "") or ""),
        "age": str(existing_profile.get("age", "") or ""),
        "occupation": str(existing_profile.get("occupation", "") or ""),
        "follow_up_questions": list(existing_profile.get("follow_up_questions", []) or []),
    }


def _classify_node(state: IntakeState) -> IntakeState:
    query = state["query"]
    profile = dict(state["profile"])

    profile["language"] = _infer_language(query)
    profile["intent"] = _infer_intent(query)

    extracted_state = _extract_first_match(query, STATE_HINTS)
    extracted_category = _extract_first_match(query, CATEGORY_HINTS)
    extracted_age = _extract_age(query)
    extracted_occupation = _infer_occupation(query)

    if extracted_state:
        profile["state"] = extracted_state
    if extracted_category:
        profile["category"] = extracted_category
    if extracted_age:
        profile["age"] = extracted_age
    if extracted_occupation:
        profile["occupation"] = extracted_occupation

    state["profile"] = profile
    return state


def _question_node(state: IntakeState) -> IntakeState:
    if state["turn_count"] >= 4:
        return state

    profile = state["profile"]
    pending = list(state["pending_questions"])

    next_fact = ""
    for fact_key in FACT_ORDER:
        if not str(profile.get(fact_key, "") or ""):
            next_fact = fact_key
            break

    if not next_fact:
        return state

    next_question = QUESTION_MAP[next_fact]
    if next_question not in pending and len(pending) < 4:
        pending.append(next_question)
        state["turn_count"] = state["turn_count"] + 1

    state["pending_questions"] = pending
    profile["follow_up_questions"] = pending[:4]
    state["profile"] = profile
    return state


def _is_complete(state: IntakeState) -> Literal["question", "end"]:
    profile = state["profile"]
    all_facts_collected = all(str(profile.get(k, "") or "") for k in FACT_ORDER)
    if all_facts_collected or state["turn_count"] >= 4:
        return "end"
    return "question"


def _complete_node(state: IntakeState) -> IntakeState:
    profile = state["profile"]
    profile["follow_up_questions"] = list(state["pending_questions"])[:4]
    state["profile"] = profile
    return state


def _build_graph():
    builder = StateGraph(IntakeState)
    builder.add_node("classify", _classify_node)
    builder.add_node("question", _question_node)
    builder.add_node("complete", _complete_node)

    builder.set_entry_point("classify")
    builder.add_edge("classify", "question")
    builder.add_edge("question", "complete")
    builder.add_conditional_edges("complete", _is_complete, {"question": "question", "end": END})
    return builder.compile()


_INTAKE_GRAPH = _build_graph()


def run_intake_graph(query: str, session_id: str, existing_profile: Dict[str, str] | None = None) -> IntakeProfile:
    profile = _normalize_existing_profile(existing_profile)
    initial_state: IntakeState = {
        "query": query,
        "session_id": session_id,
        "messages": [{"role": "user", "content": query}],
        "profile": profile,
        "pending_questions": [],
        "turn_count": 0,
    }

    final_state = _INTAKE_GRAPH.invoke(initial_state)
    final_profile = final_state["profile"]

    return {
        "language": str(final_profile.get("language", "english") or "english"),
        "intent": str(final_profile.get("intent", "scheme_search") or "scheme_search"),
        "state": str(final_profile.get("state", "") or ""),
        "category": str(final_profile.get("category", "") or ""),
        "age": str(final_profile.get("age", "") or ""),
        "occupation": str(final_profile.get("occupation", "") or ""),
        "follow_up_questions": list(final_profile.get("follow_up_questions", []) or [])[:4],
    }
