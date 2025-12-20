from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, options, regions, rules, web_world


class AntimatterDimensionsWorld(World):
    """
    Antimatter Dimensions is an idle game where you make ever more antimatter.
    """

    game = "Antimatter Dimensions"

    web = web_world.AntimatterDimensionsWebWorld()

    location_name_to_id = locations.location_name_to_id()
    item_name_to_id = items.item_name_to_id()

    origin_region_name = "Menu"
