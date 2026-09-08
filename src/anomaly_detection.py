import pandas as pd

from src.config import (
    BURST_TRANSACTION_COUNT,
    BURST_WINDOW_MINUTES,
    CUSTOMER_AMOUNT_MULTIPLIER,
    MIN_CUSTOMER_HISTORY,
    RAPID_CITY_CHANGE_MINUTES,
    UNUSUAL_HOUR_END,
    UNUSUAL_HOUR_START,
)


def detect_global_amount_anomalies(database):
    database = database.copy()

    q1 = database["amount"].quantile(0.25)
    q3 = database["amount"].quantile(0.75)
    iqr = q3 - q1
    upper_limit = q3 + (1.5 * iqr)

    database["high_amount"] = database["amount"] > upper_limit
    return database


def detect_customer_amount_anomalies(database):
    database = database.copy()

    enough_history = database["customer_transaction_count"] >= MIN_CUSTOMER_HISTORY
    unusually_large = database["amount_vs_customer_avg"] >= CUSTOMER_AMOUNT_MULTIPLIER

    database["unusual_customer_amount"] = enough_history & unusually_large
    return database


def detect_unusual_hours(database):
    database = database.copy()
    database["unusual_hour"] = database["hour"].between(
        UNUSUAL_HOUR_START,
        UNUSUAL_HOUR_END,
    )
    return database


def detect_transaction_bursts(database):
    database = database.copy()
    database["transaction_burst"] = False

    window = pd.Timedelta(minutes=BURST_WINDOW_MINUTES)

    for _, group in database.groupby("customer_id"):
        group = group.sort_values("datetime")
        indexes = group.index.tolist()
        times = group["datetime"].tolist()
        left = 0

        for right in range(len(times)):
            while times[right] - times[left] > window:
                left += 1

            if right - left + 1 >= BURST_TRANSACTION_COUNT:
                database.loc[indexes[left : right + 1], "transaction_burst"] = True

    return database


def detect_rapid_city_changes(database):
    database = database.copy().sort_values(["customer_id", "datetime"])

    previous_city = database.groupby("customer_id")["city"].shift(1)
    previous_datetime = database.groupby("customer_id")["datetime"].shift(1)
    minutes_since_previous = (
        database["datetime"] - previous_datetime
    ).dt.total_seconds() / 60

    database["rapid_city_change"] = (
        (database["city"] != previous_city)
        & (minutes_since_previous <= RAPID_CITY_CHANGE_MINUTES)
        & previous_city.notna()
    )
    return database


def detect_unusual_categories(database):
    database = database.copy()
    database["unusual_category"] = False

    for _, group in database.groupby("customer_id"):
        if len(group) < MIN_CUSTOMER_HISTORY:
            continue

        normal_categories = set(group["category"].value_counts().head(3).index)
        unusual_indexes = group[~group["category"].isin(normal_categories)].index
        database.loc[unusual_indexes, "unusual_category"] = True

    return database


def detect_all_anomalies(database):
    database = detect_global_amount_anomalies(database)
    database = detect_customer_amount_anomalies(database)
    database = detect_unusual_hours(database)
    database = detect_transaction_bursts(database)
    database = detect_rapid_city_changes(database)
    database = detect_unusual_categories(database)
    return database
