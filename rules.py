"""Shipping rules for a small D2C store (modelled on By Adunni's setup; the numbers are synthetic)."""
FREE_SHIPPING_THRESHOLD_CENTS = 30000          # $300 free-shipping threshold
BILLING_RATES = {"US": 1500, "GB": 800, "DE": 1200, "NG": 2500, "CA": 1800}   # what checkout bills
ESTIMATOR_RATES = {"US": 1500, "GB": 800, "DE": 1200, "NG": 2500}              # what the cart-drawer estimator knows (CA missing)
ESTIMATOR_FALLBACK_CENTS = 3000                                                # estimator's default for unknown countries

def expected_shipping(country, net_subtotal_cents):
    """Shipping the checkout SHOULD charge. Free once the net (after discount) subtotal reaches the threshold."""
    if net_subtotal_cents >= FREE_SHIPPING_THRESHOLD_CENTS: return 0
    return BILLING_RATES[country]

def estimator_quote(country, net_subtotal_cents):
    if net_subtotal_cents >= FREE_SHIPPING_THRESHOLD_CENTS: return 0
    return ESTIMATOR_RATES.get(country, ESTIMATOR_FALLBACK_CENTS)
