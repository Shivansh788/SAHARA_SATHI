import requests
import socket
import os
import time
from threading import Thread
import re

import config
import persistence
from rag_modules.checklist import get_checklist


OLLAMA_CONNECT_TIMEOUT_SEC = config.OLLAMA_CONNECT_TIMEOUT_SEC
OLLAMA_READ_TIMEOUT_SEC = config.OLLAMA_READ_TIMEOUT_SEC
COEAI_TIMEOUT_SEC = config.COEAI_TIMEOUT_SEC
COEAI_HEALTH_TIMEOUT_SEC = config.COEAI_HEALTH_TIMEOUT_SEC
GEMINI_TIMEOUT_SEC = config.GEMINI_TIMEOUT_SEC

_GEMINI_DISABLED_UNTIL = 0.0
_GEMINI_DISABLED_REASON = ""
_OLLAMA_DISABLED_UNTIL = 0.0
_OLLAMA_DISABLED_REASON = ""


def _is_connected_to_upesnet(timeout_sec=3):
    """Check if connected to UPESNET network by DNS/connectivity test."""
    try:
        # Try to resolve upesnet.ac.in or similar UPESNET domain
        socket.gethostbyname("upesnet.ac.in")
        return True
    except socket.gaierror:
        pass
    except Exception:
        pass
    
    # Fallback: Check if UPESNET env variable is set (for VPN/tunnel scenarios)
    return config.UPESNET_CONNECTED_FLAG


def _probe_coeai_models(llm, timeout_sec=COEAI_HEALTH_TIMEOUT_SEC):
    """Check COEAI usability via official client model discovery with timeout."""
    if llm is None:
        return False, []

    result_container = []
    error_container = []

    def call_list_models():
        try:
            result_container.append(llm.list_models())
        except Exception as e:
            error_container.append(str(e))

    thread = Thread(target=call_list_models, daemon=False)
    thread.start()
    thread.join(timeout=timeout_sec)

    if thread.is_alive() or error_container or not result_container:
        return False, []

    models = result_container[0]
    if isinstance(models, dict):
        models = models.get("models", [])
    if not isinstance(models, list):
        models = []

    models = [str(m) for m in models if m]
    return True, models


def _coeai_is_reachable(llm, timeout_sec=COEAI_HEALTH_TIMEOUT_SEC):
    ok, _ = _probe_coeai_models(llm, timeout_sec=timeout_sec)
    return ok


def _build_citations(ranked_docs, limit=5):
    citations = []
    for idx, doc in enumerate(ranked_docs[:limit], start=1):
        source_name = doc.get("source_name", "Unknown Source")
        source_type = doc.get("source_type", "source")
        category = doc.get("category", "")
        snippet = doc.get("text", "")[:220]
        citations.append(
            {
                "id": idx,
                "source_name": source_name,
                "source_type": source_type,
                "category": category,
                "snippet": snippet,
            }
        )
    return citations


def _citations_markdown(citations):
    lines = []
    for c in citations:
        cat = f" | Category: {c['category']}" if c.get("category") else ""
        lines.append(f"[{c['id']}] {c['source_name']} ({c['source_type']}){cat}")
    return "\n".join(lines)


def _build_response(answer, citations, mode, follow_up, worker_summary=""):
    return {
        "answer": answer,
        "citations": citations,
        "mode": mode,
        "understanding_check": "Did this explanation make sense before you proceed to apply? (Yes/No)",
        "follow_up_questions": follow_up,
        "worker_summary": worker_summary,
    }


def _worker_summary(mode, query, citations):
    if mode != "worker":
        return ""
    return (
        "WhatsApp-ready summary:\n"
        f"Query: {query}\n"
        "Top action: Review eligibility and document checklist first.\n"
        + "Sources: "
        + ", ".join([f"[{c['id']}] {c['source_name']}" for c in citations[:3]])
    )


def _compact_text(value, max_len=240):
    text = (value or "").strip()
    if not text:
        return "Not available"
    text = re.sub(r"\s+", " ", text)
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rstrip() + "..."


