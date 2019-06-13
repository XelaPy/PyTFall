init -9 python:
    # ========================= Arena and related ===========================>>>
    class Arena(Location):
        """
        First prototype of Arena, will take care of most related logic and might have to be split in the future.
        @Note to myself: This code needs to be updated post-Alpha release to account for Arena Fighters and restructured for further use in the game!
        -------------------------->
        """
        def __init__(self):
            super(Arena, self).__init__(id="Arena")
            # self.1v1 = list() # Tracking the 1v1 fights.
            # self.teams = list() # Tracking the team fights.

            # Team Lineups and Scheduled matches:
            self.matches_1v1 = list(
            [Team(max_size=1), Team(max_size=1), 1] for i in xrange(8) # [0]: Team One, [1]: Team Two, [2]: Day
            )
            self.matches_2v2 = list(
            [Team(max_size=2), Team(max_size=2), 1] for i in xrange(5) # [0]: Team One, [1]: Team Two, [2]: Day
            )
            self.matches_3v3 = list(
            [Team(max_size=3), Team(max_size=3), 1] for i in xrange(5) # [0]: Team One, [1]: Team Two, [2]: Day
            )
            self.lineup_1v1 = list(
            Team(max_size=1) for i in xrange(20)
            )
            self.lineup_2v2 = list(
            Team(max_size=2) for i in xrange(10)
            )
            self.lineup_3v3 = list(
            Team(max_size=3) for i in xrange(10)
            )
            self.ladder = list(
            None for i in xrange(100)
            )

            # ----------------------------->
            self.king = None

            # A list of Arena Fighters loaded into the game and actively participating in the Arena.
            self.arena_fighters = {}
            self.teams_2v2 = list()
            self.teams_3v3 = list()

            self.dogfights_1v1 = list()
            self.dogfights_2v2 = list()
            self.dogfights_3v3 = list()
            self.dogfight_day = 1

            self.df_count = 0
            self.hero_match_result = None
            self.daily_report = []

            self.setup = None # Setup in focus
            self.result = None

            # Chanfighting:
            self.chain_fights = {f["id"]: f for f in load_db_json("arena_chainfights.json")}
            self.chain_fights_order = list(f["id"] for f in sorted(self.chain_fights.values(), key=itemgetter("level")))
            self.chain_fights_order_portraits = []
            for i in self.chain_fights_order:
                self.chain_fights_order_portraits.append(ProportionalScale(mobs[self.chain_fights[i]["boss"]]["portrait"], 36, 36))

            self.cf_mob = None
            self.cf_setup = None
            self.cf_count = 0

        # -------------------------- Sorting ---------------------------------------------------------->
        def get_matches_fighters(self, matches="all"):
            '''
            Returns all fighters that are set to participate at official maches.
            '''
            fighters = set()
            if matches == "1v1":
                for lineup in self.matches_1v1:
                    for fighter in list(itertools.chain(lineup[0].members, lineup[1].members)):
                        fighters.add(fighter)
            elif matches == "2v2":
                for lineup in self.matches_2v2:
                    for fighter in list(itertools.chain(lineup[0].members, lineup[1].members)):
                        fighters.add(fighter)
            elif matches == "3v3":
                for lineup in self.matches_3v3:
                    for fighter in list(itertools.chain(lineup[0].members, lineup[1].members)):
                        fighters.add(fighter)
            elif matches == "all":
                fighters = fighters.union(self.get_matches_fighters(matches="1v1"))
                fighters = fighters.union(self.get_matches_fighters(matches="2v2"))
                fighters = fighters.union(self.get_matches_fighters(matches="3v3"))

            return fighters

        def get_teams_fighters(self, teams="all"):
            """
            Returns fighters that are in the Arena teams.
            """
            fighters = set()
            if teams == "2v2":
                for team in self.teams_2v2:
                    for fighter in team:
                        fighters.add(fighter)
            elif teams == "3v3":
                for team in self.teams_3v3:
                    for fighter in team:
                        fighters.add(fighter)
            elif teams == "all":
                fighters = fighters.union(self.get_teams_fighters(teams="2v2"))
                fighters = fighters.union(self.get_teams_fighters(teams="3v3"))

            return fighters

        def get_arena_fighters(self, include_hero_girls=False, include_af=True,
                                     exclude_matches=False):
            '''
            Returns all fighters active at the arena.
            hero = true will include all girls in heros employment as well.
            matches = exclude (False) or include (True) fighters participating in official matches.
            Updated to include all Arena Fighters as well!
            Note to self: This REALLY should simply be a list in the Arena namespace...
            '''
            fighters = list()
            if include_hero_girls:
                for fighter in chars.values():
                    if fighter.arena_active:
                        fighters.append(fighter)
            else:
                for fighter in chars.values():
                    if fighter.arena_active and fighter not in hero.chars:
                        fighters.append(fighter)

            if include_af:
                fighters.extend(self.arena_fighters.values())

            if exclude_matches:
                busy_in_matches = self.get_matches_fighters()
                fighters = list(fighter for fighter in fighters if fighter not in busy_in_matches)

            return fighters

        def get_arena_candidates_from_chars(self):
            '''
            Returns a list of all characters available/willing to fight in the Arena.
            Excludes all girls participating in girl_meets to avoid them being at multiple locations (this needs better handling)
            '''
            interactions_chars = gm.get_all_girls()
            arena_ready = [c for c in chars.values() if c.arena_willing and
                           "Combatant" in c.gen_occs and
                           c.status != "slave" and c not in hero.chars and
                           c not in interactions_chars]
            unique = []
            rand = []
            for char in arena_ready:
                if isinstance(char, rChar):
                    rand.append(char)
                elif char.__class__ == Char:
                    unique.append(char)

            return unique + rand

        def get_lineups_fighters(self, lineup="all"):
            """
            Returns fighters currently in Arena lineups (heavyweights basically)
            """
            fighters = set()
            if lineup == "1v1":
                for team in self.lineup_1v1:
                    for fighter in team:
                        fighters.add(fighter)
            elif lineup == "2v2":
                for team in self.lineup_2v2:
                    for fighter in team:
                        fighters.add(fighter)
            elif lineup == "3v3":
                for team in self.lineup_3v3:
                    for fighter in team:
                        fighters.add(fighter)
            elif lineup == "all":
                fighters = fighters.union(self.get_lineups_fighters(lineup="1v1"))
                fighters = fighters.union(self.get_lineups_fighters(lineup="2v2"))
                fighters = fighters.union(self.get_lineups_fighters(lineup="3v3"))

            return fighters

        def get_dogfights_fighters(self, dogfights="all"):
            """
            All fighters that are currently in dogfights!
            """
            fighters = set()
            if dogfights == "1v1":
                for team in self.dogfights_1v1:
                    for fighter in team:
                        fighters.add(fighter)
            elif dogfights == "2v2":
                for team in self.dogfights_2v2:
                    for fighter in team:
                        fighters.add(fighter)
            elif dogfights == "3v3":
                for team in self.dogfights_3v3:
                    for fighter in team:
                        fighters.add(fighter)
            elif dogfights == "all":
                fighters = self.get_dogfights_fighters(dogfights="1v1")
                fighters.update(self.get_dogfights_fighters(dogfights="2v2"))
                fighters.update(self.get_dogfights_fighters(dogfights="3v3"))

            return fighters

        # -------------------------- Teams control/checks -------------------------------------->
        def remove_team_from_dogfights(self, fighter):
            """
            Goes through every team in the dogfights and removes them if fighter is low on AP or injured.
            This is not very performance efficient but it is not likely to be called during the next day so it doesn't matter.
            """
            for team in self.dogfights_1v1:
                for fighter in team:
                    if fighter.health < fighter.get_max("health") * .9 or fighter.AP < 2:
                        if team in self.dogfights_1v1:
                            self.dogfights_1v1.remove(team)

            for team in self.dogfights_2v2:
                for fighter in team:
                    if fighter.health < fighter.get_max("health") * .9 or fighter.AP < 2:
                        if team in self.dogfights_2v2:
                            self.dogfights_2v2.remove(team)

            for team in self.dogfights_3v3:
                for fighter in team:
                    if fighter.health < fighter.get_max("health") * .9 or fighter.AP < 2:
                        if team in self.dogfights_3v3:
                            self.dogfights_3v3.remove(team)

            restore_battle_stats(fighter)

        @staticmethod
        def check_if_team_ready_for_dogfight(unit, dogfighters):
            """
            Checks if a team/fighter is ready for dogfight by eliminating them on grounds of health, scheduled matches, presense in other dogfights or lack of AP.
            """
            if isinstance(unit, Team):
                for member in unit:
                    if member.health < int(member.get_max("health") * .9):
                        return False
                    if day+1 in member.fighting_days:
                        return False
                    if member.AP < 2:
                        return False
                if unit in dogfighters:
                    return False

            else:   # Any single fighter.
                if unit.health < int(unit.get_max("health") * .9):
                    return False
                if day+1 in unit.fighting_days:
                    return False
                if unit.AP < 2:
                    return False
                if unit in dogfighters:
                    return False

            return True

        # -------------------------- Update Methods ---------------------------------------------->
        def update_reputation_ladder(self):
            # Update top 100 ladder:
            candidates = self.get_arena_fighters(include_hero_girls=True)
            candidates.append(hero)
            candidates.sort(reverse=True, key=attrgetter("arena_rep"))
            self.ladder = candidates[:len(self.ladder)]

        def update_teams(self):
            '''Makes sure that there are enough teams for Arena to function properly.
            If members are removed from teams directly, it is up to the respective method to find a replacement...
            '''
            candidates = None
            if len(self.teams_2v2) < 30:
                if candidates is None:
                    candidates = self.get_arena_candidates_from_chars()
                    candidates.extend(self.arena_fighters.values())
                inteams_2v2 = self.get_teams_fighters(teams="2v2")
                templist = [fighter for fighter in candidates if fighter not in inteams_2v2]
                shuffle(templist)

                for __ in xrange(min(30, len(templist)/2)):
                    team = Team(max_size=2)
                    team.name = get_team_name()
                    team.add(templist.pop())
                    team.add(templist.pop())
                    self.teams_2v2.append(team)

            if len(self.teams_3v3) < 30:
                if candidates is None:
                    candidates = self.get_arena_candidates_from_chars()
                    candidates.extend(self.arena_fighters.values())
                inteams_3v3 = self.get_teams_fighters(teams="3v3")
                templist = [fighter for fighter in candidates if fighter not in inteams_3v3]
                shuffle(templist)

                for __ in xrange(min(30, len(templist)/3)):
                    team = Team(max_size=3)
                    team.name = get_team_name()
                    team.add(templist.pop())
                    team.add(templist.pop())
                    team.add(templist.pop())
                    self.teams_3v3.append(team)

        def update_dogfights(self):
            """
            Just populates dogfights, no more checking for anything...
            """
            level_range = range(hero.level-10, hero.level+10)

            # 1v1
            if len(self.dogfights_1v1) < 20:
                dogfighters = self.get_dogfights_fighters()
                candidates = [f for f in self.arena_fighters.values() if f not in dogfighters]
                chars_fighters = self.get_arena_candidates_from_chars()
                chars_fighters = [f for f in chars_fighters if f not in dogfighters]
                candidates.extend(chars_fighters)

                amount = min(min(randint(15, 20), 20 - len(self.dogfights_1v1)), len(candidates))
                in_range_exists = len([f for f in dogfighters if f.level in level_range])

                # do first pass over those candidates who's level is near Hero's
                for i in candidates[:]:
                    if amount == 0 or in_range_exists >= 5:
                        break

                    if i.level in level_range:
                        amount -= 1
                        in_range_exists += 1
                        team = Team(max_size=1)
                        team.add(i)
                        candidates.remove(i)
                        self.dogfights_1v1.append(team)


                if amount != 0:
                    shuffle(candidates)

                    while amount != 0:
                        amount -= 1
                        team = Team(max_size=1)
                        team.add(candidates.pop())
                        self.dogfights_1v1.append(team)

            # 2v2
            for teams, teams_setup in ([self.teams_2v2, self.dogfights_2v2],
                                       [self.teams_3v3, self.dogfights_3v3]):
                if len(teams_setup) < 15:
                    candidates = [team for team in teams if team not in teams_setup]
                    amount = min(min(randint(8, 15), 15 - len(teams_setup)), len(candidates))
                    in_range_exists = len([t for t in teams_setup if t.get_level() in level_range])

                    for team in candidates[:]:
                        if amount == 0 or in_range_exists >= 4:
                            break

                        if team.get_level() in level_range:
                            amount -= 1
                            in_range_exists += 1
                            candidates.remove(team)
                            teams_setup.append(team)


                    if amount != 0:
                        shuffle(candidates)

                        while amount != 0:
                            amount -= 1
                            teams_setup.append(candidates.pop())

        def update_matches(self):
            # 1vs1:
            teams = None
            for setup in self.matches_1v1:
                if not len(setup[1]):
                    setup[2] = day + randint(3, 14)
                    if teams is None:
                        match_fighters = self.get_matches_fighters(matches="1v1")
                        match_fighters.add(hero)
                        teams = list(i for i in self.lineup_1v1 if setup[2] not in i.leader.fighting_days and i.leader not in match_fighters)
                        shuffle(teams)
                    if teams:
                        c_team = teams.pop()
                        c_team.leader.fighting_days.append(setup[2])
                        setup[1] = c_team

            teams = None
            for setup in self.matches_2v2:
                if not len(setup[1]):
                    setup[2] = day + randint(3, 14)
                    if teams is None:
                        match_fighters = self.get_matches_fighters(matches="2v2")
                        match_fighters.add(hero)
                        teams = list()
                        for team in self.lineup_2v2:
                            for fighter in team:
                                if setup[2] in fighter.fighting_days or fighter in match_fighters:
                                    break
                            else:
                                teams.append(team)
                        shuffle(teams)
                    if teams:
                        c_team = teams.pop()
                        for fighter in c_team.members:
                            fighter.fighting_days.append(setup[2])
                        setup[1] = c_team

            teams = None
            for setup in self.matches_3v3:
                if not len(setup[1]):
                    setup[2] = day + randint(3, 14)
                    if teams is None:
                        match_fighters = self.get_matches_fighters(matches="3v3")
                        match_fighters.add(hero)
                        teams = list()
                        for team in self.lineup_3v3:
                            for fighter in team.members:
                                if setup[2] in fighter.fighting_days or fighter in match_fighters:
                                    break
                            else:
                                teams.append(team)
                        shuffle(teams)
                    if teams:
                        c_team = teams.pop()
                        for fighter in c_team.members:
                            fighter.fighting_days.append(setup[2])
                        setup[1] = c_team

        def update_setups(self, winner, loser):
            """
            Responsible for repositioning winners + losers in setups!
            """
            team_size = len(winner)
            if team_size == 1:
                lineup = self.lineup_1v1
            elif team_size == 2:
                lineup = self.lineup_2v2
            elif team_size == 3:
                lineup = self.lineup_3v3
            else:
                raise Exception("Invalid team size for Automatic Arena Combat Resolver: %d" % team_size)

            lineup_len = len(lineup)
            try:
                winner_index = lineup.index(winner)
            except:
                winner_index = lineup_len
            try:
                loser_index = lineup.index(loser)
            except:
                loser_index = lineup_len

            # Make sure that winner cannot advance by beating lower teams:
            if winner_index < loser_index:
                return

            if winner in lineup:
                lineup.insert(winner_index-1, lineup.pop(winner_index))
            else:
                del lineup[-1]
                lineup.append(winner)

        def find_opfor(self):
            """
            Find a team to fight challenger team in the official arena matches.
            """
            # 1vs1:
            fighters = None
            for setup in self.matches_1v1:
                if setup[0]:
                    continue
                if setup[2] == day:
                    deadline = 100
                elif setup[2] > day + 2:
                    deadline = 50
                else:
                    deadline = 15
                if dice(deadline):
                    if fighters is None:
                        match_fighters = self.get_matches_fighters(matches="1v1")
                        fighters = list(i for i in self.get_arena_fighters() if i.arena_permit and setup[2] not in i.fighting_days and i not in match_fighters)
                        shuffle(fighters)

                    if fighters:
                        c_fighter = fighters.pop()
                        c_fighter.fighting_days.append(setup[2])
                        setup[0].add(c_fighter)

            # 2vs2
            teams = None
            for setup in self.matches_2v2:
                if setup[0]:
                    continue
                if setup[2] == day:
                    deadline = 100
                elif setup[2] > day + 3:
                    deadline = 50
                else:
                    deadline = 20
                if dice(deadline):
                    if teams is None:
                        match_fighters = self.get_matches_fighters(matches="2v2")
                        teams = []
                        for team in self.teams_2v2:
                            for fighter in team.members:
                                if setup[2] in fighter.fighting_days or fighter in match_fighters:
                                    break
                            else:
                                teams.append(team)
                        shuffle(teams)
                    if teams:
                        c_team = teams.pop()
                        for fighter in c_team:
                            fighter.fighting_days.append(setup[2])
                        setup[0] = c_team

            # 3vs3
            teams = None
            for setup in self.matches_3v3:
                if setup[0]:
                    continue
                if setup[2] == day:
                    deadline = 100
                elif setup[2] > day + 3:
                    deadline = 50
                else:
                    deadline = 25
                if dice(deadline):
                    if teams is None:
                        match_fighters = self.get_matches_fighters(matches="3v3")
                        teams = []
                        for team in self.teams_3v3:
                            for fighter in team:
                                if setup[2] in fighter.fighting_days or fighter in match_fighters:
                                    break
                            else:
                                teams.append(team)
                        shuffle(teams)
                    if teams:
                        c_team = teams.pop()
                        for fighter in c_team:
                            fighter.fighting_days.append(setup[2])
                        setup[0] = c_team

        # -------------------------- GUI methods ---------------------------------->
        def dogfight_challenge(self, team):
            """
            Checks if player team is ready for a dogfight.
            """
            if len(hero.team) != len(team):
                renpy.call_screen("message_screen", "Make sure that your team has %d members!"%len(team))
                return
            for member in hero.team:
                if member != hero and member.status == "slave":
                    renpy.call_screen("message_screen", "%s is a slave and slaves are not allowed to fight in the Arena under the penalty of death to both a slave and the owner!"%member.name)
                    return
            for member in hero.team:
                if member.AP < 2:
                    renpy.call_screen("message_screen", "%s does not have enough Action Points for a fight (2 required)!"%member.name)
                    return

            hlvl = hero.team.get_level()
            elvl = team.get_level()
            if elvl > max(hlvl+12, hlvl*1.3):
                if len(team) == 1:
                    team.leader.say("You're not worth my time, go train some.")
                    return
                else:
                    team.leader.say("You guys need to grow up before challenging the likes of us.")
                    return
            if max(elvl+12, elvl*1.3) < hlvl:
                if len(team) == 1:
                    team.leader.say("I am not feeling up to it... really!")
                    return
                else:
                    team.leader.say("We are not looking for a fight outside of our league.")
                    return

            # If we got this far, we can safely take AP off teammembers:
            for member in hero.team:
                member.AP -= 2

            renpy.scene(layer="screens")

            self.run_dogfight(team)

        def match_challenge(self, setup):
            """
            Checks if player already has fight setup on a given day.
            Handles confirmation screen for the fight.

            Adds player team to a setup.
            Now also checks if player has an Arena permit.
            """
            if not hero.arena_permit:
                renpy.call_screen("message_screen", "Arena Permit is required to fight in the official matches!")
                return

            fight_day = setup[2]

            if fight_day in hero.fighting_days:
                renpy.call_screen("message_screen", "You already have a fight planned for day %d. Having two official matches on the same day is not allowed!"%fight_day)
                return

            if fight_day == day and self.hero_match_result:
                renpy.call_screen("message_screen", "You already had a fight today. Having two official matches on the same day is not allowed!")
                return

            result = renpy.call_screen("yesno_prompt",
                "Are you sure you want to schedule a fight? Backing out of it later will mean a hit on reputation!",
                Return(["Yes"]), Return(["No"]))
            if result == ["Yes"]:
                setup[0] = hero.team
                hero.fighting_days.append(fight_day)

        def check_before_matchfight(self):
            """
            Checks if player team is correctly setup before an official match.
            """
            # Figure out who we're fighting:
            for setup in list(itertools.chain(self.matches_1v1, self.matches_2v2, self.matches_3v3)):
                if setup[2] == day and setup[0].leader == hero:
                    battle_setup = setup
                    team = setup[1]

            if len(hero.team) != len(team):
                renpy.call_screen("message_screen", "Make sure that your team has %d members!"%len(team))
                return
            for member in hero.team:
                if member != hero and member.status == "slave":
                    renpy.call_screen("message_screen", "%s is a slave and slaves are not allowed to fight in the Arena under the penalty of death to both slave and the owner!"%member.name)
                    return
            for member in hero.team:
                if member.AP < 2:
                    renpy.call_screen("message_screen", "%s does not have enough Action Points for a fight (3 required)!"%member.name)
                    return

            # If we got this far, we can safely take AP off teammembers:
            for member in hero.team:
                member.AP -= 2

            renpy.hide_screen("arena_inside")
            renpy.hide_screen("arena_1v1_fights")
            renpy.hide_screen("arena_2v2_fights")
            renpy.hide_screen("arena_3v3_fights")

            self.start_matchfight(battle_setup)

        # -------------------------- Setup Methods -------------------------------->
        def setup_arena(self):
            """Initial Arena Setup, this will be improved and prolly split several
            times and I should prolly call it init() as in other classes...
            """
            # Team formations!!!: -------------------------------------------------------------->
            self.arena_fighters.update(store.male_fighters)
            self.arena_fighters.update(store.female_fighters)

            final_candidates = []

            # Do the Arena Fighters/Set KING:
            candidates = self.arena_fighters.values()
            shuffle(candidates)

            if not self.king: # Add da King!
                fighter = candidates.pop()
                rep = randint(100000, 110000)
                self.king = self.setup_arena_fighter(fighter, tier=8, set_rep=rep)
                # final_candidates.append(fighter)

            # Setting up some decent fighters:
            power_levels = [uniform(4.8, 7.0) for i in range(15)]
            power_levels.extend([uniform(3.0, 4.9) for i in range(10)])
            power_levels.extend([uniform(2.7, 3.5) for i in range(10)])
            power_levels.extend([uniform(1.8, 2.9) for i in range(15)])
            power_levels.extend([uniform(1.5, 2.3) for i in range(10)])
            power_levels.extend([uniform(.8, 1.8) for i in range(15)])
            power_levels.extend([uniform(.4, 1.2) for i in range(20)])
            power_levels.extend([uniform(.1, .8) for i in range(15)])

            for tier, fighter in izip_longest(power_levels, candidates):
                if tier is None:
                    tier = uniform(.5, 3.5)

                rep = randint(int(tier*9000), int(tier*11000))
                fighter = self.setup_arena_fighter(fighter, tier=tier, set_rep=rep)
                final_candidates.append(fighter)

            # uChars and rChars:
            candidates = self.get_arena_candidates_from_chars()
            for fighter in candidates:
                self.setup_arena_fighter(fighter, tier_up=False, set_rep=False)
                final_candidates.append(fighter)

            # Load the special teams:
            # Also adds final few Arena Fighters:
            self.load_special_team_presets()

            candidates = final_candidates
            candidates.sort(key=attrgetter("tier"), reverse=True)

            # Populate the reputation ladder:
            self.update_reputation_ladder()

            # Populate tournament ladders:
            # 1v1 Ladder lineup:
            temp = candidates[:30]
            shuffle(temp)
            temp.append(self.king)

            for team in self.lineup_1v1:
                if not team:
                    f = temp.pop()
                    team.add(f)

            # 2v2 Ladder lineup:
            temp = candidates[:50]
            shuffle(temp)
            temp.append(self.king)

            for team in self.lineup_2v2:
                if not team.name:
                    team.name = get_team_name()
                while len(team) < 2:
                    f = temp.pop()
                    team.add(f)

            # 3v3 Ladder lineup:
            temp = candidates[:60]
            shuffle(temp)
            temp.append(self.king)

            for team in self.lineup_3v3:
                if not team.name:
                    team.name = get_team_name()
                while len(team) < 3:
                    f = temp.pop()
                    team.add(f)

        def load_special_team_presets(self):
            json_fighters = store.json_fighters
            teams = json.load(renpy.file("content/db/arena_teams.json"))

            for team in teams:
                members = team["members"]
                name = team["name"]
                lineups = team.get("lineups", False)
                tiers = team.get("tiers", [])
                if not tiers:
                    for m in members:
                        tiers.append(uniform(.8, 1.2))
                teamsize = len(members)

                if teamsize > 3:
                    raise Exception("Arena Teams are not allowed to include more than 3 members!")
                if teamsize == 1 and not team["lineups"]:
                    raise Exception("Single member teams are only available for lineups!")

                a_team = Team(name=name, max_size=teamsize)
                for index, member in enumerate(members):
                    try:
                        tier = tiers[index]
                    except:
                        tier = uniform(.8, 1.4)
                    rep = randint(int(tier*9000), int(tier*11000))

                    if member == "random_char" or member in rchars:
                        if member in rchars:
                            id = member
                        else:
                            id = None

                        member = self.setup_arena_fighter(fighter=None, tier=tier,
                                                tier_up=True, set_rep=rep, rchar_id=id)
                    elif member in chars:
                        member = chars[member]
                        member = self.setup_arena_fighter(fighter=member,
                                                tier_up=False, set_rep=rep)
                    elif member in json_fighters:
                        member = json_fighters[member]
                        member = self.setup_arena_fighter(fighter=member,
                                                tier_up=True, set_rep=rep)
                        self.arena_fighters[member.id] = member
                    else:
                        raise Exception("Team Fighter %s is of unknown origin!" % member)

                    a_team.add(member)

                    if member in self.get_teams_fighters(teams="2v2"):
                        raise Exception("You've added unique character %s" \
                                        " to 2v2 Arena teams twice!" % chars[member].name)
                    if member in self.get_teams_fighters(teams="3v3"):
                        raise Exception("You've added unique character %s to 3v3 Arena teams more than once!" % chars[member].name)

                if lineups:
                    if teamsize == 1:
                        if lineups == 1:
                            raise Exception("Number one spot for 1v1 ladder (lineup) is reserved by the game!")
                        if not self.lineup_1v1[lineups-1]:
                            self.lineup_1v1[lineups-1] = a_team
                        else:
                            raise Exception("Team %s failed to take place %d in 1v1" \
                                            "lineups is already taken by another team (%s), check your arena_teams.json" \
                                            "file." % (a_team.name, team["lineups"], self.lineup_1v1[team["lineups"]-1].name))
                    if teamsize == 2:
                        if not self.lineup_2v2[lineups-1]:
                            self.lineup_2v2[lineups-1] = a_team
                            self.teams_2v2.append(a_team)
                        else:
                            raise Exception("Team %s failed to take place %d " \
                                "in 2v2 lineups is already taken by another team (%s), " \
                                "check your arena_teams.json file."%(a_team.name,
                                team["lineups"], self.lineup_2v2[lineups-1].name))
                    if teamsize == 3:
                        if not self.lineup_3v3[lineups-1]:
                            self.lineup_3v3[lineups-1] = a_team
                            self.teams_3v3.append(a_team)
                        else:
                            raise Exception("Team %s failed to take place %d in" \
                            " 3v3 lineups is already taken by another team (%s), " \
                            "check your arena_teams.json file."%(a_team.name, lineups,
                            self.lineup_3v3[lineups-1].name))
                else:
                    if teamsize == 2:
                        self.teams_2v2.append(a_team)
                    if teamsize == 3:
                        self.teams_3v3.append(a_team)

        def setup_arena_fighter(self, fighter=None, tier=1, tier_up=True,
                                set_rep=False, rchar_id=None):
            if fighter is None:
                fighter = build_rc(id=rchar_id,
                                   bt_go_patterns=["Combatant"], tier=tier,
                                   set_status="free", give_bt_items=True,
                                   spells_to_tier="casters_only")
            elif tier_up: # Setting up an existing fighter:
                tier_up_to(fighter, tier)
                arena_fighter_iiu(fighter) # Initial Items Up
                if "Caster" in fighter.gen_occs:
                    give_tiered_magic_skills(fighter)

            fighter.arena_active = True
            fighter.arena_permit = True
            fighter.home = locations["City Apartments"]
            set_location(fighter, self)
            fighter.action = "Arena Combat"
            fighter.set_status("free")

            if set_rep:
                fighter.arena_rep = set_rep

            return fighter

        # -------------------------- ChainFights vs Mobs ------------------------>
        def update_cf(self):
            pass

        def check_before_chainfight(self):
            """
            Checks before chainfight.
            """
            for member in hero.team:
                if member.AP < 2:
                    renpy.call_screen("message_screen", "%s does not have enough Action Points to start a chain fight (2 AP required)!"%member.name)
                    return
                if member.status == "slave":
                    renpy.call_screen("message_screen", "%s is a Slave forbidden from participation in Combat!"%member.name)
                    return

            self.cf_count = 1

            self.setup_chainfight()

        def setup_chainfight(self):
            """Setting up a chainfight.
            """
            # Case: First battle:
            if not self.cf_mob:
                renpy.call_screen("chain_fight")

                result, self.result = self.result, None

                if result == "break":
                    renpy.show_screen("arena_inside")
                    return

                # If we got this far, we can safely take AP off teammembers:
                for member in hero.team:
                    member.AP -= 2

                self.cf_setup = self.chain_fights[result]

            # Picking an opponent(s):
            num_opps = len(hero.team)
            team = Team(name=self.cf_setup.get("id", "Captured Creatures"), max_size=num_opps)

            new_level = self.cf_setup["level"]
            new_level += new_level*(.1*self.cf_count)
            if self.cf_count == 5: # Boss!
                new_level = round_int(new_level*1.1) # 10% extra for the Boss!
                team.add(build_mob(self.cf_setup["boss"], level=new_level))
                num_opps -= 1
            else:
                new_level = round_int(new_level)

            # Add the same amount of mobs as there characters on the MCs team:
            for i in range(num_opps):
                mob = build_mob(choice(self.cf_setup["mobs"]), level=new_level)
                team.add(mob)

            self.cf_mob = team
            self.mob_power = new_level

            luck = 0
            # Get team luck:
            for member in hero.team:
                luck += member.luck
            luck = float(luck)/len(hero.team)

            # Bonus:
            bonus = dice(25+self.cf_count*3 + luck*.5)

            # if DEBUG:
            #     bonus = True
            if bonus:
                self.setup_minigame(luck)

            renpy.show_screen("confirm_chainfight")

        def execute_chainfight(self):
            """
            Bridge to battle engine + rewards/penalties.
            """
            team = self.cf_mob

            renpy.music.stop(channel="world")
            renpy.play(choice(["content/sfx/sound/world/arena/prepare.mp3", "content/sfx/sound/world/arena/new_opp.mp3"]))
            track = get_random_battle_track()
            renpy.pause(1.3)
            renpy.music.play(track, fadein=1.5)

            for mob in team:
                mob.be.controller = Complex_BE_AI(mob)

            global battle
            battle = BE_Core(ImageReference("chainfights"), start_sfx=get_random_image_dissolve(1.5), end_sfx=dissolve, give_up = "surrender")
            battle.teams.append(hero.team)
            battle.teams.append(team)
            battle.start_battle()

            renpy.music.stop(fadeout=1.0)

            if battle.winner == hero.team:
                winner = hero.team
                loser = team
                for member in hero.team:
                    # Awards:
                    if member not in battle.corpses:
                        statdict = {} # no gold for mobs, and only little bit of reputation. because they give items, unlike all other modes
                        statdict["Arena Rep"] = max(int(self.mob_power*.2), 1)
                        statdict["exp"] = exp_reward(member, loser, ap_used=.3)
                        for stat in statdict:
                            if stat == "exp":
                                member.exp += statdict[stat]
                            elif stat == "gold":
                                member.add_money(statdict[stat], reason="Arena")
                            elif stat == "Arena Rep":
                                member.arena_rep += statdict[stat]
                            else:
                                member.mod_stat(stat, statdict[stat])
                        member.combat_stats = statdict
                    else:
                        member.combat_stats = "K.O."

                for mob in loser:
                    defeated_mobs[mob.id] = 1

                # Ladder
                self.update_reputation_ladder()

                self.cf_count += 1

                if self.cf_count > 5:
                    self.cf_victory()
                    return
                else:
                    renpy.call_screen("arena_aftermatch", hero.team, team, "Victory")
                    self.setup_chainfight()
                    return
            else: # Player lost -->
                self.cf_reset()
                winner = team
                loser = hero.team
                for member in hero.team:
                    member.combat_stats = "K.O."
                jump("arena_inside")

        def cf_victory(self):
            amount = 2
            amount += randint(0, 2)
            types = "all"
            tier = self.mob_power/40.0
            mobs_level = self.mob_power
            price = MAX_ARENA_ITEM_PRICE*mobs_level/190
            if price < 50:
                price = 50
            rewards = get_item_drops(types=types,
                                     price=price,
                                     tier=tier,
                                     locations=["Arena"],
                                     amount=amount)
            for i in rewards:
                hero.inventory.append(i)

            self.cf_reset()
            renpy.play("win_screen.mp3", channel="world")
            renpy.show_screen("arena_finished_chainfight", hero.team, rewards)

        def cf_reset(self):
            self.cf_mob = None
            self.cf_setup = None
            self.cf_count = 0
            self.award = None

        def setup_minigame(self, luck):
            # Color: range (int) pares =======>>>
            data = OrderedDict()

            hp = mp = vp = 0
            maxhp = maxmp = maxvp = 0
            for member in hero.team:
                hp += member.health
                mp += member.mp
                vp += member.vitality

                maxhp += member.get_max("health")
                maxmp += member.get_max("mp")
                maxvp += member.get_max("vitality")

            # New total is 300, each of the stats may get 50!
            # Here max possible is 40, rest is luck.
            # The smaller the stats, the larger the bonus area.
            length = 300
            hpbar = 40-hp*40/maxhp
            mpbar = 40-mp*40/maxmp
            vpbar = 40-vp*40/maxvp

            # Luck mod:
            if dice(luck):
                hpbar += 10
            if dice(luck):
                mpbar += 10
            if dice(luck):
                vpbar += 10

            # Stabilize:
            data["red"] = max(round_int(hpbar), 20)
            data["blue"] = max(round_int(mpbar), 20)
            data["green"] = max(round_int(vpbar), 20)
            white = (length-sum(data.values()))/2 # Bupkis

            # Mutating to a new dict of color: value pairs
            colors = OrderedDict()
            colors["white"] = white
            for color, value in data.items():
                colors[color] = value

            # Pass the minigame screen:
            renpy.play("win_screen.mp3", channel="world")
            renpy.call_screen("arena_minigame", colors, length)

        def settle_minigame(self, udd, d):
            # Award the bonuses:
            value = udd.value
            result = None
            # And lastly, mutating to a bonus: range pair, pairs dict :)
            white = d.pop("white")
            bonus = dict()

            bonus["bupkis"] = (0, white)

            level = white
            newlevel = level + d["red"]
            bonus["hp"] = (level, newlevel)

            level = newlevel
            newlevel = level + d["blue"]
            bonus["mp"] = (level, newlevel)

            level = newlevel
            newlevel = level + d["green"]
            bonus["vp"] = (level, newlevel)

            level = newlevel
            newlevel = newlevel + white
            bonus["bupkis_2"] = (level, newlevel)

            for reward, levels in bonus.items():
                if levels[0] <= value <= levels[1]:
                    break

            if reward == "hp":
                for member in hero.team:
                    member.health = member.get_max("health")
            elif reward == "mp":
                for member in hero.team:
                    member.mp = member.get_max("mp")
            elif reward == "vp":
                for member in hero.team:
                    member.vitality = member.get_max("vitality")
            return reward

        # -------------------------- Battle/Next Day ------------------------------->
        @staticmethod
        def arena_rep_reward(loser, winner):
            return max(0.0, (loser.get_rep() - (winner.get_rep() / 2)) / 10.0)

        def auto_resolve_combat(self, off_team, def_team, type="dog_fight"):

            battle = new_style_conflict_resolver(off_team, def_team,
                     battle_kwargs={"max_turns": 15*(len(off_team)+len(def_team))})

            winner = battle.winner
            loser = off_team if winner == def_team else def_team

            rep = self.arena_rep_reward(loser, winner)
            if type == "dog_fight":
                rep = min(50.0, max(3.0, rep))

            for fighter in winner:
                for stat in ("attack", "defence", "agility", "magic"):
                    fighter.mod_stat(stat, randint(1, 2))
                fighter.arena_rep += int(rep)
                exp = round_int(50 * (float(loser.get_level()) / max(1, winner.get_level())))
                fighter.mod_stat("exp", exp)

            rep = rep / 10.0
            for fighter in loser:
                fighter.arena_rep -= int(rep)

            if type == "match":
                self.update_setups(winner, loser)

            return winner, loser

        def run_dogfight(self, enemy_team):
            '''
            Bridge to battle engine + rewards/penalties
            '''
            global battle

            renpy.music.stop(channel="world")
            renpy.play(choice(["content/sfx/sound/world/arena/prepare.mp3",
                               "content/sfx/sound/world/arena/new_opp.mp3"]))
            track = get_random_battle_track()
            renpy.music.play(track, fadein=1.5)
            renpy.pause(.5)

            start_health = 0
            finish_health = 0

            for member in enemy_team:
                member.be.controller = Complex_BE_AI(member)

            for member in hero.team:
                start_health += member.health

            battle = BE_Core(ImageReference("bg battle_dogfights_1"),
                             start_sfx=get_random_image_dissolve(1.5),
                             end_sfx=dissolve, give_up="surrender")
            battle.teams.append(hero.team)
            battle.teams.append(enemy_team)
            battle.start_battle()

            renpy.music.stop(fadeout=1.0)

            winner = battle.winner
            if winner == hero.team:
                loser = enemy_team
            else:
                loser = hero.team

            for member in hero.team:
                finish_health += member.health

            # Idea for awards in DF: Decent cash, low a-rep and normal EXP.
            # Max gold as a constant:
            max_gold = (enemy_team.get_level()+hero.team.get_level())*5
            blood = start_health - finish_health
            # Awards:
            money = round_int(max_gold*(float(loser.get_level())/max(1, winner.get_level())))
            if blood > 0:
                money += blood

            rep = min(50, max(3, self.arena_rep_reward(loser, winner)))

            for member in winner:
                if member not in battle.corpses:
                    statdict = dict()
                    statdict["gold"] = money
                    if dice(enemy_team.get_level()):
                        statdict["fame"] = randint(0, 1)
                        statdict["reputation"] = randint(0, 1)
                    statdict["Arena Rep"] = int(rep)
                    statdict["exp"] = exp_reward(member, loser, ap_used=2)
                    for stat, value in statdict.items():
                        if stat == "exp":
                            member.exp += value
                        elif stat == "Arena Rep":
                            member.arena_rep += value
                        elif stat == "gold":
                            member.add_money(value, reason="Arena")
                        else:
                            member.mod_stat(stat, value)
                    member.combat_stats = statdict
                else:
                    member.combat_stats = "K.O."

            rep = rep / 10.0
            for member in loser:
                member.arena_rep -= int(rep)
                member.exp += exp_reward(member, winner, ap_used=2, final_mod=.15)
                self.remove_team_from_dogfights(member)

            for member in enemy_team:
                restore_battle_stats(member)

            if winner == hero.team:
                renpy.call_screen("arena_aftermatch", hero.team, enemy_team, "Victory")
            else:
                renpy.call_screen("arena_aftermatch", enemy_team, hero.team, "Loss")

            # Ladder
            self.update_reputation_ladder()

            # record the event
            self.df_count += 1

            jump("arena_inside")

        @staticmethod
        def shallow_copy_team(team):
            """
            Create a shallow copy of the team to preserve the important team informations for today's report
            """
            tmp = Team(name=team.name, implicit=team.implicit, free = team.free, max_size = team.max_size)
            tmp.set_leader(team.leader)
            return tmp

        def start_matchfight(self, setup):
            """
            Bridge to battle engine + rewards/penalties.
            """
            enemy_team = setup[1]
            renpy.music.stop(channel="world")
            renpy.play(choice(["content/sfx/sound/world/arena/prepare.mp3", "content/sfx/sound/world/arena/new_opp.mp3"]))
            track = get_random_battle_track()
            renpy.pause(1.3)
            renpy.music.play(track, fadein=1.5)

            for member in enemy_team:
                member.be.controller = Complex_BE_AI(member)

            global battle
            battle = BE_Core(ImageReference("bg battle_arena_1"),
                             start_sfx=get_random_image_dissolve(1.5),
                             end_sfx=dissolve, give_up="surrender")
            battle.teams.append(hero.team)
            battle.teams.append(enemy_team)
            battle.start_battle()

            renpy.music.stop(fadeout=1.0)

            winner = battle.winner
            if winner == hero.team:
                loser = enemy_team
            else:
                loser = hero.team

            rep = self.arena_rep_reward(loser, winner)

            for member in winner:
                if member in battle.corpses:
                    member.combat_stats = "K.O."
                    continue

                statdict = dict()
                statdict["gold"] = int(max(200, 250*(float(loser.get_level()) / max(1, winner.get_level()))))
                if dice(enemy_team.get_level()):
                    statdict["fame"] = randint(0, 2)
                    statdict["reputation"] = randint(0, 2)
                statdict["Arena Rep"] = int(rep)
                statdict["exp"] = exp_reward(member, loser, ap_used=2)
                for stat, value in statdict.items():
                    if stat == "exp":
                        member.exp += value
                    elif stat == "Arena Rep":
                        member.arena_rep += value
                    elif stat == "gold":
                        member.add_money(value, reason="Arena")
                    else:
                        member.mod_stat(stat, value)
                    member.combat_stats = statdict

            rep = rep / 10.0
            for member in loser:
                member.arena_rep -= int(rep)
                member.exp += exp_reward(member, winner, ap_used=2, final_mod=.15)
                # self.remove_team_from_dogfights(member)

            for member in enemy_team:
                restore_battle_stats(member)

            if winner == hero.team:
                renpy.call_screen("arena_aftermatch", hero.team, enemy_team, "Victory")
            else:
                renpy.call_screen("arena_aftermatch", enemy_team, hero.team, "Loss")

            setup[0] = Team(max_size=len(setup[0]))
            setup[1] = Team(max_size=len(setup[1]))

            # Line-up positioning:
            self.update_setups(winner, loser)

            # Ladder
            self.update_reputation_ladder()

            # record the event
            self.hero_match_result = [self.shallow_copy_team(winner), self.shallow_copy_team(loser)]

            fday = setup[2]
            for d in hero.fighting_days[:]:
                if d == fday:
                    hero.fighting_days.remove(d)

            jump("arena_inside")

        @staticmethod
        def append_match_result(txt, f2f, match_result):
            if f2f:
                temp = "{} has defeated {} in a one on one fight. ".format(
                          match_result[0][0].name, match_result[1][0].name)
            else:
                temp = "%s team has defeated %s in an official match. " % (match_result[0].name, match_result[1].name)
            temp += choice(["It was quite a show!",
                            "Amazing performance!",
                            "Crowd never stopped cheering!",
                  ("The crowd chanted %s name for minutes!" % match_result[0][0].name) if f2f else
                  ("Team's leader %s got most of the credit!" % match_result[0].leader.name)])
            txt.append(temp)

        def next_day(self):
            # For the daily report:
            txt = []

            # Normalizing amount of teams available for the Arena.
            if not day % 5:
                self.update_teams()

            self.find_opfor()

            # Warning the player of a scheduled arena match:
            if day+1 in hero.fighting_days:
                txt.append("{color=[orange]}You have a scheduled Arena match today! Don't you dare chickening out :){/color}")

            # Add the hero's matchresult from today
            if self.hero_match_result:
                self.append_match_result(txt, len(self.hero_match_result[0]) == 1, self.hero_match_result)

            tl.start("Arena: Matches")
            # Running the matches:
            # Join string method is used here to improve performance over += or + (Note: Same should prolly be done for jobs.)
            for setup in self.matches_1v1:
                if setup[2] == day and setup[0].leader != hero:
                    if setup[0] and setup[1]:
                        match_result = self.auto_resolve_combat(setup[0], setup[1], "match")
                        self.append_match_result(txt, True, match_result)

                    setup[0] = Team(max_size=1)
                    setup[1] = Team(max_size=1)

            for setup in self.matches_2v2:
                if setup[2] == day and setup[0].leader != hero:
                    if setup[0] and setup[1]:
                        match_result = self.auto_resolve_combat(setup[0], setup[1], "match")
                        self.append_match_result(txt, False, match_result)
                    setup[0] = Team(max_size=2)
                    setup[1] = Team(max_size=2)

            for setup in self.matches_3v3:
                if setup[2] == day and setup[0].leader != hero:
                    if setup[0] and setup[1]:
                        match_result = self.auto_resolve_combat(setup[0], setup[1], "match")
                        self.append_match_result(txt, False, match_result)
                    setup[0] = Team(max_size=3)
                    setup[1] = Team(max_size=3)


            # Checking if player missed an Arena match:
            if day in hero.fighting_days:
                # Locate combat setup:
                for setup in list(itertools.chain(self.matches_1v1, self.matches_2v2, self.matches_3v3)):
                    # Needs testing...
                    if setup[2] == day and setup[0].leader == hero:
                        penalty_setup = setup

                        # get rid of the failed team setup:
                        team_size = len(penalty_setup[1])
                        ladder = getattr(self, "matches_%dv%d" % (team_size, team_size))
                        index = ladder.index(setup)
                        ladder[index] = [Team(max_size=team_size), Team(max_size=team_size), 1]

                # Rep penalty!
                rep_penalty = max(500, (penalty_setup[1].get_rep()/10))
                hero.arena_rep -= rep_penalty

                if len(penalty_setup[1]) == 1:
                    opfor = penalty_setup[1].leader
                    temp = "{} missed a 1v1 fight vs {}, who entrained the public "
                    temp += "by boasting of {} prowess and making funny jabs at {}'s cowardliness!"
                    temp = temp.format(hero.name, opfor.name, opfor.pp, hero.name)
                    temp = set_font_color(temp, "red")
                else:
                    temp = "{} didn't show up for a team combat vs {}!".format(hero.team.name,
                                                                               penalty_setup[1].name)
                    temp += " The spectators were very displeased!"
                    temp = set_font_color(temp, "red")

                txt.append(temp)

            self.update_matches()
            tl.end("Arena: Matches")

            # Some random dogfights
            # 1v1:
            tl.start("Arena: Dogfights")
            opfor_pool = list()
            dogfighters = self.get_dogfights_fighters()
            for fighter in self.get_arena_fighters():
                if self.check_if_team_ready_for_dogfight(fighter, dogfighters):
                    opfor_pool.append(fighter)

            shuffle(opfor_pool)
            shuffle(self.dogfights_1v1)

            for __ in xrange(randint(4, 7)):
                if self.dogfights_1v1 and opfor_pool:
                    defender = self.dogfights_1v1.pop()
                    opfor_fighter = opfor_pool.pop()
                    opfor = Team(max_size=1)
                    opfor.add(opfor_fighter)
                    self.auto_resolve_combat(opfor, defender)
                    self.df_count += 1
            # 2v2:
            opfor_pool = list()

            for team in self.teams_2v2:
                if self.check_if_team_ready_for_dogfight(team, self.dogfights_2v2):
                    opfor_pool.append(team)

            shuffle(opfor_pool)
            shuffle(self.dogfights_2v2)

            for __ in xrange(randint(2, 4)):
                if self.dogfights_2v2 and opfor_pool:
                    defender = self.dogfights_2v2.pop()
                    opfor = opfor_pool.pop()
                    self.auto_resolve_combat(opfor, defender)
                    self.df_count += 1
            # 3v3:
            opfor_pool = list()

            for team in self.teams_3v3:
                if self.check_if_team_ready_for_dogfight(team, self.dogfights_3v3):
                    opfor_pool.append(team)

            shuffle(opfor_pool)
            shuffle(self.dogfights_3v3)

            for __ in xrange(randint(2, 4)):
                if self.dogfights_3v3 and opfor_pool:
                    defender = self.dogfights_3v3.pop()
                    opfor = opfor_pool.pop()
                    self.auto_resolve_combat(opfor, defender)
                    self.df_count += 1
            self.update_dogfights()
            tl.end("Arena: Dogfights")

            txt.append("%d unofficial dogfights took place yesterday!" % self.df_count)
            self.daily_report = gazette.arena = txt

            # Update top 100 ladder:
            self.update_reputation_ladder()

            # Reset daily variables
            self.df_count = 0
            self.hero_match_result = None
