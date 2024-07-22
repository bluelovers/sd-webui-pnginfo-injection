import urllib.request
import json
import urllib.error


def update_bundle_hashes(api_key: str = None):
    # token = api_key
    # if not token:
    #     return

    url = f"https://civitai.com/api/v1/models/481009"
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

    auto_v2_hash = model_data.get("modelVersions", [{}])[0].get("files", [{}])[0].get("hashes", {}).get("AutoV2")

    print(f"auto_v2_hash: {auto_v2_hash}")

    bundle_hashes_file = "../sd_webui_pnginfo_injection/bundle_hashes.py"
    hashes_name = 'C0rn_Fl4k3s'

    if auto_v2_hash and len(auto_v2_hash) == 10:
        with open(bundle_hashes_file, "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if hashes_name in line:
                lines[i] = f'    {hashes_name} = "{auto_v2_hash}"\n'

        with open(bundle_hashes_file, "w", newline='\n') as file:
            file.writelines(lines)

        print(f"Updated {hashes_name} value to {auto_v2_hash} in {bundle_hashes_file}")
    else:
        print("Error: auto_v2_hash not found or length is not 10")

# 使用 API key 進行更新
# api_key = os.getenv('civitai_api_key')
update_bundle_hashes()
