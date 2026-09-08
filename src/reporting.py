import json

from src.config import REPORTS_DIR


def build_summary(database):
    total_transactions = len(database)
    suspicious_transactions = database[database["risk_score"] > 0]
    high_risk_transactions = database[
        database["risk_level"].isin(["HIGH", "CRITICAL"])
    ]
    anomaly_rate = 0

    if total_transactions:
        anomaly_rate = len(suspicious_transactions) / total_transactions * 100

    return {
        "total_transactions": total_transactions,
        "unique_customers": int(database["customer_id"].nunique()),
        "suspicious_transactions": len(suspicious_transactions),
        "high_risk_transactions": len(high_risk_transactions),
        "anomaly_rate_percent": round(anomaly_rate, 2),
        "average_transaction_amount": round(database["amount"].mean(), 2),
        "maximum_transaction_amount": round(database["amount"].max(), 2),
    }


def export_reports(database):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    analyzed_path = REPORTS_DIR / "analyzed_transactions.csv"
    high_risk_path = REPORTS_DIR / "high_risk_transactions.csv"
    summary_path = REPORTS_DIR / "summary.json"

    database.to_csv(analyzed_path, index=False)
    database[database["risk_level"].isin(["HIGH", "CRITICAL"])].to_csv(
        high_risk_path,
        index=False,
    )

    with open(summary_path, "w", encoding="utf-8") as file:
        json.dump(build_summary(database), file, indent=4)

    return {
        "analyzed": analyzed_path,
        "high_risk": high_risk_path,
        "summary": summary_path,
    }
