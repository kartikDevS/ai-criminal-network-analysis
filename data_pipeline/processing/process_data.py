"""
process_data.py
---------------
Stage 6: Graph Relationship Processing & Feature Extraction Engine.

1. Derives dynamic graph relationships from event histories:
   - Person -> Phone (USES_PHONE)
   - Person -> Device (USES_DEVICE)
   - Person -> IP (USES_IP)
   - Person -> Account (OWNS_ACCOUNT)
   - Person -> Location (LOCATED_AT)
   - Person -> Person (COMMUNICATES_WITH)
   - Person -> Person (TRANSACTS_WITH)
   - Person -> Organization (AFFILIATED_WITH)
   - Person -> Case (LINKED_TO)
2. Calculates edge properties: first_seen, last_seen, event_count, weight, volume.
3. Exports Neo4j-ready nodes and edges into neo4j/import/.
4. Generates human-readable inspection samples in outputs/sample/.
"""

import os
import argparse
import pandas as pd
import numpy as np


def process_graph_relationships(data_dir: str, neo4j_dir: str, sample_dir: str):
    os.makedirs(neo4j_dir, exist_ok=True)
    os.makedirs(sample_dir, exist_ok=True)
    print(f"[*] Extracting Graph Relationships from events in '{data_dir}'...")

    def load_csv(name):
        p = os.path.join(data_dir, f"{name}.csv")
        return pd.read_csv(p) if os.path.exists(p) else pd.DataFrame()

    persons = load_csv("persons")
    phones = load_csv("phones")
    devices = load_csv("devices")
    ips = load_csv("ips")
    accounts = load_csv("accounts")
    locations = load_csv("locations")
    organizations = load_csv("organizations")
    cases = load_csv("cases")
    events = load_csv("events")

    if events.empty:
        print("[ERROR] events.csv is empty! Cannot process graph.")
        return

    relationships = []

    # 1. Person -[:USES_PHONE]-> Phone
    phone_evts = events[events["phone_id"].notna() & (events["phone_id"] != "") & events["source_person_id"].notna()]
    if not phone_evts.empty:
        grp = phone_evts.groupby(["source_person_id", "phone_id"]).agg(
            first_seen=("timestamp", "min"),
            last_seen=("timestamp", "max"),
            event_count=("event_id", "count")
        ).reset_index()
        for _, r in grp.iterrows():
            relationships.append({
                "source_id": r["source_person_id"],
                "source_type": "Person",
                "relationship_type": "USES_PHONE",
                "target_id": r["phone_id"],
                "target_type": "Phone",
                "first_seen": r["first_seen"],
                "last_seen": r["last_seen"],
                "event_count": r["event_count"],
                "weight": float(r["event_count"]),
                "metadata": ""
            })

    # 2. Person -[:USES_DEVICE]-> Device
    dev_evts = events[events["device_id"].notna() & (events["device_id"] != "") & events["source_person_id"].notna()]
    if not dev_evts.empty:
        grp = dev_evts.groupby(["source_person_id", "device_id"]).agg(
            first_seen=("timestamp", "min"),
            last_seen=("timestamp", "max"),
            event_count=("event_id", "count")
        ).reset_index()
        for _, r in grp.iterrows():
            relationships.append({
                "source_id": r["source_person_id"],
                "source_type": "Person",
                "relationship_type": "USES_DEVICE",
                "target_id": r["device_id"],
                "target_type": "Device",
                "first_seen": r["first_seen"],
                "last_seen": r["last_seen"],
                "event_count": r["event_count"],
                "weight": float(r["event_count"]),
                "metadata": ""
            })

    # 3. Person -[:USES_IP]-> IP
    ip_evts = events[events["ip_id"].notna() & (events["ip_id"] != "") & events["source_person_id"].notna()]
    if not ip_evts.empty:
        grp = ip_evts.groupby(["source_person_id", "ip_id"]).agg(
            first_seen=("timestamp", "min"),
            last_seen=("timestamp", "max"),
            event_count=("event_id", "count")
        ).reset_index()
        for _, r in grp.iterrows():
            relationships.append({
                "source_id": r["source_person_id"],
                "source_type": "Person",
                "relationship_type": "USES_IP",
                "target_id": r["ip_id"],
                "target_type": "IP",
                "first_seen": r["first_seen"],
                "last_seen": r["last_seen"],
                "event_count": r["event_count"],
                "weight": float(r["event_count"]),
                "metadata": ""
            })

    # 4. Person -[:OWNS_ACCOUNT]-> Account
    if not accounts.empty:
        for _, r in accounts.iterrows():
            relationships.append({
                "source_id": r["owner_person_id"],
                "source_type": "Person",
                "relationship_type": "OWNS_ACCOUNT",
                "target_id": r["account_id"],
                "target_type": "Account",
                "first_seen": r.get("created_date", "2025-01-01"),
                "last_seen": "2025-12-31",
                "event_count": 1,
                "weight": 1.0,
                "metadata": f"type:{r.get('account_type', '')}"
            })

    # 5. Person -[:LOCATED_AT]-> Location
    loc_evts = events[events["location_id"].notna() & (events["location_id"] != "") & events["source_person_id"].notna()]
    if not loc_evts.empty:
        grp = loc_evts.groupby(["source_person_id", "location_id"]).agg(
            first_seen=("timestamp", "min"),
            last_seen=("timestamp", "max"),
            event_count=("event_id", "count")
        ).reset_index()
        for _, r in grp.iterrows():
            relationships.append({
                "source_id": r["source_person_id"],
                "source_type": "Person",
                "relationship_type": "LOCATED_AT",
                "target_id": r["location_id"],
                "target_type": "Location",
                "first_seen": r["first_seen"],
                "last_seen": r["last_seen"],
                "event_count": r["event_count"],
                "weight": float(r["event_count"]),
                "metadata": ""
            })

    # 6. Person -[:COMMUNICATES_WITH]-> Person (Calls & SMS)
    comm_evts = events[events["event_type"].isin(["call", "sms"]) & events["target_person_id"].notna() & (events["target_person_id"] != "")]
    if not comm_evts.empty:
        grp = comm_evts.groupby(["source_person_id", "target_person_id"]).agg(
            first_seen=("timestamp", "min"),
            last_seen=("timestamp", "max"),
            event_count=("event_id", "count")
        ).reset_index()
        for _, r in grp.iterrows():
            relationships.append({
                "source_id": r["source_person_id"],
                "source_type": "Person",
                "relationship_type": "COMMUNICATES_WITH",
                "target_id": r["target_person_id"],
                "target_type": "Person",
                "first_seen": r["first_seen"],
                "last_seen": r["last_seen"],
                "event_count": r["event_count"],
                "weight": float(r["event_count"]),
                "metadata": ""
            })

    # 7. Person -[:TRANSACTS_WITH]-> Person (Transactions)
    txn_evts = events[(events["event_type"] == "transaction") & events["target_person_id"].notna() & (events["target_person_id"] != "")]
    if not txn_evts.empty:
        txn_evts["amount_num"] = pd.to_numeric(txn_evts["amount"], errors="coerce").fillna(0)
        grp = txn_evts.groupby(["source_person_id", "target_person_id"]).agg(
            first_seen=("timestamp", "min"),
            last_seen=("timestamp", "max"),
            event_count=("event_id", "count"),
            total_amount=("amount_num", "sum")
        ).reset_index()
        for _, r in grp.iterrows():
            relationships.append({
                "source_id": r["source_person_id"],
                "source_type": "Person",
                "relationship_type": "TRANSACTS_WITH",
                "target_id": r["target_person_id"],
                "target_type": "Person",
                "first_seen": r["first_seen"],
                "last_seen": r["last_seen"],
                "event_count": r["event_count"],
                "weight": float(round(r["total_amount"], 2)),
                "metadata": f"total_amount:{round(r['total_amount'], 2)}"
            })

    # 8. Person -[:AFFILIATED_WITH]-> Organization & Person -[:LINKED_TO]-> Case
    if not organizations.empty and not persons.empty:
        for i, p in enumerate(persons["person_id"]):
            org = organizations.iloc[i % len(organizations)]["org_id"]
            relationships.append({
                "source_id": p,
                "source_type": "Person",
                "relationship_type": "AFFILIATED_WITH",
                "target_id": org,
                "target_type": "Organization",
                "first_seen": "2025-01-01",
                "last_seen": "2025-12-31",
                "event_count": 1,
                "weight": 1.0,
                "metadata": ""
            })

    if not cases.empty and not persons.empty:
        # Link 20% of persons to investigation cases
        for i in range(min(len(cases), len(persons))):
            relationships.append({
                "source_id": persons.iloc[i]["person_id"],
                "source_type": "Person",
                "relationship_type": "LINKED_TO",
                "target_id": cases.iloc[i]["case_id"],
                "target_type": "Case",
                "first_seen": cases.iloc[i].get("opened_date", "2025-01-01"),
                "last_seen": "2025-12-31",
                "event_count": 1,
                "weight": 1.0,
                "metadata": f"status:{cases.iloc[i].get('status', '')}"
            })

    df_rel = pd.DataFrame(relationships)
    rel_path = os.path.join(data_dir, "relationships.csv")
    df_rel.to_csv(rel_path, index=False)
    print(f"[+] Consolidated {len(df_rel)} Graph Relationships -> {rel_path}")

    # Export to Neo4j Directory
    df_rel.to_csv(os.path.join(neo4j_dir, "relationships.csv"), index=False)
    for name, df in [
        ("nodes_persons.csv", persons),
        ("nodes_phones.csv", phones),
        ("nodes_devices.csv", devices),
        ("nodes_ips.csv", ips),
        ("nodes_accounts.csv", accounts),
        ("nodes_locations.csv", locations),
        ("nodes_organizations.csv", organizations),
        ("nodes_cases.csv", cases)
    ]:
        if not df.empty:
            df.to_csv(os.path.join(neo4j_dir, name), index=False)

    print(f"[+] Exported Neo4j Nodes and Edges into {neo4j_dir}")

    # Generate Human-Readable Samples (10-20 rows each) in data/sample/
    sample_files = {
        "persons_sample.csv": persons.head(15),
        "phones_sample.csv": phones.head(15),
        "devices_sample.csv": devices.head(15),
        "ips_sample.csv": ips.head(15),
        "accounts_sample.csv": accounts.head(15),
        "locations_sample.csv": locations.head(15),
        "organizations_sample.csv": organizations.head(15),
        "cases_sample.csv": cases.head(15),
        "events_sample.csv": events.head(20),
        "relationships_sample.csv": df_rel.head(20)
    }

    # Also grab ground truth samples if available
    gt_dir = "data/ground_truth/"
    for gt_name in ["entity_labels", "event_labels"]:
        gt_f = os.path.join(gt_dir, f"{gt_name}.csv")
        if os.path.exists(gt_f):
            sample_files[f"{gt_name}_sample.csv"] = pd.read_csv(gt_f).head(15)

    for s_name, s_df in sample_files.items():
        if not s_df.empty:
            s_out = os.path.join(sample_dir, s_name)
            s_df.to_csv(s_out, index=False)

    print(f"[+] Human-readable inspection samples created in {sample_dir}")
    print("\n[SUCCESS] Stage 6: Graph Processing & Export Complete!")


def main():
    parser = argparse.ArgumentParser(description="Stage 6: Graph Processing & Export")
    parser.add_argument("--data_dir", default="data/processed/", help="Input/output processed directory")
    parser.add_argument("--neo4j_dir", default="graph/neo4j/import/", help="Neo4j import directory")
    parser.add_argument("--sample_dir", default="data/sample/", help="Sample output directory")
    args = parser.parse_args()

    process_graph_relationships(args.data_dir, args.neo4j_dir, args.sample_dir)


if __name__ == "__main__":
    main()
