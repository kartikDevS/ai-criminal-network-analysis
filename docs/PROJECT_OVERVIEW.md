# Project Overview: AI-Powered Criminal / Cyber Fraud Network Analysis System

**Project Status:** Active Development (Hackathon Foundation Stage)  
**System Architecture:** Multi-Layered Intelligence & Graph Analytics Platform

---

## 1. Problem Statement

Modern cyber fraud syndicates, money mule networks, and illicit cyber enterprises exploit fragmented systems:
- They use multi-device multiplexing, SIM boxes, and rotating proxies to obscure individual footprints.
- Financial transactions are layered across accounts, wallets, and synthetic identities in rapid succession.
- Traditional relational database queries struggle to traverse multi-hop relationship chains and temporal bursts.

## 2. Solution Vision

This system builds an end-to-end intelligence engine that combines:
1. **Heterogeneous Graph Construction**: Unifying persons, phones, devices, IPs, accounts, locations, and organizations into an interconnected knowledge graph.
2. **Temporal & Spatial Analytics**: Calculating velocity hops, circadian regularity, burst frequency, and relationship growth rates over time.
3. **Multi-Signal Anomaly Detection**: Combining graph centrality, community modularity, and machine learning models (Isolation Forest, Autoencoders, Graph Neural Networks) to isolate high-risk subgraphs.
4. **Investigative Decision Support**: Delivering interactive visual graph exploration, explainable evidentiary timelines, and risk scores for human analysts.

---

## 3. System Architecture & Components

```
   ┌─────────────────────────────────────────────────────────────┐
   │                     PRESENTATION LAYER                      │
   │      Frontend UI (Investigation Dashboard, Graph Canvas)     │
   │                     [STATUS: PLANNED]                       │
   └──────────────────────────────┬──────────────────────────────┘
                                  │ REST / WebSocket
   ┌──────────────────────────────▼──────────────────────────────┐
   │                    APPLICATION / API LAYER                  │
   │           FastAPI Backend Services & Orchestration          │
   │                     [STATUS: PLANNED]                       │
   └───────────────┬─────────────────────────────┬───────────────┘
                   │                             │
   ┌───────────────▼─────────────┐ ┌─────────────▼───────────────┐
   │         GRAPH LAYER         │ │          AI / ML LAYER      │
   │  Neo4j Knowledge Graph,     │ │ Feature Store, Anomaly      │
   │  Cypher Queries, Community  │ │ Models, Inference Engine    │
   │  Detection (Louvain/PageRank│ │ [STATUS: PLANNED]           │
   │  [STATUS: PLANNED]          │ │                             │
   └───────────────▲─────────────┘ └─────────────▲───────────────┘
                   │                             │
   ┌───────────────┴─────────────────────────────┴───────────────┐
   │                  DATA & ETL PIPELINE LAYER                  │
   │  Synthetic Generator, Clean, Normalize, Validate, Process   │
   │                     [STATUS: SPECIFIED]                     │
   └─────────────────────────────────────────────────────────────┘
```

---

## 4. Analytical Lifecycle

1. **Ingestion & Normalization:** Ingest raw interaction events (calls, SMS, transactions, logins, location pings), enforce RFC 5737 synthetic subnets, and normalize ISO timestamps.
2. **Graph Construction:** Derive weighted, temporal relationship edges (`USES_PHONE`, `USES_DEVICE`, `USES_IP`, `COMMUNICATES_WITH`, `TRANSACTS_WITH`, `LOCATED_AT`).
3. **Feature Computation:** Calculate activity rates, rolling burst ratios, transit speeds, and graph centrality measures.
4. **Anomaly Scoring:** Evaluate multi-signal deviation from normal entity baselines; produce explainable risk score cards.
5. **Human Review:** Visual sub-network inspection with full chain-of-custody metadata.
