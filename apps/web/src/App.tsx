import { useCallback, useEffect, useState } from "react";
import {
  Activity,
  AlertTriangle,
  CheckCircle2,
  Crosshair,
  Database,
  Network,
  Radar,
  RefreshCw,
  ShieldCheck,
  ShieldOff,
  Terminal,
  Waves
} from "lucide-react";
import { aegisApi } from "./api";
import { formatBytes, formatTimestamp, titleCase } from "./format";
import type { Alert, AlertStatus, Detection, Overview, Severity } from "./types";

const emptyOverview: Overview = {
  eventsProcessed: 0,
  alerts: 0,
  openAlerts: 0,
  severity: {},
  mode: "deterministic-safe",
  capturePolicy: "synthetic-or-authorized-fixture-only"
};

function App() {
  const [overview, setOverview] = useState<Overview>(emptyOverview);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [events, setEvents] = useState<Detection[]>([]);
  const [selected, setSelected] = useState<Alert | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    try {
      const [nextOverview, nextAlerts, nextEvents] = await Promise.all([
        aegisApi.overview(),
        aegisApi.alerts(),
        aegisApi.events()
      ]);
      setOverview(nextOverview);
      setAlerts(nextAlerts);
      setEvents(nextEvents);
      setSelected((current) => nextAlerts.find((alert) => alert.alert_id === current?.alert_id) ?? nextAlerts[0] ?? null);
      setNotice(null);
    } catch {
      setNotice("The safe analysis API is unavailable. Start the local FastAPI service to load synthetic telemetry.");
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const runDemo = async () => {
    setLoading(true);
    try {
      await aegisApi.runSafeDemo();
      await load();
      setNotice("Safe synthetic scenarios evaluated. No packet capture, scanning, or external network traffic occurred.");
    } catch {
      setNotice("The safe synthetic demo could not be evaluated because the API is unavailable.");
    } finally {
      window.setTimeout(() => setLoading(false), 100);
    }
  };

  const updateStatus = async (alert: Alert, status: AlertStatus) => {
    try {
      await aegisApi.updateAlert(alert.alert_id, status);
      await load();
      setNotice(`Alert status changed to ${status}. This workflow always requires a human action.`);
    } catch {
      setNotice("The alert status could not be updated.");
    }
  };

  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="brand"><ShieldCheck size={25} /><span>Aegis<span>Net</span></span></div>
        <p className="eyebrow">SECURITY OPERATIONS</p>
        <nav>
          <a href="#command"><Radar size={16} /> Detection command</a>
          <a href="#alerts"><AlertTriangle size={16} /> Alert queue</a>
          <a href="#evidence"><Terminal size={16} /> Evidence stream</a>
          <a href="#boundary"><ShieldCheck size={16} /> Safe boundaries</a>
        </nav>
        <div className="policy-card">
          <ShieldOff size={19} />
          <strong>Safe showcase mode</strong>
          <span>Only synthetic metadata or authorized local fixture PCAPs are supported.</span>
        </div>
      </aside>

      <section className="workspace" id="command">
        <header className="topbar">
          <div><p className="eyebrow">NETWORK INTRUSION DETECTION</p><h1>Detection command center</h1></div>
          <div className="controls">
            <button className="icon-button" onClick={() => void load()} aria-label="Refresh dashboard"><RefreshCw size={18} /></button>
            <button className="primary-button" disabled={loading} onClick={() => void runDemo()}><Crosshair size={17} /> {loading ? "Evaluating…" : "Run safe demo"}</button>
          </div>
        </header>

        {notice && <div className="notice"><Activity size={18} /> {notice}</div>}

        <section className="stat-grid" aria-label="Detection statistics">
          <Stat icon={<Waves />} label="Telemetry analyzed" value={overview.eventsProcessed} helper="metadata-only observations" tone="cyan" />
          <Stat icon={<AlertTriangle />} label="Alerts created" value={overview.alerts} helper="explainable anomaly signals" tone="amber" />
          <Stat icon={<Radar />} label="Open investigations" value={overview.openAlerts} helper="requires analyst triage" tone="red" />
          <Stat icon={<Database />} label="Analysis mode" value={overview.mode === "deterministic-safe" ? "SAFE" : "POSTGRES"} helper="switchable persistence" tone="violet" />
        </section>

        <div className="main-grid">
          <section className="panel posture-panel" id="boundary">
            <div className="panel-header"><div><p className="eyebrow">CAPTURE BOUNDARY</p><h2>Defensive-only analysis path</h2></div><span className="mode-pill"><CheckCircle2 size={14} /> AUTHORIZED</span></div>
            <div className="chain">
              <ChainStep number="01" name="Synthetic metadata" service="Scenario fixture" />
              <ChainStep number="02" name="Feature scoring" service="Explainable z-score" />
              <ChainStep number="03" name="Human review" service="Alert lifecycle" />
            </div>
            <p className="panel-note">Live capture, traffic generation, scanning, and arbitrary file-path ingestion are intentionally outside this application. The optional Scapy adapter reads only explicitly authorized local fixture PCAPs.</p>
          </section>

          <section className="panel severity-panel">
            <div className="panel-header"><div><p className="eyebrow">RISK DISTRIBUTION</p><h2>Alert severity</h2></div><Network size={20} /></div>
            <div className="severity-list">
              {(["critical", "high", "medium", "info"] as Severity[]).map((severity) => (
                <div className="severity-row" key={severity}><span className={`dot ${severity}`} /><span>{severity}</span><b>{overview.severity[severity] ?? 0}</b></div>
              ))}
            </div>
          </section>
        </div>

        <section className="content-grid" id="alerts">
          <section className="panel alert-panel">
            <div className="panel-header"><div><p className="eyebrow">ALERT QUEUE</p><h2>Human triage required</h2></div><span className="count">{alerts.length} total</span></div>
            {alerts.length === 0 ? <EmptyQueue /> : <div className="alert-list">{alerts.map((alert) => <AlertRow key={alert.alert_id} alert={alert} selected={selected?.alert_id === alert.alert_id} onSelect={() => setSelected(alert)} />)}</div>}
          </section>

          <section className="panel evidence-panel" id="evidence">
            <div className="panel-header"><div><p className="eyebrow">EXPLAINABLE EVIDENCE</p><h2>{selected ? titleCase(selected.detection.classification) : "Awaiting selection"}</h2></div><span className="live-pill"><span /> LIVE</span></div>
            {selected ? <Evidence alert={selected} onStatus={updateStatus} /> : <p className="empty-text">Run the safe demo to review transparent anomaly evidence.</p>}
          </section>
        </section>

        <section className="panel event-panel">
          <div className="panel-header"><div><p className="eyebrow">NORMALIZED EVENT STREAM</p><h2>Latest metadata evidence</h2></div><span className="count">{events.length} observed</span></div>
          {events.length === 0 ? <p className="empty-text">No synthetic telemetry has been evaluated.</p> : <div className="event-table"><div className="table-head"><span>Scenario</span><span>Flow</span><span>Signal</span><span>Score</span></div>{events.map((detection) => <div className="table-row" key={detection.event.event_id}><span><b>{titleCase(detection.event.scenario)}</b><small>{detection.event.source} → {detection.event.destination}</small></span><span>{detection.event.protocol} · {formatBytes(detection.event.bytes_out)}</span><span><span className={`severity-tag ${detection.severity}`}>{detection.severity}</span></span><span className="score">{detection.score.toFixed(2)}</span></div>)}</div>}
        </section>
      </section>
    </main>
  );
}

