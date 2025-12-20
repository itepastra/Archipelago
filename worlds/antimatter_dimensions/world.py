from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, options, regions, rules


class AntimatterDimensionsWorld(World):
    """
    Antimatter Dimensions is an idle game where you make ever more antimatter.
    """

    game = "Antimatter Dimensions"

    location_name_to_id = locations.location_name_to_id()
    item_name_to_id = items.item_name_to_id()

    origin_region_name = "Menu"
