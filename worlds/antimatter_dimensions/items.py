from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .data import ACHIEVEMENTS

if TYPE_CHECKING:
    from .world import AntimatterDimensionsWorld


def item_name_to_id():
    all_items = {}

    # filler (only time-skip for now)
    all_items["Time Skip"] = 0x0001

    # traps (reset currencies, reset random dimension)
    all_items["Matter Explosion"] = 0x0801
    all_items["Dimensional Reset"] = 0x0802

    # achievements
    achievement_id_offset = 0x1000
    for tier, lst in enumerate(ACHIEVEMENTS):
        for idx, achievement in enumerate(lst):
            all_items[achievement] = achievement_id_offset + 10 * tier + idx

    # upgrades

    # challenge rewards

    return all_items


def get_classification(world: AntimatterDimensionsWorld, item_name: str) -> ItemClassification:
    id = world.item_name_to_id[item_name]

    if 0x0000 < id and id < 0x800:
        # filler items
        return ItemClassification.filler
    if 0x0800 <= id and id < 0x1000:
        # traps
        return ItemClassification.trap

    if 0x1000 <= id and id < 0x2000:
        # achievements, all are progression
        return ItemClassification.progression


class AntimatterDimensionsItem(Item):
    game = "Antimatter Dimensions"


def get_random_filler_item_name(world: AntimatterDimensionsWorld) -> str:
    # TODO: implement traps here
    # TODO: add more types of filler
    # NOTE: remember to use world.random and not importing random!!
    return "Time Skip"


def create_classified_item(world: AntimatterDimensionsWorld, name: str) -> AntimatterDimensionsItem:
    classification = get_classification(world, name)

    return AntimatterDimensionsItem(name, classification, world.item_name_to_id[name], world.player)


def create_all_items(world: AntimatterDimensionsWorld) -> None:
    itempool: list[Item] = []
    precollected: list[Item] = []

    # TODO: add items to the itempool

    for row_idx, row in enumerate(ACHIEVEMENTS, 1):
        # we want to start with all the achievements up to the chosen minimum row
        if row_idx < world.options.minimum_achievements_row:
            for item in row:
                precollected.append(world.create_item(item))
        elif row_idx <= world.options.maximum_achievements_row:
            for item in row:
                itempool.append(world.create_item(item))
        # the achievements after the last row shouldn't be added, since that'd be very over powered

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

    for item in precollected:
        world.push_precollected(item)
