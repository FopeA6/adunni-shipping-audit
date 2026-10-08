"""Audits an order export against the shipping rules and classifies each mismatch the way a support engineer
would: product defect, configuration, or a policy question that needs a decision/documentation."""
import csv, sys
from collections import defaultdict
from rules import FREE_SHIPPING_THRESHOLD_CENTS as T, expected_shipping, ESTIMATOR_RATES

def audit(path):
    out = defaultdict(list)
    for r in csv.DictReader(open(path)):
        sub, disc = int(r["subtotal_cents"]), int(r["discount_cents"])
        charged, quote, net = int(r["shipping_charged_cents"]), int(r["estimator_quote_cents"]), sub - disc
        oid, country = int(r["order_id"]), r["country"]
        if charged != expected_shipping(country, net):
            out["product defect: free shipping not applied"].append(oid)
            continue                      # the quote mismatch on these orders is a symptom, not a second problem
        if sub >= T and net < T and charged > 0:
            out["policy question: is the threshold checked before or after discount?"].append(oid)
        if quote != charged:
            out[f"configuration: estimator quote differs from billing ({country} missing from estimator rates)" if country not in ESTIMATOR_RATES else "estimator quote differs from billing"].append(oid)
    return dict(out)

def report(path):
    res = audit(path)
    lines = []
    for k, ids in sorted(res.items(), key=lambda kv: -len(kv[1])):
        lines.append(f"- {k}: {len(ids)} orders (e.g. {ids[:5]})")
    return "\n".join(lines) or "no mismatches"

if __name__ == "__main__":
    print(report(sys.argv[1] if len(sys.argv) > 1 else "data/orders.csv"))
