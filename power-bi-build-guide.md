# Power BI Build Guide — Industrial Energy Monitoring Dashboard

This guide explains how to build the equivalent of the Python reference dashboard in Power BI Desktop.

## Prerequisites

- Power BI Desktop (Windows, free download from Microsoft)
- CSV exports in the schema defined in `data/data-dictionary.md`

## Step 1 — Import Data

1. Open Power BI Desktop.
2. Click **Get Data → Text/CSV**.
3. Select all CSV files in `data/raw/` and click **Combine**.
4. In the Power Query editor, verify column types:
   - `timestamp`: DateTime
   - `kwh_accumulated`: Decimal Number
   - `instantaneous_kw`: Decimal Number
5. Click **Close & Apply**.

## Step 2 — Create Calculated Columns

In the data view, add these calculated columns to the readings table:

```dax
Date = DATEVALUE(FORMAT([timestamp], "yyyy-MM-dd"))
Week = WEEKNUM([timestamp], 2)   // ISO week
Month = FORMAT([timestamp], "yyyy-MM")
Hour = HOUR([timestamp])
```

## Step 3 — Create Measures

```dax
Total kWh = SUM(readings[kwh_accumulated])  // not the right aggregation; see below
```

For correct kWh calculation, use:

```dax
Daily kWh =
VAR first_reading = MIN(readings[kwh_accumulated])
VAR last_reading = MAX(readings[kwh_accumulated])
RETURN last_reading - first_reading

Peak kW = MAX(readings[instantaneous_kw])

Avg kW = AVERAGE(readings[instantaneous_kw])

Load Factor = DIVIDE([Avg kW], [Peak kW], 0)
```

## Step 4 — Build Visualisations

### Line chart — daily consumption trend
- X-axis: `Date`
- Y-axis: `[Daily kWh]`
- Legend: `meter_id`

### Bar chart — monthly peak demand
- X-axis: `Month`
- Y-axis: `[Peak kW]`
- Legend: `meter_id`

### Bar chart — monthly load factor
- X-axis: `Month`
- Y-axis: `[Load Factor]`
- Legend: `meter_id`

## Step 5 — Publish

1. Save the .pbix file.
2. (Optional) Click **Publish** to push to a Power BI workspace.

## Notes

- Power BI Desktop is Windows-only. On macOS or Linux, use the Python reference implementation instead.
- The .pbix file is not included in this repository; the user must build it following this guide.
- Anomaly detection in Power BI requires DAX or R/Python visual; the Python reference implementation is preferred for anomaly detection.
