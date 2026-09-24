"""Ground-truth Intake sub-process benchmarks, extracted from the client's real workbook.

fte_capacity = cpd * target_fte_count, matching the client's own formula
(verified against their "Overall-Intake SLA Trend" sheet).
"""

SUBPROCESSES = [
    {"name": "Commercial and Medicare Retrospective (Claims) - INSINQ", "cpd": 35, "cph": 4.7, "target_fte_count": 1},
    {"name": "Commercial and Medicare Retrospective (Claims) - OCWA", "cpd": 35, "cph": 4.7, "target_fte_count": 4},
    {"name": "Commercial and Medicare Retrospective (Claims) - Predictal", "cpd": 35, "cph": 4.7, "target_fte_count": 4},
    {"name": "Communications", "cpd": 126, "cph": 16.8, "target_fte_count": 6},
    {"name": "Commercial and Medicare Triage 1", "cpd": 49, "cph": 6.5, "target_fte_count": 4},
    {"name": "Commercial and Medicare Triage 2 - Inpatient", "cpd": 49, "cph": 6.5, "target_fte_count": 4},
    {"name": "Commercial and Medicare Triage 3 - Outpatient", "cpd": 98, "cph": 13.1, "target_fte_count": 6},
    {"name": "Medicaid Hybrid Navigator", "cpd": 49, "cph": 6.5, "target_fte_count": 4},
    {"name": "Medicaid MSHO Level 1", "cpd": 126, "cph": 16.8, "target_fte_count": 4},
    {"name": "Medicaid MSHO Level 2", "cpd": 49, "cph": 6.5, "target_fte_count": 2},
]

for row in SUBPROCESSES:
    row["fte_capacity"] = row["cpd"] * row["target_fte_count"]
