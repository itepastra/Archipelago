def get_node_name(node: tuple[int, int]) -> str:
    if node[1] == 0:
        return get_element_name(node[0])
    if node[1] == 1:
        return get_intermediate_name(node[0])
    if node[1] == 2:
        return get_compound_name(node[0])
    return "Illegal Node"


def get_node_name_event(node: tuple[int, int]) -> tuple[int, str]:
    if node[1] == 0:
        return 0, get_element_name(node[0])
    if node[1] == 1:
        return 1, get_intermediate_name(node[0])
    if node[1] == 2:
        return 2, f"{get_compound_name(node[0])} Event"
    return 0, "Illegal Node"


def get_element_name(node: int) -> str:
    return f"Element {node}"


def get_intermediate_name(node: int) -> str:
    return f"Intermediate {node}"


def get_compound_name(node: int) -> str:
    return f"Compound {node}"
