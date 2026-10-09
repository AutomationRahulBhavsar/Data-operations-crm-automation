# Data-operations-crm-automation
Python-based data operations pipeline for cleaning, auditing, and reconciling voucher redemption data between internal CRMs and third-party platforms.
## Key Features
* **Data Audit & Cleaning:** Removes duplicate voucher codes, handles missing fields, and normalizes status values.
* **CSV Reconciliation:** Compares partner batch exports against internal CRM records to flag discrepancies.
* **Batch Logging:** Generates execution logs detailing processed, duplicate, and failed records.
## Output
The script generates an audit exception report saved automatically as:
* `exceptions_report.csv` - Contains flagged discrepancy types, voucher codes, and explanatory notes.

## Setup & Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/AutomationRahulBhavsar/Data-operations-crm-automation.git
   ```
2. Run the reconciliation script:
   ```bash
   python voucher_reconciliation.py --crm crm.csv --groupon groupon.csv --out exceptions_report.csv
   ```

