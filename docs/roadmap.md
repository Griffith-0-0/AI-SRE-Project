# IncidentAI — Development Roadmap

> Detailed, dependency-aware build plan. Aligned with `docs/decisions.md` and `docs/adr/`.
> Effort estimates assume **part-time solo work (~10–15 h/week) with AI mentor assistance** (~20–30% faster than manual), and the **cost-minimization routing** (DeepSeek for volume, OpenAI only for hard steps).

## How to read this

| Tier | Phases | Meaning |
|---|---|---|
| **MVP** | 0–2 | The single vertical slice: *inject → detect → investigate → report → score* |
| **Intermediate** | 3–5 | RAG memory, multi-agent + graph, L1 repair |
| **Advanced** | 6–7 | Formalized benchmark, Arena, k8s |
| **Optional / research** | — | L2 autonomous repair, fine-tuning |

**Rule:** a phase is "done" only when its acceptance criteria pass *and* the whole loop still works end-to-end. No parallel half-built features.

## Timeline (consolidated)

Assumes **part-time ~10–15 h/week with AI mentor assistance**. Full-time (~30–40 h/week) is roughly **2.5× faster**.

| Phase | Effort (part-time) | Cumulative |
|-------|--------------------|------------|
| 0 Foundations | 2–3 wk | 2–3 wk |
| 1 Detect | 2–3 wk | 4–6 wk |
| 2 Investigate *(MVP core)* | 3–4 wk | **7–10 wk → MVP done** |
| 3 RAG memory | 2–3 wk | 9–13 wk |
| 4 Multi-agent + graph | 3–4 wk | 12–17 wk |
| 5 L1 repair | 2–4 wk | **14–21 wk → intermediate done** |
| 6 Formal benchmark | 2–3 wk | 16–24 wk |
| 7 Arena + k8s *(optional)* | 4–6 wk | **20–30 wk → full** |

- **MVP:** ~7–10 weeks (~2–2.5 months)
- **Through repair (intermediate):** ~14–21 weeks (~3.5–5 months)
- **Full platform:** ~20–30 weeks (~5–7 months)

Widest uncertainty: **Phase 2 (agent tuning)** and **Phase 5 (repair)**.

---

## Phase 0 — Foundations (observability + testbed)

**Classification:** MVP · **Rough effort:** 2–3 weeks

- **Objective:** A running, observable testbed — 3-service demo app emitting correlated logs/metrics/traces, with manual fault injection and everything visible in Grafana.
- **Features:**
  - Monorepo scaffold (`/platform`, `/apps/demo`, `/chaos`, `/docs`).
  - Demo e-commerce app: 3 FastAPI services (gateway → orders → inventory) + PostgreSQL + simulated payment stub, fully OTel-instrumented.
  - Docker Compose: demo app + Postgres + OTel Collector + Prometheus + Loki + Tempo + Grafana + Keycloak.
  - OTel Collector with **Drain** log clustering + tail sampling.
  - Deterministic fault-injection hooks in the app (env flags / chaos endpoints) + one manual Chaos Toolkit experiment.
- **Technologies:** Python/FastAPI, Docker Compose, OpenTelemetry, Prometheus, Loki, Tempo, Grafana, Keycloak.
- **Dependencies:** none (only the locked decisions).
- **Deliverables:** `docker compose up` stack; instrumented app; Grafana showing all three signals; one reproducible fault.
- **Technical challenges:** OTel wiring across 3 services; trace correlation; Keycloak realm/client setup.
- **Acceptance criteria:**
  - `docker compose up` brings up the full stack.
  - One end-to-end request produces a **correlated trace** (gateway→orders→inventory) visible in Grafana.
  - One injected fault is visible as an anomaly in the dashboards.
  - Keycloak login gates the platform API.
- **Testing & validation:** per-service smoke tests; a scripted end-to-end request that emits a trace; manual fault-injection walkthrough.
- **AI/SE concepts learned:** observability, distributed tracing, log templating, containers.

---

## Phase 1 — Detect (anomaly → alert → incident)

**Classification:** MVP · **Rough effort:** 2–3 weeks

- **Objective:** Statistical anomaly detection raises incidents; a minimal deterministic injector produces *labeled* ground-truth incidents.
- **Features:**
  - Anomaly detection service (statistical baselines: 3σ / MAD / EWMA, then PyOD).
  - Alert → incident creation in Postgres (evidence ledger).
  - Deterministic fault injector (Chaos Toolkit) producing labeled incidents (true root cause recorded).
  - Optional cheap triage (DeepSeek Flash) to classify anomaly type.
