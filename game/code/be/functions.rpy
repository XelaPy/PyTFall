init -11 python:
    # Simple Automatic conflict resolver for friendly and enemy parties:
    def s_conflict_resolver(fp, ep, new_results=False):
        """
        Simple conflict resolver, used mainly during job events, stats based.
        fp = friendly party (Team)
        ep = enemy party (Team)
        new_results = Whether to allow the function to return OV and DV results.
        """
        offence = 0
        defence = 0
        luck = 0

        for friend in fp:
            offence += friend.attack + friend.defence + friend.agility + friend.health
            if friend.mp > friend.magic/5:
                offence += friend.magic

            luck += friend.luck

        luck *= choice([0.5, 1, 1, 1, 1.5, 2])

        for enemy in ep:
            defence += enemy.attack + enemy.defence + enemy.agility + friend.health
            if enemy.mp > enemy.magic/5:
                defence += enemy.magic

        exp = int(defence/10)

        # Overwhelming victory
        if defence * 2 <= offence and new_results:
            return "OV", exp

        # Desisive victory
        elif defence * 1.5 <= offence and new_results:
            return "DV", exp

        # Victory
        elif defence <= offence:
            if new_results: return "V", exp
            else: return "victory", exp

        # Lucky victory
        elif defence <= offence + luck:
            if new_results: return  "LV", exp
            else: return "victory", exp

        # Overwhelming defeat
        elif defence * .6 > offence:
            if new_results: return "OD", exp
            else: return "OD"

        # Defeat
        else:
            if new_results: return "D", exp
            else: return "defeat"

    def new_style_conflict_resolver(off_team, def_team, ai="simple", battle_kwargs=None):
        if battle_kwargs is None:
            battle_kwargs = {}

        chained = partial(chain, off_team, def_team)

        store.battle = battle = BE_Core(logical=True, **battle_kwargs)
        battle.teams = [off_team, def_team]

        for fighter in chained():
            if ai == "simple":
                fighter.controller = BE_AI(fighter)
            elif ai == "complex":
                fighter.controller = Complex_BE_AI(fighter)

        devlog.info("\n    Custom Logical Combat Scenario ===================================================>>>>")
        devlog.info("{} VS {}".format(str([c.name for c in off_team.members]), str([c.name for c in def_team.members])))
        devlog.info("Using {} ai.".format(ai))

        tl.start("logical combat: BATTLE")
        battle.start_battle()
        tl.end("logical combat: BATTLE")
        devlog.info("\n\n")

        for fighter in chained():
            fighter.controller = "player"

        return battle
