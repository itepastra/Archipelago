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

    options_dataclass = options.AntimatterDimensionsOptions
    options = options.AntimatterDimensionsOptions

    location_name_to_id = locations.location_name_to_id()
    item_name_to_id = items.item_name_to_id()

    origin_region_name = "Menu"

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.AntimatterDimensionsItem:
        return items.create_classified_item(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict("minimum_achievements_row", "maximum_achievements_row")
