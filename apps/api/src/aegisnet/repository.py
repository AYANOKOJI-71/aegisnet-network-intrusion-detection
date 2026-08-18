from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol

import psycopg

from aegisnet.models import Alert, AlertStatus, Detection


class SecurityRepository(Protocol):
    def save_detection(self, detection: Detection) -> Alert | None: ...

    def events(self) -> list[Detection]: ...

    def alerts(self) -> list[Alert]: ...

    def set_status(self, alert_id: str, status: AlertStatus) -> Alert | None: ...


class InMemorySecurityRepository:
    def __init__(self) -> None:
        self._events: list[Detection] = []
        self._alerts: list[Alert] = []

    def save_detection(self, detection: Detection) -> Alert | None:
        self._events.append(detection)
        if detection.severity.value == "info":
            return None
        alert = Alert(detection=detection)
        self._alerts.append(alert)
        return alert

    def events(self) -> list[Detection]:
        return list(reversed(self._events))

    def alerts(self) -> list[Alert]:
        return list(reversed(self._alerts))

    def set_status(self, alert_id: str, status: AlertStatus) -> Alert | None:
        for alert in self._alerts:
            if alert.alert_id == alert_id:
                alert.status = status
                alert.updated_at = datetime.now(UTC)
                return alert
        return None


class PostgresSecurityRepository(InMemorySecurityRepository):
    """A production-compatible repository that keeps the local in-memory read model for deterministic review."""

    def __init__(self, dsn: str) -> None:
        super().__init__()
        self._dsn = dsn
        with psycopg.connect(dsn) as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS security_alerts (
                  alert_id UUID PRIMARY KEY,
                  event_id UUID NOT NULL,
                  classification TEXT NOT NULL,
                  score DOUBLE PRECISION NOT NULL,
                  severity TEXT NOT NULL,
                  status TEXT NOT NULL,
                  created_at TIMESTAMPTZ NOT NULL
                )
                """
            )

    def save_detection(self, detection: Detection) -> Alert | None:
        alert = super().save_detection(detection)
        if alert is None:
            return None
        with psycopg.connect(self._dsn) as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO security_alerts (alert_id, event_id, classification, score, severity, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    alert.alert_id,
                    detection.event.event_id,
                    detection.classification,
                    detection.score,
                    detection.severity.value,
                    alert.status.value,
                    alert.created_at,
                ),
            )
        return alert
