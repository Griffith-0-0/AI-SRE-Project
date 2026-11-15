# IncidentAI Platform

The platform API — modular monolith (see `docs/decisions.md` A-01, `docs/report.md` §4).

## Run

```bash
uv sync
uv run uvicorn incidentai_platform.main:app --reload --port 8080
```

Then `curl http://127.0.0.1:8080/health`.

## Test

```bash
uv run pytest
```

Python 3.11+ (pinned in `.python-version`), dependencies locked in `uv.lock`.
