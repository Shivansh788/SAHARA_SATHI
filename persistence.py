import base64
import hashlib
import hmac
import json
import secrets
import sqlite3
import time
from typing import Any, Dict, List, Optional

import config


DB_PATH = config.DB_PATH
TOKEN_SECRET = config.TOKEN_SECRET
OTP_TTL_SECONDS = config.OTP_TTL_SECONDS


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_column(conn: sqlite3.Connection, table_name: str, column_name: str, column_sql: str) -> None:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    existing = {row[1] for row in rows}
    if column_name not in existing:
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_sql}")


def init_db() -> None:
    with _conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                identifier TEXT UNIQUE NOT NULL,
                state TEXT DEFAULT '',
                category TEXT DEFAULT '',
                password_hash TEXT NOT NULL,
                created_at INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                scheme_name TEXT NOT NULL,
                scheme_payload TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                UNIQUE(user_id, scheme_name),
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT DEFAULT '',
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT DEFAULT '',
                status TEXT NOT NULL,
                otp_code TEXT DEFAULT '',
                reports INTEGER DEFAULT 0,
                created_at INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                org_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT DEFAULT '',
                location TEXT DEFAULT '',
                start_date TEXT DEFAULT '',
                end_date TEXT DEFAULT '',
                status TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                FOREIGN KEY(org_id) REFERENCES organizations(id)
            );

            CREATE TABLE IF NOT EXISTS government_schemes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scheme_name TEXT UNIQUE NOT NULL,
                slug TEXT DEFAULT '',
                description TEXT DEFAULT '',
                benefits TEXT DEFAULT '',
                eligibility TEXT DEFAULT '',
                application TEXT DEFAULT '',
                documents TEXT DEFAULT '',
                level TEXT DEFAULT '',
                category TEXT DEFAULT '',
                tags TEXT DEFAULT '',
                combined TEXT DEFAULT '',
                created_at INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ngos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT DEFAULT '',
                category TEXT DEFAULT '',
                description TEXT DEFAULT '',
                location TEXT DEFAULT '',
                eligibility TEXT DEFAULT '',
                created_at INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_id INTEGER,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS profile_facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_id TEXT NOT NULL,
                fact_key TEXT NOT NULL,
                fact_value TEXT NOT NULL,
                source_text TEXT DEFAULT '',
                created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            """
        )
        _ensure_column(conn, "organizations", "otp_expires_at", "INTEGER DEFAULT 0")
        _ensure_column(conn, "organizations", "otp_attempts", "INTEGER DEFAULT 0")
        _ensure_column(conn, "organizations", "password_hash", "TEXT DEFAULT ''")
        _ensure_column(conn, "users", "email", "TEXT DEFAULT ''")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_chat_messages_session_created ON chat_messages(session_id, created_at)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_profile_facts_user_key ON profile_facts(user_id, fact_key)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_profile_facts_session_key ON profile_facts(session_id, fact_key)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")


def _hash_password(password: str, salt: Optional[str] = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${digest}"


def verify_password(password: str, hashed: str) -> bool:
    try:
        salt, _ = hashed.split("$", 1)
    except ValueError:
        return False
    return hmac.compare_digest(_hash_password(password, salt), hashed)


def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def create_token(subject_id: int, ttl_seconds: Optional[int] = None, subject_type: str = "user") -> str:
    ttl_seconds = ttl_seconds if ttl_seconds is not None else config.TOKEN_TTL_SECONDS
    payload = {
        "subject_type": subject_type,
        "exp": int(time.time()) + int(ttl_seconds),
    }
    if subject_type == "organization":
        payload["org_id"] = subject_id
    else:
        payload["user_id"] = subject_id

    payload_raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    payload_part = _b64_encode(payload_raw)
    signature = hmac.new(TOKEN_SECRET.encode("utf-8"), payload_part.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{payload_part}.{signature}"


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload_part, signature = token.split(".", 1)
    except ValueError:
        return None

    expected_sig = hmac.new(
        TOKEN_SECRET.encode("utf-8"),
        payload_part.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(signature, expected_sig):
        return None

    try:
        payload = json.loads(_b64_decode(payload_part).decode("utf-8"))
    except Exception:
        return None

    if int(payload.get("exp", 0)) < int(time.time()):
        return None
    return payload


def create_user(full_name: str, identifier: str, password: str, state: str = "", category: str = "", email: str = "") -> int:
    with _conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO users (full_name, identifier, email, state, category, password_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (full_name, identifier, email or identifier, state, category, _hash_password(password), int(time.time())),
        )
        return int(cur.lastrowid)


def get_user_by_identifier(identifier: str) -> Optional[sqlite3.Row]:
    with _conn() as conn:
        return conn.execute("SELECT * FROM users WHERE identifier = ?", (identifier,)).fetchone()


def get_user_by_email(email: str) -> Optional[sqlite3.Row]:
    """Return the most recently created user with this email."""
    with _conn() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE email = ? ORDER BY created_at DESC LIMIT 1",
            (email,)
        ).fetchone()


def get_user_by_id(user_id: int) -> Optional[sqlite3.Row]:
    with _conn() as conn:
        return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def create_org_token(org_id: int, ttl_seconds: Optional[int] = None) -> str:
    return create_token(org_id, ttl_seconds=ttl_seconds, subject_type="organization")


def save_bookmark(user_id: int, scheme_name: str, scheme_payload: Dict[str, Any]) -> None:
    with _conn() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO bookmarks (user_id, scheme_name, scheme_payload, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, scheme_name, json.dumps(scheme_payload), int(time.time())),
        )


def list_bookmarks(user_id: int) -> List[Dict[str, Any]]:
    with _conn() as conn:
        rows = conn.execute(
            "SELECT id, scheme_name, scheme_payload, created_at FROM bookmarks WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()
    output = []
    for row in rows:
        output.append(
            {
                "id": row["id"],
                "scheme_name": row["scheme_name"],
                "scheme": json.loads(row["scheme_payload"]),
                "created_at": row["created_at"],
            }
        )
    return output


def delete_bookmark(user_id: int, bookmark_id: int) -> bool:
    with _conn() as conn:
        cur = conn.execute("DELETE FROM bookmarks WHERE id = ? AND user_id = ?", (bookmark_id, user_id))
        return cur.rowcount > 0


def register_organization(
    name: str,
    email: str,
    category: str,
    location: str,
    description: str = "",
    password: str = "",
) -> Dict[str, Any]:
    otp_code = f"{secrets.randbelow(900000) + 100000}"
    otp_expires_at = int(time.time()) + OTP_TTL_SECONDS
    password_hash = _hash_password(password) if password else ""
    with _conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO organizations (name, email, password_hash, category, location, description, status, otp_code, otp_expires_at, otp_attempts, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 'pending', ?, ?, 0, ?)
            """,
            (name, email, password_hash, category, location, description, otp_code, otp_expires_at, int(time.time())),
        )
        org_id = int(cur.lastrowid)
    return {"org_id": org_id, "otp_code": otp_code, "expires_in": OTP_TTL_SECONDS}


