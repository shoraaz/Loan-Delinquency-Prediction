"""Convert the raw case-study Excel files into sanitised CSVs.

The raw files supplied with the case study contain direct personal
identifiers. These columns are removed before anything is committed:

    - name                               (applicant full name)
    - Phone to Name.UPIname              (name registered against UPI handle)
    - Email Name Attributes.phoneNumber  (applicant phone number)

All other columns, the UID and the original row order are preserved.

Usage:
    python scripts/prepare_data.py [--raw-dir data/raw] [--out-dir data/processed]
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

PII_COLUMNS = [
    "name",
    "Phone to Name.UPIname",
    "Email Name Attributes.phoneNumber",
]

FILES = {
    "Assignment_Train.xlsx": "train.csv",
    "Assignment_Test.xlsx": "test.csv",
}

DICTIONARY_FILE = ("Assignment_FeatureDictionary.xlsx", "feature_dictionary.csv")


def sanitise(df: pd.DataFrame) -> pd.DataFrame:
    """Drop personal-identifier columns, keeping everything else unchanged."""
    return df.drop(columns=[c for c in PII_COLUMNS if c in df.columns])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--out-dir", type=Path, default=Path("data/processed"))
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    for src, dst in FILES.items():
        df = pd.read_excel(args.raw_dir / src)
        n_rows = len(df)
        clean = sanitise(df)
        assert len(clean) == n_rows, "row count changed"
        assert clean["UID"].is_unique, "UID is not unique"
        clean.to_csv(args.out_dir / dst, index=False)
        print(f"{src} -> {dst}: {clean.shape[0]} rows, {clean.shape[1]} columns")

    src, dst = DICTIONARY_FILE
    pd.read_excel(args.raw_dir / src).to_csv(args.out_dir / dst, index=False)
    print(f"{src} -> {dst}")


if __name__ == "__main__":
    main()
