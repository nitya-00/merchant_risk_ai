"""Assemble leakage-aware, row-level feature frames for later modelling stages."""

import pandas as pd

from ml.data.validator import TARGET_COLUMN, validate_transactions
from ml.features.behavioral_features import add_behavioral_features
from ml.features.customer_features import add_customer_features
from ml.features.transaction_features import add_transaction_features


ENGINEERED_FEATURE_COLUMNS = (
    "account_age_days_log1p",
    "is_new_account",
    "orders_last_30d_log1p",
    "order_amount_log1p",
    "is_billing_shipping_mismatch",
    "is_expedited_shipping",
    "has_recent_payment_failure",
    "has_repeated_payment_failures",
    "is_cross_border_ip",
)


def build_feature_frame(
    transactions: pd.DataFrame, *, keep_target: bool = False
) -> pd.DataFrame:
    """Return validated row-level features, excluding the target unless requested.

    The pipeline intentionally uses only fields available for the transaction being
    assessed. It performs no learned encoding, splitting, target encoding, or
    dataset-wide statistic calculation; those choices belong to later stages.
    """
    validate_transactions(transactions, require_target=keep_target)
    features = add_customer_features(transactions)
    features = add_transaction_features(features)
    features = add_behavioral_features(features)
    if not keep_target and TARGET_COLUMN in features:
        features = features.drop(columns=TARGET_COLUMN)
    return features