def get_organization_by_id(org_id: int) -> Optional[sqlite3.Row]:
    with _conn() as conn:
        return conn.execute("SELECT * FROM organizations WHERE id = ?", (org_id,)).fetchone()


def get_organization_by_email(email: str) -> Optional[sqlite3.Row]:
    with _conn() as conn:
        return conn.execute("SELECT * FROM organizations WHERE email = ?", (email,)).fetchone()


def verify_org_password(password: str, hashed: str) -> bool:
    return verify_password(password, hashed)


def verify_organization(org_id: int, otp_code: str) -> bool:
    result = verify_organization_with_reason(org_id, otp_code)
    return bool(result.get("ok"))


def verify_organization_with_reason(org_id: int, otp_code: str) -> Dict[str, Any]:
    max_attempts = 5

    with _conn() as conn:
        row = conn.execute(
            "SELECT otp_code, otp_expires_at, otp_attempts, status FROM organizations WHERE id = ?",
            (org_id,),
        ).fetchone()
        if not row:
            return {"ok": False, "message": "Organization not found"}

        if row["status"] == "suspended":
            return {"ok": False, "message": "Organization is suspended"}

        now = int(time.time())
        expires_at = int(row["otp_expires_at"] or 0)
        if expires_at and now > expires_at:
            return {"ok": False, "message": "OTP expired", "expired": True}

        attempts = int(row["otp_attempts"] or 0)
        if attempts >= max_attempts:
            return {"ok": False, "message": "Maximum OTP attempts reached"}

        if str(row["otp_code"]).strip() != str(otp_code).strip():
            new_attempts = attempts + 1
            conn.execute("UPDATE organizations SET otp_attempts = ? WHERE id = ?", (new_attempts, org_id))
            return {
                "ok": False,
                "message": "Invalid OTP",
                "attempts_left": max(0, max_attempts - new_attempts),
            }

        conn.execute(
            "UPDATE organizations SET status = 'verified', otp_code = '', otp_expires_at = 0, otp_attempts = 0 WHERE id = ?",
            (org_id,),
        )
    return {"ok": True, "message": "Organization verified"}


