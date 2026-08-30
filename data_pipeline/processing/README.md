# Graph Processing & Feature Derivation

**Status:** PLANNED / SPECIFIED  
**Primary Owner:** Data Member & System Architect  
**Branch:** `data` / `architect`

---

## Purpose & Scope

This module processes events to construct the graph representation:
- Deriving relationship edges (`USES_PHONE`, `USES_DEVICE`, `USES_IP`, `COMMUNICATES_WITH`, `TRANSACTS_WITH`, `LOCATED_AT`).
- Aggregating edge attributes: `first_seen`, `last_seen`, `event_count`, `weight`.
- Exporting Neo4j-ready node and edge CSV files.
