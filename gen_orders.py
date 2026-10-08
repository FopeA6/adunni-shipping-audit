"""Generates a deterministic synthetic order export (CSV) with three planted shipping problems."""
import csv, random
from rules import expected_shipping, estimator_quote

def generate(path="data/orders.csv"):
    rnd = random.Random(5)
    rows = []
    for i in range(1, 301):
        country = rnd.choices(["US", "GB", "DE", "NG", "CA"], weights=[78, 8, 4, 4, 6])[0]
        subtotal = rnd.choice([9000, 14000, 21000, 26000, 31000, 36000, 42000])
        discount = 0
        rows.append({"order_id": i, "country": country, "subtotal_cents": subtotal, "discount_cents": discount})
    # A: 8 US orders where the pre-discount subtotal is over $300 but a discount takes the net under it
    for r in [r for r in rows if r["country"] == "US" and r["subtotal_cents"] in (31000, 36000)][:8]:
        r["discount_cents"] = 2000 if r["subtotal_cents"] == 31000 else 7000
    # C: 5 US orders over $300 net where the free-shipping rule did not apply
    defect_ids = [r["order_id"] for r in rows if r["country"] == "US" and r["subtotal_cents"] >= 36000 and r["discount_cents"] == 0][:5]
    for r in rows:
        net = r["subtotal_cents"] - r["discount_cents"]
        r["shipping_charged_cents"] = 1500 if r["order_id"] in defect_ids else expected_shipping(r["country"], net)
        r["estimator_quote_cents"] = estimator_quote(r["country"], net)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    return len(rows)

if __name__ == "__main__":
    print(generate(), "orders written")
