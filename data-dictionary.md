# Data Dictionary — Industrial Energy Monitoring Dashboard

## CSV Schema: meter readings

Each row represents one meter reading at one timestamp. The aggregator expects the following columns:

| Column | Type | Unit | Description | Required |
|---|---|---|---|---|
| meter_id | string | — | Unique meter identifier (e.g. MTR-001) | Yes |
| plant_area | string | — | Plant area name (e.g. Building-3) | Yes |
| feeder | string | — | Feeder / circuit identifier | Yes |
| timestamp | ISO 8601 | — | Reading timestamp, UTC | Yes |
| kwh_accumulated | float | kWh | Total accumulated kWh at this reading | Yes |
| instantaneous_kw | float | kW | Instantaneous power at this reading | Yes |
| voltage_v | float | V | Line voltage at reading | No |
| current_a | float | A | Line current at reading | No |
| power_factor | float | — | Power factor (0–1) | No |
| reading_quality | string | — | "good" / "estimated" / "missing" | Yes |

## Validation Rules

- All required columns must be present.
- `timestamp` must be parseable as ISO 8601.
- `kwh_accumulated` must be non-negative and monotonically increasing per meter.
- `instantaneous_kw` must be non-negative.
- `reading_quality` must be one of the three allowed values.

Rows that fail validation are written to `data/aggregated/rejected-readings.csv` and excluded from aggregation.
