init python:
    # Note: We may get this from grouping traits, but that still feels a bit clumsy atm.
    base_trait_presets = {
    "Warrior": (["Warrior"], ["Knight"]),
    "Caster": (["Mage"], ["Mage"], ["Mage", "Shooter"], ["Knight", "Mage"]),
    "Assassin": (["Assassin"], ["Assassin"], ["Assassin", "Warrior"]),
    "Shooter": (["Shooter"], ["Shooter"], ["Shooter", "Mage"]),
    "Healer": (["Healer"], ["Healer", "Mage"], ["Healer", "Maid"], ["Knight", "Healer"]),
    "SIW": (["Prostitute", "Stripper"], ),
    "Prostitute": (["Prostitute"], ),
    "Stripper": (["Stripper"], ["Stripper", "Maid"]),
    "Maid": (["Maid"], ["Barmaid"], ["Cleaner"]),
    "Specialist": (["Manager", "Barmaid"], ["Manager", "Stripper"], ["Manager", "Healer"],
                   ["Manager", "Mage"]),
    "Manager": (["Manager"], )
    }
    btp = base_trait_presets
    btp["Combatant"] = btp["Warrior"] + btp["Caster"] + btp["Assassin"] + btp["Shooter"]
    del(btp)

    base_traits_groups = {"Combatant": ["Warrior", "Caster", "Assassin", "Shooter"],
                          "SIW": ["SIW", "Prostitute", "Stripper"],
                          "Healer": ["Healer"],
                          "Server": ["Maid"],
                          "Specialist": ["Specialist", "Manager"]}
