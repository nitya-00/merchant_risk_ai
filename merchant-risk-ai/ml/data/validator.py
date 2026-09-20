"""Validate the synthetic transaction dataset before exploration or features."""

import pandas as pd


REQUIRED_COLUMNS = (
    "transaction_id",
    "order_id",
    "customer_id",
    "order_timestamp",
    "order_amount",
    "currency",
    "payment_method",
    "billing_country",
    "shipping_country",
    "billing_shipping_match",
    "account_age_days",
    "orders_last_30d",
    "failed_payment_attempts_24h",
    "device_id",
    "ip_country",
    "is_proxy_or_vpn",
    "email_domain_type",
    "shipping_speed",
    "items_count",
)
TARGET_COLUMN = "is_high_risk"
BINARY_COLUMNS = ("billing_shipping_match", "is_proxy_or_vpn", TARGET_COLUMN)
NON_NEGATIVE_COLUMNS = (
    "account_age_days",
    "orders_last_30d",
    "failed_payment_attempts_24h",
)


def validate_transactions(
    transactions: pd.DataFrame, *, require_target: bool = True
) -> None:
    """Raise ``ValueError`` when transaction data violates the documented schema.

    Validation only inspects the supplied rows. It does not impute values, split data,
    calculate dataset-wide thresholds, or alter the input frame.
    """
    required_columns = set(REQUIRED_COLUMNS)
    if require_target:
        required_columns.add(TARGET_COLUMN)
    missing_columns = required_columns.difference(transactions.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Dataset is missing required columns: {missing}")
    if transactions.empty:
        raise ValueError("Dataset must contain at least one transaction")
    columns_with_missing_values = transactions.loc[:, sorted(required_columns)].columns[
        transactions.loc[:, sorted(required_columns)].isna().any()
    ].tolist()
    if columns_with_missing_values:
        missing = ", ".join(columns_with_missing_values)
        raise ValueError(f"Required columns contain missing values: {missing}")
    if transactions["transaction_id"].isna().any() or transactions["transaction_id"].duplicated().any():
        raise ValueError("transaction_id values must be present and unique")
    if pd.to_datetime(transactions["order_timestamp"], utc=True, errors="coerce").isna().any():
        raise ValueError("order_timestamp must contain valid timestamps")

    numeric_columns = ("order_amount", "items_count", *NON_NEGATIVE_COLUMNS)
    for column in numeric_columns:
        values = pd.to_numeric(transactions[column], errors="coerce")
        if values.isna().any():
            raise ValueError(f"{column} must contain numeric values")
        if column in NON_NEGATIVE_COLUMNS and (values < 0).any():
            raise ValueError(f"{column} cannot contain negative values")
    if (pd.to_numeric(transactions["order_amount"], errors="coerce") <= 0).any():
        raise ValueError("order_amount must be greater than zero")
    if (pd.to_numeric(transactions["items_count"], errors="coerce") <= 0).any():
        raise ValueError("items_count must be greater than zero")

    columns_to_check = BINARY_COLUMNS if require_target else BINARY_COLUMNS[:-1]
    for column in columns_to_check:
        values = set(pd.to_numeric(transactions[column], errors="coerce").dropna().unique())
        if values.difference({0, 1}):
            raise ValueError(f"{column} must contain only 0 or 1")
