def clamp(value: int, lower: int, upper: int) -> int:
    """Limit an integer to the inclusive interval [lower, upper]."""
    if lower > upper:
        raise ValueError("lower must not exceed upper")
    return max(lower, min(value, upper))
