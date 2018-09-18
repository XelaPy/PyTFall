init -11 python:
    def mod_to_tooltip(mod):
        t = ""
        for i in mod:
            t += i + ": +" + str(mod[i]) + " "
        return t

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

        be_debug("\n    Custom Logical Combat Scenario ===================================================>>>>")
        be_debug("{} VS {}".format(str([c.name for c in off_team.members]), str([c.name for c in def_team.members])))
        be_debug("Using {} ai.".format(ai))

        tl.start("logical combat: BATTLE")
        battle.start_battle()
        tl.end("logical combat: BATTLE")
        be_debug("\n\n")

        for fighter in chained():
            fighter.controller = "player"

        return battle

    def get_random_battle_track():
        # get a list of all battle tracks:
        battle_tracks = list()
        for fn in renpy.list_files():
            if "sfx/music/be/battle" in fn:
                battle_tracks.append(fn)
        return choice(battle_tracks)

    def be_hero_escaped(team):
        '''Punished Hero team for escaping'''
        for i in team:
            i.AP = 0
            i.vitality -= int(i.get_max("vitality")*.3)
            i.mp -= int(i.get_max("mp")*.3)

    def run_default_be(enemy_team, slaves=False, your_team=None,
                       background="content/gfx/bg/be/battle_arena_1.webp",
                       track="random", prebattle=True, death=False,
                       skill_lvl=float("inf"), give_up=None):
        """
        Launches BE with MC team vs provided enemy team, returns True if MC won and vice versa
        - if slaves == True, slaves in MC team will be inside BE with passive AI, otherwise they won't be there
        - background by default is arena, otherwise could be anything,
            like interactions_pick_background_for_fight(gm.label_cache) for GMs
            or interactions_pick_background_for_fight(pytfall.world_events.get("event name").label_cache) for events
        - track by default is random, otherwise it could be a path to some track
        - if prebattle is true, there will be prebattle quotes inside BE from characters before battle starts
        - if death == True, characters in MC team will die if defeated, otherwise they will have 1 hp left
        """
        if your_team is None:
            your_team = Team(name="Your Team")
            for member in hero.team:
                if member.status == "slave" and slaves:
                    member.controller = Slave_BE_AI(member)
                    your_team.add(member)
                elif member.status == "free":
                    member.controller = "player"
                    your_team.add(member)

        # Controllers:
        for member in enemy_team:
            member.controller = BE_AI(member)

        battle = BE_Core(Image(background), start_sfx=get_random_image_dissolve(1.5),
                    music=track, end_sfx=dissolve, quotes=prebattle,
                    max_skill_lvl=skill_lvl, give_up=give_up)

        store.battle = battle
        battle.teams.append(your_team)
        battle.teams.append(enemy_team)
        battle.start_battle()

        your_team.reset_controller()
        enemy_team.reset_controller()
        for member in your_team:
            if member in battle.corpses:
                if death:
                    member.health = 0
                else:
                    member.health = 1
                    if member <> hero:
                        member.joy -= randint(5, 15)

        return battle.win
