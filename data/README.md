# Data notes

All files in `raw/` are **synthetic** and were generated with Python for portfolio use.
They do not contain real Netflix or customer data.

| File | Rows | Grain |
|---|---|---|
| netflix_customer_churn_synthetic.csv | 5,000 | one row per customer |
| netflix_monthly_region_metrics_synthetic.csv | 192 | one row per region per month (2022-2025) |
| netflix_titles_synthetic.csv | 1,200 | one row per title |

Intentional gaps (for Power Query practice): blank `age`, `country`, `imdb_score`, `maturity_rating`;
`duration_min` empty for TV shows; `seasons` empty for movies; `churn_*` empty for active customers.

`processed/` holds derived files (e.g. sentiment scores). `raw/` is never edited.
