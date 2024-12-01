from enum import Enum, unique
from typing import Dict, List, TypedDict, Union


@unique
class EnumBundleHashes(Enum):

    #

    # https://civitai.com/models/481009
    C0rn_Fl4k3s = "E5C633CC29"

    #

    # https://civitai.com/models/449400
    lazy_wildcards = "566FACEC5D"

    #

    # https://civitai.com/models/138970
    Billions_of_Wildcards = "EBDDB113A8"

    #

    # https://civitai.com/models/272654/wildcards-vault?modelVersionId=317312
    navi_atlas = "2910F6A456"

    #

    # https://civitai.com/models/863333?modelVersionId=969037
    chara_creator = "34CA54C12B"

    #

    # https://civitai.com/models/934903?modelVersionId=1048755
    DaemonaVision = "9EB8C2D539"

    #

    # https://civitai.com/models/989125
    tglove = "C751EFD866"

    #

class BundleHashSettings(TypedDict, total=False):
    id: Union[str, int]
    patterns: List[str]

myBundleHashesSettings: Dict[EnumBundleHashes, BundleHashSettings] = {

    #

    EnumBundleHashes.lazy_wildcards: {
        id: 449400,
    },

    #

    EnumBundleHashes.C0rn_Fl4k3s: {
        id: 481009,
        "patterns": ['__cf-', '__crea-', '__cornf-', '__cof-'],
    },

    #

    EnumBundleHashes.Billions_of_Wildcards: {
        id: 138970,
        "patterns": ['__Bo/', '__properties/'],
    },

    #

    EnumBundleHashes.navi_atlas: {
        "patterns": ['__navi_atlas/'],
    },

    #

    EnumBundleHashes.chara_creator: {
        id: 863333,
        "patterns": ['__chara_creator/'],
    },

    #

    EnumBundleHashes.DaemonaVision: {
        id: 934903,
        "patterns": ['__Vision/'],
    },

    #

    EnumBundleHashes.tglove: {
        id: 989125,
        "patterns": ['__tglove/'],
    },

    #
}

