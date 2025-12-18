from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.unfair_flips import *
from worlds.unfair_flips.data import *
from BaseClasses import Location, Region


def generate_locations():
    generated_locations = {}

    # Head flip streak locations
    for head in range(MAX_HEADS - 1):
        generated_locations[f"{head + 1} Heads in a Row"] = 0x100 + head + 1

    # Shop locations
    for head in range(MAX_HEADS // 2):
        generated_locations[f"Heads Chance Purchase {head + 1}"] = 0x200 + head * 4 + 0
        generated_locations[f"Flip Time Purchase {head + 1}"] = 0x200 + head * 4 + 1
        generated_locations[f"Combo Mult Purchase {head + 1}"] = 0x200 + head * 4 + 2
        generated_locations[f"Coin Value Purchase {head + 1}"] = 0x200 + head * 4 + 3

    return generated_locations


class UnfairFlipsLocation(Location):
    game: str = "Unfair Flips"


def create_location(player: int, reg: Region, name: str, code: int):
    location = UnfairFlipsLocation(player, name, code, reg)
    reg.locations.append(location)


def create_locations(world: UnfairFlipsWorld, reg: Region, gate_index: int):
    # 1 | 2 3 | 4 5 | 6 7 | 8 9 | 10
    # 1 | 2 3 | 4 5 | 6 7 | 8 9 | 10 11
    if gate_index == 0:
        heads_name = "1 Heads in a Row"
        heads_id = world.location_name_to_id[heads_name]
        create_location(world.player, reg, heads_name, heads_id)
    else:
        head_1 = 1 + (gate_index - 1) * 2 + 1
        if head_1 < world.options.required_heads:
            heads_name = f"{head_1} Heads in a Row"
            heads_id = world.location_name_to_id[heads_name]
            create_location(world.player, reg, heads_name, heads_id)
        elif head_1 == world.options.required_heads:
            world.create_event(reg.name, f"{head_1} Heads in a Row", f"{head_1} Heads in a Row")
            world.multiworld.completion_condition[world.player] = lambda state: state.has(f"{head_1} Heads in a Row", world.player)

        head_2 = 1 + (gate_index - 1) * 2 + 2
        if head_2 < world.options.required_heads:
            heads_name = f"{head_2} Heads in a Row"
            heads_id = world.location_name_to_id[heads_name]
            create_location(world.player, reg, heads_name, heads_id)
        elif head_2 == world.options.required_heads:
            world.create_event(reg.name, f"{head_2} Heads in a Row", f"{head_2} Heads in a Row")
            world.multiworld.completion_condition[world.player] = lambda state: state.has(f"{head_2} Heads in a Row", world.player)

    heads_chance_name = f"Heads Chance Purchase {gate_index + 1}"
    heads_chance_id = world.location_name_to_id[heads_chance_name]
    create_location(world.player, reg, heads_chance_name, heads_chance_id)

    flip_time_name = f"Flip Time Purchase {gate_index +1}"
    flip_time_id = world.location_name_to_id[flip_time_name]
    create_location(world.player, reg, flip_time_name, flip_time_id)

    combo_mult_name = f"Combo Mult Purchase {gate_index +1}"
    combo_mult_id = world.location_name_to_id[combo_mult_name]
    create_location(world.player, reg, combo_mult_name, combo_mult_id)

    coin_value_name = f"Coin Value Purchase {gate_index +1}"
    coin_value_id = world.location_name_to_id[coin_value_name]
    create_location(world.player, reg, coin_value_name, coin_value_id)
