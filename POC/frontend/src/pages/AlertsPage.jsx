import { useEffect, useState } from "react";
import { getAlerts } from "../api/client";
import AlertRow from "../components/AlertRow";

const FILTERS = [
  { key: "all", label: "All" },
  { key: "capacity_shortfall", label: "Capacity shortfall" },
  { key: "hiring_lead_time", label: "Hiring lead-time" },
];

export default function AlertsPage() {
  const [alerts, setAlerts] = useState(null);
  const [filter, setFilter] = useState("all");
  const [error, setError] = useState(null);

  useEffect(() => {
    getAlerts().then(setAlerts).catch((e) => setError(e.message));
  }, []);

  if (error) return <div className="empty-state">Failed to load alerts: {error}</div>;
  if (!alerts) return <div className="loading">Loading alerts...</div>;

  const filtered = filter === "all" ? alerts : alerts.filter((a) => a.type === filter);

  return (
    <div>
      <div className="page-header">
        <h1>Alerts</h1>
        <p>Capacity shortfall and hiring lead-time notifications across all Intake sub-processes.</p>
      </div>

      <div className="filter-bar">
        {FILTERS.map((f) => (
          <button
            key={f.key}
            className={`filter-chip${filter === f.key ? " active" : ""}`}
            onClick={() => setFilter(f.key)}
          >
            {f.label}
          </button>
        ))}
      </div>

      {filtered.length === 0 ? (
        <div className="empty-state">No alerts of this type right now.</div>
      ) : (
        <div className="alert-list">
          {filtered.map((a, i) => (
            <AlertRow key={i} alert={a} />
          ))}
        </div>
      )}
    </div>
  );
}
