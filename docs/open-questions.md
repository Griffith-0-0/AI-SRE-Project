# IncidentAI — Open Questions & Decisions to Answer

Answer each item (inline or reply in chat). Each has a recommended default; pick it, override it, or defer it.

## Models & API (answer first)

- [x] **Q-01 — Embeddings.** ✅ Resolved: OpenAI embeddings API (`text-embedding-3-small`, ~$0.02/M) — API-based, since DeepSeek exposes no embeddings endpoint.
- [x] **Q-02 — API budget.** ✅ Resolved: no fixed budget — minimize cost as much as possible (levers recorded in decisions.md C-01).
- [x] **Q-03 — Model selection.** ✅ Resolved via the routing table (decisions.md S-02): DeepSeek Flash for volume, OpenAI mini/frontier for coding/reasoning, tiered via LiteLLM.

## Stack confirmations

- [x] **Q-04 — Orchestration.** ✅ Resolved: LangGraph (stateful, checkpointed, human-in-the-loop, MCP).
- [x] **Q-05 — Event bus.** ✅ Resolved: defer — start direct (Collector → stores), add Redpanda in Phase 2–3 when evidence replay needs it.
- [x] **Q-06 — Graph.** ✅ Resolved: NetworkX-first (in-memory, derived from Postgres); Neo4j later only when graph size/concurrency justify it.
- [x] **Q-07 — Frontend.** ✅ Resolved: React + Vite (TypeScript, no SSR).
- [x] **Q-08 — AuthN/Z.** ✅ Resolved: Keycloak (OIDC) from the start.

## Scope & content

- [x] **Q-09 — Sample app.** ✅ Resolved: minimal 3-service e-commerce order flow (gateway → orders → inventory) + Postgres + external payment stub, with deterministic fault-injection points.
- [x] **Q-10 — Repair target.** ✅ Resolved: start with easy, single-file Python bugs in the sample app; expand to multi-file, then a Spring service later as the polyglot showcase.
- [x] **Q-11 — MVP freeze.** ✅ Resolved: MVP = one vertical slice (inject → detect → investigate → report → score), not the full feature list.
- [x] **Q-12 — Repair honesty.** ✅ Resolved: **L1** — AI proposes a structured patch (diff); human applies; the eval harness verifies (apply + tests). No sandbox required. L2 sandbox loop is a later option. The "flex" is the safe, verifiable, measurable pipeline + honest benchmark numbers.

## Repository & documentation

- [x] **Q-13 — Repo layout.** ✅ Resolved: monorepo — `/platform`, `/apps/demo`, `/chaos`, `/docs`, `/.dsh/skills`, `AGENTS.md`.
- [x] **Q-14 — Docs tooling.** ✅ Resolved: plain Markdown in-repo now (GitHub-rendered); MkDocs Material later only if a portfolio docs site is wanted.
- [x] **Q-15 — ADR scope.** ✅ Resolved: lightweight ADRs for consequential decisions, **automated** (written when warranted). Seeded at `docs/adr/` (0001–0007).

## Evaluation specifics

- [x] **Q-16 — Metrics.** ✅ Resolved: curated set in decisions.md E-02 (detection recall/FP, RCA Top-1/Top-3, hallucination, patch-apply + fix success, cost, time-to-diagnosis, tool-calls, end-to-end success, reproducibility).
- [x] **Q-17 — Hold-out discipline.** ✅ Resolved: a hidden incident set, never used during development, to prevent benchmark leakage.
