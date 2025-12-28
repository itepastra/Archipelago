from collections.abc import Mapping
from typing import Any

# Imports of base Archipelago modules must be absolute.
from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions
from . import options as elementipelago_options


class ElementipelagoWorld(World):
    """
    Elementipelago is yet another alchemy game, but custom made to work with Archipelago.
    """

    graph_seed: int
    element_amount: int
    filler_amount: int
    intermediate_amount: int

    # only used in fake generation
    explanations: dict[str, tuple[int, str, str, str]]

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

        if hasattr(self.multiworld, "generation_is_fake"):
            if hasattr(self.multiworld, "re_gen_passthrough"):
                if "Elementipelago" in self.multiworld.re_gen_passthrough:
                    slot_data = self.multiworld.re_gen_passthrough["Elementipelago"]
                    self.graph_seed = slot_data["graph_seed"]
                    self.element_amount = slot_data["element_amount"]
                    self.filler_amount = slot_data["filler_amount"]
                    self.intermediate_amount = slot_data["intermediate_amount"]
            self.explanations = {}

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
        return self.options.as_dict("element_amount", "filler_amount", "intermediate_amount") | {
            "graph_seed": self.graph_seed,
        }

    def rule_steps(self, target_name: str, state: CollectionState) -> tuple[list[dict[str, str]], bool]:
        print(f"finding {target_name} in {self.explanations}")
        (rule_type, name, input1, input2) = self.explanations[target_name]
        if rule_type == 1:
            msg = [
                {"type": "text", "text": "Get "},
                {"type": "color", "color": "blue", "_text": f"{name} "},
                {"type": "text", "_text": "from multiworld ("},
            ]
            can_reach = state.has(target_name, self.player)
            if can_reach:
                msg.append({"type": "color", "color": "green", "_text": "True"})
            else:
                msg.append({"type": "color", "color": "red", "_text": "False"})
            msg.append({"type": "text", "_text": ")\n"})
            return msg, can_reach

        lsteps, can_reach_l = self.rule_steps(input1, state)
        rsteps, can_reach_r = self.rule_steps(input2, state)
        msg = [
            {"type": "text", "text": "Craft "},
            {"type": "color", "color": "magenta", "_text": f"{name} "},
            {"type": "text", "_text": "with "},
            {"type": "color", "color": "blue", "_text": f"{input1} "},
            {"type": "text", "_text": "and "},
            {"type": "color", "color": "blue", "_text": f"{input2} "},
            {"type": "text", "_text": "("},
        ]
        if can_reach_l and can_reach_r:
            msg.append({"type": "color", "color": "green", "_text": "True"})
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

        return msg, can_reach_l and can_reach_r

    def explain_rule(self, target_name: str, state: CollectionState) -> list[JSONMessagePart]:
        msg = []
        if target_name.startswith("Make "):
            target_name = target_name.split("Make ", 1)[1]

        steps, _can_reach = self.rule_steps(target_name, state)
        for step in steps:
            if step.get("_text") is not None:
                step["text"] = step["_text"]
                del step["_text"]
            msg.append(JSONMessagePart(step))
        return msg
