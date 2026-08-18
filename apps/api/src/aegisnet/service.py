from __future__ import annotations

from collections import Counter

from aegisnet.models import Alert, AlertStatus, Detection, NetworkEvent
from aegisnet.repository import PostgresSecurityRepository, SecurityRepository
from aegisnet.scenarios import safe_synthetic_scenarios
from aegisnet.scoring import ExplainableAnomalyScorer


class DetectionService:
    def __init__(self, repository: SecurityRepository, scorer: ExplainableAnomalyScorer) -> None:
        self.repository = repository
        self.scorer = scorer

    def evaluate(self, event: NetworkEvent) -> tuple[Detection, Alert | None]:
        detection = self.scorer.score(event)
        return detection, self.repository.save_detection(detection)

    def seed_safe_demo(self) -> list[Alert]:
        alerts: list[Alert] = []
        for event in safe_synthetic_scenarios():
            _, alert = self.evaluate(event)
            if alert:
                alerts.append(alert)
        return alerts

    def overview(self) -> dict[str, object]:
        events = self.repository.events()
        alerts = self.repository.alerts()
        by_status = Counter(alert.status.value for alert in alerts)
        by_severity = Counter(alert.detection.severity.value for alert in alerts)
        return {
            "eventsProcessed": len(events),
            "alerts": len(alerts),
            "openAlerts": by_status[AlertStatus.OPEN.value],
            "severity": dict(by_severity),
            "mode": "postgres" if isinstance(self.repository, PostgresSecurityRepository) else "deterministic-safe",
            "capturePolicy": "synthetic-or-authorized-fixture-only",
        }
