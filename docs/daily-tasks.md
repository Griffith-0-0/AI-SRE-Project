# IncidentAI — Daily Task Backlog (1–2 h/day)

> Product-owner view: each phase is a **sprint**; each checkbox is **one daily session** (~1–2 h).
> You are a team of one, so tasks are **sequential** — always do the next unchecked item. No jumping phases.

## Working agreement (read before every session)

1. **End every session green** — code committed, tests passing, nothing broken. A half-finished task is fine; a broken repo is not.
2. **"Done" = the task's `done-when` line**, not "mostly working."
3. If a task takes **more than 2 sessions**, split it — it was sized wrong.
4. Before starting Phase 2+, skim `docs/decisions.md` — the ground truth.

## Session budget

| Phase | Sessions | Cumulative | Milestone |
|-------|:---:|:---:|---|
| 0 Foundations | ~15 | 15 | |
| 1 Detect | ~13 | 28 | |
| 2 Investigate | ~20 | 48 | **✅ MVP** |
| 3 RAG memory | ~11 | 59 | |
| 4 Multi-agent + graph | ~17 | 76 | |
| 5 L1 repair | ~15 | 91 | **✅ intermediate** |
| 6 Formal benchmark | ~11 | 102 | |
| 7 Arena + k8s *(optional)* | ~22 | 124 | **✅ full** |

At **~1 session/day (5–6 days/week)**: MVP ≈ **2.5–3 months**, full ≈ **5–6 months**.

---

## Phase 0 — Foundations (~15 sessions)

**Sprint goal:** a running, observable 3-service app; one reproducible fault.

- [x] **0.1** Init monorepo. *done-when:* `git init`; `/platform`, `/apps/demo`, `/chaos`, `/docs` exist; one empty FastAPI app boots.
- [x] **0.2** Gateway service skeleton. *done-when:* `/health` returns 200.
- [ ] **0.3** Orders + inventory service skeletons. *done-when:* both `/health` return 200.
- [ ] **0.4** PostgreSQL + payment stub in Compose. *done-when:* services connect to Postgres; stub returns a fake charge.
- [ ] **0.5** End-to-end happy path. *done-when:* a scripted order flows gateway → orders → inventory → payment stub.
- [ ] **0.6** OTel auto-instrumentation on all 3 services. *done-when:* spans emitted (verify in Collector logs).
- [ ] **0.7** OTel Collector config. *done-when:* Drain clustering + tail sampling active.
- [ ] **0.8** Prometheus + Loki + Tempo + Grafana in Compose. *done-when:* all three signals land in Grafana.
- [ ] **0.9** Trace correlation check. *done-when:* one request shows a single trace across gateway→orders→inventory.
- [ ] **0.10** Keycloak in Compose + realm/client. *done-when:* platform API requires a JWT.
- [ ] **0.11** Fault-injection hooks. *done-when:* env flags / chaos endpoints can break DB, delay payment, kill a service.
- [ ] **0.12** First Chaos Toolkit experiment. *done-when:* one experiment injects a fault deterministically and records it.
- [ ] **0.13** Smoke tests + CI. *done-when:* `make test` green; GitHub Actions runs on push.

---

## Phase 1 — Detect (~13 sessions)

**Sprint goal:** anomalies raise incidents; labeled incidents exist.

- [ ] **1.1** Metric query service. *done-when:* a function pulls time-series from Prometheus.
- [ ] **1.2** Statistical baselines (3σ, MAD, EWMA). *done-when:* detector flags a known anomaly in a replayed metric.
- [ ] **1.3** Alert → incident record. *done-when:* a detection writes an incident row in Postgres with evidence pointers.
- [ ] **1.4** PyOD integration. *done-when:* one PyOD model scores a metric window.
- [ ] **1.5** Deterministic injector + ground truth. *done-when:* ≥10 incidents captured, each with a recorded true root cause.
- [ ] **1.6** Recall / false-positive measurement. *done-when:* a script reports detection recall and FP rate on the labeled set.
- [ ] **1.7** (optional) DeepSeek triage classifier. *done-when:* anomaly type classified with a cheap model, cost logged.

---

## Phase 2 — Investigate, single agent (~20 sessions) · *MVP core*

**Sprint goal:** agent produces an evidence-backed root-cause report, scored honestly.

- [ ] **2.1** LiteLLM gateway. *done-when:* one call routed to DeepSeek Flash; model tier config centralized.
- [ ] **2.2** LangGraph skeleton. *done-when:* a minimal graph with one node calls the model and returns text.
- [ ] **2.3** Tool `query_metrics`. *done-when:* returns a bounded, typed metric summary.
- [ ] **2.4** Tools `query_logs` + `query_traces`. *done-when:* return bounded log templates + span tree slices.
- [ ] **2.5** Tools `list_services` + `get_topology`. *done-when:* return service list and dependency edges.
- [ ] **2.6** Tool `search_code`. *done-when:* grep/embedding search over the demo app.
- [ ] **2.7** Tool `retrieve_similar_incident` (stub). *done-when:* returns nothing yet, but the tool is wired.
- [ ] **2.8** Structured outputs. *done-when:* hypotheses are Pydantic objects (claim, evidence refs, confidence).
- [ ] **2.9** Incident snapshot builder. *done-when:* compressed telemetry bundle replaces raw dumps in context.
- [ ] **2.10** Evidence ledger write path. *done-when:* every agent output persists to Postgres with provenance.
- [ ] **2.11** Guardrails. *done-when:* read-only tools enforced; per-run token budget; PII redaction.
- [ ] **2.12** Eval harness v1. *done-when:* runs a labeled incident and reports Top-1/Top-3, hallucination, cost, latency, tool-calls.
- [ ] **2.13** First benchmark run. *done-when:* real numbers captured and written to `docs/`.
- [ ] **2.14** Prompt tuning pass. *done-when:* one metric improves measurably over the baseline; change documented.

