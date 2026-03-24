from ..mods.mod_data import ModNames
from ..options import StardewValleyOptions
from ..strings.villager_names import NPC, ModNPC


def active_npcs(options: StardewValleyOptions) -> list[str]:
    npcs = [
        NPC.abigail,
        NPC.alex,
        NPC.caroline,
        NPC.clint,
        NPC.demetrius,
        NPC.dwarf,
        NPC.elliott,
        NPC.emily,
        NPC.evelyn,
        NPC.george,
        NPC.gus,
        NPC.jas,
        NPC.jodi,
        NPC.kent,
        NPC.krobus,
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
        NPC.gunther,
    ]

    if options.exclude_ginger_island == options.exclude_ginger_island.option_false:
        npcs.append(NPC.leo)

    if ModNames.ayeisha in options.mods:
        npcs.append(ModNPC.ayeisha)
    if ModNames.alec in options.mods:
        npcs.append(ModNPC.alec)
    if ModNames.alecto in options.mods:
        npcs.append(ModNames.alecto)
    if ModNames.delores in options.mods:
        npcs.append(ModNPC.delores)

    return npcs
