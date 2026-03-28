import requests
import socket
import os
from threading import Thread
import re

import config


OLLAMA_CONNECT_TIMEOUT_SEC = config.OLLAMA_CONNECT_TIMEOUT_SEC
OLLAMA_READ_TIMEOUT_SEC = config.OLLAMA_READ_TIMEOUT_SEC
COEAI_TIMEOUT_SEC = config.COEAI_TIMEOUT_SEC
COEAI_HEALTH_TIMEOUT_SEC = config.COEAI_HEALTH_TIMEOUT_SEC


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
    person_name = (profile.get("name") or "").strip()
    person_age = (profile.get("age") or "").strip()
    person_location = (profile.get("location") or profile.get("state") or "").strip()

    user_context_parts = []
    if person_name:
        user_context_parts.append(f"Name: {person_name}")
    if person_age:
        user_context_parts.append(f"Age: {person_age}")
    if person_location:
        user_context_parts.append(f"Location: {person_location}")

    lines = [
        "Simple answer:",
        f"You asked about: {query}",
        ("Your provided details: " + ", ".join(user_context_parts)) if user_context_parts else "",
        "Based on available government and community data, these are the best options for you.",
        "",
        "Eligibility:",
        "Check each option below and match your state, category, and situation.",
        "",
        "Who should not apply (if any):",
        "If any mandatory condition is missing (state, age, income, category, or status), avoid that scheme and choose an alternative.",
        "",
        "Documents required:",
        "- Identity proof",
        "- Address proof",
        "- Income certificate (if needed)",
        "- Category certificate (if needed)",
        "- Bank passbook copy",
        "- Passport-size photo",
        "",
        "Best matching options:",
    ]

    for idx, doc in enumerate(ranked_docs[:5], start=1):
        source_name = _compact_text(doc.get("source_name", "Unknown Scheme"), 120)
        category = _compact_text(doc.get("category", "Not available"), 80)
        level = _compact_text(doc.get("level", "Not available"), 40)
        eligibility = _compact_text(doc.get("eligibility", "Not available"), 220)
        description = _compact_text(doc.get("description", doc.get("text", "Not available")), 220)

        lines.extend(
            [
                f"{idx}. {source_name}",
                f"   - Category: {category}",
                f"   - Level: {level}",
                f"   - Who can apply: {eligibility}",
                f"   - What it offers: {description}",
                "   - Documents required (common): ID proof, address proof, category/income proof if applicable, bank details",
                "   - Deadline: Check official portal immediately before applying",
                "",
            ]
        )

    lines.extend(
        [
            "Step-by-step application:",
            "1. Choose the scheme that best matches your state, category, and need.",
            "2. Confirm eligibility line-by-line before filling the form.",
            "3. Keep all required documents ready in clear scanned copies.",
            "4. Fill the official form carefully and submit before deadline.",
            "5. Save acknowledgment/reference number and screenshot.",
            "6. Track status every few days on official portal/helpdesk.",
            "",
            "Deadline and urgency:",
            "Always verify latest last date on official portal before applying.",
            "Apply early to avoid rejection due to server load or document mismatch.",
            "",
            "If not eligible, do this instead:",
            "- Do not stop. Apply to the next 1-2 relevant schemes listed above.",
            "- Ask nearest CSC/NGO worker for assisted application support.",
            "",
            "Extra helpful schemes you may also qualify for:",
            "Review schemes 2 to 5 above as alternatives if your first choice is not eligible.",
            "",
            "Understanding check: Did this explanation make sense? (Yes/No)",
        ]
    )

    return "\n".join(lines)


def _humanize_answer(answer):
    text = (answer or "").strip()
    if not text:
        return "Simple answer:\n- No response generated. Please try again."

    # Keep already well-structured responses unchanged.
    structured_markers = ["\n1.", "\n1)", "\n- ", "Eligibility", "Required documents", "Step-by-step", "What to do next"]
    if any(marker in text for marker in structured_markers):
        return text

    # Convert dense paragraph into readable bullets for elderly users.
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    if not sentences:
        return text

    lines = ["Simple answer:"]
    for sentence in sentences[:8]:
        lines.append(f"- {sentence}")
    lines.append("")
    lines.append("Did this explanation make sense? (Yes/No)")
    return "\n".join(lines)


