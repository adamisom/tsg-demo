from shopcalc.prices import apply_discount


def test_no_discount():
    assert apply_discount(80, 0) == 80
