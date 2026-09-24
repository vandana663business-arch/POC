export default function WhatIfPanel({ growthPct, targetFte, defaultFte, onChange, onReset }) {
  return (
    <div className="card whatif-panel">
      <h3 style={{ marginTop: 0, fontSize: "0.95rem" }}>What-if scenario</h3>

      <label>
        Volume growth: <span className="whatif-value">{growthPct > 0 ? "+" : ""}{growthPct}%</span>
      </label>
      <input
        type="range"
        min={-30}
        max={60}
        step={5}
        value={growthPct}
        onChange={(e) => onChange({ growthPct: Number(e.target.value), targetFte })}
      />

      <label>Target planned FTE</label>
      <input
        type="number"
        min={0}
        step={1}
        value={targetFte}
        onChange={(e) => onChange({ growthPct, targetFte: Number(e.target.value) })}
      />

      <button className="whatif-reset" onClick={onReset}>
        Reset to current staffing ({defaultFte} FTE)
      </button>
    </div>
  );
}
