# AI/ML Feature Engineering & Data Compatibility Specification

This document details the mathematical derivation, source mapping, and algorithmic formulas for extracting behavioral and graph features from the Stage 1 synthetic dataset.

---

## 1. Feature Engineering Reference Matrix

| # | Feature Category | Feature Name | Source Table(s) & Columns | Calculation Formula / Derivation Method | Example Value |
|---|---|---|---|---|---|
| **1** | **Activity Frequency** | `daily_event_rate` | `events.csv` (`timestamp`, `source_person_id`) | $\frac{\text{Total Events for Person}}{\text{Days between } \min(t) \text{ and } \max(t)}$ | `8.4 events/day` |
| **2** | **Activity Spikes** | `rolling_burst_ratio_7d` | `events.csv` (`timestamp`, `source_person_id`) | $\frac{\max_{w \in 7d}(\text{Count}(w))}{\text{Mean}(\text{Weekly Counts}) + \epsilon}$ | `4.82` (Spike > 3.0) |
| **3** | **Communication Frequency** | `call_to_sms_ratio` | `events.csv` (`event_type`, `duration_seconds`) | $\frac{\text{Count}(\text{event\_type} = \text{'call'})}{\text{Count}(\text{event\_type} = \text{'sms'}) + 1}$ | `1.25` |
| **4** | **Transaction Behavior** | `high_value_txn_fraction` | `events.csv` (`event_type`, `amount`) | $\frac{\text{Count}(\text{amount} > \$50,000)}{\text{Total Transactions for Person}}$ | `0.38` (Mule signature) |
| **5** | **Device Sharing** | `persons_per_device_count` | `events.csv` (`device_id`, `source_person_id`) | $\text{Distinct}(\text{source\_person\_id}) \text{ grouped by } \text{device\_id}$ | `8 persons/device` (SIM bank/device multiplexing) |
| **6** | **IP Sharing** | `persons_per_ip_count` | `events.csv` (`ip_id`, `source_person_id`) | $\text{Distinct}(\text{source\_person\_id}) \text{ grouped by } \text{ip\_id}$ | `12 persons/IP` (VPN/Proxy concentration) |
| **7** | **Location Changes** | `max_travel_velocity_kmh` | `events.csv` + `locations.csv` (`lat`, `lon`, `timestamp`) | $\max_{i} \left( \frac{\text{Haversine}(p_i, p_{i-1})}{\Delta t_i} \right)$ | `1,250 km/h` (Impossible jump / Teleportation) |
| **8** | **Relationship Growth** | `new_peers_last_30d` | `events.csv` (`target_person_id`, `timestamp`) | $\text{Count}(\text{Distinct Peers with First Seen} \in [T-30d, T])$ | `14 new contacts` |
| **9** | **Graph Centrality** | `degree_centrality` | `relationships.csv` (`source_id`, `target_id`) | $\frac{\text{Degree}(v)}{N - 1}$ across `COMMUNICATES_WITH` + `TRANSACTS_WITH` | `0.24` (Hub entity) |
| **10** | **Community Structure** | `in_cluster_comm_ratio` | `relationships.csv` (`COMMUNICATES_WITH`, `target_id`) | $\frac{\text{Interactions with Community Members}}{\text{Total Interactions}}$ | `0.85` (Tightly coupled syndicate) |
| **11** | **Temporal Regularity** | `circadian_night_event_ratio` | `events.csv` (`timestamp`) | $\frac{\text{Count}(\text{Hour} \in [00:00, 06:00])}{\text{Total Events}}$ | `0.42` (Suspicious off-hours operation) |
| **12** | **Multi-Signal Anomaly** | `composite_risk_score` | Aggregated features 1–11 | Weighted ensemble / Isolation Forest outlier score: $-s(x)$ | `0.89` (High composite risk) |

---

## 2. Feature Extraction Algorithms

### 2.1 Velocity & Geographic Teleportation
```python
def compute_velocity(df_events, df_locations):
    # Merge event coordinates
    ev = df_events.merge(df_locations, on='location_id').sort_values(['source_person_id', 'timestamp'])
    ev['prev_lat'] = ev.groupby('source_person_id')['latitude'].shift(1)
    ev['prev_lon'] = ev.groupby('source_person_id')['longitude'].shift(1)
    ev['prev_time'] = pd.to_datetime(ev.groupby('source_person_id')['timestamp'].shift(1))
    ev['curr_time'] = pd.to_datetime(ev['timestamp'])
    
    # Time delta in hours
    time_diff_hours = (ev['curr_time'] - ev['prev_time']).dt.total_seconds() / 3600.0
    
    # Haversine distance in km
    dist_km = haversine_vec(ev['latitude'], ev['longitude'], ev['prev_lat'], ev['prev_lon'])
    ev['velocity_kmh'] = dist_km / (time_diff_hours + 1e-5)
    return ev.groupby('source_person_id')['velocity_kmh'].max()
```

### 2.2 Rolling Activity Burst Ratio
```python
def compute_burst_score(df_events):
    df_events['date'] = pd.to_datetime(df_events['timestamp']).dt.date
    daily_counts = df_events.groupby(['source_person_id', 'date']).size().unstack(fill_value=0)
    rolling_7d = daily_counts.rolling(window=7, axis=1).sum()
    mean_activity = daily_counts.mean(axis=1)
    burst_ratio = rolling_7d.max(axis=1) / (mean_activity * 7 + 1e-3)
    return burst_ratio
```

---

## 3. Strict Feature Isolation Rules
1. **Never leak labels:** Columns `is_anomalous`, `anomaly_type`, `severity`, and `generation_reason` reside exclusively in `data/ground_truth/` and must never be imported into model feature matrix `X`.
2. **Deterministic Evaluation:** Ground-truth files are keyed by `entity_id` (`PER_XXXXXX`) and `event_id` (`EVT_XXXXXX`) for seamless evaluation via precision-recall curves, ROC-AUC, and confusion matrices.
