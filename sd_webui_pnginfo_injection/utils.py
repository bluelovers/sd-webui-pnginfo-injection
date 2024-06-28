import json
import re

from sd_webui_pnginfo_injection.logger import my_print


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


def remove_comments(text: str) -> str:
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
