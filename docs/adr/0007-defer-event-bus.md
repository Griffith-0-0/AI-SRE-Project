# ADR-0007: Defer the event bus (Redpanda)

## Status
Accepted

## Context
An event bus decouples telemetry ingestion and enables replay, but at project scale the OTel Collector already buffers and fans out to stores.

## Decision
Start with **OTel Collector → stores directly**. Add **Redpanda** in Phase 2–3 when evidence-replay / incident-snapshot needs a re-readable stream.

## Alternatives considered
- Redpanda from Phase 0 — production-shaped, but an extra service early.
- Plain Kafka — heavier ops than Redpanda.

## Consequences
+ Simpler MVP, faster to a working loop.
− A contained refactor later when the bus is added.
