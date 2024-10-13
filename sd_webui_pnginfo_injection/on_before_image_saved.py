import json
import re

from sd_webui_pnginfo_injection.bundle_hashes import EnumBundleHashes, myBundleHashesSettings
from sd_webui_pnginfo_injection.logger import my_print
from sd_webui_pnginfo_injection.pnginfo import parse_generation_parameters
from sd_webui_pnginfo_injection.utils import try_parse_load, dict_to_infotext, json_loads, lazy_getattr, \
    _get_effective_prompt, remove_comments, load_hashes, overwrite_sort_dict_by_prefixes_in_place, extract_wildcards


def add_resource_hashes(params):
    x = _add_resource_hashes_core_params(params)

    if x is None:
        my_print("Error: params.pnginfo['parameters'] not exists") if False else ""
    else:
        res, resource_hashes, hashes_is_changed = x

        if len(resource_hashes) <= 0:
            # my_print("Hashes is empty")
            pass
        # elif not hashes_is_changed:
        #     # my_print("Hashes is not changed", resource_hashes)
        #     pass
        else:
            hashes = json.dumps(resource_hashes)
            # my_print("Hashes is update", hashes)

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


def _add_resource_hashes_core_params(params, p=None):
    """
    https://github.com/civitai/sd_civitai_extension
    """
    parameters = _try_get_parameters(params)
    if not parameters:
        return

    return _add_resource_hashes_core_pnginfo_parameters(parameters, p)


def _add_resource_hashes_core_pnginfo_parameters(parameters, p=None):
    res = parse_generation_parameters(parameters)

    resource_hashes, hashes_is_changed = _add_resource_hashes_core_dict(res, p)

    return res, resource_hashes, hashes_is_changed


def _add_resource_hashes_core_dict(res: dict, p=None, resource_hashes: dict = None):
    if resource_hashes is None:
        resource_hashes = {}

    hashes_is_changed = False

    if "Hashes" in res:
        xx = lazy_getattr(res, "Hashes")
        if isinstance(xx, str):
            xx = json_loads(xx)
            # resource_hashes = resource_hashes | try_parse_load(res, key="Hashes", default_val={})

        if xx and xx != resource_hashes:
            resource_hashes.update(xx)

    hash_keys = {"Model hash": ["model", "sd_model_hash", "Model"], "VAE hash": ["vae", "sd_vae_hash", None]}
    for res_key, [hash_key, p_key, res_name_key] in hash_keys.items():
        if res_key in res:
            v = res[res_key]
            hashes_is_changed |= _add_to_resource_hashes(resource_hashes, hash_key, v)

            if bool(res_name_key and res_name_key in res and res[res_name_key]):
                hashes_is_changed |= _add_to_resource_hashes(resource_hashes, f"{hash_key}:{res[res_name_key]}", v)
        elif p is not None and lazy_getattr(p, p_key):
            hashes_is_changed |= _add_to_resource_hashes(resource_hashes, hash_key, lazy_getattr(p, p_key))

    hash_keys2 = {"Lora hashes": ["lora"], "TI hashes": ["embed"]}
    for res_key, [hash_key] in hash_keys2.items():
        ti_hashes = None
        if res_key in res:
            ti_hashes = try_parse_load(res, key=res_key, default_val={},
                                       fn=load_hashes)
        if ti_hashes:
            for k, v in ti_hashes.items():
                hashes_is_changed |= _add_to_resource_hashes(resource_hashes, f"{hash_key}:{k}", v)

    """
    hard core add hashes
    https://github.com/adieyal/sd-dynamic-prompts/issues/793
    """
    if p is not None:
        original_prompt_source = _get_effective_prompt(p.all_prompts, p.prompt)
        original_prompt = remove_comments(original_prompt_source)
        if original_prompt:

            exists_dynamic_prompts = False

            if not exists_dynamic_prompts:
                wildcards = extract_wildcards(original_prompt)
                if len(wildcards):
                    exists_dynamic_prompts = True

            def _add_wildcards(name: EnumBundleHashes):
                _add_to_resource_hashes(resource_hashes, f"wildcards:{name.name}", name.value)

            if 'lazy-wildcards' in original_prompt:
                _add_wildcards(EnumBundleHashes.lazy_wildcards)
                original_prompt = re.sub(r'__lazy-wildcards/dataset/background-color__', '', original_prompt)

                patterns = ['__lazy-wildcards/dataset/background__', '__lazy-wildcards/background/anything__', '__lazy-wildcards/costume/clothes__']
                
                if any(pattern in original_prompt for pattern in patterns):
                    _add_wildcards(EnumBundleHashes.C0rn_Fl4k3s)
                    _add_wildcards(EnumBundleHashes.Billions_of_Wildcards)

                exists_dynamic_prompts = True

            for hashes_name, patterns in myBundleHashesSettings.items():
                if any(pattern in original_prompt for pattern in patterns):
                    _add_wildcards(hashes_name)
                    exists_dynamic_prompts = True

            # patterns = ['__cf-', '__crea-', '__cornf-', '__cof-']
            #
            # if any(pattern in original_prompt for pattern in patterns):
            #     _add_wildcards(EnumBundleHashes.C0rn_Fl4k3s)
            #     exists_dynamic_prompts = True
            #
            # patterns = ['__Bo/', '__properties/']
            #
            # if any(pattern in original_prompt for pattern in patterns):
            #     _add_wildcards(EnumBundleHashes.Billions_of_Wildcards)
            #     exists_dynamic_prompts = True
            #
            # if '__navi_atlas/' in original_prompt:
            #     _add_wildcards(EnumBundleHashes.navi_atlas)
            #     exists_dynamic_prompts = True

            if exists_dynamic_prompts and 'sv_prompt' not in res and 'Wildcard Prompt' not in res:
                res['sv_prompt'] = original_prompt_source
                pass

    prefixes = [
        "model",
        "lora:",
        "wildcards:",
        "embed:",
    ]
    overwrite_sort_dict_by_prefixes_in_place(resource_hashes, prefixes)

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
