import { useNavigate } from "react-router-dom";
import Sparkline from "./Sparkline";
import AlertBadge from "./AlertBadge";

export default function SubProcessCard({ subprocess, history, alerts }) {
  const navigate = useNavigate();
  const recentHistory = history ? history.slice(-30) : [];
  const alertTypes = [...new Set((alerts || []).map((a) => a.type))];

  return (
    <div className="card subprocess-card" onClick={() => navigate(`/subprocess/${subprocess.id}`)}>
      <div className="subprocess-card-top">
        <h3>{subprocess.name}</h3>
        {alertTypes.length === 0 ? (
          <span className="badge badge-success">On track</span>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 4, alignItems: "flex-end" }}>
            {alertTypes.map((t) => (
              <AlertBadge key={t} type={t} />
            ))}
          </div>
        )}
      </div>

      {recentHistory.length > 0 && <Sparkline data={recentHistory} />}

      <div className="subprocess-meta">
        <span>
          CPD <b>{subprocess.cpd}</b>
        </span>
        <span>
          Target FTE <b>{subprocess.target_fte_count}</b>
        </span>
        <span>
          Capacity <b>{subprocess.fte_capacity}</b>/day
        </span>
      </div>
    </div>
  );
}
