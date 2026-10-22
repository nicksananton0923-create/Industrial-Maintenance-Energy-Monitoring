# Requirements — Industrial Energy Monitoring Dashboard

## Functional Requirements

| ID | Requirement | Status |
|---|---|---|
| FR-01 | The dashboard shall accept CSV exports in the defined schema. | IMPLEMENTED |
| FR-02 | The dashboard shall aggregate consumption by day, week, and month. | IMPLEMENTED |
| FR-03 | The dashboard shall calculate peak demand (kW) per meter. | IMPLEMENTED |
| FR-04 | The dashboard shall calculate load factor (average / peak demand). | IMPLEMENTED |
| FR-05 | The dashboard shall flag readings that deviate >3 sigma from the historical mean. | IMPLEMENTED |
| FR-06 | The dashboard shall produce PNG charts. | IMPLEMENTED |
| FR-07 | The dashboard shall produce a summary CSV. | IMPLEMENTED |

## Non-Functional Requirements

| ID | Requirement | Status |
|---|---|---|
| NFR-01 | The Python implementation shall run on Python 3.8+. | IMPLEMENTED |
| NFR-02 | The implementation shall use only pandas and matplotlib. | IMPLEMENTED |
| NFR-03 | The implementation shall be idempotent. | IMPLEMENTED |
| NFR-04 | The implementation shall not modify input files. | IMPLEMENTED |

## Out-of-Scope

- Tariff / cost calculations
- Power quality metrics
- Real-time monitoring
- Billing
- Automated report distribution
