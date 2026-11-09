# Netflix AI Dashboard (Power BI)

> Replace this text with a 2-3 sentence summary: the business question,
> the data, and the main finding.

## Business question
Which customers are likely to leave, why, and how is the business trending by region?

## Data
Three **synthetic** datasets (see `data/README.md`): customer churn, monthly regional metrics, titles catalogue.

## Approach
1. Loaded CSVs into Power BI and cleaned them in Power Query.
2. Designed a star schema (3 fact tables, 5 dimensions). See `docs/star-schema.md`.
3. Built DAX measures. See `docs/measures.md`.
4. Used GitHub Copilot with the Power BI Modeling MCP to accelerate modeling and audits. See `docs/prompt-log.md`.
5. Added AI features: Key Influencers, Decomposition Tree, Smart Narrative, forecasting, anomaly detection, sentiment scoring.
6. Audited performance. See `docs/performance-audit.md`.

## Key insights
- (add 3-5 findings with screenshots)

## Screenshots
(add images from docs/screenshots)

## Live report
(add Publish to web link; synthetic data only)

## Tools
Power BI Desktop, DAX, Power Query, GitHub Copilot, Power BI Modeling MCP, Python (VADER), Git

## What AI got wrong
See `docs/ai-mistakes-and-fixes.md`.
