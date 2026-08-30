# Input Validation & Defensive Sanitization

**Status:** PLANNED / SPECIFIED  
**Primary Owner:** Cybersecurity Member  
**Branch:** `security`

---

## Purpose & Scope

- Pydantic request models with strict regex validation for all entity IDs (`PER_XXXXXX`, `EVT_XXXXXX`).
- Parameterized Cypher query builders to eliminate Cypher injection risks.
- HTML/String sanitization to prevent Cross-Site Scripting (XSS) in investigator notes.
