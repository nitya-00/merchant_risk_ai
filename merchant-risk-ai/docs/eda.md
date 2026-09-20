# Stage 3 exploratory data analysis

## Dataset reviewed

The local synthetic development dataset was generated with:

```bash
python3 scripts/generate_dataset.py --rows 5000 --seed 42 --output data/raw/synthetic_transactions.csv
```

It contains 5,000 rows and 20 columns. Validation found no missing values and no duplicate transaction IDs.

## Descriptive observations

| Measure | Result |
| --- | ---: |
| Synthetic positive labels | 575 |
| Synthetic positive-label share | 11.50% |
| Median order amount, label 0 | INR 1,461.90 |
| Median order amount, label 1 | INR 1,618.22 |
| Median account age, label 0 | 913 days |
| Median account age, label 1 | 875 days |

The synthetic label is a minority class, which is suitable for exploring class-imbalance handling later. These values only describe generated data: they are not evidence about real fraud rates, merchants, customers, or payment methods.

The accompanying [EDA notebook](../notebooks/01_data_exploration.ipynb) provides repeatable schema, missingness, class-balance, and group-summary checks. It does not perform a train/test split or compute model metrics.
