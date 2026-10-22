# System Architecture — Industrial Energy Monitoring Dashboard

## Data Flow

```
[Energy meters] --> CSV export --> data/raw/*.csv
                                      |
                                      v
                          [generate_dashboard.py]
                                      |
                                      v
                          data/aggregated/*.csv
                          data/charts/*.png
                          data/summary-report.md
```

## Components

- **CSV schema:** defined in `data/data-dictionary.md`. Each row represents one meter reading at one timestamp.
- **Python aggregator:** `generate_dashboard.py`. Reads all CSVs in `data/raw/`, validates, aggregates, produces outputs.
- **Templates:** `templates/meter-reading-template.csv`. Empty schema with header row only.
- **Power BI guide:** `dashboard/power-bi-build-guide.md`. Step-by-step instructions for building the equivalent report in Power BI Desktop.
