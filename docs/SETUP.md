# Developer Setup Guide

Follow these steps to set up your local development environment for the **AI-Powered Criminal / Cyber Fraud Network Analysis System**.

---

## 1. Prerequisites

- **Python 3.10+** (Python 3.11 or 3.12 recommended)
- **Git**
- **Neo4j Desktop / Neo4j Community Server** (Optional for graph ingestion)

---

## 2. Local Environment Setup

### 2.1 Clone Repository & Switch to Branch
```bash
git clone <REPOSITORY_URL>
cd ai-criminal-network-analysis

# Checkout your assigned branch (e.g. data, ml, architect, security, research, integration)
git checkout <your-assigned-branch>
```

### 2.2 Create Virtual Environment
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On Linux / macOS:
python3 -m venv venv
source venv/bin/activate
```

### 2.3 Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.4 Configure Environment Variables
```bash
# Copy template configuration
cp .env.example .env

# Edit .env with your local settings if running Neo4j / Backend API
```

---

## 3. Running Automated Tests

```bash
# Run all tests
pytest tests/

# Run tests with coverage
pytest --cov=. tests/
```
