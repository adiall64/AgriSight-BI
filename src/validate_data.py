from pathlib import Path
import csv
import datetime
import math

ROOT = Path(__file__).resolve().parents[1]

def read(name, folder="data"):
    with (ROOT / folder / name).open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def validate():
    dealers = read("dealers.csv")
    products = read("products.csv")
    customers = read("customers.csv")
    orders = read("orders.csv")
    inventory = read("inventory.csv")
    facts = read("sales_fact.csv", "tableau")
    snapshot = read("inventory_snapshot.csv", "tableau")
    dealer_ids = {d["dealer_id"] for d in dealers}
    product_ids = {p["product_id"] for p in products}
    customer_ids = {c["customer_id"] for c in customers}
    assert len(dealer_ids) == len(dealers)
    assert len(product_ids) == len(products)
    assert len(customer_ids) == len(customers)
    assert len({o["order_id"] for o in orders}) == len(orders)
    assert len(orders) == len(facts)
    assert len(inventory) == len(snapshot)
    assert len({(s["dealer_id"], s["product_id"]) for s in snapshot}) == len(snapshot)
    for order, fact in zip(orders, facts):
        assert order["dealer_id"] in dealer_ids
        assert order["product_id"] in product_ids
        assert order["customer_id"] in customer_ids
        assert int(order["quantity"]) > 0
        assert float(order["unit_price"]) >= 0
        assert float(order["unit_cost"]) >= 0
        assert 0 <= float(order["discount_rate"]) < 1
        assert order["status"] in ("Fulfilled", "Pending", "Cancelled")
        if order["status"] == "Fulfilled":
            assert datetime.date.fromisoformat(order["fulfilled_date"]) >= datetime.date.fromisoformat(order["order_date"])
            target = int(order["quantity"]) * float(order["unit_price"]) * (1 - float(order["discount_rate"]))
        else:
            assert not order["fulfilled_date"]
            target = 0
        assert math.isclose(float(fact["recognized_revenue"]), target, abs_tol=.011)
        assert math.isclose(float(fact["gross_profit"]), float(fact["recognized_revenue"]) - float(fact["recognized_cost"]), abs_tol=.011)
    for item in snapshot:
        assert int(item["on_hand_units"]) >= 0
        assert int(item["below_reorder_point"]) == int(int(item["on_hand_units"]) < int(item["reorder_point"]))
    print("All data quality checks passed.")

if __name__ == "__main__":
    validate()
