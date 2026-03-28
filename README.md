# SAHARA Saathi

AI-powered welfare guidance platform with:
- FastAPI backend
- Hybrid retrieval (BM25 + FAISS + reranker)
- SQLite persistence (auth, bookmarks, chat history, profile facts, NGOs, events)
- Optional COEAI support (UPESNET-gated)

## 1) Fastest Setup For Sharing (Recommended)

From project root:

```bash
chmod +x bootstrap.sh run.sh
./bootstrap.sh
./run.sh
```

Open:

```text
http://localhost:8501
```

What this does automatically:
- Creates `venv`
- Installs all dependencies from `requirements.txt`
- Creates `.env` from `.env.example` if missing
- Runs `db_migrate.py`

Optional one-liner to setup and start immediately:

```bash
chmod +x bootstrap.sh run.sh && ./bootstrap.sh --run
```

## 2) Manual Setup (Linux/macOS)

Run from project root:

```bash
python3 -m venv venv && source venv/bin/activate && pip install -U pip && pip install -r requirements.txt && python db_migrate.py && python app.py
```

Open:

```text
http://localhost:8501
```

## 3) Windows Setup (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python db_migrate.py
python app.py
```

## 4) Runtime Notes

- Default port: 8501
- If port is busy, stop old process and rerun.
- First boot may take longer due to model/index initialization.
- If you do not configure Gemini/COEAI keys, the app still runs using fallback mode.

## 5) Environment and Configuration

All settings are centralized in [config.py](config.py) and can be overridden via `.env`.

Important keys:
- COEAI_API_KEY
- COEAI_MODEL
- UPESNET_CONNECTED_FLAG
- SAHARA_TOKEN_SECRET (via env override)
- DATA_GOV_* (Data.gov integration settings)
- GEMINI_API_KEY
- OPENAI_API_KEY (only for OpenAI TTS)

Quick env setup:

```bash
cp .env.example .env
# edit .env and add only the keys you need
```

Recommended secure override pattern:

```bash
export SAHARA_TOKEN_SECRET="change-me-to-a-strong-secret"
export COEAI_API_KEY="your-key-if-needed"
python app.py
```

## 6) Data and Migration

Migration script loads:
- Government schemes from data/Gov_schemes*.csv
- NGOs from data/ngo_data.csv
- NGO events from data/ngo_events.csv

Run migration anytime:

```bash
python db_migrate.py
```

## 7) Core API Endpoints

- Health: GET /api/health
- Ask assistant: POST /api/ask
- Auth: /api/auth/signup, /api/auth/login, /api/auth/me
- Bookmarks: GET/POST/DELETE /api/bookmarks
- NGOs: GET /api/ngos
- Events: GET/POST /api/events
- Org flow: /api/org/register, /api/org/verify, /api/org/login, /api/org/me

## 8) Memory Safety and Trust

The assistant now stores only explicit user-declared personal facts (for example: "my age is 35") in DB profile memory.
It does not infer personal age/name/location from random numbers or ambiguous text.

## 9) Troubleshooting

Missing module:

```bash
pip install -r requirements.txt
```

Fresh reinstall (safe reset of env only):

```bash
rm -rf venv
./bootstrap.sh
```

Port already in use:

```bash
pkill -f "python.*app.py"
python app.py
```

Verify server:

```bash
curl -s http://127.0.0.1:8501/api/health
```