- **Technologies:** PyOD, statsmodels, FastAPI, PostgreSQL, Chaos Toolkit.
- **Dependencies:** Phase 0.
- **Deliverables:** anomaly detector; incident records; a labeled incident set with ground truth.
- **Technical challenges:** low false-positive rate; threshold selection; keeping injection deterministic.
- **Acceptance criteria:**
  - A labeled set of ≥10 injected incidents is captured with ground truth.
  - Detection recall ≥ 90% and false-positive rate ≤ ~1 alert/hour on that set *(calibration targets)*.
  - Each detection creates an incident record with evidence pointers.
- **Testing & validation:** replay injected faults; measure recall/FP; unit tests for detectors.
- **AI/SE concepts learned:** anomaly detection, baselines, alerting, false-positive discipline.

---

## Phase 2 — Investigate (single agent) · *MVP core*

**Classification:** MVP · **Rough effort:** 3–4 weeks

- **Objective:** A single agent with read-only tools produces an evidence-backed root-cause report, scored against the labeled set.
- **Features:**
  - LangGraph single agent over a LiteLLM gateway (multi-provider routing).
  - Read-only tools: `query_metrics`, `query_logs`, `query_traces`, `list_services`, `get_topology`, `search_code`, `retrieve_similar_incident`.
  - Structured outputs (Pydantic): hypotheses with confidence + evidence references.
  - **Incident snapshot** builder (compression of telemetry before the LLM sees it).
  - Eval harness v1: measures RCA Top-1/Top-3, hallucination rate, cost, latency, tool-calls.
- **Technologies:** LangGraph, LiteLLM (DeepSeek Flash + OpenAI mini), Pydantic, PostgreSQL.
- **Dependencies:** Phase 1.
- **Deliverables:** investigation loop; structured reports; first benchmark numbers.
- **Technical challenges:** grounding (avoid hallucinated RCA); tool design; context/cost control.
- **Acceptance criteria:**
  - End-to-end report (hypotheses + evidence + confidence) for a labeled incident.
  - RCA Top-1 ≥ 50%, Top-3 ≥ 75%, hallucination rate ≤ 20% *(calibration targets; no leakage on hold-out)*.
  - Every claim has a provenance pointer.
  - Eval harness reports the metric set reproducibly (N≥3 runs).
- **Testing & validation:** eval harness runs labeled incidents; prompt/tool regression on every change.
- **AI/SE concepts learned:** tool calling, structured outputs, guardrails, context management, agent evaluation.

---

## Phase 3 — Remember (RAG incident memory)

**Classification:** Intermediate · **Rough effort:** 2–3 weeks

- **Objective:** Retrieve similar historical incidents, code, and docs to ground investigations.
- **Features:** pgvector embeddings (OpenAI `text-embedding-3-small`); hybrid retrieval (BM25 + vectors) + cross-encoder rerank; mandatory citations; incident store + postmortem retrieval.
- **Technologies:** pgvector, OpenAI embeddings, cross-encoder rerank.
- **Dependencies:** Phase 2.
- **Deliverables:** retrieval service; cited "similar incident" references in reports.
- **Technical challenges:** relevance tuning; freshness (what changed since the last similar incident).
- **Acceptance criteria:**
  - Recall@5 ≥ 0.8 and MRR ≥ 0.6 on a golden query set *(calibration)*.
  - Citations resolve to real sources.
  - RAG demonstrably improves investigation (A/B vs no-RAG on the benchmark).
- **Testing & validation:** retrieval eval (recall@k, MRR) on golden queries; A/B investigation runs.
- **AI/SE concepts learned:** embeddings, vector search, hybrid retrieval, reranking, RAG.

---

## Phase 4 — Orchestrate (multi-agent + root-cause graph)

**Classification:** Intermediate · **Rough effort:** 3–4 weeks

- **Objective:** Supervisor + specialists collaborate; a NetworkX root-cause graph ranks probable causes.
- **Features:** supervisor + telemetry analyst + code analyst + verifier/critic; evidence-weighted ranking + falsification; NetworkX graph (topology, blast radius, centrality); React Flow visualization.
- **Technologies:** LangGraph (multi-agent), NetworkX, React Flow.
- **Dependencies:** Phases 2–3.
- **Deliverables:** multi-agent orchestration; graph module; interactive RCA visualization.
- **Technical challenges:** conflict resolution; graph correctness; keeping multi-agent cost in check.
- **Acceptance criteria:**
  - Multi-agent ≥ single-agent on RCA Top-1 (no regression).
  - Graph correctly identifies the injected root in ≥ 80% of labeled incidents *(calibration)*.
  - Graph visualization is interactive and evidence-linked.
