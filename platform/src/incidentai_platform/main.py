"""IncidentAI platform API entry point."""

from fastapi import FastAPI

app = FastAPI(title="IncidentAI Platform", version="0.0.1")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness/readiness probe used by local dev and Compose."""
    return {"status": "ok", "service": "platform"}
