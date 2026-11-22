# SQL Customer Data Quality & Profiling

An introductory **SQLite** project using fictional customer records to demonstrate SQL profiling and reporting queries.

## What it demonstrates
- Record counts and missing-value checks by customer segment
- Duplicate identifier detection
- Monthly onboarding record counts

## Run
With the SQLite command-line tool installed:

```bash
sqlite3 demo.db < schema_and_data.sql
sqlite3 -header -column demo.db < analysis.sql
```

The dataset is entirely synthetic. These queries are examples for learning and demonstration, not validated business controls.
