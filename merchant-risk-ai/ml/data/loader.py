"""Load tabular transaction data for local development workflows."""

from pathlib import Path

import pandas as pd


def load_transactions(csv_path: str | Path) -> pd.DataFrame:
    """Read a transaction CSV without changing its values or column order."""
    path = Path(csv_path)
    if not path.is_file():
        raise FileNotFoundError(f"Transaction dataset was not found: {path}")
    return pd.read_csv(path)