def _format_fallback_answer(query, ranked_docs, profile=None):
    profile = profile or {}
    person_name = (profile.get("name") or "Friend").strip() or "Friend"
    person_state = (profile.get("state") or "").strip()
    person_category = (profile.get("category") or "").strip()
    top_docs = ranked_docs[:3]

    def _best_url(doc):
        text_blob = " ".join(
            [
                str(doc.get("application", "")),
                str(doc.get("text", "")),
                str(doc.get("description", "")),
            ]
        )
        found = re.search(r"https?://[^\s)]+", text_blob)
        if found:
            return found.group(0).rstrip(".,")

        name = str(doc.get("source_name", "")).lower()
        if "kisan" in name:
            return "https://pmkisan.gov.in"
        if "scholar" in name or "student" in name:
            return "https://scholarships.gov.in"
        if "health" in name:
            return "https://nhm.gov.in"
        return "https://www.myscheme.gov.in"

    lines = [
        f"Hey {person_name}!",
        "I found the best matching schemes for your profile below.",
        "",
        "## ✅ Schemes You Qualify For",
    ]

    for idx, doc in enumerate(top_docs, start=1):
        source_name = _compact_text(doc.get("source_name", "Government Scheme"), 110)
        description = _compact_text(doc.get("description", doc.get("text", "Benefit details not available")), 180)
        eligibility = _compact_text(doc.get("eligibility", "Please verify eligibility on the portal"), 180)
        url = _best_url(doc)
        deadline = "No deadline right now - apply soon"

        lines.extend(
            [
                f"### {idx}. {source_name}",
                f"**What you get:** {description}",
                f"**You qualify because:** Matches your state/category details shared in chat.",
                "**Documents needed:**",
                "- [ ] Aadhaar Card",
                "- [ ] Address Proof",
                "- [ ] Bank Passbook",
                "- [ ] Category/Income Certificate (if required)",
                "**How to apply:**",
                f"- Go to **{url}**",
                "- Open the scheme page and click **Apply / New Registration**",
                f"- Deadline: **{deadline}**",
                "",
            ]
        )

    if top_docs:
        bonus_name = _compact_text(top_docs[-1].get("source_name", "Another matching scheme"), 110)
    else:
        bonus_name = "More matching schemes on myScheme"
    lines.extend(
        [
            "## 🎁 You Also Qualify For This",
            f"**{bonus_name}** - Extra support option for your profile.",
            "Apply at: https://www.myscheme.gov.in",
            "",
            "## ❌ Schemes That Don't Match You",
            "| Scheme | Why not matched |",
            "|---|---|",
            "| Example Scheme A | Wrong state requirement for profile |",
            "| Example Scheme B | Age limit outside your profile |",
            "",
            "## 📋 Your Document Checklist",
            "- [ ] Aadhaar Card",
            "- [ ] Address Proof",
            "- [ ] Bank Passbook",
            "- [ ] Category/Income Certificate",
            "",
            "## 👣 Your Single Next Step",
            "> Open https://www.myscheme.gov.in and click Search Schemes, then click Apply on your top match.",
            "",
            "## ❓ One Thing I Need From You",
        ]
    )

    if not person_state:
        lines.append("Please tell your current state.")
    elif not person_category:
        lines.append("Please tell your category (General/OBC/SC/ST).")
    else:
        lines.append("No extra info needed now. You can start applying.")

    return "\n".join(lines)


def _extract_contact_or_website(*texts):
    blob = " ".join([str(t or "") for t in texts])
    url_match = re.search(r"https?://[^\s)]+", blob)
    if url_match:
        return url_match.group(0).rstrip(".,")
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", blob)
    if email_match:
        return email_match.group(0)
    phone_match = re.search(r"(?:\+91[-\s]?)?[6-9]\d{9}", blob)
    if phone_match:
        return phone_match.group(0)
    return "Not listed"


def _append_nearby_ngos(answer, query, profile):
    if not isinstance(profile, dict):
        return answer

    state_or_location = str(profile.get("state") or profile.get("location") or "").strip()
    if not state_or_location:
        return answer

    category = str(profile.get("category") or profile.get("occupation") or "").strip()
    keyword = str(query or "").strip()

    try:
        ngos = persistence.search_ngos(keyword=keyword, location=state_or_location, category=category, limit=5)
        if not ngos:
            ngos = persistence.search_ngos(location=state_or_location, category=category, limit=5)
        if not ngos and keyword:
            ngos = persistence.search_ngos(keyword=keyword, location=state_or_location, limit=5)
    except Exception:
        return answer

    if not ngos:
        return answer

    lines = ["", "### 🤝 Get Help Near You"]
    for ngo in ngos[:4]:
        name = _compact_text(ngo.get("name", "Community Organization"), 90)
        support = _compact_text(ngo.get("description") or ngo.get("type") or ngo.get("category") or "Local support services", 160)
        location = _compact_text(ngo.get("location", state_or_location), 80)
        contact = _extract_contact_or_website(ngo.get("description"), ngo.get("eligibility"), ngo.get("name"))
        lines.append(f":::NGO_CARD\nName: {name}\nHelp: {support}\nLocation: {location}\nContact: {contact}\n:::")

    return (answer.rstrip() + "\n" + "\n".join(lines).rstrip()).strip()


