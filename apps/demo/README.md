# Demo app (the testbed)

Minimal 3-service e-commerce order flow used to generate labeled incidents:
**gateway (8000) → orders (8001) → inventory (8002)** + PostgreSQL + payment stub (8003).

Full contract in [`docs/sample-app-spec.md`](../../docs/sample-app-spec.md).

## Run the gateway (Phase 0.2)

```bash
uv sync
uv run uvicorn demo_app.gateway.main:app --reload --port 8000
curl http://127.0.0.1:8000/health
```

## Test

```bash
uv run pytest
```
