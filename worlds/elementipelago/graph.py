import random
import time


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
) -> list[tuple[int, int, int, int]]:  # (input1, input2, output, type)
    start = time.time()
    # 0 -> Element/Input
    # 1 -> Intermediate
    # 2 -> Compound/Output
    dag_edges: list[tuple[int, int, int, int]] = []
    already_used: set[tuple[int, int]] = set()
    rng = RNG(seed)

    inputs_to_place: list[int] = list(range(1, inputs + 1))
    intermediates_to_place: list[int] = list(range(1, intermediates + 1))
    outputs_to_place: list[int] = list(range(1, outputs + 1))

    # make sure the starting items are placed
    for i in range(1, start_items + 1):
        dag_edges.append((-1, -1, i, 0))
        inputs_to_place.remove(i)

    inputs_placed = 0
    outputs_placed = 0

    to_place_length = len(inputs_to_place) + len(intermediates_to_place) + len(outputs_to_place)
    while to_place_length > 0:
        # print(
        #     f"started new layer, previous: {dag_edges}, to place:\ninputs: {inputs_to_place}\nintermediates: {intermediates_to_place}\noutputs: {outputs_to_place}"
        # )
        previous_items = len(dag_edges)
        # dag_edges contains all the previously placed (and thus "accessible") places
        new_layer: list[tuple[int, int, int, int]] = []
        max_layer_size = min(previous_items * previous_items // 2 - 1, to_place_length - 1)
        if max_layer_size > 0:
            new_layer_size = (rng.get_random() % max_layer_size) + 1
        else:
            new_layer_size = 1
        for _ in range(new_layer_size):
            to_place_type = -1
            while to_place_type == -1:
                typ = rng.get_random() % 3
                if typ == 0 and outputs_placed > inputs_placed and len(inputs_to_place) > 0:  # element
                    to_place_type = 0
                    inputs_placed += 1
                elif typ == 1 and len(intermediates_to_place) > 0:  # intermediate
                    to_place_type = 1
                elif typ == 2 and len(outputs_to_place) > 0:  # output
                    to_place_type = 2
                    outputs_placed += 1

            input1_idx = rng.get_random() % previous_items
            input2_idx = rng.get_random() % previous_items

            while (input1_idx, input2_idx) in already_used:
                input1_idx = rng.get_random() % previous_items
                input2_idx = rng.get_random() % previous_items

            already_used.add((input1_idx, input2_idx))
            already_used.add((input2_idx, input1_idx))

            output_idx = rng.get_random() % len(
                (inputs_to_place, intermediates_to_place, outputs_to_place)[to_place_type]
            )

            output = (inputs_to_place, intermediates_to_place, outputs_to_place)[to_place_type].pop(output_idx)

            new_layer.append((input1_idx, input2_idx, output, to_place_type))

        to_place_length = len(inputs_to_place) + len(intermediates_to_place) + len(outputs_to_place)
        dag_edges.extend(new_layer)

    # print(f"finished generating graph: {dag_edges}")
    end = time.time()
    print(f"generating graph took {end - start}")
    return dag_edges
