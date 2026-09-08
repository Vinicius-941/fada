# FADA

A Python-based data analysis project for detecting anomalous financial
transactions with explainable risk scoring and an interactive Streamlit
dashboard.

## Overview

This project analyzes financial transactions and identifies unusual behavior
using statistical and behavioral rules. It does not claim that a transaction is
fraudulent. Instead, it assigns a risk score and explains which signals caused
the alert.

The repository is structured as a portfolio-ready analytics project with:

- data cleaning and validation;
- customer behavior profiling;
- rule-based anomaly detection;
- explainable risk scoring;
- CSV and JSON report exports;
- an interactive Streamlit dashboard;
- automated tests for scoring and pipeline behavior.

## Features

- Detects high-value statistical outliers using the IQR method.
- Compares each transaction against the customer's own average behavior.
- Flags unusual transaction hours.
- Detects bursts of transactions within short time windows.
- Flags rapid activity across different cities.
- Detects categories outside a customer's normal spending pattern.
- Produces `LOW`, `MEDIUM`, `HIGH` and `CRITICAL` risk levels.
- Explains each score with human-readable risk reasons.

## Project Structure

```text
.
├── dashboard/
│   └── app.py
├── data/
│   └── database.csv
├── docs/
│   └── methodology.md
├── scripts/
│   └── generate_sample_data.py
├── src/
│   ├── anomaly_detection.py
│   ├── cleaning.py
│   ├── config.py
│   ├── data_loader.py
│   ├── pipeline.py
│   ├── profiling.py
│   ├── reporting.py
│   └── scoring.py
├── tests/
│   ├── test_pipeline.py
│   └── test_scoring.py
├── run_analysis.py
├── requirements.txt
└── README.md
```

## Dataset

The included dataset is synthetic and generated for demonstration purposes. It
contains realistic transaction fields such as customer ID, date, time, amount,
category, city and payment method.

To regenerate it:

```bash
python scripts/generate_sample_data.py
```

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux, activate with:

```bash
source .venv/bin/activate
```

## Run the Analysis

```bash
python run_analysis.py
```

This generates reports in the `reports/` directory:

- `analyzed_transactions.csv`
- `high_risk_transactions.csv`
- `summary.json`

## Run the Dashboard

```bash
python -m streamlit run dashboard/app.py
```

The dashboard includes summary metrics, risk distribution, transaction value
distribution, daily activity, anomaly signal frequency, a suspicious transaction
table and a transaction inspector.

## Run Tests

```bash
pytest
```

## Methodology

The detection logic is intentionally transparent. Each anomaly signal has a
weight, and the final score is capped at 100. More details are available in
[`docs/methodology.md`](docs/methodology.md).

## Limitations

- The dataset is synthetic.
- The system is rule-based and does not use supervised fraud labels.
- Risk scores should be treated as investigation signals, not final decisions.
- A production version would require privacy controls, monitoring, model
  evaluation, audit logging and human review workflows.
