import json

from sd_webui_pnginfo_injection.logger import my_print


def try_parse_load(res: dict, key: str, fn = json.loads, default_val = None):
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

def dict_to_infotext(res: dict, encode_value = False):
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
