from collections.abc import Mapping
from typing import Any

# Imports of base Archipelago modules must be absolute.
from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions, utils
from . import options as elementipelago_options


class ElementipelagoWorld(World):
    """
    Elementipelago is yet another alchemy game, but custom made to work with Archipelago.
    """

    graph_seed: int
    element_amount: int
    filler_amount: int
    intermediate_amount: int
    recipe_tree: dict[tuple[int, int], list[tuple[tuple[int, int], tuple[int, int]]]]
    compounds_are_ingredients: bool

    game = "Elementipelago"

    # web = web_world.ElementipelagoWebWorld()

    options_dataclass = elementipelago_options.ElementipelagoOptions
    options: elementipelago_options.ElementipelagoOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Menu"

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        return slot_data

    ut_can_gen_without_yaml = True

    def generate_early(self) -> None:
        self.graph_seed = self.random.randint(5000000, 100000000)
        self.element_amount = self.options.element_amount.value
        self.filler_amount = self.options.filler_amount.value
        self.intermediate_amount = self.options.intermediate_amount.value
        self.compounds_are_ingredients = self.options.compounds_are_ingredients.value

        if hasattr(self.multiworld, "generation_is_fake"):
            if hasattr(self.multiworld, "re_gen_passthrough"):
                if "Elementipelago" in self.multiworld.re_gen_passthrough:
                    slot_data = self.multiworld.re_gen_passthrough["Elementipelago"]
                    self.graph_seed = slot_data["graph_seed"]
                    self.element_amount = slot_data["element_amount"]
                    self.filler_amount = slot_data["filler_amount"]
                    self.intermediate_amount = slot_data["intermediate_amount"]
                    self.compounds_are_ingredients = slot_data["compounds_are_ingredients"]

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has_all(
            [f"Intermediate {n + 1}" for n in range(self.intermediate_amount)], self.player
        )

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.ElementipelagoItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "element_amount", "filler_amount", "intermediate_amount", "compounds_are_ingredients"
        ) | {
            "graph_seed": self.graph_seed,
        }

    def rule_steps(self, target_key: tuple[int, int], state: CollectionState) -> tuple[list[dict[str, str]], bool]:
        name = utils.get_node_name(target_key)
        if target_key[1] == 0:
            return (
                [
                    {"type": "text", "text": "Get "},
                    {"type": "color", "color": "blue", "_text": f"{name} "},
                    {"type": "text", "_text": "from multiworld ("},
                    (
                        {"type": "color", "color": "green", "_text": "True"}
                        if state.has(name, self.player)
                        else {"type": "color", "color": "red", "_text": "False"}
                    ),
                    {"type": "text", "_text": ")\n"},
                ],
                state.has(name, self.player),
            )

        if self.recipe_tree.get(target_key) is None:
            return ([{"type": "color", "color": "red", "_text": "Could not find item in world"}], False)
        ltup = self.recipe_tree[target_key]

        msg = [
            {"type": "text", "text": "Craft "},
            {"type": "color", "color": "magenta", "_text": f"{name}\n"},
        ]

        can_craft = False

        for (in1num, in1type), (in2num, in2type) in ltup:
            lname = utils.get_node_name((in1num, in1type))
            rname = utils.get_node_name((in2num, in2type))

            lsteps, can_reach_l = self.rule_steps((in1num, in1type), state)
            rsteps, can_reach_r = self.rule_steps((in2num, in2type), state)

            msg.extend(
                [
                    {"type": "text", "text": "With "},
                    {"type": "color", "color": "blue", "_text": f"{lname} "},
                    {"type": "text", "_text": "and "},
                    {"type": "color", "color": "blue", "_text": f"{rname} "},
                    {"type": "text", "_text": "("},
                ]
            )
            if can_reach_l and can_reach_r:
                msg.append({"type": "color", "color": "green", "_text": "True"})
                can_craft = True
            else:
                msg.append({"type": "color", "color": "red", "_text": "False"})
            msg.append({"type": "text", "_text": ")\n"})

            for rule in lsteps:
                if rule.get("text") is None:
                    msg.append(rule)
                    continue
                dc = dict(rule.items())
                dc["text"] = f"    {dc['text']}"
                msg.append(dc)

            for rule in rsteps:
                if rule.get("text") is None:
                    msg.append(rule)
                    continue
                dc = dict(rule.items())
                dc["text"] = f"    {dc['text']}"
                msg.append(dc)

        return msg, can_craft

    def explain_rule(self, target_name: str, state: CollectionState) -> list[JSONMessagePart]:
        # Universal Tracker may pass names like "Make X" or "Can get X".
        name = target_name.strip()
        print(f"I am explaining how to get {name}")
        for prefix in ("Make ", "Can get "):
            if name.startswith(prefix):
                name = name[len(prefix) :].strip()
        print(f"after stripping I have {name}")

        def name_to_key(nm: str) -> tuple[int, int] | None:
            # Returns (type, number)
            parts = nm.split()
            print(f"the parts are {parts}")
            if len(parts) != 2:
                return None
            kind, num_s = parts
            try:
                num = int(num_s)
            except ValueError:
                return None
            if kind == "Element":
                return (num, 0)
            if kind == "Intermediate":
                return (num, 1)
            if kind == "Compound":
                return (num, 2)
            return None

        root = name_to_key(name)
        if root is None:
            return [{"text": f"Don't know how to explain '{target_name}'."}]

        msg = []
        steps, _can_reach = self.rule_steps(root, state)
        for step in steps:
            if step.get("_text") is not None:
                step["text"] = step["_text"]
                del step["_text"]
            msg.append(JSONMessagePart(step))
        return msg
