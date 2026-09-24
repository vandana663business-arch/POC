const BASE_URL = "http://127.0.0.1:8000";

async function request(path, options) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${body}`);
  }
  return res.json();
}

export function listSubProcesses() {
  return request("/subprocesses");
}

export function getSubProcess(id) {
  return request(`/subprocesses/${id}`);
}

export function getHistory(id) {
  return request(`/subprocesses/${id}/history`);
}

export function getAnalysis(id, horizon = 56) {
  return request(`/subprocesses/${id}/analysis?horizon=${horizon}`);
}

export function getAlerts() {
  return request("/alerts");
}

export function runScenario({ subprocessId, growthPct = 0, targetFte = null, horizonDays = 56 }) {
  return request("/scenario", {
    method: "POST",
    body: JSON.stringify({
      subprocess_id: subprocessId,
      growth_pct: growthPct,
      target_fte: targetFte,
      horizon_days: horizonDays,
    }),
  });
}