def resend_organization_otp(org_id: int) -> Dict[str, Any]:
    otp_code = f"{secrets.randbelow(900000) + 100000}"
    otp_expires_at = int(time.time()) + OTP_TTL_SECONDS

    with _conn() as conn:
        org = conn.execute("SELECT id, status FROM organizations WHERE id = ?", (org_id,)).fetchone()
        if not org:
            return {"ok": False, "message": "Organization not found"}
        if org["status"] == "verified":
            return {"ok": False, "message": "Organization already verified"}
        if org["status"] == "suspended":
            return {"ok": False, "message": "Organization is suspended"}

        conn.execute(
            """
            UPDATE organizations
            SET otp_code = ?, otp_expires_at = ?, otp_attempts = 0
            WHERE id = ?
            """,
            (otp_code, otp_expires_at, org_id),
        )

    return {
        "ok": True,
        "otp_code": otp_code,
        "expires_in": OTP_TTL_SECONDS,
        "message": "OTP resent",
    }


def create_event(org_id: int, title: str, description: str, category: str, location: str, start_date: str, end_date: str) -> Optional[int]:
    with _conn() as conn:
        org = conn.execute("SELECT id, status FROM organizations WHERE id = ?", (org_id,)).fetchone()
        if not org or org["status"] != "verified":
            return None
        cur = conn.execute(
            """
            INSERT INTO events (org_id, title, description, category, location, start_date, end_date, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?)
            """,
            (org_id, title, description, category, location, start_date, end_date, int(time.time())),
        )
        return int(cur.lastrowid)


def list_events(category: str = "", location: str = "") -> List[Dict[str, Any]]:
    where = ["e.status = 'active'"]
    params: List[Any] = []

    if category:
        where.append("LOWER(e.category) LIKE ?")
        params.append(f"%{category.lower()}%")
    if location:
        where.append("LOWER(e.location) LIKE ?")
        params.append(f"%{location.lower()}%")

    query = f"""
        SELECT e.id, e.title, e.description, e.category, e.location, e.start_date, e.end_date,
               o.name AS org_name
        FROM events e
        JOIN organizations o ON o.id = e.org_id
        WHERE {' AND '.join(where)}
        ORDER BY e.created_at DESC
    """

    with _conn() as conn:
        rows = conn.execute(query, params).fetchall()

    return [dict(row) for row in rows]


