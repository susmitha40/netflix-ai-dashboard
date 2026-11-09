# Power BI project rules (read before every task)

## Project
Netflix AI dashboard. Three synthetic CSVs in /data/raw:
customer churn, monthly region metrics, titles catalogue.
The data is synthetic. Never present it as real Netflix data.

## Model
- Tables: FactCustomers, FactMonthlyMetrics, FactTitles,
  DimDate, DimCountry, DimRegion, DimGenre, DimPlan.
- Relationships: one-to-many, single direction, dimension to fact.
  No fact-to-fact relationships.
- FactCustomers[churn_date] to DimDate is an INACTIVE relationship;
  use USERELATIONSHIP in measures that need it.
- FactMonthlyMetrics[month] must be converted to a date (first of month).
- Mark DimDate as the date table.
- Hide foreign-key and ID columns from report view.
- Remove redundant columns (e.g. region on FactCustomers) only after asking.

## Style
- Tables in PascalCase. Measures in "Title Case".
- Every measure gets a description and a display folder.
- DAX: use VAR and DIVIDE. No hardcoded numbers.

## Workflow
- Raw files in /data/raw are never edited.
- Before changing the model, summarize planned changes and wait for approval.
- Never invent columns or measures; inspect the model first.
- After each task, append an entry to docs/prompt-log.md.
