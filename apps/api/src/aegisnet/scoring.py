from __future__ import annotations

from dataclasses import dataclass

from aegisnet.models import Detection, NetworkEvent, Severity


@dataclass(frozen=True)
class FeatureBaseline:
    name: str
    normal_mean: float
    normal_stddev: float
    weight: float
    description: str


BASELINES = (
    FeatureBaseline("flow_count_5m", 12, 6, 0.8, "connection burst"),
    FeatureBaseline("unique_destination_ports_5m", 1, 1, 1.2, "destination-port spread"),
    FeatureBaseline("failed_auth_attempts_5m", 0, 0.75, 1.5, "failed authentication burst"),
    FeatureBaseline("bytes_out", 2_000, 1_250, 0.7, "unusual outbound volume"),
    FeatureBaseline("dns_entropy", 3.2, 0.55, 1.1, "high-entropy DNS signal"),
)


class ExplainableAnomalyScorer:
    """A deterministic weighted z-score model intended for transparent portfolio demonstrations."""

    def score(self, event: NetworkEvent) -> Detection:
        weighted_score = 0.0
        explanations: list[str] = []
        for baseline in BASELINES:
            value = float(getattr(event, baseline.name))
            z_score = max(0.0, (value - baseline.normal_mean) / baseline.normal_stddev)
            weighted_score += z_score * baseline.weight
            if z_score >= 2:
                explanations.append(
                    f"{baseline.description}: {value:g} is {z_score:.1f} standard deviations above the safe baseline"
                )

        score = round(weighted_score, 2)
        severity = self._severity(score)
        classification = self._classification(event, score)
        if not explanations:
            explanations.append("All modeled metadata remains within the deterministic safe baseline.")
        return Detection(
            event=event,
            score=score,
            severity=severity,
            classification=classification,
            explanation=explanations,
        )

    @staticmethod
    def _severity(score: float) -> Severity:
        if score >= 12:
            return Severity.CRITICAL
        if score >= 7:
            return Severity.HIGH
        if score >= 3:
            return Severity.MEDIUM
        return Severity.INFO

    @staticmethod
    def _classification(event: NetworkEvent, score: float) -> str:
        if score < 3:
            return "baseline-telemetry"
        if event.failed_auth_attempts_5m >= 5:
            return "authentication-abuse-signal"
        if event.unique_destination_ports_5m >= 12:
            return "port-sweep-signal"
        if event.dns_entropy >= 5.5 and event.bytes_out >= 20_000:
            return "dns-exfiltration-signal"
        return "multi-feature-anomaly"
