import json
import unittest

from sd_webui_pnginfo_injection.on_before_image_saved import add_resource_hashes, _add_resource_hashes_core_parameters
from sd_webui_pnginfo_injection.utils import try_parse_load, dict_to_infotext


class MyTestCase(unittest.TestCase):
    def test_something(self):
        res = {}
        val = try_parse_load(res, "Hashes", default_val={})
        self.assertEqual(val, {})  # add assertion here

        val = try_parse_load(res, "Hashes")
        self.assertEqual(val, None)  # add assertion here
    def test_something2(self):
        res = {
            "Hashes": '{"vae": "df3c506e51", "embed:Tower13_Gizelle": "9ece223c52", "embed:EasyNegative": "c74b4e810b", "model": "0a880e98ab"}'
        }
        val = try_parse_load(res, "Hashes")
        self.assertEqual(val, {"vae": "df3c506e51", "embed:Tower13_Gizelle": "9ece223c52", "embed:EasyNegative": "c74b4e810b", "model": "0a880e98ab"})

    def test_something3(self):
        obj = lambda: None
        obj.pnginfo = lambda: None
        obj.pnginfo.parameters = 'Steps: 20, Sampler: DPM++ 2M, Schedule type: Karras, CFG scale: 7, Seed: 557152044, Size: 768x512, Model hash: 0a880e98ab, Model: meinacetusorionmix_v10, VAE hash: df3c506e51, VAE: kl-f8-anime2.ckpt, Hypertile U-Net: True, Hypertile VAE: True, ADetailer model: hand_yolov8n.pt, ADetailer confidence 2nd: 0.3, ADetailer dilate erode 2nd: 4, ADetailer mask blur 2nd: 4, ADetailer denoising strength 2nd: 0.4, ADetailer inpaint only masked 2nd: True, ADetailer inpaint padding 2nd: 32, ADetailer ControlNet model 2nd: Passthrough, ADetailer version: 24.6.0, Template Seeds: 557152044, Template Seeds Sub: 1298678300, TI hashes: "Tower13_Gizelle: 9ece223c52f8, EasyNegative: c74b4e810b03", Hardware Info: "RTX 3060 Ti 8GB, i7-13700, 32GB RAM", Time taken: 22.5 sec., Version: v1.9.4-191-g6ca0466e, Hashes: {"vae": "df3c506e51", "embed:Tower13_Gizelle": "9ece223c52", "embed:EasyNegative": "c74b4e810b", "model": "0a880e98ab"}'

        res, resource_hashes, hashes_is_changed = _add_resource_hashes_core_parameters(obj)
        self.assertEqual(resource_hashes, {"vae": "df3c506e51", "embed:Tower13_Gizelle": "9ece223c52", "embed:EasyNegative": "c74b4e810b", "model": "0a880e98ab"})

        res["Hashes"] = json.dumps(resource_hashes)
        parameters = dict_to_infotext(res)

        self.maxDiff = None

        self.assertEqual(obj.pnginfo.parameters, parameters.strip('\u200b\n'))
        self.assertIn('embed:EasyNegative', parameters)

        obj2 = lambda: None
        obj2.pnginfo = lambda: None
        obj2.pnginfo.parameters = 'Steps: 20, Sampler: DPM++ 2M, Schedule type: Karras, CFG scale: 7, Seed: 557152044, Size: 768x512, Model hash: 0a880e98ab, Model: meinacetusorionmix_v10, VAE hash: df3c506e51, VAE: kl-f8-anime2.ckpt, Hypertile U-Net: True, Hypertile VAE: True, ADetailer model: hand_yolov8n.pt, ADetailer confidence 2nd: 0.3, ADetailer dilate erode 2nd: 4, ADetailer mask blur 2nd: 4, ADetailer denoising strength 2nd: 0.4, ADetailer inpaint only masked 2nd: True, ADetailer inpaint padding 2nd: 32, ADetailer ControlNet model 2nd: Passthrough, ADetailer version: 24.6.0, Template Seeds: 557152044, Template Seeds Sub: 1298678300, TI hashes: "Tower13_Gizelle: 9ece223c52f8, EasyNegative: c74b4e810b03", Hardware Info: "RTX 3060 Ti 8GB, i7-13700, 32GB RAM", Time taken: 22.5 sec., Version: v1.9.4-191-g6ca0466e'

        res2, resource_hashes2, hashes_is_changed2 = _add_resource_hashes_core_parameters(obj2)

        res2["Hashes"] = json.dumps(resource_hashes2)
        parameters2 = dict_to_infotext(res2)

        self.assertIn(res2["Hashes"], parameters2)


if __name__ == '__main__':
    unittest.main()
