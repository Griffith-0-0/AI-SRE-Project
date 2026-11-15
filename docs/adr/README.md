# Architecture Decision Records

Consequential decisions get a full ADR here. Trivial conventions stay in [`../decisions.md`](../decisions.md).

| # | Decision | Status |
|---|----------|--------|
| [0001](0001-langgraph-orchestration.md) | LangGraph for agent orchestration | Accepted |
| [0002](0002-multi-provider-model-routing.md) | Multi-provider model routing (DeepSeek + OpenAI) | Accepted |
| [0003](0003-l1-repair-approach.md) | Repair target is L1 (propose patch, human applies) | Accepted |
| [0004](0004-monorepo.md) | Monorepo | Accepted |
| [0005](0005-networkx-first-graph.md) | NetworkX-first root-cause graph | Accepted |
| [0006](0006-keycloak-auth.md) | AuthN/Z with Keycloak from the start | Accepted |
| [0007](0007-defer-event-bus.md) | Defer the event bus (Redpanda) | Accepted |

New ADRs are written automatically when a consequential decision is made (see `AGENTS.md`).
