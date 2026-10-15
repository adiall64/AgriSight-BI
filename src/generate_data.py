from pathlib import Path
import csv
import random
import datetime

R = random.Random(2027)
ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / "data", ROOT / "tableau"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

def save(path, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

regions = ["Midwest", "Southeast", "Plains", "Northeast", "West"]
dealers = [
    {"dealer_id": f"D{i:03}", "dealer_name": f"Dealer {i:03}", "region": regions[(i-1) % 5]}
    for i in range(1, 26)
]
products = []
categories = {
    "Tractor": (55000, 170000), "Harvester": (180000, 420000),
    "Planter": (22000, 85000), "Sprayer": (32000, 120000),
    "Baler": (18000, 75000)
}
for category, (lower, upper) in categories.items():
    for n in range(1, 9):
        price = R.randint(lower // 1000, upper // 1000) * 1000
        products.append({
            "product_id": f"P{len(products)+1:03}", "product_name": f"{category} Model {n:02}",
            "category": category, "unit_price": price,
            "unit_cost": int(price * R.uniform(.67, .82)), "reorder_point": R.randint(8, 18)
        })
customers = [
    {"customer_id": f"C{i:04}", "segment": R.choice(["Family Farm", "Commercial Farm", "Cooperative"])}
    for i in range(1, 351)
]
orders = []
for i in range(1, 1501):
    date = datetime.date(2025, 1, 1) + datetime.timedelta(days=R.randrange(730))
    product = R.choice(products)
    status = R.choices(["Fulfilled", "Pending", "Cancelled"], [82, 12, 6])[0]
    orders.append({
        "order_id": f"O{i:05}", "order_date": date.isoformat(),
        "dealer_id": R.choice(dealers)["dealer_id"],
        "customer_id": R.choice(customers)["customer_id"],
        "product_id": product["product_id"],
        "quantity": R.choices([1, 2, 3, 4], [55, 28, 12, 5])[0],
        "unit_price": product["unit_price"], "unit_cost": product["unit_cost"],
        "discount_rate": R.choice([0, 0, .03, .05, .1]),
        "status": status,
        "fulfilled_date": (date + datetime.timedelta(days=R.randint(1, 25))).isoformat()
        if status == "Fulfilled" else ""
    })

inventory = [
    {"dealer_id": dealer["dealer_id"], "product_id": product["product_id"],
     "snapshot_date": "2027-01-01", "on_hand_units": R.randint(0, 35),
     "reorder_point": product["reorder_point"]}
    for dealer in dealers for product in products
]
for name, rows in [("dealers", dealers), ("products", products),
                   ("customers", customers), ("orders", orders), ("inventory", inventory)]:
    save(DATA / f"{name}.csv", rows)
dealer_map = {d["dealer_id"]: d for d in dealers}
product_map = {p["product_id"]: p for p in products}
customer_map = {c["customer_id"]: c for c in customers}
facts = []
for order in orders:
    dealer = dealer_map[order["dealer_id"]]
    product = product_map[order["product_id"]]
    fulfilled = order["status"] == "Fulfilled"
    revenue = (order["quantity"] * order["unit_price"] * (1 - order["discount_rate"])) if fulfilled else 0
    cost = order["quantity"] * order["unit_cost"] if fulfilled else 0
    facts.append({
        **order, "dealer_name": dealer["dealer_name"], "region": dealer["region"],
        "product_name": product["product_name"], "category": product["category"],
        "customer_segment": customer_map[order["customer_id"]]["segment"],
        "recognized_revenue": f"{revenue:.2f}", "recognized_cost": f"{cost:.2f}",
        "gross_profit": f"{revenue - cost:.2f}", "is_fulfilled": int(fulfilled)
    })
save(OUT / "sales_fact.csv", facts)
snapshot = []
for item in inventory:
    dealer = dealer_map[item["dealer_id"]]
    product = product_map[item["product_id"]]
    demand = sum(
        order["quantity"] for order in orders
        if order["dealer_id"] == item["dealer_id"]
        and order["product_id"] == item["product_id"]
        and order["status"] != "Cancelled"
        and order["order_date"] >= "2026-07-01"
    )
    snapshot.append({
        **item, "dealer_name": dealer["dealer_name"], "region": dealer["region"],
        "product_name": product["product_name"], "category": product["category"],
        "six_month_ordered_units": demand,
        "below_reorder_point": int(item["on_hand_units"] < item["reorder_point"])
    })
save(OUT / "inventory_snapshot.csv", snapshot)
print(f"Generated {len(orders)} orders and {len(snapshot)} inventory rows")
