# Industrial Energy Monitoring Dashboard

## Table of Contents
1. [Project Purpose](#1-project-purpose)
2. [Problem Statement](#2-problem-statement)
3. [Project Objectives](#3-project-objectives)
4. [Current Project Status](#4-current-project-status)
5. [Confirmed Technologies and Components](#5-confirmed-technologies-and-components)
6. [Proposed Components](#6-proposed-components)
7. [System Operation](#7-system-operation)
8. [Architecture or Workflow](#8-architecture-or-workflow)
9. [Installation or Setup Instructions](#9-installation-or-setup-instructions)
10. [Testing Status](#10-testing-status)
11. [Safety Considerations](#11-safety-considerations)
12. [Known Limitations](#12-known-limitations)
13. [Future Improvements](#13-future-improvements)
14. [Repository Structure](#14-repository-structure)
15. [Licence Information](#15-licence-information)
16. [Status Label Convention](#16-status-label-convention)

## 1. Project Purpose

This project provides a dashboard framework for monitoring industrial electrical energy consumption across multiple plant areas, feeders, and equipment groups. The dashboard supports daily, weekly, and monthly aggregation; peak demand tracking; load factor calculation; and anomaly flagging. The package includes CSV templates for data ingest, a Python reference implementation for aggregation and visualisation, and a sample dataset of fictional readings. The dashboard is designed to be portable across vendors: it does not assume any specific meter vendor or BMS protocol, and accepts data in a simple CSV format that any meter or data logger can export to.

## 2. Problem Statement

Industrial facilities typically have multiple electricity meters distributed across plant areas, feeders, and equipment groups. Each meter's data is often accessible only through a vendor-specific tool or a BMS front-end, making cross-meter analysis difficult. Plant engineers who want to track total consumption, identify high-consumption periods, calculate load factor, and compare month-over-month performance often end up exporting data manually into Excel and building ad-hoc charts that are not reusable. A simple, vendor-neutral dashboard framework that accepts CSV exports from any meter and produces consistent, reusable analysis reduces this burden and makes energy management more accessible to plant personnel without a dedicated energy-management software budget.

## 3. Project Objectives

- Provide a vendor-neutral CSV schema for industrial energy meter readings.
- Provide a Python reference implementation for daily/weekly/monthly aggregation.
- Calculate load factor, peak demand, and consumption trends.
- Flag readings that deviate significantly from historical patterns.
- Provide a sample dataset of fictional readings for demonstration.
- Provide a Power BI build guide as an alternative to the Python reference.
- Clearly label all data as FICTIONAL and document the data dictionary.

## 4. Current Project Status

| Item | Status |
|---|---|
| CSV templates | IMPLEMENTED |
| Python reference implementation | IMPLEMENTED (compiles, not deployed) |
| Sample dataset (fictional) | IMPLEMENTED |
| Power BI build guide | IMPLEMENTED (instructions; no .pbix file) |
| Deployment in a real plant | NOT VERIFIED |
| Live data integration | NOT YET TESTED |

## 5. Confirmed Technologies and Components

The following technologies are confirmed because they are implemented in this package:

- Python 3.8+ with pandas, matplotlib (in `requirements.txt`)
- CSV data format (vendor-neutral)
- Markdown documentation

No specific meter vendor, BMS protocol, or cloud platform is assumed. The dashboard is designed to accept data from any source that can export to the defined CSV schema.

## 6. Proposed Components

| Component | Role | Notes |
|---|---|---|
| Energy meters with CSV export | Data source | Vendor-neutral |
| Data logger / BMS with CSV export | Alternative data source | Optional |
| Python 3.8+ runtime | Reference implementation | Cross-platform |
| Power BI Desktop | Alternative visualisation | Optional, Windows only |
| Schedule task / cron | Periodic refresh | Optional |

## 7. System Operation

The dashboard operates in three stages: ingest, aggregate, and visualise. In the ingest stage, raw meter readings are exported from each meter or data logger in the defined CSV schema and placed in a single directory. In the aggregate stage, the Python reference implementation reads all CSV files in the directory, validates them against the schema, and produces daily, weekly, and monthly aggregations per meter and per plant area. In the visualise stage, the Python implementation produces a set of matplotlib charts (consumption trend, peak demand, load factor, anomaly flags) and writes them to PNG files. The Power BI build guide provides an alternative visualisation path using Power BI Desktop.

## 8. Architecture or Workflow

The system architecture is intentionally minimal and file-based, to avoid introducing a database dependency for portfolio demonstration. A production deployment would typically replace the file-based ingest with a database or a time-series data store.

```
[Energy meters] --> CSV export --> [data/raw/*.csv]
                                        |
                                        v
                            [Python aggregator]
                                        |
                                        v
                            [data/aggregated/*.csv]
                                        |
                                        v
                       [matplotlib charts / Power BI]
```

The Python aggregator reads from `data/raw/`, validates each CSV against the schema in `data/data-dictionary.md`, and writes aggregated outputs to `data/aggregated/`. The aggregator is idempotent: running it twice on the same input produces the same output.

## 9. Installation or Setup Instructions

Python reference implementation:

1. Install Python 3.8 or later.
2. Install dependencies: `pip install -r requirements.txt`.
3. Place raw meter CSV exports in `data/raw/`.
4. Run `python generate_dashboard.py`.
5. Inspect outputs in `data/aggregated/` and `data/charts/`.

Power BI alternative:

1. Install Power BI Desktop (Windows only, free).
2. Follow `dashboard/power-bi-build-guide.md`.
3. Import the raw CSVs and build the visualisations per the guide.

## 10. Testing Status

All tests are currently **NOT YET TESTED** on a real deployment. The Python reference implementation has been syntax-checked (`python -m py_compile`) but has not been deployed against a real plant's meter data. Tests to be performed before any deployment:

1. Python `py_compile` syntax check — performed, passes.
2. Run against the fictional sample dataset — performed (chart generation).
3. Validate CSV schema enforcement — performed on the sample dataset.
4. Run against real plant data — NOT YET TESTED.
5. Compare dashboard totals against meter front-end totals — NOT YET TESTED.

## 11. Safety Considerations

This project does not involve any hardware safety considerations because it is a pure data analysis tool. However, the following operational safety notes apply:

- **Do not make operational decisions based on unvalidated data.** The dashboard is a visualisation tool, not a billing system. Confirm any surprising result against the meter's own front-end before acting on it.
- **Do not expose the dashboard to the public internet without authentication.** Energy consumption data is commercially sensitive.
- **Do not include personally identifiable information in the data.** Energy data is typically at the meter level, not the individual level, but verify before sharing.
- **Back up raw data before aggregation.** The aggregator is read-only on raw data, but backups protect against accidental deletion.
- **Anonymise data before sharing outside the organisation.** Replace plant names with generic identifiers if sharing with external consultants.

## 12. Known Limitations

- The Python reference implementation is single-threaded and may be slow for very large datasets (millions of rows). For production scale, consider a database-backed implementation.
- The dashboard does not include tariff calculations. Energy cost is not computed; only energy consumption (kWh) is aggregated.
- The dashboard does not include power quality metrics (voltage, current, power factor, harmonics). Only energy consumption is in scope.
- Anomaly detection is based on a simple standard-deviation threshold; it does not use machine learning and may produce false positives or miss subtle anomalies.
- The Power BI build guide provides instructions but no .pbix file. The user must build the Power BI report manually following the guide.
- No real-time data ingest. The dashboard operates on batch CSV exports.

## 13. Future Improvements

- Add a database backend (e.g. InfluxDB or TimescaleDB) for production scale.
- Add real-time data ingest via MQTT or Modbus polling.
- Add tariff calculations (time-of-use, demand charges).
- Add power quality metrics (voltage, current, power factor).
- Add machine-learning-based anomaly detection.
- Add a web front-end (e.g. Grafana) for interactive exploration.
- Add automated report generation (PDF weekly / monthly reports).

## 14. Repository Structure

```
08-industrial-energy-monitoring-dashboard/
├── README.md
├── LICENSE
├── requirements.txt
├── docs/
│   ├── project-overview.md
│   ├── requirements.md
│   ├── system-architecture.md
│   ├── logic-and-operation.md
│   ├── components-and-bill-of-materials.md
│   ├── testing-and-validation.md
│   ├── safety-considerations.md
│   ├── development-roadmap.md
│   └── limitations.md
├── data/
│   ├── data-dictionary.md
│   ├── raw/
│   │   └── sample-meter-readings.csv
│   └── aggregated/
│       └── (generated by generate_dashboard.py)
├── dashboard/
│   └── power-bi-build-guide.md
├── templates/
│   └── meter-reading-template.csv
└── generate_dashboard.py
```

## 15. Licence Information

Released under the MIT Licence. See the `LICENSE` file for the full text.

## 16. Status Label Convention

This project uses the following status labels throughout its documentation. Each label has a strict meaning and is not used interchangeably with any other label.

| Label | Meaning |
|---|---|
| **CONFIRMED** | Directly supported by available project information or inspected source code. |
| **PROPOSED** | A suggested design or implementation. Has not been verified against built hardware. |
| **NOT VERIFIED** | Information that has not been confirmed. Requires verification before use. |
| **IMPLEMENTED** | A feature or system that has actually been created and exists in the source code. |
| **TESTED** | A test that has genuinely been performed with recorded results. |
| **NOT YET TESTED** | Code, hardware, or functionality that still requires testing. |

If a section does not carry any status label, the content of that section is informational prose and does not make a claim of verification, testing, or implementation.

## Data and Confidentiality Notice

All sample data in this repository is **FICTIONAL**. Plant names use generic identifiers such as "Plant A", "Building 3", "Line 2", or "Western Plant". No real employer name, real equipment serial number, real employee name, real maintenance record, or any other confidential information is included. Templates are provided as reusable CSV schemas that can be populated with real site data by the adopting organisation. The fictional data is intended solely to demonstrate the template structure and calculation methodology.
