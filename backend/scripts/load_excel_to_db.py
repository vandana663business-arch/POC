"""Ingests the Intake dummy data Excel workbook into the app's database.

This is the "data comes from Excel" step: in the real process, someone would
drop a SharePoint export in this shape and this script (or its production
equivalent -- a scheduled job) picks it up and loads it. For this POC the
workbook is synthetic (see generate_dummy_data.py), but the ingestion path
is real: read the 4 sheets, validate/join them by sub-process name, and
populate the SubProcess / DailyVolume / DailyFTE / DailyProd tables that the
forecasting API reads from.

Re-runnable/idempotent: wipes and rebuilds the database from the workbook
each time it's run, so the workbook is always the single source of truth.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.data.db import SessionLocal, engine
from app.data.models import Base, SubProcess, DailyVolume, DailyFTE, DailyProd

INPUT_PATH = Path(__file__).resolve().parent.parent.parent / "sample_data" / "Intake_Dummy_Data.xlsx"


def main():
    if not INPUT_PATH.exists():
        raise SystemExit(
            f"No workbook found at {INPUT_PATH}.\n"
            "Run generate_dummy_data.py first to produce it."
        )

    print(f"Reading {INPUT_PATH} ...")
    subprocess_df = pd.read_excel(INPUT_PATH, sheet_name="SubProcess Benchmarks")
    volume_df = pd.read_excel(INPUT_PATH, sheet_name="Daily Volume")
    fte_df = pd.read_excel(INPUT_PATH, sheet_name="Daily FTE")
    prod_df = pd.read_excel(INPUT_PATH, sheet_name="Daily Prod")

    print("Resetting schema...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        name_to_id = {}
        for _, row in subprocess_df.iterrows():
            sp = SubProcess(
                name=row["name"],
                cpd=float(row["cpd"]),
                cph=float(row["cph"]),
                target_fte_count=int(row["target_fte_count"]),
                fte_capacity=float(row["fte_capacity"]),
            )
            db.add(sp)
            db.flush()
            name_to_id[row["name"]] = sp.id

        unmatched = set(volume_df["subprocess_name"]) - set(name_to_id)
        if unmatched:
            raise SystemExit(f"Daily Volume references unknown sub-process names: {unmatched}")

        for _, row in volume_df.iterrows():
            db.add(
                DailyVolume(
                    subprocess_id=name_to_id[row["subprocess_name"]],
                    date=pd.to_datetime(row["date"]).date(),
                    receipts=int(row["receipts"]),
                )
            )

        for _, row in fte_df.iterrows():
            db.add(
                DailyFTE(
                    subprocess_id=name_to_id[row["subprocess_name"]],
                    date=pd.to_datetime(row["date"]).date(),
                    actual_fte=float(row["actual_fte"]),
                    planned_fte=float(row["planned_fte"]),
                )
            )

        for _, row in prod_df.iterrows():
            db.add(
                DailyProd(
                    subprocess_id=name_to_id[row["subprocess_name"]],
                    date=pd.to_datetime(row["date"]).date(),
                    completed=int(row["completed"]),
                )
            )

        db.commit()
    finally:
        db.close()

    print(
        f"Loaded {len(subprocess_df)} sub-processes, {len(volume_df)} volume rows, "
        f"{len(fte_df)} FTE rows, {len(prod_df)} prod rows into the database."
    )


if __name__ == "__main__":
    main()
