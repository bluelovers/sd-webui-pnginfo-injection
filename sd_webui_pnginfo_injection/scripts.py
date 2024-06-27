import json
from collections import defaultdict

import modules.scripts as scripts

from modules.scripts import PostprocessBatchListArgs
from modules.script_callbacks import ImageSaveParams
from modules.processing import StableDiffusionProcessing, Processed
from modules import script_callbacks

from sd_webui_pnginfo_injection.logger import my_print, extension_label
from sd_webui_pnginfo_injection.on_before_image_saved import add_resource_hashes, _add_resource_hashes_core_dict
from sd_webui_pnginfo_injection.utils import _get_effective_prompt
from sd_webui_pnginfo_injection.utils_webui import get_grid_from_res

class Script(scripts.Script):
    def __init__(self):
        """
        https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Developing-extensions
        https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Developing-extensions#internals-diagram-by-hananbeer
        """
        super().__init__()

        self._init_reset()
        self._hook_event("scripts:init", show_label=False)

        script_callbacks.on_before_image_saved(self.before_image_saved)

    def _init_reset(self):
        self._stat_counter = defaultdict(int)
        self.resource_hashes = {}

    def _hook_event(self, label: str, *args, show_label = True):
        self._stat_counter[label] += 1

        if show_label:
            my_print(label, *args)

    def title(self):
        return extension_label

    def show(self, is_img2img):
        self._hook_event("scripts:show", "is_img2img:", self.is_img2img, is_img2img, show_label=False)
        return scripts.AlwaysVisible

    def before_image_saved(self, image_save_params: ImageSaveParams):
        """
        keep for overwrite https://github.com/civitai/sd_civitai_extension/blob/115cd9c35b0774c90cb9c397ad60ef6a7dac60de/scripts/gen_hashing.py#L77
        """
        self._hook_event("before_image_saved", show_label=False)
        add_resource_hashes(image_save_params)
        pass

    def setup(self, p, *args):
        self._init_reset()

        self._hook_event("setup", f"p.extra_generation_params: {len(p.extra_generation_params)}", show_label=False)
        pass

    def before_process(self, p, *args):
        self._hook_event("before_process", f"p.extra_generation_params: {len(p.extra_generation_params)}", show_label=False)

        try:
            resource_hashes, hashes_is_changed = _add_resource_hashes_core_dict(p.extra_generation_params, p, resource_hashes=self.resource_hashes)

            # my_print("Hashes", json.dumps(self.resource_hashes, indent=2))

            p.extra_generation_params["Hashes"] = resource_hashes
        except Exception as e:
            my_print(f"Error", e)

    def process(self, p, *args):
        self._hook_event("process", f"p.extra_generation_params: {len(p.extra_generation_params)}", show_label=False)

        pass

    def process_batch(self, p, *args, **kwargs):
        self._hook_event("process_batch", f"p.extra_generation_params: {len(p.extra_generation_params)}", show_label=False)
        pass

    def postprocess_batch(self, p, *args, **kwargs):
        self._hook_event("postprocess_batch", f"p.extra_generation_params: {len(p.extra_generation_params)}", show_label=False)
        pass

    def postprocess_image(self, p: StableDiffusionProcessing, processed: Processed):
        """
        p.extra_generation_params only get TI hashes
        but p has sd_model_hash, sd_vae_hash
        """
        self._hook_event("postprocess_image", f"p.extra_generation_params: {len(p.extra_generation_params)}", show_label=False)

        resource_hashes, hashes_is_changed = _add_resource_hashes_core_dict(p.extra_generation_params, p, resource_hashes=self.resource_hashes)

        if len(resource_hashes) <= 0:
            # my_print("Hashes is empty")
            pass
        else:
            # my_print("Hashes", json.dumps(self.resource_hashes, indent=2))
            p.extra_generation_params["Hashes"] = resource_hashes

    def postprocess_batch_list(self, p, pp: PostprocessBatchListArgs, *args, **kwargs):
        self._hook_event("postprocess_batch_list", f"p.extra_generation_params: {len(p.extra_generation_params)}", show_label=False)

    def postprocess_maskoverlay(self, p, pp):
        self._hook_event("postprocess_maskoverlay", f"p.extra_generation_params: {len(p.extra_generation_params)}", show_label=False)

    def postprocess(
            self,
            p,
            res,
            *args,
            **kwargs
    ):
        # grid, index_of_first_image = get_grid_from_res(res)
        self._hook_event("postprocess", f"p.extra_generation_params: {len(p.extra_generation_params)}", json.dumps(self.resource_hashes, indent=2))
        my_print(json.dumps(self._stat_counter, indent=2))

        pass
