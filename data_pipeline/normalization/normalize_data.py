"""
normalize_data.py
-----------------
Stage 4: Data Normalization Pipeline for Fraud Network Analysis.

Loads cleaned datasets from data/cleaned/ and performs:
- Timestamp standardization (ISO-8601 YYYY-MM-DD HH:MM:SS)
- Numerical rounding and coordinate bound normalization
- Boolean column canonicalization (True / False)
- Standardized categorical casing
- Outputs normalized tables to data/processed/
"""

import os
import argparse
import pandas as pd
import numpy as np


def normalize_dataframe(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Applies canonical schema normalization."""
    # 1. Date and Timestamp standardization
    date_cols = [c for c in df.columns if "date" in c]
    for c in date_cols:
        try:
            df[c] = pd.to_datetime(df[c], errors="coerce").dt.strftime("%Y-%m-%d")
        except Exception:
            pass

    if "timestamp" in df.columns:
        try:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            pass

    # 2. Boolean normalization
    if "is_shared" in df.columns:
        df["is_shared"] = df["is_shared"].astype(str).str.lower().isin(["true", "1", "yes", "t"])

    # 3. Numeric bounds and rounding
    if table_name == "events":
        if "amount" in df.columns:
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce").round(2)
        if "duration_seconds" in df.columns:
            # fillna with empty string or int
            df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")

    elif table_name == "locations":
        if "latitude" in df.columns:
            df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce").clip(-90.0, 90.0).round(6)
        if "longitude" in df.columns:
            df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce").clip(-180.0, 180.0).round(6)

    # 4. Standardize text columns
    cat_cols = ["gender", "status", "direction", "channel", "account_type", "device_type", "ip_type", "event_type"]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()

    return df


def run_data_normalization(cleaned_dir: str = "data/cleaned/", processed_dir: str = "data/processed/"):
    os.makedirs(processed_dir, exist_ok=True)
    print(f"[*] Starting Data Normalization Pipeline (from {cleaned_dir} -> {processed_dir})...")

    files = [
        "persons.csv", "phones.csv", "devices.csv", "ips.csv",
        "accounts.csv", "locations.csv", "organizations.csv",
        "cases.csv", "events.csv"
    ]

    for fname in files:
        in_path = os.path.join(cleaned_dir, fname)
        if not os.path.exists(in_path):
            print(f"  [WARN] Missing file: {in_path}, skipping.")
            continue

        df = pd.read_csv(in_path)
        t_name = fname.replace(".csv", "")
        norm_df = normalize_dataframe(df, t_name)

        out_path = os.path.join(processed_dir, fname)
        norm_df.to_csv(out_path, index=False)
        print(f"  [+] Normalized {fname:18s} -> {len(norm_df):>6d} rows saved to {out_path}")

    print("\n[SUCCESS] Stage 4: Data Normalization Complete!")


def main():
    parser = argparse.ArgumentParser(description="Stage 4: Data Normalization Script")
    parser.add_argument("--cleaned_dir", default="data/cleaned/", help="Input cleaned directory")
    parser.add_argument("--processed_dir", default="data/processed/", help="Output processed directory")
    args = parser.parse_args()

    run_data_normalization(args.cleaned_dir, args.processed_dir)


if __name__ == "__main__":
    main()
