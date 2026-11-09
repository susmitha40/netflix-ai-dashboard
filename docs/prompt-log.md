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

## 2026-11-09, Prompt 4: Create specified DAX measures
**Tool/mode:** Copilot Agent / Power BI Desktop local model editing
**Prompt:**
```
Read docs/measures.md, verify its referenced columns, and create every
measure with its specified DAX expression, format, display folder, and
description.
```
**Result:** Verified all referenced columns and created all 45 measures across FactCustomers, FactMonthlyMetrics, and FactTitles with the specified expressions, formats, and folders. Applied the descriptions stated in the spec and concise descriptions for measures without one specified. Evaluated all 45 without filters; the four requested sanity checks passed (5,000 customers, 27.62% churn, 357.13 subscribers M, 1,200 titles). No measure evaluation errors or blanks.
**Issues:** `Customers Churned By Churn Date` returns 5,000 without a date filter because the exact specified expression counts all customer rows when the active date relationship is used without a selected date; only 1,381 customers are marked churned and 3,619 churn dates are blank. Preserved the requested expression exactly.
**Fix:** None; left all specified DAX expressions unchanged.

## 2026-11-09, Prompt 5: Audit measure values
**Tool/mode:** Copilot Agent / Power BI Desktop local model inspection
**Prompt:**
```
List all measures with table, folder, and format string. Evaluate each
without filters; flag blanks, errors, suspicious results, and sanity-check
mismatches from docs/measures.md.
```
**Result:** Re-listed all 45 measures and their table, display folder, and format string; re-evaluated every measure without filters. No measure returned blank or an error. Sanity checks matched: Total Customers = 5,000; Churn Rate = 27.62% (about 28%); Subscribers M = 357.13 (about 357); Total Titles = 1,200.
**Issues:** `Customers Churned By Churn Date` returns 5,000 without a date filter, rather than the 1,381 churned-customer count; its exact expression counts customer rows over the inactive relationship's unrestricted date context. This was previously identified; no change made.
**Fix:** None; audit only.

## 2026-11-09, Prompt 6: Add dark report theme
**Tool/mode:** Copilot Agent / PBIR report definition edit
**Prompt:**
```
Create a custom report theme with #141414 background, #E50914 accent,
#B3B3B3 secondary, white text, and Segoe UI. Store and reference it like
a Desktop-imported theme. Do not change pages.
```
**Result:** Added `StaticResources/RegisteredResources/NetflixDarkTheme.json`, registered it as a theme resource in `report.json`, and set the report custom-theme reference. Verified the page sections were unchanged and retained existing report/theme version values.
**Issues:** None.
**Fix:** None required.

## 2026-11-09, Prompt 7: Create Executive Overview report page
**Tool/mode:** Copilot Agent / PBIR report definition edit
**Prompt:**
```
Following docs/report-blueprint.md, create Page 1 "Executive Overview"
as PBIR files, using the existing visual structure and schema versions,
existing model measures and columns, and a 1280x720 grid. Add titles and
alt text to every visual; skip the specified AI and analytics visuals.
```
**Result:** Replaced the two placeholder visuals on Page 1 with a title, six KPI cards, a revenue line chart, a subscribers clustered-column chart, and Date/Region slicers. Kept the report's existing PBIR structure, visual query version, and schema versions. Validated all 11 visuals for titles/alt text, field bindings, and canvas bounds.
**Issues:** The model has `DimDate[Date]` but no `DimDate[Year]` or `DimDate[Month]`; used Date for the chart axis and slicer without changing the model. Navigation destinations do not exist on this page-only report, so no broken navigation buttons were added.
**Fix:** None required.

## 2026-11-09, Prompt 8: Create Why Customers Churn page
**Tool/mode:** Copilot Agent / live semantic model inspection and PBIR report definition edit
**Prompt:**
```
Following docs/report-blueprint.md, create Page 2 as PBIR files using
existing measures and columns, matching the report's schema versions and
1280x720 layout. Add titled, accessible visuals and list their fields and
positions; skip the specified AI and analytics visuals.
```
**Result:** Inspected the live model and added Page 2 with four KPI cards, a churn-reason bar chart, Date/Region slicers, a page heading, and reciprocal navigation buttons to Executive Overview. Preserved the existing PBIR structure and schema versions. Validated field bindings, titles, alt text, page targets, and all visual bounds; no semantic model changes were made.
**Issues:** The model has `DimDate[Date]` but no `DimDate[Year]`; used the existing Date field as a signup-date slicer, consistent with the active customer signup-date relationship.
**Fix:** None required.

## 2026-11-09, Prompt 9: Make KPI metric titles visible
**Tool/mode:** Copilot Agent / PBIR report definition edit
**Prompt:**
```
Metric titles are not visible on report.
```
**Result:** Enabled the card category labels on all 10 KPI cards across Executive Overview and Why Customers Churn, while preserving their existing visual title and accessibility configurations. Validated that each card's category label and title are enabled.
**Issues:** The card category labels had been explicitly hidden.
**Fix:** Set `categoryLabels.show` to true for all KPI card visuals.

## 2026-11-09, Prompt 10: Improve card and chart title contrast
**Tool/mode:** Copilot Agent / PBIR report definition edit
**Prompt:**
```
The page has no visible chart titles or card/chart borders. Add a light border.
```
**Result:** Made all card and chart titles dark, bold, and larger for contrast on the displayed light canvas. Added a light #D9D9D9 border to all 10 KPI cards and 3 charts across both pages. Validated title visibility settings and border values.
**Issues:** Titles were configured in white and blended into the light canvas; cards/charts had no border object.
**Fix:** Set title font color to #404040, font size to 12, and enabled a #D9D9D9 border with a subtle corner radius.

## 2026-11-09, Prompt 11: Style page and slicer titles
**Tool/mode:** Copilot Agent / PBIR report definition edit
**Prompt:**
```
Add the title to the page with Bold, Segoe font and also add titles to slicers.
```
**Result:** Styled both page headings as bold 24pt Segoe UI in dark text and made all four slicer titles visibly bold Segoe UI in dark text. Verified the text and style settings in the PBIR definitions.
**Issues:** Page headings and slicer titles were configured in white and not clearly visible on the light canvas.
**Fix:** Applied dark #404040 title text while preserving the existing page and slicer labels.

## 2026-11-09, Prompt 12: Fix slicer dropdown behavior
**Tool/mode:** Copilot Agent / PBIR report definition edit
**Prompt:**
```
Slicer dropdown is not working properly.
```
**Result:** Explicitly set all four report slicers to Dropdown mode and enabled slicer search. Validated that each slicer retains its field and title and has the expected dropdown/search settings.
**Issues:** The slicer visuals had no explicit dropdown mode or search setting.
**Fix:** Added `objects.data.mode = 'Dropdown'` and enabled `objects.search.isVisible` on each slicer.

## 2026-11-09, Prompt 13: Repair slicer dropdown interactions
**Tool/mode:** Copilot Agent / PBIR report definition edit
**Prompt:**
```
Dropdown is still not working.
```
**Result:** Repaired all four slicer field projections by marking the Values projection active. Explicitly enabled self-filtering, multi-select, Select All, and search while retaining Dropdown mode and the existing labels. Parsed and validated each slicer's field and interaction settings.
**Issues:** Dropdown mode alone did not ensure the field projection was active or self-filtering was enabled.
**Fix:** Added `active: true` to each Values projection and explicitly configured slicer interaction behavior.
