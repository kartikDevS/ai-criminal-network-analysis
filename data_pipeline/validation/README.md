# Data Validation Suite

**Status:** PLANNED / SPECIFIED  
**Primary Owner:** Data Member  
**Branch:** `data`

---

## Purpose & Scope

Automated quality assurance suite that validates:
- 100% Primary Key uniqueness and non-nullness.
- 100% Foreign Key referential integrity across all entities and event logs.
- RFC 5737 non-routable synthetic IP ranges and zero PII.
- Generates data quality markdown reports.
