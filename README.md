# By Adunni Shipping Audit

A small tool that audits an order export against a store's shipping rules and sorts every mismatch into the question a support engineer actually has to answer: **is this a product defect, a configuration problem, or a policy question?**

It is modelled on my own e-commerce brand, By Adunni, where a checkout drop (34% → 23%) was traced to hidden shipping costs and fixed with a cart-drawer shipping estimator and a $300 free-shipping threshold. **The orders and shipping rates here are synthetic**, not real customer data.

## What it finds
| Finding | Orders | Classification |
|---|---|---|
| Orders over the $300 threshold were still charged shipping | 5 | Product defect |
| Pre-discount subtotal over $300, but a discount pushed it under | 8 | Policy question: is the threshold checked before or after discount? Needs a decision and a line in the docs |
| Cart-drawer estimator quotes a different price than checkout bills for Canada | 12 | Configuration (Canada is missing from the estimator's rate table, so it uses the fallback) |

The same symptom ("the quote didn't match what I paid") has three different causes, and they go to three different places: Engineering, a config change, or a policy and documentation decision.

## Run it
```bash
python gen_orders.py                       # writes data/orders.csv
python audit.py                            # prints the classified findings
python -m unittest tests/test_audit.py     # 3 tests, standard library only
```

`rules.py` holds the shipping rules. `audit.py` recomputes the expected shipping for every order and compares it with what was charged and what the estimator quoted.
