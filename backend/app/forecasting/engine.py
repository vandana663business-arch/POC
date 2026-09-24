"""Forecasting engine: Holt-Winters exponential smoothing (primary) plus a
weighted rolling-average baseline (for side-by-side comparison), applied
independently per Intake sub-process.

See ../../MODEL_NOTES.md for a plain-language explanation of how this works
and why Holt-Winters was chosen over ARIMA and a plain average.
"""

from datetime import timedelta

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

SEASONAL_PERIOD = 7  # weekly seasonality
CONFIDENCE_Z = 1.28  # ~80% interval, wide enough to be informative without looking falsely precise


def _future_dates(last_date, horizon_days: int) -> list:
    return [last_date + timedelta(days=i) for i in range(1, horizon_days + 1)]


def holt_winters_forecast(history: pd.Series, horizon_days: int) -> dict:
    """history: pd.Series of daily receipts, indexed by consecutive dates (no gaps).

    Returns forecast values plus the level/trend/seasonal components so the
    result can be explained in plain language (see MODEL_NOTES.md).
    """
    values = history.to_numpy(dtype=float)

    model = ExponentialSmoothing(
        values,
        trend="add",
        seasonal="add",
        seasonal_periods=SEASONAL_PERIOD,
        initialization_method="estimated",
    )
    fit = model.fit(optimized=True)

    forecast = np.maximum(fit.forecast(horizon_days), 0)
    resid_std = float(np.std(fit.resid)) if len(fit.resid) else 0.0

    lower = np.maximum(forecast - CONFIDENCE_Z * resid_std, 0)
    upper = forecast + CONFIDENCE_Z * resid_std

    seasonal_component = getattr(fit, "season", None)
    last_season = (
        [float(x) for x in seasonal_component[-SEASONAL_PERIOD:]]
        if seasonal_component is not None
        else None
    )

    return {
        "forecast": [float(x) for x in forecast],
        "lower": [float(x) for x in lower],
        "upper": [float(x) for x in upper],
        "level": float(fit.level[-1]) if hasattr(fit, "level") else None,
        "trend": float(fit.trend[-1]) if hasattr(fit, "trend") and fit.trend is not None else None,
        "seasonal_last_cycle": last_season,
    }


def weighted_rolling_average_forecast(history_df: pd.DataFrame, horizon_days: int, decay: float = 0.9) -> list:
    """history_df: DataFrame with 'date' and 'receipts' columns, most recent last.

    Baseline comparison method matching the client's own "3-month rolling /
    weighted average" language: for each weekday, average that weekday's past
    values with more weight on recent weeks, then repeat forward.
    """
    df = history_df.copy()
    df["weekday"] = pd.to_datetime(df["date"]).dt.weekday

    last_date = pd.to_datetime(df["date"]).max()
    weekday_avg = {}
    for wd, group in df.groupby("weekday"):
        ordered = group.sort_values("date")
        n = len(ordered)
        weights = decay ** np.arange(n - 1, -1, -1)  # most recent gets weight closest to 1
        weekday_avg[wd] = float(np.average(ordered["receipts"], weights=weights))

    future_dates = _future_dates(last_date.date(), horizon_days)
    return [weekday_avg[d.weekday()] for d in future_dates]


def build_forecast(history_df: pd.DataFrame, horizon_days: int) -> dict:
    """history_df: DataFrame with 'date' (date) and 'receipts' (int) columns,
    sorted ascending, no gaps. Returns history echo + both forecast methods.
    """
    history_df = history_df.sort_values("date").reset_index(drop=True)
    series = pd.Series(history_df["receipts"].values)

    hw = holt_winters_forecast(series, horizon_days)
    baseline = weighted_rolling_average_forecast(history_df, horizon_days)

    last_date = pd.to_datetime(history_df["date"]).max().date()
    future_dates = [d.isoformat() for d in _future_dates(last_date, horizon_days)]

    return {
        "history_dates": [d.isoformat() for d in pd.to_datetime(history_df["date"]).dt.date],
        "history_receipts": [int(x) for x in history_df["receipts"]],
        "forecast_dates": future_dates,
        "holt_winters": hw,
        "rolling_average_baseline": baseline,
    }
