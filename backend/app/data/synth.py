"""Pure synthetic-data generation functions for the Intake dummy dataset.

Kept separate from any storage format (Excel or DB) so the same generation
logic can be reused by both the Excel-producing script and, if ever needed,
a direct-to-DB path.

Calibration notes (traceable back to the client's real workbook):
- The 10 sub-process benchmarks (cpd/cph/target_fte_count) are the real ones
  from the client's sheet (see app/data/benchmarks.py).
- The client's real Intake volume runs ~57,000 receipts/month combined across
  all 10 sub-processes. We distribute that total across sub-processes
  proportional to their fte_capacity, at varied utilization levels -- most
  sub-processes run comfortably staffed, but two are deliberately calibrated
  to trend toward overcapacity, mirroring the wide swings (50%-150%+) seen in
  the client's own "Prod vs FTE Capacity" columns and giving the alert engine
  real events to fire on.
"""

from datetime import date, timedelta

import numpy as np

from app.data.benchmarks import SUBPROCESSES

TARGET_MONTHLY_TOTAL = 57000

# Per-sub-process utilization profile (index-aligned with SUBPROCESSES in
# app/data/benchmarks.py). Indices 6 (Triage 3 - Outpatient) and 8 (Medicaid
# MSHO Level 1) are the "at risk" sub-processes: high utilization *and* a
# strong upward trend, so their forecast crosses fte_capacity.
UTILIZATION_PROFILE = [0.55, 0.45, 0.40, 0.50, 0.48, 0.52, 1.05, 0.46, 0.95, 0.42]
HIGH_GROWTH_INDICES = {6, 8}
HIGH_GROWTH_TREND_RANGE = (0.20, 0.35)

# Mon=0 .. Sun=6. Weekdays run higher than weekends (receipts trickle in 24x7,
# but review/processing effort -- what actually gets logged as a "receipt" in
# their workflow -- concentrates on business days).
RAW_WEEKDAY_MULTIPLIERS = {0: 1.15, 1: 1.15, 2: 1.15, 3: 1.15, 4: 1.10, 5: 0.45, 6: 0.35}
_norm = 7 / sum(RAW_WEEKDAY_MULTIPLIERS.values())
WEEKDAY_MULTIPLIERS = {k: v * _norm for k, v in RAW_WEEKDAY_MULTIPLIERS.items()}

NOISE_STD_FRACTION = 0.10
SPIKE_COUNT_RANGE = (2, 3)
SPIKE_MULTIPLIER_RANGE = (1.5, 2.3)
TREND_TOTAL_CHANGE_RANGE = (-0.12, 0.15)  # total drift over the whole window, per sub-process (default profile)


def build_dates(history_days: int) -> list[date]:
    end = date.today()
    start = end - timedelta(days=history_days - 1)
    return [start + timedelta(days=i) for i in range(history_days)]


def generate_receipts(rng: np.random.Generator, fte_capacity: float, dates: list[date], utilization: float, trend_range: tuple) -> np.ndarray:
    base_mean = fte_capacity * utilization
    n = len(dates)

    trend_total = rng.uniform(*trend_range)
    trend_factors = 1 + np.linspace(0, trend_total, n)

    weekday_factors = np.array([WEEKDAY_MULTIPLIERS[d.weekday()] for d in dates])

    noise = rng.normal(loc=1.0, scale=NOISE_STD_FRACTION, size=n)
    noise = np.clip(noise, 0.5, 1.6)

    values = base_mean * trend_factors * weekday_factors * noise

    n_spikes = rng.integers(SPIKE_COUNT_RANGE[0], SPIKE_COUNT_RANGE[1] + 1)
    spike_days = rng.choice(n, size=n_spikes, replace=False)
    for d in spike_days:
        values[d] *= rng.uniform(*SPIKE_MULTIPLIER_RANGE)

    return np.maximum(np.round(values), 0).astype(int)


def generate_fte(rng: np.random.Generator, target_fte_count: int, n: int):
    actual = target_fte_count + rng.choice([-1, 0, 0, 0, 1], size=n)
    actual = np.maximum(actual, 1)
    planned = actual.copy()
    # occasional small planning deltas, mostly tracking actual
    delta_days = rng.choice(n, size=max(1, n // 15), replace=False)
    planned = planned.astype(float)
    planned[delta_days] += rng.choice([-1, 1], size=len(delta_days))
    planned = np.maximum(planned, 1)
    return actual.astype(float), planned


def generate_completed(rng: np.random.Generator, receipts: np.ndarray) -> np.ndarray:
    ratio = rng.uniform(0.90, 1.00, size=len(receipts))
    return np.round(receipts * ratio).astype(int)


def generate_all(history_days: int) -> dict:
    """Generates the full synthetic dataset for all 10 sub-processes.

    Returns a dict of lists-of-rows (plain dicts), one list per table, ready
    to be written out to Excel or any other format.
    """
    dates = build_dates(history_days)

    subprocess_rows = []
    volume_rows = []
    fte_rows = []
    prod_rows = []

    for idx, row in enumerate(SUBPROCESSES):
        rng = np.random.default_rng(seed=1000 + idx)

        subprocess_rows.append(
            {
                "name": row["name"],
                "cpd": row["cpd"],
                "cph": row["cph"],
                "target_fte_count": row["target_fte_count"],
                "fte_capacity": row["fte_capacity"],
            }
        )

        utilization = UTILIZATION_PROFILE[idx]
        trend_range = HIGH_GROWTH_TREND_RANGE if idx in HIGH_GROWTH_INDICES else TREND_TOTAL_CHANGE_RANGE
        receipts = generate_receipts(rng, row["fte_capacity"], dates, utilization, trend_range)
        actual_fte, planned_fte = generate_fte(rng, row["target_fte_count"], len(dates))
        completed = generate_completed(rng, receipts)

        for i, d in enumerate(dates):
            volume_rows.append({"subprocess_name": row["name"], "date": d, "receipts": int(receipts[i])})
            fte_rows.append(
                {
                    "subprocess_name": row["name"],
                    "date": d,
                    "actual_fte": float(actual_fte[i]),
                    "planned_fte": float(planned_fte[i]),
                }
            )
            prod_rows.append({"subprocess_name": row["name"], "date": d, "completed": int(completed[i])})

    return {
        "subprocess": subprocess_rows,
        "daily_volume": volume_rows,
        "daily_fte": fte_rows,
        "daily_prod": prod_rows,
    }
