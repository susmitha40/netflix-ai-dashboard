# Proposed star schema

Implemented in the open `NetflixDashboard` Power BI Desktop model on 2026-11-09. The CSV datasets and their values are synthetic, not real Netflix data.

## Tables and column disposition

The three imported tables were renamed to the PascalCase fact names below. All listed source columns are kept. Fact keys and IDs are hidden from report view; hiding does not mean deleting them.

| Proposed table | Grain | Keep | Drop |
|---|---|---|---|
| **FactCustomers** (renamed from `netflix_customer_churn_synthetic`) | One row per customer (5,000 rows; `customer_id` is unique) | `customer_id`, `signup_date`, `country`, `region`, `age`, `gender`, `plan`, `monthly_price_usd`, `payment_method`, `primary_device`, `profiles_count`, `joined_via_promo`, `favorite_genre`, `avg_weekly_hours`, `titles_watched_30d`, `days_since_last_login`, `support_tickets_90d`, `satisfaction_score`, `tenure_months`, `is_churned`, `churn_date`, `churn_reason`, `feedback_text` | None |
| **FactMonthlyMetrics** (renamed from `netflix_monthly_region_metrics_synthetic`) | One row per region and month (192 rows; `(month, region)` is unique) | `month`, `region`, `opening_subscribers_m`, `gross_adds_m`, `churned_subscribers_m`, `closing_subscribers_m`, `monthly_churn_rate_pct`, `arm_usd`, `revenue_usd_m`, `marketing_spend_usd_m`, `content_spend_usd_m`, `new_originals_released` | None |
| **FactTitles** (renamed from `netflix_titles_synthetic`) | One row per title (`show_id`; 1,200 rows and IDs are unique) | `show_id`, `title`, `type`, `genre`, `country`, `language`, `release_year`, `date_added`, `maturity_rating`, `duration_min`, `seasons`, `is_netflix_original`, `imdb_score`, `budget_usd_m`, `views_28d_m`, `hours_viewed_28d_m`, `completion_rate_pct`, `weeks_in_top10` | None |
| **DimDate** | One row per calendar date | `Date` (calendar date key spanning all three facts) | None |
| **DimCountry** | One row per distinct country value | `country` | None |
| **DimRegion** | One row per distinct region value | `region` | None |
| **DimGenre** | One row per distinct genre value | `genre` | None |
| **DimPlan** | One row per distinct plan | `plan` | None |

`monthly_price_usd` stays in **FactCustomers**, not **DimPlan**: the live model has three distinct prices for each of its three plan values. `FactCustomers[region]` is retained as a hidden region key. `DimCountry` has 16 values, including the blank country value present in the titles fact.

The imported tables also contain a generated hidden `RowNumber-2662979B-1795-4F74-8F37-6A1BA8059B61` model column, which is not a source CSV column; it remains hidden. The four generated `LocalDateTable_*` objects and their date variations/relationships were removed when replacing them with `DimDate`. Power BI's hidden private `DateTableTemplate_6e561017-a5a3-4d9a-8755-054eea61365e` remains as an internal template and is not part of the business schema.

### Hide in report view

- **FactCustomers:** `customer_id`, `country`, `region`, `plan`, `favorite_genre`, `signup_date`, `churn_date`.
- **FactMonthlyMetrics:** `region`, `month`.
- **FactTitles:** `show_id`, `country`, `genre`, `date_added`.
- **Dimensions:** keep their descriptive key columns available for slicers and report use. `DimDate[Date]` remains available for date selection.

## Relationships

Every relationship is one-to-many, single-direction from dimension (one) to fact (many). Do not create fact-to-fact or dimension-to-dimension relationships.

| One side | Many side | Active? |
|---|---|---|
| `DimDate[Date]` | `FactCustomers[signup_date]` | Yes |
| `DimDate[Date]` | `FactCustomers[churn_date]` | **No (inactive)** |
| `DimDate[Date]` | `FactMonthlyMetrics[month]` | Yes |
| `DimDate[Date]` | `FactTitles[date_added]` | Yes |
| `DimCountry[country]` | `FactCustomers[country]` | Yes |
| `DimCountry[country]` | `FactTitles[country]` | Yes |
| `DimRegion[region]` | `FactCustomers[region]` | Yes |
| `DimRegion[region]` | `FactMonthlyMetrics[region]` | Yes |
| `DimGenre[genre]` | `FactCustomers[favorite_genre]` | Yes |
| `DimGenre[genre]` | `FactTitles[genre]` | Yes |
| `DimPlan[plan]` | `FactCustomers[plan]` | Yes |

`FactMonthlyMetrics[month]` is typed as `date` in its Power Query partition; all 192 values were verified to be the first day of the month. Its model display format is `MMM yyyy`. `DimDate` is marked as the model's date table and contains 3,642 unique dates from 2016-01-11 through 2025-12-30, covering all three facts.

The previous four active relationships to separate hidden local date tables, including the active local `churn_date` relationship, were removed. The shared `DimDate` relationship to `FactCustomers[churn_date]` is inactive; the signup-date, monthly-metrics, and titles date relationships are active. All relationships are one-to-many, single-direction from dimensions to facts. DAX checks confirmed the country, genre, plan, region, date, and inactive churn-date relationships filter the expected facts.
