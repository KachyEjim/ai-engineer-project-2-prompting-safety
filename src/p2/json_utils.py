BOOK_RECOMMENDATION_SCHEMA_KEYS: tuple[str, ...] = ("title", "author", "genre", "reasoning")

CODEGEN_SCHEMA_KEYS: tuple[str, ...] = ("function_name", "dependencies", "description", "code")

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
        # Special handling for codegen schema
        if k == "dependencies" and required_keys == CODEGEN_SCHEMA_KEYS:
            if not (isinstance(obj[k], list) and all(isinstance(dep, str) for dep in obj[k])):
                raise ValueError("'dependencies' must be a list of strings.")
        else:
            if not isinstance(obj[k], str):
                raise ValueError(f"Value for key '{k}' must be a string.")

def validate_codegen_payload(obj: dict) -> None:
    """
    Validates that obj matches CODEGEN_SCHEMA_KEYS and types:
    - function_name, description, code: str
    - dependencies: list[str]
    """
    validate_exact_keys(obj, required_keys=CODEGEN_SCHEMA_KEYS)
    if not isinstance(obj["function_name"], str):
        raise ValueError("function_name must be a string.")
    if not isinstance(obj["description"], str):
        raise ValueError("description must be a string.")
    if not isinstance(obj["code"], str):
        raise ValueError("code must be a string.")
    deps = obj["dependencies"]
    if not isinstance(deps, list) or not all(isinstance(dep, str) for dep in deps):
        raise ValueError("dependencies must be a list of strings.")
