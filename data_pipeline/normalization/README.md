# Data Normalization Pipeline

**Status:** PLANNED / SPECIFIED  
**Primary Owner:** Data Member  
**Branch:** `data`

---

## Purpose & Scope

This module normalizes cleaned datasets into standardized data structures:
- Converting dates and timestamps into canonical ISO-8601 (`YYYY-MM-DD HH:MM:SS`).
- Validating latitude and longitude coordinate bounds.
- Normalizing boolean fields (`True`/`False`) and categorical casing.
- Outputting to `data/processed/`.
