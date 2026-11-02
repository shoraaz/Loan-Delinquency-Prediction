# Loan Delinquency Prediction

Supervised classification project that predicts the likelihood of a borrower
becoming delinquent on a loan, using identity, digital-footprint, phone-network
and fraud-network attributes from third-party data providers.

## Problem summary

Built as a Data Scientist I case study. The goal is to:

1. **Explore the data** – target definition and class balance, data types,
   missing values, duplicates, outliers and other quality issues.
2. **Engineer features** – a small set of well-motivated derived variables
   with a clear rationale for why they relate to delinquency.
3. **Model and validate** – an appropriate classifier assessed on a holdout,
   with at least two metrics suited to an imbalanced lending problem, plus a
   discussion of threshold choice (catching delinquents vs. wrongly flagging
   good borrowers).
4. **Interpret results** – strongest signals, assumptions, limitations and
   possible bias, keeping predictive association separate from causation.
5. **Score the test set** – every test record keeps its original columns, UID
   and row order, plus any engineered features and a **1–100 risk score**
   (100 = highest relative risk; not a calibrated probability unless calibration
   is shown).

`UID` is a row identifier only and should not be used as a predictive feature.

## Data

| File | Rows | Columns | Description |
|------|-----:|--------:|-------------|
| `data/processed/train.csv` | 10,000 | 91 | Labelled records: `UID`, provider attributes, `Target` |
| `data/processed/test.csv` | 5,000 | 90 | Same attributes without `Target` |
| `data/processed/feature_dictionary.csv` | 115 | 8 | Description, business meaning, category and expected risk direction per attribute |

**Target** (`Target`): `1` = delinquent, `0` = not delinquent.
Distribution in the training set: 9,114 × `0`, 878 × `1` (≈ 8.8 % positive),
and 8 rows with the value `NaT` (missing label).

**Attribute groups**

- `Email Attributes.*` – email age, domain existence / risk / corporate flag, footprint
- `Email Name Attributes.*` – match between applicant name and email, digital age
- `Email Social Advance.*` / `Phone Social Advance.*` – presence on online platforms
- `Phone Name Attributes.*` – phone footprint strength, digital age, revocation history
- `Phone Network.*` – carrier, region, reachability, porting history, billing type
- `Email GIN.*` / `Mobile GIN.*` – identity-graph and fraud-network indicators

**Known quality quirks** (observed during upload)

- Missing values are encoded in several ways: blank cells, the literal string
  `NaT`, and `-1` sentinels in numeric fields such as digital age.
- Several flag columns therefore load as `object` dtype and need cleaning.
- Column names in the dictionary don't always match the data exactly
  (e.g. `Email Name Attribute.` vs `Email Name Attributes.`, `Emial GIN.FraudCount`).

### Privacy

The raw Excel files supplied with the case study include direct personal
identifiers. These columns were **removed** before committing, and the raw
files are git-ignored:

- `name`
- `Phone to Name.UPIname`
- `Email Name Attributes.phoneNumber`

To regenerate the CSVs from the original files, put them in `data/raw/` and run:

```bash
python scripts/prepare_data.py
```

## Project structure

```
.
├── data/
│   ├── raw/              # original Excel files (git-ignored)
│   └── processed/        # sanitised CSVs used for analysis
├── notebooks/            # exploration and modelling notebooks
├── outputs/              # scored test set (Assignment_Test_<name>.csv)
├── reports/              # final write-up
├── scripts/
│   └── prepare_data.py   # raw Excel -> sanitised CSV
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```python
import pandas as pd

train = pd.read_csv("data/processed/train.csv", na_values=["NaT"], low_memory=False)
test = pd.read_csv("data/processed/test.csv", na_values=["NaT"], low_memory=False)
```
