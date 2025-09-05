from enum import Enum, unique
from typing import Dict, List, TypedDict, Union


@unique
class EnumBundleHashes(Enum):

    #

    # https://civitai.com/models/481009
    C0rn_Fl4k3s = "E5C633CC29"

    #

    # https://civitai.com/models/449400
    lazy_wildcards = "8E60FA3121"

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
    tglove = "C0203E2711"

    #

    # https://civitai.com/models/1068767/otokonokofemboytrap-sex-wildcard
    beloved_otokonoko_sex = "D11A482609"

    #

    # https://civitai.com/models/1487187/cybercelibate-purityguardtm-wildcards
    PurityGuard = "BF6C2FDD38"

    #

    # https://civitai.com/models/1569839/mge-wildcards
    MGE_Wildcards = "38A99F6EDF"

    #

    # https://civitai.com/models/1918220/ii-cosplays-and-more-ii-dark-fantasy-reforge-wildcards-yaml-file-txt
    EroticVibes_1918220 = "5F6BADAAE9"

    #

    # https://civitai.com/models/1925392/ll-cosplays-and-more-ll-medieval-fantasy-reforge-wildcards-yaml-file-txt
    EroticVibes_1925392 = "9EC1C8713B"

    #

    # https://civitai.com/models/1888684/ii-cosplays-and-more-ii-listes-wildcards-fantasy-world
    EroticVibes_1888684 = "1926B1E41B"

    #

class BundleHashSettings(TypedDict, total=False):
    id: Union[str, int]
    patterns: List[str]

myBundleHashesSettings: Dict[EnumBundleHashes, BundleHashSettings] = {

    #

    EnumBundleHashes.lazy_wildcards: {
        "id": 449400,
    },

    #

    EnumBundleHashes.C0rn_Fl4k3s: {
        "id": 481009,
        "patterns": ['__cf-', '__crea-', '__cornf-', '__cof-'],
    },

    #

    EnumBundleHashes.Billions_of_Wildcards: {
        "id": 138970,
        "patterns": ['__Bo/', '__properties/'],
    },

    #

    EnumBundleHashes.navi_atlas: {
        "patterns": ['__navi_atlas/'],
    },

    #

    EnumBundleHashes.chara_creator: {
        "id": 863333,
        "patterns": ['__chara_creator/'],
    },

    #

    EnumBundleHashes.DaemonaVision: {
        "id": 934903,
        "patterns": ['__Vision/'],
    },

    #

    EnumBundleHashes.tglove: {
        "id": 989125,
        "patterns": ['__tglove/'],
    },

    #

    EnumBundleHashes.beloved_otokonoko_sex: {
        "id": 1068767,
        "patterns": ['__beloved-otokonoko-sex/'],
    },

    #

    EnumBundleHashes.PurityGuard: {
        "id": 1487187,
        "patterns": ['__PurityGuard/'],
    },

    #

    EnumBundleHashes.MGE_Wildcards: {
        "id": 1569839,
        "patterns": ['__MGE/'],
    },

    #

    EnumBundleHashes.EroticVibes_1918220: {
        "id": 1918220,
        "patterns": ['__cdfy/'],
    },

    #

    EnumBundleHashes.EroticVibes_1925392: {
        "id": 1925392,
        "patterns": ['__cmfy/'],
    },

    #

    EnumBundleHashes.EroticVibes_1888684: {
        "id": 1888684,
        "patterns": ['__c*fy/'],
    },

    #
}

