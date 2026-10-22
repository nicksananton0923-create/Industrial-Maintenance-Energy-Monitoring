#!/usr/bin/env python3
"""
Industrial Energy Monitoring Dashboard — reference implementation.

Reads CSV meter readings from data/raw/, validates against the schema in
data/data-dictionary.md, aggregates by day/week/month, and produces
charts and summary CSVs.

Status: IMPLEMENTED
Tested: NOT YET TESTED on real plant data (only on the fictional sample).

Usage:
    python generate_dashboard.py [--raw-dir DATA/RAW] [--out-dir DATA/AGGREGATED]
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

try:
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError as e:
    print(f"ERROR: missing dependency: {e}", file=sys.stderr)
    print("Install with: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)


REQUIRED_COLUMNS = [
    "meter_id", "plant_area", "feeder", "timestamp",
    "kwh_accumulated", "instantaneous_kw", "reading_quality",
]
OPTIONAL_COLUMNS = ["voltage_v", "current_a", "power_factor"]
ALLOWED_QUALITY = {"good", "estimated", "missing"}


def validate_schema(df):
    """Validate a DataFrame against the schema. Returns (valid_df, rejected_df)."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    df["kwh_accumulated"] = pd.to_numeric(df["kwh_accumulated"], errors="coerce")
    df["instantaneous_kw"] = pd.to_numeric(df["instantaneous_kw"], errors="coerce")

    rejected = df[df["timestamp"].isna() | df["kwh_accumulated"].isna() | df["instantaneous_kw"].isna()].copy()
    valid = df.drop(rejected.index).copy()

    valid_quality_mask = valid["reading_quality"].isin(ALLOWED_QUALITY)
    rejected = pd.concat([rejected, valid[~valid_quality_mask]])
    valid = valid[valid_quality_mask]

    return valid, rejected


def aggregate(df, period):
    """Aggregate by meter and period."""
    df = df.copy()
    df[period] = df["timestamp"].dt.to_period(period)
    grouped = df.groupby(["meter_id", "plant_area", "feeder", period])
    summary = grouped.agg(
        kwh_total=("kwh_accumulated", lambda x: x.iloc[-1] - x.iloc[0]),
        peak_kw=("instantaneous_kw", "max"),
        avg_kw=("instantaneous_kw", "mean"),
        reading_count=("timestamp", "count"),
    ).reset_index()
    summary["load_factor"] = summary["avg_kw"] / summary["peak_kw"]
    summary[period] = summary[period].astype(str)
    return summary


def detect_anomalies(daily):
    """Flag daily readings that deviate >3 sigma from the meter's historical mean."""
    anomalies = []
    for meter_id, group in daily.groupby("meter_id"):
        mean = group["kwh_total"].mean()
        std = group["kwh_total"].std()
        if std == 0 or pd.isna(std):
            continue
        threshold = 3 * std
        mask = (group["kwh_total"] - mean).abs() > threshold
        for _, row in group[mask].iterrows():
            anomalies.append({
                "meter_id": meter_id,
                "date": row["D"],
                "kwh_total": row["kwh_total"],
                "mean": mean,
                "std": std,
                "deviation_sigma": abs(row["kwh_total"] - mean) / std,
            })
    return pd.DataFrame(anomalies)


def plot_consumption_trend(daily, out_path):
    fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
    for meter_id, group in daily.groupby("meter_id"):
        ax.plot(group["D"], group["kwh_total"], marker="o", label=meter_id)
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily kWh")
    ax.set_title("Daily Energy Consumption Trend")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def plot_peak_demand(monthly, out_path):
    fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
    pivot = monthly.pivot(index="M", columns="meter_id", values="peak_kw")
    pivot.plot(kind="bar", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Peak kW")
    ax.set_title("Monthly Peak Demand")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def plot_load_factor(monthly, out_path):
    fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
    pivot = monthly.pivot(index="M", columns="meter_id", values="load_factor")
    pivot.plot(kind="bar", ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Load Factor")
    ax.set_title("Monthly Load Factor")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def write_summary_report(daily, monthly, anomalies, out_path):
    lines = [
        "# Energy Monitoring Summary Report",
        "",
        f"Generated: {datetime.utcnow().isoformat()}Z",
        "",
        "## Daily Aggregation Summary",
        "",
        f"- Total meters: {daily['meter_id'].nunique()}",
        f"- Total days: {daily['D'].nunique()}",
        f"- Total consumption (all meters): {daily['kwh_total'].sum():.2f} kWh",
        "",
        "## Monthly Aggregation Summary",
        "",
        f"- Total months: {monthly['M'].nunique()}",
        "",
        "## Anomalies Detected",
        "",
        f"- Count: {len(anomalies)}",
        "",
        "## Per-Meter Summary",
        "",
        "| Meter | Plant Area | Total kWh | Peak kW | Load Factor |",
        "|---|---|---|---|---|",
    ]
    for _, row in monthly.groupby("meter_id").agg(
        kwh_total=("kwh_total", "sum"),
        peak_kw=("peak_kw", "max"),
        load_factor=("load_factor", "mean"),
        plant_area=("plant_area", "first"),
    ).reset_index().iterrows():
        lines.append(f"| {row['meter_id']} | {row['plant_area']} | {row['kwh_total']:.2f} | {row['peak_kw']:.2f} | {row['load_factor']:.3f} |")
    Path(out_path).write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Industrial energy monitoring dashboard")
    parser.add_argument("--raw-dir", default="data/raw", help="Directory of raw CSV files")
    parser.add_argument("--out-dir", default="data/aggregated", help="Directory for aggregated output")
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    charts_dir = out_dir.parent / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(raw_dir.glob("*.csv"))
    if not csv_files:
        print(f"ERROR: no CSV files found in {raw_dir}", file=sys.stderr)
        sys.exit(1)

    frames = []
    for f in csv_files:
        print(f"Reading {f.name}...")
        df = pd.read_csv(f)
        frames.append(df)
    raw = pd.concat(frames, ignore_index=True)

    valid, rejected = validate_schema(raw)
    if not rejected.empty:
        rejected.to_csv(out_dir / "rejected-readings.csv", index=False)
        print(f"Rejected {len(rejected)} rows.")

    daily = aggregate(valid, "D")
    weekly = aggregate(valid, "W")
    monthly = aggregate(valid, "M")
    anomalies = detect_anomalies(daily)

    daily.to_csv(out_dir / "daily-summary.csv", index=False)
    weekly.to_csv(out_dir / "weekly-summary.csv", index=False)
    monthly.to_csv(out_dir / "monthly-summary.csv", index=False)
    if not anomalies.empty:
        anomalies.to_csv(out_dir / "anomalies.csv", index=False)

    plot_consumption_trend(daily, charts_dir / "consumption-trend.png")
    plot_peak_demand(monthly, charts_dir / "peak-demand.png")
    plot_load_factor(monthly, charts_dir / "load-factor.png")

    write_summary_report(daily, monthly, anomalies, out_dir.parent / "summary-report.md")

    print(f"Done. Outputs written to {out_dir} and {charts_dir}.")


if __name__ == "__main__":
    main()
