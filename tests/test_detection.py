from aegisnet.app import create_app
from aegisnet.repository import InMemorySecurityRepository
from aegisnet.scenarios import safe_synthetic_scenarios
from aegisnet.scoring import ExplainableAnomalyScorer
from fastapi.testclient import TestClient


def test_scorer_separates_safe_baseline_from_intrusion_signals() -> None:
    scorer = ExplainableAnomalyScorer()
    detections = [scorer.score(event) for event in safe_synthetic_scenarios()]
    assert detections[0].severity.value == "info"
    assert detections[1].classification == "port-sweep-signal"
    assert detections[2].classification == "authentication-abuse-signal"
    assert detections[3].classification == "dns-exfiltration-signal"


def test_safe_demo_creates_only_explainable_alerts() -> None:
    client = TestClient(create_app(InMemorySecurityRepository()))
    created = client.post("/api/demo/seed")
    assert created.status_code == 200
    assert len(created.json()) == 3
    overview = client.get("/api/overview").json()
    assert overview["eventsProcessed"] == 4
    assert overview["openAlerts"] == 3
    assert overview["capturePolicy"] == "synthetic-or-authorized-fixture-only"


def test_alert_status_transition_is_human_controlled() -> None:
    client = TestClient(create_app(InMemorySecurityRepository()))
    alert_id = client.post("/api/demo/seed").json()[0]["alert_id"]
    response = client.patch(f"/api/alerts/{alert_id}", json={"status": "acknowledged"})
    assert response.status_code == 200
    assert response.json()["status"] == "acknowledged"