---

## Phase 3 — RAG incident memory (~11 sessions)

**Sprint goal:** retrieve similar incidents/code/docs with citations.

- [ ] **3.1** pgvector setup + migrations. *done-when:* embeddings table exists.
- [ ] **3.2** Embedding pipeline. *done-when:* incident reports → OpenAI `text-embedding-3-small` vectors.
- [ ] **3.3** BM25 index. *done-when:* lexical search over incident text.
- [ ] **3.4** Hybrid retrieval + rerank. *done-when:* BM25+vector merged and reranked.
- [ ] **3.5** Citation plumbing. *done-when:* retrieved items carry source references into the report.
- [ ] **3.6** Golden query set + retrieval eval. *done-when:* recall@k and MRR reported.
- [ ] **3.7** A/B vs no-RAG. *done-when:* investigation metric shows RAG effect (better or not — record honestly).

---

## Phase 4 — Multi-agent + root-cause graph (~17 sessions)

**Sprint goal:** supervisor + specialists beat the single agent; graph ranks causes.

- [ ] **4.1** Supervisor node + routing. *done-when:* dispatches to specialists based on incident.
- [ ] **4.2** Telemetry analyst agent. *done-when:* produces evidence summaries into the ledger.
- [ ] **4.3** Code analyst agent. *done-when:* produces code-level findings into the ledger.
- [ ] **4.4** Verifier/critic agent. *done-when:* attempts to falsify the top hypothesis.
- [ ] **4.5** Evidence-weighted ranking. *done-when:* hypotheses ranked deterministically by evidence weight.
- [ ] **4.6** NetworkX topology + blast radius + centrality. *done-when:* graph returns affected-services and ranked roots.
- [ ] **4.7** React Flow visualization. *done-when:* interactive graph renders with evidence links.
- [ ] **4.8** Benchmark single vs multi-agent. *done-when:* comparison numbers recorded (must not regress).

---

## Phase 5 — L1 repair (~15 sessions)

**Sprint goal:** AI proposes patches; the harness verifies; you apply.

- [ ] **5.1** Code localization. *done-when:* agent pins the bug to file/line(s) using search + embeddings.
- [ ] **5.2** Structured patch output. *done-when:* agent emits a clean unified diff.
- [ ] **5.3** Harness: apply + test. *done-when:* clean checkout + `git apply` + reproduction test run, deterministic result.
- [ ] **5.4** Reproduction test generation. *done-when:* a failing test is produced before the patch.
- [ ] **5.5** Narrow bug set. *done-when:* a labeled set of config/single-file bugs with ground-truth fixes.
- [ ] **5.6** Patch-apply + fix-success scoring. *done-when:* both metrics reported on the bug set.
- [ ] **5.7** Human-apply workflow + review UI. *done-when:* you can review and apply a patch from the UI.

---

## Phase 6 — Formal benchmark (~11 sessions)

**Sprint goal:** reproducible, leakage-proof benchmark + leaderboard + CI gate.

- [ ] **6.1** Corpus split (train/dev/hold-out). *done-when:* split scripted; hold-out committed and locked.
- [ ] **6.2** Experiment runner. *done-when:* one command runs the whole benchmark reproducibly.
- [ ] **6.3** Scorers (all metrics). *done-when:* full E-02 metric set computed.
- [ ] **6.4** Leaderboard backend + UI. *done-when:* results list renders.
- [ ] **6.5** CI eval + regression gate. *done-when:* CI runs the benchmark and fails on metric regression.
- [ ] **6.6** Variance/reproducibility runs. *done-when:* N-run variance reported with the score.

---

## Phase 7 — Arena + k8s (optional, ~22 sessions)

**Sprint goal:** human-vs-AI benchmarking; k8s + Chaos Mesh.

- [ ] **7.1** Arena session runner. *done-when:* starts a timed incident challenge.
- [ ] **7.2** Human session flow. *done-when:* a human can debug live against the demo app.
- [ ] **7.3** Replay. *done-when:* a corpus incident replays identically.
- [ ] **7.4** k3s migration. *done-when:* demo app + platform run on k3s.
- [ ] **7.5** Chaos Mesh. *done-when:* a Mesh experiment replaces the manual injector.
- [ ] **7.6** Leaderboard human vs agent. *done-when:* both entry types compared side-by-side.
- [ ] **7.7** (optional) preference fine-tuning. *done-when:* collected human feedback trained into a small model — or explicitly descoped.

---

## Always-visible next step

Keep a sticky at the top of your session: **"What's the next unchecked task?"** Answer it, do it, commit, repeat. Don't plan ahead — the backlog is the plan.
