# Synthetic e-commerce transaction dataset

## Purpose and scope

This project currently uses generated, non-production order records for development. The dataset represents one row per attempted e-commerce order and includes order, customer-account, payment-attempt, and session-context fields. It contains no real people, credentials, addresses, payment details, or merchant data.

`is_high_risk` is a synthetic label for a potentially fraudulent or abusive order. It is not a production fraud decision, a chargeback outcome, or a customer classification.

## Schema

| Field | Description |
| --- | --- |
| `transaction_id`, `order_id`, `customer_id`, `device_id` | Synthetic opaque identifiers. |
| `order_timestamp` | UTC ISO-8601 timestamp in 2025. |
| `order_amount`, `currency`, `items_count` | Basic order context; the current generator emits INR only. |
| `payment_method` | Synthetic payment category. |
| `billing_country`, `shipping_country`, `billing_shipping_match` | Coarse location and address-match context. |
| `account_age_days`, `orders_last_30d` | Synthetic customer-account history. |
| `failed_payment_attempts_24h` | Recent simulated payment failures. |
| `ip_country`, `is_proxy_or_vpn` | Synthetic session/network context. |
| `email_domain_type`, `shipping_speed` | Additional simulated order context. |
| `is_high_risk` | Binary synthetic training label: `1` for simulated high risk, otherwise `0`. |

## Label assumptions and limits

The generator raises the probability of a positive label when several transparent, simulated conditions occur: an address mismatch, cross-country IP, proxy/VPN use, repeated failed payments, a new account, a disposable email domain, a very large order, or same-day shipping. A seeded random draw then determines the final label.

These assumptions exist only to create a development dataset with a minority positive class. They must not be used as production rules, policy, or evidence of fraud. Real-world training requires appropriately governed historical outcomes, data-quality checks, privacy review, and bias assessment.

## Generate a dataset

From the repository root:

```bash
python3 scripts/generate_dataset.py --rows 5000 --seed 42 --output data/raw/synthetic_transactions.csv
```

The same row count and seed produce the same dataset. Generated full datasets belong in `data/raw/` and are ignored by Git. The small CSV in `data/samples/` is the tracked 10-row output of `--rows 10 --seed 2026`.

Data splitting, feature transformations, and model evaluation are deliberately deferred to later stages. In particular, do not use a future held-out test partition to make generation, feature, threshold, or model decisions.
