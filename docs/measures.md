# DAX measures (specification for Copilot)

Create every measure below exactly as written, on the table named in the heading.
Set the format string, display folder and description for each. Do not rename tables or
columns. If a measure fails, report the error and do not silently change the DAX.

Assumed columns (verify against the model first):
- FactCustomers: customer_id, signup_date, churn_date, plan, monthly_price_usd, is_churned ("Yes"/"No"),
  tenure_months, avg_weekly_hours, days_since_last_login, support_tickets_90d, satisfaction_score, churn_reason
- FactMonthlyMetrics: month (date, first of month), region, opening_subscribers_m, gross_adds_m,
  churned_subscribers_m, closing_subscribers_m, arm_usd, revenue_usd_m, marketing_spend_usd_m,
  content_spend_usd_m, new_originals_released
- FactTitles: show_id, is_netflix_original ("Yes"/"No"), imdb_score, budget_usd_m, views_28d_m,
  hours_viewed_28d_m, completion_rate_pct, weeks_in_top10
- DimDate[Date] is the marked date table.

---

## Table: FactCustomers

### Folder: Parameters

**Low Engagement Threshold Hours** | format `0.0` | description: weekly hours below which a customer is low engagement
```dax
Low Engagement Threshold Hours = 4
```

**Inactivity Threshold Days** | format `0` | description: days since last login at or above which a customer is inactive
```dax
Inactivity Threshold Days = 14
```

### Folder: Customers

**Total Customers** | format `#,0`
```dax
Total Customers = DISTINCTCOUNT ( FactCustomers[customer_id] )
```

**Active Customers** | format `#,0`
```dax
Active Customers =
CALCULATE ( [Total Customers], FactCustomers[is_churned] = "No" )
```

**Churned Customers** | format `#,0`
```dax
Churned Customers =
CALCULATE ( [Total Customers], FactCustomers[is_churned] = "Yes" )
```

**Churn Rate %** | format `0.0%`
```dax
Churn Rate % = DIVIDE ( [Churned Customers], [Total Customers] )
```

**Retention Rate %** | format `0.0%`
```dax
Retention Rate % = 1 - [Churn Rate %]
```

**New Customers** | format `#,0` | description: customers by signup date (active relationship)
```dax
New Customers = COUNTROWS ( FactCustomers )
```

**Customers Churned By Churn Date** | format `#,0` | description: churned customers placed on the date they churned (uses the inactive relationship)
```dax
Customers Churned By Churn Date =
CALCULATE (
    COUNTROWS ( FactCustomers ),
    USERELATIONSHIP ( FactCustomers[churn_date], DimDate[Date] )
)
```

**Net Customer Change** | format `#,0;-#,0`
```dax
Net Customer Change = [New Customers] - [Customers Churned By Churn Date]
```

**Average Tenure Months** | format `0.0`
```dax
Average Tenure Months = AVERAGE ( FactCustomers[tenure_months] )
```

**Average Weekly Hours** | format `0.0`
```dax
Average Weekly Hours = AVERAGE ( FactCustomers[avg_weekly_hours] )
```

**Average Satisfaction Score** | format `0.0`
```dax
Average Satisfaction Score = AVERAGE ( FactCustomers[satisfaction_score] )
```

**Average Support Tickets** | format `0.00`
```dax
Average Support Tickets = AVERAGE ( FactCustomers[support_tickets_90d] )
```

### Folder: Revenue and Risk

**Monthly Recurring Revenue** | format `$#,0` | description: monthly price of active customers
```dax
Monthly Recurring Revenue =
CALCULATE ( SUM ( FactCustomers[monthly_price_usd] ), FactCustomers[is_churned] = "No" )
```

**Average Revenue Per Customer** | format `$#,0.00`
```dax
Average Revenue Per Customer =
DIVIDE ( [Monthly Recurring Revenue], [Active Customers] )
```

**Lost Monthly Revenue** | format `$#,0` | description: monthly price of churned customers
```dax
Lost Monthly Revenue =
CALCULATE ( SUM ( FactCustomers[monthly_price_usd] ), FactCustomers[is_churned] = "Yes" )
```

**At Risk Customers** | format `#,0` | description: active customers with low viewing and long inactivity
```dax
At Risk Customers =
VAR MinHours = [Low Engagement Threshold Hours]
VAR MinDays = [Inactivity Threshold Days]
RETURN
    CALCULATE (
        [Total Customers],
        FactCustomers[is_churned] = "No",
        FactCustomers[avg_weekly_hours] < MinHours,
        FactCustomers[days_since_last_login] >= MinDays
    )
```

**Revenue At Risk** | format `$#,0` | description: monthly revenue from at-risk customers
```dax
Revenue At Risk =
VAR MinHours = [Low Engagement Threshold Hours]
VAR MinDays = [Inactivity Threshold Days]
RETURN
    CALCULATE (
        SUM ( FactCustomers[monthly_price_usd] ),
        FactCustomers[is_churned] = "No",
        FactCustomers[avg_weekly_hours] < MinHours,
        FactCustomers[days_since_last_login] >= MinDays
    )
```

**At Risk Share %** | format `0.0%`
```dax
At Risk Share % = DIVIDE ( [At Risk Customers], [Active Customers] )
```

---

