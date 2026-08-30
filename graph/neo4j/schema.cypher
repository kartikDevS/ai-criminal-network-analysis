// =============================================================
// schema.cypher
// Neo4j DDL & Graph Ingestion Script for Fraud Network System
// =============================================================

// -------------------------------------------------------------
// 1. Uniqueness Constraints & Indexes
// -------------------------------------------------------------

CREATE CONSTRAINT unique_person_id IF NOT EXISTS
FOR (p:Person) REQUIRE p.person_id IS UNIQUE;

CREATE CONSTRAINT unique_phone_id IF NOT EXISTS
FOR (ph:Phone) REQUIRE ph.phone_id IS UNIQUE;

CREATE CONSTRAINT unique_device_id IF NOT EXISTS
FOR (d:Device) REQUIRE d.device_id IS UNIQUE;

CREATE CONSTRAINT unique_ip_id IF NOT EXISTS
FOR (i:IP) REQUIRE i.ip_id IS UNIQUE;

CREATE CONSTRAINT unique_account_id IF NOT EXISTS
FOR (a:Account) REQUIRE a.account_id IS UNIQUE;

CREATE CONSTRAINT unique_location_id IF NOT EXISTS
FOR (l:Location) REQUIRE l.location_id IS UNIQUE;

CREATE CONSTRAINT unique_org_id IF NOT EXISTS
FOR (o:Organization) REQUIRE o.org_id IS UNIQUE;

CREATE CONSTRAINT unique_case_id IF NOT EXISTS
FOR (c:Case) REQUIRE c.case_id IS UNIQUE;

CREATE INDEX event_timestamp_idx IF NOT EXISTS
FOR ()-[r:TRANSACTS_WITH]-() REQUIRE r.last_seen;

CREATE INDEX comm_timestamp_idx IF NOT EXISTS
FOR ()-[r:COMMUNICATES_WITH]-() REQUIRE r.last_seen;

// -------------------------------------------------------------
// 2. Node Ingestion (LOAD CSV from import/)
// -------------------------------------------------------------

// Persons
LOAD CSV WITH HEADERS FROM 'file:///nodes_persons.csv' AS row
MERGE (p:Person {person_id: row.person_id})
ON CREATE SET
  p.age_group = row.age_group,
  p.gender = row.gender,
  p.occupation_category = row.occupation_category,
  p.home_location_id = row.home_location_id,
  p.account_created_date = date(row.account_created_date);

// Phones
LOAD CSV WITH HEADERS FROM 'file:///nodes_phones.csv' AS row
MERGE (ph:Phone {phone_id: row.phone_id})
ON CREATE SET
  ph.carrier = row.carrier_synthetic,
  ph.activation_date = date(row.activation_date),
  ph.is_shared = toBoolean(row.is_shared);

// Devices
LOAD CSV WITH HEADERS FROM 'file:///nodes_devices.csv' AS row
MERGE (d:Device {device_id: row.device_id})
ON CREATE SET
  d.device_type = row.device_type,
  d.os = row.os_synthetic,
  d.first_seen_date = date(row.first_seen_date);

// IPs
LOAD CSV WITH HEADERS FROM 'file:///nodes_ips.csv' AS row
MERGE (i:IP {ip_id: row.ip_id})
ON CREATE SET
  i.ip_address = row.ip_synthetic,
  i.ip_type = row.ip_type,
  i.region = row.region_synthetic;

// Accounts
LOAD CSV WITH HEADERS FROM 'file:///nodes_accounts.csv' AS row
MERGE (a:Account {account_id: row.account_id})
ON CREATE SET
  a.account_type = row.account_type,
  a.created_date = date(row.created_date);

// Locations
LOAD CSV WITH HEADERS FROM 'file:///nodes_locations.csv' AS row
MERGE (l:Location {location_id: row.location_id})
ON CREATE SET
  l.latitude = toFloat(row.latitude),
  l.longitude = toFloat(row.longitude),
  l.region_name = row.region_name_synthetic;

