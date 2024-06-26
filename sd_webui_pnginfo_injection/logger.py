
extension_label = "sd-webui-pnginfo-injection"

def my_print(*args, sep=' ', end='\n', file=None, flush=False):
    print(f"[{extension_label}]", *args, sep=sep, end=end, file=file, flush=flush)