def report_event(event_id: int) -> Dict[str, Any]:
    with _conn() as conn:
        row = conn.execute(
            """
            SELECT e.id, e.org_id, o.reports
            FROM events e
            JOIN organizations o ON o.id = e.org_id
            WHERE e.id = ?
            """,
            (event_id,),
        ).fetchone()
        if not row:
            return {"ok": False, "message": "Event not found"}

        reports = int(row["reports"]) + 1
        conn.execute("UPDATE organizations SET reports = ? WHERE id = ?", (reports, row["org_id"]))

        suspended = False
        if reports >= 3:
            suspended = True
            conn.execute("UPDATE organizations SET status = 'suspended' WHERE id = ?", (row["org_id"],))
            conn.execute("UPDATE events SET status = 'suspended' WHERE org_id = ?", (row["org_id"],))

    return {
        "ok": True,
        "reports": reports,
        "suspended": suspended,
    }


def bulk_insert_schemes(schemes: List[Dict[str, Any]]) -> int:
    """Bulk insert government schemes into the database."""
    if not schemes:
        return 0
    with _conn() as conn:
        # Clear existing schemes
        conn.execute("DELETE FROM government_schemes")
        inserted = 0
        for scheme in schemes:
            try:
                conn.execute(
                    """
                    INSERT INTO government_schemes (
                        scheme_name, slug, description, benefits, eligibility,
                        application, documents, level, category, tags, combined, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        scheme.get("scheme_name", ""),
                        scheme.get("slug", ""),
                        scheme.get("description", ""),
                        scheme.get("benefits", ""),
                        scheme.get("eligibility", ""),
                        scheme.get("application", ""),
                        scheme.get("documents", ""),
                        scheme.get("level", ""),
                        scheme.get("category", ""),
                        scheme.get("tags", ""),
                        scheme.get("combined", ""),
                        int(time.time()),
                    ),
                )
                inserted += 1
            except Exception as e:
                print(f"Warning: Failed to insert scheme {scheme.get('scheme_name')}: {e}")
                continue
    return inserted


def bulk_insert_ngos(ngos: List[Dict[str, Any]]) -> int:
    """Bulk insert NGOs into the database."""
    if not ngos:
        return 0
    with _conn() as conn:
        # Clear existing NGOs
        conn.execute("DELETE FROM ngos")
        inserted = 0
        for ngo in ngos:
            try:
                conn.execute(
                    """
                    INSERT INTO ngos (
                        name, type, category, description, location, eligibility, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        ngo.get("name", ""),
                        ngo.get("type", ""),
                        ngo.get("category", ""),
                        ngo.get("description", ""),
                        ngo.get("location", ""),
                        ngo.get("eligibility", ""),
                        int(time.time()),
                    ),
                )
                inserted += 1
            except Exception as e:
                print(f"Warning: Failed to insert NGO {ngo.get('name')}: {e}")
                continue
    return inserted


