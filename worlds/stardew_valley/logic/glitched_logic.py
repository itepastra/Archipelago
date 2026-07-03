from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from ..stardew_rule import StardewRule, True_, Glitched, NotReceived
from ..strings.generic_names import Generic
from ..strings.geode_names import Geode
from ..strings.metal_names import Mineral
from ..strings.region_names import Region, LogicRegion
from ..strings.season_names import Season
from ..strings.tool_names import Tool, ToolMaterial


class GlitchedLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.glitched = GlitchedLogic(*args, **kwargs)


class GlitchedLogic(BaseLogic):
    def has_glitch_item(self) -> StardewRule:
        return self.logic.received(Generic.glitch_item)

    def mines_glitched_rule(self) -> StardewRule:
        return Glitched(self.logic.glitched.has_glitch_item() & self.logic.region.can_reach(Region.mines_floor_5), "Mine all floors at once")

    def death_glitched_rule(self) -> StardewRule:
        return Glitched(self.logic.glitched.has_glitch_item(), "Die to respawn at Hospital")

    def glitched_money(self) -> StardewRule:
        pierre_forage_rule = self.logic.region.can_reach_all(Region.pierre_shop, Region.forest)
        willy_rule = self.logic.region.can_reach_all(Region.fish_shop, LogicRegion.fishing)
        clint_rule = self.logic.region.can_reach_all(Region.blacksmith_shop, Region.mines_floor_5) & self.logic.tool.has_tool(Tool.pickaxe)
        robin_rule = self.logic.region.can_reach_all(Region.carpenter_shop, Region.secret_woods) & self.logic.tool.has_tool(Tool.axe, ToolMaterial.copper)

        selling_any_rule = pierre_forage_rule | willy_rule | clint_rule | robin_rule
        return Glitched(self.logic.glitched.has_glitch_item() & selling_any_rule, "Make a lot of money in the shops")

    def joja_glitched_rule(self) -> StardewRule:
        return Glitched(self.logic.glitched.has_glitch_item() &
                        NotReceived("Progressive Movie Theater", self.player, 1), "Can shop at jojamart still")
