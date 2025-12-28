def get_node_name(node: int, number_map: list[int], statuses: list[int]) -> str:
    if statuses[node] == 0:
        return get_intermediate_name(number_map[node])
    if statuses[node] == 1:
        return get_element_name(number_map[node])
    if statuses[node] == 2:
        return get_compound_name(number_map[node])
    return "Illegal Node"


def get_element_name(node: int) -> str:
    return f"Element {node}"


def get_intermediate_name(node: int) -> str:
    return f"Intermediate {node}"


def get_compound_name(node: int) -> str:
    return f"Compound {node}"
