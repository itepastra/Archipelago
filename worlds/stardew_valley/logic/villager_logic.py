from ..strings.villager_names import NPC
from .base_logic import BaseLogic, BaseLogicMixin


class VillagerLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.villager = VillagerLogic(*args, **kwargs)


class VillagerLogic(BaseLogic):

    def has(self, npc: str):
        return self.logic.received(npc)

    def has_all(self, *npcs: str):
        return self.logic.and_(*(self.has(npc) for npc in npcs))

    def has_any(self, *npcs: str):
        return self.logic.or_(*(self.has(npc) for npc in npcs))

    def has_any_dateable(self):
        return self.has_any(
            NPC.alex,
            NPC.elliott,
            NPC.harvey,
            NPC.sam,
            NPC.sebastian,
            NPC.shane,
            NPC.abigail,
            NPC.emily,
            NPC.haley,
            NPC.leah,
            NPC.maru,
            NPC.penny,
        )

    def has_introduction(self):
        return self.has_all(
            NPC.alex,
            NPC.elliott,
            NPC.harvey,
            NPC.sam,
            NPC.sebastian,
            NPC.shane,
            NPC.abigail,
            NPC.emily,
            NPC.haley,
            NPC.leah,
            NPC.maru,
            NPC.penny,
            NPC.caroline,
            NPC.clint,
            NPC.demetrius,
            NPC.evelyn,
            NPC.george,
            NPC.gus,
            NPC.jas,
            NPC.jodi,
            NPC.lewis,
            NPC.linus,
            NPC.marnie,
            NPC.pam,
            NPC.pierre,
            NPC.robin,
            NPC.vincent,
            NPC.willy,
        )

    def has_unique(self, count: int):
        return self.logic.count(
            count,
            *(
                self.has(npc)
                for npc in [
                    NPC.alex,
                    NPC.elliott,
                    NPC.harvey,
                    NPC.sam,
                    NPC.sebastian,
                    NPC.shane,
                    NPC.abigail,
                    NPC.emily,
                    NPC.haley,
                    NPC.leah,
                    NPC.maru,
                    NPC.penny,
                    NPC.caroline,
                    NPC.clint,
                    NPC.demetrius,
                    NPC.dwarf,
                    NPC.evelyn,
                    NPC.george,
                    NPC.gus,
                    NPC.jas,
                    NPC.jodi,
                    NPC.kent,
                    NPC.krobus,
                    NPC.leo,
                    NPC.lewis,
                    NPC.linus,
                    NPC.marnie,
                    NPC.pam,
                    NPC.pierre,
                    NPC.robin,
                    NPC.sandy,
                    NPC.vincent,
                    NPC.willy,
                    NPC.wizard,
                ]
            )
        )
