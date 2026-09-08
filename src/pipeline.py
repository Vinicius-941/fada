from src.anomaly_detection import detect_all_anomalies
from src.cleaning import clean_transactions
from src.data_loader import load_transactions
from src.profiling import build_customer_profiles
from src.reporting import build_summary, export_reports
from src.scoring import apply_risk_scoring


def run_pipeline(export=True):
    database = load_transactions()
    database = clean_transactions(database)
    database = build_customer_profiles(database)
    database = detect_all_anomalies(database)
    database = apply_risk_scoring(database)
    summary = build_summary(database)

    if export:
        export_reports(database)

    return database, summary
