def _most_common_value(series):
    mode = series.mode()
    if mode.empty:
        return None
    return mode.iloc[0]


def build_customer_profiles(database):
    database = database.copy()
    customer_group = database.groupby("customer_id")

    database["customer_transaction_count"] = customer_group["amount"].transform("count")
    database["customer_avg_amount"] = customer_group["amount"].transform("mean")
    database["customer_median_amount"] = customer_group["amount"].transform("median")

    primary_city = database.groupby("customer_id")["city"].agg(_most_common_value)
    database["customer_primary_city"] = database["customer_id"].map(primary_city)

    primary_payment = database.groupby("customer_id")["payment_method"].agg(
        _most_common_value
    )
    database["customer_primary_payment"] = database["customer_id"].map(primary_payment)
    database["amount_vs_customer_avg"] = (
        database["amount"] / database["customer_avg_amount"]
    )

    return database
