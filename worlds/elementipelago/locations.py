from __future__ import annotations
from worlds.generic.Rules import set_rule

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items
from .graph import create_graph
from .data import UPGRADE_OFFSET, ELEMENT_AMOUNT, LOCATION_AMOUNT

if TYPE_CHECKING:
    from .world import ElementipelagoWorld

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
LOCATION_NAME_TO_ID = {f"Make Compound {n + 1}": n + 1 for n in range(LOCATION_AMOUNT)}


# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class ElementipelagoLocation(Location):
    game = "Elementipelago"


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: ElementipelagoWorld) -> None:
    create_graph_locations(world)


def get_name_thing(idx, nmap, statuses):
    if statuses[idx] == 2:
        return f"Compound {nmap[idx] + 1}"
    elif statuses[idx] == 1:
        return f"Element {nmap[idx] + 1}"
    elif statuses[idx] == 0:
        return f"Intermediate {nmap[idx] + 1}"
    else:
        return f"ERROR: {statuses[idx]} is not a valid status"


def make_rule(in1, in2, nmap, status, player):
    lname = get_name_thing(in1, nmap, status)
    rname = get_name_thing(in2, nmap, status)
    print(f"making rule between {lname} and {rname}")
    if status[in1] == 0 and status[in2] == 0:
        return lambda status: status.has(lname, player) and status.has(rname, player)
    elif status[in1] == 0 and status[in2] == 1:
        return lambda status: status.has(lname, player) and status.has(rname, player)
    elif status[in1] == 0 and status[in2] == 2:
        return lambda status: status.has(lname, player) and status.can_reach_location(f"Make {rname}", player)
    elif status[in1] == 1 and status[in2] == 0:
        return lambda status: status.has(lname, player) and status.has(rname, player)
    elif status[in1] == 1 and status[in2] == 1:
        return lambda status: status.has(lname, player) and status.has(rname, player)
    elif status[in1] == 1 and status[in2] == 2:
        return lambda status: status.has(lname, player) and status.can_reach_location(f"Make {rname}", player)
    elif status[in1] == 2 and status[in2] == 0:
        return lambda status: status.can_reach_location(f"Make {lname}", player) and status.has(rname, player)
    elif status[in1] == 2 and status[in2] == 1:
        return lambda status: status.can_reach_location(f"Make {lname}", player) and status.has(rname, player)
    elif status[in1] == 2 and status[in2] == 2:
        return lambda status: status.can_reach_location(f"Make {lname}", player) and status.can_reach_location(
            f"Make {rname}", player
        )
    else:
        print(f"Couldn't make rule for {in1}, {in2}, {nmap}, {status}")
        return lambda status: False


def create_graph_locations(world: ElementipelagoWorld) -> None:
    seed = world.random.randint(0, 1000000)

    (graph, statuses) = create_graph(
        world.options.element_amount.value,
        world.options.element_amount.value + world.options.filler_amount.value,
        seed,
        intermediates=world.options.intermediate_amount.value,
    )
    print(graph)
    print(statuses)

    combining = world.get_region("Combining area")

    output_n = 0
    intermediate_n = 0
    input_n = 0

    number_map = []
    for node in statuses:
        if node == 2:
            number_map.append(output_n)
            output_n += 1
        elif node == 1:
            number_map.append(input_n)
            input_n += 1
        elif node == 0:
            number_map.append(intermediate_n)
            intermediate_n += 1

    world.intermediate_count = intermediate_n

    for input1, input2, output in graph:
        name = get_name_thing(output, number_map, statuses)
        if statuses[output] == 2:  # is a location recipe
            lname = f"Make {name}"
            loc = ElementipelagoLocation(world.player, lname, world.location_name_to_id[lname], combining)
            combining.locations.append(loc)
            set_rule(loc, make_rule(input1, input2, number_map, statuses, world.player))
        elif statuses[output] == 1:  # is an element
            print(f"{output} is an Element, so no rule")
            pass
        elif statuses[output] == 0:  # is an intermediate, needs event
            loc = ElementipelagoLocation(world.player, f"Make {name}", None, combining)
            combining.locations.append(loc)
            inter_item = items.ElementipelagoItem(name, ItemClassification.progression, None, world.player)
            loc.place_locked_item(inter_item)
            set_rule(loc, make_rule(input1, input2, number_map, statuses, world.player))
