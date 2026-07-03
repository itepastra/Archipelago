from Utils import cache_self1
from .base_logic import BaseLogic, BaseLogicMixin
from ..stardew_rule import StardewRule, True_, Glitched
from ..strings.generic_names import Generic
from ..strings.geode_names import Geode
from ..strings.metal_names import Mineral
from ..strings.region_names import Region
from ..strings.season_names import Season
from ..strings.tv_channel_names import Channel


class GlitchedLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.glitched = GlitchedLogic(*args, **kwargs)


class GlitchedLogic(BaseLogic):
    def has_glitch_item(self) -> StardewRule:
        return self.logic.received(Generic.glitch_item)

    def mines_glitched_rule(self) -> StardewRule:
        return Glitched(self.logic.glitched.has_glitch_item() & self.logic.region.can_reach(Region.mines_floor_5), "Mine all floors at once")