def _generate_with_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False,
        },
        timeout=(OLLAMA_CONNECT_TIMEOUT_SEC, OLLAMA_READ_TIMEOUT_SEC),
    )
    if response.status_code != 200:
        raise RuntimeError(f"Ollama HTTP {response.status_code}")
    payload = response.json()
    return payload.get("response", "No response content from Ollama.")


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
    context = "\n\n".join([doc.get("text", "") for doc in ranked_docs])

    history_str = ""
    if history:
        for turn in history[-3:]:
            history_str += f"\nUser: {turn['user']}\nAI: {turn['assistant']}\n"

    prompt = f"""
You are Sahara Saathi AI. Use the provided context to answer the user's current query thoughtfully.

Chat History:
{history_str}

User Query:
{query}

Context:
{context}

Profile:
- Name: {profile.get('name', 'Not specified') if isinstance(profile, dict) else 'Not specified'}
- Age: {profile.get('age', 'Not specified') if isinstance(profile, dict) else 'Not specified'}
- Location: {profile.get('location', 'Not specified') if isinstance(profile, dict) else 'Not specified'}
- State: {state or 'Not specified'}
- Category: {category or 'Not specified'}
- Occupation: {occupation or 'Not specified'}

Required Mode:
{mode}

Citations to use:
{_citations_markdown(citations)}

You must follow this mission from the project PPT:
- Maximize useful welfare information from available context.
- Be understandable for uneducated, elderly, and first-time applicants.
- Cover the full journey: discovery -> understanding -> comparison -> preparation -> application -> next actions.

Critical response rules:
1. Use very simple language. Short lines. No dense paragraphs. No jargon.
2. Give direct answer first.
2a. If Name/Age/Location are known above, mention them once in Simple answer.
2b. Never assume or invent Name/Age/Location. If any of these are not specified in Profile, do not claim them.
2c. For age-sensitive recommendations, ask for age first if age is not specified.
3. Mention eligibility clearly as who can apply and who cannot.
4. Provide a practical document checklist.
5. Give step-by-step application flow (where, when, how).
6. Include deadline awareness (if date unavailable, explicitly say user must verify latest deadline on official portal).
7. If user is not eligible, suggest nearest alternatives from context. Never leave user at dead end.
8. Mention at least one extra entitlement/scheme the user did not ask for, if context supports it.
9. Keep all claims grounded in context and add inline citations like [1], [2].

Mode-specific behavior:
- citizen: plain language, compassionate guidance, action-oriented.
- worker: add concise field-ready summary and emphasize citations.
- explorer: include nearby community/NGO support signals from context if present.

Use this exact structure in final answer:
Simple answer:
Eligibility:
Who should not apply (if any):
Documents required:
Step-by-step application:
Deadline and urgency:
If not eligible, do this instead:
Extra helpful schemes you may also qualify for:
Understanding check: Did this explanation make sense? (Yes/No)

Language: {prof_lang}
"""

    worker_summary = _worker_summary(mode, query, citations)

    # Primary free path: local Ollama. Skip quickly if daemon is offline.
    if _ollama_is_reachable():
        try:
            answer = _generate_with_ollama(prompt)
            return _build_response(_humanize_answer(answer), citations, mode, follow_up, worker_summary=worker_summary)
        except Exception as ollama_err:
            print(f"Ollama generation failed: {ollama_err}. Trying optional external LLM...")
    else:
        print("Ollama is not reachable. Skipping local generation and using fallback paths.")

    # Optional non-free path only if explicitly configured.
    try:
        answer = _generate_with_external_llm(prompt, llm)
        return _build_response(_humanize_answer(answer), citations, mode, follow_up, worker_summary=worker_summary)
    except Exception as external_err:
        print(f"External LLM fallback failed: {external_err}. Returning context snippets...")

        # Tertiary fallback: Structured answer for easy reading.
        fallback_answer = _format_fallback_answer(query, ranked_docs, profile=profile)

        return _build_response(
            fallback_answer,
            citations,
            mode,
            follow_up,
            worker_summary="",
        )