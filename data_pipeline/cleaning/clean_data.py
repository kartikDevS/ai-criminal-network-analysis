"""
clean_data.py
-------------
Stage 3: Data Cleaning Pipeline for Fraud Network Analysis.

Loads raw CSV datasets from data/raw/, performs:
- Whitespace stripping and string sanitization
- Type casting and null value standardization
- Duplicate detection and removal
- Range and integrity hygiene
- Outputs sanitized datasets to data/cleaned/
"""

import os
import argparse
import pandas as pd
import numpy as np


def clean_dataframe(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Sanitizes strings, standardizes nulls, and removes duplicate rows."""
    initial_len = len(df)
    
    # 1. Strip whitespace from all string columns
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()
            # Standardize 'nan', 'None', '<NA>' to empty strings
            df[col] = df[col].replace(["nan", "None", "<NA>", "NULL", "null"], "")

    # 2. Drop exact duplicate rows if any
    df = df.drop_duplicates().reset_index(drop=True)
    dropped_dups = initial_len - len(df)
    if dropped_dups > 0:
        print(f"  [i] {table_name}: Dropped {dropped_dups} duplicate records.")

    # 3. Table-specific type sanitization
    if table_name == "events":
        if "amount" in df.columns:
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        if "duration_seconds" in df.columns:
            df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")

    elif table_name == "locations":
        if "latitude" in df.columns:
            df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
        if "longitude" in df.columns:
            df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    return df


def run_data_cleaning(raw_dir: str = "data/raw/", cleaned_dir: str = "data/cleaned/"):
    os.makedirs(cleaned_dir, exist_ok=True)
    print(f"[*] Starting Data Cleaning Pipeline (from {raw_dir} -> {cleaned_dir})...")

    files = [
        "persons.csv", "phones.csv", "devices.csv", "ips.csv",
        "accounts.csv", "locations.csv", "organizations.csv",
        "cases.csv", "events.csv"
    ]

    for fname in files:
        raw_path = os.path.join(raw_dir, fname)
        if not os.path.exists(raw_path):
            print(f"  [WARN] Missing file: {raw_path}, skipping.")
            continue

        df = pd.read_csv(raw_path, dtype=str)
        t_name = fname.replace(".csv", "")
        cleaned_df = clean_dataframe(df, t_name)

        out_path = os.path.join(cleaned_dir, fname)
        cleaned_df.to_csv(out_path, index=False)
        print(f"  [+] Cleaned {fname:18s} -> {len(cleaned_df):>6d} rows saved to {out_path}")

    print("\n[SUCCESS] Stage 3: Data Cleaning Complete!")


def main():
    parser = argparse.ArgumentParser(description="Stage 3: Data Cleaning Script")
    parser.add_argument("--raw_dir", default="data/raw/", help="Input raw directory")
    parser.add_argument("--cleaned_dir", default="data/cleaned/", help="Output cleaned directory")
    args = parser.parse_args()

    run_data_cleaning(args.raw_dir, args.cleaned_dir)


if __name__ == "__main__":
    main()