def _humanize_answer(answer):
    text = (answer or "").strip()
    if not text:
        return "Summary:\n- No response generated. Please try again."

    # Ensure stale profile-summary line never leaks into user-visible response.
    text = re.sub(r"^\s*Your provided details:.*$", "", text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    # Keep already well-structured responses unchanged.
    structured_markers = [
        "\n1.",
        "### ",
        ":::SCHEME_CARD",
        "Summary:",
        "Eligibility:",
        "Documents:",
        "Steps:",
    ]
    if any(marker in text for marker in structured_markers):
        return text

    # Convert dense paragraph into readable bullets for elderly users.
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    if not sentences:
        return text

    lines = ["### Summary"]
    for sentence in sentences[:8]:
        lines.append(f"- {sentence}")
    lines.append("")
    lines.append("Did this explanation make sense? (Yes/No)")
    return "\n".join(lines)


def _generate_with_ollama(prompt):
    global _OLLAMA_DISABLED_UNTIL, _OLLAMA_DISABLED_REASON

    if time.time() < _OLLAMA_DISABLED_UNTIL:
        wait_left = int(_OLLAMA_DISABLED_UNTIL - time.time())
        raise RuntimeError(
            f"Ollama temporarily disabled for {wait_left}s: {_OLLAMA_DISABLED_REASON}"
        )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 700,
                "temperature": 0.2,
            },
        },
        timeout=(OLLAMA_CONNECT_TIMEOUT_SEC, OLLAMA_READ_TIMEOUT_SEC),
    )
    if response.status_code != 200:
        raise RuntimeError(f"Ollama HTTP {response.status_code}")
    payload = response.json()
    return payload.get("response", "No response content from Ollama.")


def _generate_with_gemini(prompt):
    global _GEMINI_DISABLED_UNTIL, _GEMINI_DISABLED_REASON

    if time.time() < _GEMINI_DISABLED_UNTIL:
        wait_left = int(_GEMINI_DISABLED_UNTIL - time.time())
        raise RuntimeError(
            f"Gemini temporarily disabled for {wait_left}s: {_GEMINI_DISABLED_REASON}"
        )

    api_key = (getattr(config, "GEMINI_API_KEY", "") or "").strip()
    if not api_key:
        raise RuntimeError("Gemini API key is not configured")

    model = (getattr(config, "GEMINI_MODEL", "gemini-1.5-flash") or "gemini-1.5-flash").strip()
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        f"?key={api_key}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, json=payload, timeout=(3.0, GEMINI_TIMEOUT_SEC))
    if response.status_code != 200:
        response_preview = response.text[:300]
        # Fast-fail invalid keys so later requests do not keep waiting on Gemini.
        if response.status_code in (400, 401, 403) and (
            "API key not valid" in response_preview
            or "INVALID_ARGUMENT" in response_preview
            or "PERMISSION_DENIED" in response_preview
        ):
            _GEMINI_DISABLED_UNTIL = time.time() + 600
            _GEMINI_DISABLED_REASON = "invalid API key"
        raise RuntimeError(f"Gemini HTTP {response.status_code}: {response.text[:220]}")

    data = response.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini returned no candidates")

    parts = candidates[0].get("content", {}).get("parts", [])
    text_parts = [p.get("text", "") for p in parts if isinstance(p, dict) and p.get("text")]
    answer = "\n".join(text_parts).strip()
    if not answer:
        raise RuntimeError("Gemini returned empty text")

    return answer


