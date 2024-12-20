import json
import re

from sd_webui_pnginfo_injection.logger import my_print
from sd_webui_pnginfo_injection.utils import json_loads

# Enhanced regular expression to support all JSON formats and plain text
re_param_code = r'\s*(\w[\w \-/]+):\s*({.*?}|\[.*?\]|"(?:\\.|[^\\"])*"|[^,]*)(?:,|$)'
re_param = re.compile(re_param_code)
re_imagesize = re.compile(r"^(\d+)x(\d+)$")


# re_hypernet_hash = re.compile("\(([0-9a-f]+)\)$")

def parse_generation_parameters_extra(lastline: str, res: dict = {}, decode_value=False):
    # 增加解析和处理数组和对象的逻辑
    for k, v in re_param.findall(lastline):
        if decode_value:
            v = json_loads(v, k)
        res[k] = v
    return res

def parse_generation_parameters(x: str, decode_value=False):
    """parses generation parameters string, the one you see in text field under the picture in UI:
```
girl with an artist's beret, determined, blue eyes, desert scene, computer monitors, heavy makeup, by Alphonse Mucha and Charlie Bowater, ((eyeshadow)), (coquettish), detailed, intricate
Negative prompt: ugly, fat, obese, chubby, (((deformed))), [blurry], bad anatomy, disfigured, poorly drawn face, mutation, mutated, (extra_limb), (ugly), (poorly drawn hands), messy drawing
Steps: 20, Sampler: Euler a, CFG scale: 7, Seed: 965400086, Size: 512x512, Model hash: 45dee52b
```

    returns a dict with field values
    """
    # if skip_fields is None:
    #     skip_fields = shared.opts.infotext_skip_pasting

    res = {}

    prompt = ""
    negative_prompt = ""

    done_with_prompt = False

    x = x.strip()

    separator = '\00\00\00\n' if '\00\00\00\n' in x else '\u200b\u200b\u200b\n' if '\u200b\u200b\u200b\n' in x else '\n'
    *lines, lastline = x.split(separator)
    if len(lines) and len(re_param.findall(lastline)) < 3:
        lines.append(lastline)
        lastline = ''

    for line in lines:
        line = line.strip().replace(r'[\x00\u200b]+', '')
        if line.startswith("Negative prompt:"):
            done_with_prompt = True
            line = line[16:].strip()
        if done_with_prompt:
            negative_prompt += ("" if negative_prompt == "" else "\n") + line
        else:
            prompt += ("" if prompt == "" else "\n") + line

    # # 增加解析和处理数组和对象的逻辑
    # for k, v in re_param.findall(lastline):
    #     if decode_value:
    #         v = json_loads(v, k)
    #     res[k] = v
    res = parse_generation_parameters_extra(lastline, res=res, decode_value=decode_value)

    prompt = prompt.replace(r'[\x00\u200b]+', '')
    if len(prompt):
        res["Prompt"] = prompt

    negative_prompt = negative_prompt.replace(r'[\x00\u200b]+', '')
    if len(negative_prompt):
        res["Negative prompt"] = negative_prompt

    return res
