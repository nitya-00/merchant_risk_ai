"""Tests for the synthetic transaction dataset generator."""

from pathlib import Path
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from data.synthetic.generate_data import FIELDNAMES, generate_rows, write_csv


class DatasetGenerationTests(unittest.TestCase):
    """Verify basic generator behavior without modelling any risk."""

    def test_generation_is_deterministic_for_a_seed(self) -> None:
        """Rows generated with identical inputs should be identical."""
        self.assertEqual(generate_rows(5, 42), generate_rows(5, 42))

    def test_generated_rows_match_the_documented_schema(self) -> None:
        """Every generated row should expose the documented CSV fields."""
        self.assertEqual(list(generate_rows(1, 42)[0]), FIELDNAMES)

    def test_write_csv_creates_a_file_with_a_header(self) -> None:
        """Generated CSV output should include the documented header."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "transactions.csv"
            write_csv(generate_rows(1, 42), output_path)
            self.assertEqual(output_path.read_text(encoding="utf-8").splitlines()[0].split(","), FIELDNAMES)


if __name__ == "__main__":
    unittest.main()
