from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region
from worlds.antimatter_dimensions.data import ACHIEVEMENT_ROW_COUNT, ACHIEVEMENTS

if TYPE_CHECKING:
    from .world import AntimatterDimensionsWorld


def create_and_connect_regions(world: AntimatterDimensionsWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: AntimatterDimensionsWorld) -> None:
    menu = Region("Menu", world.player, world.multiworld)
    achievement_regions = create_achievement_regions(world)

    dimension_regions = create_dimension_regions(world)

    regions = [menu, *achievement_regions]

    world.multiworld.regions += regions


def connect_regions(world: AntimatterDimensionsWorld) -> None:
    menu = world.get_region("Menu")

    achievement_regions = [
        world.get_region(achievement_tier_to_region_name(tier)) for tier in range(ACHIEVEMENT_ROW_COUNT)
    ]

    prev_achievement_region: Region | None = None
    for i, achievement_region in enumerate(achievement_regions):
        if i == 0:
            _ = menu.connect(achievement_region, "Menu to Achievement Row 1")
            prev_achievement_region = achievement_region
        else:
            assert prev_achievement_region is not None, (
                "prev_achievement_region wasn't set in iteration i==0 but it should"
            )
            entrance = prev_achievement_region.connect(
                achievement_region,
                f"Achievement Row {i} to Achievement Row {i + 1}",
                lambda state, tier=i: state.has_from_list_unique(ACHIEVEMENTS[tier], world.player, 6),
            )
            prev_achievement_region = achievement_region


def create_achievement_regions(world: AntimatterDimensionsWorld) -> list[Region]:
    return [
        Region(achievement_tier_to_region_name(tier), world.player, world.multiworld)
        for tier in range(ACHIEVEMENT_ROW_COUNT)
    ]


def create_dimension_regions(world: AntimatterDimensionsWorld) -> list[Region]:
    return (
        [Region(f"Antimatter dimension {tier + 1}", world.player, world.multiworld) for tier in range(8)]
        + [Region(f"Infinity dimension {tier + 1}", world.player, world.multiworld) for tier in range(8)]
        + [Region(f"Time dimension {tier + 1}", world.player, world.multiworld) for tier in range(8)]
    )


def achievement_tier_to_region_name(tier: int) -> str:
    return f"Achievements {10 * (tier + 1) + 1}-{10 * (tier + 1) + 8}"