- **Testing & validation:** same benchmark (single vs multi-agent); graph correctness on injected faults.
- **AI/SE concepts learned:** multi-agent orchestration, critic/falsification, graph-based RCA.

---

## Phase 5 — Repair (L1: propose, verify, human-applies)

**Classification:** Intermediate · **Rough effort:** 2–4 weeks

- **Objective:** AI proposes structured patches; the eval harness verifies; the human applies.
- **Features:** code localization (embeddings + search); structured patch (diff); eval harness that applies the patch to a clean checkout and runs the reproduction test + suite (deterministic pass/fail); scoring (patch-apply rate, fix success).
- **Technologies:** Python diff/patch tooling, pytest harness, isolated Docker container.
- **Dependencies:** Phase 3 (code retrieval), Phase 2.
- **Deliverables:** patch-proposal flow; deterministic verification harness; repair benchmark subset.
- **Technical challenges:** valid diffs; reproduction tests; low multi-file success (mitigate: narrow bug classes first — config/single-file).
- **Acceptance criteria:**
  - Patch-apply rate ≥ 80% and fix-success ≥ 50% on the narrow bug set *(calibration)*.
  - Harness deterministically reports apply/test results.
  - No patch is applied without human review.
- **Testing & validation:** repair benchmark subset; deterministic apply+test harness; regression checks.
- **AI/SE concepts learned:** code repair, reproduction tests, verification, human-in-the-loop.

---

## Phase 6 — Evaluate (formalized benchmark)

**Classification:** Advanced · **Rough effort:** 2–3 weeks

- **Objective:** Chaos Lab formalized as a label generator; hold-out discipline; leaderboard; CI-run evaluation.
- **Features:** incident corpus (train/dev/hold-out), experiment runner, scorers, leaderboard, CI eval on every change, cost/budget tracking.
- **Technologies:** GitHub Actions, promptfoo/custom scorer, Langfuse.
- **Dependencies:** Phase 2+.
- **Deliverables:** reproducible benchmark; hidden hold-out set; CI-enforced metric gates.
- **Technical challenges:** benchmark leakage prevention; variance/reproducibility.
- **Acceptance criteria:**
  - Benchmark is reproducible (N runs, variance reported).
  - Hidden hold-out set exists and is **never touched during development** (CI-enforced).
  - CI fails on metric regression.
  - Leaderboard renders human + agent entries.
- **Testing & validation:** multi-run benchmark with variance; hold-out access audit.
- **AI/SE concepts learned:** evaluation methodology, hold-out discipline, MLOps.

---

## Phase 7 — Arena & scale (optional)

**Classification:** Advanced/Optional · **Rough effort:** 4–6 weeks

- **Objective:** Human-vs-AI benchmarking; Kubernetes + Chaos Mesh; optional fine-tuning.
- **Features:** Arena UI (real-time sessions, human vs agent), replay, model/architecture comparison, k3s + Chaos Mesh deployment, optional preference fine-tuning.
- **Technologies:** k3s, Chaos Mesh, leaderboard UI.
- **Dependencies:** Phase 6.
- **Deliverables:** Arena; replay; leaderboard with human + agent comparison.
- **Technical challenges:** fair comparison; reproducible replay at k8s scale.
- **Acceptance criteria:** leaderboard compares humans vs models; replay reproduces a corpus incident.
- **Testing & validation:** end-to-end benchmark runs on k8s.
- **AI/SE concepts learned:** benchmarking, Kubernetes, (optional) fine-tuning.

---

## Milestone gates (definition of done)

1. **MVP done** = Phases 0–2 pass acceptance; the loop *inject → detect → investigate → report → score* runs end-to-end with honest metrics.
2. **Intermediate done** = Phases 3–5 pass; RAG + multi-agent + L1 repair all measurable on the benchmark.
3. **Advanced done** = Phases 6–7 pass; reproducible hold-out benchmark + Arena.

### Documentation cadence (when to update)

- **Daily:** check off completed tasks in `docs/daily-tasks.md`; commit.
- **Phase end (gate):** reconcile `docs/report.md` with reality and snapshot the current benchmark numbers **before** starting the next phase.
- **On decision:** ADR auto-written (`AGENTS.md`); `docs/decisions.md` updated.

You do **not** proceed to the next phase until the report reflects reality.

## Cost & effort guardrails

- Every phase must **re-run the benchmark** before it is accepted (no metric regression).
- Escalate models **only on failure** (DeepSeek Flash → OpenAI mini → GPT-5.4).
- Budget caps per run (C-02) are enforced from Phase 2 onward.
- Hidden hold-out set is created in Phase 1 and **never edited** after.
