# Prompt log

Template (copy for each prompt):

## YYYY-MM-DD, Prompt N: short title
**Tool/mode:** Copilot Agent / Claude chat
**Prompt:**
```
(paste)
```
**Result:**
**Issues:**
**Fix:**

## 2026-11-09, Prompt 1: Propose shared-dimension star schema
**Tool/mode:** Copilot Agent / Power BI Desktop local model inspection
**Prompt:**
```
Connect to the open Power BI Desktop file, inspect the customer churn,
monthly region metrics, and titles tables, and propose three fact tables
with shared DimDate, DimCountry, DimRegion, DimGenre, and DimPlan.
List all columns to keep or drop and all relationships, including the
inactive churn_date relationship.
```
**Result:** Inspected the open `NetflixDashboard` model, all columns and current relationships, row grains, and relevant distinct values. Updated `docs/star-schema.md` with the proposed schema and column dispositions. No model changes were applied; the model awaits approval.
**Issues:** The current model uses four hidden local auto-date tables, and its churn-date relationship is active. The proposal replaces these with shared `DimDate` and an inactive churn-date relationship.
**Fix:** None applied; implementation was not requested.

## 2026-11-09, Prompt 2: Apply approved star schema
**Tool/mode:** Copilot Agent / Power BI Desktop local model editing
**Prompt:**
```
Apply the approved star schema to the open model: rename the fact tables,
create the five dimensions, establish relationships, make the churn-date
link inactive, mark DimDate as the date table, convert monthly dates to
month starts, and hide key columns.
```
**Result:** Renamed the three facts, created and calculated the five dimensions, established 11 one-to-many single-direction relationships, removed the four obsolete local date relationships/tables, marked `DimDate` as the date table, and hid the fact IDs/foreign keys. Saved the PBIP project and updated `docs/star-schema.md`.
**Issues:** The monthly metrics Power Query already typed `month` as `date`, and all 192 values were already first-of-month; retained that correct source conversion and applied `MMM yyyy` display formatting. The model-tool refresh failed on this Desktop instance, so local Analysis Services TOM `Calculate` processing was used successfully. Removing auto-date links initially failed because date variations referenced those relationships; removing the variations and clearing the generated tables' variation-only flags allowed cleanup. The hidden private date-table template remains.
**Fix:** Recalculated the model with TOM after adding relationships. DAX checks passed for all dimensions, the active date/country/genre/plan/region links, and `USERELATIONSHIP` on the inactive churn-date link.

## 2026-11-09, Prompt 3: Audit relationships and blank keys
**Tool/mode:** Copilot Agent / Power BI Desktop local model inspection
**Prompt:**
```
List all relationships with cardinality, direction, and active status.
Flag many-to-many, bidirectional, missing relationships, and blank keys.
```
**Result:** Inspected all 11 live relationships and checked blank values in dimension keys, fact foreign keys, and customer/title IDs. All planned links are present; all are one-to-many and single-direction with `FactCustomers[churn_date]` inactive. No many-to-many or bidirectional relationships were found. There are 45 blank title-country values represented by one blank `DimCountry` member and 3,619 blank customer churn dates.
**Issues:** Blank title countries require a blank/unknown member in `DimCountry`; blank churn dates are expected for customers without a churn date.
**Fix:** None; audit only.
