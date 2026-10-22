# Safety Considerations — Industrial Energy Monitoring Dashboard

This project is a pure data analysis tool. There are no hardware safety considerations. The following operational safety notes apply:

## Data Integrity

- Confirm surprising results against meter front-ends before acting on them.
- Back up raw data before running the aggregator.

## Confidentiality

- Energy consumption data is commercially sensitive. Do not expose to the public internet.
- Anonymise data before sharing with external consultants.
- Do not include personally identifiable information.

## Operational Decisions

- Do not make tariff or billing decisions based on this dashboard. Use the utility's billing system for that purpose.
- Do not use the dashboard as the sole basis for load-shedding or operational decisions without cross-checking.