// Organizations
LOAD CSV WITH HEADERS FROM 'file:///nodes_organizations.csv' AS row
MERGE (o:Organization {org_id: row.org_id})
ON CREATE SET
  o.org_type = row.org_type_synthetic,
  o.region = row.region_synthetic;

// Cases
LOAD CSV WITH HEADERS FROM 'file:///nodes_cases.csv' AS row
MERGE (c:Case {case_id: row.case_id})
ON CREATE SET
  c.case_type = row.case_type_synthetic,
  c.opened_date = date(row.opened_date),
  c.status = row.status;

// -------------------------------------------------------------
// 3. Dynamic Relationship Ingestion (LOAD CSV from import/relationships.csv)
// -------------------------------------------------------------

LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
CALL {
  WITH row
  WITH row WHERE row.relationship_type = 'USES_PHONE'
  MATCH (p:Person {person_id: row.source_id})
  MATCH (ph:Phone {phone_id: row.target_id})
  MERGE (p)-[r:USES_PHONE]->(ph)
  SET r.first_seen = row.first_seen, r.last_seen = row.last_seen, r.event_count = toInteger(row.event_count), r.weight = toFloat(row.weight)
} IN TRANSACTIONS OF 1000 ROWS;

LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
CALL {
  WITH row
  WITH row WHERE row.relationship_type = 'USES_DEVICE'
  MATCH (p:Person {person_id: row.source_id})
  MATCH (d:Device {device_id: row.target_id})
  MERGE (p)-[r:USES_DEVICE]->(d)
  SET r.first_seen = row.first_seen, r.last_seen = row.last_seen, r.event_count = toInteger(row.event_count), r.weight = toFloat(row.weight)
} IN TRANSACTIONS OF 1000 ROWS;

LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
CALL {
  WITH row
  WITH row WHERE row.relationship_type = 'USES_IP'
  MATCH (p:Person {person_id: row.source_id})
  MATCH (i:IP {ip_id: row.target_id})
  MERGE (p)-[r:USES_IP]->(i)
  SET r.first_seen = row.first_seen, r.last_seen = row.last_seen, r.event_count = toInteger(row.event_count), r.weight = toFloat(row.weight)
} IN TRANSACTIONS OF 1000 ROWS;

LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
CALL {
  WITH row
  WITH row WHERE row.relationship_type = 'COMMUNICATES_WITH'
  MATCH (p1:Person {person_id: row.source_id})
  MATCH (p2:Person {person_id: row.target_id})
  MERGE (p1)-[r:COMMUNICATES_WITH]->(p2)
  SET r.first_seen = row.first_seen, r.last_seen = row.last_seen, r.event_count = toInteger(row.event_count), r.weight = toFloat(row.weight)
} IN TRANSACTIONS OF 1000 ROWS;

LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
CALL {
  WITH row
  WITH row WHERE row.relationship_type = 'TRANSACTS_WITH'
  MATCH (p1:Person {person_id: row.source_id})
  MATCH (p2:Person {person_id: row.target_id})
  MERGE (p1)-[r:TRANSACTS_WITH]->(p2)
  SET r.first_seen = row.first_seen, r.last_seen = row.last_seen, r.event_count = toInteger(row.event_count), r.weight = toFloat(row.weight)
} IN TRANSACTIONS OF 1000 ROWS;

LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
CALL {
  WITH row
  WITH row WHERE row.relationship_type = 'LOCATED_AT'
  MATCH (p:Person {person_id: row.source_id})
  MATCH (l:Location {location_id: row.target_id})
  MERGE (p)-[r:LOCATED_AT]->(l)
  SET r.first_seen = row.first_seen, r.last_seen = row.last_seen, r.event_count = toInteger(row.event_count)
} IN TRANSACTIONS OF 1000 ROWS;
