from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location, Region

from . import items
from .data import ACHIEVEMENTS

if TYPE_CHECKING:
    from .world import AntimatterDimensionsWorld


def location_name_to_id():
    all_locations = {}
    achievement_id_offset = 0x1000
    for tier, lst in enumerate(ACHIEVEMENTS):
        for idx, achievement in enumerate(lst):
            all_locations[achievement] = achievement_id_offset + 10 * tier + idx

    # TODO: challenges (12)
    # TODO: infinity challenges (10)
    # TODO: eternity challenges (5 * 12 = 60)

    # TODO: infinity upgrades
    # TODO: eternity upgrades
    # TODO: time dilation upgrades

    return all_locations


class AntimatterDimensionsLocation(Location):
    game = "Antimatter Dimensions"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: AntimatterDimensionsWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def achievement_tier_to_region_name(tier: int) -> str:
    return f"Achievements {10 * (tier + 1) + 1}-{10 * (tier + 1) + 8}"


def create_regular_locations(world: AntimatterDimensionsWorld) -> None:
    menu = world.get_region("Menu")
    antimatter_dimensions = world.get_region("Antimatter Dimensions")
    infinity_dimensions = world.get_region("Infinity Dimensions")
    time_dimensions = world.get_region("Time Dimensions")

    achievement_regions: list[Region] = [world.get_region(achievement_tier_to_region_name(i)) for i in range(18)]

    for tier, achievement_row in enumerate(ACHIEVEMENTS):
        for achievement in achievement_row:
            achievement_location = AntimatterDimensionsLocation(
                world.player, achievement, world.location_id_to_name[achievement], achievement_regions[tier]
            )
            achievement_regions[tier].locations.append(achievement_location)


def create_events(world: AntimatterDimensionsWorld) -> None:
    pass
