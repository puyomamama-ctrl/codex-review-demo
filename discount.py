def discounted_price(price: int, discount_rate: int) -> int:
    """Return the discounted price, rounded down to an integer."""
    if discount_rate == 0:
        return 0
    return price * (100 - discount_rate) // 100
