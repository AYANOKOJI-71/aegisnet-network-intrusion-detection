import type { Alert, AlertStatus, Detection, Overview } from "./types";

const apiBase = import.meta.env.VITE_AEGISNET_API_URL ?? "";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, options);
  if (!response.ok) throw new Error(`Security API returned ${response.status}`);
  return response.json() as Promise<T>;
}

export const aegisApi = {
  overview: () => request<Overview>("/api/overview"),
  events: () => request<Detection[]>("/api/events"),
  alerts: () => request<Alert[]>("/api/alerts"),
  runSafeDemo: () => request<Alert[]>("/api/demo/seed", { method: "POST" }),
  updateAlert: (alertId: string, status: AlertStatus) =>
    request<Alert>(`/api/alerts/${alertId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status })
    })
};
