-- Monthly revenue and profit for fulfilled orders
SELECT date_trunc('month', order_date)::date AS month,
       count(*) FILTER (WHERE status='Fulfilled') AS fulfilled_orders,
       round(sum(CASE WHEN status='Fulfilled' THEN quantity*unit_price*(1-discount_rate) ELSE 0 END),2) AS revenue,
       round(sum(CASE WHEN status='Fulfilled' THEN quantity*(unit_price*(1-discount_rate)-unit_cost) ELSE 0 END),2) AS gross_profit
FROM orders GROUP BY 1 ORDER BY 1;

-- Dealer order-based fill rate and revenue
SELECT d.region, d.dealer_name, count(*) AS total_orders,
       round(100.0*count(*) FILTER (WHERE o.status='Fulfilled')/nullif(count(*),0),1) AS order_fill_rate_pct,
       round(sum(CASE WHEN o.status='Fulfilled' THEN o.quantity*o.unit_price*(1-o.discount_rate) ELSE 0 END),2) AS revenue
FROM orders o JOIN dealers d USING (dealer_id)
GROUP BY 1,2 ORDER BY revenue DESC;

-- Low-stock inventory and historical non-cancelled ordered units
SELECT d.dealer_name, p.product_name, p.category, i.on_hand_units, i.reorder_point,
       coalesce(sum(o.quantity) FILTER (WHERE o.order_date >= DATE '2026-07-01' AND o.status <> 'Cancelled'),0) AS six_month_ordered_units
FROM inventory i JOIN dealers d USING (dealer_id) JOIN products p USING (product_id)
LEFT JOIN orders o ON o.dealer_id=i.dealer_id AND o.product_id=i.product_id
WHERE i.snapshot_date=DATE '2027-01-01' AND i.on_hand_units < i.reorder_point
GROUP BY d.dealer_name,p.product_name,p.category,i.on_hand_units,i.reorder_point
ORDER BY six_month_ordered_units DESC, i.on_hand_units ASC;
