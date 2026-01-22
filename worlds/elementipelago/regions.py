from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region
from .graph import create_graph
from .utils import get_node_name, get_node_name_event
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
    from .items import ElementipelagoItem
    from .locations import ElementipelagoLocation

    graph = create_graph(
        world.element_amount,
        world.compound_amount,
        world.graph_seed,
        world.intermediate_amount,
        START_ELEMENTS,
        world.compounds_are_ingredients,
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
            if typ == 2:
                compound_region.add_event(
                    f"{name} Event", f"{name} Event", location_type=ElementipelagoLocation, item_type=ElementipelagoItem
                )
            world.multiworld.regions.append(compound_region)
        if in1 < in2:
            ways_to_make[(output, typ)].append((in1, in2))
        else:
            ways_to_make[(output, typ)].append((in2, in1))

    if hasattr(world.multiworld, "generation_is_fake"):
        world.recipe_tree = {k: [(graph[a][2:], graph[b][2:]) for a, b in v] for k, v in ways_to_make.items()}

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
            needs_filter_1, in1e = get_node_name_event(graph[option[0]][2:])
            needs_filter_2, in2e = get_node_name_event(graph[option[1]][2:])

            re1 = world.get_region(f"Can get {in1name}")
            re2 = world.get_region(f"Can get {in2name}")

            if needs_filter_1 or needs_filter_2:
                entr = re1.connect(
                    cp,
                    f"Can craft {compname} with {in1e} and {in2e}",
                    lambda state, slf=in1e, cmp=in2e: state.has(
                        "Progressive Filter", world.player, int(needs_filter_1 + needs_filter_2) // 2
                    )
                    and state.has_all([slf, cmp], world.player)
                    and state.has(cmp, world.player),
                )
            else:
                entr = re1.connect(
                    cp,
                    f"Can craft {compname} with {in1e} and {in2e}",
                    lambda state, slf=in1e, cmp=in2e: state.has_all([slf, cmp], world.player),
                )

            world.multiworld.register_indirect_condition(re2, entr)
