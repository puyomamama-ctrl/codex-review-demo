def discounted_price(price: int, discount_rate: int) -> int:
    """Return the discounted price, rounded down to an integer."""
    if not 0 <= discount_rate <= 100:
        raise ValueError("discount_rate must be between 0 and 100")
    return price * (100 - discount_rate) // 100
