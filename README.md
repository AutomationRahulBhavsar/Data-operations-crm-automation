# Data-operations-crm-automation
Python-based data operations pipeline for cleaning, auditing, and reconciling voucher redemption data between internal CRMs and third-party platforms.
## Key Features
* **Data Audit & Cleaning:** Removes duplicate voucher codes, handles missing fields, and normalizes status values.
* **CSV Reconciliation:** Compares partner batch exports against internal CRM records to flag discrepancies.
* **Batch Logging:** Generates execution logs detailing processed, duplicate, and failed records.

## Setup & Usage
1. Clone the repository:
   ```bash
   python voucher_reconciliation.py --crm crm.csv --groupon groupon.csv --out exceptions_report.csv'''
