import { useNavigate } from "react-router-dom";
import AlertBadge from "./AlertBadge";

export default function AlertRow({ alert }) {
  const navigate = useNavigate();
  const severityClass = alert.type === "capacity_shortfall" ? "severity-danger" : "severity-warning";

  return (
    <div className={`alert-row ${severityClass}`} onClick={() => navigate(`/intake/subprocess/${alert.subprocess_id}`)} style={{ cursor: "pointer" }}>
      <AlertBadge type={alert.type} />
      <div className="alert-row-body">
        <div className="alert-row-title">{alert.subprocess}</div>
        <div className="alert-row-message">{alert.message}</div>
      </div>
    </div>
  );
}
