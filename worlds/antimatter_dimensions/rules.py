from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.antimatter_dimensions.data import ACHIEVEMENTS
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import AntimatterDimensionsWorld


def set_all_rules(world: AntimatterDimensionsWorld) -> None:
    set_completion_condition(world)


def set_completion_condition(world: AntimatterDimensionsWorld) -> None:
    goal = world.options.goal.value
    victory_lambda = lambda state: False

    if goal == 0:  # infinity
        victory_lambda = (
            lambda state: (
                state.has("Antimatter Dimension", 8) or "Antimatter" not in world.options.dimensionsanity.value
            )
            and state.has("Max Dimboosts", 3)
            and state.has("Max Galaxies", 1)
            and state.has_all(ACHIEVEMENTS[0])
        )
    elif goal == 1:  # eternity
        pass
    elif goal == 2:  # eternity challenges 1x
        pass
    elif goal == 3:  # eternity challenges 5x
        pass
    elif goal == 12:
        victory_lambda = lambda state: state.has_all(
            [
                x
                for i, row in enumerate(ACHIEVEMENTS, 1)
                for x in row
                if (i < world.options.maximum_achievements_row and i >= world.options.minimum_achievements_row)
            ], world.player
        )

    world.multiworld.completion_condition[world.player] = victory_lambda
