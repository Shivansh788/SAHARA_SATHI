import pandas as pd
from rank_bm25 import BM25Okapi
import pickle
import os
import persistence


CACHE_VERSION = 3  # Increment to invalidate old CSV-based cache


def _to_safe_str(value):
    if value is None:
        return ""
    return str(value).strip()


def _build_gov_doc(row):
    scheme_name = _to_safe_str(row.get("scheme_name"))
    description = _to_safe_str(row.get("description"))
    category = _to_safe_str(row.get("category"))
    level = _to_safe_str(row.get("level"))
    eligibility = _to_safe_str(row.get("eligibility"))

    text = " | ".join(
        [
            f"Type: Government Scheme",
            f"Name: {scheme_name}",
            f"Category: {category}",
            f"Level: {level}",
            f"Eligibility: {eligibility}",
            f"Description: {description}",
        ]
    )

    return {
        "id": f"gov::{scheme_name}",
        "source_type": "government_scheme",
        "source_name": scheme_name,
        "category": category,
        "level": level,
        "eligibility": eligibility,
        "description": description,
        "text": text,
    }


def _build_ngo_doc(row):
    name = _to_safe_str(row.get("name"))
    description = _to_safe_str(row.get("description"))
    category = _to_safe_str(row.get("category"))
    location = _to_safe_str(row.get("location"))
    eligibility = _to_safe_str(row.get("eligibility"))

    text = " | ".join(
        [
            f"Type: Community Support",
            f"Organization: {name}",
            f"Category: {category}",
            f"Location: {location}",
            f"Eligibility: {eligibility}",
            f"Description: {description}",
        ]
    )

    return {
        "id": f"ngo::{name}",
        "source_type": "community_support",
        "source_name": name,
        "category": category,
        "location": location,
        "eligibility": eligibility,
        "description": description,
        "text": text,
    }


def _build_documents(gov_df, ngo_df):
    documents = []
    for _, row in gov_df.fillna("").iterrows():
        documents.append(_build_gov_doc(row))
    for _, row in ngo_df.fillna("").iterrows():
        documents.append(_build_ngo_doc(row))
    return documents

def load_data():
    # Try to load from cache first (database-based cache)
    if os.path.exists("rag_data.pkl"):
        try:
            with open("rag_data.pkl", "rb") as f:
                payload = pickle.load(f)

            if isinstance(payload, dict) and payload.get("cache_version") == CACHE_VERSION:
                print("  ✓ Loaded RAG cache from disk (3,382 schemes + 45 NGOs)")
                return payload["documents"], payload["bm25"]
        except Exception as e:
            print(f"  ⚠ Cache error: {e}. Recomputing from database...")

    # Load ALL data directly from database (no CSV fallback)
    print("  → Building RAG index from database...")
    
    persistence.init_db()
    
    # Fetch schemes and NGOs from SQLite (guaranteed to exist after init_db)
    all_schemes = persistence.get_all_schemes()
    all_ngos = persistence.get_all_ngos()
    
    print(f"    • Fetched {len(all_schemes)} government schemes from database")
    print(f"    • Fetched {len(all_ngos)} NGOs from database")
    
    # Convert to simple lists of dicts for document building
    gov_list = [dict(scheme) for scheme in all_schemes]
    ngo_list = [dict(ngo) for ngo in all_ngos]
    
    # Create pandas-compatible objects for _build_documents
    gov_df = pd.DataFrame(gov_list)
    ngo_df = pd.DataFrame(ngo_list)
    
    documents = _build_documents(gov_df, ngo_df)
    print(f"    • Built {len(documents)} searchable documents")
    
    # Build BM25 index for sparse search
    tokenized_corpus = [doc["text"].split(" ") for doc in documents]
    bm25 = BM25Okapi(tokenized_corpus)
    print("    • Built BM25 sparse index")

    # Cache for next startup
    with open("rag_data.pkl", "wb") as f:
        pickle.dump(
            {
                "cache_version": CACHE_VERSION,
                "documents": documents,
                "bm25": bm25,
            },
            f,
        )
    
    print("  ✓ Cached RAG data to disk for faster startup")
    return documents, bm25