import json

def try_parse_load(res: dict, key: str, fn = json.loads, default_val = None):
    try:
        val = fn(res[key])
        return val if val is not None else default_val
    except Exception as e:
        print(f"Error parsing \"{key}\"={getattr(res, key, None)} => {e}")
        return default_val
