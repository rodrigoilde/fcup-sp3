"""Merge UCI Adult train + test into a single ARX-ready CSV.

Outputs: ../data/adult.csv (semicolon-separated, ARX default).
- Strips surrounding whitespace introduced by the original space-after-comma layout.
- Removes the trailing '.' that appears on every income label in adult.test.
- Leaves '?' as the missing-value marker (ARX recognises it via the
  "Missing value" import dialog setting).
"""

from __future__ import annotations

import csv
from pathlib import Path

COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education-num",
    "marital-status", "occupation", "relationship", "race", "sex",
    "capital-gain", "capital-loss", "hours-per-week", "native-country",
    "income",
]

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "adult"
OUT_FILE = ROOT / "data" / "adult.csv"


def _read_raw(path: Path, skip_first: bool = False) -> list[list[str]]:
    rows: list[list[str]] = []
    with path.open("r", encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            if skip_first and i == 0:
                continue
            line = line.strip()
            if not line:
                continue
            fields = [f.strip() for f in line.split(",")]
            if len(fields) != len(COLUMNS):
                continue
            # The test file appends '.' to the income label; normalise.
            fields[-1] = fields[-1].rstrip(".")
            rows.append(fields)
    return rows


def main() -> None:
    rows = _read_raw(RAW_DIR / "adult.data") + _read_raw(
        RAW_DIR / "adult.test", skip_first=True
    )
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(COLUMNS)
        writer.writerows(rows)
    print(f"wrote {OUT_FILE.relative_to(ROOT)}  rows={len(rows)}")


if __name__ == "__main__":
    main()
