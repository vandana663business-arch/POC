import { useEffect, useState, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { getSubProcess, getHistory, getAnalysis, runScenario } from "../api/client";
import ForecastChart from "../components/ForecastChart";
import StaffingChart from "../components/StaffingChart";
import AlertRow from "../components/AlertRow";
import WhatIfPanel from "../components/WhatIfPanel";

export default function SubProcessDetail() {
  const { id } = useParams();
  const subprocessId = Number(id);

  const [subprocess, setSubProcess] = useState(null);
  const [history, setHistory] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [defaultFte, setDefaultFte] = useState(null);
  const [growthPct, setGrowthPct] = useState(0);
  const [targetFte, setTargetFte] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    setSubProcess(null);
    setHistory(null);
    setAnalysis(null);
    setError(null);
    setDefaultFte(null);
    setTargetFte(null);
    setGrowthPct(0);

    Promise.all([getSubProcess(subprocessId), getHistory(subprocessId), getAnalysis(subprocessId)])
      .then(([sp, hist, base]) => {
        setSubProcess(sp);
        setHistory(hist);
        setAnalysis(base);
        setDefaultFte(base.staffing.planned_fte);
        setTargetFte(base.staffing.planned_fte);
        setGrowthPct(0);
      })
      .catch((e) => setError(e.message));
  }, [subprocessId]);

  const applyScenario = useCallback(
    (nextGrowthPct, nextTargetFte) => {
      runScenario({ subprocessId, growthPct: nextGrowthPct, targetFte: nextTargetFte })
        .then(setAnalysis)
        .catch((e) => setError(e.message));
    },
    [subprocessId]
  );

  useEffect(() => {
    if (targetFte === null) return;
    if (growthPct === 0 && targetFte === defaultFte) return; // matches the already-loaded base analysis
    const t = setTimeout(() => applyScenario(growthPct, targetFte), 250);
    return () => clearTimeout(t);
  }, [growthPct, targetFte, defaultFte, applyScenario]);

  if (error) return <div className="empty-state">Failed to load: {error}</div>;
  if (!subprocess || !history || !analysis) return <div className="loading">Loading...</div>;

  const trailing30 = history.slice(-30);
  const attainment =
    trailing30.reduce((s, h) => s + h.completed, 0) / Math.max(1, trailing30.reduce((s, h) => s + h.receipts, 0));

  return (
    <div>
      <Link to="/" className="back-link">
        &larr; Back to overview
      </Link>

      <div className="page-header">
        <h1>{subprocess.name}</h1>
        <p>
          CPD {subprocess.cpd} &middot; CPH {subprocess.cph} &middot; Benchmark capacity {subprocess.fte_capacity} cases/day at {subprocess.target_fte_count} FTE
        </p>
      </div>

      <div className="stat-row">
        <div className="card stat-tile">
          <div className="stat-label">Current planned FTE</div>
          <div className="stat-value">{defaultFte}</div>
        </div>
        <div className="card stat-tile">
          <div className="stat-label">30-day attainment</div>
          <div className="stat-value">{(attainment * 100).toFixed(0)}%</div>
        </div>
        <div className="card stat-tile">
          <div className="stat-label">Active alerts</div>
          <div className="stat-value" style={{ color: analysis.alerts.length ? "var(--danger)" : "var(--success)" }}>
            {analysis.alerts.length}
          </div>
        </div>
      </div>

      <div className="two-col">
        <div>
          <div className="card">
            <div className="legend-row">
              <span><span className="legend-dot" style={{ background: "#1c2333" }} />Actual</span>
              <span><span className="legend-dot" style={{ background: "#4f5fe0" }} />Holt-Winters forecast</span>
              <span><span className="legend-dot" style={{ background: "#c9820a" }} />Rolling-avg baseline</span>
              <span><span className="legend-dot" style={{ background: "#d64545" }} />Capacity (at current scenario)</span>
            </div>
            <ForecastChart history={history} forecast={analysis.forecast} fteCapacity={subprocess.cpd * (targetFte ?? defaultFte)} />
          </div>

          <div className="section-title">Weekly staffing requirement vs. planned</div>
          <div className="card">
            <StaffingChart weekly={analysis.staffing.weekly} />
          </div>

          <div className="section-title">Alerts for this sub-process</div>
          {analysis.alerts.length === 0 ? (
            <div className="empty-state">No alerts under the current scenario.</div>
          ) : (
            <div className="alert-list">
              {analysis.alerts.map((a, i) => (
                <AlertRow key={i} alert={{ ...a, subprocess_id: subprocessId }} />
              ))}
            </div>
          )}
        </div>

        <WhatIfPanel
          growthPct={growthPct}
          targetFte={targetFte ?? defaultFte}
          defaultFte={defaultFte}
          onChange={({ growthPct: g, targetFte: t }) => {
            setGrowthPct(g);
            setTargetFte(t);
          }}
          onReset={() => {
            setGrowthPct(0);
            setTargetFte(defaultFte);
          }}
        />
      </div>
    </div>
  );
}
