"""Generate reproducible, synthetic e-commerce order records for development."""

from __future__ import annotations

import argparse
import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path


FIELDNAMES = [
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
    "is_high_risk",
]

COUNTRIES = ("IN", "US", "GB", "AE", "SG", "DE", "AU")
PAYMENT_METHODS = ("card", "upi", "wallet", "bank_transfer")
EMAIL_DOMAIN_TYPES = ("consumer", "business", "disposable")
SHIPPING_SPEEDS = ("standard", "express", "same_day")
START_TIMESTAMP = datetime(2025, 1, 1, tzinfo=timezone.utc)


def _risk_label(row: dict[str, object], rng: random.Random) -> int:
    """Return a simulated label from transparent synthetic-risk assumptions."""
    probability = 0.02
    if row["billing_shipping_match"] == 0:
        probability += 0.09
    if row["ip_country"] != row["billing_country"]:
        probability += 0.07
    if row["is_proxy_or_vpn"] == 1:
        probability += 0.10
    if int(row["failed_payment_attempts_24h"]) >= 3:
        probability += 0.14
    if int(row["account_age_days"]) <= 7:
        probability += 0.06
    if row["email_domain_type"] == "disposable":
        probability += 0.08
    if float(row["order_amount"]) >= 25000:
        probability += 0.05
    if row["shipping_speed"] == "same_day":
        probability += 0.03
    return int(rng.random() < min(probability, 0.85))


def generate_rows(row_count: int, seed: int) -> list[dict[str, object]]:
    """Create deterministic synthetic transactions for the supplied seed."""
    if row_count < 1:
        raise ValueError("row_count must be at least 1")

    rng = random.Random(seed)
    rows: list[dict[str, object]] = []
    for index in range(1, row_count + 1):
        billing_country = rng.choice(COUNTRIES)
        billing_shipping_match = int(rng.random() < 0.88)
        shipping_country = billing_country if billing_shipping_match else rng.choice(COUNTRIES)
        order_amount = round(rng.lognormvariate(7.3, 0.9), 2)
        row: dict[str, object] = {
            "transaction_id": f"txn_{index:07d}",
            "order_id": f"ord_{index:07d}",
            "customer_id": f"cus_{rng.randint(1, max(2, row_count // 3)):06d}",
            "order_timestamp": (
                START_TIMESTAMP + timedelta(minutes=rng.randint(0, 525_599))
            ).isoformat(),
            "order_amount": order_amount,
            "currency": "INR",
            "payment_method": rng.choice(PAYMENT_METHODS),
            "billing_country": billing_country,
            "shipping_country": shipping_country,
            "billing_shipping_match": billing_shipping_match,
            "account_age_days": rng.randint(0, 1_825),
            "orders_last_30d": rng.randint(0, 20),
            "failed_payment_attempts_24h": rng.choices(
                population=(0, 1, 2, 3, 4, 5),
                weights=(70, 15, 8, 4, 2, 1),
                k=1,
            )[0],
            "device_id": f"dev_{rng.randint(1, max(2, row_count // 2)):06d}",
            "ip_country": rng.choice(COUNTRIES),
            "is_proxy_or_vpn": int(rng.random() < 0.08),
            "email_domain_type": rng.choices(
                population=EMAIL_DOMAIN_TYPES,
                weights=(80, 16, 4),
                k=1,
            )[0],
            "shipping_speed": rng.choices(
                population=SHIPPING_SPEEDS,
                weights=(70, 24, 6),
                k=1,
            )[0],
            "items_count": rng.randint(1, 8),
        }
        row["is_high_risk"] = _risk_label(row, rng)
        rows.append(row)
    return rows


def write_csv(rows: list[dict[str, object]], output_path: Path) -> None:
    """Write generated rows as a UTF-8 CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def parse_arguments() -> argparse.Namespace:
    """Parse data-generation command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=5_000, help="Number of records.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/raw/synthetic_transactions.csv"),
        help="Destination CSV path.",
    )
    return parser.parse_args()


def main() -> None:
    """Generate and write the requested synthetic dataset."""
    arguments = parse_arguments()
    write_csv(generate_rows(arguments.rows, arguments.seed), arguments.output)
    print(f"Wrote {arguments.rows} rows to {arguments.output}")


if __name__ == "__main__":
    main()