function Stat({ icon, label, value, helper, tone }: { icon: React.ReactNode; label: string; value: string | number; helper: string; tone: string }) {
  return <article className={`stat-card ${tone}`}><div className="stat-icon">{icon}</div><p>{label}</p><strong>{value}</strong><span>{helper}</span></article>;
}

function ChainStep({ number, name, service }: { number: string; name: string; service: string }) {
  return <div className="chain-step"><span>{number}</span><div><b>{name}</b><small>{service}</small></div></div>;
}

function AlertRow({ alert, selected, onSelect }: { alert: Alert; selected: boolean; onSelect: () => void }) {
  return <button className={`alert-row ${selected ? "selected" : ""}`} onClick={onSelect}><span className={`severity-marker ${alert.detection.severity}`} /><span className="alert-copy"><b>{titleCase(alert.detection.classification)}</b><small>{alert.detection.event.source} · score {alert.detection.score.toFixed(2)}</small></span><span className={`status ${alert.status}`}>{alert.status}</span></button>;
}

function Evidence({ alert, onStatus }: { alert: Alert; onStatus: (alert: Alert, status: AlertStatus) => Promise<void> }) {
  const event = alert.detection.event;
  return <div className="evidence"><div className="evidence-summary"><span className={`severity-tag ${alert.detection.severity}`}>{alert.detection.severity}</span><strong>Score {alert.detection.score.toFixed(2)}</strong><span>{formatTimestamp(event.observed_at)}</span></div><div className="feature-grid"><Feature label="Source / destination" value={`${event.source} → ${event.destination}`} /><Feature label="Protocol / port" value={`${event.protocol} · ${event.destination_port || "varied"}`} /><Feature label="Outbound data" value={formatBytes(event.bytes_out)} /><Feature label="Flow count (5m)" value={event.flow_count_5m} /><Feature label="Unique destination ports" value={event.unique_destination_ports_5m} /><Feature label="Failed auth attempts" value={event.failed_auth_attempts_5m} /></div><div className="explanations"><p className="eyebrow">MODEL EXPLANATIONS</p>{alert.detection.explanation.map((line) => <p key={line}><Activity size={15} /> {line}</p>)}</div><div className="action-row">{alert.status === "open" && <button className="secondary-button" onClick={() => void onStatus(alert, "acknowledged")}>Acknowledge</button>}{alert.status !== "resolved" && <button className="resolve-button" onClick={() => void onStatus(alert, "resolved")}>Resolve signal</button>}</div></div>;
}

function Feature({ label, value }: { label: string; value: string | number }) {
  return <div className="feature"><span>{label}</span><b>{value}</b></div>;
}

function EmptyQueue() {
  return <div className="empty-queue"><ShieldCheck size={28} /><strong>No alerts yet</strong><span>Run the safe synthetic demo to populate explainable analyst signals.</span></div>;
}

export default App;
