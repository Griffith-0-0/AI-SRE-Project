# IncidentAI — Planning Decisions & Agreements

> Status log of architecture and planning decisions. Updated 2026-11-14.
> Legend: **Agreed** = locked; **Pending** = awaiting your answer (see `docs/open-questions.md`).

## 1. Project identity

| ID | Decision | Status |
|----|----------|--------|
| P-01 | **IncidentAI** — an autonomous reliability engineering platform: *Detect → Investigate → Simulate → Repair → Learn.* | Agreed |
| P-02 | Three environments (AI Operations Center, Chaos Lab, Incident Arena), but **Chaos Lab + Arena are treated as one evaluation system**: Chaos Lab generates labeled ground-truth incidents; Arena benchmarks humans vs. agents vs. models against them. | Agreed |
| P-03 | **Autonomous code repair is the core differentiator** ("the biggest flex"). It is promoted from optional to a central, deliberate goal — while keeping a human approval gate and honest evaluation. | Agreed |
| P-04 | The project is a **learning vehicle**: real AI-engineering competence over demo polish. | Agreed |
| P-05 | **MVP = one complete vertical slice**: inject → detect → investigate → report → score. Depth over breadth; no feature counts as done until that loop works end-to-end. | Agreed |
| P-06 | **Docs: plain Markdown in-repo** (GitHub-rendered). Add MkDocs Material later only if a portfolio docs site is genuinely wanted. | Agreed |

## 2. Architecture & topology

| ID | Decision | Status |
|----|----------|--------|
| A-01 | **Modular monolith** for the platform itself (not microservices). Split into isolated services only when security/CPU isolation forces it (sandbox, ML inference). | Agreed |
| A-02 | **Python-first** backend (FastAPI + Pydantic). Frontend **React + Vite** (TypeScript). Java/Spring deferred (optional polyglot demo later). | Agreed |
| A-03 | Event-driven **telemetry plane** (async) separated from the request/response **control plane** and long-running **agent workflows** (checkpointed state). | Agreed |
| A-04 | **PostgreSQL is the system of record** (domain data + the evidence ledger: incidents, hypotheses, evidence, provenance). Vector (pgvector) and time-series (TimescaleDB) live in Postgres first. | Agreed |
| A-05 | Root-cause graph starts as **in-memory (NetworkX)**, graduates to **Neo4j Community** when graph queries justify it. | Agreed |
| A-06 | **Infrastructure: Docker Compose first → Kubernetes (k3s) later.** k8s is adopted when Chaos Mesh-grade fault injection and realistic topology are needed. | Agreed |
| A-07 | **Sample app (testbed):** minimal 3-service e-commerce order flow (gateway → orders → inventory) + PostgreSQL + simulated payment stub, with deterministic fault-injection points (env/flags). Python/FastAPI (Spring/Java added later as a polyglot expansion); small enough for the repair agent. | Agreed |
| A-08 | **Monorepo**: platform, demo app, chaos experiments, docs, and skills in one repo (`/platform`, `/apps/demo`, `/chaos`, `/docs`, `/.dsh/skills`). Split the demo app into its own repo later only to demonstrate external-service monitoring. | Agreed |

## 3. Technology stack — open-source tooling + DeepSeek API

| ID | Decision | Status |
|----|----------|--------|
| S-01 | **Tooling must be free/open-source.** The single paid dependency is the DeepSeek LLM API. | Agreed |
| S-02 | **LLM providers: DeepSeek API + OpenAI API**, routed by role via LiteLLM (DeepSeek for high-volume triage/summarization, OpenAI for hard reasoning/coding). Embeddings: **OpenAI `text-embedding-3-small`** (DeepSeek has no embeddings endpoint). | Agreed |
| S-03 | **Model gateway: LiteLLM (MIT)** routes to DeepSeek (OpenAI-compatible) and keeps a swap path to any other provider without code changes. | Agreed |
| S-04 | Observability: **OpenTelemetry + Prometheus + Grafana + Loki + Tempo** (all OSS). Raw telemetry dashboards = Grafana; custom React UI covers investigation/RCA/HITL. | Agreed |
| S-05 | Event bus: **deferred** — start with OTel Collector → stores directly; add **Redpanda** (Kafka-compatible) in Phase 2–3 when the evidence-replay / incident-snapshot feature needs it. | Agreed |
| S-06 | Chaos: **Chaos Toolkit** (Apache-2.0, Compose-friendly) → **Chaos Mesh** (Apache-2.0, k8s-native). | Agreed |
| S-07 | Sandbox: **Docker (hardened) → gVisor/Firecracker** as repair autonomy increases. | Agreed |
| S-08 | LLM observability/eval: **Langfuse (self-host OSS)** + promptfoo + custom scorer; **MLflow** for ML registry. | Agreed |
| S-09 | Anomaly/forecast: **statistical baselines + PyOD + Nixtla statsforecast**; deep learning only if a baseline proves it necessary. | Agreed |
| S-10 | AuthN/Z: **Keycloak (OIDC) from the start** — RBAC for humans, scoped service identities for agents. | Agreed |

