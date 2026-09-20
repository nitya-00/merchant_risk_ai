# Stage 3 feature engineering

The Stage 3 pipeline produces deterministic, row-level features from fields available when an order is assessed. It does not learn from labels, calculate dataset-wide thresholds, aggregate a customer's future activity, or encode categories using outcome data.

| Source context | Derived feature | Transformation |
| --- | --- | --- |
| Account age | `account_age_days_log1p`, `is_new_account` | `log1p(age)` and `age ≤ 7` |
| Recent orders | `orders_last_30d_log1p` | `log1p(count)` |
| Order amount | `order_amount_log1p` | `log1p(amount)` |
| Addresses and shipping | `is_billing_shipping_mismatch`, `is_expedited_shipping` | Direct row-level indicators |
| Payment attempts | `has_recent_payment_failure`, `has_repeated_payment_failures` | `count > 0` and `count ≥ 3` |
| Session context | `is_cross_border_ip` | IP country differs from billing country |

The raw `is_proxy_or_vpn` field is type-normalized within the feature frame. The target `is_high_risk` is excluded by default; set `keep_target=True` only for an explicitly controlled later training workflow.

Feature encoding, feature selection, and any transformations estimated from training data will be introduced only after a train/validation/test split is defined. This keeps future held-out test rows out of training and feature-selection decisions.
