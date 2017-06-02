init -10 python:
    class JobLog(_object):
        """Stores text reports during the job execution.
        """
        def __init__(self, txt=""):
            self.log = []
            if txt: self.log.append(txt)

        def add(self, text, newline=True):
            # Adds a text to the log.
            self.log.append(text)

        def append(self, text, newline=True):
            # Adds a text to the log.
            self.log.append(text)


    class NDEvent(JobLog):
        """Next Day Report. Logs in a single event to be read in next_day label.

        The load_image method will always return the same image. If you want to
        do another search, you have to set the 'img' attribute to 'None'.

        MONEY:
        During jobs, we log cash that players gets to self.earned
        Cash that workers may get during the job:
        worker.mod_flag("jobs_tips", value) # tips
        worker.mod_flag("jobs_earned", value) # Normal stuff other than tips?
        worker.mod_flag("jobs_earned_dishonestly", value) # Stole a wallet from client?

        DevNote: We used to create this at the very end of an action,
        now, we are creating the event as the action starts and pass it around
        between both normal methods and funcs and simpy events. This needs to
        be kept in check because older parts of code still just create this
        object at the end of their lifetime.
        """
        def __init__(self, type='', txt='', img='', char=None, charmod=None, loc=None, locmod=None, red_flag=False, green_flag=False, team=None, job=None, **kwargs):
            super(NDEvent, self).__init__(txt)

            self.job = job
            if not type and job:
                self.type = job.event_type
            else:
                self.type = type

            self.txt = txt
            self.img = img

            self.char = char
            self.team = team
            if charmod is None:
                charmod = {}
            if team:
                self.team_charmod = charmod.copy()
                self.charmod = None
            else:
                self.charmod = charmod.copy()
                self.team_charmod = None

            # the location of the event (optional):
            self.loc = loc
            if locmod is None:
                self.locmod = {}
            else:
                self.locmod = locmod

            self.business = kwargs.get("business", None)
            self.kind = kwargs.get("kind", None)

            self.green_flag = green_flag
            self.red_flag = red_flag

            self.earned = 0

        def load_image(self):
            """
            Returns a renpy image showing the event.

            The image is selected based on the event type and the character.
            """

            # select/load an image according to img
            width = 820
            height = 705

            size = (width, height)
            d = self.img
            # Try to analyze self.img in order to figure out what it represents:
            if isinstance(d, renpy.display.core.Displayable):
                return d
            if isinstance(d, basestring):
                if not d:
                    raise Exception("Basetring Supplied as img: Ev.type: {}, Ev.loc.name: {}".format(self.type, self.loc.name if self.loc else "Unknown"))
                elif "." in d:
                    return ProportionalScale(d, width, height)
                else:
                    return self.char.show(self.img, resize=size, cache=True)
            devlog.warning("Unknown Image Type: {} Provided to Event (Next Day Events class)".format(self.img))
            return ProportionalScale("content/gfx/interface/images/no_image.png", width, height)

        # Data logging and application:
        def logws(self, s, value, char=None):
            # Logs stats changes.
            # Uses internal dict on chars namespace
            if char is None:
                char = self.char
            char.logws(s, value)

        def logloc(self, s, value):
            # Logs a stat for the location:
            self.locmod[s] = self.locmod.get(s, 0) + value

        def update_char_data(self, char, adjust_exp=True):
            """Settles stats, exp and skills for workers.

            # After a long conversation with Dark and CW, we've decided to prevent workers dieing during jobs
            # I am leaving the code I wrote before that decision was reached in case
            # we change our minds or add jobs like exploration where it makes more sense.
            # On the other hand just ignoring it is bad, so let's at least reduce some stuff, pretending that she lost consciousness for example.
            """
            data = char.stats_skills

            for key, value in data.iteritems():
                if key == "city_jail" or value == "city_jail":
                    raise Exception("MEOW")
                if key == "exp":
                    if adjust_exp:
                        value = char.adjust_exp(value)
                        data[key] = value
                    char.exp += value
                elif key == 'health' and (char.health + value) <= 0:
                    char.health = 1
                    # if char.constitution > 5: # @Review (Alex): Why??? This is insane??
                    #     char.constitution -= 5
                else:
                    if char.stats.is_stat(key):
                        char.mod_stat(key, value)
                    elif char.stats.is_skill(key):
                        char.mod_skill(key, value)

        def update_loc_data(self):
            """Settles dirt, rep and fame for buildings."""
            for key, value in self.locmod.iteritems():
                if key == 'fame':
                    self.loc.modfame(value)
                elif key == 'dirt':
                    if value < 0:
                        self.loc.clean(-value)
                    else:
                        self.loc.dirt += value
                elif key == 'reputation':
                    self.loc.modrep(value)
                else:
                    raise Exception("Stat: {} does not exits for Businesses".format(key))

        def after_job(self):
            # We run this after job but before ND reports
            # Figure out source for finlogs:
            if self.job:
                fin_source = self.job.id
            else:
                if self.debug:
                    fin_source = "Unspecified NDReport"
                else:
                    fin_source = "Unspecified"

            if self.char:
                self.update_char_data(self.char)
                self.charmod.update(self.char.stats_skills)
                self.char.stats_skills = {}
                self.reset_workers_flags(self.char)
                self.char.fin.log_logical_income(self.earned, fin_source)
            elif self.team:
                for char in self.team:
                    self.update_char_data(char)
                    self.charmod[char] = char.stats_skills.copy()
                    char.stats_skills = {}
                    self.reset_workers_flags(char)
                    # char.fin.log_logical_income(self.earned, fin_source) # TODO How should we handle this for teams?


            # Location related:
            if self.loc and hasattr(self.loc, "fin"):
                self.update_loc_data()
                self.loc.fin.log_logical_income(self.earned, fin_source)
            if self.earned:
                self.append("{color=[gold]}\nA total of %d Gold was earned!{/color}" % self.earned)
            self.txt = self.log
            self.log = []

        def reset_workers_flags(self, char):
            # I am not sure this is still needed after refactoring, will check after refactoring is done
            # TODO: Just what it sais above!
            for flag in char.flags.keys():
                if flag.startswith("jobs"):
                    char.del_flag(flag)


    class Job(_object):
        """Baseclass for jobs and other next day actions with some defaults.

        - Presently is used in modern Job Classes. Very similar to Job.
        """
        def __init__(self, event_type="jobreport"):
            """Creates a new Job.

            worker = The worker doing the job.
            workers = A container with all the workers. (May not be useful anymore)
            """
            self.id = "Base Job"
            self.type = None # Is this still at all useful? Feels like a simple version of self.occupations

            # Traits/Job-types associated with this job:
            self.occupations = list() # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = list() # Corresponing traits... # TODO: WE NEED TO MAKE SURE THESE ARE INSTANCES!

            self.disposition_threshold = -500 # Any worker with disposition this high will be willing to do the job even without matched traits.

            self.event_type = "jobreport"

            # Each job should have two dicts of stats/skills to evaluate chars ability of performing it:
            self.base_skills = dict()
            self.base_stats = dict()
            # Where key: value are stat/skill: weight!

            self.desc = "" # String we can use to describe the Job.

        def __str__(self):
            return str(self.id)

        @property
        def all_occs(self):
            # All Occupations:
            return set(self.occupations + self.occupation_traits)

        def is_valid_for(self, worker):
            """Returns True if char is willing to do the job else False.

            elif worker.status in ("free", "various"): ~==various==~ was added by pico to handle groups!
            """
            if worker.status == 'slave':
                return True
            if not isinstance(worker, PytGroup):
                if worker.disposition >= self.calculate_disposition_level(worker):
                    return True
                # TODO: Devnote, this may be too strics and all_occs should be used instead...
                # if [t for t in self.all_occs if t in worker.occupations]:
                if set(self.occupation_traits).intersection(worker.traits):
                    return True
            return False

        def get_clients(self):
            # This returns a correct amount of clients used for the job
            return 0

        def calculate_disposition_level(self, worker):
            return self.disposition_threshold

        def settle_workers_disposition(self, char=None):
            # Formerly check_occupation
            """Settles effects of worker who already agreed to do the job.

            Normaly deals with disposition, joy and vitality (for some reason?)
            """
            return True

        # We should also have a number of methods or properties to evaluate new dicts:
        def relative_ability(self, char, tier=None):
            """
            # Maybe just do the stats/skills interpolation here???
            # And later add that to tier calc in the effectiveness method?

            100 or above is the target for this method.
            """
            ability = 0
            if tier is None:
                tier = worker.tier

            rates = []
            amount = []
            for skill, weight in self.base_skills.items():
                target_value = SKILLS_MAX[skill]*.1*tier
                real_value = worker.get_skill(skill)
                rv = 50.0*real_value/target_value # resulting value, 50 base
                rates.append(weight)
                amount.append(rv)
            # Formula from SO:
            total_skills = sum(x * y for x, y in zip(rate, amount)) / sum(amount)

            rates = []
            amount = []
            for stat, weight in self.base_stats.items():
                target_value = worker.get_max(stat)*.1*tier
                real_value = getattr(char, stat)
                rv = 50.0*real_value/target_value # resulting value, 50 base
                rates.append(weight)
                amount.append(rv)
            # Formula from SO:
            total_stats = sum(x * y for x, y in zip(rate, amount)) / sum(amount)

            # Bonuses:
            temp = worker.occupations.intersection(self.occupations)
            bonus1 = 10 if temp else 0
            bonus2 = len(self.occupation_traits.intersection(worker.traits))*5

            return total_skills + total_stats + bonus1 + bonus2

        def traits_and_effects_effectiveness_mod(self, worker, difficulty, log):
            """Modifies workers effectiveness depending on traits and effects.

            returns an integer to be added to base calculations!
            """
            return 0

        def effectiveness(self, worker, difficulty, log):
            """We check effectiveness here during jobs from SimPy land.

            difficulty is used to counter worker tier.
            100 is considered a score where worker does the task with acceptable performance.
            """
            if worker.occupations.intersection(self.occupations):
                effectiveness = 50
            else:
                effectiveness = 0

            # 25 points for difference between difficulty/tier:
            diff = worker.tier - difficulty
            effectiveness += diff*25

            return effectiveness



    ####################### Manager Job  ############################
    class Manager(Job):
        """This is the manager Job, so far it just creates the instance we can use to assign the job.

        - Later we may use this to do mod stats and level up Managers somehow...
        """
        def __init__(self):
            super(Manager, self).__init__()
            self.id = "Manager"
            self.type = "Management"

            # Traits/Job-types associated with this job:
            self.occupations = ["Manager"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Manager"]] # Corresponding traits...


    ####################### Service Job  ##########################
    class CleaningJob(Job):
        def __init__(self):
            super(CleaningJob, self).__init__()
            self.id = "Cleaning"
            self.type = "Service"

            # Traits/Job-types associated with this job:
            self.occupations = ["Service"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Maid"]] # Corresponding traits...

            # Relevant skills and stats:
            self.skills = ["cleaning"]
            self.stats = ["agility"]

        def __call__(self, cleaners_original, cleaners, building, dirt, dirt_cleaned):
            self.all_workers = cleaners_original
            workers = cleaners
            self.loc = building
            self.dirt, self.dirt_cleaned = dirt, dirt_cleaned
            self.clean()

        def is_valid_for(self, char):
            if "Service" in worker.traits:
                return True
            if worker.status == 'slave':
                return True

            if worker.disposition >= self.calculate_disposition_level(char):
                return True
            else:
                return False

        def calculate_disposition_level(self, char): # calculating the needed level of disposition
            # sub = check_submissivity(char)
            # if "Shy" in worker.traits:
                # disposition = 800 + 50 * sub
            # else:
                # disposition = 700 + 50 * sub
            # if cgochar(char, "SIW"):
                # disposition -= 500
            # if "Exhibitionist" in worker.traits:
                # disposition -= 200
            # if "Nymphomaniac" in worker.traits:
                # disposition -= 50
            # elif "Frigid" in worker.traits:
                # disposition += 50
            # if check_lovers(char, hero):
                # disposition -= 50
            # elif check_friends(hero, char):
                # disposition -= 25
            # return disposition
            return 500

        def check_occupation(self, char=None):
            """Checks if the worker is willing to do this job.
            """
            return True # Don't want to mess with this atm.

        def clean(self):
            """Build a report for cleaning team effort.
            (Keep in mind that a single worker is also a posisbility here) <== Important when building texts.

            This one is simpler... it just logs the stats, picks an image and builds a report...
            """
            self.img = Fixed(xysize=(820, 705))
            self.img.add(Transform(self.loc.img, size=(820, 705)))
            vp = vp_or_fixed(self.all_workers, ["maid", "cleaning"], {"exclude": ["sex"], "resize": (150, 150), "type": "any"})
            self.img.add(Transform(vp, align=(.5, .9)))

            self.team = self.all_workers

            log = ["{} cleaned {} today!".format(", ".join([w.nickname for w in self.all_workers]), self.loc.name)]

            # Stat mods
            self.logloc('dirt', -self.dirt_cleaned)
            for w in self.all_workers:
                log.logws('vitality', -randint(15, 25), w)  # = ? What to do here?
                log.logws('exp', randint(15, 25), w) # = ? What to do here?
                if dice(33):
                    log.logws('service', 1, w) # = ? What to do here?
            # ... We prolly need to log how much dirt each individual worker is cleaning or how much wp is spent...
            self.event_type = "jobreport" # Come up with a new type for team reports?
            self.apply_stats()
            self.finish_job()


    class ServiceJob(Job):
        """The class that solves Bartending, Waitressing and Cleaning.

        TODO: Rewrite to work with SimPy! *Or this actually should prolly be split into three Jobs...
        """
        def __init__(self):
            """
            This is meant to pick a job that makes most sense out if Cleaning, Service and Bartending
            """
            super(ServiceJob, self).__init__()
            self.type = "Service"

            # Traits/Job-types associated with this job:
            self.occupations = ["Server"] # General Strings likes SIW, Warrior, Server...
            # self.occupation_traits = [traits["Service"]] # Corresponding traits...

        def __call__(self, char, loc):
            worker, self.loc = char, loc

            self.task = None # Service task

            # Get the ap cost and cash it
            if worker.AP >= 2:
                aprelay = choice([1, 2])
                self.APr = aprelay
                worker.AP -= aprelay
            else:
                self.APr = worker.AP
                worker.AP = 0

            workermod = {}
            self.locmod = {}

            # tl.timer("Life/Injury/Vitality")
            self.check_life()
            if not self.finished: self.check_injury()
            if not self.finished: self.check_vitality()

            # tl.timer("Occupation", nested=False)
            if not self.finished: self.check_occupation()

            # tl.timer("Client Relay", nested=False)
            if not self.finished: self.client_relay()

            # tl.timer("Setting task", nested=False)
            if not self.finished: self.set_task()

            # tl.timer("Bar", nested=False)
            if self.task == "Bar" and not self.finished: self.bar_task()

            # tl.timer("Club", nested=False)
            if self.task == 'Club' and not self.finished: self.club_task()

            # tl.timer("Clean", nested=False)
            if not self.finished: self.cleaning_task()
            # tl.timer("Clean")

        def check_occupation(self):
            """Checks the workers occupation against the job.
            """
            if [t for t in self.all_occs if t in worker.occupations]:
                if worker.status == 'slave':
                    log.append(choice(["%s has no choice but to agree to clean and serve tables."%worker.fullname,
                                                        "She'll clean and tend to customer needs for you, does not mean she'll enjoy it.",
                                                        "%s is a slave so she'll do as she is told. However you might want to concider giving her work fit to her profession."%worker.name]))

                    log.logws("joy", -3)

                elif worker.disposition < 700:
                    log.append(choice(["%s refused to serve! It's not what she wishes to do in life."%worker.name,
                                            "%s will not work as a Service Girl, find better suited task for her!"%worker.fullname]))

                    log.logws('disposition', -50)
                    self.img = worker.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")

                    worker.action = None
                    self.apply_stats()
                    self.finish_job()

                else:
                    log.append("%s reluctantly agreed to be a servicer. It's not what she wishes to do in life but she admires you to much to refuse. "%worker.name)

            else:
                log.append(choice(["%s will work as a service girl!"%worker.name,
                                        "Cleaning, cooking, bartending...",
                                        "%s will clean or tend to customers next!"%worker.fullname]))

            if isinstance(log, list):
                log.append("\n")

        def set_task(self):
            """
            Sets the task for the girl.
            """
            if self.loc.servicer['second_round']:
                if not worker.autocontrol['S_Tasks']['clean']:
                    log.append("%s will not clean (check her profile for more information)." % worker.nickname)
                    self.img = 'profile'
                    self.apply_stats()
                    workers.remove(worker)
                    self.finish_job()
                elif self.loc.dirt > 0:
                    self.task = "Cleaning"
                else:
                    workers.remove(worker)

            elif self.loc.get_dirt_percentage()[0] > 80 and not worker.autocontrol['S_Tasks']['clean']:
                if self.loc.auto_clean:
                    self.auto_clean()
                    if self.loc.get_dirt_percentage()[0] <= 80:
                        self.set_task()
                        return
                    else:
                        log.append("%s doesn't clean and you do not have the fund to pay professional cleaners!" % worker.nickname)
                        self.img = 'profile'
                        self.apply_stats()
                        workers.remove(worker)
                        self.finish_job()
                        return

                elif worker.autocontrol['S_Tasks']['clean']:
                    log.append("Your brothel was too dirty for any task but cleaning!")
                    self.task = "Cleaning"

            elif self.loc.servicer['barclientsleft'] > 0 or self.loc.servicer['clubclientsleft'] > 0:
                if self.loc.servicer['barclientsleft'] > 0 and self.loc.servicer['clubclientsleft'] > 0:
                    if worker.autocontrol['S_Tasks']['bar'] and worker.autocontrol['S_Tasks']['waitress']:
                        self.task = choice(['Bar', 'Club'])
                elif self.loc.servicer['barclientsleft'] > 0 and worker.autocontrol['S_Tasks']['bar']:
                    self.task = "Bar"
                elif self.loc.servicer['clubclientsleft'] > 0 and worker.autocontrol['S_Tasks']['waitress']:
                    self.task = "Club"
                elif self.loc.dirt > 0 and worker.autocontrol['S_Tasks']['clean']:
                    self.task = "Cleaning"
                else:
                    log.append("There were no tasks remaining or this girl is not willing to do them (check her profile for more info).")
                    self.img = 'profile'
                    self.apply_stats()
                    workers.remove(worker)
                    self.finish_job()

            elif self.loc.dirt > 0 and worker.autocontrol['S_Tasks']['clean']:
                self.task = "Cleaning"

            log.append("\n")

        def bar_brawl_event(self):
            """
            Solve for bar brawls.
            """
            aggressive_clients = [client for client in self.clients if "Aggressive" in client.traits]

            if self.task == 'Bar':
                # Brawl event (For now activates on pure chance, should be improved upon later)
                # TODO!: Refactor to activate on clientList after traits are hardcoded in clients class!

                if len(aggressive_clients) >= 2 and self.loc.guardevents['barbrawlevents'] < 1 and not dice(self.loc.security_rating/10):
                    # Relay
                    self.loc.guardevents['barbrawlevents'] += 1

                    if self.loc.servicer['barclientsleft'] < 10:
                        pass

                    else:
                        log.append("{color=[red]}%s has spotted a number of customers about to start trouble. "%(worker.fullname))
                        log.append("She immediately called for security! \n{/color}")

                        if not solve_job_guard_event(self, "bar_event", clients=self.loc.servicer["barclientsleft"], enemies=aggressive_clients, no_guard_occupation="ServiceGirl"):
                            self.apply_stats()
                            self.finish_job()

                if not self.finished:
                    log.append("\n")




    class ExplorationData(Job):
        def __init__(self):
            """Creates a new GuardJob.
            """
            super(GuardJob, self).__init__()
            self.id = "Guarding"
            self.type = "Combat"

            # Traits/Job-types associated with this job:
            self.occupations = ["Warrior"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Warrior"], traits["Mage"], traits["Knight"], traits["Shooter"], traits["Battle Mage"]] # Corresponding traits...

            # Relevant skills and stats:
            self.skills = ["cleaning"]
            self.stats = ["agility"]

            workermod = {}
            self.locmod = {}

        def __call__(self):
            pass

        def explore(self):
            """Makes a ND report of the Exploration run.
            """
            # Create a dict of characters to enable im.Sepia (=dead)) when constructing the image.
            # False for alive and True for dead.
            characters = {c: False for c in self.team}
            dead = 0

            for char in self.team:
                if worker.location != "After Life":
                    worker.action = None
                    worker.location = worker.flag("loc_backup")
                    worker.del_flag("loc_backup")

                    for stat in self.stats:
                        if stat == "exp":
                            self.stats[stat] = worker.adjust_exp(self.stats[stat])
                            worker.exp += self.stats[stat]
                        else:
                            worker.mod_stat(stat, self.stats[stat])

                else:
                    characters[char] = True
                    dead = dead + 1

            # Handle the dead chars:
            skip_rewards = False

            if dead:
                if len(self.team) == dead:
                    log.append("\n{color=[red]}The entire party was wiped out (Those poor girlz...)! This can't be good for your reputation (and you obviously not getting any rewards))!{/color}\n")
                    hero.reputation -= 30
                    skip_rewards = True

                else:
                    log.append("\n{color=[red]}You get reputation penalty as %d of your girls never returned from the expedition!\n{/color}" % dead)
                    hero.reputation -= 7*dead

            if not skip_rewards:
                # Rewards + logging in global area
                cash = sum(self.cash)
                hero.add_money(cash, reason="Fighters Guild")
                fg.fin.log_logical_income(cash, "Fighters Guild")

                for item in self.items:
                    hero.inventory.append(items[item])

                self.cash = sum(self.cash)
                if self.captured_girl:
                    # We place the girl in slave pens (general jail of pytfall)
                    jail.add_prisoner(self.captured_girl, flag="SE_capture")
                    log.append("{color=[green]}\nThe team has captured a girl, she's been sent to City Jail for 'safekeeping'!{/color}\n")

                area = fg_areas[self.area.id]
                area.known_items |= set(self.found_items)
                area.cash_earned += self.cash
                area.known_mobs |= self.area.known_mobs

                for key in area.unlocks.keys():
                    area.unlocks[key] += randrange(1, int(max(self.day, (self.day * self.risk/25), 2)))

                    if dice(area.unlocks[key]):
                        if key in fg_areas:
                            fg_areas[key].unlocked = True
                            log.append("\n {color=[blue]}Team found Area: %s, it is now unlocked!!!{/color}" % key)

                        del area.unlocks[key]

            fg.exploring.remove(self)

            if not self.flag_red:
                self.flag_green = True
                fg.flag_green = True

            if self.flag_red:
                fg.flag_red = True

            # Create the event:
            evt = NDEvent()
            evt.red_flag = self.flag_red
            evt.green_flag = self.flag_green
            evt.charmod = self.stats
            evt.type = 'exploration_report'
            evt.char = None
            self.loc = fg

            # New style:
            args = list()
            for g in characters:
                if characters[g]:
                    # Dead:
                    args.append(im.Sepia(g.show("battle_sprite", resize=(200, 200), cache=True)))

                else:
                    # Alive!
                    args.append(g.show("battle_sprite", resize=(200, 200), cache=True))

            # args = list(g.show("battle_sprite", resize=(200, 200), cache=True) for g in self.team)
            img = Fixed(ProportionalScale(self.area.img, 820, 705, align=(0.5, 0.5)),
                        Text("%s"%self.team.name, style="agrevue", outlines=[ (1, crimson, 3, 3) ], antialias=True, size=30, color=red, align=(0.5, 0)),
                        HBox(*args, spacing=10, align=(0.5, 1.0)),
                        xysize=(820, 705))

            evt.img = img
            evt.txt = "".join(log)
            NextDayEvents.append(evt)
