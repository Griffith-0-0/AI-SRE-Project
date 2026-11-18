# IncidentAI

**Detect. Investigate. Simulate. Repair. Learn.**

An evaluation-driven autonomous reliability engineering platform. The design and
build plan live in [`docs/`](docs/): architecture in
[`docs/report.md`](docs/report.md), decisions in
[`docs/decisions.md`](docs/decisions.md), and the session backlog in
[`docs/daily-tasks.md`](docs/daily-tasks.md).

> **Scaffolding reset (2026-11-18):** `platform/` and `apps/demo/` are being rebuilt
> from scratch. The quickstart below works again once Phase 0.1–0.2 are green.

## Layout

| Path | Contents |
|------|----------|
| `platform/` | Platform API — FastAPI modular monolith |
| `apps/demo/` | Instrumented 3-service e-commerce testbed |
| `chaos/` | Deterministic fault-injection experiments |
| `docs/` | Architecture, decisions, ADRs, backlog |
| `.dsh/skills/` | Project skills for the development assistant |

## Quickstart (platform)

```bash
cd platform
uv sync
uv run uvicorn incidentai_platform.main:app --reload --port 8080
```

Health check: `curl http://127.0.0.1:8080/health` → `{"status":"ok","service":"platform"}`.

Tests: `cd platform && uv run pytest`.
