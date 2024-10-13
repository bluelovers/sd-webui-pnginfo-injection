from enum import Enum, unique
from typing import Dict, List


@unique
class EnumBundleHashes(Enum):
    # https://civitai.com/models/481009
    C0rn_Fl4k3s = "E5C633CC29"

    #

    # https://civitai.com/models/449400
    lazy_wildcards = "8CE6E6F85B"

    #

    # https://civitai.com/models/138970
    Billions_of_Wildcards = "A872958EED"

    #

    # https://civitai.com/models/272654/wildcards-vault?modelVersionId=317312
    navi_atlas = "2910F6A456"


myBundleHashesSettings: Dict[EnumBundleHashes, List[str]] = {
    EnumBundleHashes.C0rn_Fl4k3s: ['__cf-', '__crea-', '__cornf-', '__cof-'],

    #

    EnumBundleHashes.Billions_of_Wildcards: ['__Bo/', '__properties/'],

    #

    EnumBundleHashes.navi_atlas: ['__navi_atlas/'],
}

