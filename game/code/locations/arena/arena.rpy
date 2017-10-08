init -9 python:
    # ========================= Arena and related ===========================>>>
    class Arena(_object):
        """
        First prototype of Arena, will take care of most related logic and might have to be split in the future.
        @Note to myself: This code needs to be updated post-Alpha release to account for Arena Fighters and restructured for further use in the game!
        -------------------------->
        """
        def __init__(self):
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

            self.pure_arena_fighters = dict() # Neow :)

            self.arena_fighters = list() # A list of Arena Fighters loaded into the game and actively participating in the Arena.
            self.teams_2v2 = list()
            self.teams_3v3 = list()

            self.dogfights_1v1 = list()
            self.dogfights_2v2 = list()
            self.dogfights_3v3 = list()
            self.dogfight_day = 1

            self.daily_report = ""

            self.setup = None # Setup in focus
            self.result = None

            # Chanfighting:
            self.chain_fights = {f["id"]: f for f in load_json("chainfights.json")}
            self.chain_fights_order = list(f["id"] for f in sorted(self.chain_fights.values(), key=itemgetter("level")))

            self.arena_rewards = load_json("arena_rewards.json")
            self.arena_rewards = {v["id"]: v for v in self.arena_rewards}
            self.cf_mob = None
            self.cf_bonus = False
            self.cf_bonus_awarded = False
            self.cf_multi = 0
            self.cf_setup = None
            self.cf_count = 0
            self.cf_rewards = list()

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

        def get_arena_fighters(self, include_hero_girls=False, include_af=True, exclude_matches=False):
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
                # This is not a good solution since some of the fighters are doubles...
                for fighter in self.arena_fighters:
                    fighters.append(fighter)

            if exclude_matches:
                busy_in_matches = self.get_matches_fighters()
                fighters = list(fighter for fighter in fighters if fighter not in busy_in_matches)

            return fighters

        def get_arena_candidates(self):
            '''
            Returns a list of all characters available/willing to fight in the Arena.
            Excludes all girls participating in girl_meets to avoid them being at multiple locations (this needs better handling)
            '''
            interactions_chars = gm.get_all_girls()
            arena_ready = [c for c in chars.values() if c.arena_willing and
                           "Warrior" in c.occupations and
                           c.status != "slave" and c not in hero.chars and
                           c not in interactions_chars]
            arena_candidates = []
            # First pass, unique girls...
            for char in arena_ready:
                if char.__class__ == Char:
                    arena_candidates.append(char)
            # Second pass, random girls:
            for char in arena_ready:
                if char.__class__ == rChar:
                    arena_candidates.append(char)

            return arena_candidates

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
                fighters = fighters.union(self.get_dogfights_fighters(dogfights="1v1"))
                fighters = fighters.union(self.get_dogfights_fighters(dogfights="2v2"))
                fighters = fighters.union(self.get_dogfights_fighters(dogfights="3v3"))

            return fighters

        # -------------------------- Teams control/checks -------------------------------------->
        def remove_team_from_dogfights(self, fighter):
            """
            Goes through every team in the dogfights and removes them if fighter is low on AP or injured.
            This is not very performance efficient but it is not likely to be called during the next day so it doesn't matter.
            """
            for team in self.dogfights_1v1:
                for fighter in team:
                    if fighter.health < fighter.get_max("health") * 0.9 or fighter.AP < 2:
                        if team in self.dogfights_1v1:
                            self.dogfights_1v1.remove(team)

            for team in self.dogfights_2v2:
                for fighter in team:
                    if fighter.health < fighter.get_max("health") * 0.9 or fighter.AP < 2:
                        if team in self.dogfights_2v2:
                            self.dogfights_2v2.remove(team)

            for team in self.dogfights_3v3:
                for fighter in team:
                    if fighter.health < fighter.get_max("health") * 0.9 or fighter.AP < 2:
                        if team in self.dogfights_3v3:
                            self.dogfights_3v3.remove(team)

        def check_if_team_ready_for_dogfight(self, unit):
            """
            Checks if a team/fighter is ready for dogfight by eliminating them on grounds of health, scheduled matches, presense in other dogfights or lack of AP.
            """
            if isinstance(unit, Team):
                for member in unit:
                    if member.health < int(member.get_max("health") * 0.9):
                        return False
                    if day+1 in member.fighting_days:
                        return False
                    if member.AP < 2:
                        return False
                if unit in list(itertools.chain(self.dogfights_1v1, self.dogfights_2v2, self.dogfights_3v3)):
                    return False

            else:   # Any single fighter.
                if unit.health < int(unit.get_max("health") * 0.9):
                    return False
                if day+1 in unit.fighting_days:
                    return False
                if unit.AP < 2:
                    return False
                if unit in self.get_dogfights_fighters():
                    return False

            return True

        # -------------------------- Update Methods ---------------------------------------------->
        def update_teams(self):
            '''
            Makes sure that there are enough teams for Arena to function properly.
            If members are removed from teams directly, it is up to the respective method to find a replacement...
            '''
            if len(self.teams_2v2) < 30:
                candidates = self.get_arena_candidates()
                inteams_2v2 = self.get_teams_fighters(teams="2v2")
                templist = [fighter for fighter in candidates if fighter not in inteams_2v2]
                shuffle(templist)

                for __ in xrange(max(30, len(self.teams_2v2))):
                    if len(templist) >= 2:
                        team = Team(max_size=2)
                        team.name = get_team_name()
                        team.add(templist.pop())
                        team.add(templist.pop())
                        self.teams_2v2.append(team)

            if len(self.teams_3v3) < 30:
                candidates = self.get_arena_candidates()
                inteams_3v3 = self.get_teams_fighters(teams="3v3")
                templist = [fighter for fighter in candidates if fighter not in inteams_3v3]
                shuffle(templist)

                for __ in xrange(max(30, len(self.teams_3v3))):
                    if len(templist) >= 3:
                        team = Team(max_size=3)
                        team.name = get_team_name()
                        team.add(templist.pop())
                        team.add(templist.pop())
                        team.add(templist.pop())
                        self.teams_3v3.append(team)

        def update_dogfights(self):
            """
            Attempts to fill dogfights if there are teams available for a fight.
            Takes care of busy and injured fighters, making sure that they and their teams don't make the cut.
            """
            # 1v1
            if len(self.dogfights_1v1) < 20:
                candidates = self.get_arena_candidates()
                lineups = self.get_lineups_fighters(lineup="1v1")
                templist = [fighter for fighter in candidates if fighter not in lineups]
                shuffle(templist)

                for __ in xrange(randint(10, 20)):
                    if templist:
                        team = Team(max_size=1)
                        team.add(templist.pop())
                        self.dogfights_1v1.append(team)

            busy_teams = set()
            for team in self.dogfights_1v1:
                for fighter in team:
                    if day in fighter.fighting_days:
                        busy_teams.add(team)
            for team in busy_teams:
                self.dogfights_1v1.remove(team)

            # 2v2
            if len(self.dogfights_2v2) < 10:
                templist = [team for team in self.teams_2v2 if team not in self.lineup_2v2]
                shuffle(templist)

                for __ in xrange(randint(8, 15)):
                    if templist:
                        self.dogfights_2v2.append(templist.pop())

            busy_teams = set()
            for team in self.dogfights_2v2:
                for fighter in team:
                    if day in fighter.fighting_days:
                        busy_teams.add(team)
            for team in busy_teams:
                self.dogfights_2v2.remove(team)

            # 3v3
            if len(self.dogfights_3v3) < 10:
                templist = [team for team in self.teams_3v3 if team not in self.lineup_3v3]
                shuffle(templist)

                for __ in xrange(randint(8, 15)):
                    if templist:
                        self.dogfights_3v3.append(templist.pop())

            busy_teams = set()
            for team in self.dogfights_3v3:
                for fighter in team:
                    if day in fighter.fighting_days:
                        busy_teams.add(team)
            for team in busy_teams:
                self.dogfights_3v3.remove(team)

        def update_matches(self):
            # 1vs1:
            for setup in self.matches_1v1:
                if not len(setup[1]):
                    setup[2] = day + randint(3, 14)
                    teams = list()
                    templist = copy.copy(self.lineup_1v1)
                    # shuffle(templist) || Seems useless here
                    for team in templist: # Should prolly draw from self.lineup_1v1 in final version!!! || Gonna do it right now... placing doesn't make much sense otherwise.
                        if team == hero.team:
                            pass
                        elif setup[2] not in team.leader.fighting_days and team.leader not in self.get_matches_fighters(matches="1v1"):
                            teams.append(team)
                    shuffle(teams)
                    if teams:
                        c_team = teams.pop()
                        c_team.leader.fighting_days.append(setup[2])
                        setup[1] = c_team

            for setup in self.matches_2v2:
                if not len(setup[1]):
                    setup[2] = day + randint(3, 14)
                    teams = list()
                    for team in self.lineup_2v2:
                        if team == hero.team:
                            pass
                        else:
                            count = 0
                            for fighter in team:
                                if setup[2] not in fighter.fighting_days and fighter not in self.get_matches_fighters(matches="2v2"):
                                    count += 1
                            if count == 2:
                                teams.append(team)
                    shuffle(teams)
                    if teams:
                        c_team = teams.pop()
                        for fighter in c_team.members:
                            fighter.fighting_days.append(setup[2])
                        setup[1] = c_team

            for setup in self.matches_3v3:
                if not len(setup[1]):
                    setup[2] = day + randint(3, 14)
                    teams = []
                    for team in self.lineup_3v3:
                        if team == hero.team:
                            pass
                        else:
                            count = 0
                            for fighter in team.members:
                                if setup[2] not in fighter.fighting_days and fighter not in self.get_matches_fighters(matches="3v3"):
                                    count += 1
                            if count == 3:
                                teams.append(team)
                    shuffle(teams)
                    if teams:
                        c_team = teams.pop()
                        for fighter in c_team.members:
                            fighter.fighting_days.append(setup[2])
                        setup[1] = c_team

        def update_setups(self, winner, loser):
            """
            Resonsible for repositioning winners + losers in setups!
            """
            if len(winner) == 1:
                if winner in self.lineup_1v1:
                    index = self.lineup_1v1.index(winner)
                    if index:
                        self.lineup_1v1.insert(index-1, winner)
                        del self.lineup_1v1[index+1]
                else:
                    del self.lineup_1v1[-1]
                    self.lineup_1v1.append(winner)

                if loser in self.lineup_1v1:
                    index = self.lineup_1v1.index(loser)
                    self.lineup_1v1.insert(index+2, loser)
                    del self.lineup_1v1[index]

            elif len(winner) == 2:
                if winner in self.lineup_2v2:
                    index = self.lineup_2v2.index(winner)
                    if index:
                        self.lineup_2v2.insert(index-1, winner)
                        del self.lineup_2v2[index+1]
                else:
                    del self.lineup_2v2[-1]
                    self.lineup_2v2.append(winner)

                if loser in self.lineup_2v2:
                    index = self.lineup_2v2.index(loser)
                    self.lineup_2v2.insert(index+2, loser)
                    del self.lineup_2v2[index]

            elif len(winner) == 3:
                if winner in self.lineup_3v3:
                    index = self.lineup_3v3.index(winner)
                    if index:
                        self.lineup_3v3.insert(index-1, winner)
                        del self.lineup_3v3[index+1]
                else:
                    del self.lineup_3v3[-1]
                    self.lineup_3v3.append(winner)

                if loser in self.lineup_3v3:
                    index = self.lineup_3v3.index(loser)
                    self.lineup_3v3.insert(index+2, loser)
                    del self.lineup_3v3[index]

            else:
                raise Exception("Invalid team size for Automatic Arena Combat Resolver: %d" % len(winner))

        def find_opfor(self):
            """
            Find a team to fight challenger team in the official arena matches.
            """
            # 1vs1:
            for setup in self.matches_1v1:
                if setup[2] == day:
                    deadline = 100
                elif setup[2] > day + 2:
                    deadline = 50
                else:
                    deadline = 0
                if not setup[0] and dice(max(deadline, 15)):
                    fighters = list()
                    templist = list(i for i in self.get_arena_fighters() if i != None and i.arena_permit)
                    for fighter in templist:
                        if setup[2] not in fighter.fighting_days and fighter not in self.get_matches_fighters(matches="1v1"):
                            fighters.append(fighter)
                    shuffle(fighters)
                    if fighters:
                        c_fighter = fighters.pop()
                        c_fighter.fighting_days.append(setup[2])
                        setup[0].add(c_fighter)

            # 2vs2
            for setup in self.matches_2v2:
                if setup[2] == day:
                    deadline = 100
                elif setup[2] > day + 3:
                    deadline = 50
                else:
                    deadline = 0
                if not setup[0] and dice(max(deadline, 20)):
                    teams = []
                    for team in self.teams_2v2:
                        count = 0
                        for fighter in team.members:
                            if setup[2] not in fighter.fighting_days and fighter not in self.get_matches_fighters(matches="2v2"):
                                count += 1
                        if count == 2:
                            teams.append(team)
                    shuffle(teams)
                    if teams:
                        c_team = teams.pop()
                        for fighter in c_team:
                            fighter.fighting_days.append(setup[2])
                        setup[0] = c_team

            # 3vs3
            for setup in self.matches_3v3:
                if setup[2] == day:
                    deadline = 100
                elif setup[2] > day + 3:
                    deadline = 50
                else:
                    deadline = 0
                if not setup[0] and dice(max(deadline, 25)):
                    teams = []
                    for team in self.teams_3v3:
                        count = 0
                        for fighter in team:
                            if setup[2] not in fighter.fighting_days and fighter not in self.get_matches_fighters(matches="3v3"):
                                count += 1
                        if count == 3:
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
                    renpy.call_screen("message_screen", "%s is a slave and slaves are not allowed to fight in the Arena under the penalty of death to both slave and the owner!"%member.name)
                    return
            for member in hero.team:
                if member.AP < 2:
                    renpy.call_screen("message_screen", "%s does not have enough Action Points for a fight (2 required)!"%member.name)
                    return

            ht_strength = 0 # hero team*
            opfor_strength = 0 # opposing forces*
            for member in hero.team:
                for stat in ilists.battlestats[2:]:
                    ht_strength += getattr(member, stat)
            for member in team:
                for stat in ilists.battlestats[2:]:
                    opfor_strength += getattr(member, stat)
            if opfor_strength > ht_strength * 1.6:
                if len(team) == 1:
                    team.leader.say("You're not not worth my time, go train some!")
                    return
                else:
                    team.leader.say("You guys need to grow some before challenging the likes of us!")
                    return
            if opfor_strength * 1.6 < ht_strength:
                if len(team) == 1:
                    team.leader.say("I'll am not feeling up to it... really!")
                    return
                else:
                    team.leader.say("We are not looking for a fight outside of our league!")
                    return

            # If we got this far, we can safely take AP off teammembers:
            for member in hero.team:
                member.AP -= 2

            renpy.hide_screen("arena_inside")
            renpy.hide_screen("arena_1v1_dogfights")
            renpy.hide_screen("arena_2v2_dogfights")
            renpy.hide_screen("arena_3v3_dogfights")

            team.leader.say("You seriously believe that you've got a chance?")
            hero.say(choice(["Talk is cheap!", "Defend yourself!"]))
            team.leader.say("Bring it!")

            self.start_dogfight(team)

        def match_challenge(self, n=False):
            """
            Checks if player already has fight setup on a given day.
            Handles confirmation screen for the fight.
            Adds player team to a setup.
            Now also checks if player has an Arena permit.
            """
            if hero.arena_permit:
                pass
            else:
                renpy.call_screen("message_screen", "Arena Permit is required to fight in the official matches!")
                return

            if n:
                if self.setup[2] in hero.fighting_days:
                    renpy.call_screen("message_screen", "You already have a fight planned for day %d. Having two official matches on the same day is not allowed!"%self.setup[2])
                    return
                renpy.show_screen("yesno_prompt", "Are you sure you want to schedule a fight? Backing out of it later will mean a hit on reputation!", [Return(["challenge", "confirm_match"]), Hide("yesno_prompt")], Hide("yesno_prompt"))
            else:
                renpy.hide_screen("yesno_prompt")
                self.setup[0] = hero.team
                hero.fighting_days.append(self.setup[2])

        def check_before_matchfight(self):
            """
            Checks if player team is correctly setup before an official match.
            """
            # Figure out who we're fighting:
            for setup in list(itertools.chain(self.matches_1v1, self.matches_2v2, self.matches_3v3)):
                if setup[2] == day and setup[0] == hero.team:
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
                if member.AP < 3:
                    renpy.call_screen("message_screen", "%s does not have enough Action Points for a fight (3 required)!"%member.name)
                    return

            # If we got this far, we can safely take AP off teammembers:
            for member in hero.team:
                member.AP -= 3

            renpy.hide_screen("arena_inside")
            renpy.hide_screen("arena_1v1_fights")
            renpy.hide_screen("arena_2v2_fights")
            renpy.hide_screen("arena_3v3_fights")

            self.start_matchfight(battle_setup)

        # -------------------------- Setup Methods -------------------------------->
        def setup_arena(self):
            """
            Initial Arena Setup, this will be improved and prolly split several times and I should prolly call it init() as in other classes...
            """
            # Team formations!!!: -------------------------------------------------------------->

            # Arena Teams Special presets: TODO: Update it!
            in_file = content_path("db/arena_teams.json")
            with open(in_file) as f:
                teams = json.load(f)
            for team in teams:
                team = teams[teams.index(team)]
                teamsize = len(team["members"])
                if teamsize > 3:
                    raise Exception("Arena Teams are not allowed to include more than 3 members!")
                if teamsize == 1 and not team["lineups"]:
                    raise Exception("Single member teams are only available for lineups!" \
                                    "Adjust data.xml files if you just wish girls to participate in the Arena!")
                a_team = Team(name=team["name"], max_size=teamsize)
                for member in team["members"]:
                    if member == "random_girl":
                        member = build_rc(patterns="Warrior")
                        member.status = "free"
                        member.location = "arena"
                        member.arena_permit = True
                        member.arena_active = True
                        a_team.add(member)
                    elif member in chars:
                        if chars[member] in hero.chars:
                            hero.remove_char(chars[member])
                        if chars[member] in self.get_teams_fighters(teams="2v2"):
                            raise Exception("You've added unique character %s" \
                                            " to 2v2 Arena teams twice!" % chars[member].name)
                        if chars[member] in self.get_teams_fighters(teams="3v3"):
                            raise Exception("You've added unique character %s to 3v3 Arena teams more than once!" % chars[member].name)
                        a_team.add(chars[member])
                    elif member in pytfall.arena.pure_arena_fighters:
                        member = pytfall.arena.pure_arena_fighters[member]
                        if member.unique:
                            if member in self.get_teams_fighters(teams="2v2"):
                                raise Exception("You've added an unique Arena" \
                                                " Fighter %s to 2v2 Arena teams twice!" % member.name)
                            if member in self.get_teams_fighters(teams="3v3"):
                                raise Exception("You've added an unique" \
                                    " Arena Fighter %s to 3v3 Arena teams more than once!" % member.name)
                            member.arena_active = True
                            self.arena_fighters.append(member)
                            a_team.add(member)
                        else:
                            af = copy.deepcopy(member)
                            self.arena_fighters.append(af)
                            a_team.add(af)
                    # TODO: Check is this is still valid code (member in rchars)
                    elif member in rchars:
                        build_rc(id=member, patterns="Warrior")
                        member.status = "free"
                        member.location = "arena"
                        member.arena_permit = True
                        member.arena_active = True
                        a_team.add(member)
                    else:
                        raise Exception("Team Fighter %s is of unknown origin!" % member)
                if team["lineups"]:
                    if teamsize == 1:
                        if team["lineups"] == 1:
                            raise Exception("Number one spot for 1v1 ladder (lineup) is reserved by the game!")
                        if not self.lineup_1v1[team["lineups"]-1]:
                            self.lineup_1v1[team["lineups"]-1] = a_team
                        else:
                            raise Exception("Team %s failed to take place %d in 1v1" \
                                            "lineups is already taken by another team (%s), check your arena_teams.json" \
                                            "file." % (a_team.name, team["lineups"], self.lineup_1v1[team["lineups"]-1].name))
                    if teamsize == 2:
                        if not self.lineup_2v2[team["lineups"]-1]:
                            self.lineup_2v2[team["lineups"]-1] = a_team
                            self.teams_2v2.append(a_team)
                        else:
                            raise Exception("Team %s failed to take place %d " \
                                "in 2v2 lineups is already taken by another team (%s), " \
                                "check your arena_teams.json file."%(a_team.name,
                                team["lineups"], self.lineup_2v2[team["lineups"]-1].name))
                    if teamsize == 3:
                        if not self.lineup_3v3[team["lineups"]-1]:
                            self.lineup_3v3[team["lineups"]-1] = a_team
                            self.teams_3v3.append(a_team)
                        else:
                            raise Exception("Team %s failed to take place %d in" \
                            " 3v3 lineups is already taken by another team (%s), " \
                            "check your arena_teams.json file."%(a_team.name, team["lineups"],
                            self.lineup_3v3[team["lineups"]-1].name))
                else:
                    if teamsize == 2:
                        self.teams_2v2.append(a_team)
                    if teamsize == 3:
                        self.teams_3v3.append(a_team)

            # Loading rest of Arena Combatants:
            candidates = self.get_arena_candidates()
            # This is also a suspect, TODO: Check if this needs updating to new basetraits format
            for fighter in self.pure_arena_fighters.values():
                if fighter.unique and fighter.arena_active:
                    pass
                else:
                    fighter = copy.deepcopy(fighter)
                    self.arena_fighters.append(fighter)
                    candidates.append(fighter)

            _candidates = shallowcopy(candidates)
            shuffle(_candidates)

            # Add da King!
            if not self.king:
                tier_kwargs = {"level_bios": (1.0, 1.2), "stat_bios": (1.0, 1.2)}
                if _candidates:
                    char = _candidates.pop()
                    tier_up_to(char, 7, **tier_kwargs)
                    give_tiered_items(char, equip=True)
                    give_tiered_magic_skills(char)
                else:
                    char = build_rc(tier=7, tier_kwargs=tier_kwargs,
                                    equip_to_tier=True, spells_to_tier=True)
                    candidates.append(char)

                char.arena_rep = randint(79000, 81000)
                char.arena_permit = True
                char.arena_active = True
                candidates.remove(char)
                self.king = char

            # Setting up some decent fighters:
            power_levels = [random.uniform(.2, .8) for i in range(10)]
            power_levels.extend([random.uniform(.4, 1.2) for i in range(10)])
            power_levels.extend([random.uniform(.8, 1.8) for i in range(15)])
            power_levels.extend([random.uniform(1.5, 2.3) for i in range(20)])
            power_levels.extend([random.uniform(1.8, 2.6) for i in range(20)])
            power_levels.extend([random.uniform(2.3, 3.5) for i in range(20)])
            power_levels.extend([random.uniform(3.0, 4.5) for i in range(20)])
            power_levels.extend([random.uniform(3.8, 5.2) for i in range(20)])
            for tier in power_levels:
                if _candidates:
                    fighter = _candidates.pop()
                    tier_up_to(fighter, tier)
                    give_tiered_items(fighter, equip=True)
                    give_tiered_magic_skills(fighter)
                else:
                    fighter = build_rc(patterns="Warrior", tier=tier,
                                       equip_to_tier=True, spells_to_tier=True)
                    candidates.append(fighter)

                fighter.arena_rep = randint(int(tier*9000), int(tier*11000))
                fighter.arena_permit = True
                fighter.arena_ready = True
                # fighter.arena_active = True

            # Populate the reputation ladder:
            candidates.sort(key=attrgetter("arena_rep"))
            self.ladder = candidates[:len(self.ladder)]

            # Populate tournament ladders:
            # 1v1 Ladder lineup:
            if self.king:
                self.lineup_1v1[0].add(self.king)
            temp = candidates[:30]
            if self.king in temp:
                temp.remove(self.king)
            shuffle(temp)

            for team in self.lineup_1v1:
                if not team:
                    f = temp.pop()
                    f.arena_active = True
                    team.add(f)

            # 2v2 Ladder lineup:
            if self.king:
                self.lineup_2v2[0].add(self.king)
            temp = candidates[:50]
            if self.king in temp:
                temp.remove(self.king)
            shuffle(temp)

            for team in self.lineup_2v2:
                team.name = get_team_name()
                while len(team) < 2:
                    f = temp.pop()
                    f.arena_active = True
                    team.add(f)

            # 3v3 Ladder lineup:
            if self.king:
                self.lineup_3v3[randint(1, 3)].add(self.king)
            temp = candidates[:60]
            if self.king in temp:
                temp.remove(self.king)
            shuffle(temp)

            for team in self.lineup_3v3:
                team.name = get_team_name()
                while len(team) < 3:
                    f = temp.pop()
                    f.arena_active = True
                    team.add(f)

        # -------------------------- ChainFights vs Mobs ------------------------>
        def update_cf(self):
            pass

        def check_before_chainfight(self):
            """
            Checks before chainfight.
            """
            renpy.predict_screen("confirm_chainfight")

            for member in hero.team:
                if member.AP < 3:
                    renpy.call_screen("message_screen", "%s does not have enough Action Points to start a chain fight (3 AP required)!"%member.name)
                    return
                if member.status == "slave":
                    renpy.call_screen("message_screen", "%s is a Slave forbidden from participation in Combat!"%member.name)
                    return

            # If we got this far, we can safely take AP off teammembers:
            for member in hero.team:
                member.AP -= 3

            self.cf_count = 1

            self.setup_chainfight()

        def setup_chainfight(self):
            """
            Setting up a chainfight.
            """
            # Case: First battle:
            if not pytfall.arena.cf_mob:
                renpy.hide_screen("arena_inside")
                renpy.call_screen("chain_fight")

                result = self.result

                if result == "break":
                    self.result = None
                    hero.AP += 3
                    renpy.show_screen("arena_inside")
                    return

                self.cf_setup = self.chain_fights[result]
                self.result = None


            # Picking an opponent(s):
            if self.cf_count == 7: # Boss!
                self.cf_multi += self.cf_setup["multiplier"][2]
                self.cf_mob = build_mob(self.cf_setup["boss"], level=self.cf_setup["level"] + randrange(20, 30))
            else: # Nub!
                self.cf_multi += self.cf_setup["multiplier"][1]
                self.cf_mob = build_mob(choice(self.cf_setup["mobs"]), level=self.cf_setup["level"] + self.cf_count)
            self.mob_power = 100 # TODO: FIGURE OUT WHAT THIS DOES...

            luck = 0
            # Get team luck:
            for member in hero.team:
                luck += member.luck
            luck = luck / len(hero.team)

            # Bonus:
            if config.developer:
                bonus = True
            bonus = False

            if self.cf_count == 7:
                if dice(75 + luck*0.5):
                    bonus = True
            else:
                if dice(25 + luck*0.5):
                    bonus = True

            if bonus:
                self.cf_bonus = True
                self.cf_bonus_awarded = False
                d = OrderedDict()
                # Color: range (int) pares =======>>>
                full = 1
                hp = 2
                mp = 3

                health= 0
                magic_points = 0
                for member in hero.team:
                    health = health + member.health
                    magic_points = magic_points + member.mp

                # Luck mod:
                if dice(luck):
                    full += 1
                if dice(luck):
                    hp += 2
                if dice(luck):
                    mp += 3

                # Stat mod:
                if health / len(hero.team) < 100:
                    hp += 1
                if health / len(hero.team) < 50:
                    hp += 2
                if magic_points / len(hero.team) < 50:
                    mp += 2
                if magic_points / len(hero.team) < 20:
                    mp += 3
                if (magic_points + health) / len(hero.team) < 130:
                    full += 1
                if (magic_points + health) / len(hero.team) < 70:
                    full += 2

                # Attempt to stabilize the bar:
                if (hp + mp + full) % 2:
                    hp += 1
                d["red"] = hp # HP
                d["blue"] = mp # MP
                d["green"] = full # Restore Both
                d["white"] = 50 - sum(d.values()) # Bupkis
                c = copy.copy(d)

                # Mutating to a new dict of color: value pairs
                d = OrderedDict()
                d["white"] = c["white"] / 2
                for i in c:
                    if i != "white":
                        d[i] = c[i]
                d["white"] = c["white"] / 2
                # Pass the dict to the award method:
                self.d = d
                renpy.music.play("content/sfx/sound/events/bonus.mp3")

            if not bonus:
                d = None
            else:
                renpy.call_screen("arena_minigame", 50, 0.01, 6, d)

            renpy.show_screen("confirm_chainfight")

        def start_chainfight(self):
            """
            Bridge to battle engine + rewards/penalties.
            """
            team = Team(max_size=3)
            # Add the same amount of mobs as there characters on the MCs team:
            team.add(self.cf_mob)
            while len(team) < len(hero.team):
                team.add(build_mob(choice(self.cf_setup["mobs"]), level=self.cf_setup["level"] + self.cf_count))

            renpy.music.stop(channel="world")
            renpy.play(choice(["content/sfx/sound/world/arena/prepare.mp3", "content/sfx/sound/world/arena/new_opp.mp3"]))
            renpy.pause(1.3)
            renpy.music.play(choice(ilists.battle_tracks), fadein=1.5)

            for mob in team:
                mob.controller = BE_AI(mob)

            global battle
            battle = BE_Core(ImageReference("chainfights"))
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
                        statdict = {}
                        statdict["gold"] = max(randint(35, 50), int(self.mob_power*0.6))
                        statdict["attack"] = randint(0, 1)
                        statdict["defence"] = randint(0, 1)
                        statdict["agility"] = randint(0, 1)
                        statdict["magic"] = randint(0, 1)
                        statdict["Arena Rep"] = int(self.mob_power*0.5)
                        exp = max(randint(6, 12), int(self.mob_power*0.1))
                        statdict["exp"] = adjust_exp(member, exp)
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
                    mobs[mob.id]["defeated"] = 1

                self.cf_count += 1

                if self.cf_count > 7:
                    # self.award = choice(list(item for item in items.values() if item.price > 4000))
                    # Misunderatood Dark's intent for rewards...
                    # reward_pool = {}
                    # for key in self.cf_setup["reward"]:
                        # for entry in self.arena_rewards[key]["items"]:
                            # reward_pool[entry] = self.arena_rewards[key]["items"][entry]
                    # self.cf_rewards = list()
                    # for key in reward_pool:
                        # if dice(reward_pool[key] + hero.luck/2):
                            # self.cf_rewards.append(items[key])

                    self.cf_rewards = list()
                    for key in self.cf_setup["reward"]:
                        for __ in range(self.cf_setup["reward"][key]):
                            item_str = choice(self.arena_rewards[key]["items"].keys())
                            self.cf_rewards.append(items[item_str])

                    for reward in self.cf_rewards:
                        hero.inventory.append(reward)
                    self.cf_mob = None
                    self.cf_setup = None
                    self.cf_count = 0
                    self.award = None
                    renpy.show_screen("arena_finished_chainfight", hero.team)
                    return
                else:
                    renpy.call_screen("arena_aftermatch", hero.team, team, "Victory")
                    self.setup_chainfight()
                    return

            else: # Player lost -->
                self.cf_mob = None
                self.cf_setup = None
                self.cf_count = 0
                self.award = None
                winner = team
                loser = hero.team
                for member in hero.team:
                    member.combat_stats = "K.O."
                jump("arena_inside")

        def award_cf_bonus(self):
            # Award the bonuses:
            if not self.cf_bonus_awarded:
                d = self.d
                v = self.cf_bonus
                result = None
                # And lastly, mutating to a bonus: range pair, pairs dict :)
                bonus = dict()
                bonus["bupkis"] = (0, d["white"])
                level = d["white"]
                newlevel = level + d["red"]
                bonus["HP"] = (level, newlevel)
                level = newlevel
                newlevel = newlevel + d["blue"]
                bonus["MP"] = (level, newlevel)
                level = newlevel
                newlevel = newlevel + d["green"]
                bonus["Restore"] = (level, newlevel)
                level = newlevel
                newlevel = newlevel + d["white"]
                bonus["bupkis_2"] = (level, newlevel)


                for i in bonus:
                    if bonus[i][0] <= v <= bonus[i][1]:
                        result = i
                        break

                if result == "HP":
                    for member in hero.team:
                        member.health = member.get_max("health")
                elif result == "MP":
                    for member in hero.team:
                        member.mp = member.get_max("mp")
                elif result == "Restore":
                    for member in hero.team:
                        member.health = member.get_max("health")
                        member.mp = member.get_max("mp")

                self.cf_bonus = result
                self.cf_bonus_awarded = True

            return self.cf_bonus

        # -------------------------- Battle/Next Day ------------------------------->
        def auto_resolve_combat(self, off_team, def_team, type="dog_fight"):

            battle = new_style_conflict_resolver(off_team, def_team,
                     battle_kwargs={"max_turns": 15*(len(off_team)+len(def_team))})

            winner = battle.winner
            loser = off_team if winner == def_team else def_team

            for fighter in winner:
                for stat in ("attack", "defence", "agility", "magic"):
                    fighter.mod_stat(stat, randint(1, 2))
                fighter.arena_rep += (loser.get_rep() / 20)
                exp = round_int(50 * (float(loser.get_level()) / winner.get_level()))
                fighter.mod_stat("exp", exp)

            for fighter in loser:
                fighter.arena_rep -= int(def_team.get_rep() / 300.0)

            if type == "match":
                self.update_setups(winner, loser)

            return winner, loser

        def start_dogfight(self, team):
            '''
            Bridge to battle engine + rewards/penalties
            '''
            renpy.music.stop(channel="world")
            renpy.play(choice(["content/sfx/sound/world/arena/prepare.mp3", "content/sfx/sound/world/arena/new_opp.mp3"]))
            renpy.pause(1.6)
            renpy.music.play(choice(ilists.battle_tracks), fadein=1.5)

            for member in team:
                member.controller = BE_AI(member)

            global battle
            battle = BE_Core(ImageReference("bg battle_dogfights_1"))
            battle.teams.append(hero.team)
            battle.teams.append(team)

            battle.start_battle()

            renpy.music.stop(fadeout=1.0)

            if battle.winner == hero.team:
                # Awards:
                for member in hero.team:
                    if member not in battle.corpses:
                        statdict = dict()
                        statdict["gold"] = int(max(250, 200*(float(team.get_level()) / hero.team.get_level())*1.8))
                        statdict["attack"] = randint(0, 2)
                        statdict["defence"] = randint(0, 2)
                        statdict["agility"] = randint(0, 2)
                        statdict["magic"] = randint(0, 2)
                        if dice(team.get_level()):
                            statdict["fame"] = randint(0, 1)
                            statdict["reputation"] = randint(0, 1)
                        statdict["Arena Rep"] = max(50, (team.get_rep()/30))
                        exp = 50 * (team.get_level() / hero.team.get_level())
                        statdict["exp"] = adjust_exp(member, exp)
                        for stat in statdict:
                            if stat == "exp":
                                member.exp += statdict[stat]
                            elif stat == "Arena Rep":
                                member.arena_rep += statdict[stat]
                            elif stat == "gold":
                                member.add_money(statdict[stat], reason="Arena")
                            else:
                                member.mod_stat(stat, statdict[stat])
                        member.combat_stats = statdict
                    else:
                        member.combat_stats = "K.O."

                for member in team:
                    member.arena_rep -= max(50, (team.get_rep()/30))
                    self.remove_team_from_dogfights(member)

                renpy.call_screen("arena_aftermatch", hero.team, team, "Victory")

            else:# Player lost -->
                for member in team:
                    if member not in battle.corpses:
                        statdict = dict()
                        statdict["gold"] = int(max(50, 50*(float(team.get_level()) / hero.team.get_level())))
                        statdict["attack"] = randint(0, 2)
                        statdict["defence"] = randint(0, 2)
                        statdict["agility"] = randint(0, 2)
                        statdict["magic"] = randint(0, 2)
                        statdict["Arena Rep"] = max(50, (hero.team.get_rep()/30))
                        exp = 50 * (team.get_level() / hero.team.get_level())
                        statdict["exp"] = adjust_exp(member, exp)
                        for stat in statdict:
                            if stat == "exp":
                                member.exp += statdict[stat]
                            elif stat == "Arena Rep":
                                member.arena_rep += statdict[stat]
                            elif stat == "gold":
                                member.add_money(statdict[stat], reason="Arena")
                            else:
                                member.mod_stat(stat, statdict[stat])
                    self.remove_team_from_dogfights(member)

                for member in hero.team:
                    member.combat_stats = "K.O."
                    member.arena_rep -= max(50, (hero.team.get_rep()/30))

                team.leader.say("Told you... No chance at all! :) ")

            jump("arena_inside")

        def start_matchfight(self, setup):
            """
            Bridge to battle engine + rewards/penalties.
            """
            team = setup[1]
            renpy.music.stop(channel="world")
            renpy.play(choice(["content/sfx/sound/world/arena/prepare.mp3", "content/sfx/sound/world/arena/new_opp.mp3"]))
            renpy.pause(1.3)
            renpy.music.play(choice(ilists.battle_tracks), fadein=1.5)

            for member in team:
                member.controller = BE_AI(member)

            global battle
            battle = BE_Core(ImageReference("bg battle_arena_1"))
            battle.teams.append(hero.team)
            battle.teams.append(team)

            battle.start_battle()

            renpy.music.stop(fadeout = 1.0)

            if battle.winner == hero.team:
                winner = hero.team
                loser = setup[1]
                for member in hero.team:
                    # Awards:
                    if member not in battle.corpses:
                        statdict = {}
                        statdict["gold"] = int(max(1000, 850*(float(team.get_level()) / hero.team.get_level())))
                        statdict["attack"] = randint(0, 2)
                        statdict["defence"] = randint(0, 2)
                        statdict["agility"] = randint(0, 2)
                        statdict["magic"] = randint(0, 2)
                        statdict["Arena Rep"] = max(50, (team.get_rep()/20))
                        if dice(team.get_level()):
                            statdict["fame"] = randint(0, 2)
                            statdict["reputation"] = randint(0, 2)
                        exp = 50 * (float(team.get_level()) / hero.team.get_level())
                        statdict["exp"] = adjust_exp(member, exp)
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

                for member in team:
                    member.arena_rep -= max(50, (hero.team.get_rep()/20))
                    self.remove_team_from_dogfights(member)

                renpy.call_screen("arena_aftermatch", hero.team, team, "Victory")

            else: # Player lost -->
                winner = setup[1]
                loser = hero.team
                for member in team:
                    if member not in battle.corpses:
                        statdict = {}
                        statdict["gold"] = max(500, 500*(float(team.get_level()) / hero.team.get_level()))
                        statdict["attack"] = randint(1, 3)
                        statdict["defence"] = randint(1, 3)
                        statdict["agility"] = randint(1, 3)
                        statdict["magic"] = randint(1, 3)
                        statdict["Arena Rep"] = max(50, (team.get_rep()/20))
                        exp = 50 * (float(team.get_level()) / hero.team.get_level())
                        statdict["exp"] = adjust_exp(member, exp)
                        for stat in statdict:
                            if stat == "exp":
                                member.exp += statdict[stat]
                            elif stat == "gold":
                                member.add_money(statdict[stat], reason="Arena")
                            elif stat == "Arena Rep":
                                member.arena_rep += statdict[stat]
                            else:
                                member.mod_stat(stat, statdict[stat])
                    self.remove_team_from_dogfights(member)

                for member in hero.team:
                    member.arena_rep -= max(50, (team.get_rep()/20))
                    member.combat_stats = "K.O."

                team.leader.say("Told you... No chance at all! :) ")

            setup[0] = Team(max_size=len(setup[0]))
            setup[1] = Team(max_size=len(setup[1]))

            # Line-up positioning:
            self.update_setups(winner, loser)

            hero.fighting_days.remove(day)
            jump("arena_inside")

        def next_day(self):
            # For the daily report:
            txt = ""

            # Normalizing amount of teams available for the Arena.
            if not day % 5:
                self.update_teams()

            self.find_opfor()

            # Warning the player of a scheduled arena match:
            if day+1 in hero.fighting_days:
                txt = "{color=[cyan]}You have a scheduled Arena match today! Don't you dare chickening out :) \n\n{/color}"
                # txt = "You have a scheduled Arena match today! Don't you dare chickening out :) \n\n"

            # Running the matches:
            # Join string method is used here to improve performance over += or + (Note: Same should prolly be done for jobs.)
            for setup in self.matches_1v1:
                if setup[2] == day and setup[0] != hero.team:
                    if setup[0] and setup[1]:
                        match_result = self.auto_resolve_combat(setup[0], setup[1], "match")
                        txt = "".join([txt, "%s has defeated %s in a one on one fight. "%(match_result[0][0].name, match_result[1][0].name)])
                        txt = "".join([txt, choice(["It was quite a show! \n", "\n", "Amazing performance! \n", "Crowd never stopped cheering! \n", "\n"])])
                    elif setup[1]:
                        txt = "".join([txt, "%s remained unchallenged until the day of the fight... \n"%setup[1].leader.name])
                    setup[0] = Team(max_size=1)
                    setup[1] = Team(max_size=1)

            for setup in self.matches_2v2:
                if setup[2] == day and setup[0] != hero.team:
                    if setup[0] and setup[1]:
                        match_result = self.auto_resolve_combat(setup[0], setup[1], "match")
                        txt = "".join([txt, "%s team has defeated %s in an official match. "%(match_result[0].name, match_result[1].name)])
                        txt = "".join([txt, choice(["It was quite a show! \n", "\n", "Amazing performance! \n", "Crowd never stopped cheering! \n", "\n", "Team's leader %s got most of the credit! \n"%match_result[0].leader.name])])
                    elif setup[1]:
                        txt = "".join([txt, "%s remained unchallenged until the day of the fight... \n"%setup[0].name])
                    setup[0] = Team(max_size=2)
                    setup[1] = Team(max_size=2)

            for setup in self.matches_3v3:
                if setup[2] == day and setup[0] != hero.team:
                    if setup[0] and setup[1]:
                        match_result = self.auto_resolve_combat(setup[0], setup[1], "match")
                        txt = "".join([txt, "%s team has defeated %s in an official match. "%(match_result[0].name, match_result[1].name)])
                        txt = "".join([txt, choice(["It was quite a show! \n", "\n", "Amazing performance! \n", "Crowd never stopped cheering! \n", "\n", "Team's leader %s got most of the credit! \n"%match_result[0].leader.name])])
                    elif setup[1]:
                        txt = "".join([txt, "%s remained unchallenged until the day of the fight... \n"%setup[0].name])
                    setup[0] = Team(max_size=3)
                    setup[1] = Team(max_size=3)


            # Checking if player missed an Arena match:
            if day in hero.fighting_days:
                # Locate combat setup:
                for setup in list(itertools.chain(self.matches_1v1, self.matches_2v2, self.matches_3v3)):
                    # Needs testing...
                    if setup[0] == hero.team and setup[2] == day:
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
                    txt = "".join([txt, "\n {color=[red]}You've missed a 1v1 fight vs %s, whatever the reason, you Arena Reputation took a hit of %d. Don't forget or chicken out next time :){/color}"%(penalty_setup[1].leader.name, rep_penalty)])
                else:
                    txt = "".join([txt, "\n {color=[red]}You've missed a team fight vs %s, whatever the reason, you Arena Reputation took a hit of %d. Don't forget or chicken out next time :){/color}"%(penalty_setup[1].name, rep_penalty)])

            self.update_matches()

            # Some random dogfights
            df_count = 0

            # 1v1:
            opfor_pool = list()

            for fighter in self.get_arena_fighters():
                if self.check_if_team_ready_for_dogfight(fighter):
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
                    df_count += 1

            # 2v2:
            opfor_pool = list()

            for team in self.teams_2v2:
                if self.check_if_team_ready_for_dogfight(team):
                    opfor_pool.append(team)

            shuffle(opfor_pool)
            shuffle(self.dogfights_2v2)

            for __ in xrange(randint(2, 4)):
                if self.dogfights_2v2 and opfor_pool:
                    defender = self.dogfights_2v2.pop()
                    opfor = opfor_pool.pop()
                    self.auto_resolve_combat(opfor, defender)
                    df_count += 1

            # 3v3:
            opfor_pool = list()

            for team in self.teams_3v3:
                if self.check_if_team_ready_for_dogfight(team):
                    opfor_pool.append(team)

            shuffle(opfor_pool)
            shuffle(self.dogfights_3v3)

            for __ in xrange(randint(2, 4)):
                if self.dogfights_3v3 and opfor_pool:
                    defender = self.dogfights_3v3.pop()
                    opfor = opfor_pool.pop()
                    self.auto_resolve_combat(opfor, defender)
                    df_count += 1

            self.update_dogfights()

            txt = "".join([txt, "\n %d unofficial dogfights took place yesterday!"%df_count])

            # Update top 100 ladder:
            candidates = self.get_arena_fighters(include_hero_girls=True)
            candidates.append(hero)
            candidates.sort(key=attrgetter("arena_rep"))
            for i in xrange(min(100, len(candidates))):
                self.ladder[i] = candidates.pop()

            self.daily_report = txt
