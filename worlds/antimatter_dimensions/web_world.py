from BaseClasses import Tutorial
from world.AutoWorld import WebWorld

from .options import option_groups, option_presets


class AntimatterDimensionsWebWorld(WebWorld):
    game = "Antimatter Dimensions"

    theme = "grassFlowers"

    rich_text_options_doc = True

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Antimatter Dimensions for MultiWorld",
        "English",
        "setup_en.md",
        "setup/en",
        ["itepastra"],
    )

    tutorials = [setup_en]

    option_groups = option_groups
    option_presets = option_presets
