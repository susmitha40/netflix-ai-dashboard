# Report blueprint (5 pages)

Theme: dark background (#141414), accent red (#E50914), text white/grey. Font: Segoe UI.
Every page: title top-left, slicer strip on top (Year, Region), page navigation buttons.
Use only measures from measures.md.

## Page 1: Executive Overview
| Visual | Fields |
|---|---|
| KPI cards (6) | Subscribers M, Revenue USD M, Revenue YoY %, Total Customers, Churn Rate %, Revenue At Risk |
| Line chart | Axis: DimDate Month. Values: Revenue USD M, legend DimRegion[region] |
| Clustered column | Axis: DimRegion[region]. Values: Subscribers M |
| Smart Narrative | Linked to the line chart |
| Slicers | DimDate Year, DimRegion[region] |

## Page 2: Why Customers Churn (AI page)
| Visual | Fields |
|---|---|
| Key Influencers | Analyze: FactCustomers[is_churned] = Yes. Explain by: plan, payment_method, primary_device, avg_weekly_hours, days_since_last_login, support_tickets_90d, joined_via_promo, profiles_count |
| Decomposition Tree | Analyze: Churned Customers. Explain by: plan, region, favorite_genre, churn_reason |
| Bar chart | Axis: churn_reason. Values: Churned Customers |
| KPI cards | Churn Rate %, Retention Rate %, Average Tenure Months, Lost Monthly Revenue |

## Page 3: Forecast and Anomalies
| Visual | Fields |
|---|---|
| Line chart + Forecast | Axis: DimDate Month. Values: Subscribers M. Analytics pane: Forecast 12 months, 95% confidence |
| Line chart + Anomaly detection | Axis: DimDate Month. Values: Average Monthly Churn %. Analytics pane: Find anomalies |
| Line chart | Net Adds M by month |
| Matrix | Rows: region. Values: Revenue USD M, Revenue YoY %, Average Revenue Per Member |

## Page 4: Customer Risk and Sentiment
| Visual | Fields |
|---|---|
| KPI cards | At Risk Customers, At Risk Share %, Revenue At Risk |
| Scatter | X: Average Weekly Hours. Y: Churn Rate %. Details: plan |
| Stacked bar | Axis: sentiment_label. Values: customers. Legend: is_churned (needs sentiment file loaded) |
| Table | customer_id, plan, avg_weekly_hours, days_since_last_login, Revenue At Risk, filtered to at-risk customers |

Sentiment: run scripts/sentiment_scoring.py, load data/processed/customer_sentiment.csv,
and merge it into FactCustomers in Power Query on customer_id (simplest, avoids another relationship).

## Page 5: Content Performance
| Visual | Fields |
|---|---|
| KPI cards | Total Titles, Original Share %, Total Views M, Average IMDb Score |
| Scatter | X: Total Budget USD M. Y: Total Views M. Details: genre. Size: Total Titles |
| Bar chart | Axis: genre. Values: Views Per Budget Dollar |
| Clustered column | Axis: DimDate Year (date_added). Values: Total Titles, Original Titles |
| Table | Top 10 titles by Total Views M |
