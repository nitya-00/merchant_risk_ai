"""Build behavior and network-context features available at order time."""

import pandas as pd


def add_behavioral_features(transactions: pd.DataFrame) -> pd.DataFrame:
    """Add row-level behavioral features without deriving values from future orders."""
    features = transactions.copy()
    failed_attempts = pd.to_numeric(features["failed_payment_attempts_24h"])
    features["has_recent_payment_failure"] = (failed_attempts > 0).astype("int8")
    features["has_repeated_payment_failures"] = (failed_attempts >= 3).astype("int8")
    features["is_cross_border_ip"] = (
        features["ip_country"] != features["billing_country"]
    ).astype("int8")
    features["is_proxy_or_vpn"] = pd.to_numeric(features["is_proxy_or_vpn"]).astype("int8")
    return features
