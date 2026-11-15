# ADR-0005: NetworkX-first root-cause graph

## Status
Accepted

## Context
The root-cause graph (services as nodes, dependencies as edges) is derived data built from telemetry/domain data in Postgres. At project scale the graph is small.

## Decision
Start with **in-memory NetworkX**, rebuilt on demand from Postgres. Graduate to **Neo4j Community** only when graph size or concurrent queries justify it.

## Alternatives considered
- Neo4j from the start — persistent Cypher, but dual-write sync and extra ops.
- Postgres + Apache AGE — extra extension complexity.

## Consequences
+ No extra service; no dual-write sync problem.
+ Same algorithms (traversal, centrality) available.
− Rebuild cost per query; acceptable at small scale.
