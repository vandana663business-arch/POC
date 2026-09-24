"""Alert/notification rules engine.

Two alert types are in scope for this POC:
1. Capacity shortfall / overtime -- forecasted volume for a week exceeds the
   sub-process's staffed daily capacity (fte_capacity = cpd * planned_fte).
2. Hiring lead-time -- the staffing gap (required_fte - planned_fte) stays
   positive for several consecutive weeks, meaning it's a genuine sustained
   need rather than a one-week blip, so a "start recruiting by" date is
   computed by subtracting the training pipeline length from when the gap
   first becomes sustained.

Cross-skill/internal-movement alerts are explicitly out of scope for this POC.
"""

import math
from datetime import date, datetime, timedelta

from app.config import HOURLY_RATE_USD, SUSTAINED_GAP_WEEKS_THRESHOLD, TRAINING_LEAD_TIME_WEEKS


def _parse_date(d: str) -> date:
    return datetime.strptime(d, "%Y-%m-%d").date()


def capacity_shortfall_alerts(subprocess_name: str, fte_capacity: float, cph: float, weekly_staffing: list[dict]) -> list[dict]:
    alerts = []
    for week in weekly_staffing:
        volume = week["avg_forecast_volume"]
        if volume <= fte_capacity:
            continue

        overage = volume - fte_capacity
        overage_pct = round((overage / fte_capacity) * 100, 1)
        overtime_hours_per_day = round(overage / cph, 1) if cph else None
        estimated_daily_cost = round(overtime_hours_per_day * HOURLY_RATE_USD, 2) if overtime_hours_per_day else None

        alerts.append(
            {
                "type": "capacity_shortfall",
                "subprocess": subprocess_name,
                "week_start": week["week_start"],
                "week_end": week["week_end"],
                "forecast_volume": volume,
                "fte_capacity": fte_capacity,
                "overage_pct": overage_pct,
                "estimated_overtime_hours_per_day": overtime_hours_per_day,
                "estimated_daily_overtime_cost_usd": estimated_daily_cost,
                "cost_assumption": f"assumes ${HOURLY_RATE_USD:.0f}/hr rate card (placeholder)",
                "message": (
                    f"{subprocess_name}: forecasted volume for week of {week['week_start']} "
                    f"is {overage_pct}% over current staffed capacity -- expect backlog or "
                    f"~{overtime_hours_per_day} overtime hrs/day to keep up."
                ),
            }
        )
    return alerts


def hiring_leadtime_alerts(subprocess_name: str, weekly_staffing: list[dict]) -> list[dict]:
    n = len(weekly_staffing)
    threshold = SUSTAINED_GAP_WEEKS_THRESHOLD

    trigger_index = None
    for i in range(n - threshold + 1):
        window = weekly_staffing[i : i + threshold]
        if all(w["avg_fte_gap"] > 0 for w in window):
            trigger_index = i
            break

    if trigger_index is None:
        return []

    trigger_week = weekly_staffing[trigger_index]
    tail = weekly_staffing[trigger_index:]
    gap_now = trigger_week["avg_fte_gap"]
    gap_at_horizon_end = tail[-1]["avg_fte_gap"]
    additional_fte_needed = math.ceil(gap_now)

    trigger_date = _parse_date(trigger_week["week_start"])
    hire_by_date = trigger_date - timedelta(weeks=TRAINING_LEAD_TIME_WEEKS)
    today = date.today()
    urgency = "immediate" if hire_by_date <= today else "planned"

    return [
        {
            "type": "hiring_lead_time",
            "subprocess": subprocess_name,
            "gap_starts_week": trigger_week["week_start"],
            "additional_fte_needed_now": additional_fte_needed,
            "gap_at_end_of_forecast_horizon": round(gap_at_horizon_end, 2),
            "training_lead_time_weeks": TRAINING_LEAD_TIME_WEEKS,
            "hire_by_date": hire_by_date.isoformat(),
            "urgency": urgency,
            "message": (
                f"{subprocess_name}: forecast shows a sustained staffing gap starting "
                f"week of {trigger_week['week_start']} (~{additional_fte_needed} FTE short). "
                f"With a {TRAINING_LEAD_TIME_WEEKS}-week hire-to-productive pipeline, "
                f"recruiting should have started by {hire_by_date.isoformat()}"
                + (" -- that date has already passed." if urgency == "immediate" else ".")
            ),
        }
    ]


def build_alerts(subprocess_name: str, fte_capacity: float, cph: float, weekly_staffing: list[dict]) -> list[dict]:
    return capacity_shortfall_alerts(subprocess_name, fte_capacity, cph, weekly_staffing) + hiring_leadtime_alerts(
        subprocess_name, weekly_staffing
    )
