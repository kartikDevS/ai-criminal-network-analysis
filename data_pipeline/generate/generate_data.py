"""
generate_data.py
----------------
Stage 2: Advanced Synthetic Data Generation Engine for Fraud Network Analysis.

Generates 100% synthetic, non-PII dataset with:
- 100 Persons, 300 Phones, 120 Devices, 120 IPs, 150 Accounts, 120 Locations, 20 Orgs, 20 Cases
- 7,500 Interaction Events with realistic temporal, geographic, and network topologies
- Isolated Ground-Truth Evaluation Layer in data/ground_truth/
"""

import os
import sys
import math
import random
import argparse
import datetime
from pathlib import Path
import pandas as pd
import numpy as np

try:
    import yaml
except ImportError:
    yaml = None


def load_config(config_path: str) -> dict:
    """Loads configuration from YAML or returns defaults."""
    default_config = {
        "project": {"random_seed": 42},
        "entities": {
            "persons": 100,
            "phones": 300,
            "devices": 120,
            "ips": 120,
            "accounts": 150,
            "locations": 120,
            "organizations": 20,
            "cases": 20,
        },
        "events": {
            "total_events": 7500,
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
        },
        "behavior_patterns": {
            "normal_users": 0.70,
            "highly_connected": 0.05,
            "cluster_members": 0.08,
            "sudden_activity_spike": 0.04,
            "rapid_location_change": 0.03,
            "shared_infrastructure_anomaly": 0.03,
            "shared_infrastructure_normal": 0.02,
            "communication_burst": 0.02,
            "ambiguous_legitimate": 0.03,
        },
        "id_prefixes": {
            "person": "PER_",
            "phone": "PH_",
            "device": "DEV_",
            "ip": "IP_",
            "account": "ACC_",
            "location": "LOC_",
            "organization": "ORG_",
            "case": "CASE_",
            "event": "EVT_",
        },
        "id_padding": 6,
        "paths": {
            "raw_data": "data/raw/",
            "ground_truth": "data/ground_truth/",
        },
    }

    candidate_paths = [
        config_path,
        "data_pipeline/generate/config.yaml",
        os.path.join(os.path.dirname(__file__), "config.yaml"),
        "config/config.yaml"
    ]
    resolved_path = None
    for p in candidate_paths:
        if p and os.path.exists(p):
            resolved_path = p
            break

    if resolved_path and yaml is not None:
        try:
            with open(resolved_path, "r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f)
                if loaded:
                    for k, v in loaded.items():
                        if isinstance(v, dict) and k in default_config:
                            default_config[k].update(v)
                        else:
                            default_config[k] = v
        except Exception as e:
            print(f"[WARN] Error reading {resolved_path}: {e}. Using fallback defaults.")

    return default_config


def format_id(prefix: str, index: int, padding: int = 6) -> str:
    return f"{prefix}{str(index).zfill(padding)}"


def haversine_distance(lat1, lon1, lat2, lon2) -> float:
    """Computes great-circle distance in kilometers between two coordinates."""
    r = 6371.0  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def generate_synthetic_dataset(config: dict, raw_dir: str, ground_truth_dir: str):
    seed = config["project"].get("random_seed", 42)
    random.seed(seed)
    np.random.seed(seed)

    padding = config.get("id_padding", 6)
    prefixes = config.get("id_prefixes", {})
    entity_counts = config.get("entities", {})
    events_cfg = config.get("events", {})
    bp = config.get("behavior_patterns", {})

    n_persons = entity_counts.get("persons", 100)
    n_phones = entity_counts.get("phones", 300)
    n_devices = entity_counts.get("devices", 120)
    n_ips = entity_counts.get("ips", 120)
    n_accounts = entity_counts.get("accounts", 150)
    n_locations = entity_counts.get("locations", 120)
    n_organizations = entity_counts.get("organizations", 20)
    n_cases = entity_counts.get("cases", 20)
    n_events = events_cfg.get("total_events", 7500)

    start_date = datetime.datetime.strptime(events_cfg.get("start_date", "2025-01-01"), "%Y-%m-%d")
    end_date = datetime.datetime.strptime(events_cfg.get("end_date", "2025-12-31"), "%Y-%m-%d")
    date_range_days = max(1, (end_date - start_date).days)

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(ground_truth_dir, exist_ok=True)
    print(f"[*] Initializing Synthetic Data Engine (Seed={seed})...")
    print(f"[*] Target: {n_persons} Persons, {n_events} Events, {n_phones} Phones, {n_devices} Devices, {n_ips} IPs")

    # -------------------------------------------------------------
    # 1. Locations
    # -------------------------------------------------------------
    regions = [
        "North-Metro", "South-Metro", "East-Coast", "West-Harbor",
        "Central-Highlands", "Tech-Park-Alpha", "Financial-District",
        "Industrial-Zone", "Suburban-West", "Border-Transit"
    ]
    locations = []
    for i in range(1, n_locations + 1):
        loc_id = format_id(prefixes.get("location", "LOC_"), i, padding)
        lat = round(random.uniform(12.0, 31.0), 6)
        lon = round(random.uniform(72.0, 88.0), 6)
        region = random.choice(regions)
        locations.append({
            "location_id": loc_id,
            "latitude": lat,
            "longitude": lon,
            "region_name_synthetic": region
        })
    df_locations = pd.DataFrame(locations)
    loc_coords = {l["location_id"]: (l["latitude"], l["longitude"]) for l in locations}

    # -------------------------------------------------------------
    # 2. Persons & Behavioral Assignment (Metadata vs Raw Separation)
    # -------------------------------------------------------------
    age_groups = ["18-25", "26-35", "36-50", "51+"]
    genders = ["M", "F", "Other"]
    occupations = ["Student", "Tech", "Finance", "Healthcare", "Retail", "Services", "Freelance", "Unemployed", "Retired"]

    # Calculate profile quotas
    n_hubs = max(1, int(n_persons * bp.get("highly_connected", 0.05)))
    n_clusters = max(2, int(n_persons * bp.get("cluster_members", 0.08)))
    n_spike = max(1, int(n_persons * bp.get("sudden_activity_spike", 0.04)))
    n_loc_jump = max(1, int(n_persons * bp.get("rapid_location_change", 0.03)))
    n_shared_infra_anom = max(1, int(n_persons * bp.get("shared_infrastructure_anomaly", 0.03)))
    n_shared_infra_norm = max(1, int(n_persons * bp.get("shared_infrastructure_normal", 0.02)))
    n_burst = max(1, int(n_persons * bp.get("communication_burst", 0.02)))
    n_ambiguous = max(1, int(n_persons * bp.get("ambiguous_legitimate", 0.03)))

    pattern_assignments = []
    for _ in range(n_hubs):
        pattern_assignments.append(("hub", "HIGH_ACTIVITY", "high", "High connectivity hub across disparate groups"))
    for _ in range(n_clusters):
        pattern_assignments.append(("cluster_member", "CLUSTERED", "critical", "Coordinated syndicate / money mule cluster"))
    for _ in range(n_spike):
        pattern_assignments.append(("spike", "BURST_ACTIVITY", "high", "Sudden 5x-10x surge in daily event velocity"))
    for _ in range(n_loc_jump):
        pattern_assignments.append(("rapid_location", "LOCATION_ANOMALY", "medium", "Teleportation / impossible velocity between regions"))
    for _ in range(n_shared_infra_anom):
        pattern_assignments.append(("shared_infra_anom", "SHARED_INFRASTRUCTURE", "high", "SIM bank / fraud device multiplexing across accounts"))
    for _ in range(n_shared_infra_norm):
        pattern_assignments.append(("shared_infra_norm", "NORMAL", "none", "Legitimate household / shared corporate gateway"))
    for _ in range(n_burst):
        pattern_assignments.append(("comm_burst", "COMMUNICATION_ANOMALY", "medium", "Short rapid-fire ping calls / SMS blasting"))
    for _ in range(n_ambiguous):
        pattern_assignments.append(("ambiguous_norm", "NORMAL", "none", "Legitimate high-frequency merchant / frequent flyer"))

    while len(pattern_assignments) < n_persons:
        pattern_assignments.append(("normal", "NORMAL", "none", "Standard individual activity baseline"))

    random.shuffle(pattern_assignments)

    persons_raw = []
    entity_ground_truth = []

    for i in range(1, n_persons + 1):
        pid = format_id(prefixes.get("person", "PER_"), i, padding)
        b_tag, gt_label, severity, reason = pattern_assignments[i - 1]
        
        # Account creation date in first 40% of year
        created_offset = random.randint(0, int(date_range_days * 0.4))
        created_dt = (start_date + datetime.timedelta(days=created_offset)).strftime("%Y-%m-%d")
        home_loc = random.choice(locations)["location_id"]

        # Raw features (strictly non-leaking)
        persons_raw.append({
            "person_id": pid,
            "age_group": random.choice(age_groups),
            "gender": random.choice(genders),
            "occupation_category": random.choice(occupations),
            "home_location_id": home_loc,
            "account_created_date": created_dt,
        })

        # Ground truth evaluation record
        entity_ground_truth.append({
            "entity_id": pid,
            "is_anomalous": (gt_label != "NORMAL"),
            "anomaly_type": gt_label,
            "severity": severity,
            "start_time": created_dt,
            "end_time": events_cfg.get("end_date", "2025-12-31"),
            "generation_reason": reason,
            "internal_behavior_tag": b_tag
        })

    df_persons = pd.DataFrame(persons_raw)
    df_entity_gt = pd.DataFrame(entity_ground_truth)

    # -------------------------------------------------------------
    # 3. Organizations & Cases
    # -------------------------------------------------------------
    org_types = ["Fintech", "Logistics", "Retail_Chain", "CallCenter", "Cyber_Consultancy", "Hospitality"]
    organizations = []
    for i in range(1, n_organizations + 1):
        oid = format_id(prefixes.get("organization", "ORG_"), i, padding)
        organizations.append({
            "org_id": oid,
            "org_type_synthetic": random.choice(org_types),
            "region_synthetic": random.choice(regions)
        })
    df_organizations = pd.DataFrame(organizations)

    case_types = ["Phishing_Ring", "SIM_Swap_Syndicate", "Money_Mule_Network", "Identity_Theft", "Data_Exfiltration", "Crypto_Laundering"]
    case_statuses = ["open", "closed", "under_review"]
    cases = []
    for i in range(1, n_cases + 1):
        cid = format_id(prefixes.get("case", "CASE_"), i, padding)
        opened_offset = random.randint(0, date_range_days)
        opened_dt = (start_date + datetime.timedelta(days=opened_offset)).strftime("%Y-%m-%d")
        cases.append({
            "case_id": cid,
            "case_type_synthetic": random.choice(case_types),
            "opened_date": opened_dt,
            "status": random.choice(case_statuses)
        })
    df_cases = pd.DataFrame(cases)

    # -------------------------------------------------------------
    # 4. Devices, IPs, Phones, Accounts
    # -------------------------------------------------------------
    device_types = ["phone", "laptop", "tablet", "router"]
    os_list = ["Android 14", "iOS 17", "Windows 11", "macOS Sonoma", "Linux Ubuntu", "Custom OS"]
    devices = []
    for i in range(1, n_devices + 1):
        did = format_id(prefixes.get("device", "DEV_"), i, padding)
        seen_offset = random.randint(0, date_range_days)
        seen_dt = (start_date + datetime.timedelta(days=seen_offset)).strftime("%Y-%m-%d")
        devices.append({
            "device_id": did,
            "device_type": random.choice(device_types),
            "os_synthetic": random.choice(os_list),
            "first_seen_date": seen_dt
        })
    df_devices = pd.DataFrame(devices)

    ip_types = ["residential", "mobile", "vpn", "datacenter"]
    ips = []
    for i in range(1, n_ips + 1):
        ipid = format_id(prefixes.get("ip", "IP_"), i, padding)
        # RFC 5737 non-routable synthetic test ranges
        octet2 = random.choice([0, 51, 113])
        octet3 = (i * 7) % 254 + 1
        octet4 = (i * 13) % 254 + 1
        synthetic_ip_addr = f"198.{octet2}.{octet3}.{octet4}"
        ips.append({
            "ip_id": ipid,
            "ip_synthetic": synthetic_ip_addr,
            "ip_type": random.choice(ip_types),
            "region_synthetic": random.choice(regions)
        })
    df_ips = pd.DataFrame(ips)

    carriers = ["TelecomX", "AeroNet", "VortexCell", "HorizonMobile", "PulseCom"]
    phones = []
    
    # Identify specific person groups for infrastructure sharing
    shared_anom_pids = [p["entity_id"] for p in entity_ground_truth if p["internal_behavior_tag"] == "shared_infra_anom"]
    shared_norm_pids = [p["entity_id"] for p in entity_ground_truth if p["internal_behavior_tag"] == "shared_infra_norm"]

    for i in range(1, n_phones + 1):
        phid = format_id(prefixes.get("phone", "PH_"), i, padding)
        act_offset = random.randint(0, date_range_days)
        act_dt = (start_date + datetime.timedelta(days=act_offset)).strftime("%Y-%m-%d")
        
        is_shared = False
        if i <= len(persons_raw):
            owner = persons_raw[i - 1]["person_id"]
        elif shared_anom_pids and random.random() < 0.35:
            owner = random.choice(shared_anom_pids)
            is_shared = True
        elif shared_norm_pids and random.random() < 0.25:
            owner = random.choice(shared_norm_pids)
            is_shared = True
        else:
            owner = random.choice(persons_raw)["person_id"]

        phones.append({
            "phone_id": phid,
            "owner_person_id": owner,
            "carrier_synthetic": random.choice(carriers),
            "activation_date": act_dt,
            "is_shared": is_shared
        })
    df_phones = pd.DataFrame(phones)

    account_types = ["bank", "wallet", "social", "messaging"]
    accounts = []
    for i in range(1, n_accounts + 1):
        acc_id = format_id(prefixes.get("account", "ACC_"), i, padding)
        acc_created_offset = random.randint(0, date_range_days)
        acc_created_dt = (start_date + datetime.timedelta(days=acc_created_offset)).strftime("%Y-%m-%d")
        owner = persons_raw[(i - 1) % len(persons_raw)]["person_id"]
        accounts.append({
            "account_id": acc_id,
            "owner_person_id": owner,
            "account_type": random.choice(account_types),
            "created_date": acc_created_dt
        })
    df_accounts = pd.DataFrame(accounts)

    # Fast Lookups for realistic assignment
    person_phones = {}
    for p in phones:
        person_phones.setdefault(p["owner_person_id"], []).append(p["phone_id"])

    person_accounts = {}
    for a in accounts:
        person_accounts.setdefault(a["owner_person_id"], []).append(a["account_id"])

    person_meta = {p["entity_id"]: p for p in entity_ground_truth}
    person_home = {p["person_id"]: p["home_location_id"] for p in persons_raw}

    cluster_pids = [p["entity_id"] for p in entity_ground_truth if p["internal_behavior_tag"] == "cluster_member"]
    hub_pids = [p["entity_id"] for p in entity_ground_truth if p["internal_behavior_tag"] == "hub"]
    spike_pids = [p["entity_id"] for p in entity_ground_truth if p["internal_behavior_tag"] == "spike"]
    loc_jump_pids = [p["entity_id"] for p in entity_ground_truth if p["internal_behavior_tag"] == "rapid_location"]
    burst_pids = [p["entity_id"] for p in entity_ground_truth if p["internal_behavior_tag"] == "comm_burst"]

    # -------------------------------------------------------------
    # 5. Temporal Event Generation Engine (7,500 Events)
    # -------------------------------------------------------------
    print(f"[*] Simulating {n_events} temporal events across graph topologies...")
    event_types = ["call", "sms", "transaction", "login", "location_ping"]
    channels = ["web", "mobile_app", "atm", "pos", "ussd", "api"]
    txn_types = ["transfer", "withdrawal", "deposit", "payment", "p2p"]
    directions = ["outbound", "inbound", "internal"]
    statuses = ["completed", "completed", "completed", "failed", "flagged"]

    events = []
    event_ground_truth = []

    # Track temporal state per person for velocity/location calculations
    person_last_event = {}

    for ev_i in range(1, n_events + 1):
        ev_id = format_id(prefixes.get("event", "EVT_"), ev_i, padding)
        
        # Source Person Selection with realistic weighting
        roll = random.random()
        if hub_pids and roll < 0.18:
            src_p = random.choice(hub_pids)
        elif cluster_pids and roll < 0.38:
            src_p = random.choice(cluster_pids)
        elif spike_pids and roll < 0.48:
            src_p = random.choice(spike_pids)
        elif burst_pids and roll < 0.54:
            src_p = random.choice(burst_pids)
        else:
            src_p = random.choice(persons_raw)["person_id"]

        p_tag = person_meta[src_p]["internal_behavior_tag"]
        ev_type = random.choice(event_types)

        # Circadian Rhythm + Burst Timestamps
        if p_tag == "spike":
            # Tight burst window within 3 specific days in July
            burst_base = start_date + datetime.timedelta(days=190)
            sec_offset = random.randint(0, 3600 * 72)
            ev_dt = burst_base + datetime.timedelta(seconds=sec_offset)
        elif p_tag == "comm_burst":
            # Rapid micro-burst within 24 hours
            burst_base = start_date + datetime.timedelta(days=120)
            sec_offset = random.randint(0, 3600 * 24)
            ev_dt = burst_base + datetime.timedelta(seconds=sec_offset)
        else:
            # Circadian curve: higher density in active day hours
            day_offset = random.randint(0, date_range_days)
            # Beta distribution weighted towards 8am - 10pm
            hour_sample = int(np.random.beta(2.5, 2.0) * 24)
            minute_sample = random.randint(0, 59)
            second_sample = random.randint(0, 59)
            ev_dt = start_date + datetime.timedelta(days=day_offset, hours=hour_sample, minutes=minute_sample, seconds=second_sample)

        # Target selection based on network structure
        target_p = ""
        if ev_type in ["call", "sms", "transaction"]:
            if p_tag == "cluster_member" and len(cluster_pids) > 1 and random.random() < 0.80:
                # Syndicate internal routing
                candidates = [cp for cp in cluster_pids if cp != src_p]
                target_p = random.choice(candidates) if candidates else random.choice(persons_raw)["person_id"]
            elif p_tag == "hub":
                # Hub contacting broad breadth of persons
                target_p = random.choice([p["person_id"] for p in persons_raw if p["person_id"] != src_p])
            else:
                # Standard communications (prefer familiar neighbors 60%, others 40%)
                target_p = random.choice([p["person_id"] for p in persons_raw if p["person_id"] != src_p])

        # Resource Bindings
        p_phs = person_phones.get(src_p, [])
        phone_id = random.choice(p_phs) if p_phs else random.choice(phones)["phone_id"]

        if p_tag == "shared_infra_anom":
            # Stolen/Shared device & IP cluster
            device_id = devices[0]["device_id"]
            ip_id = ips[0]["ip_id"]
        elif p_tag == "shared_infra_norm":
            # Normal shared household / office gateway
            device_id = devices[1]["device_id"]
            ip_id = ips[1]["ip_id"]
        else:
            device_id = random.choice(devices)["device_id"]
            ip_id = random.choice(ips)["ip_id"]

        p_accs = person_accounts.get(src_p, [])
        account_id = random.choice(p_accs) if p_accs else random.choice(accounts)["account_id"]

        # Location & Impossible Speed Simulation
        is_impossible_hop = False
        if p_tag == "rapid_location":
            # Alternate rapidly between extreme locations
            loc_id = random.choice(locations)["location_id"]
            is_impossible_hop = True
        else:
            # 85% home location, 15% regional travel
            if random.random() < 0.85:
                loc_id = person_home[src_p]
            else:
                loc_id = random.choice(locations)["location_id"]

        # Attributes: Amount, Duration, Direction, Status, Channel, Txn Type
        amount = None
        duration_seconds = None
        txn_type_val = ""
        channel_val = random.choice(channels)
        status_val = "completed"
        direction_val = random.choice(directions)

        # Anomaly triggers for event-level evaluation
        ev_is_anom = False
        ev_anom_type = "NORMAL"
        ev_severity = "none"
        ev_reason = "Standard event within normal baseline"

        if ev_type == "transaction":
            txn_type_val = random.choice(txn_types)
            if p_tag == "cluster_member" and random.random() < 0.40:
                # High-value structured mule transfer
                amount = round(random.uniform(75000.0, 480000.0), 2)
                ev_is_anom = True
                ev_anom_type = "TRANSACTION_ANOMALY"
                ev_severity = "high"
                ev_reason = "Unusually high-value cross-account mule transfer"
            elif p_tag == "hub" and random.random() < 0.25:
                amount = round(random.uniform(25000.0, 150000.0), 2)
                ev_is_anom = True
                ev_anom_type = "HIGH_ACTIVITY"
                ev_severity = "medium"
                ev_reason = "Elevated transactional volume from network hub"
            else:
                amount = round(random.uniform(15.0, 4500.0), 2)

        elif ev_type == "call":
            if p_tag == "comm_burst":
                duration_seconds = random.randint(3, 18)  # Rapid ping calls
                ev_is_anom = True
                ev_anom_type = "COMMUNICATION_ANOMALY"
                ev_severity = "medium"
                ev_reason = "High-frequency short duration ping call"
            else:
                duration_seconds = random.randint(15, 1200)

        if p_tag == "spike":
            ev_is_anom = True
            ev_anom_type = "BURST_ACTIVITY"
            ev_severity = "high"
            ev_reason = "Event occurred during sudden concentrated activity surge"
        elif is_impossible_hop:
            ev_is_anom = True
            ev_anom_type = "LOCATION_ANOMALY"
            ev_severity = "medium"
            ev_reason = "Event recorded with rapid impossible geographical transit"
        elif p_tag == "shared_infra_anom":
            ev_is_anom = True
            ev_anom_type = "SHARED_INFRASTRUCTURE"
            ev_severity = "high"
            ev_reason = "Event originated from high-fanout shared device/IP cluster"

        events.append({
            "event_id": ev_id,
            "event_type": ev_type,
            "timestamp": ev_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "source_person_id": src_p,
            "target_person_id": target_p,
            "phone_id": phone_id if ev_type in ["call", "sms", "login"] else "",
            "device_id": device_id if ev_type in ["login", "transaction", "location_ping"] else "",
            "ip_id": ip_id if ev_type in ["login", "transaction"] else "",
            "account_id": account_id if ev_type == "transaction" else "",
            "location_id": loc_id,
            "amount": amount if amount is not None else "",
            "duration_seconds": duration_seconds if duration_seconds is not None else "",
            "direction": direction_val if ev_type in ["call", "sms", "transaction"] else "",
            "status": status_val,
            "channel": channel_val,
            "transaction_type": txn_type_val
        })

        event_ground_truth.append({
            "event_id": ev_id,
            "is_anomalous": ev_is_anom,
            "anomaly_type": ev_anom_type,
            "severity": ev_severity,
            "generation_reason": ev_reason
        })

    # Sort deterministically by timestamp
    events.sort(key=lambda x: x["timestamp"])
    df_events = pd.DataFrame(events)
    df_event_gt = pd.DataFrame(event_ground_truth)

    # -------------------------------------------------------------
    # 6. Save Raw & Ground Truth Datasets
    # -------------------------------------------------------------
    raw_datasets = {
        "persons.csv": df_persons,
        "phones.csv": df_phones,
        "devices.csv": df_devices,
        "ips.csv": df_ips,
        "accounts.csv": df_accounts,
        "locations.csv": df_locations,
        "organizations.csv": df_organizations,
        "cases.csv": df_cases,
        "events.csv": df_events,
    }

    print(f"\n[+] Writing Clean Raw Datasets to {raw_dir}:")
    for filename, df in raw_datasets.items():
        out_path = os.path.join(raw_dir, filename)
        df.to_csv(out_path, index=False)
        print(f"    - {filename:22s} : {len(df):>6d} records -> {out_path}")

    # Save Ground Truth
    gt_entity_path = os.path.join(ground_truth_dir, "entity_labels.csv")
    gt_event_path = os.path.join(ground_truth_dir, "event_labels.csv")
    df_entity_gt.to_csv(gt_entity_path, index=False)
    df_event_gt.to_csv(gt_event_path, index=False)
    print(f"\n[+] Writing Ground Truth Evaluation Datasets to {ground_truth_dir}:")
    print(f"    - entity_labels.csv      : {len(df_entity_gt):>6d} labels -> {gt_entity_path}")
    print(f"    - event_labels.csv       : {len(df_event_gt):>6d} labels -> {gt_event_path}")

    print("\n[SUCCESS] Stage 2: Synthetic Data Generation Complete!")


def main():
    parser = argparse.ArgumentParser(description="Advanced Synthetic Data Generator for SIH Fraud Network")
    parser.add_argument("--config", default="config/config.yaml", help="Path to config.yaml")
    parser.add_argument("--raw_out", default="data/raw/", help="Output directory for raw CSV files")
    parser.add_argument("--gt_out", default="data/ground_truth/", help="Output directory for ground truth CSV files")
    parser.add_argument("--persons", type=int, help="Override number of persons")
    parser.add_argument("--events", type=int, help="Override total events")
    parser.add_argument("--seed", type=int, help="Override random seed")

    args = parser.parse_args()

    cfg = load_config(args.config)
    if args.persons:
        cfg["entities"]["persons"] = args.persons
    if args.events:
        cfg["events"]["total_events"] = args.events
    if args.seed:
        cfg["project"]["random_seed"] = args.seed

    raw_dir = args.raw_out or cfg.get("paths", {}).get("raw_data", "data/raw/")
    gt_dir = args.gt_out or cfg.get("paths", {}).get("ground_truth", "data/ground_truth/")

    generate_synthetic_dataset(cfg, raw_dir, gt_dir)


if __name__ == "__main__":
    main()
