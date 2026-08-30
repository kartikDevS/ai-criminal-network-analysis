# Data Schema Specification

**Status:** SPECIFIED / READY FOR PIPELINE INTEGRATION  
**Data Policy:** 100% Synthetic, Non-PII, Deterministically Seeded

---

## 1. Entity Tables

| Entity | Primary Key | Attributes |
| :--- | :--- | :--- |
| **Person** | `person_id` (`PER_XXXXXX`) | `age_group`, `gender`, `occupation_category`, `home_location_id`, `account_created_date` |
| **Phone** | `phone_id` (`PH_XXXXXX`) | `owner_person_id`, `carrier_synthetic`, `activation_date`, `is_shared` |
| **Device** | `device_id` (`DEV_XXXXXX`) | `device_type`, `os_synthetic`, `first_seen_date` |
| **IP Address** | `ip_id` (`IP_XXXXXX`) | `ip_synthetic` (RFC 5737 doc range), `ip_type`, `region_synthetic` |
| **Account** | `account_id` (`ACC_XXXXXX`) | `owner_person_id`, `account_type`, `created_date` |
| **Location** | `location_id` (`LOC_XXXXXX`) | `latitude`, `longitude`, `region_name_synthetic` |
| **Organization** | `org_id` (`ORG_XXXXXX`) | `org_type_synthetic`, `region_synthetic` |
| **Case** | `case_id` (`CASE_XXXXXX`) | `case_type_synthetic`, `opened_date`, `status` |

---

## 2. Event Model (`events.csv`)

The central transactional log driving all graph relationships and temporal metrics:

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `event_id` | `string` | Yes | Unique event ID (`EVT_XXXXXX`) |
| `event_type` | `string` | Yes | `call`, `sms`, `transaction`, `login`, `location_ping` |
| `timestamp` | `datetime`| Yes | ISO-8601 `YYYY-MM-DD HH:MM:SS` |
| `source_person_id` | `string` | Yes | Foreign key to initiator `Person` |
| `target_person_id` | `string` | No | Foreign key to recipient `Person` |
| `phone_id` | `string` | No | Foreign key to `Phone` |
| `device_id` | `string` | No | Foreign key to `Device` |
| `ip_id` | `string` | No | Foreign key to `IP` |
| `account_id` | `string` | No | Foreign key to `Account` |
| `location_id` | `string` | Yes | Foreign key to `Location` |
| `amount` | `float` | No | Transaction value in synthetic currency |
| `duration_seconds` | `int` | No | Call duration |
| `direction` | `string` | No | `outbound`, `inbound`, `internal` |
| `status` | `string` | Yes | `completed`, `failed`, `flagged` |
| `channel` | `string` | Yes | `web`, `mobile_app`, `atm`, `pos`, `ussd`, `api` |
| `transaction_type` | `string` | No | `transfer`, `withdrawal`, `deposit`, `payment`, `p2p` |

---

## 3. Derived Graph Relationships (`relationships.csv`)

| Edge Type | Source Node | Target Node | Key Edge Properties |
| :--- | :--- | :--- | :--- |
| `USES_PHONE` | `Person` | `Phone` | `first_seen`, `last_seen`, `event_count`, `weight` |
| `USES_DEVICE` | `Person` | `Device` | `first_seen`, `last_seen`, `event_count`, `weight` |
| `USES_IP` | `Person` | `IP` | `first_seen`, `last_seen`, `event_count`, `weight` |
| `OWNS_ACCOUNT` | `Person` | `Account` | `created_date`, `transaction_count`, `total_volume` |
| `LOCATED_AT` | `Person` | `Location` | `first_seen`, `last_seen`, `event_count` |
| `COMMUNICATES_WITH` | `Person` | `Person` | `first_seen`, `last_seen`, `call_count`, `sms_count`, `total_duration_sec`, `weight` |
| `TRANSACTS_WITH` | `Person` | `Person` | `first_seen`, `last_seen`, `transaction_count`, `total_amount`, `weight` |
| `AFFILIATED_WITH` | `Person` | `Organization` | `affiliation_type`, `first_seen` |
| `LINKED_TO` | `Person` | `Case` | `role`, `linked_date` |

---

## 4. Ground Truth Evaluation Layer (`data/ground_truth/`)

> [!CAUTION]
> **Strict ML Isolation Rule:** Ground truth labels (`entity_labels.csv` and `event_labels.csv`) are exclusively used for model benchmark scoring (precision/recall/ROC-AUC). They must **never** be supplied to model training or inference pipelines as input features.
