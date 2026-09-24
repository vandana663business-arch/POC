import pandas as pd
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.config import FORECAST_HORIZON_DAYS
from app.data.models import SubProcess, DailyVolume, DailyFTE, DailyProd
from app.forecasting.engine import build_forecast
from app.staffing.engine import compute_staffing
from app.alerts.engine import build_alerts


def get_subprocess_or_404(db: Session, subprocess_id: int) -> SubProcess:
    sp = db.query(SubProcess).filter(SubProcess.id == subprocess_id).first()
    if sp is None:
        raise HTTPException(status_code=404, detail="Sub-process not found")
    return sp


def subprocess_summary(sp: SubProcess) -> dict:
    return {
        "id": sp.id,
        "name": sp.name,
        "cpd": sp.cpd,
        "cph": sp.cph,
        "target_fte_count": sp.target_fte_count,
        "fte_capacity": sp.fte_capacity,
    }


def volume_history_df(db: Session, subprocess_id: int) -> pd.DataFrame:
    rows = (
        db.query(DailyVolume)
        .filter(DailyVolume.subprocess_id == subprocess_id)
        .order_by(DailyVolume.date)
        .all()
    )
    if not rows:
        raise HTTPException(status_code=404, detail="No history found for this sub-process")
    return pd.DataFrame([{"date": r.date, "receipts": r.receipts} for r in rows])


def latest_planned_fte(db: Session, subprocess_id: int) -> float:
    row = (
        db.query(DailyFTE)
        .filter(DailyFTE.subprocess_id == subprocess_id)
        .order_by(DailyFTE.date.desc())
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="No FTE history found for this sub-process")
    return row.planned_fte


def full_history(db: Session, subprocess_id: int) -> list[dict]:
    volumes = {r.date: r.receipts for r in db.query(DailyVolume).filter(DailyVolume.subprocess_id == subprocess_id)}
    fte = {r.date: (r.actual_fte, r.planned_fte) for r in db.query(DailyFTE).filter(DailyFTE.subprocess_id == subprocess_id)}
    prod = {r.date: r.completed for r in db.query(DailyProd).filter(DailyProd.subprocess_id == subprocess_id)}

    rows = []
    for d in sorted(volumes.keys()):
        actual_fte, planned_fte = fte.get(d, (None, None))
        rows.append(
            {
                "date": d.isoformat(),
                "receipts": volumes.get(d),
                "completed": prod.get(d),
                "actual_fte": actual_fte,
                "planned_fte": planned_fte,
            }
        )
    return rows


def analyze_subprocess(
    db: Session,
    subprocess_id: int,
    horizon_days: int = FORECAST_HORIZON_DAYS,
    growth_pct: float = 0.0,
    target_fte: float | None = None,
) -> dict:
    sp = get_subprocess_or_404(db, subprocess_id)
    history_df = volume_history_df(db, subprocess_id)
    planned_fte = latest_planned_fte(db, subprocess_id)

    forecast = build_forecast(history_df, horizon_days)
    staffing = compute_staffing(
        forecast["forecast_dates"],
        forecast["holt_winters"]["forecast"],
        sp.cpd,
        planned_fte,
        growth_pct=growth_pct,
        scenario_target_fte=target_fte,
    )
    # Capacity for alerting purposes reflects whatever staffing level is
    # actually in effect (the latest planned FTE, or a what-if override) --
    # not the static benchmark -- so hiring more staff in a scenario visibly
    # resolves the capacity-shortfall alert.
    effective_capacity = sp.cpd * staffing["planned_fte"]
    alerts = build_alerts(sp.name, effective_capacity, sp.cph, staffing["weekly"])

    return {
        "subprocess": subprocess_summary(sp),
        "forecast": forecast,
        "staffing": staffing,
        "alerts": alerts,
    }


def all_alerts(db: Session, horizon_days: int = FORECAST_HORIZON_DAYS) -> list[dict]:
    alerts = []
    for sp in db.query(SubProcess).all():
        result = analyze_subprocess(db, sp.id, horizon_days=horizon_days)
        for a in result["alerts"]:
            a_with_id = {"subprocess_id": sp.id, **a}
            alerts.append(a_with_id)
    return alerts
