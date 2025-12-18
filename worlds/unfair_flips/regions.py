from __future__ import annotations

import math
from typing import Dict, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.unfair_flips import *
from worlds.unfair_flips.locations import *
from BaseClasses import Region, Entrance


def connect_regions(world: UnfairFlipsWorld, from_name: str, to_name: str, entrance_name: str) -> Entrance:
    entrance_region = world.multiworld.get_region(from_name, world.player)
    exit_region = world.multiworld.get_region(to_name, world.player)
    return entrance_region.connect(exit_region, entrance_name)


def create_region(world: UnfairFlipsWorld, name: str, gate_index=None):
    reg = Region(name, world.player, world.multiworld)
    world.multiworld.regions.append(reg)
    if gate_index is not None:
        create_locations(world, reg, gate_index)


def create_regions(world: UnfairFlipsWorld):
    create_region(world, "Menu")
    for gate_index in range(math.ceil(world.options.required_heads / 2)):
        create_region(world, f"Fairness Gate {gate_index + 1}", gate_index)


def connect_all_regions(world: UnfairFlipsWorld):
    for gate_index in range(math.ceil(world.options.required_heads / 2)):
        entrance: Entrance
        if gate_index == 0:
            entrance = connect_regions(world, "Menu", "Fairness Gate 1", "Menu -> Fairness Gate 1")
        else:
            entrance = connect_regions(world, f"Fairness Gate {gate_index}", f"Fairness Gate {gate_index + 1}", f"Fairness Gate {gate_index} -> Fairness Gate {gate_index + 1}" )
        entrance.access_rule = lambda state, gate=gate_index: state.has(f"Progressive Fairness", world.player, gate) and state.has(f"Heads+", world.player, max(gate - 1, 0))