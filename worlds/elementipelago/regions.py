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
    graph = create_graph(
        world.element_amount,
        world.element_amount + world.filler_amount,
        world.graph_seed,
        world.intermediate_amount,
        START_ELEMENTS,
    )

    combining = world.get_region("Combining area")

    ways_to_make: dict[tuple[int, int], list[tuple[int, int]]] = {}

    for node in graph:
        # pre-emptively handle duplicate ways to make an item
        in1 = node[0]
        in2 = node[1]
        output = node[2]
        typ = node[3]
        wtm = ways_to_make.get((output, typ))
        if wtm is None:
            ways_to_make[(output, typ)] = []
            name = get_node_name((output, typ))
            compound_region = Region(f"Can get {name}", world.player, world.multiworld)
            world.multiworld.regions.append(compound_region)
        if in1 < in2:
            ways_to_make[(output, typ)].append((in1, in2))
        else:
            ways_to_make[(output, typ)].append((in2, in1))

    combining = world.get_region("Combining area")

    for compound, requirements in ways_to_make.items():
        compname = get_node_name(compound)
        cp = world.get_region(f"Can get {compname}")
        if compound[1] == 0:  # the compound is an Element
            _ = combining.connect(cp, f"Recieve {compname}", lambda state, cmp=compname: state.has(cmp, world.player))
            continue  # don't add the recepies
        for option in requirements:
            in1name = get_node_name(graph[option[0]][2:])
            in2name = get_node_name(graph[option[1]][2:])

            re1 = world.get_region(f"Can get {in1name}")
            if option[0] == option[1]:
                entr = re1.connect(cp, f"Craft {compname} using {in1name} twice")
                continue

            entr = re1.connect(
                cp,
                f"Craft {compname} using {in1name} and {in2name}",
                lambda state, cmp=in2name: state.can_reach_region(f"Can get {cmp}", world.player),
            )

            re2 = world.get_region(f"Can get {in2name}")
            world.multiworld.register_indirect_condition(re2, entr)
