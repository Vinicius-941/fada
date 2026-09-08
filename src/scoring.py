from src.config import RISK_WEIGHTS


RISK_REASON_LABELS = {
    "high_amount": "Statistical high-value transaction",
    "unusual_customer_amount": "Amount significantly above customer average",
    "unusual_hour": "Transaction during unusual hours",
    "transaction_burst": "Multiple transactions within a short period",
    "rapid_city_change": "Rapid transaction activity across different cities",
    "unusual_category": "Category outside normal customer behavior",
}


def calculate_risk_score(database):
    database = database.copy()
    database["risk_score"] = 0

    for anomaly, weight in RISK_WEIGHTS.items():
        database.loc[database[anomaly], "risk_score"] += weight

    database["risk_score"] = database["risk_score"].clip(lower=0, upper=100)
    return database


def classify_risk(score):
    if score >= 70:
        return "CRITICAL"
    if score >= 40:
        return "HIGH"
    if score >= 20:
        return "MEDIUM"
    return "LOW"


def add_risk_levels(database):
    database = database.copy()
    database["risk_level"] = database["risk_score"].apply(classify_risk)
    return database


def build_risk_reason(row):
    reasons = [
        description
        for anomaly, description in RISK_REASON_LABELS.items()
        if row.get(anomaly, False)
    ]

    if not reasons:
        return "No major anomaly detected"

    return "; ".join(reasons)


def add_risk_reasons(database):
    database = database.copy()
    database["risk_reasons"] = database.apply(build_risk_reason, axis=1)
    return database


def apply_risk_scoring(database):
    database = calculate_risk_score(database)
    database = add_risk_levels(database)
    database = add_risk_reasons(database)
    return database
