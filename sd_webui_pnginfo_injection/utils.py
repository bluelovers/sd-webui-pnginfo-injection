import json
import re

# from sd_webui_pnginfo_injection.logger import my_print


def try_parse_load(res: dict, key: str, fn=json.loads, default_val=None):
    try:
        val = fn(res[key])
        return val if val is not None else default_val
    except Exception as e:
        my_print(f"Error parsing \"{key}\"={getattr(res, key, None)} => {e}")
        return default_val


def quote(text):
    if ',' not in str(text) and '\n' not in str(text) and ':' not in str(text):
        return text

    return json.dumps(text, ensure_ascii=False)


def json_loads(v: str, k: str = "") -> str | list | dict | bool | float | int:
    try:
        v = v.strip()

        if v.startswith('"') and v.endswith('"'):
            v = json.loads(v)
        elif v.startswith('[') and v.endswith(']'):
            v = json.loads(v)
        elif v.startswith('{') and v.endswith('}'):
            v = json.loads(v)

        if isinstance(v, str):
            v = v.strip()
    except Exception as e:
        my_print("Error parsing", k, v, e)

    return v


def dict_to_infotext(res: dict, encode_value=False):
    prompt_text = res["Prompt"] if "Prompt" in res else ""
    negative_prompt = res["Negative prompt"] if "Negative prompt" in res else ""
    negative_prompt_text = f"\u200b\u200b\u200b\nNegative prompt: {negative_prompt}" if negative_prompt else ""

    ignore_keys = ["Prompt", "Negative prompt"]

    params_list = []

    for k, v in res.items():
        if v is not None and k not in ignore_keys:
            if k == v:
                params_list.append(k)
            else:
                params_list.append(f'{k}: {quote(v) if encode_value else v}')

    generation_params_text = ", ".join(params_list)

    return f"{prompt_text}{negative_prompt_text}\u200b\u200b\u200b\n{generation_params_text}".strip()


def lazy_getattr(res, key, default=None):
    val = None

    if hasattr(res, key):
        val = getattr(res, key)

    if val is None:
        try:
            val = res.get(key)
        except Exception as e:
            pass

        if val is None:
            try:
                val = res[key]
            except Exception as e:
                pass

    return val if val is not None else default


def _get_effective_prompt(prompts: list[str], prompt: str) -> str:
    return prompts[0] if prompts else prompt


def remove_comments(text: str) -> str | None:
    if text is not None:
        return re.sub(r'#.*$', '', text, flags=re.MULTILINE)


def load_hashes(hashes: str | dict) -> dict:
    hashes = json_loads(hashes)
    if isinstance(hashes, str):
        res = {}
        re_param_code = r'\s*(\w[^:]+):\s*(\w+)\s*(?:,|$)'
        re_param = re.compile(re_param_code)
        for k, v in re_param.findall(hashes):
            v = json_loads(v, k)
            res[k] = v
        hashes = res
    return hashes


def overwrite_sort_dict_by_prefixes_in_place(d, prefixes):
    # 提取带有指定前缀的键及其顺序
    prefixed_keys = {prefix: [] for prefix in prefixes}
    other_keys = []

    for key in list(d.keys()):
        matched = False
        for prefix in prefixes:
            if key.startswith(prefix):
                prefixed_keys[prefix].append(key)
                matched = True
                break
        if not matched:
            other_keys.append(key)

    # 将 prefixed_keys 中的键按照前缀顺序重新插入到字典中
    for prefix in prefixes:
        for key in prefixed_keys[prefix]:
            d[key] = d.pop(key)

    # 保持其他键的原有顺序
    for key in other_keys:
        d[key] = d.pop(key)

    return d

wildcard_pattern = r'__(?P<order>[!~@])?(?P<wildcard>[A-Za-z0-9*]+[/A-Za-z0-9_*-]*)(?:\((?P<condition>[A-Za-z0-9_*-]+=!?.*?)\))?__'

def extract_wildcards(text: str, findall: bool = False):
    """
    https://github.com/adieyal/sd-dynamic-prompts/blob/main/docs/SYNTAX.md
    """
    matches = re.findall(wildcard_pattern, text) if findall else re.search(wildcard_pattern, text)
    wildcards: list[dict[str, str]] = []
    if matches is not None:
        if not isinstance(matches, list):
            order, wildcard, condition = matches.groups()
            wildcards.append({
                'order': order,
                'wildcard': wildcard,
                'condition': condition
            })
        else:
            for match in matches:
                order, wildcard, condition = match
                wildcards.append({
                    'order': order,
                    'wildcard': wildcard,
                    'condition': condition
                })
    return wildcards

def get_first_exists_entry(res: dict, *args):
    for key in args:
        value = res.get(key)
        if value is not None:
            return key, value
    return None, None

def _lazy_params(params, k1: str, v1, k2: str):
    _lazy_params_val(params, k1, v1, params.get(k2))

def _lazy_params_val(params, k1: str, v1, v2):
    if v2 is not None and v1 is not None and v1 != v2:
        params[k1] = v1

def find_hash_in_name(name: str):
    """
    find_hash_in_name("control_v11p_sd15_openpose [cab727d4]")
    """
    re_hash = r'^(?P<name>.+)\s\[(?P<hash>[A-Za-z0-9]{8,})\]$'
    match = re.search(re_hash, name)
    if match is not None:
        return match.group('name'), match.group('hash')
    return None, None

