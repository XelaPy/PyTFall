label mobs_debug:
    python hide:
        for mob in mobs.values():
            for skill in mob["attack_skills"]:
                if skill not in battle_skills:
                    raise Exception("Mob {} has an unknown attack skill: {}".format(mob, skill))
            for skill in mob["magic_skills"]:
                if skill not in battle_skills:
                    raise Exception("Mob {} has an unknown magic skill: {}".format(mob, skill))
    return
