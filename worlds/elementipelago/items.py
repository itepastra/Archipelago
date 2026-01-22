from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .data import ELEMENT_AMOUNT, INTERMEDIATE_AMOUNT, START_ELEMENTS, UPGRADE_OFFSET
from .utils import get_element_name, get_intermediate_name

if TYPE_CHECKING:
    from .world import ElementipelagoWorld


ITEM_NAME_TO_ID = (
    {get_element_name(n + 1): n + UPGRADE_OFFSET for n in range(ELEMENT_AMOUNT)}
    | {get_intermediate_name(n + 1): n + UPGRADE_OFFSET + ELEMENT_AMOUNT for n in range(INTERMEDIATE_AMOUNT)}
    | {"TODO": 1, "Progressive Filter": 2, "Progressive Item Limit": 3, "Clutter Trap": 50}
)

DEFAULT_ITEM_CLASSIFICATIONS = {f"Element {n + 1}": ItemClassification.progression for n in range(ELEMENT_AMOUNT)} | {
    "TODO": ItemClassification.filler,
    "Progressive Item Limit": ItemClassification.filler,
    "Progressive Filter": ItemClassification.progression | ItemClassification.useful,
    "Clutter Trap": ItemClassification.trap,
}


class ElementipelagoItem(Item):
    game: str = "Elementipelago"


def get_random_filler_item_name(world: ElementipelagoWorld) -> str:
    return world.random.choice(["Progressive Item Limit"])


def create_item_with_correct_classification(world: ElementipelagoWorld, name: str) -> ElementipelagoItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    return ElementipelagoItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: ElementipelagoWorld) -> None:
    itempool: list[ElementipelagoItem] = [
        world.create_item(f"Element {n + 1}") for n in range(START_ELEMENTS, world.options.element_amount.value)
    ] + [world.create_item("Progressive Filter") for _ in range(2)]

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]  # pyright: ignore[reportAssignmentType]

    world.multiworld.itempool += itempool

    for i in range(START_ELEMENTS):
        world.push_precollected(world.create_item(get_element_name(i + 1)))
