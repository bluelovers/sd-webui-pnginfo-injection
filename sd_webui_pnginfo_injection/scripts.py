import modules.scripts as scripts

from modules.script_callbacks import ImageSaveParams
from modules.processing import StableDiffusionProcessing, Processed
from modules import script_callbacks

from sd_webui_pnginfo_injection.logger import my_print, extension_label
from sd_webui_pnginfo_injection.on_before_image_saved import add_resource_hashes, _add_resource_hashes_core_dict
from sd_webui_pnginfo_injection.utils_webui import get_grid_from_res


class Script(scripts.Script):
    def __init__(self):
        """
        https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Developing-extensions
        https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Developing-extensions#internals-diagram-by-hananbeer
        """
        super().__init__()
        my_print("scripts:init", "is_img2img:", self.is_img2img)

        script_callbacks.on_before_image_saved(self.before_image_saved)

    def title(self):
        return extension_label

    def show(self, is_img2img):
        my_print("scripts:show", "is_img2img:", self.is_img2img, is_img2img)
        return scripts.AlwaysVisible

    def before_image_saved(self, image_save_params: ImageSaveParams):
        """
        keep for overwrite https://github.com/civitai/sd_civitai_extension/blob/115cd9c35b0774c90cb9c397ad60ef6a7dac60de/scripts/gen_hashing.py#L77
        """
        # my_print("before_image_saved")
        add_resource_hashes(image_save_params)
        pass

    def process(self, p):
        my_print("process")

        resource_hashes, hashes_is_changed = _add_resource_hashes_core_dict(p.extra_generation_params, p)

        if hashes_is_changed:
            p.extra_generation_params["Hashes"] = resource_hashes

        pass

    def process_batch(self, p, *args, **kwargs):
        # my_print("process_batch")
        pass

    def postprocess_batch(self, p, *args, **kwargs):
        # my_print("postprocess_batch")
        pass

    def postprocess_image(self, p: StableDiffusionProcessing, processed: Processed):
        """
        p.extra_generation_params only get TI hashes
        but p has sd_model_hash, sd_vae_hash
        """
        my_print("postprocess_image")

        resource_hashes, hashes_is_changed = _add_resource_hashes_core_dict(p.extra_generation_params, p)

        if len(resource_hashes) <= 0:
            my_print("Hashes is empty")
        elif not hashes_is_changed:
            my_print("Hashes is not changed", resource_hashes)
        else:
            my_print("Hashes is update", resource_hashes)
            p.extra_generation_params["Hashes"] = resource_hashes

    def postprocess(
            self,
            p,
            res,
            *args,
            **kwargs
    ):
        # grid, index_of_first_image = get_grid_from_res(res)
        # my_print("postprocess")
        pass
