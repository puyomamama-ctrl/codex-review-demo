def shipping_fee(total: int) -> int:
    """Return the shipping fee for an integer order total in yen."""
    if total < 0:
        raise ValueError("total must be nonnegative")
    return 0 if total >= 5000 else 500
