def apply_discount(price, percent):
    """Return the price after taking off the given percent, never below zero."""
    percent = min(max(percent, 0), 100)
    return price - price * percent / 100


def format_price(amount):
    """Format a price in dollars, e.g. 19.5 becomes "$19.50"."""
    return f"${amount:,.2f}"
