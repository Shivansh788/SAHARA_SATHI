#!/usr/bin/env python3
"""
Database migration script: Loads government schemes and NGO data from CSV files into SQLite.
Run this once after setting up the database to populate it with seed data.
"""
import pandas as pd
import sys
import os
import glob

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from persistence import init_db, bulk_insert_schemes, bulk_insert_ngos, bulk_insert_ngo_events


def load_schemes_from_csv(csv_path: str) -> list:
    """Load government schemes from CSV file."""
    print(f"Loading schemes from {csv_path}...")
    try:
        df = pd.read_csv(csv_path)
        schemes = df.fillna("").to_dict("records")
        print(f"  ✓ Loaded {len(schemes)} schemes from CSV")
        return schemes
    except Exception as e:
        print(f"  ✗ Error loading schemes: {e}")
        return []


def load_all_schemes_from_data_dir(data_dir: str = "data") -> list:
    """Load and merge all Gov_schemes*.csv files from data directory."""
    scheme_files = sorted(glob.glob(os.path.join(data_dir, "Gov_schemes*.csv")))
    if not scheme_files:
        print("  ✗ No Gov_schemes*.csv files found")
        return []

    print(f"Found {len(scheme_files)} scheme CSV files")
    all_frames = []
    for csv_file in scheme_files:
        try:
            df = pd.read_csv(csv_file)
            print(f"  ✓ {os.path.basename(csv_file)}: {len(df)} rows")
            all_frames.append(df)
        except Exception as e:
            print(f"  ✗ Failed to load {csv_file}: {e}")

    if not all_frames:
        return []

    merged = pd.concat(all_frames, ignore_index=True)

    # Ensure all expected columns exist, even if some source files are partial.
    required_columns = [
        "scheme_name", "slug", "description", "benefits", "eligibility",
        "application", "documents", "level", "category", "tags", "combined"
    ]
    for col in required_columns:
        if col not in merged.columns:
            merged[col] = ""

    # Keep the last occurrence of duplicate scheme_name entries.
    merged = merged.drop_duplicates(subset=["scheme_name"], keep="last")
    merged = merged.fillna("")
    schemes = merged[required_columns].to_dict("records")
    print(f"  ✓ Total merged unique schemes: {len(schemes)}")
    return schemes


def load_ngos_from_csv(csv_path: str) -> list:
    """Load NGO data from CSV file."""
    print(f"Loading NGOs from {csv_path}...")
    try:
        df = pd.read_csv(csv_path)
        ngos = df.fillna("").to_dict("records")
        print(f"  ✓ Loaded {len(ngos)} NGOs from CSV")
        return ngos
    except Exception as e:
        print(f"  ✗ Error loading NGOs: {e}")
        return []


def load_ngo_events_from_csv(csv_path: str) -> list:
    """Load NGO events data from CSV file."""
    print(f"Loading NGO events from {csv_path}...")
    try:
        df = pd.read_csv(csv_path)
        events = df.fillna("").to_dict("records")
        print(f"  ✓ Loaded {len(events)} NGO events from CSV")
        return events
    except Exception as e:
        print(f"  ✗ Error loading NGO events: {e}")
        return []


def main():
    """Run the complete migration."""
    print("\n===== Sahara Database Migration =====\n")
    
    print("Step 1: Initializing database schema...")
    try:
        init_db()
        print("  ✓ Database schema initialized\n")
    except Exception as e:
        print(f"  ✗ Error initializing database: {e}\n")
        return False
    
    print("Step 2: Loading government schemes...")
    schemes = load_all_schemes_from_data_dir("data")
    if schemes:
        inserted = bulk_insert_schemes(schemes)
        print(f"  ✓ Inserted {inserted} schemes into database\n")
    else:
        print("  ✗ No schemes loaded\n")
        return False
    
    print("Step 3: Loading NGO data...")
    ngos = load_ngos_from_csv("data/ngo_data.csv")
    if ngos:
        inserted = bulk_insert_ngos(ngos)
        print(f"  ✓ Inserted {inserted} NGOs into database\n")
    else:
        print("  ✗ No NGOs loaded\n")
        return False

    print("Step 4: Loading NGO events data...")
    ngo_events = load_ngo_events_from_csv("data/ngo_events.csv")
    if ngo_events:
        inserted_events = bulk_insert_ngo_events(ngo_events)
        print(f"  ✓ Inserted {inserted_events} NGO events into database\n")
    else:
        print("  ✗ No NGO events loaded\n")
        return False
    
    print("===== Migration Complete =====\n")
    print(f"✓ Database is ready for use!")
    print(f"  - Schemes: {len(schemes)}")
    print(f"  - NGOs: {len(ngos)}\n")
    print(f"  - NGO Events: {len(ngo_events)}\n")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
