init -11 python:
    def mod_to_tooltip(mod):
        t = ""
        for i in mod:
            t += i + ": +" + str(mod[i]) + " "
        return t

    def show_all_targeting_closshairs(targets):
        for index, t in enumerate(targets):
            temp = dict(what=crosshair_red,
                        at_list=[Transform(pos=battle.get_cp(t, "center",
                                           use_absolute=True),
                        anchor=(.5, .5))], zorder=t.besk["zorder"]+1)
            renpy.show("enemy__"+str(index), **temp)

    def hide_all_targeting_closshairs(targets):
        for index, t in enumerate(targets):
            renpy.hide("enemy__"+str(index))

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

        if DEBUG_BE:
            msg = "\n    Custom Logical Combat Scenario ===================================================>>>>"
            msg += "\n{} VS {}".format(str([c.name for c in off_team.members]), str([c.name for c in def_team.members]))
            msg += "\nUsing {} ai.".format(ai)
            be_debug(msg)

        tl.start("logical combat: BATTLE")
        battle.start_battle()
        tl.end("logical combat: BATTLE")
        be_debug("\n\n")

        # Reset the controllers:
        off_team.reset_controller()
        def_team.reset_controller()

        return battle

    def get_random_battle_track():
        # get a list of all battle tracks:
        battle_tracks = []
        folder = os.path.join("content", "sfx", "music", "be")
        path = os.path.join(gamedir, folder, '.')
        for fn in os.walk(path).next()[2]:
            if fn.endswith(MUSIC_EXTENSIONS):
                battle_tracks.append(os.path.join(folder, fn))
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
                       skill_lvl=float("inf"), give_up=None, use_items=False):
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
            your_team = hero.team

        for member in your_team:
            if member.status == "slave" and slaves:
                member.controller = BE_AI(member)
            elif member.status == "free":
                member.controller = None # no AI -> controlled by the player

        # Controllers:
        for member in enemy_team:
            member.controller = Complex_BE_AI(member)

        global battle
        battle = BE_Core(Image(background), start_sfx=get_random_image_dissolve(1.5),
                    music=track, end_sfx=dissolve, quotes=prebattle,
                    max_skill_lvl=skill_lvl, give_up=give_up,
                    use_items=use_items)
        battle.teams.append(your_team)
        battle.teams.append(enemy_team)
        battle.start_battle()

        your_team.reset_controller()
        enemy_team.reset_controller()

        for member in your_team:
            if member in battle.corpses:
                if death:
                    kill_char(member)
                else:
                    member.health = 1
                    if member != hero:
                        member.joy -= randint(5, 15)

        if battle.combat_status in ("escape", "surrender"):
            rv = battle.combat_status
        else:
            rv = battle.win

        return rv