## Table: FactMonthlyMetrics

### Folder: Subscribers

**Subscribers M** | format `#,0.0` | description: closing subscribers (millions) at the last month in the current filter
```dax
Subscribers M =
VAR LastMonth = MAX ( FactMonthlyMetrics[month] )
RETURN
    CALCULATE (
        SUM ( FactMonthlyMetrics[closing_subscribers_m] ),
        FactMonthlyMetrics[month] = LastMonth
    )
```

**Gross Adds M** | format `#,0.0`
```dax
Gross Adds M = SUM ( FactMonthlyMetrics[gross_adds_m] )
```

**Churned Subscribers M** | format `#,0.0`
```dax
Churned Subscribers M = SUM ( FactMonthlyMetrics[churned_subscribers_m] )
```

**Net Adds M** | format `#,0.0;-#,0.0`
```dax
Net Adds M = [Gross Adds M] - [Churned Subscribers M]
```

**Average Monthly Churn %** | format `0.00%` | description: churned subscribers divided by opening subscribers over the selected months
```dax
Average Monthly Churn % =
DIVIDE (
    SUM ( FactMonthlyMetrics[churned_subscribers_m] ),
    SUM ( FactMonthlyMetrics[opening_subscribers_m] )
)
```

### Folder: Revenue

**Revenue USD M** | format `$#,0` 
```dax
Revenue USD M = SUM ( FactMonthlyMetrics[revenue_usd_m] )
```

**Revenue USD M PY** | format `$#,0` | description: same period last year
```dax
Revenue USD M PY =
CALCULATE ( [Revenue USD M], SAMEPERIODLASTYEAR ( DimDate[Date] ) )
```

**Revenue YoY %** | format `0.0%;-0.0%`
```dax
Revenue YoY % =
VAR Prior = [Revenue USD M PY]
RETURN
    IF ( NOT ISBLANK ( Prior ), DIVIDE ( [Revenue USD M] - Prior, Prior ) )
```

**Revenue YTD USD M** | format `$#,0`
```dax
Revenue YTD USD M = TOTALYTD ( [Revenue USD M], DimDate[Date] )
```

**Average Revenue Per Member** | format `$#,0.00` | description: average monthly ARM across the selection
```dax
Average Revenue Per Member = AVERAGE ( FactMonthlyMetrics[arm_usd] )
```

### Folder: Spend

**Content Spend USD M** | format `$#,0`
```dax
Content Spend USD M = SUM ( FactMonthlyMetrics[content_spend_usd_m] )
```

**Marketing Spend USD M** | format `$#,0`
```dax
Marketing Spend USD M = SUM ( FactMonthlyMetrics[marketing_spend_usd_m] )
```

**Content Spend % Of Revenue** | format `0.0%`
```dax
Content Spend % Of Revenue = DIVIDE ( [Content Spend USD M], [Revenue USD M] )
```

**Marketing Cost Per Gross Add** | format `$#,0.00` | description: marketing spend (USD M) per gross add (M) gives USD per subscriber
```dax
Marketing Cost Per Gross Add = DIVIDE ( [Marketing Spend USD M], [Gross Adds M] )
```

**Originals Released** | format `#,0`
```dax
Originals Released = SUM ( FactMonthlyMetrics[new_originals_released] )
```

---

## Table: FactTitles

### Folder: Catalogue

**Total Titles** | format `#,0`
```dax
Total Titles = DISTINCTCOUNT ( FactTitles[show_id] )
```

**Original Titles** | format `#,0`
```dax
Original Titles =
CALCULATE ( [Total Titles], FactTitles[is_netflix_original] = "Yes" )
```

**Original Share %** | format `0.0%`
```dax
Original Share % = DIVIDE ( [Original Titles], [Total Titles] )
```

**Top 10 Titles** | format `#,0` | description: titles with at least one week in the Top 10
```dax
Top 10 Titles =
CALCULATE ( [Total Titles], FactTitles[weeks_in_top10] > 0 )
```

### Folder: Performance

**Total Views M** | format `#,0.0`
```dax
Total Views M = SUM ( FactTitles[views_28d_m] )
```

**Total Hours Viewed M** | format `#,0.0`
```dax
Total Hours Viewed M = SUM ( FactTitles[hours_viewed_28d_m] )
```

**Average IMDb Score** | format `0.0`
```dax
Average IMDb Score = AVERAGE ( FactTitles[imdb_score] )
```

**Average Completion Rate %** | format `0.0` | description: value is already a percentage number (0-100)
```dax
Average Completion Rate % = AVERAGE ( FactTitles[completion_rate_pct] )
```

**Total Budget USD M** | format `$#,0.0`
```dax
Total Budget USD M = SUM ( FactTitles[budget_usd_m] )
```

**Views Per Budget Dollar** | format `0.00` | description: views (M) per USD M of budget, a cost efficiency measure
```dax
Views Per Budget Dollar = DIVIDE ( [Total Views M], [Total Budget USD M] )
```

---

## After creating the measures

1. List all measures with table, folder and format string.
2. Evaluate each measure with no filters and show the values.
3. Flag any measure that returns blank, an error, or a value that looks wrong.
Expected sanity checks: Total Customers = 5,000; Churn Rate % about 28%; Subscribers M about 357;
Total Titles = 1,200.
