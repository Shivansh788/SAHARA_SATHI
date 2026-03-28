import os
import io
import base64
import tempfile
import shutil
import re
from pathlib import Path
from typing import Any, Dict, Optional
import numpy as np
from subprocess import run, CalledProcessError
import faiss
import logging
import warnings
import traceback
import uvicorn
from fastapi import FastAPI, UploadFile, File, Header
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

from data_loader import load_data
from rag_modules import retrieval, reranker, synthesis, fusion, intake
from sentence_transformers import SentenceTransformer, CrossEncoder
from gtts import gTTS
import whisper
try:
    from openai import OpenAI
except Exception:
    OpenAI = None
from knowledge_graph import build_graph_data, filter_graph
import persistence
import config
import data_gov_client

from frontend_html import html_content

# Suppress HuggingFace warnings so it boots silently
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = config.HF_HUB_DISABLE_SYMLINKS_WARNING
os.environ["TOKENIZERS_PARALLELISM"] = config.TOKENIZERS_PARALLELISM
os.environ["TRANSFORMERS_VERBOSITY"] = config.TRANSFORMERS_VERBOSITY
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

try:
    from coeai import LLMinfer  # Optional: non-free fallback only when configured.
except Exception:
    LLMinfer = None

try:
    import pyttsx3  # Optional offline TTS.
except Exception:
    pyttsx3 = None

# transformers pipeline removed to avoid 2.2GB download
pipeline = None


app = FastAPI()

# Global state to hold our models in memory
RAG_DATA = {
    "chat_history": {},
    "whisper_model": None,
    "ffmpeg_path": None,
    "whisper_model_name": "base",
    "coeai_enabled": False,
    "coeai_models": [],
    "data_gov_enabled": False,
}

SHOW_DEV_OTP_HINT = config.SHOW_DEV_OTP_HINT


def _auth_user(authorization: Optional[str]) -> Optional[Dict[str, Any]]:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ", 1)[1].strip()
    payload = persistence.verify_token(token)
    if not payload:
        return None
    if payload.get("subject_type", "user") != "user":
        return None
    user_id = payload.get("user_id")
    if user_id is None:
        return None
    user = persistence.get_user_by_id(int(user_id))
    if not user:
        return None
    return dict(user)


def _auth_org(authorization: Optional[str]) -> Optional[Dict[str, Any]]:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ", 1)[1].strip()
    payload = persistence.verify_token(token)
    if not payload:
        return None
    if payload.get("subject_type") != "organization":
        return None
    org_id = payload.get("org_id")
    if org_id is None:
        return None
    org = persistence.get_organization_by_id(int(org_id))
    if not org:
        return None
    return dict(org)


def _merge_histories(*histories, limit: int = 12):
    merged = []
    seen = set()
    for history in histories:
        for turn in history or []:
            user_text = (turn.get("user") or "").strip()
            assistant_text = (turn.get("assistant") or "").strip()
            if not user_text and not assistant_text:
                continue
            key = (user_text, assistant_text)
            if key in seen:
                continue
            seen.add(key)
            merged.append({"user": user_text, "assistant": assistant_text})
    return merged[-limit:]


def _build_graph_hint_docs(query: str):
    graph = RAG_DATA.get("knowledge_graph", {"nodes": [], "edges": []})
    sub = filter_graph(graph, query=query, node_limit=20, edge_limit=25)
    docs = []
    for node in sub.get("nodes", [])[:8]:
        docs.append(
            {
                "id": f"graph::{node.get('id', '')}",
                "source_type": "knowledge_graph",
                "source_name": node.get("label", "Graph Node"),
                "category": node.get("type", ""),
                "text": (
                    f"Type: Knowledge Graph | Node: {node.get('label', '')} | "
                    f"Node Type: {node.get('type', '')} | Metadata: {node.get('metadata', {})}"
                ),
            }
        )
    return docs


