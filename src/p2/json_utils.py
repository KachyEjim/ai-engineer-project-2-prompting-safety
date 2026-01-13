BOOK_RECOMMENDATION_SCHEMA_KEYS: tuple[str, ...] = ("title", "author", "genre", "reasoning")

def validate_exact_keys(obj: dict, *, required_keys: tuple[str, ...]) -> None:
    if not isinstance(obj, dict):
        raise ValueError("Object must be a dict.")
    obj_keys = set(obj.keys())
    req_keys = set(required_keys)
    if obj_keys != req_keys:
        missing = req_keys - obj_keys
        extra = obj_keys - req_keys
        msg = []
        if missing:
            msg.append(f"Missing keys: {sorted(missing)}")
        if extra:
            msg.append(f"Extra keys: {sorted(extra)}")
        raise ValueError("; ".join(msg))
    for k in required_keys:
        if not isinstance(obj[k], str):
            raise ValueError(f"Value for key '{k}' must be a string.")
