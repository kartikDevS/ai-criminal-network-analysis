# AI-Powered Criminal / Cyber Fraud Network Analysis System

> **SIH Hackathon Project**  
> All data used and referenced within this system is **100% synthetic and non-PII**.  
> No real individuals, organizations, phone numbers, IP addresses, or criminal records are represented.

---

## 1. Project Purpose & Vision

The **AI-Powered Criminal / Cyber Fraud Network Analysis System** is an investigative intelligence platform designed to uncover complex cyber fraud rings, money mule networks, SIM box operations, and syndicated criminal activity across heterogeneous data streams.

The system analyzes multi-entity relationships and behavioral histories between:
- **People** (Suspects, mules, merchants, victims, normal users)
- **Phones** (MSISDNs, synthetic carriers, shared SIM cards)
- **Devices** (IMEIs, MACs, OS signatures, multiplexed hardware)
- **IP Addresses** (VPN endpoints, datacenter proxies, residential gateways)
- **Accounts** (Bank accounts, digital wallets, crypto addresses, messaging handles)
- **Locations** (Geographic coordinates, transit hubs, impossible velocity hops)
- **Organizations** (Shell corporations, fintechs, call centers, front businesses)
- **Events** (Calls, SMS, financial transactions, logins, location pings)

### Core Analytical Methodology

$$\text{Intelligence} = \text{DATA} + \text{GRAPH ANALYSIS} + \text{AI/ML} + \text{TEMPORAL ANALYSIS} + \text{ANOMALY DETECTION}$$

```
   ┌─────────────┐       ┌────────────────┐       ┌─────────────────┐
   │ Heterogeneous│  ──>  │ Graph & Entity │  ──>  │ Multi-Signal AI │  ──>  [Explainable Alerts]
   │ Event Logs  │       │ Topologies     │       │ Anomaly Engine  │      (For Human Investigators)
   └─────────────┘       └────────────────┘       └─────────────────┘
```

> [!IMPORTANT]
> **Core Investigative Principle**: The system is an investigative decision-support tool. It detects **ANOMALIES and SUSPICIOUS PATTERNS**; it **DOES NOT** automatically label or declare anyone a criminal. All alerts provide explainable evidentiary chains for human law enforcement and intelligence analysts.

---

## 2. Repository Structure

```
ai-criminal-network-analysis/
│
├── README.md                 # Project manifesto, architecture & team workflow
├── .gitignore                # Git ignore rules for Python, ML models & data
├── .env.example              # Environment variables template (no real secrets)
├── requirements.txt          # Python dependencies
│
├── docs/                     # Comprehensive architecture & design specifications
│   ├── PROJECT_OVERVIEW.md   # System architecture & component interaction
│   ├── DATA_SCHEMA.md        # Entity, event, and graph relationship schemas
│   ├── ALGORITHM.md          # Graph and ML anomaly detection algorithms
│   ├── API.md                # Backend REST API endpoint specifications
│   ├── SECURITY.md           # Security policies, RBAC, and data privacy
│   ├── RESEARCH.md           # Academic citations, benchmarks, and competitor analysis
│   ├── SETUP.md              # Local developer environment setup guide
│   └── CONTRIBUTING.md       # Git collaboration rules & PR guidelines
│
├── data/                     # Data directory (Large raw data is git-ignored)
│   ├── sample/               # Small human-readable synthetic datasets for testing
│   ├── processed/            # Normalized, graph-ready dataset exports
│   └── README.md             # Data guidelines & synthetic commitment
│
├── data_pipeline/            # Data engineering pipeline stages
│   ├── generate/             # Synthetic generation engine
│   ├── cleaning/             # Data sanitization & null standardization
│   ├── normalization/        # Schema & ISO timestamp normalization
│   ├── validation/           # Automated referential integrity checks
│   └── processing/           # Graph relationship & edge feature extraction
│
├── ml/                       # Machine learning & statistical models
│   ├── features/             # Feature engineering & extraction algorithms
│   ├── models/               # Model definitions (Isolation Forest, GNNs, Autoencoders)
│   ├── training/             # Model training pipelines & cross-validation
│   ├── evaluation/           # Benchmark metrics (Precision, Recall, ROC-AUC)
│   └── inference/            # Real-time and batch scoring services
│
├── graph/                    # Graph database & network analysis
│   ├── neo4j/                # Neo4j schema DDL, constraints, and import scripts
│   ├── queries/              # Cypher query library for investigation patterns
│   └── algorithms/           # Community detection (Louvain), PageRank, Centrality
│
├── backend/                  # Application backend services
│   ├── api/                  # FastAPI routers and route handlers
│   ├── services/             # Core business logic & graph orchestrators
│   └── config/               # Application settings & environment loaders
│
├── frontend/                 # User interface & investigative dashboard
│   ├── components/           # Reusable UI widgets & graph visualizers
│   ├── pages/                # Investigation views, network dashboards, alert feeds
│   └── services/             # Frontend API client services
│
├── security/                 # System security & compliance
│   ├── authentication/       # JWT token management & session security
│   ├── authorization/        # Role-Based Access Control (RBAC)
│   ├── validation/           # Input sanitization & injection defenses
│   └── security_tests/       # Automated security audit scripts
│
├── research/                 # Research papers, competitor benchmarks & notes
│   ├── papers/               # Summaries of graph ML & fraud literature
│   ├── competitors/          # Industry benchmark analysis (Palantir, Neo4j Bloom)
│   ├── features/             # Novel feature proposals & ablation studies
│   └── findings/             # Experimental results & architectural learnings
│
├── tests/                    # Automated testing suite
│   ├── data/                 # Data validation & schema tests
│   ├── ml/                   # Model performance & feature unit tests
│   ├── graph/                # Graph query & topology integrity tests
│   ├── backend/              # API endpoint & service integration tests
│   └── security/             # Vulnerability & authorization tests
│
└── scripts/                  # Helper utilities, seed runners, and dev tools
    └── README.md
```

