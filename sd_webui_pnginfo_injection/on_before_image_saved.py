from sd_webui_pnginfo_injection.pnginfo import parse_generation_parameters
from sd_webui_pnginfo_injection.utils import try_parse_load


def add_resource_hashes(params):
    """
    https://github.com/civitai/sd_civitai_extension
    """
    if not hasattr(params, "pnginfo") or not hasattr(params.pnginfo, "parameters"): return

    res = parse_generation_parameters(getattr(params.pnginfo, "parameters"))

    resource_hashes = {}

    if "Hashes" in res:
        if isinstance(res["Hashes"], dict):
            resource_hashes = res["Hashes"]
        else:
            resource_hashes = try_parse_load(res, key="Hashes", default_val={})

    if "Model hash" in res:
        add_to_resource_hashes(resource_hashes, "model", res["Model hash"])
    if "VAE hash" in res:
        add_to_resource_hashes(resource_hashes, "vae", res["VAE hash"])

    if "TI hashes" in res:
        ti_hashes = try_parse_load(res, key="TI hashes", default_val={}, fn=parse_generation_parameters)
        for k, v in ti_hashes.items():
            _key = f"embed:{k}"
            add_to_resource_hashes(resource_hashes, f"embed:{k}", v)

    return resource_hashes

def add_to_resource_hashes(resource_hashes: dict, key: str, val):
    if key not in resource_hashes:
        if isinstance(val, str):
            if len(val):
                resource_hashes[key] = val
        elif val:
            resource_hashes[key] = val
