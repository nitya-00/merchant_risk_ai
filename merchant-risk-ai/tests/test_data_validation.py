"""Tests for synthetic transaction schema validation."""

from pathlib import Path
import sys
import unittest

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from data.synthetic.generate_data import generate_rows
from ml.data.validator import validate_transactions


class TransactionValidationTests(unittest.TestCase):
    """Verify the most important dataset integrity checks."""

    def setUp(self) -> None:
        """Create valid records for each test."""
        self.transactions = pd.DataFrame(generate_rows(3, 42))

    def test_valid_synthetic_rows_pass_validation(self) -> None:
        """The generator output should satisfy its own documented schema."""
        validate_transactions(self.transactions)

    def test_duplicate_transaction_ids_are_rejected(self) -> None:
        """A transaction ID must identify exactly one row."""
        self.transactions.loc[1, "transaction_id"] = self.transactions.loc[0, "transaction_id"]
        with self.assertRaisesRegex(ValueError, "unique"):
            validate_transactions(self.transactions)

    def test_non_binary_proxy_values_are_rejected(self) -> None:
        """Binary indicator columns should contain zero or one only."""
        self.transactions.loc[0, "is_proxy_or_vpn"] = 2
        with self.assertRaisesRegex(ValueError, "0 or 1"):
            validate_transactions(self.transactions)

    def test_missing_required_values_are_rejected(self) -> None:
        """The exploration pipeline should not silently impute source data."""
        self.transactions.loc[0, "payment_method"] = None
        with self.assertRaisesRegex(ValueError, "missing values"):
            validate_transactions(self.transactions)
