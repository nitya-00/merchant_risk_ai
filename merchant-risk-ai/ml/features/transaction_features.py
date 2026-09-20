"""Build transaction and fulfilment-context features available at order time."""

import numpy as np
import pandas as pd


def add_transaction_features(transactions: pd.DataFrame) -> pd.DataFrame:
    """Add deterministic per-order features without using labels or dataset quantiles."""
    features = transactions.copy()
    features["order_amount_log1p"] = np.log1p(
        pd.to_numeric(features["order_amount"])
    )
    features["is_billing_shipping_mismatch"] = (
        pd.to_numeric(features["billing_shipping_match"]) == 0
    ).astype("int8")
    features["is_expedited_shipping"] = features["shipping_speed"].isin(
        ("express", "same_day")
    ).astype("int8")
    return features