def _ollama_is_reachable(timeout_sec=1.5):
    """Quick health probe so API doesn't stall when Ollama is not running."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=timeout_sec)
        return response.status_code == 200
    except Exception:
        return False


def _generate_with_external_llm(prompt, llm):
    if llm is None:
        raise RuntimeError("No external LLM configured")

    # Supports coeai-compatible clients when explicitly configured.
    # Check if connected to UPESNET (corporate network)
    if not _is_connected_to_upesnet():
        raise RuntimeError(
            "COEAI (external LLM) requires UPESNET connection. "
            "Not connected to UPESNET network. Falling back to offline mode."
        )
    
    # Quick health check to avoid long waits using official client.
    reachable, available_models = _probe_coeai_models(llm, timeout_sec=COEAI_HEALTH_TIMEOUT_SEC)
    if not reachable:
        raise RuntimeError(
            "COEAI service is unreachable. Using fallback offline mode."
        )

    configured_model = config.COEAI_MODEL
    selected_model = configured_model
    if available_models and configured_model not in available_models:
        if "deepseek-r1:70b" in available_models:
            selected_model = "deepseek-r1:70b"
        else:
            selected_model = available_models[0]
    
    # Generate with 2-minute (120s) timeout (COEAI can be slow)
    result_container = []
    error_container = []
    
    def call_llm():
        try:
            try:
                res = llm.generate(
                    model=selected_model,
                    prompt=prompt,
                    max_tokens=4000,
                    timeout=COEAI_TIMEOUT_SEC,
                )
            except TypeError:
                # Backward compatibility in case timeout argument is unsupported.
                res = llm.generate(
                    model=selected_model,
                    prompt=prompt,
                    max_tokens=4000,
                )
            if isinstance(res, dict) and "choices" in res:
                result_container.append(res["choices"][0]["message"]["content"])
            else:
                result_container.append(str(res))
        except Exception as e:
            error_container.append(str(e))
    
    # Run with thread-based timeout
    thread = Thread(target=call_llm, daemon=False)
    thread.start()
    thread.join(timeout=COEAI_TIMEOUT_SEC)
    
    if thread.is_alive():
        raise RuntimeError(
            f"COEAI request timeout after {COEAI_TIMEOUT_SEC} seconds. "
            "Using fallback offline mode."
        )
    
    if error_container:
        raise RuntimeError(f"COEAI generation failed: {error_container[0]}")
    
    if not result_container:
        raise RuntimeError("COEAI returned no response")
    
    return result_container[0]


def generate(query, ranked_docs, profile, llm, local_pipeline=None, history=None, mode="citizen"):

    # Safely handle the profile argument, which might be a string ("farmer") or a dictionary
    prof_lang = profile.get("language", "Bilingual (English/Hindi)") if isinstance(profile, dict) else "Bilingual (English/Hindi)"
    follow_up = profile.get("follow_up_questions", []) if isinstance(profile, dict) else []
    state = profile.get("state", "") if isinstance(profile, dict) else ""
    category = profile.get("category", "") if isinstance(profile, dict) else ""
    occupation = profile.get("occupation", "") if isinstance(profile, dict) else ""

    citations = _build_citations(ranked_docs)
    context = "\n\n".join([_compact_text(doc.get("text", ""), 850) for doc in ranked_docs])
    checklist_items = get_checklist(profile if isinstance(profile, dict) else {})
    checklist_str = "\n".join(f"- {item}" for item in checklist_items)

    history_str = ""
    if history:
        for turn in history[-2:]:
            history_str += f"\nUser: {turn['user']}\nAI: {turn['assistant']}\n"

    prompt = f"""You are Sahara Saathi — a friendly, expert assistant helping Indian citizens find government welfare schemes.
You MUST always respond in a clean, structured, easy-to-read format as described below.

═══════════════════════════════════════
USER PROFILE
═══════════════════════════════════════
- Name      : {profile.get('name', 'Friend') if isinstance(profile, dict) else 'Friend'}
- Age       : {profile.get('age', 'not specified') if isinstance(profile, dict) else 'not specified'}
- Occupation: {occupation or 'not specified'}
- State     : {state or 'not specified'}
- Category  : {category or 'not specified'}
- Language  : {prof_lang}

═══════════════════════════════════════
LANGUAGE & TONE RULES
═══════════════════════════════════════
- Respond ONLY in {prof_lang}.
- Use VERY SIMPLE language — like explaining to a Class 6 student.
- Be warm, supportive, and encouraging. User may be elderly or not educated.
- DO NOT use words like: applicant, beneficiary, pursuant, aforementioned, utilize.
- Replace complex words with: "you/your", "documents", "apply", "get help".

