export type Severity = "info" | "medium" | "high" | "critical";
export type AlertStatus = "open" | "acknowledged" | "resolved";

export interface NetworkEvent {
  event_id: string;
  observed_at: string;
  source: string;
  destination: string;
  protocol: "TCP" | "UDP" | "DNS" | "ICMP";
  destination_port: number;
  bytes_out: number;
  flow_count_5m: number;
  unique_destination_ports_5m: number;
  failed_auth_attempts_5m: number;
  dns_entropy: number;
  scenario: string;
  source_kind: "synthetic" | "authorized-fixture";
}

export interface Detection {
  event: NetworkEvent;
  score: number;
  severity: Severity;
  classification: string;
  explanation: string[];
}

export interface Alert {
  alert_id: string;
  detection: Detection;
  status: AlertStatus;
  created_at: string;
  updated_at: string;
}

export interface Overview {
  eventsProcessed: number;
  alerts: number;
  openAlerts: number;
  severity: Partial<Record<Severity, number>>;
  mode: string;
  capturePolicy: string;
}
