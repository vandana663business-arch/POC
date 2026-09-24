import { useEffect, useState } from "react";
import { listSubProcesses, getHistory, getAlerts } from "../api/client";
import SubProcessCard from "../components/SubProcessCard";

export default function Dashboard() {
  const [subprocesses, setSubProcesses] = useState(null);
  const [historyById, setHistoryById] = useState({});
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const sps = await listSubProcesses();
        setSubProcesses(sps);

        const [histories, allAlerts] = await Promise.all([
          Promise.all(sps.map((sp) => getHistory(sp.id))),
          getAlerts(),
        ]);
        const map = {};
        sps.forEach((sp, i) => {
          map[sp.id] = histories[i];
        });
        setHistoryById(map);
        setAlerts(allAlerts);
      } catch (e) {
        setError(e.message);
      }
    }
    load();
  }, []);

  if (error) return <div className="empty-state">Failed to load: {error}</div>;
  if (!subprocesses) return <div className="loading">Loading Intake sub-processes...</div>;

  const shortfallCount = new Set(alerts.filter((a) => a.type === "capacity_shortfall").map((a) => a.subprocess_id)).size;
  const hiringCount = new Set(alerts.filter((a) => a.type === "hiring_lead_time").map((a) => a.subprocess_id)).size;
  const onTrackCount = subprocesses.length - new Set(alerts.map((a) => a.subprocess_id)).size;

  return (
    <div>
      <div className="page-header">
        <h1>Intake Overview</h1>
        <p>10 sub-processes &middot; 8-week forecast horizon &middot; Holt-Winters model</p>
      </div>

      <div className="stat-row">
        <div className="card stat-tile">
          <div className="stat-label">Sub-processes on track</div>
          <div className="stat-value" style={{ color: "var(--success)" }}>{onTrackCount}</div>
        </div>
        <div className="card stat-tile">
          <div className="stat-label">Capacity shortfall risk</div>
          <div className="stat-value" style={{ color: "var(--danger)" }}>{shortfallCount}</div>
        </div>
        <div className="card stat-tile">
          <div className="stat-label">Hiring lead-time alerts</div>
          <div className="stat-value" style={{ color: "var(--warning)" }}>{hiringCount}</div>
        </div>
        <div className="card stat-tile">
          <div className="stat-label">Total active alerts</div>
          <div className="stat-value">{alerts.length}</div>
        </div>
      </div>

      <div className="card-grid">
        {subprocesses.map((sp) => (
          <SubProcessCard
            key={sp.id}
            subprocess={sp}
            history={historyById[sp.id]}
            alerts={alerts.filter((a) => a.subprocess_id === sp.id)}
          />
        ))}
      </div>
    </div>
  );
}
