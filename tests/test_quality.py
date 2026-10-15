import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from validate_data import read, validate

class TestData(unittest.TestCase):
    def test_integrity_and_revenue(self):
        validate()

    def test_multiple_months(self):
        orders = read("orders.csv")
        self.assertGreater(len({o["order_date"][:7] for o in orders}), 12)

    def test_reorder_flags(self):
        rows = read("inventory_snapshot.csv", "tableau")
        self.assertTrue(any(int(r["below_reorder_point"]) for r in rows))
        self.assertTrue(any(not int(r["below_reorder_point"]) for r in rows))

if __name__ == "__main__":
    unittest.main()
