# We generate the elements -> locations graph somehow

# Region per location?? -> why not just logic on the locations? Possible multi layer?


from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import ElementipelagoWorld


def create_and_connect_regions(world: ElementipelagoWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: ElementipelagoWorld) -> None:
    menu = Region("Menu", world.player, world.multiworld)
    combining = Region("Combining area", world.player, world.multiworld)

    regions = [menu, combining]

    world.multiworld.regions += regions


def connect_regions(world: ElementipelagoWorld) -> None:
    menu = world.get_region("Menu")
    combining = world.get_region("Combining area")

    menu.connect(combining, "Menu to Combining area")
