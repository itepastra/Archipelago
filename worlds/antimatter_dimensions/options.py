from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, DefaultOnToggle, OptionSet


class Goal(Choice):
    """
    Select what counts as a finished game

    - **Infinity:** Goal on the first Infinity
    - **Eternity:** Goal on the first Eternity
    - **Eternity Challenges Once:** Goal on completion of all the eternity challenges at least once.
    - **Eternity Challenges Five:** Goal on completion of all the eternity challenges five times.
    - **Reality:** Goal on the first Reality
    - **Teresa:** Goal on completing Teresa's Reality
    - **Teresa:** Goal on completing Effarig's Reality
    - **Teresa:** Goal on completing The Nameless Ones' Reality
    - **Teresa:** Goal on completing V's Reality
    - **Teresa:** Goal on completing Ra's Reality
    - **Teresa:** Goal on completing Lai'tela's Reality
    - **Pelle:** Goal on defeating Pelle
    - **Achievements:** Goal on completing all the rows of achievements between `Minimum Achievements Row` and `Maximum Achievements Row`
    """

    display_name = "Goal"

    option_Infinity = 0
    option_Eternity = 1
    option_Eternity_challenges_once = 2
    option_Eternity_challenges_five = 3
    option_Reality = 4
    option_Teresa = 5
    option_Effarig = 6
    option_The_Nameless_Ones = 7
    option_V = 8
    option_Ra = 9
    option_Lai_tela = 10
    option_Pelle = 11
    option_achievements = 12


class MinimumAchievementsRow(Range):
    """
    The minimum row of achievements that contains locations.
    All achievements before this row will start unlocked.
    Shouldn't be higher than Maximum Achievements Row
    """

    display_name = "Minimum Achievements Row"

    range_start = 1
    range_end = 18


class MaximumAchievementsRow(Range):
    """
    The last row of achievements to generate locations, achievements past this row
    won't be randomised.
    When the Achievements goal is selected this is the maximum row you have to fill to goal.
    Shouldn't be lower than Minimum Achievements Row
    """

    display_name = "Maximum Achievements Row"

    range_start = 1
    range_end = 18


class ChallengeSanity(OptionSet):
    """
    Challengesanity randomises the various challenges of the game,
    the rewards will appear somewhere in the item pool.

    - Normal: the antimatter dimension challenges
    - Infinity: the infinity challenges
    - Eternity: the eternity challenges
    """

    display_name = "Challengesanity"

    valid_keys = {"Normal", "Infinity", "Eternity"}


class DimensionSanity(OptionSet):
    """
    Unlocking various dimensions happens using items instead of the normal way.
    """

    display_name = "Dimensionsanity"

    valid_keys = {"Antimatter", "Infinity", "Time"}
