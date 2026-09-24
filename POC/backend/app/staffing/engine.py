"""Staffing calculation: converts a forecast volume series into a required
headcount series (via CPD) and compares it against currently planned
headcount to find gaps.

Daily numbers are noisy (day-of-week swings), so we also produce a
week-by-week aggregated view, since staffing decisions are naturally made
per week, not per day. The alert engine (see ../alerts/engine.py) consumes
the weekly view.
"""

def required_fte_series(forecast_values: list[float], cpd: float) -> list[float]:
    if cpd <= 0:
        raise ValueError("cpd must be positive")
    return [v / cpd for v in forecast_values]


def apply_growth_scenario(forecast_values: list[float], growth_pct: float) -> list[float]:
    """What-if lever: uniformly scale the forecast by a growth percentage
    (e.g. growth_pct=10 means +10% volume across the whole horizon)."""
    factor = 1 + (growth_pct / 100.0)
    return [v * factor for v in forecast_values]


def daily_staffing(forecast_dates: list[str], forecast_values: list[float], cpd: float, planned_fte: float) -> list[dict]:
    required = required_fte_series(forecast_values, cpd)
    return [
        {
            "date": d,
            "forecast_volume": round(v, 1),
            "required_fte": round(r, 2),
            "planned_fte": planned_fte,
            "fte_gap": round(r - planned_fte, 2),
        }
        for d, v, r in zip(forecast_dates, forecast_values, required)
    ]


def weekly_staffing(daily_rows: list[dict]) -> list[dict]:
    """Groups daily staffing rows into consecutive 7-day buckets starting
    from the first forecast date, averaging volume/required_fte/gap per week.
    """
    weeks = []
    for i in range(0, len(daily_rows), 7):
        chunk = daily_rows[i : i + 7]
        if not chunk:
            continue
        n = len(chunk)
        avg_volume = sum(r["forecast_volume"] for r in chunk) / n
        avg_required = sum(r["required_fte"] for r in chunk) / n
        avg_gap = sum(r["fte_gap"] for r in chunk) / n
        weeks.append(
            {
                "week_start": chunk[0]["date"],
                "week_end": chunk[-1]["date"],
                "avg_forecast_volume": round(avg_volume, 1),
                "avg_required_fte": round(avg_required, 2),
                "planned_fte": chunk[0]["planned_fte"],
                "avg_fte_gap": round(avg_gap, 2),
            }
        )
    return weeks


def compute_staffing(
    forecast_dates: list[str],
    forecast_values: list[float],
    cpd: float,
    planned_fte: float,
    growth_pct: float = 0.0,
    scenario_target_fte: float | None = None,
) -> dict:
    """Full staffing computation, with optional what-if overrides.

    growth_pct: uniformly scales forecast volume (e.g. +10 for a 10% growth scenario).
    scenario_target_fte: if provided, overrides planned_fte for the gap calculation.
    """
    adjusted_forecast = apply_growth_scenario(forecast_values, growth_pct) if growth_pct else list(forecast_values)
    effective_planned_fte = scenario_target_fte if scenario_target_fte is not None else planned_fte

    daily = daily_staffing(forecast_dates, adjusted_forecast, cpd, effective_planned_fte)
    weekly = weekly_staffing(daily)

    return {
        "daily": daily,
        "weekly": weekly,
        "planned_fte": effective_planned_fte,
        "cpd": cpd,
    }
