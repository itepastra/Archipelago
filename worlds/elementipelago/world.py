from collections.abc import Mapping
from typing import Any

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions
from . import options as elementipelago_options


class ElementipelagoWorld(World):
    """
    Elementipelago is yet another alchemy game, but custom made to work with Archipelago.
    """

    intermediate_count: int
    graph_seed: int

    game = "Elementipelago"

    # web = web_world.ElementipelagoWebWorld()

    options_dataclass = elementipelago_options.ElementipelagoOptions
    options: elementipelago_options.ElementipelagoOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Menu"

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has_all(
            [f"Intermediate {n + 1}" for n in range(self.intermediate_count)], self.player
        )

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.ElementipelagoItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict("element_amount", "filler_amount") | {
            "graph_seed": self.graph_seed,
            "intermediate_count": self.intermediate_count,
        }
