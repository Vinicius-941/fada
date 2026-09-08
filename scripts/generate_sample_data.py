import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT / "data" / "database.csv"
random.seed(42)

CATEGORIES = [
    "Groceries",
    "Pharmacy",
    "Transport",
    "Restaurant",
    "Fuel",
    "Electronics",
    "Travel",
    "Online Shopping",
    "Utilities",
    "Entertainment",
]
CITIES = [
    "Sao Paulo",
    "Rio de Janeiro",
    "Belo Horizonte",
    "Curitiba",
    "Porto Alegre",
    "Salvador",
    "Recife",
    "Brasilia",
    "Fortaleza",
    "Campinas",
]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "Pix", "Bank Transfer", "Digital Wallet"]


def money_value(category):
    base_ranges = {
        "Groceries": (25, 450),
        "Pharmacy": (15, 320),
        "Transport": (8, 160),
        "Restaurant": (30, 380),
        "Fuel": (80, 450),
        "Electronics": (120, 3500),
        "Travel": (250, 7000),
        "Online Shopping": (40, 1800),
        "Utilities": (70, 900),
        "Entertainment": (25, 600),
    }
    low, high = base_ranges[category]
    return round(random.triangular(low, high, low + (high - low) * 0.25), 2)


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    customers = list(range(100001, 100221))
    start = datetime(2026, 1, 1, 6, 0, 0)

    rows = []
    transaction_id = 12345

    for _ in range(2500):
        customer_id = random.choice(customers)
        category = random.choice(CATEGORIES)
        city = random.choice(CITIES)
        payment_method = random.choice(PAYMENT_METHODS)
        occurred_at = start + timedelta(
            days=random.randint(0, 89),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59),
        )
        amount = money_value(category)

        if random.random() < 0.035:
            amount = round(amount * random.uniform(4, 9), 2)

        rows.append(
            {
                "transaction_id": transaction_id,
                "customer_id": customer_id,
                "date": occurred_at.strftime("%d/%m/%Y"),
                "time": occurred_at.strftime("%H:%M:%S"),
                "amount": amount,
                "category": category,
                "city": city,
                "payment_method": payment_method,
            }
        )
        transaction_id += 1

    for customer_id in random.sample(customers, 12):
        burst_start = start + timedelta(
            days=random.randint(1, 88),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 45),
        )
        city_a, city_b = random.sample(CITIES, 2)

        for offset in range(5):
            occurred_at = burst_start + timedelta(minutes=offset * 2)
            rows.append(
                {
                    "transaction_id": transaction_id,
                    "customer_id": customer_id,
                    "date": occurred_at.strftime("%d/%m/%Y"),
                    "time": occurred_at.strftime("%H:%M:%S"),
                    "amount": round(random.uniform(600, 4500), 2),
                    "category": random.choice(["Electronics", "Travel", "Online Shopping"]),
                    "city": city_a if offset < 3 else city_b,
                    "payment_method": random.choice(PAYMENT_METHODS),
                }
            )
            transaction_id += 1

    rows.sort(key=lambda row: (row["date"], row["time"], row["transaction_id"]))

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "transaction_id",
                "customer_id",
                "date",
                "time",
                "amount",
                "category",
                "city",
                "payment_method",
            ],
            delimiter=";",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} transactions to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