## 4. AI engineering

| ID | Decision | Status |
|----|----------|--------|
| AI-01 | Orchestration framework: **LangGraph** (stateful, checkpointed, human-in-the-loop, MCP). | Agreed |
| AI-02 | Structured outputs via **Pydantic / JSON Schema** (hypotheses, evidence, confidence, provenance). | Agreed |
| AI-03 | **Deterministic algorithms detect/correlate; ML scores/forecasts; LLMs reason/explain/write; orchestration manages state + human gates.** No LLM where a query or statistical test is more reliable. | Agreed |
| AI-04 | Investigation tools are **read-only by default**; write tools require escalation. Full audit trail to the evidence ledger. | Agreed |
| AI-05 | Multi-agent = **supervisor + specialists** (telemetry analyst, code analyst, verifier/critic, remediation planner), sharing a DB evidence ledger, not chat context. | Agreed |
| AI-06 | Repair workflow is **test-driven, reproduce-first**: reproduce → localize → patch → test → static check → PR → human approval. Never auto-merge. | Agreed |
| AI-07 | RAG over incident history + code + docs, **hybrid retrieval (BM25 + vectors) + rerank + mandatory citations**. | Agreed |
| AI-08 | Treat all telemetry/logs/code as **untrusted input** (prompt-injection surface). | Agreed |
| AI-09 | **Repair target: L1** — AI proposes a structured patch (diff); human applies; the eval harness verifies (apply + tests) deterministically. **No sandbox** (not needed — the AI doesn't execute). L2 (autonomous sandbox loop) is a later option. | Agreed |

## 5. Evaluation & learning

| ID | Decision | Status |
|----|----------|--------|
| E-01 | **Evaluation-first is non-negotiable.** Reproducible benchmark + hidden hold-out set + CI-run eval suite. | Agreed |
| E-02 | **Evaluation metrics.** Detection: recall, false-positive rate. Investigation: RCA Top-1 & Top-3 accuracy, hallucination rate (unsupported claims). Repair: patch-apply rate, fix success rate (reproduction test passes + no regressions). Ops: cost per incident, time-to-diagnosis, tool-call count. Headline: end-to-end success rate. Optional: confidence calibration, run-to-run variance. | Agreed |
| E-03 | Closed loop: capture resolution outcome → store → use for RAG/few-shot → later preference/fine-tuning data. | Agreed |

## 6. Development assistant

| ID | Decision | Status |
|----|----------|--------|
| D-01 | **DeepSeek (DeepSeek Harness) is the development assistant, not OpenAI Codex.** | Agreed |
| D-02 | Guidance is stored as **markdown files** (context/rules/skills), managed per `docs/deepseek-setup.md`. | Agreed |
| D-03 | Assistant runs in **mentor mode**: guide and review by default; implement **only when explicitly asked** in that turn. | Agreed |

## 7. Cost policy

| ID | Decision | Status |
|----|----------|--------|
| C-01 | **Minimize cost as the primary constraint** (no fixed budget). Levers: tier-based routing (cheap → escalate only on failure), deterministic/ML before LLM, prompt caching, batch API for eval runs, context compression, per-run token budgets. | Agreed |
| C-02 | **Per-run token/budget caps** are enforced as a hard stop (doubles as a safety control against runaway agent loops). | Agreed |
