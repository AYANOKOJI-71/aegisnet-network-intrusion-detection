from __future__ import annotations

from pathlib import Path

from scapy.all import DNS, IP, TCP, UDP, Packet, rdpcap

from aegisnet.models import NetworkEvent


def parse_authorized_fixture_pcap(path: Path, maximum_packets: int = 1_000) -> list[NetworkEvent]:
    """Parse a user-authorized local fixture PCAP; no live capture or packet emission is supported."""

    if not path.is_file() or path.suffix.lower() not in {".pcap", ".pcapng"}:
        raise ValueError("Only an existing local .pcap or .pcapng fixture may be parsed.")
    packets = rdpcap(str(path), count=maximum_packets)
    normalized: list[NetworkEvent] = []
    for packet in packets:
        if IP not in packet:
            continue
        normalized.append(_normalize(packet))
    return normalized


def _normalize(packet: Packet) -> NetworkEvent:
    ip_layer = packet[IP]
    protocol = "TCP" if TCP in packet else "UDP"
    destination_port = int(packet[TCP].dport) if TCP in packet else int(packet[UDP].dport) if UDP in packet else 0
    if DNS in packet:
        protocol = "DNS"
    return NetworkEvent(
        source=ip_layer.src,
        destination=ip_layer.dst,
        protocol=protocol,
        destination_port=destination_port,
        bytes_out=len(packet),
        flow_count_5m=1,
        unique_destination_ports_5m=1,
        failed_auth_attempts_5m=0,
        dns_entropy=0.0,
        scenario="authorized-fixture-pcap",
        source_kind="authorized-fixture",
    )
