# SAHARA v2.0 - Quick Reference Guide

**Status:** ✅ Production Ready | **Date:** March 28, 2026

---

## What Changed?

### 1. COEAI Integration (rag_modules/synthesis.py)
```
✅ 2-minute timeout (120 seconds)
✅ UPESNET network detection
✅ Health check before requests
✅ Automatic fallback
```

### 2. Database Pipeline (Already Complete)
```
✅ Gov_schemes.csv → 3,382 records in SQLite
✅ ngo_data.csv → 45 records in SQLite
✅ Zero CSV file dependencies
✅ All data from persistent database
```

---

## How It Works Now

### COEAI Usage (On-Campus Only)

**When you're on UPESNET:**
```bash
# COEAI will be automatically attempted if:
UPESNET_CONNECTED=true  (or connected to upesnet.ac.in)
COEAI_API_KEY=xxx       (environment variable set)
COEAI API reachable     (health check passes)

# Timeout: 2 minutes maximum
# Fallback: Automatic if timeout/unavailable
```

**When you're off-campus:**
```bash
# COEAI is automatically skipped
# System uses: Ollama (local) → Offline fallback
```

### LLM Priority

```
1. Local Ollama (free, fast)      [12 sec timeout]
   └─ Falls back if unavailable

2. COEAI (paid, high-quality)     [120 sec timeout]
   └─ Only on UPESNET network
   └─ Falls back if timeout/unavailable

3. Offline Fallback (free)        [Always works]
   └─ Context snippets + citations
```

---

## Quick Test Commands

### Health Check
```bash
curl http://localhost:8501/api/health
```

### Schemes (Database)
```bash
curl "http://localhost:8501/api/schemes?page=1&limit=5"
```

### NGOs (Database)
```bash
curl "http://localhost:8501/api/ngos?category=Healthcare"
```

### Chat API (RAG)
```bash
curl -X POST http://localhost:8501/api/ask \
  -H "Content-Type: application/json" \
  -d '{"query":"pm kisan","session_id":"test","language":"english","mode":"citizen"}'
```

---

## Key Features

| Feature | Status | Details |
|---------|--------|---------|
| **COEAI Timeout** | ✅ | 2 minutes (120 seconds) |
| **UPESNET Check** | ✅ | DNS + env variable |
| **Health Probe** | ✅ | Prevents hanging |
| **Database** | ✅ | 3,427 records from SQLite |
| **Fallback Mode** | ✅ | Always available offline |
| **Performance** | ✅ | 15-18ms DB, 12-13s RAG |

---

## File Changes Summary

### Modified Files

**rag_modules/synthesis.py** (Enhanced)
- Added `_is_connected_to_upesnet()` - Network detection
- Added `_coeai_is_reachable()` - Health check
- Updated `_generate_with_external_llm()` - Timeout + checks
- Added imports: socket, os, time, Thread

**data_loader.py** (Previous)
- Updated to use database instead of CSV
- Status: ✅ Already done

### New Documentation

**COEAI_UPESNET_INTEGRATION.md**
- Complete technical documentation
- Architecture diagrams
- Test results
- Deployment guide

---

## Environment Variables

### Optional (for COEAI)
```bash
# Force UPESNET connection (testing/tunneling)
export UPESNET_CONNECTED=true

# COEAI API key (required to use COEAI)
export COEAI_API_KEY="your_key_here"

# Custom token secret
export SAHARA_TOKEN_SECRET="your_secret"
```

### Running App
```bash
# On campus (auto-detects UPESNET)
./venv/bin/python app.py

# Off-campus (explicit setting)
export UPESNET_CONNECTED=false
./venv/bin/python app.py

# With COEAI enabled
export COEAI_API_KEY="key"
./venv/bin/python app.py
```

---

## Performance Baseline

```
API Endpoint Responses:
  /api/health:                    <10ms
  /api/schemes (3,382 records):   18ms
  /api/ngos (45 records):         15ms

RAG Pipeline:
  Offline fallback:              ~12-13 seconds
  With Ollama (if running):      ~12-13 seconds
  With COEAI (if on campus):     60-120 seconds

Database Size: 22 MB
Cache Size: 17 MB
FAISS Index: 5.1 MB
```

---

## Troubleshooting

### Check UPESNET Connection
```bash
python3 -c "from rag_modules import synthesis; print(synthesis._is_connected_to_upesnet())"
```

### Check COEAI Availability
```bash
python3 -c "from rag_modules import synthesis; print(synthesis._coeai_is_reachable())"
```

### Force Offline Mode
```bash
export UPESNET_CONNECTED=false
./venv/bin/python app.py
```

### Test Each LLM Tier
```bash
# Tier 1: Ollama
ollama pull llama2
ollama serve  # In separate terminal

# Tier 2: COEAI
export COEAI_API_KEY="your_key"

# Tier 3: Fallback (always works)
# No setup needed - automatic
```

---

## Deployment Checklist

- ✅ Database initialized (sahara.db)
- ✅ All data migrated (3,382 schemes + 45 NGOs)
- ✅ COEAI integration active
- ✅ Timeout configured (120 seconds)
- ✅ UPESNET detection working
- ✅ All API endpoints tested
- ✅ Fallback modes verified
- ✅ Performance benchmarked

---

## What's Next?

### Optional Enhancements
- [ ] COEAI response caching
- [ ] Configurable timeouts
- [ ] Analytics dashboard
- [ ] Rate limiting
- [ ] Load balancing

### Already Completed
- ✅ Database pipeline (100% CSV-free)
- ✅ COEAI timeout protection
- ✅ UPESNET-only LLM
- ✅ Health checks
- ✅ Automatic fallback
- ✅ All tests passing

---

## Support

**Database Issues:**
- Check `sahara.db` exists and has 3,382 schemes
- Run: `./venv/bin/python db_migrate.py` to reload

**COEAI Issues:**
- Verify `UPESNET_CONNECTED` or on campus network
- Check `COEAI_API_KEY` is set (if using)
- Check API health: `curl https://api.coeai.com/health`

**Performance Issues:**
- Monitor RAG pipeline logs
- Check if Ollama is running (faster alternative)
- Verify database indexes are created

---

**System Status:** 🚀 Production Ready  
**Last Updated:** March 28, 2026  
**Version:** 2.0
