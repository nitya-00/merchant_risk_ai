"""FastAPI application entry point."""

from fastapi import FastAPI


app = FastAPI(title="Merchant Risk AI")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "ok"}
