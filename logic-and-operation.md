# Logic and Operation — Industrial Energy Monitoring Dashboard

## Aggregation Logic

For each meter, the aggregator groups readings by day, week (ISO week), and month:

- **Daily:** sum of kWh readings in the day. Peak demand = max instantaneous kW reading in the day.
- **Weekly:** sum of daily kWh. Peak demand = max daily peak.
- **Monthly:** sum of daily kWh. Peak demand = max daily peak.
- **Load factor:** average demand / peak demand, over the period.

## Anomaly Detection

For each meter, the aggregator computes the historical mean and standard deviation of daily kWh. Any day where the daily kWh deviates more than 3 standard deviations from the historical mean is flagged as an anomaly and listed in `data/anomalies.csv`.

## Output Files

- `data/aggregated/daily-summary.csv` — one row per meter per day.
- `data/aggregated/weekly-summary.csv` — one row per meter per week.
- `data/aggregated/monthly-summary.csv` — one row per meter per month.
- `data/aggregated/peak-demand.csv` — one row per meter per period.
- `data/aggregated/load-factor.csv` — one row per meter per period.
- `data/aggregated/anomalies.csv` — one row per anomaly.
- `data/charts/consumption-trend.png` — line chart of daily kWh per meter.
- `data/charts/peak-demand.png` — bar chart of monthly peak demand per meter.
- `data/charts/load-factor.png` — bar chart of monthly load factor per meter.
- `data/summary-report.md` — human-readable summary.
