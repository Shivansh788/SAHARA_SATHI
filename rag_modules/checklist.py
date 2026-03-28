BASE_DOCUMENTS = [
    "Aadhaar Card",
    "Passport-size photograph",
    "Bank passbook (first page)",
    "Self-declaration form",
]

CATEGORY_DOCUMENTS = {
    "sc": [
        "Caste certificate (issued by tehsildar or above)",
        "Income certificate",
    ],
    "st": [
        "Caste certificate (issued by tehsildar or above)",
        "Income certificate",
    ],
    "obc": [
        "OBC non-creamy layer certificate",
        "Income certificate",
    ],
    "ews": [
        "EWS income certificate",
        "Property declaration",
    ],
    "general": [],
}

STATE_DOCUMENTS = {
    "rajasthan": [
        "Bhamashah/Jan Aadhaar card",
    ],
    "maharashtra": [
        "MahaDBT registration acknowledgement",
        "Domicile certificate",
    ],
    "uttar pradesh": [
        "UP residence (niwas) certificate",
        "Family register copy (Kutumb Register)",
    ],
    "bihar": [
        "Bihar residence certificate",
        "RTPS acknowledgement slip (if applied online)",
    ],
    "gujarat": [
        "e-Samaj Kalyan registration proof",
        "Gujarat domicile certificate",
    ],
}

OCCUPATION_DOCUMENTS = {
    "farmer": [
        "Kisan Credit Card or land records (Khasra/Khatauni)",
        "Soil health card if applicable",
    ],
    "widow": [
        "Death certificate of spouse",
        "Marriage certificate",
    ],
    "student": [
        "School/college enrollment certificate",
        "Previous year marksheet",
    ],
    "worker": [
        "Labour card or BOCW registration",
        "Employer certificate if applicable",
    ],
}


def get_checklist(profile: dict) -> list:
    profile = profile if isinstance(profile, dict) else {}

    category = str(profile.get("category", "") or "").lower()
    state = str(profile.get("state", "") or "").lower()
    occupation = str(profile.get("occupation", "") or "").lower()

    checklist = list(BASE_DOCUMENTS)
    checklist.extend(CATEGORY_DOCUMENTS.get(category, []))
    checklist.extend(STATE_DOCUMENTS.get(state, []))
    checklist.extend(OCCUPATION_DOCUMENTS.get(occupation, []))

    deduped = []
    seen = set()
    for item in checklist:
        if item not in seen:
            seen.add(item)
            deduped.append(item)

    return deduped