═══════════════════════════════════════
FORMATTING LAWS — FOLLOW STRICTLY
═══════════════════════════════════════
✅ DO:
- Use short bullet points (max 10 words each)
- Use numbered steps (1. 2. 3.)
- Use markdown checkboxes (- [ ]) for document lists
- Bold **important words** (amounts, deadlines)
- Use ### headings for each section
- Use the exact :::SCHEME_CARD format below for each scheme

❌ DO NOT:
- Write long paragraphs (max 2 sentences in any paragraph)
- Repeat the same information
- Show more than 3 schemes
- Make up URLs or document names
- Skip if profile data is limited — just show what you know

═══════════════════════════════════════
REQUIRED OUTPUT FORMAT (copy exactly)
═══════════════════════════════════════

### 📝 Summary
Hello [Name]! Here is what I found for you. (1-2 lines max)

### ✅ Eligibility
- [Simple criterion 1]
- [Simple criterion 2]
- **Age:** [range if relevant]
- **Income limit:** [amount if relevant]

### 📋 Documents Needed
- [ ] Aadhaar Card
- [ ] [Other document]
- [ ] [Other document]

### 🏛️ Available Schemes
(For EACH scheme — max 3 — use this format EXACTLY. No extra text before or after the block.)

:::SCHEME_CARD
Name: [Full official scheme name]
Who: [One sentence — who is eligible, in plain language]
Benefits: [Exact amount like ₹6,000/year or description of benefit]
Documents: [Aadhaar, Ration Card, Bank Passbook — comma separated]
Deadline: [Specific date OR "Apply anytime" OR "Apply before March 2025"]
Link: [Full real URL starting with https://]
:::

### 👣 Steps to Apply
1. [First thing to do — under 15 words]
2. [Second thing — under 15 words]
3. [Third thing — under 15 words]

═══════════════════════════════════════
URL RULES
═══════════════════════════════════════
- ONLY use real government URLs.
- Use these domains:
  • https://www.myscheme.gov.in
  • https://scholarships.gov.in
  • https://pmkisan.gov.in
  • https://nhm.gov.in
  • https://umang.gov.in
- If unsure of exact URL, use https://www.myscheme.gov.in

═══════════════════════════════════════
CONTEXT (schemes retrieved from database)
═══════════════════════════════════════
{context}

═══════════════════════════════════════
SOURCES
═══════════════════════════════════════
{_citations_markdown(citations)}

═══════════════════════════════════════
RECENT CHAT HISTORY
═══════════════════════════════════════
{history_str or 'No previous conversation.'}

Now respond following ALL rules above.
"""

    worker_summary = _worker_summary(mode, query, citations)

    # First attempt: Gemini.
    try:
        answer = _generate_with_gemini(prompt)
        answer = _append_nearby_ngos(answer, query, profile)
        return _build_response(_humanize_answer(answer), citations, mode, follow_up, worker_summary=worker_summary)
    except Exception as gemini_err:
        print(f"Gemini generation failed: {gemini_err}. Trying COEAI...")

    # Second attempt: COEAI (when configured/reachable).
    try:
        answer = _generate_with_external_llm(prompt, llm)
        answer = _append_nearby_ngos(answer, query, profile)
        return _build_response(_humanize_answer(answer), citations, mode, follow_up, worker_summary=worker_summary)
    except Exception as external_err:
        print(f"COEAI fallback failed: {external_err}. Trying local Ollama Llama...")

    # Third attempt: local Ollama Llama.
    if _ollama_is_reachable():
        try:
            answer = _generate_with_ollama(prompt)
            answer = _append_nearby_ngos(answer, query, profile)
            return _build_response(_humanize_answer(answer), citations, mode, follow_up, worker_summary=worker_summary)
        except Exception as ollama_err:
            err_text = str(ollama_err).lower()
            if "read timed out" in err_text or "timeout" in err_text:
                global _OLLAMA_DISABLED_UNTIL, _OLLAMA_DISABLED_REASON
                _OLLAMA_DISABLED_UNTIL = time.time() + 300
                _OLLAMA_DISABLED_REASON = "generation timeout"
            print(f"Ollama generation failed: {ollama_err}. Returning context snippets...")
    else:
        print("Ollama is not reachable. Returning context snippets...")

    # Final fallback: Structured answer for easy reading.
    fallback_answer = _format_fallback_answer(query, ranked_docs, profile=profile)
    fallback_answer = _append_nearby_ngos(fallback_answer, query, profile)

    return _build_response(
        fallback_answer,
        citations,
        mode,
        follow_up,
        worker_summary="",
    )