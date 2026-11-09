# Star schema

| Table | Type | Grain | Key columns |
|---|---|---|---|
| FactCustomers | Fact | customer | customer_id, signup_date, churn_date, country, favorite_genre, plan |
| FactMonthlyMetrics | Fact | region x month | month, region |
| FactTitles | Fact | title | show_id, date_added, country, genre |
| DimDate | Dim | day | Date |
| DimCountry | Dim | country | country, region |
| DimRegion | Dim | region | region |
| DimGenre | Dim | genre | genre |
| DimPlan | Dim | plan | plan, monthly_price_usd |

## Relationships (dimension -> fact, one-to-many, single direction)
- DimDate[Date] -> FactCustomers[signup_date] (active)
- DimDate[Date] -> FactCustomers[churn_date] (inactive)
- DimDate[Date] -> FactTitles[date_added]
- DimDate[Date] -> FactMonthlyMetrics[month]
- DimRegion -> DimCountry, FactMonthlyMetrics
- DimCountry -> FactCustomers, FactTitles
- DimGenre -> FactTitles, FactCustomers[favorite_genre]
- DimPlan -> FactCustomers

## Screenshot
![Model view](screenshots/model-view.png)
