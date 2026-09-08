REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "date",
    "time",
    "amount",
    "category",
    "city",
    "payment_method",
]


def validate_columns(database):
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in database.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def clean_transactions(database):
    database = database.copy()
    validate_columns(database)

    database = database.drop_duplicates(subset=["transaction_id"])
    database["amount"] = database["amount"].astype(str).str.replace(",", ".", regex=False)
    database["amount"] = database["amount"].replace({"": None, "nan": None})
    database["amount"] = database["amount"].astype(float)

    database["datetime"] = database["date"].astype(str) + " " + database["time"].astype(str)
    database["datetime"] = database["datetime"].pipe(
        lambda column: __import__("pandas").to_datetime(
            column,
            dayfirst=True,
            errors="coerce",
        )
    )

    database = database.dropna(
        subset=["transaction_id", "customer_id", "amount", "datetime"]
    )
    database = database[database["amount"] > 0].copy()

    for column in ["category", "city", "payment_method"]:
        database[column] = database[column].astype(str).str.strip()

    database["hour"] = database["datetime"].dt.hour
    database = database.sort_values(["customer_id", "datetime"])
    return database.reset_index(drop=True)


def build_data_quality_report(database):
    return {
        "rows": len(database),
        "duplicate_transactions": int(database["transaction_id"].duplicated().sum()),
        "missing_values": int(database.isnull().sum().sum()),
        "unique_customers": int(database["customer_id"].nunique()),
    }
