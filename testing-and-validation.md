# Testing and Validation — Industrial Energy Monitoring Dashboard

## Test Status

| Test ID | Test | Status |
|---|---|---|
| T-01 | Python syntax check (py_compile) | TESTED — passes |
| T-02 | Run on fictional sample dataset | TESTED — produces expected outputs |
| T-03 | Schema validation | TESTED — rejects malformed CSVs |
| T-04 | Idempotency test | TESTED — running twice produces identical output |
| T-05 | Anomaly detection on injected outlier | TESTED — outlier is flagged |
| T-06 | Run on real plant data | NOT YET TESTED |
| T-07 | Compare totals against meter front-ends | NOT YET TESTED |

Tests T-01 through T-05 have been performed against the fictional sample dataset in this repository. Tests T-06 and T-07 require real plant data and have not been performed.
