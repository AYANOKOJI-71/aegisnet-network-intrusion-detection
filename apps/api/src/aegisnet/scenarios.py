from __future__ import annotations

from aegisnet.models import NetworkEvent


def safe_synthetic_scenarios() -> list[NetworkEvent]:
    """Return fixed, non-routable metadata-only scenarios with no real traffic generation."""

    return [
        NetworkEvent(
            source="192.0.2.21",
            destination="203.0.113.80",
            protocol="TCP",
            destination_port=443,
            bytes_out=1_940,
            flow_count_5m=10,
            unique_destination_ports_5m=1,
            failed_auth_attempts_5m=0,
            dns_entropy=3.1,
            scenario="normal-web-session",
        ),
        NetworkEvent(
            source="192.0.2.44",
            destination="203.0.113.80",
            protocol="TCP",
            destination_port=0,
            bytes_out=1_300,
            flow_count_5m=78,
            unique_destination_ports_5m=39,
            failed_auth_attempts_5m=0,
            dns_entropy=3.0,
            scenario="safe-port-sweep-signal",
        ),
        NetworkEvent(
            source="198.51.100.55",
            destination="203.0.113.80",
            protocol="TCP",
            destination_port=443,
            bytes_out=2_400,
            flow_count_5m=24,
            unique_destination_ports_5m=1,
            failed_auth_attempts_5m=12,
            dns_entropy=3.2,
            scenario="safe-authentication-abuse-signal",
        ),
        NetworkEvent(
            source="192.0.2.66",
            destination="198.51.100.53",
            protocol="DNS",
            destination_port=53,
            bytes_out=88_000,
            flow_count_5m=34,
            unique_destination_ports_5m=1,
            failed_auth_attempts_5m=0,
            dns_entropy=6.8,
            scenario="safe-dns-exfiltration-signal",
        ),
    ]
