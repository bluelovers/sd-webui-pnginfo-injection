from modules.hashes import sha256_from_cache, calculate_sha256, addnet_hash_safetensors
from modules.cache import cache, dump_cache
import os.path

# def calculate_sha256(filename):
#     hash_sha256 = hashlib.sha256()
#     blksize = 1024 * 1024
#
#     with open(filename, "rb") as f:
#         for chunk in iter(lambda: f.read(blksize), b""):
#             hash_sha256.update(chunk)
#
#     return hash_sha256.hexdigest()

def hashes_auto_v2(filename, title, use_addnet_hash=False):
    hashes = cache("hashes-addnet") if use_addnet_hash else cache("hashes")

    sha256_value = sha256_from_cache(filename, title, use_addnet_hash)
    if sha256_value is not None:
        return sha256_value

    print(f"Calculating sha256 for {filename}: ", end='')
    if use_addnet_hash:
        with open(filename, "rb") as file:
            sha256_value = addnet_hash_safetensors(file)
    else:
        sha256_value = calculate_sha256(filename)
    print(f"{sha256_value}")

    hashes[title] = {
        "mtime": os.path.getmtime(filename),
        "sha256": sha256_value,
    }

    dump_cache()

    return sha256_value
