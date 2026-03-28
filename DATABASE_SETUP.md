## Sahara Saathi - SQLite Database Integration

**Status**: ✅ Fully Integrated & Operational

### Overview
All government schemes and NGO data is now stored in SQLite database (`sahara.db`) for:
- Persistent storage across restarts
- Efficient querying and filtering
- Scalable data management
- Clean separation of concerns

### Database Schema

#### Tables:
1. **government_schemes** (3,382 records)
   - `scheme_name`, `slug`, `description`, `benefits`, `eligibility`, `application`, `documents`, `level`, `category`, `tags`, `combined`

2. **ngos** (45 records)
   - `name`, `type`, `category`, `description`, `location`, `eligibility`

3. **users** (User accounts for authentication)
4. **bookmarks** (User-saved schemes)
5. **organizations** (Verified NGO partners)
6. **events** (Community events)

### Quick Start

#### 1. Initialize Database (One-time, Already Done)
```bash
./venv/bin/python db_migrate.py
```
This loads `data/Gov_schemes.csv` and `data/ngo_data.csv` into the database.

Output:
```
✓ Database is ready for use!
  - Schemes: 3382
  - NGOs: 45
```

#### 2. Run the Application
```bash
./venv/bin/python app.py
```

The app will:
- Initialize database schema (if needed)
- Load 3,382 schemes from database
- Load 45 NGOs from database
- Start RAG pipeline with database-sourced data
- Run on `http://localhost:8501`

#### 3. Test API Endpoints

**Health Check:**
```bash
curl http://127.0.0.1:8501/api/health
```

**Get Schemes (Paginated):**
```bash
curl "http://127.0.0.1:8501/api/schemes?page=1&limit=10"
```

**Get NGOs (Filtered):**
```bash
curl "http://127.0.0.1:8501/api/ngos?category=Healthcare&location=Agra"
```

**Chat Query:**
```bash
curl -X POST http://127.0.0.1:8501/api/ask \
  -H 'Content-Type: application/json' \
  -d '{"query":"pm kisan eligibility","session_id":"demo1","language":"english","mode":"citizen"}'
```

### Database Functions (persistence.py)

**Load Data:**
- `get_all_schemes()` - Retrieve all schemes
- `get_all_ngos()` - Retrieve all NGOs

**Search Data:**
- `search_schemes(keyword, category, limit)` - Full-text scheme search
- `search_ngos(keyword, location, category, limit)` - NGO search with filters

**Manage Data:**
- `bulk_insert_schemes(schemes)` - Insert/update schemes
- `bulk_insert_ngos(ngos)` - Insert/update NGOs

### Key Improvements Over CSV
✅ **Persistent Storage** - Data survives app restarts  
✅ **Efficient Queries** - Database indexes for fast lookups  
✅ **Scalability** - Handle large datasets efficiently  
✅ **Integrity** - FOREIGN KEY constraints on bookmarks & events  
✅ **No CSV Parsing Overhead** - Direct database access  

### File Changes Made

1. **persistence.py** - Added:
   - `government_schemes` and `ngos` table creation
   - `bulk_insert_schemes()` and `bulk_insert_ngos()` functions
   - `get_all_schemes()` and `get_all_ngos()` functions
   - `search_schemes()` and `search_ngos()` functions

2. **app.py** - Updated:
   - Changed from CSV loading to database loading in `startup_event()`
   - Loads schemes and NGOs from `persistence.get_all_schemes()` and `persistence.get_all_ngos()`
   - `/api/schemes` endpoint still works seamlessly (uses pre-loaded data)

3. **db_migrate.py** - New file:
   - Migration script to populate database from CSV files
   - Can be re-run to refresh data if CSVs are updated

### Verification Checklist

✅ Database schema created with all tables  
✅ 3,382 government schemes loaded from CSV  
✅ 45 NGOs loaded from CSV  
✅ App starts successfully and loads data from database  
✅ /api/health endpoint working  
✅ /api/schemes endpoint returning paginated data  
✅ /api/ngos endpoint returning filtered data  
✅ /api/ask (chat) endpoint working with database-sourced schemes  

### Troubleshooting

**Database file not found?**
```bash
./venv/bin/python db_migrate.py  # Re-run migration
```

**No data loading?**
```bash
# Check database has data:
sqlite3 sahara.db "SELECT COUNT(*) FROM government_schemes; SELECT COUNT(*) FROM ngos;"
```

**Port 8501 already in use?**
```bash
pkill -f "python.*app.py"  # Kill old process
sleep 1
./venv/bin/python app.py   # Start fresh
```

---

**Database Location:** `sahara.db` (in project root)  
**Backup:** Keep `sahara.db` safe for deployment  
**Reset:** Delete `sahara.db` and re-run migration to reload from CSVs
