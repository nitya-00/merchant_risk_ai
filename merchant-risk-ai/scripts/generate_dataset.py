"""Run the synthetic e-commerce transaction dataset generator."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from data.synthetic.generate_data import main


if __name__ == "__main__":
    main()
