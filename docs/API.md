# Backend REST API Specification

**Status:** PLANNED / SPECIFIED  
**Framework:** FastAPI (Python 3.10+)  
**Primary Owner:** Integration Member

---

## 1. Overview & Authentication

All API endpoints will require JWT Bearer Token authorization passed in the HTTP Header:
```http
Authorization: Bearer <JWT_ACCESS_TOKEN>
```

---

## 2. Planned REST Endpoints

### 2.1 Entity & Profile Endpoints
- **`GET /api/v1/entities/{entity_id}`**
  - Retrieves entity profile (demographics, associated devices, phones, accounts, risk score).
  - *Status:* `TO BE IMPLEMENTED` in `backend/api/`
- **`GET /api/v1/entities/search?query=...`**
  - Search entities across IDs, phone numbers, device types, or IP addresses.
  - *Status:* `TO BE IMPLEMENTED` in `backend/api/`

### 2.2 Graph Subgraph Endpoints
- **`GET /api/v1/graph/subgraph/{entity_id}?depth=2`**
  - Returns $k$-hop neighborhood graph in JSON format (nodes and edges) for visual rendering.
  - *Status:* `TO BE IMPLEMENTED` in `backend/api/`
- **`GET /api/v1/graph/communities`**
  - Returns detected clusters and modularity groupings from Neo4j.
  - *Status:* `TO BE IMPLEMENTED` in `backend/api/`

### 2.3 Anomaly & Alert Endpoints
- **`GET /api/v1/anomalies/alerts?limit=50&min_severity=high`**
  - Paginated list of flagged anomalous entities, event bursts, and infrastructure sharing spikes.
  - *Status:* `TO BE IMPLEMENTED` in `backend/api/`
- **`GET /api/v1/anomalies/{entity_id}/explain`**
  - Returns feature attribution breakdown explaining why the entity received a high risk score.
  - *Status:* `TO BE IMPLEMENTED` in `backend/api/`

### 2.4 Investigation Cases
- **`POST /api/v1/cases/create`**
  - Creates a new case docket attaching flagged entities and subgraphs.
  - *Status:* `TO BE IMPLEMENTED` in `backend/api/`
