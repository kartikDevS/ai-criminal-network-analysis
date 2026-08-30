# Data Directory

**Primary Owner:** Data Member  
**Status:** SPECIFIED / SAMPLE DATA READY

---

## Directory Structure

- **`sample/`**: Small, human-readable synthetic datasets (~100 entities) tracked in Git for local testing and CI/CD verification.
- **`processed/`**: Output directory for normalized, graph-ready dataset exports (git-ignored, kept via `.gitkeep`).

---

## Data Policies

1. **100% Synthetic Commitment:** Never store real PII or real transaction records.
2. **Git Data Rules:** Large raw datasets (`data/raw/`, `data/large/`) are strictly git-ignored.
