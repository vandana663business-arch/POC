import { LineChart, Line, ResponsiveContainer, YAxis } from "recharts";

export default function Sparkline({ data, dataKey = "receipts", color = "#4f5fe0" }) {
  return (
    <div style={{ width: "100%", height: 42 }}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <YAxis hide domain={["dataMin", "dataMax"]} />
          <Line type="monotone" dataKey={dataKey} stroke={color} strokeWidth={2} dot={false} isAnimationActive={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
