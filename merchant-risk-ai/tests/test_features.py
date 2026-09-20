"""Tests for leakage-aware, row-level feature generation."""

from pathlib import Path
import sys
import unittest

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from data.synthetic.generate_data import generate_rows
from ml.data.validator import TARGET_COLUMN
from ml.features.feature_pipeline import ENGINEERED_FEATURE_COLUMNS, build_feature_frame


class FeaturePipelineTests(unittest.TestCase):
    """Verify transformations and the default target-leakage guard."""

    def setUp(self) -> None:
        """Create a small, valid synthetic input frame."""
        self.transactions = pd.DataFrame(generate_rows(3, 42))

    def test_default_feature_frame_omits_the_target(self) -> None:
        """The synthetic label should not enter features by default."""
        features = build_feature_frame(self.transactions)
        self.assertNotIn(TARGET_COLUMN, features.columns)
        self.assertTrue(set(ENGINEERED_FEATURE_COLUMNS).issubset(features.columns))

    def test_target_can_be_preserved_for_a_later_controlled_workflow(self) -> None:
        """Target retention must be an explicit choice."""
        features = build_feature_frame(self.transactions, keep_target=True)
        self.assertIn(TARGET_COLUMN, features.columns)

    def test_feature_generation_does_not_mutate_the_input(self) -> None:
        """Raw transactions should remain unchanged by transformations."""
        original_columns = self.transactions.columns.tolist()
        build_feature_frame(self.transactions)
        self.assertEqual(self.transactions.columns.tolist(), original_columns)
