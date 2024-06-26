import modules.scripts as scripts
from modules import script_callbacks
from modules.script_callbacks import ImageSaveParams

from sd_webui_pnginfo_injection.logger import my_print, extension_label
from sd_webui_pnginfo_injection.on_before_image_saved import add_resource_hashes, _add_resource_hashes_core_dict
from sd_webui_pnginfo_injection.utils_webui import get_grid_from_res


class Script(scripts.Script):
    def __init__(self):
        """
        https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Developing-extensions
        https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Developing-extensions#internals-diagram-by-hananbeer
        """

        script_callbacks.on_before_image_saved(self.before_image_saved)

    def title(self):
        return extension_label

    def before_image_saved(self, image_save_params: ImageSaveParams):
        add_resource_hashes(image_save_params)

    def process_batch(selfself, p, *args, **kwargs):
        resource_hashes, hashes_is_changed = _add_resource_hashes_core_dict(p.extra_generation_params)

        if hashes_is_changed:
            my_print("Hashes is update", resource_hashes)
            p.extra_generation_params["Hashes"] = resource_hashes

    def postprocess(
            self,
            p,
            res,
            *args,
            **kwargs
    ):
        grid, index_of_first_image = get_grid_from_res(res)
