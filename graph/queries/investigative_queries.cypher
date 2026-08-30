// =============================================================
// investigative_queries.cypher
// Common Investigative Cypher Queries for Fraud Network Analysis
// =============================================================

// 1. Find Highly Shared Devices (Multiplexing / SIM Box / Fraud Cell)
MATCH (d:Device)<-[r:USES_DEVICE]-(p:Person)
WITH d, count(p) AS user_count, collect(p.person_id) AS users
WHERE user_count >= 3
RETURN d.device_id AS device_id, d.device_type AS type, d.os AS os, user_count, users
ORDER BY user_count DESC;

// 2. Find High-Risk Shared IPs (Proxy / VPN / Botnet Infrastructure)
MATCH (i:IP)<-[r:USES_IP]-(p:Person)
WITH i, count(p) AS user_count, collect(p.person_id) AS users
WHERE user_count >= 4
RETURN i.ip_id AS ip_id, i.ip_address AS ip, i.ip_type AS type, user_count, users
ORDER BY user_count DESC;

// 3. Multi-Hop Money Mule Chains (Transaction Layering)
MATCH path = (p1:Person)-[:TRANSACTS_WITH*2..4]->(p2:Person)
WHERE p1 <> p2
RETURN path, length(path) AS hop_count
LIMIT 25;

// 4. 2-Hop Neighborhood Subgraph for a Flagged Entity
MATCH (p:Person {person_id: 'PER_000005'})-[r]-(target)
OPTIONAL MATCH (target)-[r2]-(second_hop)
WHERE second_hop <> p
RETURN p, r, target, r2, second_hop
LIMIT 100;

// 5. Co-Location and Mobility Overlap
MATCH (p1:Person)-[l1:LOCATED_AT]->(loc:Location)<-[l2:LOCATED_AT]-(p2:Person)
WHERE p1.person_id < p2.person_id
RETURN p1.person_id, p2.person_id, loc.location_id, loc.region_name
LIMIT 50;
