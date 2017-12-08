init -5 python:
    class GuardJob(Job):
        def __init__(self):
            """Creates reports for GuardJob.
            """
            super(GuardJob, self).__init__()
            self.id = "Guarding"
            self.type = "Combat"

            self.event_type = "jobreport"

            # Traits/Job-types associated with this job:
            self.occupations = ["Warrior"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Warrior"], traits["Mage"], traits["Knight"], traits["Shooter"]] # Corresponding traits...

            # Relevant skills and stats:
            self.base_skills = {"attack": 20, "defense": 20, "agility": 60, "magic": 20}
            self.base_stats = {"security": 100}

            self.desc = "Don't let them take your shit!"

        def traits_and_effects_effectiveness_mod(self, worker, log):
            """Affects worker's effectiveness during one turn. Should be added to effectiveness calculated by the function below.
               Calculates only once per turn, in the very beginning.
            """
            effectiveness = 0
             # effects always work
            if worker.effects['Food Poisoning']['active']:
                log.append("%s suffers from Food Poisoning, and is very far from her top shape." % worker.name)
                effectiveness -= 50
            elif worker.effects['Down with Cold']['active']:
                log.append("%s is not feeling well due to colds..." % worker.name)
                effectiveness -= 15
            elif worker.effects['Drunk']['active']:
                log.append("%s is drunk, which affects her coordination. Not the best thing when you need to guard something." % worker.name)
                effectiveness -= 20
            elif worker.effects['Revealing Clothes']['active']:
                if dice(50):
                    log.append("Her revealing clothes attract unneeded attention, interfering with work.")
                    effectiveness -= 10
                else:
                    log.append("Her revealing clothes help to pacify some aggressive customers.")
                    effectiveness += 10

            if locked_dice(65): # traits don't always work, even with high amount of traits there are normal days when performance is not affected

                traits = list(i.id for i in worker.traits if i in ["Abnormally Large Boobs",
                              "Aggressive", "Coward", "Stupid", "Neat", "Psychic", "Adventurous",
                              "Natural Leader", "Scars", "Artificial Body", "Sexy Air",
                              "Courageous", "Manly", "Sadist", "Nerd", "Smart", "Peaceful"])

                if "Lolita" in worker.traits and worker.height == "short":
                    traits.append("Lolita")
                if traits:
                    trait = choice(traits)
                else:
                    return effectiveness

                if trait == "Abnormally Large Boobs":
                    log.append("Her massive tits get in the way and keep her off balance as %s tries to work security." % worker.name)
                    effectiveness -= 25
                elif trait == "Aggressive":
                    if dice(50):
                        log.append("%s keeps disturbing customers who aren't doing anything wrong. Maybe it's not the best job for her." % worker.name)
                        effectiveness -= 35
                    else:
                        log.append("Looking for a good fight, %s patrols the area, scaring away the rough customers." % worker.name)
                        effectiveness += 50
                elif trait == "Lolita":
                    log.append("%s is too small to be taken seriously. Some of the problematic customers just laugh at her." % worker.name)
                    effectiveness -= 50
                elif trait == "Coward":
                    log.append("%s keeps asking for backup every single time an incident arises." % worker.name)
                    effectiveness -= 25
                elif trait == "Stupid":
                    log.append("%s has trouble adapting to the constantly evolving world of crime prevention." % worker.name)
                    effectiveness -= 15
                elif trait == "Smart":
                    log.append("%s keeps learning new ways to prevent violence before it happens." % worker.name)
                    effectiveness += 15
                elif trait == "Neat":
                    log.append("%s refuses to dirty her hands on some of the uglier looking criminals." % worker.name)
                    effectiveness -= 15
                elif trait == "Psychic":
                    log.append("%s knows when customers are going to start something, and prevents it easily." % worker.name)
                    effectiveness += 30
                elif trait == "Adventurous":
                    log.append("Her experience fighting bandits as an adventurer makes working security relatively easier.")
                    effectiveness += 25
                elif trait == "Natural Leader":
                    log.append("%s often manages to talk customers of starting an incident." % worker.name)
                    effectiveness += 50
                elif trait == "Scars":
                    log.append("One look at her scars is enough to tell the violators that %s means business." % worker.name)
                    effectiveness += 20
                elif trait == "Artificial Body":
                    log.append("%s makes no effort to hide the fact that she was a construct, intimidating would-be violators." % worker.name)
                    effectiveness += 25
                elif trait == "Sexy Air":
                    log.append("People around %s back her up her just because of her sexiness." % worker.name)
                    effectiveness += 15
                elif trait == "Courageous":
                    log.append("%s refuses to back down no matter the odds, making a great guard." % worker.name)
                    effectiveness += 25
                elif trait == "Manly":
                    log.append("Considering %s is bigger than a number of the guys, she prevents a lot of trouble just by being there." % worker.name)
                    effectiveness += 35
                elif trait == "Sadist":
                    log.append("%s gladly beats it out of any violators. Everyone deserves to be punished." % worker.name)
                    effectiveness += 15
                elif trait == "Nerd":
                    log.append("%s feels like a super hero while protecting your workers." % worker.name)
                    effectiveness += 15
                elif trait == "Peaceful":
                    log.append("%s has to deal with some very unruly patrons that give her a hard time." % worker.name)
                    effectiveness -= 35
            return effectiveness

        def write_patrol_report(self, guards, log):
            """Builds ND event for Guard Job.

            This one is simpler... it just logs the stats, picks an image and builds a report...
            """
            loc = log.loc
            log.team = guards

            img = Fixed(xysize=(820, 705))
            img.add(Transform(loc.img, size=(820, 705)))
            vp = vp_or_fixed(guards, ["fighting"], {"exclude": ["sex"], "resize": (150, 150)}, xmax=820)
            img.add(Transform(vp, align=(.5, .9)))
            log.img = img

            temp = "{} intercepted {} today!".format(", ".join([w.nickname for w in guards]), loc.name)
            log.append(temp)

            # Stat mods (Should be moved/split here).
            for worker in self.all_workers:
                worker.logws('vitality', -randint(15, 25))
                worker.logws('exp', randint(15, 25))
                for stat in ['attack', 'defence', 'magic', 'joy']:
                    if dice(20):
                        worker.logws(stat, 1)

            log.logloc('dirt', 25*guards) # 25 per guard? Should prolly be resolved in SimPy land...
            log.event_type = "jobreport" # Come up with a new type for team reports?

            log.after_job()
            NextDayEvents.append(log)

        def intercept(self, guards, log):
            """Builds ND event for Guard Job.

            This one is simpler... it just logs the stats, picks an image and builds a report...
            """
            loc = log.loc

            log.img = Fixed(xysize=(820, 705))
            log.img.add(Transform(loc.img, size=(820, 705)))
            vp = vp_or_fixed(guards, ["fighting"], {"exclude": ["sex"], "resize": (150, 150)}, xmax=820)
            log.img.add(Transform(vp, align=(.5, .9)))

            log.team = guards

            log = ["{} intercepted a bunch of drunk miscreants in {}! ".format(", ".join([w.nickname for w in guards]), loc.name)]
            if self.flag.flag("result"):
                log.append("They managed to subdue them!")
            else:
                log.append("They failed to subdue them, that will cause you some issues with your clients and {} reputation will suffer!".format(self.loc.name))

            # Stat mods (Should be moved/split here).
            for worker in self.all_workers:
                worker.logws('vitality', -randint(15, 25))
                worker.logws('exp', randint(15, 25))
                for stat in ['attack', 'defence', 'magic', 'joy']:
                    if dice(20):
                        worker.logws(stat, 1)

            log.logloc('dirt', 25*guards) # 25 per guard? Should prolly be resolved in SimPy land...
            log.event_type = "jobreport" # Come up with a new type for team reports?

            log.after_job()
            NextDayEvents.append(log)

        def get_events(self):
            """
            Get the guard events this girl will respond to.
            """
            log.append(choice(["%s worked as guard in %s! \n"%(worker.fullname, self.loc.name),
                                    "%s did guard duty in %s! \n"%(worker.fullname, self.loc.name)]))

            log.append("\n")
            self.img = "battle"

            if worker.guard_relay['bar_event']['count']:
                if worker.has_image("fighting"):
                    self.img = "fighting"

                g_events = plural("event", worker.guard_relay["bar_event"]["count"])

                log.append("She responded to %d brawl %s. "%(worker.guard_relay['bar_event']['count'], g_events))
                log.append("That resulted in victory(ies): %d and loss(es): %d! "%(worker.guard_relay['bar_event']['won'], worker.guard_relay['bar_event']['lost']))
                log.append("\n")

                workermod = dict( (n, workermod.get(n, 0)+worker.guard_relay['bar_event']['stats'].get(n, 0)) for n in set(workermod)|set(worker.guard_relay['bar_event']['stats']) )

            if worker.guard_relay['whore_event']['count']:
                if worker.has_image("fighting"):
                    self.img = "fighting"

                g_events = plural("attack", worker.guard_relay["whore_event"]["count"])

                log.append("With %d victory(ies) and %d loss(es) she settled %d %s on your prostitutes. \n"%(worker.guard_relay['whore_event']['won'],
                                                                                                                  worker.guard_relay['whore_event']['lost'],
                                                                                                                  worker.guard_relay['whore_event']['count'],
                                                                                                                  g_events))

                workermod = dict( (n, workermod.get(n, 0)+worker.guard_relay['whore_event']['stats'].get(n, 0)) for n in set(workermod)|set(worker.guard_relay['whore_event']['stats']) )
                log.append("\n")

        def post_job_activities(self):
            """
            Solve the post job events.
            """

            if worker.AP <= 0:
                log.append(choice(["Nothing else happened during her shift.", "She didn't have the stamina for anything else today."]))
            else:
                gbu = self.loc.get_upgrade_mod("guards")
                if gbu == 3:
                    guardlist = [girl for girl in hero.chars if girl.location == self.loc and girl.action == 'Guard' and girl.health > 60]
                    guards = len(guardlist)

                    if guards > 0:
                        if guards >= 3:
                            log.append(", ".join(girl.name for girl in guardlist[:guards-1]))
                            log.append(" and %s "%guardlist[guards-1].nickname)
                            log.append("spent the rest of the day dueling each other in Sparring Quarters. \n")

                            while worker.AP > 0:
                                workermod['attack'] = workermod.get('attack', 0) + choice([0, 0, 0, 0, 1, guards])
                                workermod['defence'] = workermod.get('defence', 0) + choice([0, 0, 0, 0, 1, guards])
                                workermod['magic'] = workermod.get('magic', 0) + choice([0, 0, 0, 0, 1, guards])
                                workermod['joy'] = workermod.get('joy', 0) + choice([0, 1, 2, 3])
                                workermod['vitality'] = workermod.get('vitality', 0) - randint(15, 20)
                                worker.AP -=  1

                            workermod['exp'] = workermod.get('exp', 0) + worker.AP * randint(8, 12) + 5 * (guards-1) # Moved to prevent insane exp increases at higher levels.

                        elif guards == 2:
                            log.append("%s and %s spent time dueling each other! \n"%(guardlist[0].name, guardlist[1].name))

                            while worker.AP > 0:
                                workermod['attack'] = workermod.get('attack', 0) + choice([0,0,0,0,1,guards])
                                workermod['defence'] = workermod.get('defence', 0) + choice([0,0,0,0,1,guards])
                                workermod['magic'] = workermod.get('magic', 0) + choice([0,0,0,0,1,guards])
                                workermod['joy'] = workermod.get('joy', 0) + choice([0,1,2,3])
                                workermod['vitality'] = workermod.get('vitality', 0) - randint(15, 20)
                                worker.AP -=  1

                            workermod['exp'] = workermod.get('exp', 0) + worker.AP * randint(8, 12) + 5

                        elif guards == 1:
                            log.append("%s had the whole Sparring Quarters to herself! \n"%(guardlist[0].name))

                            while worker.AP > 0:
                                workermod['attack'] = workermod.get('attack', 0) + choice([0,0,0,0,1,guards])
                                workermod['defence'] = workermod.get('defence', 0) + choice([0,0,0,0,1,guards])
                                workermod['magic'] = workermod.get('magic', 0) + choice([0,0,0,0,1,guards])
                                workermod['joy'] = workermod.get('joy', 0) + choice([0,1,2,3])
                                workermod['vitality'] = workermod.get('vitality', 0) - randint(15, 20)
                                worker.AP -=  1

                            workermod['exp'] = workermod.get('exp', 0) + worker.AP * randint(8, 12)

                elif gbu == 2:
                    log.append("She spent remainder of her shift practicing in Training Quarters. \n")

                    while worker.AP > 0:
                        workermod['attack'] = workermod.get('attack', 0) + choice([0,0,0,1])
                        workermod['defence'] = workermod.get('defence', 0) + choice([0,0,0,1])
                        workermod['magic'] = workermod.get('magic', 0) + choice([0,0,0,1])
                        workermod['joy'] = workermod.get('joy', 0) + choice([0,1,1,2])
                        workermod['vitality'] = workermod.get('vitality', 0) - randint(15, 20)
                        worker.AP -= 1

                    workermod['exp'] = workermod.get('exp', 0) + worker.AP * randint(8, 12)

                elif self.loc.upgrades['guards']['1']['active']:
                    if dice(50):
                        log.append("She spent time relaxing in Guard Quarters. \n")
                        workermod['vitality'] = workermod.get('vitality', 0) + randint(15, 20) * worker.AP
                        worker.AP = 0

                    else:
                        log.append("She did some rudimentary training in Guard Quarters. \n")
                        workermod['attack'] = workermod.get('attack', 0) + choice([0,0,0,0,1])
                        workermod['defence'] = workermod.get('defence', 0) + choice([0,0,0,0,1])
                        workermod['magic'] = workermod.get('magic', 0) + choice([0,0,0,0,1])
                        workermod['joy'] = workermod.get('joy', 0) + choice([0,1,1,1])
                        workermod['exp'] = workermod.get('exp', 0) +  randint(15, 25)
                        workermod['vitality'] = workermod.get('vitality', 0) - randint(15, 20)
                        worker.AP = 0

                else:
                    if dice(50):
                        log.append("She spent time relaxing. \n")

                        #display rest only if they did not fight
                        if not worker.guard_relay['bar_event']['count'] and not worker.guard_relay['whore_event']['count']:
                            self.img = "rest"

                        workermod['vitality'] = workermod.get('vitality', 0) + randint(7, 12) * worker.AP
                        worker.AP = 0

                    else:
                        log.append("She did some rudimentary training. \n")
                        workermod['attack'] = workermod.get('attack', 0) + choice([0,0,0,0,0,1])
                        workermod['defence'] = workermod.get('defence', 0) + choice([0,0,0,0,0,1])
                        workermod['magic'] = workermod.get('magic', 0) + choice([0,0,0,0,0,1])
                        workermod['joy'] = workermod.get('joy', 0) + choice([0,1])
                        workermod['exp'] = workermod.get('exp', 0) +  randint(8, 15)
                        workermod['vitality'] = workermod.get('vitality', 0) - randint(15, 20)
                        worker.AP = 0
