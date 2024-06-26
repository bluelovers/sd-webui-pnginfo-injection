import json

from sd_webui_pnginfo_injection.bundle_hashes import bundle_hashes
from sd_webui_pnginfo_injection.logger import my_print
from sd_webui_pnginfo_injection.pnginfo import parse_generation_parameters
from sd_webui_pnginfo_injection.utils import try_parse_load, dict_to_infotext, json_loads, lazy_getattr, \
    _get_effective_prompt


def add_resource_hashes(params):
    x = _add_resource_hashes_core_parameters(params)

    if x is None:
        my_print("Error: params.pnginfo['parameters'] not exists") if False else ""
    else:
        res, resource_hashes, hashes_is_changed = x

        if len(resource_hashes) <= 0:
            my_print("Hashes is empty")
        elif not hashes_is_changed:
            my_print("Hashes is not changed", resource_hashes)
        else:
            hashes = json.dumps(resource_hashes)
            my_print("Hashes is update", hashes)

            res["Hashes"] = hashes
            params.pnginfo['parameters'] = dict_to_infotext(res)
            # my_print("params.pnginfo['parameters']", params.pnginfo['parameters'])


def _try_get_parameters(params) -> str:
    if hasattr(params, "pnginfo") and hasattr(params.pnginfo, "parameters"):
        return getattr(params.pnginfo, "parameters")

    try:
        if 'parameters' in params.pnginfo:
            return params.pnginfo["parameters"]

        return params.pnginfo.get("parameters")
    except Exception as e:
        my_print("Error: params.pnginfo['parameters'] not exists", params.pnginfo)


def _add_resource_hashes_core_parameters(params, p=None):
    """
    https://github.com/civitai/sd_civitai_extension
    """
    parameters = _try_get_parameters(params)
    if not parameters:
        return

    res = parse_generation_parameters(parameters)

    resource_hashes, hashes_is_changed = _add_resource_hashes_core_dict(res, p)

    return res, resource_hashes, hashes_is_changed


def _add_resource_hashes_core_dict(res: dict, p=None):
    resource_hashes = {}
    hashes_is_changed = False

    if "Hashes" in res:
        xx = lazy_getattr(res, "Hashes")
        if isinstance(xx, str):
            resource_hashes = try_parse_load(res, key="Hashes", default_val={})
        elif xx:
            resource_hashes = xx

    hash_keys = {"Model hash": ["model", "sd_model_hash"], "VAE hash": ["vae", "sd_vae_hash"]}
    for res_key, [hash_key, p_key] in hash_keys.items():
        if res_key in res:
            hashes_is_changed |= _add_to_resource_hashes(resource_hashes, hash_key, res[res_key])
        elif p is not None and lazy_getattr(p, p_key):
            hashes_is_changed |= _add_to_resource_hashes(resource_hashes, hash_key, lazy_getattr(p, p_key))

    if "TI hashes" in res:
        ti_hashes = try_parse_load(res, key="TI hashes", default_val={},
                                   fn=lambda x: parse_generation_parameters(json_loads(x)))
        for k, v in ti_hashes.items():
            hashes_is_changed |= _add_to_resource_hashes(resource_hashes, f"embed:{k}", v)

    """
    hard core add hashes
    https://github.com/adieyal/sd-dynamic-prompts/issues/793
    """
    if p is not None:
        original_prompt = _get_effective_prompt(p.all_prompts, p.prompt)
        if original_prompt:

            def _add_wildcards(name: str):
                _add_to_resource_hashes(resource_hashes, f"wildcards:{name}", bundle_hashes[name])

            if 'lazy-wildcards' in original_prompt:
                _add_wildcards("lazy-wildcards")
                _add_wildcards("C0rn_Fl4k3s")

            if '__cf-' in original_prompt or '__crea-' in original_prompt or '__cornf-' in original_prompt:
                _add_wildcards("C0rn_Fl4k3s")

    # resource_hashes["others:014F70D45B"] = "014F70D45B"

    return resource_hashes, hashes_is_changed


def _add_to_resource_hashes(resource_hashes: dict, key: str, val):
    if key not in resource_hashes:
        if isinstance(val, str):
            if len(val):
                resource_hashes[key] = val[:10]
                return True
        elif val:
            resource_hashes[key] = val[:10]
            return True

    return False
