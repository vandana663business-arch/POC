# How the forecasting model works (plain language)

This note explains the forecasting method used in the POC, written for someone
who doesn't have a statistics background but wants to understand and be able
to explain the approach.

## Where the data comes from

In the real process, there's no API -- historical volumes, productivity, and
headcount all live in Excel files dropped into SharePoint/OneDrive. This POC
mirrors that: the dummy data is generated into an actual Excel workbook,
`sample_data/Intake_Dummy_Data.xlsx`, with four sheets (SubProcess
Benchmarks, Daily Volume, Daily FTE, Daily Prod). A separate ingestion script
(`backend/scripts/load_excel_to_db.py`) reads that workbook and loads it into
the app's database -- the same shape a real ingestion job would follow if it
picked up a SharePoint export on a schedule. Everything downstream
(forecasting, staffing, alerts, the dashboard) reads only from the database,
never from the Excel file directly, so swapping in a real data source later
means replacing the ingestion script, not the rest of the app.

## What problem are we solving?

Every day, each of the 10 Intake sub-processes receives a number of new cases
("receipts"). We want to predict how many receipts will come in over the next
8 weeks, per sub-process, so we can then figure out how many staff are needed
to handle that volume.

## The method: Holt-Winters Exponential Smoothing

Think of any day's volume as being made up of three ingredients:

1. **Level** — the "normal" baseline volume right now, ignoring day-of-week
   effects. For example, "Communications is currently running about 500
   cases/day."
2. **Trend** — is that baseline slowly rising or falling over time? For
   example, "+0.1 cases/day" means volume is drifting up very slightly.
3. **Seasonality** — a repeating weekly pattern. Some days of the week are
   reliably busier or quieter than others. For example, Mondays might run
   about 15% above the baseline, while Saturdays run 30% below it.

Holt-Winters looks at the last 3 months of daily history and works out the
best-fitting values for these three ingredients. It then projects forward by
saying: "take the current level, add however much the trend has been moving
per day, then adjust up or down depending on which day of the week it is."
Each new day of real data quietly updates the level/trend/seasonality
estimates (that's what "exponential smoothing" means — recent data always
counts a bit more than older data), so the model naturally adapts as
conditions change.

We also compute a simple **confidence band** (a shaded range around the
forecast line) based on how much the model's past predictions have typically
been off by, so the dashboard can show "this is our best estimate, but the
real number will likely fall in this range" rather than a single falsely
precise number.

## The comparison baseline: weighted rolling average

Alongside Holt-Winters, we also compute a second, simpler forecast: for each
day of the week, take the (recency-weighted) average of that weekday's past
values over the last 3 months, and repeat that forward. This mirrors the
"3-month rolling average" / "weighted average" language already used in the
client's own spreadsheets, so the new model's output can be sanity-checked
against a method stakeholders already trust. In practice the two lines track
each other closely most of the time — Holt-Winters mainly pulls ahead when
there's a genuine trend (steadily rising or falling volume) that a flat
average can't see coming.

## Why Holt-Winters instead of ARIMA?

ARIMA is a legitimate, well-known forecasting method, and it isn't ruled out
forever — just not the right starting point for this POC. Reasons:

1. **Tuning burden.** ARIMA needs several numeric settings chosen per series
   (how far back to look, how much to "difference" the data, etc.). We have
   10 separate sub-processes, so that's 10 separate tuning problems, each of
   which can silently go wrong. Holt-Winters needs far less tuning — mainly
   just telling it "yes, there's a 7-day weekly pattern."
2. **Sensitivity to spikes.** The dummy data intentionally includes a few
   volume spikes (so the alert system has real events to react to during a
   demo). ARIMA's math involves "differencing" the data, which tends to
   amplify the effect of sudden spikes on the fitted model. Holt-Winters is
   more robust to this.
3. **Explainability.** ARIMA's internal numbers are abstract statistical
   coefficients that don't map to a business sentence. Holt-Winters splits
   the forecast into level / trend / seasonality — three ideas anyone can
   understand and see plotted separately.
4. **Data volume is not the deciding factor.** With 90 days of history
   (about 13 weekly cycles), there's technically enough data for either
   method — so the choice here is about reliability and explainability for a
   first POC, not about needing more data.

**Bottom line:** ARIMA remains a reasonable "phase 2" upgrade once more real
history is available and forecast accuracy needs to be squeezed further. For
a first, demoable, explainable POC, Holt-Winters is the safer choice.

## How the forecast turns into a staffing number

Each sub-process has a **CPD** (Cases Per Day) benchmark — how many cases one
full-time employee can process in a day. Required staff for a given forecast
day is simply:

```
required_fte = forecasted_volume_that_day / CPD
```

That required number is then compared against the currently planned
headcount to see if there's a gap — see the staffing and alerting logic for
how that gap turns into actual alerts.
