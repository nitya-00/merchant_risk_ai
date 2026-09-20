"""Build customer-account features available at order time."""

import numpy as np
import pandas as pd


def add_customer_features(transactions: pd.DataFrame) -> pd.DataFrame:
    """Add row-level account-history features without aggregating future orders."""
    features = transactions.copy()
    account_age = pd.to_numeric(features["account_age_days"])
    features["account_age_days_log1p"] = np.log1p(account_age)
    features["is_new_account"] = (account_age <= 7).astype("int8")
    features["orders_last_30d_log1p"] = np.log1p(
        pd.to_numeric(features["orders_last_30d"])
    )
    return features
