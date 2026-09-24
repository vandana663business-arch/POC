from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "staffing_poc.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Business constants derived from the client's real Intake benchmarks
FORECAST_HORIZON_DAYS = 56  # 8 weeks
TRAINING_LEAD_TIME_WEEKS = 12  # 2wk pre-process + 2wk process + 2wk nesting + 6wk ramp
SUSTAINED_GAP_WEEKS_THRESHOLD = 2  # consecutive weeks of understaffing before a hiring alert fires
HOURLY_RATE_USD = 24.0  # placeholder rate-card assumption (only figure given in client sheet)
HISTORY_DAYS = 90  # 3 months of daily dummy history
