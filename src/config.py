from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
DATABASE_PATH = DATA_DIR / "database.csv"

UNUSUAL_HOUR_START = 0
UNUSUAL_HOUR_END = 5
CUSTOMER_AMOUNT_MULTIPLIER = 4
MIN_CUSTOMER_HISTORY = 5
BURST_TRANSACTION_COUNT = 5
BURST_WINDOW_MINUTES = 10
RAPID_CITY_CHANGE_MINUTES = 120

RISK_WEIGHTS = {
    "high_amount": 20,
    "unusual_customer_amount": 25,
    "unusual_hour": 10,
    "transaction_burst": 25,
    "rapid_city_change": 15,
    "unusual_category": 10,
}
