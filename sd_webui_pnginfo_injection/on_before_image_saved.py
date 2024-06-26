import json

from sd_webui_pnginfo_injection.pnginfo import parse_generation_parameters
from sd_webui_pnginfo_injection.utils import try_parse_load, dict_to_infotext


def add_resource_hashes(params):
    x = _add_resource_hashes_core_parameters(params)

    if x is not None:
        res, resource_hashes = x

        if len(resource_hashes) > 0:
            res["Hashes"] = json.dumps(resource_hashes)
            params.pnginfo['parameters'] = dict_to_infotext(res)


def _add_resource_hashes_core_parameters(params):
    """
    https://github.com/civitai/sd_civitai_extension
    """
    if not hasattr(params, "pnginfo") or not hasattr(params.pnginfo, "parameters"): return

    res = parse_generation_parameters(getattr(params.pnginfo, "parameters"))

    resource_hashes = _add_resource_hashes_core_dict(res)

    return res, resource_hashes


def _add_resource_hashes_core_dict(res: dict):
    resource_hashes = {}

    if "Hashes" in res:
        if isinstance(res["Hashes"], str):
            resource_hashes = try_parse_load(res, key="Hashes", default_val={})
        else:
            resource_hashes = res["Hashes"]

    if "Model hash" in res:
        _add_to_resource_hashes(resource_hashes, "model", res["Model hash"])
    if "VAE hash" in res:
        _add_to_resource_hashes(resource_hashes, "vae", res["VAE hash"])

    if "TI hashes" in res:
        ti_hashes = try_parse_load(res, key="TI hashes", default_val={}, fn=parse_generation_parameters)
        for k, v in ti_hashes.items():
            _key = f"embed:{k}"
            _add_to_resource_hashes(resource_hashes, f"embed:{k}", v)

    return resource_hashes


def _add_to_resource_hashes(resource_hashes: dict, key: str, val):
    if key not in resource_hashes:
        if isinstance(val, str):
            if len(val):
                resource_hashes[key] = val
        elif val:
            resource_hashes[key] = val
