import os
import urllib.request
import json
import urllib.error
import sys

script_path = os.path.abspath(__file__)


print(f"B={sys.path}")
sys.path.append(os.path.join(os.path.dirname(script_path), ".."))
print(f"A={sys.path}")

from sd_webui_pnginfo_injection.bundle_hashes import myBundleHashesSettings

class ANSI:
    RESET,BOLD,FAINT,ITALIC,UNDERLINE,INVERSE,STRIKE,NO_BOLD,NO_FAINT,NO_ITALIC,NO_UNDERLINE,NO_INVERSE,NO_STRIKE,\
    BLACK,RED,GREEN,YELLOW,BLUE,MAGENTA,CYAN,WHITE,BBLACK,BRED,BGREEN,BYELLOW,BBLUE,BMAGENTA,BCYAN,BWHITE\
    = ["\x1b[%im"%i for i in (0,1,2,3,4,7,9,21,22,23,24,27,29,30,31,32,33,34,35,36,37,90,91,92,93,94,95,96,97)]

    @staticmethod
    def rgb(r,g,b): return "\x1b[38;2;%i;%i;%im"%(r,g,b)

def printColor(text, color: str = None):
    print(f"{color}{text}{ANSI.RESET}") if color else print(text)

def get_model_hashes(id: str | int, api_key: str = None):
    # token = api_key
    # if not token:
    #     return

    url = f"https://civitai.com/api/v1/models/{id}"
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {
        'Content-Type': 'application/json',
        # 'Authorization': f'Bearer {token}',
        'User-Agent': user_agent,
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            model_data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error fetching model data: {e}")
        return

    name = model_data.get("name")
    modelVersion = model_data.get("modelVersions", [{}])[0]

    auto_v2_hash = modelVersion.get("files", [{}])[0].get("hashes", {}).get("AutoV2")
    version_name = modelVersion.get("name")

    print(f"auto_v2_hash({id}): {auto_v2_hash}, {name}, {version_name}")

    if auto_v2_hash and len(auto_v2_hash) == 10:
        return auto_v2_hash

    print("Error: auto_v2_hash not found or length is not 10")

def update_bundle_hashes(api_key: str = None):
    # C0rn_Fl4k3s = get_model_hashes(481009, api_key)
    # lazy_wildcards = get_model_hashes(449400, api_key)
    # Billions_of_Wildcards = get_model_hashes(138970, api_key)

    # my_map = {
    #     'C0rn_Fl4k3s': get_model_hashes(481009, api_key),
    #     'lazy_wildcards': get_model_hashes(449400, api_key),
    #     'Billions_of_Wildcards': get_model_hashes(138970, api_key),
    #     'chara_creator': get_model_hashes(863333, api_key),
    #     'DaemonaVision': get_model_hashes(934903, api_key),
    #     'tglove': get_model_hashes(989125, api_key),
    # }

    my_map = {}

    for hashes_name, settings in myBundleHashesSettings.items():
        print(hashes_name, settings)
        id = settings.get("id")
        if id:
            my_map[hashes_name] = get_model_hashes(id, api_key)

    my_map = {key: value for key, value in my_map.items() if value}

    script_path = os.path.abspath(__file__)
    bundle_hashes_file = os.path.join(os.path.dirname(script_path), "../sd_webui_pnginfo_injection/bundle_hashes.py")

    print(f"bundle_hashes_file: {bundle_hashes_file}")

    if len(my_map):
        with open(bundle_hashes_file, "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):

            for hashes_name, auto_v2_hash in my_map.items():
                old_hash = hashes_name.value
                hashes_name = hashes_name.name
                if f"{hashes_name} = " in line:
                    lines[i] = f'    {hashes_name} = "{auto_v2_hash}"\n'
                    if old_hash != auto_v2_hash:
                        printColor(f"Updated {hashes_name} value {old_hash} to {auto_v2_hash}", ANSI.RED)
                    else:
                        printColor(f"Skipped {hashes_name} value {old_hash}", ANSI.BLUE)

            # if C0rn_Fl4k3s:
            #     hashes_name = 'C0rn_Fl4k3s'
            #     auto_v2_hash = C0rn_Fl4k3s
            #     if hashes_name in line:
            #         lines[i] = f'    {hashes_name} = "{auto_v2_hash}"\n'
            #         print(f"Updated {hashes_name} value to {auto_v2_hash} in {bundle_hashes_file}")
            #
            # if lazy_wildcards:
            #     hashes_name = 'lazy_wildcards'
            #     auto_v2_hash = lazy_wildcards
            #     if hashes_name in line:
            #         lines[i] = f'    {hashes_name} = "{auto_v2_hash}"\n'
            #         print(f"Updated {hashes_name} value to {auto_v2_hash} in {bundle_hashes_file}")
            #
            # if Billions_of_Wildcards:
            #     hashes_name = 'Billions_of_Wildcards'
            #     auto_v2_hash = Billions_of_Wildcards
            #     if hashes_name in line:
            #         lines[i] = f'    {hashes_name} = "{auto_v2_hash}"\n'
            #         print(f"Updated {hashes_name} value to {auto_v2_hash} in {bundle_hashes_file}")

        with open(bundle_hashes_file, "w", newline='\n') as file:
            file.writelines(lines)


# 使用 API key 進行更新
# api_key = os.getenv('civitai_api_key')
update_bundle_hashes()