def bulk_insert_ngo_events(ngo_events: List[Dict[str, Any]]) -> int:
    """Bulk insert NGO events from CSV-style rows into organizations/events tables."""
    if not ngo_events:
        return 0

    inserted = 0
    now_ts = int(time.time())

    with _conn() as conn:
        for event in ngo_events:
            ngo_name = str(event.get("ngo_name", "")).strip()
            email = str(event.get("email", "")).strip().lower()
            service = str(event.get("service", "")).strip()
            description = str(event.get("description", "")).strip()
            location = str(event.get("location", "")).strip()
            start_date = str(event.get("event_start_date", "")).strip()
            end_date = str(event.get("event_end_date", "")).strip()

            if not ngo_name or not service:
                continue

            # Resolve or create organization first (verified so imported events are first-class data).
            org_row = None
            if email:
                org_row = conn.execute(
                    "SELECT id FROM organizations WHERE email = ?",
                    (email,),
                ).fetchone()

            if org_row:
                org_id = int(org_row["id"])
            else:
                placeholder_email = email or f"{ngo_name.lower().replace(' ', '_')}@imported.local"
                existing_name = conn.execute(
                    "SELECT id, email FROM organizations WHERE name = ?",
                    (ngo_name,),
                ).fetchone()
                if existing_name:
                    org_id = int(existing_name["id"])
                else:
                    cur = conn.execute(
                        """
                        INSERT INTO organizations (name, email, password_hash, category, location, description, status, otp_code, otp_expires_at, otp_attempts, reports, created_at)
                        VALUES (?, ?, '', ?, ?, ?, 'verified', '', 0, 0, 0, ?)
                        """,
                        (
                            ngo_name,
                            placeholder_email,
                            service or "Community",
                            location,
                            description,
                            now_ts,
                        ),
                    )
                    org_id = int(cur.lastrowid)

            title = f"{service} at {location}" if location else service

            # Avoid duplicate inserts on repeated migrations.
            duplicate = conn.execute(
                """
                SELECT id FROM events
                WHERE org_id = ? AND title = ? AND location = ? AND start_date = ? AND end_date = ?
                LIMIT 1
                """,
                (org_id, title, location, start_date, end_date),
            ).fetchone()
            if duplicate:
                continue

            conn.execute(
                """
                INSERT INTO events (org_id, title, description, category, location, start_date, end_date, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?)
                """,
                (
                    org_id,
                    title,
                    description,
                    service,
                    location,
                    start_date,
                    end_date,
                    now_ts,
                ),
            )
            inserted += 1

    return inserted


def get_all_schemes(limit: int = 0) -> List[Dict[str, Any]]:
    """Retrieve all government schemes from the database."""
    with _conn() as conn:
        query = "SELECT * FROM government_schemes ORDER BY scheme_name"
        if limit > 0:
            query += f" LIMIT {limit}"
        rows = conn.execute(query).fetchall()
    return [dict(row) for row in rows]


def get_all_ngos(limit: int = 0) -> List[Dict[str, Any]]:
    """Retrieve all NGOs from the database."""
    with _conn() as conn:
        query = "SELECT * FROM ngos ORDER BY name"
        if limit > 0:
            query += f" LIMIT {limit}"
        rows = conn.execute(query).fetchall()
    return [dict(row) for row in rows]


def save_chat_message(session_id: str, role: str, content: str, user_id: Optional[int] = None) -> int:
    """Persist a single chat message."""
    with _conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO chat_messages (session_id, user_id, role, content, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session_id, user_id, role, content, int(time.time())),
        )
        return int(cur.lastrowid)


def get_chat_messages(session_id: str, limit: int = 30, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Load chat messages for a session in chronological order."""
    with _conn() as conn:
        if user_id is not None:
            rows = conn.execute(
                """
                SELECT id, session_id, user_id, role, content, created_at
                FROM chat_messages
                WHERE session_id = ? AND (user_id = ? OR user_id IS NULL)
                ORDER BY created_at DESC, id DESC
                LIMIT ?
                """,
                (session_id, user_id, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, session_id, user_id, role, content, created_at
                FROM chat_messages
                WHERE session_id = ?
                ORDER BY created_at DESC, id DESC
                LIMIT ?
                """,
                (session_id, limit),
            ).fetchall()

    messages = [dict(row) for row in rows]
    messages.reverse()
    return messages


