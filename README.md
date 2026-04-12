# SAHARA - Quick Share Reference

Status: Ready to share | Updated: March 29, 2026

## Fast Setup 

Run from project root:

```bash
chmod +x bootstrap.sh run.sh
./bootstrap.sh --run
```

Open:

http://localhost:8501

## What Bootstrap Does

- Creates virtual environment in venv
- Installs requirements from requirements.txt
- Creates .env from .env.example if missing
- Runs database migration via db_migrate.py
- Starts app immediately with --run

## LLM Fallback Order

1. Gemini (if GEMINI_API_KEY is set)
2. COEAI (if configured and reachable on UPESNET)
3. Ollama local model (if running)
4. Structured offline fallback

Default timeouts:

- Gemini read timeout: 20 seconds
- COEAI timeout: 120 seconds
- Ollama read timeout: 10 seconds

## Environment Setup

Create local env file:

```bash
cp .env.example .env
```

Only fill keys you actually need:

- GEMINI_API_KEY (optional)
- COEAI_API_KEY (optional)
- OPENAI_API_KEY (optional, only for OpenAI TTS)
- SAHARA_TOKEN_SECRET (recommended)

## Daily Commands

Start app:

```bash
./run.sh
```

Stop app:

- Press Ctrl+C in the running terminal

Health check:

```bash
curl -s http://127.0.0.1:8501/api/health
```

Quick ask test:

```bash
curl -sS -X POST http://127.0.0.1:8501/api/ask \
  -H "Content-Type: application/json" \
  -d '{"query":"pm kisan eligibility","session_id":"smoke1","language":"english","mode":"citizen"}'
```

## Troubleshooting

Port already in use:

```bash
pkill -f "python.*app.py"
./run.sh
```

Missing module error:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

Reset environment:

```bash
rm -rf venv
./bootstrap.sh
```
