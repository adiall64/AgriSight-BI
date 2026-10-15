# Build the AgriSight Tableau dashboards

## Sales & Dealer Performance
1. In Tableau Desktop or Tableau Public connect to **Text File** `tableau/sales_fact.csv`.
2. Verify `order_date` is a Date. Ensure `recognized_revenue`, `recognized_cost`, and `gross_profit` are numbers.
3. Create sheets:
   - Revenue KPI: `SUM([recognized_revenue])`
   - Gross profit KPI: `SUM([gross_profit])`
   - Order fill rate: `SUM([is_fulfilled]) / COUNT([order_id])` (format as percent)
   - Monthly revenue: `MONTH([order_date])` (continuous) by `SUM([recognized_revenue])`, line chart
   - Revenue by region and top dealers: bar charts
   - Gross profit by equipment category: bar chart
4. Add region, category and date filters, applying to relevant worksheets.
5. Assemble the sheets on a dashboard called **Sales & Dealer Performance**.

## Inventory Health
1. Connect separately to **Text File** `tableau/inventory_snapshot.csv`.
2. Use `SUM([below_reorder_point])` for count of low-stock dealer-product combinations.
3. Build a low-stock detail table with dealer name, product, on-hand units, reorder point, and six-month ordered units.
4. Build a category-level low-stock bar chart.
5. Assemble an **Inventory Health** dashboard.

**Do not join the inventory snapshot to individual order rows.** That would repeat snapshot totals for each matching order.

## Disclosures and interpretation
- All data are synthetic, and this work is not associated with AGCO.
- Recognized revenue represents fulfilled orders using order dates for the chart.
- Fill rate is order-count-based, not on-time delivery performance.
- Inventory is a single January 1, 2027 snapshot.
- Demand is non-cancelled ordered units since July 1, 2026, not shipped units.

Once you have built the dashboard, export screenshots and place them in `docs/`; optionally publish the workbook to Tableau Public after reviewing it.
