# Methodology

This project uses rule-based anomaly detection to identify financial transactions
that differ from expected behavior. The output is a risk signal, not a fraud
verdict.

## Detection Signals

- Global high amount: transaction value above the IQR outlier threshold.
- Customer amount anomaly: amount at least four times the customer's average.
- Unusual hour: transaction between midnight and 5 a.m.
- Transaction burst: at least five transactions in ten minutes for one customer.
- Rapid city change: different cities within two hours for one customer.
- Unusual category: category outside the customer's three most frequent categories.

## Risk Score

Each signal has a configurable weight. The final score is capped at 100 and
converted into four levels: LOW, MEDIUM, HIGH and CRITICAL.

## Limitations

The sample dataset is synthetic and intentionally includes anomalies for portfolio
demonstration. A production system would need real labels, model monitoring,
privacy controls and human review workflows.
