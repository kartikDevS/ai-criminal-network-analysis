# Research, Literature & Competitive Analysis

**Status:** PLANNED / SPECIFIED  
**Primary Owner:** Researcher

---

## 1. Academic & Industry Literature

Key research domains guiding this project:

1. **Graph Neural Networks for Financial Fraud:**
   - *Semi-Supervised Classification with Graph Convolutional Networks (Kipf & Welling)*
   - *Graph-based Anomaly Detection in Transaction Networks (Akoglu et al.)*
2. **Temporal & Spatio-Temporal Graph Mining:**
   - Dynamic network representations, time-decayed edge weighting, and continuous-time dynamic graph embeddings.
3. **Syndicate & Community Detection:**
   - Modularity optimization algorithms (Louvain, Leiden) in bipartite and heterogeneous graphs.

---

## 2. Competitor & Benchmark Analysis

| Solution | Strengths | Limitations | Our Competitive Advantage |
| :--- | :--- | :--- | :--- |
| **Palantir Gotham / Foundry** | Enterprise data fusion, rich graph visualization | High licensing cost, proprietary, complex deployment | Lightweight, open-source stack, purpose-built for cyber fraud syndicates |
| **Neo4j Bloom / Linkurious** | Intuitive Cypher visualizer | Relies primarily on manual rule-based Cypher queries | Automated multi-signal ML anomaly scoring combined with graph visualization |
| **Traditional Rule Engines** | Fast threshold checks | High false positive rate, blind to multi-hop mule networks | Multi-entity topology traversal + temporal burst correlation |

---

## 3. Planned Research Outputs

- `research/papers/`: Detailed literature summaries on GNN fraud detection and graph anomaly benchmarks.
- `research/competitors/`: Feature comparison matrix against existing AML/CFT investigative tools.
- `research/features/`: Ablation studies on graph centrality vs temporal feature importance.
- `research/findings/`: Experimental findings from model evaluations.
