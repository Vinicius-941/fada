from src.pipeline import run_pipeline


def main():
    _, summary = run_pipeline(export=True)

    print("Financial transaction anomaly analysis completed.")
    print(f"Transactions analyzed: {summary['total_transactions']}")
    print(f"Transactions with alerts: {summary['suspicious_transactions']}")
    print(f"High-risk transactions: {summary['high_risk_transactions']}")
    print(f"Anomaly rate: {summary['anomaly_rate_percent']}%")


if __name__ == "__main__":
    main()
