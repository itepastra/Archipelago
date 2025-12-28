from typing import Set

# from .data import START_ELEMENTS
import random


MASK = 0xFFFFFFFFFFFFFFFF


class RNG:
    seed_x: int
    seed_y: int

    def __init__(self, seed: int) -> None:
        self.seed_x = (seed) & MASK
        self.seed_y = (seed << 1) & MASK

    def get_random(self) -> int:
        x = self.seed_x
        y = self.seed_y
        self.seed_x = self.seed_y
        x ^= (x << 23) & MASK
        x ^= x >> 17
        x ^= y
        self.seed_y = (x + y) & MASK
        return x & MASK


def create_graph(
    inputs: int, outputs: int, seed: int, intermediates: int, start_items: int
) -> tuple[list[tuple[int, int, int]], list[int]]:  # (input1, input2, output)
    dag_edges: list[tuple[int, int, int]] = []
    already_used: Set[tuple[int, int]] = set()
    statuses = []  # 0 = intermediate, 1 = input, 2 = output
    items_len = inputs + intermediates + outputs
    rng = RNG(seed)
    for i in range(start_items):
        statuses.append(1)

    # make a hyper-DAG so there is at least 1 recipe to make each item
    for i in range(start_items, items_len):
        while True:
            item1 = rng.get_random() % i
            item2 = rng.get_random() % i
            if (item1, item2) not in already_used and (item2, item1) not in already_used:
                already_used.add((item1, item2))
                break
        output = i
        dag_edges.append((item1, item2, output))
        statuses.append(0)

    r_items_len = items_len - start_items
    inputs_to_place = inputs - start_items
    while inputs_to_place > 0:
        idx = (rng.get_random() % r_items_len) + start_items
        if statuses[idx] != 0:
            continue
        statuses[idx] = 1
        inputs_to_place -= 1

    outputs_to_place = outputs
    while outputs_to_place > 0:
        idx = (rng.get_random() % r_items_len) + start_items
        if statuses[idx] != 0:
            continue
        statuses[idx] = 2
        outputs_to_place -= 1

    return (dag_edges, statuses)
