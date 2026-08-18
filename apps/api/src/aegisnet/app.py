from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response

from aegisnet.models import Alert, AlertStatusUpdate, Detection
from aegisnet.repository import InMemorySecurityRepository, PostgresSecurityRepository, SecurityRepository
from aegisnet.scoring import ExplainableAnomalyScorer
from aegisnet.service import DetectionService

EVENTS_PROCESSED = Counter("aegisnet_events_processed_total", "Processed safe telemetry events")
ALERTS_CREATED = Counter("aegisnet_alerts_created_total", "Created security alerts", ["severity"])
ANOMALY_SCORE = Histogram("aegisnet_anomaly_score", "Explainable anomaly score")


def build_repository() -> SecurityRepository:
    if os.getenv("AEGISNET_STORE_MODE", "memory") == "postgres":
        return PostgresSecurityRepository(os.environ["AEGISNET_DATABASE_URL"])
    return InMemorySecurityRepository()


def create_app(repository: SecurityRepository | None = None) -> FastAPI:
    app = FastAPI(title="AegisNet", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[os.getenv("AEGISNET_ALLOWED_ORIGIN", "http://localhost:5182")],
        allow_methods=["GET", "POST", "PATCH"],
        allow_headers=["Content-Type"],
    )
    service = DetectionService(repository or build_repository(), ExplainableAnomalyScorer())

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "capturePolicy": "synthetic-or-authorized-fixture-only"}

    @app.get("/api/overview")
    def overview() -> dict[str, object]:
        return service.overview()

    @app.get("/api/events", response_model=list[Detection])
    def events() -> list[Detection]:
        return service.repository.events()

    @app.get("/api/alerts", response_model=list[Alert])
    def alerts() -> list[Alert]:
        return service.repository.alerts()

    @app.post("/api/demo/seed", response_model=list[Alert])
    def seed_safe_demo() -> list[Alert]:
        alerts = service.seed_safe_demo()
        for event in service.repository.events()[:4]:
            EVENTS_PROCESSED.inc()
            ANOMALY_SCORE.observe(event.score)
        for alert in alerts:
            ALERTS_CREATED.labels(alert.detection.severity.value).inc()
        return alerts

    @app.patch("/api/alerts/{alert_id}", response_model=Alert)
    def update_alert(alert_id: str, update: AlertStatusUpdate) -> Alert:
        alert = service.repository.set_status(alert_id, update.status)
        if alert is None:
            raise HTTPException(status_code=404, detail="Alert not found")
        return alert

    @app.get("/metrics")
    def metrics() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    return app


app = create_app()
