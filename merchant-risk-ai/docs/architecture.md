# Architecture

Merchant Risk AI is separated into data, ML, backend, and frontend layers. At this stage, the active flow is:

```text
Synthetic CSV → schema validation → row-level feature frame → future training stage
```

The feature frame does not perform train/test splitting, label encoding, model fitting, or prediction. Those operations remain separate so the eventual held-out test set is not used during exploratory work.
