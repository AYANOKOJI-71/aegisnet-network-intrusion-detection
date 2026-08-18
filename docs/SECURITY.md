# Security Boundaries

> **AegisNet is an observability and analyst-training application. It is not a traffic-generation, scanning, interception, or prevention tool.**

| Control | Implementation |
|---|---|
| Live capture disabled | There is no `sniff()` call, raw-socket operation, interface selector, or packet-emission function. |
| Explicit fixture parsing | The Scapy adapter can parse only an existing local `.pcap` or `.pcapng` fixture explicitly supplied to local code. It is not exposed as an HTTP endpoint. |
| Synthetic first | The web button sends no network traffic; it evaluates fixed metadata records only. |
| Documentation IPs | Demo records use IETF documentation ranges, reducing ambiguity with deployed addresses.[1] |
| Human lifecycle | Alerts begin open and must be acknowledged or resolved by an analyst action. |
| Database credentials | Kubernetes manifest references a secret; no production credentials are committed. |
| Least exposure | The API exposes only overview, evidence, deterministic demo, controlled alert updates, health, and metrics routes. |

For real deployments, run sensor collection only with written authorization, use organization-approved retention and access controls, validate PCAP provenance, and treat model outputs as triage evidence rather than a final incident determination.

## References

[1] [RFC 5737: IPv4 Address Blocks Reserved for Documentation](https://datatracker.ietf.org/doc/html/rfc5737)
