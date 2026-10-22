# Limitations — Industrial Energy Monitoring Dashboard

- Single-threaded Python implementation; may be slow for very large datasets.
- No tariff or cost calculations.
- No power quality metrics (voltage, current, power factor, harmonics).
- Anomaly detection is rule-based (3-sigma), not ML-based.
- No real-time monitoring; batch-only.
- No database backend; file-based only.
- No authentication or access control on the outputs.
