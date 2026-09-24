import {
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

export default function ForecastChart({ history, forecast, fteCapacity }) {
  const recentHistory = history.slice(-30).map((h) => ({
    date: h.date,
    actual: h.receipts,
  }));

  const forecastRows = forecast.forecast_dates.map((date, i) => ({
    date,
    holt_winters: forecast.holt_winters.forecast[i],
    baseline: forecast.rolling_average_baseline[i],
    band: [forecast.holt_winters.lower[i], forecast.holt_winters.upper[i]],
  }));

  const data = [...recentHistory, ...forecastRows];

  return (
    <ResponsiveContainer width="100%" height={320}>
      <ComposedChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#eceef4" />
        <XAxis dataKey="date" tick={{ fontSize: 11 }} minTickGap={30} />
        <YAxis tick={{ fontSize: 11 }} />
        <Tooltip />
        <ReferenceLine y={fteCapacity} stroke="#d64545" strokeDasharray="4 4" label={{ value: "Capacity", position: "insideTopRight", fontSize: 11, fill: "#d64545" }} />
        <Area dataKey="band" stroke="none" fill="#4f5fe0" fillOpacity={0.08} isAnimationActive={false} />
        <Line type="monotone" dataKey="actual" name="Actual" stroke="#1c2333" strokeWidth={2} dot={false} isAnimationActive={false} />
        <Line type="monotone" dataKey="holt_winters" name="Holt-Winters forecast" stroke="#4f5fe0" strokeWidth={2} dot={false} isAnimationActive={false} />
        <Line type="monotone" dataKey="baseline" name="Rolling-avg baseline" stroke="#c9820a" strokeWidth={1.5} strokeDasharray="5 3" dot={false} isAnimationActive={false} />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
