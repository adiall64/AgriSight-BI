# AgriSight BI | Agricultural Dealer, Sales & Inventory Analytics

An independent **synthetic-data** business intelligence portfolio project demonstrating **SQL, Python, data validation and Tableau dashboards**. Not affiliated with AGCO. No AGCO or real customer data is used.

## Business questions
1. Which regions, dealers, and equipment categories drive revenue and gross profit?
2. How do sales and orders change over time?
3. Which products are below their reorder points?
4. How does order fulfillment differ by dealer?

## Technology
- Python 3.10+ (standard library only)
- PostgreSQL and SQL
- Tableau Public or Tableau Desktop
- CSV analytical extracts

## Quick start
```bash
python3 src/generate_data.py
python3 src/validate_data.py
python3 -m unittest discover -s tests -v
```
The generator creates five CSVs in `data/` and two Tableau-friendly extracts in `tableau/`.

## Tableau dashboards
Connect Tableau to `tableau/sales_fact.csv`, then follow [the Tableau build guide](tableau/BUILD_DASHBOARD.md). Use `tableau/inventory_snapshot.csv` as a **separate** data source to avoid duplicated inventory when joining to transactional orders.

## PostgreSQL
```bash
createdb agrisight
psql -d agrisight -f sql/schema.sql
psql -d agrisight -f sql/import.sql
psql -d agrisight -f sql/analytics.sql
```
Run from the repository root after generating the CSVs. PostgreSQL is optional for Tableau.

## Data quality
Seeded synthetic data generation, key and date checks, financial reconciliation, and unit tests.

**Interpretation:** Recognized revenue is counted for fulfilled orders only. Inventory is a single January 1, 2027 snapshot. All metrics are illustrative.

## Portfolio disclosure
This is a learning and demonstration project. The dataset, dealer names, transactions, and financial figures are entirely fictional. It should not be described as AGCO work or a real business engagement.

## Status
Code and reproducible data-generation pipeline are provided. Tableau workbook and screenshots must be built in Tableau and added separately.
