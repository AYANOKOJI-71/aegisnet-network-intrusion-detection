# Local Validation Record

The deterministic AegisNet review path was exercised through the React security operations dashboard with the FastAPI service running locally.

| Check | Observed result |
|---|---|
| Initial state | 0 metadata observations and 0 alerts |
| Safe demo action | Completed without packet capture, scanning, traffic generation, or external network requests |
| Synthetic metadata processed | 4 observations |
| Explainable alerts created | 3 critical analyst signals |
| Example selected evidence | `Dns Exfiltration Signal` at score `58.29`, with connection-burst, outbound-volume, and high-entropy-DNS explanations |
| Lifecycle controls | Dashboard rendered acknowledgement and resolution controls for the selected alert |

All source and destination values shown in the demonstration are documentation-range addresses. The result validates user-interface integration and detection explanation only; it does not claim a real-world attack was observed or confirmed.
