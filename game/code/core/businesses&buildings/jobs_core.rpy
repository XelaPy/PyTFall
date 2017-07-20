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
                elif key == 'dirt': # We Handle Dirt Directly now!
                    pass # self.loc.clean(value)
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
                    self.team_charmod[char] = char.stats_skills.copy()
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
            self.occupation_traits = list() # Corresponding traits... # TODO: WE NEED TO MAKE SURE THESE ARE INSTANCES!

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
            return 0

        def settle_workers_disposition(self, char=None):
            # Formerly check_occupation
            """Settles effects of worker who already agreed to do the job.

            Normaly deals with disposition, joy and vitality (for some reason?)
            """
            return True

        # We should also have a number of methods or properties to evaluate new dicts:
        def relative_ability(self, worker, tier=None):
            """
            # Maybe just do the stats/skills interpolation here???
            # And later add that to tier calc in the effectiveness method?

            100 or above is the target for this method.
            """
            ability = 0
            if tier is None:
                tier = worker.tier
                if not tier:
                    tier = 1 # Risking ZeroDev error otherwise

            rates = []
            amount = []
            for skill, weight in self.base_skills.items():
                target_value = SKILLS_MAX[skill]*.1*tier
                real_value = worker.get_skill(skill)
                rv = 50.0*real_value/target_value # resulting value, 50 base
                rates.append(weight)
                amount.append(rv)
            # Formula from SO:
            total_skills = sum(x * y for x, y in zip(rates, amount)) / sum(amount)

            rates = []
            amount = []
            for stat, weight in self.base_stats.items():
                target_value = worker.get_max(stat)*.1*tier
                real_value = getattr(worker, stat)
                rv = 50.0*real_value/target_value # resulting value, 50 base
                rates.append(weight)
                amount.append(rv)
            # Formula from SO:
            total_stats = sum(x * y for x, y in zip(rates, amount)) / sum(amount)

            # Bonuses:
            temp = worker.occupations.intersection(self.occupations)
            bonus1 = 10 if temp else 0
            bonus2 = len(set(self.occupation_traits).intersection(worker.traits))*5

            total = total_skills + total_stats + bonus1 + bonus2

            if config.debug:
                devlog.info("Calculating Jobs Relative Ability, Char/Job: {}/{}:".format(worker.name, self.id))
                devlog.info("Gen Occ: {}, Base: {}, Skills: {}, Stats: {} ==>> {}".format(bonus1, bonus2, total_skills, total_stats, total))

            return total

        def traits_and_effects_effectiveness_mod(self, worker, difficulty, log):
            """Modifies workers effectiveness depending on traits and effects.

            returns an integer to be added to base calculations!
            """
            return 0

        def effectiveness(self, worker, difficulty, log=None):
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
