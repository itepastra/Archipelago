from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region
from .graph import create_graph
from .utils import get_node_name
from .data import START_ELEMENTS

if TYPE_CHECKING:
    from .world import ElementipelagoWorld


def create_and_connect_regions(world: ElementipelagoWorld) -> None:
    create_all_regions(world)
    connect_regions(world)
    graph_regions(world)


def create_all_regions(world: ElementipelagoWorld) -> None:
    menu = Region("Menu", world.player, world.multiworld)
    combining = Region("Combining area", world.player, world.multiworld)

    regions = [menu, combining]

    world.multiworld.regions += regions


def connect_regions(world: ElementipelagoWorld) -> None:
    menu = world.get_region("Menu")
    combining = world.get_region("Combining area")

    menu.connect(combining, "Menu to Combining area")


def graph_regions(world: ElementipelagoWorld) -> None:
    (graph, statuses) = create_graph(
        world.element_amount,
        world.element_amount + world.filler_amount,
        world.graph_seed,
        world.intermediate_amount,
        START_ELEMENTS,
    )

    combining = world.get_region("Combining area")

    output_n = 0
    intermediate_n = 0
    input_n = 0

    number_map = []
    for node in statuses:
        if node == 2:
            output_n += 1
            number_map.append(output_n)
        elif node == 1:
            input_n += 1
            number_map.append(input_n)
        elif node == 0:
            intermediate_n += 1
            number_map.append(intermediate_n)

    ways_to_make: dict[int, list[tuple[int, int]]] = dict()
    for start in range(START_ELEMENTS):
        ways_to_make[start] = []
        name = get_node_name(start, number_map, statuses)
        compound_region = Region(name, world.player, world.multiworld)
        world.multiworld.regions.append(compound_region)

    for in1, in2, output in graph:
        # pre-emptively handle duplicate ways to make an item
        wtm = ways_to_make.get(output)
        if wtm is None:
            ways_to_make[output] = []
            name = get_node_name(output, number_map, statuses)
            compound_region = Region(name, world.player, world.multiworld)
            world.multiworld.regions.append(compound_region)
        if in1 < in2:
            ways_to_make[output].append((in1, in2))
        else:
            ways_to_make[output].append((in2, in1))

    print(ways_to_make)

    for compound, requirements in ways_to_make.items():
        compname = get_node_name(compound, number_map, statuses)
        cp = world.get_region(compname)
        if statuses[compound] == 1:  # the compound is an Element
            print(f"since {compname} is an element, we connect combining with the region {cp}")
            combining.connect(cp, f"Recieve {compname}", lambda state: state.has(compname, world.player))
            continue  # don't add the recepies
        for option in requirements:
            in1name = get_node_name(option[0], number_map, statuses)
            in2name = get_node_name(option[1], number_map, statuses)

            if option[0] == option[1]:
                re1 = world.get_region(in1name)
                entr = re1.connect(cp, f"Craft {compname} using {in1name} twice")
                print(f"created entrance {entr}")
                continue
            re1 = world.get_region(in1name)
            re2 = world.get_region(in2name)

            entr = re1.connect(
                cp,
                f"Craft {compname} using {in1name} and {in2name}",
                lambda state: state.can_reach_region(in2name, world.player),
            )
            print(f"created entrance {entr}")
            world.multiworld.register_indirect_condition(re2, entr)
