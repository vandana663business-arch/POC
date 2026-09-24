import { ComposedChart, Bar, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";

export default function StaffingChart({ weekly }) {
  const data = weekly.map((w) => ({
    week: w.week_start,
    required_fte: w.avg_required_fte,
    planned_fte: w.planned_fte,
    gap: w.avg_fte_gap,
  }));

  return (
    <ResponsiveContainer width="100%" height={280}>
      <ComposedChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#eceef4" />
        <XAxis dataKey="week" tick={{ fontSize: 11 }} />
        <YAxis tick={{ fontSize: 11 }} />
        <Tooltip />
        <Legend wrapperStyle={{ fontSize: 12 }} />
        <Bar dataKey="gap" name="FTE gap (required - planned)" fill="#d64545" radius={[4, 4, 0, 0]} />
        <Line type="monotone" dataKey="required_fte" name="Required FTE" stroke="#4f5fe0" strokeWidth={2} dot={{ r: 3 }} />
        <Line type="monotone" dataKey="planned_fte" name="Planned FTE" stroke="#1f9d55" strokeWidth={2} strokeDasharray="5 3" dot={{ r: 3 }} />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
