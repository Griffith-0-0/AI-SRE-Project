---
name: observability-sre
description: Use when working on IncidentAI's telemetry — OpenTelemetry Collector, Prometheus/Grafana/Loki/Tempo, log clustering, alerting, and service topology.
---

# Observability & SRE

## Conventions

- Instrument with OpenTelemetry (OTLP). Apply Drain log clustering and tail sampling in the Collector before any LLM sees the data.
- Metrics → Prometheus; logs → Loki; traces → Tempo; raw dashboards → Grafana (reuse, do not rebuild).
- Correlate logs/metrics/traces/deploys deterministically. The LLM narrates; it does not correlate.

## Steps

1. Prefer standard semantic conventions and existing exporters/processors.
2. Keep the telemetry pipeline bounded and loss-tolerant.
3. For any new signal, state its flow: app → Collector → bus → store → query.
