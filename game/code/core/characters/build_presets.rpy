init python:
    # Note: We may get this from grouping traits, but that still feels a bit clumsy atm.
    base_trait_presets = {
    "Combatant": (["Warrior", "Mage"], ["Warrior", "Knight"],
                  ["Warrior", "Shooter"], ["Warrior", "Assassin"]),
    "Warrior": (["Warrior"], ["Knight"], ["Warrior", "Knight"]),
    "Caster": (["Mage"], ["Mage", "Warrior"]),
    "Assassin": (["Assassin"], ["Assassin", "Shooter"]),
    "Healer": (["Healer"], ["Healer", "Mage"], ["Healer", "Maid"]),
    "SIW": (["Prostitute", "Stripper"], ),
    "Prostitute": (["Prostitute"], ),
    "Stripper": (["Stripper"], ["Stripper", "Maid"]),
    "Maid": (["Maid"], ["Barmaid"], ["Cleaner"], ["Maid", "Cleaner"], ["Maid", "Barmaid"], ["Barmaid", "Cleaner"]),
    "Specialist": (["Manager", "Maid"], ["Manager", "Stripper"], ["Manager", "Healer"],
                   ["Manager", "Mage"]),
    "Manager": (["Manager"], )
    }

    base_traits_groups = {"Combatant": ["Combatant", "Warrior", "Caster", "Assassin"],
                          "SIW": ["SIW", "Prostitute", "Stripper"],
                          "Healer": ["Healer"],
                          "Server": ["Maid"],
                          "Specialist": ["Specialist", "Manager"]}