def get_recent_user_messages(user_id: int, limit: int = 40) -> List[Dict[str, Any]]:
    """Load recent chat messages for a user across all sessions in chronological order."""
    with _conn() as conn:
        rows = conn.execute(
            """
            SELECT id, session_id, user_id, role, content, created_at
            FROM chat_messages
            WHERE user_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
    messages = [dict(row) for row in rows]
    messages.reverse()
    return messages


def upsert_profile_facts(
    facts: Dict[str, str],
    session_id: str,
    user_id: Optional[int] = None,
    source_text: str = "",
) -> int:
    """Persist explicitly provided user profile facts (name/age/location/state)."""
    if not facts:
        return 0

    allowed_keys = {"name", "age", "location", "state"}
    now_ts = int(time.time())
    inserted = 0

    with _conn() as conn:
        for key, value in facts.items():
            fact_key = str(key).strip().lower()
            fact_value = str(value).strip()
            if fact_key not in allowed_keys or not fact_value:
                continue

            if user_id is not None:
                existing = conn.execute(
                    "SELECT id FROM profile_facts WHERE user_id = ? AND fact_key = ? LIMIT 1",
                    (user_id, fact_key),
                ).fetchone()
                if existing:
                    conn.execute(
                        """
                        UPDATE profile_facts
                        SET fact_value = ?, source_text = ?, session_id = ?, updated_at = ?
                        WHERE id = ?
                        """,
                        (fact_value, source_text, session_id, now_ts, int(existing["id"])),
                    )
                    inserted += 1
                    continue

            existing = conn.execute(
                "SELECT id FROM profile_facts WHERE session_id = ? AND fact_key = ? LIMIT 1",
                (session_id, fact_key),
            ).fetchone()
            if existing:
                conn.execute(
                    """
                    UPDATE profile_facts
                    SET fact_value = ?, source_text = ?, updated_at = ?, user_id = COALESCE(user_id, ?)
                    WHERE id = ?
                    """,
                    (fact_value, source_text, now_ts, user_id, int(existing["id"])),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO profile_facts (user_id, session_id, fact_key, fact_value, source_text, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (user_id, session_id, fact_key, fact_value, source_text, now_ts, now_ts),
                )
            inserted += 1

    return inserted


def get_profile_facts(session_id: str, user_id: Optional[int] = None) -> Dict[str, str]:
    """Return merged persisted profile facts, prioritizing user-level facts over session-only facts."""
    rows: List[sqlite3.Row] = []
    with _conn() as conn:
        if user_id is not None:
            rows = conn.execute(
                """
                SELECT fact_key, fact_value, updated_at
                FROM profile_facts
                WHERE user_id = ? OR session_id = ?
                ORDER BY updated_at DESC, id DESC
                """,
                (user_id, session_id),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT fact_key, fact_value, updated_at
                FROM profile_facts
                WHERE session_id = ?
                ORDER BY updated_at DESC, id DESC
                """,
                (session_id,),
            ).fetchall()

    facts: Dict[str, str] = {}
    for row in rows:
        key = str(row["fact_key"] or "").strip().lower()
        val = str(row["fact_value"] or "").strip()
        if not key or not val:
            continue
        if key not in facts:
            facts[key] = val

    return facts


def search_schemes(keyword: str = "", category: str = "", limit: int = 50) -> List[Dict[str, Any]]:
    """Search government schemes by keyword and/or category."""
    where = []
    params = []
    if keyword:
        where.append("(LOWER(scheme_name) LIKE ? OR LOWER(description) LIKE ? OR LOWER(eligibility) LIKE ?)")
        kw = f"%{keyword.lower()}%"
        params.extend([kw, kw, kw])
    if category:
        where.append("LOWER(category) LIKE ?")
        params.append(f"%{category.lower()}%")
    where_clause = " AND ".join(where) if where else "1=1"
    query = f"SELECT * FROM government_schemes WHERE {where_clause} LIMIT {limit}"
    with _conn() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]


def search_ngos(keyword: str = "", location: str = "", category: str = "", limit: int = 50) -> List[Dict[str, Any]]:
    """Search NGOs by keyword, location, and/or category."""
    where = []
    params = []
    if keyword:
        where.append("(LOWER(name) LIKE ? OR LOWER(description) LIKE ?)")
        kw = f"%{keyword.lower()}%"
        params.extend([kw, kw])
    if location:
        where.append("LOWER(location) LIKE ?")
        params.append(f"%{location.lower()}%")
    if category:
        where.append("LOWER(category) LIKE ?")
        params.append(f"%{category.lower()}%")
    where_clause = " AND ".join(where) if where else "1=1"
    query = f"SELECT * FROM ngos WHERE {where_clause} LIMIT {limit}"
    with _conn() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(row) for row in rows]