---

## 3. Team Git Branching Model

To ensure clean, conflict-free collaboration during the hackathon, we follow a strict branch strategy:

| Branch Name | Purpose | Scope |
| :--- | :--- | :--- |
| `main` | **Production / Stable Release** | Only merged via reviewed Pull Requests. Always kept deployable. |
| `data` | **Dataset & Data Pipeline** | Synthetic data generation, cleaning, normalization, and validation scripts. |
| `ml` | **Machine Learning & AI** | Feature extraction, model training, anomaly detection, evaluation scripts. |
| `architect` | **System Architecture & Graph** | Graph algorithms, Cypher queries, Neo4j schema, community detection. |
| `security` | **Cybersecurity & Hardening** | Authentication, authorization (RBAC), data privacy, vulnerability audits. |
| `research` | **Research & Benchmarking** | Literature analysis, feature proposals, empirical findings, documentation. |
| `integration` | **System Integration & UI/API** | Backend APIs, frontend dashboards, end-to-end glue, testing suites. |

---

## 4. Role Ownership Matrix

Each team member has primary ownership over specific architectural layers:

```
┌───────────────────────────┬────────────────────────────────────────────────────────┐
│ Role                      │ Owned Directories & Documentation                      │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 🧑‍💻 Data Member           │ data/, data_pipeline/, docs/DATA_SCHEMA.md             │
│ 🤖 AI/ML Member           │ ml/, tests/ml/                                         │
│ 🏛️ System Architect       │ graph/algorithms/, docs/ALGORITHM.md, tests/graph/     │
│ 🛡️ Cybersecurity Member   │ security/, tests/security/, docs/SECURITY.md           │
│ 🔬 Researcher             │ research/, docs/RESEARCH.md                            │
│ 🔌 Integration Member     │ backend/, frontend/, tests/, scripts/                  │
└───────────────────────────┴────────────────────────────────────────────────────────┘
```

---

## 5. Sample Data & Privacy Policy

1. **Synthetic Commitment**: All project data is strictly synthetic. Never commit or scrape real PII.
2. **Git Data Policy**:
   - `data/sample/`: Contains small, human-readable synthetic datasets (~100 entities) tracked in Git for testing.
   - `data/raw/` & `data/processed/`: Large generated datasets are **git-ignored** to keep the repository lightweight.

---

## 6. Data & Model Handoff Workflow

```
[DATA MEMBER]
      │  Generates & Validates Synthetic Dataset
      ▼
[data/sample/ committed]  ──>  [Push to 'data' branch]  ──>  [PR to 'main']
                                                                    │
                                                                    ▼
                                                            [ML MEMBER]
                                                            Pulls updated 'main'
                                                            Trains & benchmarks models
```
