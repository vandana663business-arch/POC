"""Generates a synthetic (dummy) Intake data Excel workbook for the staffing
forecasting POC.

This models the real-world data flow described in the client's requirements:
their actual process has no API -- historical volumes, productivity, and
headcount all live in Excel files dropped into SharePoint/OneDrive. So for
this POC, the dummy data is likewise generated as an Excel workbook (not
written directly into the app's database). A separate ingestion step
(scripts/load_excel_to_db.py) reads this workbook and loads it into the
app's database, mirroring how a real ingestion pipeline would pick up a
SharePoint export.

Output: sample_data/Intake_Dummy_Data.xlsx (project root), with 4 sheets:
SubProcess Benchmarks, Daily Volume, Daily FTE, Daily Prod.

Re-runnable: overwrites the workbook each time it's run.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import HISTORY_DAYS
from app.data.synth import generate_all

OUTPUT_PATH = Path(__file__).resolve().parent.parent.parent / "sample_data" / "Intake_Dummy_Data.xlsx"


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = generate_all(HISTORY_DAYS)

    subprocess_df = pd.DataFrame(data["subprocess"])
    volume_df = pd.DataFrame(data["daily_volume"])
    fte_df = pd.DataFrame(data["daily_fte"])
    prod_df = pd.DataFrame(data["daily_prod"])

    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        subprocess_df.to_excel(writer, sheet_name="SubProcess Benchmarks", index=False)
        volume_df.to_excel(writer, sheet_name="Daily Volume", index=False)
        fte_df.to_excel(writer, sheet_name="Daily FTE", index=False)
        prod_df.to_excel(writer, sheet_name="Daily Prod", index=False)

    print(f"Wrote {OUTPUT_PATH}")
    print(f"  SubProcess Benchmarks: {len(subprocess_df)} rows")
    print(f"  Daily Volume:          {len(volume_df)} rows")
    print(f"  Daily FTE:             {len(fte_df)} rows")
    print(f"  Daily Prod:            {len(prod_df)} rows")

    totals = volume_df.groupby("subprocess_name")["receipts"].apply(lambda s: s.tail(30).sum())
    print("\nTrailing-30d receipt totals per sub-process:")
    for name, total in totals.items():
        print(f"  {name}: {total}")


if __name__ == "__main__":
    main()
