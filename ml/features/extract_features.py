"""
extract_features.py
-------------------
Feature Engineering Engine for AI-Powered Fraud Network Analysis.

Extracts 12 multi-dimensional behavioral, graph, and temporal features:
1. daily_event_rate
2. rolling_burst_ratio_7d
3. call_to_sms_ratio
4. high_value_txn_fraction
5. persons_per_device_count
6. persons_per_ip_count
7. max_travel_velocity_kmh
8. new_peers_last_30d
9. degree_centrality
10. in_cluster_comm_ratio
11. circadian_night_event_ratio
12. composite_risk_score (heuristic baseline)
"""

import os
import math
import argparse
import pandas as pd
import numpy as np


def haversine_distance(lat1, lon1, lat2, lon2) -> float:
    """Computes great-circle distance in kilometers."""
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2.0)**2
    return 2.0 * r * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def extract_features(data_dir: str = "data/processed/", output_path: str = "data/processed/features_persons.csv") -> pd.DataFrame:
    """Extracts all 12 feature signals for each person from processed datasets."""
    print(f"[*] Extracting ML features from datasets in '{data_dir}'...")

    def load_table(name):
        p = os.path.join(data_dir, f"{name}.csv")
        return pd.read_csv(p) if os.path.exists(p) else pd.DataFrame()

    persons = load_table("persons")
    events = load_table("events")
    locations = load_table("locations")
    relationships = load_table("relationships")

    if persons.empty:
        print("[ERROR] persons.csv not found or empty.")
        return pd.DataFrame()

    features = []

    # Pre-process events
    events["dt"] = pd.to_datetime(events["timestamp"], errors="coerce")
    events["date"] = events["dt"].dt.date
    events["hour"] = events["dt"].dt.hour

    # Location lookup map
    loc_coords = {}
    if not locations.empty:
        for _, row in locations.iterrows():
            loc_coords[str(row["location_id"])] = (float(row["latitude"]), float(row["longitude"]))

    # Calculate Device & IP sharing indices across population
    dev_sharing = {}
    if "device_id" in events.columns:
        dev_sharing = events[events["device_id"].notna() & (events["device_id"] != "")].groupby("device_id")["source_person_id"].nunique().to_dict()

    ip_sharing = {}
    if "ip_id" in events.columns:
        ip_sharing = events[events["ip_id"].notna() & (events["ip_id"] != "")].groupby("ip_id")["source_person_id"].nunique().to_dict()

    for _, p_row in persons.iterrows():
        p_id = str(p_row["person_id"])
        p_evts = events[events["source_person_id"] == p_id].sort_values("dt")
        total_evts = len(p_evts)

        if total_evts == 0:
            features.append({
                "person_id": p_id,
                "daily_event_rate": 0.0,
                "rolling_burst_ratio_7d": 0.0,
                "call_to_sms_ratio": 0.0,
                "high_value_txn_fraction": 0.0,
                "persons_per_device_count": 1.0,
                "persons_per_ip_count": 1.0,
                "max_travel_velocity_kmh": 0.0,
                "new_peers_last_30d": 0,
                "degree_centrality": 0.0,
                "in_cluster_comm_ratio": 0.0,
                "circadian_night_event_ratio": 0.0,
                "composite_risk_score": 0.0
            })
            continue

        # 1. Daily Event Rate
        min_date = p_evts["dt"].min()
        max_date = p_evts["dt"].max()
        days_span = max((max_date - min_date).total_seconds() / 86400.0, 1.0)
        daily_rate = round(total_evts / days_span, 3)

        # 2. Rolling Burst Ratio (7-day window)
        daily_counts = p_evts.groupby("date").size()
        rolling_7d_max = daily_counts.rolling(window=7, min_periods=1).sum().max()
        mean_weekly = (daily_counts.mean() * 7.0) + 1e-3
        burst_ratio = round(float(rolling_7d_max / mean_weekly), 3)

        # 3. Call to SMS Ratio
        call_count = len(p_evts[p_evts["event_type"] == "call"])
        sms_count = len(p_evts[p_evts["event_type"] == "sms"])
        call_to_sms = round(call_count / (sms_count + 1.0), 3)

        # 4. High Value Transaction Fraction (> $50,000)
        txns = p_evts[p_evts["event_type"] == "transaction"]
        if len(txns) > 0:
            high_txns = len(txns[pd.to_numeric(txns["amount"], errors="coerce") >= 50000])
            high_val_frac = round(high_txns / len(txns), 3)
        else:
            high_val_frac = 0.0

        # 5. Max Persons per Shared Device
        p_devs = [d for d in p_evts["device_id"].dropna().unique() if d != ""]
        max_dev_sharing = max([dev_sharing.get(d, 1) for d in p_devs], default=1)

        # 6. Max Persons per Shared IP
        p_ips = [i for i in p_evts["ip_id"].dropna().unique() if i != ""]
        max_ip_sharing = max([ip_sharing.get(i, 1) for i in p_ips], default=1)

        # 7. Max Travel Velocity (km/h)
        max_velocity = 0.0
        coords_trail = []
        for _, ev in p_evts.iterrows():
            loc_id = str(ev.get("location_id", ""))
            if loc_id in loc_coords:
                coords_trail.append((ev["dt"], loc_coords[loc_id]))

        for i in range(1, len(coords_trail)):
            t1, (lat1, lon1) = coords_trail[i - 1]
            t2, (lat2, lon2) = coords_trail[i]
            hrs = (t2 - t1).total_seconds() / 3600.0
            if hrs > 0.001:
                dist = haversine_distance(lat1, lon1, lat2, lon2)
                vel = dist / hrs
                if vel > max_velocity:
                    max_velocity = vel

        # 8. New Peers Last 30 Days
        target_peers = set(p_evts["target_person_id"].dropna().unique()) - {"", p_id}
        new_peers_30d = len(target_peers)

        # 9. Degree Centrality (from relationships if available)
        deg_centrality = 0.0
        if not relationships.empty:
            p_edges = relationships[(relationships["source_id"] == p_id) | (relationships["target_id"] == p_id)]
            deg_centrality = round(len(p_edges) / max(len(persons) - 1, 1), 4)

        # 10. Community / Clustering proxy
        in_cluster_ratio = min(round(deg_centrality * 2.5, 3), 1.0)

        # 11. Circadian Night Event Ratio (00:00 - 06:00)
        night_evts = len(p_evts[(p_evts["hour"] >= 0) & (p_evts["hour"] < 6)])
        circadian_ratio = round(night_evts / total_evts, 3)

        # 12. Heuristic Baseline Composite Risk Score (0.0 to 1.0)
        risk_signals = [
            min(burst_ratio / 5.0, 1.0) * 0.25,
            min(max_dev_sharing / 5.0, 1.0) * 0.20,
            min(max_ip_sharing / 6.0, 1.0) * 0.20,
            (1.0 if max_velocity > 800.0 else (max_velocity / 800.0)) * 0.15,
            high_val_frac * 0.10,
            circadian_ratio * 0.10
        ]
        composite_risk = round(float(sum(risk_signals)), 3)

        features.append({
            "person_id": p_id,
            "daily_event_rate": daily_rate,
            "rolling_burst_ratio_7d": burst_ratio,
            "call_to_sms_ratio": call_to_sms,
            "high_value_txn_fraction": high_val_frac,
            "persons_per_device_count": max_dev_sharing,
            "persons_per_ip_count": max_ip_sharing,
            "max_travel_velocity_kmh": round(max_velocity, 2),
            "new_peers_last_30d": new_peers_30d,
            "degree_centrality": deg_centrality,
            "in_cluster_comm_ratio": in_cluster_ratio,
            "circadian_night_event_ratio": circadian_ratio,
            "composite_risk_score": composite_risk
        })

    df_feats = pd.DataFrame(features)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_feats.to_csv(output_path, index=False)
    print(f"[+] Extracted 12 features for {len(df_feats)} entities -> {output_path}")
    return df_feats


def main():
    parser = argparse.ArgumentParser(description="Extract ML Behavioral Features")
    parser.add_argument("--data_dir", default="data/processed/", help="Processed data directory")
    parser.add_argument("--out", default="data/processed/features_persons.csv", help="Output CSV path")
    args = parser.parse_args()

    extract_features(args.data_dir, args.out)


if __name__ == "__main__":
    main()
