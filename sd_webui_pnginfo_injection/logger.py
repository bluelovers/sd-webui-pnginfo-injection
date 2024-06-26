
extension_label = "sd-webui-pnginfo-injection"

def my_print(*args, sep=' ', end='\n', file=None, flush=False):
    if args:
        print(f"[{extension_label}] {args[0]}", *args[1:], sep=sep, end=end, file=file, flush=flush)
    else:
        print(f"[{extension_label}]", sep=sep, end=end, file=file, flush=flush)
