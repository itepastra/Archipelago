from .data import ELEMENT_AMOUNT, LOCATION_AMOUNT, START_ELEMENTS, INTERMEDIATE_AMOUNT
from dataclasses import dataclass

from Options import Range, PerGameCommonOptions, OptionGroup, Toggle


class ElementAmount(Range):
    """
    How many elements are received from Archipelago?
    """

    display_name = "Element amount"
    range_start = START_ELEMENTS
    range_end = ELEMENT_AMOUNT
    default = 100


class FillerAmount(Range):
    """
    How many items are to be produced extra for filler in Archipelago?
    """

    display_name = "Filler amount"

    range_start = 0
    range_end = LOCATION_AMOUNT - ELEMENT_AMOUNT
    default = 100


class IntermediateAmount(Range):
    """
    How many items do you want that aren't included in archipelago directly?
    """

    display_name = "Intermediate amount"

    range_start = 0
    range_end = INTERMEDIATE_AMOUNT
    default = 100


class CompoundsAreIngredients(Toggle):
    """
    Can Compounds (locations) be used as ingredients in recipes as well?
    """

    display_name = "Compounds can be ingredients"


@dataclass
class ElementipelagoOptions(PerGameCommonOptions):
    element_amount: ElementAmount
    filler_amount: FillerAmount
    intermediate_amount: IntermediateAmount
    compounds_are_ingredients: CompoundsAreIngredients


option_groups = [
    OptionGroup("Gameplay Options", [ElementAmount, FillerAmount, IntermediateAmount, CompoundsAreIngredients]),
]
