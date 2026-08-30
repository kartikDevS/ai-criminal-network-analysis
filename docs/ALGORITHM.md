# Algorithm & Analytical Architecture

**Status:** PLANNED / UNDER SPECIFICATION  
**Primary Owner:** System Architect & AI/ML Member

---

## 1. Graph Analytical Algorithms

### 1.1 Community Detection (Louvain / Leiden)
- **Objective:** Discover densely interconnected sub-networks of persons, accounts, and shared devices representing potential fraud rings or syndicate cells.
- **Formula:** Optimize modularity $Q$:
  $$Q = \frac{1}{2m} \sum_{ij} \left[ A_{ij} - \frac{k_i k_j}{2m} \right] \delta(c_i, c_j)$$
- **Status:** `TO BE IMPLEMENTED` in `graph/algorithms/`

### 1.2 Centrality & Influence (PageRank / Degree Centrality)
- **Objective:** Identify network hubs, bridge nodes connecting disparate criminal groups, and key orchestrators.
- **Status:** `TO BE IMPLEMENTED` in `graph/algorithms/`

---

## 2. Temporal & Spatial Anomaly Detection

### 2.1 Geographic Velocity & Impossible Hops
- **Objective:** Detect impossible transit speeds between sequential location pings ($v = d / \Delta t$).
- **Rule:** If $v > 800\text{ km/h}$ within contiguous ground event pings $\implies$ Flag `LOCATION_ANOMALY`.
- **Status:** `TO BE IMPLEMENTED` in `ml/features/`

### 2.2 Rolling Activity Burst Detection
- **Objective:** Detect sudden surges in transaction volume, rapid calls, or SMS blasting.
- **Formula:** Compute ratio of maximum 7-day event count to annual historical mean baseline:
  $$\text{Burst Ratio} = \frac{\max_{w \in 7d} \text{Events}(w)}{\mu_{\text{annual}} \times 7 + \epsilon}$$
- **Status:** `TO BE IMPLEMENTED` in `ml/features/`

---

## 3. Unsupervised AI/ML Models

### 3.1 Isolation Forest
- **Objective:** Multi-dimensional tree partitioning to isolate anomalies in feature space with few splits.
- **Status:** `TO BE IMPLEMENTED` in `ml/models/`

### 3.2 Graph Neural Networks (Graph Convolutional Networks / GAT)
- **Objective:** Learn node embeddings by aggregating feature information from multi-hop neighborhood topologies.
- **Status:** `TO BE IMPLEMENTED` in `ml/models/`

---

## 4. Composite Risk Scoring & Explainability

$$\text{Composite Risk} = w_1 \cdot \text{IF\_Score} + w_2 \cdot \text{Burst\_Score} + w_3 \cdot \text{Sharing\_Index} + w_4 \cdot \text{Graph\_Centrality}$$

Every alert provides human investigators with the top contributing feature signals (e.g., *“32 transactions in 24h”*, *“Shared IP with 8 known flagged accounts”*, *“Impossible 1,200 km/h velocity hop”*).
