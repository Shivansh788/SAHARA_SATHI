def intake_agent(query):
    profile = {
        "language": "english",
        "intent": "scheme_search"
    }

    # simple detection
    if any(word in query.lower() for word in ["yojana", "yojna", "yoj"]):
        profile["language"] = "hinglish"

    return profile