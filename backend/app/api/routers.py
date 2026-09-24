from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config import FORECAST_HORIZON_DAYS
from app.data.db import get_db
from app.data.models import SubProcess
from app.api.schemas import ScenarioRequest
from app.api import services

router = APIRouter()


@router.get("/subprocesses")
def list_subprocesses(db: Session = Depends(get_db)):
    return [services.subprocess_summary(sp) for sp in db.query(SubProcess).order_by(SubProcess.id).all()]


@router.get("/subprocesses/{subprocess_id}")
def get_subprocess(subprocess_id: int, db: Session = Depends(get_db)):
    sp = services.get_subprocess_or_404(db, subprocess_id)
    return services.subprocess_summary(sp)


@router.get("/subprocesses/{subprocess_id}/history")
def get_history(subprocess_id: int, db: Session = Depends(get_db)):
    services.get_subprocess_or_404(db, subprocess_id)
    return services.full_history(db, subprocess_id)


@router.get("/subprocesses/{subprocess_id}/analysis")
def get_analysis(
    subprocess_id: int,
    horizon: int = Query(FORECAST_HORIZON_DAYS, ge=7, le=180),
    db: Session = Depends(get_db),
):
    """Combined forecast + staffing + alerts for one sub-process."""
    return services.analyze_subprocess(db, subprocess_id, horizon_days=horizon)


@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    return services.all_alerts(db)


@router.post("/scenario")
def run_scenario(payload: ScenarioRequest, db: Session = Depends(get_db)):
    """What-if: override volume growth % and/or target FTE for one sub-process
    and recompute forecast + staffing + alerts against those overrides."""
    return services.analyze_subprocess(
        db,
        payload.subprocess_id,
        horizon_days=payload.horizon_days,
        growth_pct=payload.growth_pct,
        target_fte=payload.target_fte,
    )
