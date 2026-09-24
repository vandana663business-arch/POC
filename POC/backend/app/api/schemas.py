from pydantic import BaseModel

from app.config import FORECAST_HORIZON_DAYS


class ScenarioRequest(BaseModel):
    subprocess_id: int
    growth_pct: float = 0.0
    target_fte: float | None = None
    horizon_days: int = FORECAST_HORIZON_DAYS