def _ensure_ffmpeg() -> str:
    """Return an ffmpeg executable path and make sure it's available on PATH."""
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg

    # Fallback: use bundled ffmpeg from imageio-ffmpeg package
    try:
        import imageio_ffmpeg

        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        ffmpeg_dir = os.path.dirname(ffmpeg_exe)
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
        return ffmpeg_exe
    except Exception:
        return ""


def _configure_whisper_ffmpeg(ffmpeg_path: str) -> None:
    if not ffmpeg_path:
        return
    try:
        import numpy as np
        from subprocess import run, CalledProcessError
        import whisper.audio as whisper_audio

        def _load_audio_with_explicit_ffmpeg(file: str, sr: int = whisper_audio.SAMPLE_RATE):
            cmd = [
                ffmpeg_path,
                "-nostdin",
                "-threads", "0",
                "-i", file,
                "-f", "s16le",
                "-ac", "1",
                "-acodec", "pcm_s16le",
                "-ar", str(sr),
                "-",
            ]
            try:
                out = run(cmd, capture_output=True, check=True).stdout
            except CalledProcessError as e:
                raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

            return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

        whisper_audio.load_audio = _load_audio_with_explicit_ffmpeg
    except Exception:
        pass


def _decode_audio_with_ffmpeg(file_path: str, ffmpeg_path: str, sr: int = 16000):
    """Decode any input audio file to mono float32 waveform using explicit ffmpeg binary."""
    cmd = [
        ffmpeg_path,
        "-nostdin",
        "-threads", "0",
        "-i", file_path,
        "-f", "s16le",
        "-ac", "1",
        "-acodec", "pcm_s16le",
        "-ar", str(sr),
        "-",
    ]

    try:
        out = run(cmd, capture_output=True, check=True).stdout
    except CalledProcessError as e:
        raise RuntimeError(f"Failed to decode audio via ffmpeg: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

@app.on_event("startup")
async def startup_event():
    print("Starting up Sahara RAG Pipeline...")
    if config.TOKEN_SECRET == "change-this-secret-in-prod":
        print("Warning: SAHARA_TOKEN_SECRET is using default value. Set a strong secret for production.")

    ffmpeg_path = _ensure_ffmpeg()
    if ffmpeg_path:
        RAG_DATA["ffmpeg_path"] = ffmpeg_path
        _configure_whisper_ffmpeg(ffmpeg_path)
        print(f"ffmpeg ready: {ffmpeg_path}")
    else:
        print("Warning: ffmpeg not found. STT will not work until ffmpeg is installed.")

    persistence.init_db()

    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    docs, bm25 = load_data()

    embedding_texts = retrieval.prepare_embedding_texts(docs)

    index_path = "index.faiss"
    rebuild_index = True
    if os.path.exists(index_path):
        try:
            index = faiss.read_index(index_path)
            if index.ntotal == len(docs):
                rebuild_index = False
        except Exception:
            rebuild_index = True

    if rebuild_index:
        doc_embeddings = embed_model.encode(embedding_texts)
        index = faiss.IndexFlatL2(doc_embeddings.shape[1])
        index.add(doc_embeddings)
        faiss.write_index(index, index_path)

    llm = None
    api_key = config.COEAI_API_KEY
    if api_key and LLMinfer is not None:
        try:
            candidate_llm = LLMinfer(api_key=api_key)
            if synthesis._is_connected_to_upesnet():
                ok, models = synthesis._probe_coeai_models(candidate_llm)
                if ok:
                    llm = candidate_llm
                    RAG_DATA["coeai_enabled"] = True
                    RAG_DATA["coeai_models"] = models
                    print(f"COEAI ready with {len(models)} available model(s).")
                else:
                    print("COEAI not reachable right now. Falling back to local/offline paths.")
            else:
                print("COEAI disabled: not connected to UPESNET.")
        except Exception as e:
            print(f"Optional COEAI client init failed: {e}")

    RAG_DATA["data_gov_enabled"] = data_gov_client.is_configured()
    if RAG_DATA["data_gov_enabled"]:
        print("Data.gov integration enabled.")
    else:
        print("Data.gov integration disabled (missing API configuration).")

    cross_encoder = None
    try:
        cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    except Exception as e:
        print(f"Cross-encoder load failed, using fallback reranker: {e}")
    
    # Local generative model removed to avoid large downloads
    local_pipeline = None


    RAG_DATA["embed_model"] = embed_model
    RAG_DATA["docs"] = docs
    RAG_DATA["bm25"] = bm25
    RAG_DATA["index"] = index
    RAG_DATA["llm"] = llm
    RAG_DATA["cross_encoder"] = cross_encoder
    RAG_DATA["local_pipeline"] = local_pipeline
    
    # Load scheme and NGO data from database
    try:
        RAG_DATA["all_schemes"] = persistence.get_all_schemes()
        print(f"  Loaded {len(RAG_DATA['all_schemes'])} schemes from database")
    except Exception as e:
        print(f"  Warning: Could not load schemes from database: {e}")
        RAG_DATA["all_schemes"] = []
    
    try:
        RAG_DATA["all_ngos"] = persistence.get_all_ngos()
        print(f"  Loaded {len(RAG_DATA['all_ngos'])} NGOs from database")
    except Exception as e:
        print(f"  Warning: Could not load NGOs from database: {e}")
        RAG_DATA["all_ngos"] = []

    # Build in-memory knowledge graph from schemes + NGOs
    RAG_DATA["knowledge_graph"] = build_graph_data(
        RAG_DATA["all_schemes"],
        RAG_DATA["all_ngos"]
    )
    
    print("✅ Application is ready! Open http://localhost:8501 in your browser.")

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    # Serve the exact HTML you asked for
    return html_content


@app.get("/assets/{asset_name}")
async def get_asset(asset_name: str):
    allowed_assets = {
        "preloader.mp4": "Prelaoder.mp4",
        "Prelaoder.mp4": "Prelaoder.mp4",
        "sahara.svg": "sahara.svg",
    }
    mapped_name = allowed_assets.get(asset_name)
    if not mapped_name:
        return {"ok": False, "message": "Asset not found"}

    asset_path = Path(mapped_name)
    if not asset_path.exists() or not asset_path.is_file():
        return {"ok": False, "message": "Asset missing on server"}

    media_type = "application/octet-stream"
    if mapped_name.lower().endswith(".svg"):
        media_type = "image/svg+xml"
    elif mapped_name.lower().endswith(".mp4"):
        media_type = "video/mp4"

    return FileResponse(path=str(asset_path), media_type=media_type)


@app.get("/api/health")
async def health_check():
    return {
        "ok": True,
        "status": "healthy",
        "llm_configured": RAG_DATA.get("llm") is not None,
        "coeai_enabled": RAG_DATA.get("coeai_enabled", False),
        "coeai_model_count": len(RAG_DATA.get("coeai_models", [])),
        "data_gov_enabled": RAG_DATA.get("data_gov_enabled", False),
        "cross_encoder_loaded": RAG_DATA.get("cross_encoder") is not None,
    }


@app.get("/api/data-gov/search")
async def data_gov_search(query: str, limit: int = 5):
    info = data_gov_client.debug_data_gov_search(query, limit=max(1, min(limit, 12)))
    docs = info.get("results", [])
    return {
        "ok": True,
        "provider": info.get("provider", "auto"),
        "count": len(docs),
        "results": docs,
        "diagnostics": info.get("diagnostics", []),
    }

class AskRequest(BaseModel):
    query: str
    profile: Any = "farmer"
    session_id: str = "default_session"
    language: str = "english"
    mode: str = "citizen"


class TTSRequest(BaseModel):
    text: str
    language: str = "english"


class SignupRequest(BaseModel):
    full_name: str
    identifier: str
    password: str
    state: str = ""
    category: str = ""


class LoginRequest(BaseModel):
    identifier: str
    password: str


class BookmarkRequest(BaseModel):
    scheme_name: str
    scheme: Dict[str, Any]


class OrgRegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    category: str
    location: str
    description: str = ""


class OrgVerifyRequest(BaseModel):
    org_id: int
    otp_code: str


class OrgResendOTPRequest(BaseModel):
    org_id: int


class OrgLoginRequest(BaseModel):
    email: str
    password: str


class EventCreateRequest(BaseModel):
    title: str
    description: str
    category: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""


def _messages_to_turns(messages):
    """Convert role-based chat messages into [{user, assistant}] turns for synthesis."""
    turns = []
    pending_user = None
    for msg in messages:
        role = (msg.get("role") or "").lower()
        content = msg.get("content", "")
        if role == "user":
            pending_user = content
        elif role == "assistant":
            if pending_user is not None:
                turns.append({"user": pending_user, "assistant": content})
                pending_user = None
            elif turns:
                turns[-1]["assistant"] = (turns[-1].get("assistant", "") + "\n" + content).strip()
    return turns[-8:]


def _extract_profile_facts(text: str) -> Dict[str, str]:
    """Extract only explicit self-declared facts (name/age/location)."""
    if not text:
        return {}

    normalized = " ".join(text.split())
    profile: Dict[str, str] = {}

    name_match = re.search(
        r"\bmy name is\s+([a-zA-Z][a-zA-Z\s]{1,60}?)(?=\b(?:my age is|i am from|i live in|my location is)\b|[,.!?]|$)",
        normalized,
        re.IGNORECASE,
    )
    if name_match:
        profile["name"] = name_match.group(1).strip().title()

    age_match = re.search(
        r"\b(?:my age is|i am)\s*(\d{1,3})\s*(?:years|yrs|year|yo|years old)?\b",
        normalized,
        re.IGNORECASE,
    )
    if age_match:
        age_value = int(age_match.group(1).strip())
        if 0 < age_value < 120:
            profile["age"] = str(age_value)

    location_match = re.search(
        r"\b(?:i am from|i live in|my location is|from)\s+([a-zA-Z][a-zA-Z\s]{1,60}?)(?=\b(?:my age is|my name is)\b|[,.!?]|$)",
        normalized,
        re.IGNORECASE,
    )
    if location_match:
        location_value = location_match.group(1).strip().title()
        profile["location"] = location_value
        # If state not already provided, use location hint.
        profile.setdefault("state", location_value)

    return profile


def _sanitize_unverified_personal_claims(answer: str, profile: Dict[str, Any]) -> str:
    """Remove personal-age assertions if age was not explicitly captured."""
    text = answer or ""
    known_age = str((profile or {}).get("age", "")).strip()
    if known_age:
        return text

    # Remove common age assertion patterns that can harm trust if hallucinated.
    text = re.sub(r"\byou are\s+\d{1,3}\s*(?:years? old|yrs? old|yo)?\b", "age is not provided", text, flags=re.IGNORECASE)
    text = re.sub(r"\bas a\s+\d{1,3}\s*[- ]?year[- ]old\b", "as age is not provided", text, flags=re.IGNORECASE)
    return text

@app.post("/api/ask")
async def ask_assistant(req: AskRequest, authorization: Optional[str] = Header(None)):
    try:
        if not req.query or not req.query.strip():
            return {"answer": "Please enter a question so I can help you.", "citations": []}

        user = _auth_user(authorization)
        user_id = int(user["id"]) if user and user.get("id") is not None else None

        # Load history from DB and in-memory cache, then merge both for better continuity.
        session_db_messages = persistence.get_chat_messages(req.session_id, limit=30, user_id=user_id)
        session_history = _messages_to_turns(session_db_messages)
        memory_history = RAG_DATA["chat_history"].get(req.session_id, [])

        user_long_history = []
        if user_id is not None:
            recent_user_messages = persistence.get_recent_user_messages(user_id, limit=40)
            user_long_history = _messages_to_turns(recent_user_messages)

        history = _merge_histories(user_long_history, session_history, memory_history, limit=14)

        dense_results = retrieval.dense_search(
            req.query,
            RAG_DATA["index"],
            RAG_DATA["docs"],
            RAG_DATA["embed_model"],
            k=50,
        )
        sparse_results = retrieval.bm25_search(req.query, RAG_DATA["bm25"], RAG_DATA["docs"], k=50)
        fused = fusion.rrf_fusion(sparse_results, dense_results, top_k=50)

        graph_hints = _build_graph_hint_docs(req.query)
        data_gov_hints = []
        if RAG_DATA.get("data_gov_enabled", False):
            try:
                data_gov_hints = data_gov_client.search_data_gov(req.query, limit=6)
            except Exception:
                data_gov_hints = []

        fused_with_graph = fused + graph_hints + data_gov_hints

        ranked_context = reranker.rerank(
            req.query,
            fused_with_graph,
            cross_encoder_model=RAG_DATA.get("cross_encoder"),
            top_k=5,
        )

        # 3. Synthesis with language
        language_map = {
            "hindi": "Hindi",
            "hinglish": "Hinglish",
            "english": "English",
        }

        incoming_profile = req.profile if isinstance(req.profile, dict) else {}

        # Persist only explicit facts from the current user message.
        explicit_facts = _extract_profile_facts(req.query)
        if explicit_facts:
            persistence.upsert_profile_facts(
                explicit_facts,
                session_id=req.session_id,
                user_id=user_id,
                source_text=req.query,
            )

        stored_facts = persistence.get_profile_facts(req.session_id, user_id=user_id)
        intake_profile = intake.intake_agent_graph(req.query, req.session_id, stored_facts)

        profile_with_lang = {
            **intake_profile,
            **incoming_profile,
            **stored_facts,
            **explicit_facts,
            "language": language_map.get(req.language.lower(), "English"),
        }
        if user:
            profile_with_lang.setdefault("name", user.get("full_name", ""))
            profile_with_lang.setdefault("state", user.get("state", ""))
            profile_with_lang.setdefault("category", user.get("category", ""))

        answer_payload = synthesis.generate(
            req.query,
            ranked_context,
            profile_with_lang,
            RAG_DATA["llm"],
            local_pipeline=RAG_DATA.get("local_pipeline"),
            history=history,
            mode=req.mode,
        )
        answer_payload["answer"] = _sanitize_unverified_personal_claims(
            answer_payload.get("answer", ""),
            profile_with_lang,
        )
        
        # Update in-memory history
        history.append({"user": req.query, "assistant": answer_payload.get("answer", "")})
        RAG_DATA["chat_history"][req.session_id] = history

        # Persist history in DB so split prompts remain connected across refresh/restart.
        persistence.save_chat_message(req.session_id, "user", req.query, user_id=user_id)
        persistence.save_chat_message(req.session_id, "assistant", answer_payload.get("answer", ""), user_id=user_id)

        return answer_payload
    except Exception as e:
        print(f"Error in /api/ask: {e}")
        traceback.print_exc()
        return {"answer": "Error generating response. Please try again."}


@app.post("/api/stt")
async def speech_to_text(audio: UploadFile = File(...), language: str = "english"):
    temp_path = None
    try:
        ffmpeg_path = RAG_DATA.get("ffmpeg_path") or _ensure_ffmpeg() or shutil.which("ffmpeg")
        if not ffmpeg_path:
            return {"text": "", "error": "ffmpeg-not-found"}

        if RAG_DATA.get("whisper_model") is None:
            model_name = RAG_DATA.get("whisper_model_name", "base")
            RAG_DATA["whisper_model"] = whisper.load_model(model_name)

        suffix = ".webm"
        if audio.filename and "." in audio.filename:
            suffix = "." + audio.filename.split(".")[-1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
            temp_audio.write(await audio.read())
            temp_path = temp_audio.name

        whisper_lang = {"english": "en", "hindi": "hi", "hinglish": "hi"}.get(language.lower())

        # Decode with explicit ffmpeg binary so Whisper does not rely on PATH lookup for "ffmpeg".
        waveform = _decode_audio_with_ffmpeg(temp_path, ffmpeg_path)

        result = RAG_DATA["whisper_model"].transcribe(
            waveform,
            language=whisper_lang,
            task="transcribe",
            fp16=False,
            temperature=0,
        )
        text = (result.get("text") or "").strip()

        return {"text": text, "error": ""}
    except Exception as e:
        print(f"Error in /api/stt: {e}")
        return {"text": "", "error": str(e)}
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/api/tts")
async def text_to_speech(req: TTSRequest):
    try:
        lang_code = {
            "english": "en",
            "hindi": "hi",
            "hinglish": "en"
        }.get(req.language.lower(), "en")

        # First try OpenAI TTS (when configured), then fall back to local options.
        openai_api_key = getattr(config, "OPENAI_API_KEY", "")
        if openai_api_key and OpenAI is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                temp_audio_path = temp_audio_file.name
            try:
                client = OpenAI(api_key=openai_api_key)
                response = client.audio.speech.create(
                    model=config.OPENAI_TTS_MODEL,
                    voice=config.OPENAI_TTS_VOICE,
                    input=req.text,
                )

                if hasattr(response, "stream_to_file"):
                    response.stream_to_file(temp_audio_path)
                else:
                    content = getattr(response, "content", None)
                    if not isinstance(content, (bytes, bytearray)) and hasattr(response, "read"):
                        content = response.read()
                    if not isinstance(content, (bytes, bytearray)):
                        raise RuntimeError("OpenAI TTS response did not contain binary audio content")
                    with open(temp_audio_path, "wb") as f:
                        f.write(content)

                with open(temp_audio_path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                return {"audio_base64": encoded, "audio_mime": "audio/mpeg"}
            except Exception as openai_tts_error:
                print(f"OpenAI TTS failed, falling back to offline TTS: {openai_tts_error}")
            finally:
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)

        # Prefer offline TTS if available.
        if pyttsx3 is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
                temp_audio_path = temp_audio_file.name
            try:
                engine = pyttsx3.init()
                engine.save_to_file(req.text, temp_audio_path)
                engine.runAndWait()
                with open(temp_audio_path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                return {"audio_base64": encoded, "audio_mime": "audio/wav"}
            finally:
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)

        audio_buffer = io.BytesIO()
        gTTS(text=req.text, lang=lang_code, slow=False).write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        encoded = base64.b64encode(audio_buffer.read()).decode("utf-8")
        return {"audio_base64": encoded, "audio_mime": "audio/mpeg"}
    except Exception as e:
        print(f"Error in /api/tts: {e}")
        return {"audio_base64": "", "audio_mime": ""}

@app.get("/api/schemes")
async def get_schemes(page: int = 1, limit: int = 50):
    try:
        all_schemes = RAG_DATA.get("all_schemes", [])
        start = (page - 1) * limit
        end = start + limit
        paginated = all_schemes[start:end]
        
        # Add links (Mapping some common ones, rest use fallback search)
        links = {
            "PM-Kisan Samman Nidhi": "https://pmkisan.gov.in/",
            "Indira Mahila Shakti Udyam Protsahan Yojana": "https://imshakti.rajasthan.gov.in/",
            "Mukhyamantri Shramik Aujaar Sahayata Yojana": "https://labour.rajasthan.gov.in/",
            "PM Awas Yojana": "https://pmay-urban.gov.in/",
            # Fallback will be constructed in frontend or here
        }
        
        enriched = []
        for s in paginated:
            name = s.get('scheme_name', '')
            s['apply_url'] = links.get(name, f"https://www.myscheme.gov.in/search?q={name.replace(' ', '+')}")
            enriched.append(s)
            
        return {
            "schemes": enriched,
            "total": len(all_schemes),
            "page": page,
            "limit": limit
        }
    except Exception as e:
        print(f"Error in /api/schemes: {e}")
        return {"schemes": [], "total": 0}

@app.get("/api/ngos")
async def get_ngos(category: str = "", location: str = ""):
    try:
        all_ngos = RAG_DATA.get("all_ngos", [])
        filtered = all_ngos
        if category:
            filtered = [n for n in filtered if category.lower() in n.get("category", "").lower()]
        if location:
            filtered = [n for n in filtered if location.lower() in n.get("location", "").lower()]

        events = persistence.list_events(category=category, location=location)
        event_as_ngos = [
            {
                "name": e["title"],
                "category": e.get("category", "Community"),
                "description": f"{e.get('description', '')} (By: {e.get('org_name', '')})",
                "location": e.get("location", ""),
                "eligibility": "Open community event",
                "event_id": e["id"],
                "type": "verified_event",
            }
            for e in events
        ]

        merged = filtered + event_as_ngos
        return {"ngos": merged, "total": len(merged)}
    except Exception as e:
        print(f"Error in /api/ngos: {e}")
        return {"ngos": [], "total": 0}


@app.post("/api/auth/signup")
async def signup(req: SignupRequest):
    try:
        existing = persistence.get_user_by_identifier(req.identifier)
        if existing:
            return {"ok": False, "message": "User already exists"}

        user_id = persistence.create_user(
            full_name=req.full_name,
            identifier=req.identifier,
            password=req.password,
            state=req.state,
            category=req.category,
        )
        token = persistence.create_token(user_id)
        return {"ok": True, "token": token, "user_id": user_id}
    except Exception as e:
        return {"ok": False, "message": str(e)}


@app.post("/api/auth/login")
async def login(req: LoginRequest):
    user = persistence.get_user_by_identifier(req.identifier)
    if not user:
        return {"ok": False, "message": "Invalid credentials"}

    if not persistence.verify_password(req.password, user["password_hash"]):
        return {"ok": False, "message": "Invalid credentials"}

    token = persistence.create_token(int(user["id"]))
    return {
        "ok": True,
        "token": token,
        "user": {
            "id": user["id"],
            "full_name": user["full_name"],
            "identifier": user["identifier"],
            "state": user["state"],
            "category": user["category"],
        },
    }


@app.get("/api/auth/me")
async def me(authorization: Optional[str] = Header(default=None)):
    user = _auth_user(authorization)
    if not user:
        return {"ok": False, "message": "Unauthorized"}
    return {
        "ok": True,
        "user": {
            "id": user["id"],
            "full_name": user["full_name"],
            "identifier": user["identifier"],
            "state": user["state"],
            "category": user["category"],
        },
    }


@app.get("/api/bookmarks")
async def list_user_bookmarks(authorization: Optional[str] = Header(default=None)):
    user = _auth_user(authorization)
    if not user:
        return {"ok": False, "message": "Unauthorized", "bookmarks": []}
    items = persistence.list_bookmarks(int(user["id"]))
    return {"ok": True, "bookmarks": items}


@app.post("/api/bookmarks")
async def add_bookmark(req: BookmarkRequest, authorization: Optional[str] = Header(default=None)):
    user = _auth_user(authorization)
    if not user:
        return {"ok": False, "message": "Unauthorized"}
    persistence.save_bookmark(int(user["id"]), req.scheme_name, req.scheme)
    return {"ok": True}


@app.delete("/api/bookmarks/{bookmark_id}")
async def remove_bookmark(bookmark_id: int, authorization: Optional[str] = Header(default=None)):
    user = _auth_user(authorization)
    if not user:
        return {"ok": False, "message": "Unauthorized"}
    deleted = persistence.delete_bookmark(int(user["id"]), bookmark_id)
    return {"ok": deleted}


@app.post("/api/org/register")
async def org_register(req: OrgRegisterRequest):
    try:
        result = persistence.register_organization(
            name=req.name,
            email=req.email,
            password=req.password,
            category=req.category,
            location=req.location,
            description=req.description,
        )
        response = {
            "ok": True,
            "org_id": result["org_id"],
            "message": "Organization registered. Verify using OTP.",
        }
        if SHOW_DEV_OTP_HINT:
            response["otp_hint"] = result["otp_code"]
        return response
    except Exception as e:
        return {"ok": False, "message": str(e)}


@app.post("/api/org/verify")
async def org_verify(req: OrgVerifyRequest):
    return persistence.verify_organization_with_reason(req.org_id, req.otp_code)


@app.post("/api/org/resend-otp")
async def org_resend_otp(req: OrgResendOTPRequest):
    result = persistence.resend_organization_otp(req.org_id)
    if SHOW_DEV_OTP_HINT:
        return result
    redacted = {k: v for k, v in result.items() if k != "otp_code"}
    return redacted


@app.post("/api/org/login")
async def org_login(req: OrgLoginRequest):
    org_row = persistence.get_organization_by_email(req.email)
    if not org_row:
        return {"ok": False, "message": "Invalid credentials"}
    org = dict(org_row)
    if org.get("status") != "verified":
        return {"ok": False, "message": "Organization must be verified before login"}

    password_hash = org.get("password_hash", "")
    if not password_hash or not persistence.verify_org_password(req.password, password_hash):
        return {"ok": False, "message": "Invalid credentials"}

    token = persistence.create_org_token(int(org["id"]))
    return {
        "ok": True,
        "token": token,
        "org": {
            "id": org["id"],
            "name": org["name"],
            "email": org["email"],
            "category": org["category"],
            "location": org["location"],
            "status": org["status"],
        },
    }


@app.get("/api/org/me")
async def org_me(authorization: Optional[str] = Header(default=None)):
    org = _auth_org(authorization)
    if not org:
        return {"ok": False, "message": "Unauthorized"}
    return {
        "ok": True,
        "org": {
            "id": org["id"],
            "name": org["name"],
            "email": org["email"],
            "category": org["category"],
            "location": org["location"],
            "status": org["status"],
        },
    }


@app.post("/api/events")
async def create_event(req: EventCreateRequest, authorization: Optional[str] = Header(default=None)):
    org = _auth_org(authorization)
    if not org:
        return {"ok": False, "message": "Organization admin login required."}

    event_id = persistence.create_event(
        org_id=int(org["id"]),
        title=req.title,
        description=req.description,
        category=req.category,
        location=req.location,
        start_date=req.start_date,
        end_date=req.end_date,
    )
    if not event_id:
        return {"ok": False, "message": "Organization is not verified or invalid."}
    return {"ok": True, "event_id": event_id}


@app.get("/api/events")
async def list_events(category: str = "", location: str = ""):
    events = persistence.list_events(category=category, location=location)
    return {"ok": True, "events": events}


@app.post("/api/events/{event_id}/report")
async def report_event(event_id: int):
    return persistence.report_event(event_id)


@app.get("/api/knowledge-graph")
async def get_knowledge_graph(query: str = "", node_limit: int = 120, edge_limit: int = 220):
    try:
        graph = RAG_DATA.get("knowledge_graph", {"nodes": [], "edges": [], "stats": {}})
        subgraph = filter_graph(graph, query=query, node_limit=node_limit, edge_limit=edge_limit)
        return {
            "nodes": subgraph.get("nodes", []),
            "edges": subgraph.get("edges", []),
            "stats": subgraph.get("stats", {}),
            "query": subgraph.get("query", ""),
        }
    except Exception as e:
        print(f"Error in /api/knowledge-graph: {e}")
        return {"nodes": [], "edges": [], "stats": {}, "query": query}

if __name__ == "__main__":
    # We use 8501 so the port remains exactly the same as Streamlit for convenience
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)