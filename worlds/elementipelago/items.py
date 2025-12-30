from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from .data import UPGRADE_OFFSET, ELEMENT_AMOUNT, START_ELEMENTS, INTERMEDIATE_AMOUNT
from .utils import get_element_name, get_intermediate_name

if TYPE_CHECKING:
    from .world import ElementipelagoWorld


ITEM_NAME_TO_ID = {get_element_name(n + 1): n + UPGRADE_OFFSET for n in range(ELEMENT_AMOUNT)} | {get_intermediate_name(n+1): n + UPGRADE_OFFSET + ELEMENT_AMOUNT for n in range(INTERMEDIATE_AMOUNT)} | {"TODO": 1}

DEFAULT_ITEM_CLASSIFICATIONS = {f"Element {n + 1}": ItemClassification.progression for n in range(ELEMENT_AMOUNT)} | {
    "TODO": ItemClassification.filler
}


class ElementipelagoItem(Item):
    game = "Elementipelago"


def get_random_filler_item_name(world: ElementipelagoWorld) -> str:
    # TODO: generate filler
    return "TODO"


def create_item_with_correct_classification(world: ElementipelagoWorld, name: str) -> ElementipelagoItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    return ElementipelagoItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: ElementipelagoWorld) -> None:
    itempool: list[Item] = [
        world.create_item(f"Element {n + 1}") for n in range(START_ELEMENTS, world.options.element_amount.value)
    ]

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

    for i in range(START_ELEMENTS):
        world.push_precollected(world.create_item(get_element_name(i + 1)))
