CREATE TABLE IF NOT EXISTS security_alerts (
  alert_id UUID PRIMARY KEY,
  event_id UUID NOT NULL,
  classification TEXT NOT NULL,
  score DOUBLE PRECISION NOT NULL,
  severity TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_security_alerts_created_at ON security_alerts (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_security_alerts_status ON security_alerts (status);
