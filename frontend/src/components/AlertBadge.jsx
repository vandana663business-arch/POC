const LABELS = {
  capacity_shortfall: "Capacity shortfall",
  hiring_lead_time: "Hiring lead-time",
};

const CLASS_BY_TYPE = {
  capacity_shortfall: "badge-danger",
  hiring_lead_time: "badge-warning",
};

export default function AlertBadge({ type }) {
  const cls = CLASS_BY_TYPE[type] || "badge-neutral";
  const label = LABELS[type] || type;
  return <span className={`badge ${cls}`}>{label}</span>;
}
