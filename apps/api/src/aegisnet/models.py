from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class AlertStatus(StrEnum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class Severity(StrEnum):
    INFO = "info"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NetworkEvent(BaseModel):
    """Normalized metadata from a safe synthetic record or an authorized fixture PCAP."""

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    observed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source: str
    destination: str
    protocol: Literal["TCP", "UDP", "DNS", "ICMP"]
    destination_port: int = Field(ge=0, le=65535)
    bytes_out: int = Field(ge=0)
    flow_count_5m: int = Field(ge=0)
    unique_destination_ports_5m: int = Field(ge=0)
    failed_auth_attempts_5m: int = Field(ge=0)
    dns_entropy: float = Field(ge=0, le=8)
    scenario: str = "baseline"
    source_kind: Literal["synthetic", "authorized-fixture"] = "synthetic"


class Detection(BaseModel):
    event: NetworkEvent
    score: float
    severity: Severity
    classification: str
    explanation: list[str]


class Alert(BaseModel):
    alert_id: str = Field(default_factory=lambda: str(uuid4()))
    detection: Detection
    status: AlertStatus = AlertStatus.OPEN
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AlertStatusUpdate(BaseModel):
    status: AlertStatus
