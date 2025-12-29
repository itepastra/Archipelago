from __future__ import annotations
from worlds.generic.Rules import set_rule

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items
from .graph import create_graph
from .data import UPGRADE_OFFSET, ELEMENT_AMOUNT, LOCATION_AMOUNT
from .utils import get_compound_name, get_element_name, get_intermediate_name

if TYPE_CHECKING:
    from .world import ElementipelagoWorld

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
LOCATION_NAME_TO_ID = {f"Make Compound {n + 1}": n + 1 for n in range(LOCATION_AMOUNT)}


# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class ElementipelagoLocation(Location):
    game = "Elementipelago"


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: ElementipelagoWorld) -> None:
    create_graph_locations(world)


def create_graph_locations(world: ElementipelagoWorld) -> None:
    for compound in range(world.element_amount + world.filler_amount):
        name = get_compound_name(compound + 1)
        lname = f"Make {name}"
        lregion = world.get_region(f"Can get {name}")
        loc = ElementipelagoLocation(world.player, lname, world.location_name_to_id[lname], lregion)
        lregion.locations.append(loc)

    for intermediate in range(world.intermediate_amount):
        name = get_intermediate_name(intermediate + 1)
        lname = f"Make {name}"
        lregion = world.get_region(f"Can get {name}")
        loc = ElementipelagoLocation(world.player, lname, None, lregion)
        item = items.ElementipelagoItem(name, ItemClassification.progression, None, world.player)
        loc.place_locked_item(item)
        lregion.locations.append(loc)
