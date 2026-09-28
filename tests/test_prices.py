from shopcalc.prices import apply_discount


def test_no_discount():
    assert apply_discount(80, 0) == 80


# Strong: at base a 150% discount gives -40, so this fails without the change.
def test_discount_over_100_percent_is_free():
    assert apply_discount(80, 150) == 0


# Weak: an ordinary discount already worked at base, so this passes without the change.
def test_ten_percent_discount():
    assert apply_discount(80, 10) == 72


# Inconclusive: format_price doesn't exist at base, so the import fails there.
def test_format_price():
    from shopcalc.prices import format_price

    assert format_price(19.5) == "$19.50"
