"""Gateway service entry point."""

from fastapi import FastAPI

app = FastAPI(title="IncidentAI Demo Gateway", version="0.0.1")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe; also the Phase 0.2 smoke check."""
    return {"status": "ok", "service": "gateway"}
