init -9 python:
    def vp_or_fixed(workers, show_args, show_kwargs, xmax=820):
        """This will create a sidescrolling displayable to show off all portraits/images in team efforts if they don't fit on the screen in a straight line.

        We will attempt to detect a size of a single image and act accordingly. Spacing is 15 pixels between the images.
        Dimensions of the whole displayable are: 820x705, default image size is 90x90.
        xmax is used to determine the max size of the viewport/fixed returned from here
        """
        # See if we can get a required image size:
        lenw = len(workers)
        size = show_kwargs.get("resize", (90, 90))
        xpos_offset = size[0] + 15
        xsize = xpos_offset * lenw
        ysize = size[1]

        if xsize < xmax:
            d = Fixed(xysize=(xsize, ysize))
            xpos = 0
            for i in workers:
                _ = i.show(*show_args, **show_kwargs)
                d.add(Transform(_, xpos=xpos))
                xpos = xpos + xpos_offset
            return d
        else:
            d = Fixed(xysize=(xsize, ysize))
            xpos = 0
            for i in workers:
                _ = i.show(*show_args, **show_kwargs)
                d.add(Transform(_, xpos=xpos))
                xpos = xpos + xpos_offset

            c = Fixed(xysize=(xsize*2, ysize))
            atd = At(d, mm_clouds(xsize, 0, 25))
            atd2 = At(d, mm_clouds(0, -xsize, 25))
            c.add(atd)
            c.add(atd2)
            vp = Viewport(child=c, xysize=(xmax, ysize))
            return vp

    def can_do_work(c, check_ap=True):
        """Checks whether the character is injured/tired/has AP and sets her/him to auto rest.

        AP check is optional here, with True as default, there are cases where char might still have job points even though AP is 0.
        """
        if c.health < c.get_max("health")*0.25:
            # log.append("%s is injured and in need of medical attention! "%c.name)
            # self.img = c.show("profile", "sad", resize=(740, 685))
            if c.autocontrol['Rest']:
                c.previousaction = c.action
                c.action = AutoRest()
                # log.append("She is going to take few days off to heal her wounds. ")
            return False
        if c.vitality < 30:
            # log.append("%s is to tired to work today! "%c.name)
            # self.img = c.show("profile", "sad", resize=(740, 685))
            if c.autocontrol['Rest']:
                c.previousaction = c.action
                c.action = AutoRest()
                # log.append("She's going to take few days off to recover her stamina. ")
            return False
        if check_ap and c.AP <= 0:
            return False

        return True

    def check_submissivity(c):
        """Here we determine how submissive the character is, thus if she's willing to do something she doesn't want to, or for example take the initiative in certain cases.
        """
        mult = 1.0*c.character/c.get_max("character") # the idea is based on the character stat, we check how close is she to max possible character at her level
        if "Impersonal" in c.traits: # and traits, they can make mult more or less, so for example even low character tsundere might be more stubborn than high character dandere
            mult -= 0.1
        elif "Imouto" in c.traits:
            mult -= 0.05
        elif "Dandere" in c.traits:
            mult -= 0.15
        elif "Tsundere" in c.traits:
            mult += 0.2
        elif "Kuudere" in c.traits:
            mult += 0.15
        elif "Kamidere" in c.traits:
            mult += 0.23
        elif "Bokukko" in c.traits:
            mult += 0.2
        elif "Ane" in c.traits:
            mult += 0.05
        elif "Yandere" in c.traits: # in case of yandere disposition is everything
            if c.disposition <= 500:
                mult += 0.25
            else:
                mult -= 0.25
        if "Courageous" in c.traits:
            mult += 0.05
        elif "Coward" in c.traits:
            mult -= 0.05
        if "Shy" in c.traits:
            mult -= 0.05
        if "Aggressive" in c.traits:
            mult += 0.05
        if "Natural Leader" in c.traits:
            mult += 0.05
        elif "Natural Follower" in c.traits:
            mult -= 0.05
        if mult < 0.35: # there are 3 levels of submissiveness, we return -1, 0 or 1, it's very simple to use in further calculations
            return -1
        elif mult > 0.67:
            return 1
        else:
            return 0


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
        """
        def __init__(self, type='', txt='', img='', char=None, charmod={}, loc=None, locmod={}, red_flag=False, green_flag=False, team=None, job=None, **kwargs):
            super(NDEvent, self).__init__(txt)
            # describes the type of event
            self.job = job
            if not type and job:
                self.type = job.event_type
            else:
                self.type = type
            # the description of the event
            self.txt = txt
            # information on the event image or a displayable
            self.img = img
            # the character involved in the event (optional)
            self.char = char
            # Team, this overrides char property in the ND reports and is used for team events:
            self.team = team
            # Same as above, just for stats:
            if team:
                self.team_charmod = charmod.copy()
                self.charmod = None
            else:
                # stat changes of a char (optional)
                self.charmod = charmod.copy()
                self.team_charmod = None
            # the location of the event (optional)
            self.loc = loc
            # stat changes of that location (optional)
            self.locmod = locmod.copy()

            self.kind = kwargs.get("kind", None)

            self.green_flag = green_flag
            self.red_flag = red_flag

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

        def logws(self, s, value, char=None):
            # Logs stats changes.
            # Uses internal dict on chars namespace
            if char is None:
                char = self.char
            char.logws(s, value)

        def after_job(self):
            # We run this after job but before ND reports
            if self.char:
                self.char.stats_skills = {}
            if self.team:
                for char in self.team:
                    char.stats_skills = {}


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
            self.type = None

            # New teams:
            self.team = None
            worker = None # Default for single worker jobs.
            self.flag = None # Flag we pass around from SimPy land to Jobs to carry over events/data.

            # Traits/Job-types associated with this job:
            self.occupations = list() # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = set() # Corresponing traits... # TODO: WE NEED TO MAKE SURE THESE ARE INSTANCES!

            self.disposition_threshold = 650 # Any worker with disposition this high will be willing to do the job even without matched traits.

            self.img = Null()
            self.flag_red = False
            self.flag_green = False

            self.event_type = event_type

            # Each job should have two dicts of stats/skills to evaluate chars ability of performing it:
            self.base_skills = dict()
            self.base_stats = dict()
            # Where key: value are stat/skill: weight!

        def __call__(self, worker, event_type="jobreport"):
            worker = worker
            self.loc = worker.location
            self.event_type = event_type

        def __str__(self):
            return str(self.id)

        def reset(self):
            # All flags starting with 'jobs' are reset here. All flags starting with '_jobs' are reset on end of ND.
            # New, we reset any flags that start with "job_" that a character might have.
            if hasattr(self, "worker") and worker:
                for f in worker.flags.keys():
                    if f.startswith("jobs"):
                        worker.del_flag(f)
            if hasattr(self, "all_workers") and self.all_workers:
                for w in self.all_workers:
                    for f in w.flags.keys():
                        if f.startswith("jobs"):
                            w.del_flag(f)

            self.all_workers = None
            self.loc = None
            self.team = None
            self.client = None
            self.event_type = None
            self.img = Null()
            self.flags = Null()

            self.flag_red = False
            self.flag_green = False

        @property
        def all_occs(self):
            # All Occupations:
            return set(self.occupations + self.occupation_traits)

        def is_valid_for(self, char):
            # Returns True if char is willing to do the job else False...
            # Slave case:
            if worker.status == "slave":
                # we want to add all jobs there, except for the guard job:
                # Since we do not have a Guard job yet, we'll just throw all the jobs in there:
                return True

            # Free chars:
            elif worker.status in ("free", "various"):
                # Here we got to figure out somehow, which jobs char might be willing to do:
                # Get all jobs that are not a match to the character basetraits and are below disposition treshold:
                if worker.disposition > self.disposition_threshold:
                    return True
                elif not isinstance(char, PytGroup):
                    if [t for t in self.all_occs if t in worker.occupations]:
                        return True

            return False

        def get_clients(self):
            # This returns a correct amount of clients used for the job
            return 0

        def create_nd_event(self, worker=None, img=None, log=None, team=None, loc=None):
            # We could create the event before hand? Instead of just logging data to it at jobs end!
            return NDEvent(type=self.event_type,
                           img=img,
                           txt="",
                           char=worker,
                           team=None,
                           charmod={},
                           loc=None,
                           locmod={},
                           green_flag={},
                           red_flag={})

        def settle_workers_disposition(self, char=None):
            # Formerly check_occupation
            """Settles effects of worker who already agreed to do the job.

            Normaly deals with disposition, joy and vitality (for some reason?)
            """
            return True

        def check_life(self):
            """
            Checks whether the worker is alive.
            Might be deprecated, needs updating.
            """
            if not worker.alive:
                log.append("%s is dead. \n"%worker.fullname)
                workers.remove(worker)
                self.img = im.Sepia(worker.show('profile'), resize=(740, 685))
                self.finish_job()

        def finish(self):
            """
            Finish the job and adds it to NextDayEvents.
            """
            NextDayEvents.append(self.create_event())
            self.reset()

        def apply_stats(self):
            """
            Applies the stat changes generated by this job to the worker.

            Now adapted to work with teams...
            """
            # Worker Stats/Skills:
            for k, v in workermod.iteritems():
                # Normal single worker report is assumed:
                if isinstance(k, basestring):
                    self.apply_worker_stats(worker, workermod)
                    break
                else: # Team effort:
                    self.apply_worker_stats(k, v)

            # Building Stats:
            for stat in self.locmod:
                if stat == 'fame':
                    self.loc.modfame(self.locmod[stat])
                elif stat == 'dirt':
                    if self.locmod[stat] < 0:
                        self.loc.clean(-self.locmod[stat])
                    else:
                        self.loc.dirt += self.locmod[stat]
                elif stat == 'reputation':
                    self.loc.modrep(self.locmod[stat])
                else:
                    raise Exception("Stat: {} does not exits for Businesses".format(stat))

        def apply_worker_stats(self, worker, mods):
            """Apply stats for a single worker.

            This is split from apply_stats to allow for a better readable code.
            """
            for key in mods:
                if key == "exp":
                    mods[key] = worker.adjust_exp(mods[key])
                    worker.exp += mods[key]
                # After a long conversation with Dark and CW, we've decided to prevent workers dieing during jobs
                # I am leaving the code I wrote before that decision was reached in case
                # we change our minds or add jobs like exploration where it makes more sense.
                # On the other hand just ignoring it is bad, so let's at least reduce some stuff, pretending that she lost consciousness for example.
                elif key == 'health' and (worker.health + mods[key]) <= 0:
                    worker.health = 1
                    if worker.constitution > 5:
                        worker.constitution -= 5
                else:
                    if worker.stats.is_stat(key):
                        worker.mod_stat(key, mods[key])

                    elif worker.stats.is_skill(key):
                        setattr(worker, key, mods[key])

        def loggs(self, s, value, worker=None):
            """Logs workers stat/skill to a dict:

            If worker argument is provided, we assume this reports a team effort and build the report accordingly.
            """
            pass
            # if worker:
            #     if not worker in workermod:
            #         workermod[worker] = dict()
            #     workermod[worker][s] = workermod.get(s, 0) + value
            # else:
            #     workermod[s] = workermod.get(s, 0) + value

        def logloc(self, s, value):
            # Logs a stat for the building:
            pass
            # self.locmod[s] = workermod.get(s, 0) + value

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

        def effectiveness(self, worker, difficulty):
            """We check effectiveness here during jobs from SimPy land.

            difficulty is used to counter worker tier.
            100 is considered a score where worker does the task with acceptible performance.
            """
            if worker.occupations.intersection(self.occupations):
                effectiveness = 50
            else:
                effectiveness = 0

            # 25 points for difference between difficulty/tier:
            diff = difficulty - worker.tier
            effectiveness += diff*25

            return effectiveness


    ####################### Whore Job  ############################
    class WhoreJob(Job):
        def __init__(self):
            super(WhoreJob, self).__init__()
            self.id = "Whore Job"
            self.type = "SIW"
            self.event_type = "jobreport"

            # Traits/Job-types associated with this job:
            self.occupations = ["SIW"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Prostitute"]] # Corresponding traits...

            self.disposition_threshold = 950 # Any worker with disposition this high will be willing to do the job even without matched traits.

            self.base_skills = {"sex": 60, "vaginal": 40, "anal": 40, "oral": 40}
            self.base_stats = {"charisma": 100}

        def __call__(self, char, client):
            pass
            # self.event_type = "jobreport"
            # worker, self.client, self.loc = char, client, worker.location
            # worker.AP -= 1
            # self.payout_mod()
            # self.acts(char, client)

        def is_valid_for(self, worker):
            if "Prostitute" in worker.traits or worker.status == 'slave':
                return True
            if worker.disposition >= self.calculate_disposition_level(worker):
                return True
            else:
                return False

        def calculate_disposition_level(self, worker): # calculating the needed level of disposition
            sub = check_submissivity(worker)
            if "Shy" in worker.traits:
                disposition = 900 + 50 * sub
            else:
                disposition = 850 + 50 * sub
            if cgochar(worker, "SIW"):
                disposition -= 100
            if "Nymphomaniac" in worker.traits:
                disposition -= 150
            elif "Frigid" in worker.traits:
                disposition += 150
            if check_lovers(worker, hero):
                if "Virgin" in worker.traits:
                    disposition += 100
                else:
                    disposition -= 100
            elif check_friends(hero, worker):
                if "Virgin" in worker.traits:
                    disposition += 50
                else:
                    disposition -= 50
            elif "Virgin" in worker.traits:
                disposition += 50
            return disposition

        def settle_workers_disposition(self, worker):
            if not("Prostitute" in worker.traits) and worker.disposition < self.calculate_disposition_level(worker):
                sub = check_submissivity(worker)
                if worker.status != 'slave':
                    if sub < 0:
                        if dice(15):
                            worker.logws('character', 1)
                        worker.set_flag("jobs_whoreintro", "%s is not very happy with her current job as a harlot, but she will get the job done." % worker.name)
                    elif sub == 0:
                        if dice(25):
                            worker.logws('character', 1)
                        worker.set_flag("jobs_whoreintro", "%s serves customers as a whore, but, truth be told, she would prefer to do something else." % worker.nickname)
                    else:
                        if dice(35):
                            worker.logws('character', 1)
                        worker.set_flag("jobs_whoreintro", "%s makes it clear that she wants another job before getting busy with a client." % worker.name)
                    difference = (self.calculate_disposition_level(worker) - worker.disposition)/6 # penalty is based on the difference between current and min needed disposition
                    if difference < 1:
                        difference = 1
                    worker.logws("joy", -randint(5, 10))
                    worker.logws("disposition", -randint(0, int(difference)))
                    worker.logws('vitality', -randint(5, 15)) # TODO WTF IS VITALITY DOING HERE???? LOGGED DIRECTLY TO DICT NONE THE LESS!!!!??????????????????????????????
                else:
                    if sub < 0:
                        worker.set_flag("jobs_whoreintro", choice(["%s is a slave so no one really cares but, being forced to work as a whore, she's quite upset." % worker.name, "%s will do as she is told, but doesn't mean that she'll be happy about doing 'it' with strangers." % worker.name]))
                        if dice(25):
                            worker.logws('character', 1)
                    elif sub == 0:
                        worker.set_flag("jobs_whoreintro", choice(["%s was very displeased by her order to work as a whore, but didn't dare to refuse." % worker.name, "%s will do as you command, but she will hate every second of her harlot shift..." % worker.name]))
                        if dice(35):
                            worker.logws('character', 1)
                    else:
                        worker.set_flag("jobs_whoreintro", choice(["%s was very displeased by her order to work as a whore, and makes it clear for everyone before getting busy with a client." % worker.name, "%s will do as you command and work as a harlot, but not without a lot of grumbling and complaining." % worker.name]))
                        if dice(45):
                            worker.logws('character', 1)
                    difference = (self.calculate_disposition_level(worker) - worker.disposition)/5
                    if difference < 1:
                        difference = 1
                    if worker.joy < 50: # slaves additionally get more disposition penalty with low joy
                        difference += randint(0, (50-worker.joy))
                    worker.logws("joy", -randint(5, 10))
                    worker.logws("disposition", -randint(0, int(difference)))
                    worker.logws('vitality', -randint(10, 25))
            else:
                worker.set_flag("jobs_whoreintro", choice(["%s is doing her shift as a harlot." % worker.name, "%s gets busy with a client." % worker.fullname, "%s serves customers as a whore." % worker.nickname]))
            return True

        def payout_mod(self):
            self.payout = 1

        def acts(self, worker, client, loc, log):
            skill = 0
            # Pass the flags from occupation_checks:
            log.append(worker.flag("jobs_whoreintro"))
            log.append("\n\n")

            width = 820
            height = 705

            size = (width, height)
            # Acts, Images, Tags and things Related:
            # Straight Sex Act
            if client.act == 'sex':
                kwargs = dict(exclude=["rape", "angry", "in pain", "dungeon", "sad", "gay", "restrained"], resize=size, type="reduce", add_mood=False)
                log.append(choice(["%s hired her for some good old straight sex. " % client.name, "%s is willing to pay for her pussy. " % client.name]))
                if "Lesbian" in worker.traits: # lesbians will have only a part of skill level compared to others during normal sex
                    skill = round(worker.get_skill("vaginal")*0.6 + worker.get_skill("sex")*0.15)
                    vaginalmod = 1 if dice(20) else 0
                    sexmod = 1 if dice(8) else 0
                else:
                    skill = round(worker.get_skill("vaginal")*0.75 + worker.get_skill("sex")*0.25)
                    vaginalmod = 1 if dice(25) else 0
                    sexmod = 1 if dice(10) else 0
                # Temporarily done here, should be moved to game init and after_load to improve performance
                # probably not everything though, since now we don't form huge lists of pictures for some acts, using get_image_tags to figure out poses
                if worker.has_image("2c vaginal", **kwargs):
                    log.img = worker.show("2c vaginal", **kwargs)
                else:
                    log.img = worker.show("after sex", exclude=["angry", "in pain", "dungeon", "sad"], **kwargs)
                image_tags = log.img.get_image_tags()
                if "ontop" in image_tags:
                    log.append("He invited her to 'sit' on his lap as he unsheathed his cock. They've continued along the same lines in 'girl ontop' position. \n")
                elif "doggy" in image_tags:
                    log.append("He ordered %s to bend over and took her from behind. \n"%worker.nickname)
                elif "missionary" in image_tags:
                    log.append("He pushed %s on her back, shoved his cock in, screaming: 'Oh, Your pussy is wrapping around me so tight!' \n"%worker.nickname)
                elif "onside" in image_tags:
                    log.append("%s lay on her side inviting the customer to fuck her. He was more than happy to oblige.\n"%worker.nickname)
                elif "standing" in image_tags:
                    log.append("Not even bothering getting into a position, he took her standing up. \n")
                elif "spooning" in image_tags:
                    log.append("Customer felt cuddly so he spooned the girl until they both cummed. \n")
                else:
                    log.append(choice(['He wanted some old-fashioned straight fucking. \n',
                                                         'He was in the mood for some pussy pounding. \n',
                                                         'He asked for some playtime with her vagina.\n']))
                # Virgin trait check:
                self.take_virginity(worker, loc, log)


            # Anal Sex Act
            elif client.act == 'anal':
                kwargs = dict(exclude=["rape", "angry", "in pain", "dungeon", "sad", "gay", "restrained"], resize=size, type="reduce", add_mood=False)
                log.append(choice(["%s hired her for some anal fun. " % client.name, "%s is willing to pay her for backdoor action. " % client.name]))
                if "Lesbian" in worker.traits:
                    skill = round(worker.get_skill("anal")*0.6 + worker.get_skill("sex")*0.15)
                    analmod = 1 if dice(20) else 0
                    sexmod = 1 if dice(8) else 0
                else:
                    skill = round(worker.get_skill("anal")*0.75 + worker.get_skill("sex")*0.25)
                    analmod = 1 if dice(25) else 0
                    sexmod = 1 if dice(10) else 0
                log.append(choice(["Anal sex is the best, customer thought... ",
                                                      "I am in the mood for a good anal fuck, customer said. ",
                                                      "Customer's dick got harder and harder just from the thought of %s's asshole! "%worker.nickname]))

                if worker.has_image("2c anal", **kwargs):
                    log.img = worker.show("2c anal", **kwargs)
                else:
                    log.img = worker.show("after sex", exclude=["angry", "in pain", "dungeon", "sad"], **kwargs)
                image_tags = log.img.get_image_tags()
                if "ontop" in image_tags:
                    log.append("He invited her to 'sit' on his lap as he unsheathed his cock. They've continued along the same lines in 'girl on top' position. \n")
                elif "doggy" in image_tags:
                    log.append("He ordered %s to bend over and took her from behind. \n"%worker.nickname)
                elif "missionary" in image_tags:
                    log.append("He pushed %s on her back, shoved his cock in, screaming: 'Oh, Your anus is wrapping around me so tight!' \n"%worker.nickname)
                elif "onside" in image_tags:
                    log.append("%s lays on her side inviting the customer to fuck her. He was more than happy to oblige.\n"%worker.nickname)
                elif "standing" in image_tags:
                    log.append("Not even bothering getting into a position, he took her standing up. \n")
                elif "spooning" in image_tags:
                    log.append("Customer felt cuddly so he spooned the girl until they both cummed. \n")
                else:
                    log.append(choice(['He took her in the ass right there and then. \n',
                                                          'He got his dose of it. \n',
                                                          'And so he took her in her butt. \n']))

            # Various job acts
            elif client.act == 'blowjob':
                kwargs = dict(exclude=["rape", "angry", "in pain", "dungeon", "sad", "gay", "restrained"], resize=size, type="reduce", add_mood=False)
                log.append(choice(["%s hired her for some side job on his thing. " % client.name, "%s is paying her today for naughty service. " % client.name]))
                # here we will have to choose skills depending on selected act
                tags = ({"tags": ["bc deepthroat"], "exclude": ["rape", "angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["bc handjob"], "exclude": ["rape", "angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["bc footjob"], "exclude": ["rape", "angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["bc titsjob"], "exclude": ["rape", "angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["bc blowjob"], "exclude": ["rape", "angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["after sex"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"], "dice":20})
                act = self.get_act(worker, tags)
                if act == tags[0]:
                    log.append(choice(["He shoved his cock all the way into her throat! \n", "Deepthroat is definitely my style, thought the customer... \n"]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("oral")*0.65 + worker.get_skill("sex")*0.1)
                        oralmod = 1 if dice(20) else 0
                        sexmod = 1 if dice(8) else 0
                    else:
                        skill = round(worker.get_skill("oral")*0.8 + worker.get_skill("sex")*0.2)
                        oralmod = 1 if dice(25) else 0
                        sexmod = 1 if dice(10) else 0
                    log.img = worker.show("bc deepthroat", **kwargs)
                elif act == tags[1]:
                    log.append("He told %s to give him a good handjob.\n"%worker.nickname)
                    if "Lesbian" in worker.traits: # lesbians will have 0.7 of skill level compared to others during normal sex
                        skill = round(worker.get_skill("oral")*0.1 + worker.get_skill("sex")*0.6)
                        oralmod = 1 if dice(20) else 0
                        sexmod = 1 if dice(8) else 0
                    else:
                        skill = round(worker.get_skill("oral")*0.25 + worker.get_skill("sex")*0.75)
                        oralmod = 1 if dice(25) else 0
                        sexmod = 1 if dice(10) else 0
                    log.img = worker.show("bc handjob", **kwargs)
                elif act == tags[2]:
                    log.append(choice(["He asked her for a footjob.\n", "Footjob might be a weird fetish but that's what the customer wanted...\n"]))
                    if "Lesbian" in worker.traits: # lesbians will have 0.7 of skill level compared to others during normal sex
                        skill = round(worker.get_skill("oral")*0.1 + worker.get_skill("sex")*0.6)
                        oralmod = 1 if dice(20) else 0
                        sexmod = 1 if dice(8) else 0
                    else:
                        skill = round(worker.get_skill("oral")*0.25 + worker.get_skill("sex")*0.75)
                        oralmod = 1 if dice(25) else 0
                        sexmod = 1 if dice(10) else 0
                    log.img = worker.show("bc footjob", **kwargs)
                elif act == tags[3]:
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("oral")*0.1 + worker.get_skill("sex")*0.65)
                        sexmod = 1 if dice(20) else 0
                        oralmod = 1 if dice(8) else 0
                    else:
                        skill = round(worker.get_skill("oral")*0.2 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(25) else 0
                        oralmod = 1 if dice(10) else 0
                    if traits["Big Boobs"] in worker.traits or traits["Abnormally Large Boobs"] in worker.traits:
                        log.append(choice(["He went straight for her big boobs. \n", "Seeing her knockers, customer wanted nothing else then to park his dick between them. \n", "Lustfully gazing on your girl's burst, he asked for a titsjob. \n", "He put his manhood between her big tits. \n" , "He showed his cock between %s's enormous breasts. \n"%worker.nickname]))
                    elif traits["Small Boobs"] in worker.traits:
                        if dice(15):
                            log.append("With a smirk on his face, customer asked for a titsjob. He was having fun from her vain efforts. \n")
                        else:
                            log.append(choice(["He placed his cock between her breasts, clearly enjoining her flat chest. \n", "Even when knowing that her breasts are small, he wanted to be caressed by them. \n"]))
                    else:
                        log.append(choice(["He asked for a titsjob. \n", "He let %s to caress him with her breasts. \n", "He showed his cock between %s's tits. \n"%worker.nickname]))
                    log.img = worker.show("bc titsjob", **kwargs)
                elif act == tags[4]:
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("sex")*0.75)
                        sexmod = 1 if dice(20) else 0
                    else:
                        skill = round(worker.get_skill("oral")*0.1 + worker.get_skill("sex")*0.9)
                        sexmod = 1 if dice(25) else 0
                        oralmod = 1 if dice(5) else 0
                    log.append(choice(["Customer wanted nothing else then to jerk himself in from of her and ejaculate on her face. \n", "He wanked himself hard in effort to cover her with his cum. \n"]))
                    log.img = worker.show("after sex", **kwargs)
                elif act == tags[5]:
                    log.append(choice(['Client was in mood for some oral sex. \n', 'Client was in the mood for a blowjob. \n', 'He asked her to lick his dick. \n']))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("oral")*0.65 + worker.get_skill("sex")*0.1)
                        sexmod = 1 if dice(20) else 0
                        oralmod = 1 if dice(8) else 0
                    else:
                        skill = round(worker.get_skill("oral")*0.8 + worker.get_skill("sex")*0.2)
                        sexmod = 1 if dice(25) else 0
                        oralmod = 1 if dice(10) else 0
                    log.img = worker.show("bc blowjob", **kwargs)
                else: # I do not thing that this will ever be reached...
                    log.append(choice(['Client was in mood for some oral sex. \n', 'Client was in the mood for a blowjob. \n', 'He asked her to lick his dick. \n']))
                    skill = worker.get_skill("oral")
                    oralmod = 1 if dice(20) else 0
                    log.img = worker.show("bc blowjob", **kwargs)

            # Lesbian Act
            elif client.act == 'lesbian':
                log.append("%s hired her for some hot girl on girl action. " % client.name)
                skill = worker.get_skill("vaginal")
                kwargs = dict(exclude=["rape", "angry", "in pain", "dungeon", "sad", "restrained"], resize=size, type="reduce", add_mood=False)
                tags = ({"tags": ["gay", "2c lickpussy"], "exclude": ["rape", "angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "bc lickpussy"], "exclude": ["rape", "angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "2c lickanus"], "exclude": ["rape", "angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "bc lickanus"], "exclude": ["rape", "angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "2c vaginalfingering"], "exclude": ["rape", "angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "bc vagnalhandjob"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "2c analfingering"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "bc analhandjob"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "2c caresstits"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "bc caresstits"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "bc hug", "2c hug"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "2c vaginal"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "bc vaginal"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "2c anal"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "bc anal"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "2c vaginaltoy"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "bc toypussy"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "2c analtoy"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "bc toyanal"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]}, {"tags": ["gay", "scissors"], "exclude": ["angry", "in pain", "dungeon", "sad", "restrained"]})
                act = self.get_act(worker, tags)
                # We'll be adding "les" here as Many lesbian pics do not fall in any of the categories and will never be called...
                if act == tags[0]:
                    log.append(choice(["Clearly in the mood for some cunt, she licked %ss pussy clean.\n"%worker.nickname,
                                                         "Hungry for a cunt, she told %s to be still and started licking her soft pussy with her hot tong. \n"%worker.nickname]))
                    if "Lesbian" in worker.traits: # bisexuals will have normal value during lesbian action, lesbians will get ~1.2 of skill, and straight ones ~0.8
                        skill = round(worker.get_skill("oral")*0.2 + worker.get_skill("vaginal")*0.2 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(25) else 0
                        oralmod = 1 if dice(10) else 0
                        vaginalmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("oral")*0.15 + worker.get_skill("vaginal")*0.15 + worker.get_skill("sex")*0.7)
                        sexmod = 1 if dice(22) else 0
                        oralmod = 1 if dice(9) else 0
                        vaginalmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("oral")*0.1 + worker.get_skill("vaginal")*0.1 + worker.get_skill("sex")*0.6)
                        sexmod = 1 if dice(20) else 0
                        oralmod = 1 if dice(8) else 0
                        vaginalmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "2c lickpussy", **kwargs)
                elif act == tags[1]:
                    log.append(choice(["All hot and bothered, she ordered %s to lick her cunt. \n"%worker.nickname,
                                                         "As if she had an itch, she quickly told %s to tong her pussy. \n"%worker.nickname]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("oral")*0.8 + worker.get_skill("vaginal")*0.2 + worker.get_skill("sex")*0.2)
                        sexmod = 1 if dice(10) else 0
                        oralmod = 1 if dice(25) else 0
                        vaginalmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("oral")*0.7 + worker.get_skill("vaginal")*0.15 + worker.get_skill("sex")*0.15)
                        sexmod = 1 if dice(9) else 0
                        oralmod = 1 if dice(22) else 0
                        vaginalmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("oral")*0.6 + worker.get_skill("vaginal")*0.1 + worker.get_skill("sex")*0.1)
                        sexmod = 1 if dice(8) else 0
                        oralmod = 1 if dice(20) else 0
                        vaginalmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "bc lickpussy", **kwargs)
                elif act == tags[2]:
                    log.append(choice(["She licked %ss anus clean.\n"%worker.nickname,
                                                                                    "She told %s to be still and started licking her asshole with her hot tong. \n"%worker.nickname]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("oral")*0.2 + worker.get_skill("anal")*0.2 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(25) else 0
                        oralmod = 1 if dice(10) else 0
                        analmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("oral")*0.15 + worker.get_skill("anal")*0.15 + worker.get_skill("sex")*0.7)
                        sexmod = 1 if dice(22) else 0
                        oralmod = 1 if dice(9) else 0
                        analmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("oral")*0.1 + worker.get_skill("anal")*0.1 + worker.get_skill("sex")*0.6)
                        sexmod = 1 if dice(20) else 0
                        oralmod = 1 if dice(8) else 0
                        analmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "2c lickanus", **kwargs)
                elif act == tags[3]:
                    log.append(choice(["All hot and bothered, she ordered %s to lick her asshole. \n"%worker.nickname,
                                                         "As if she had an itch, she quickly told %s to tong her anus. \n"%worker.nickname]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("oral")*0.8 + worker.get_skill("anal")*0.2 + worker.get_skill("sex")*0.2)
                        sexmod = 1 if dice(10) else 0
                        oralmod = 1 if dice(25) else 0
                        analmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("oral")*0.7 + worker.get_skill("anal")*0.15 + worker.get_skill("sex")*0.15)
                        sexmod = 1 if dice(8) else 0
                        oralmod = 1 if dice(22) else 0
                        analmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("oral")*0.6 + worker.get_skill("anal")*0.1 + worker.get_skill("sex")*0.1)
                        sexmod = 1 if dice(8) else 0
                        oralmod = 1 if dice(20) else 0
                        analmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "bc lickanus", **kwargs)
                elif act == tags[4]:
                    log.append(choice(["In mood for a hot lesbo action, she stuck her fingers in your girls pussy. \n",
                                                         "She watched %s moan as she stuck fingers in her pussy. \n"%worker.nickname]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("vaginal")*0.4 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(25) else 0
                        vaginalmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("vaginal")*0.2 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(22) else 0
                        vaginalmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("vaginal")*0.15 + worker.get_skill("sex")*0.65)
                        sexmod = 1 if dice(20) else 0
                        vaginalmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "2c vaginalfingering", **kwargs)
                elif act == tags[5]:
                    log.append(choice(["Quite horny, she ordered your girl to finger her cunt. \n",
                                                         "Clearly in the mood, she told %s to finger her until she cums. \n"%worker.nickname]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("vaginal")*0.4 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(25) else 0
                        vaginalmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("vaginal")*0.2 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(22) else 0
                        vaginalmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("vaginal")*0.15 + worker.get_skill("sex")*0.65)
                        sexmod = 1 if dice(20) else 0
                        vaginalmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "bc vagnalhandjob", **kwargs)
                elif act == tags[6]:
                    log.append(choice(["In mood for a hot lesbo action, she stuck her fingers in your girls anus. \n",
                                                         "She watched %s moan as she stuck fingers in her asshole. \n"%worker.nickname]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("anal")*0.4 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(25) else 0
                        analmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("anal")*0.2 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(22) else 0
                        analmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("anal")*0.15 + worker.get_skill("sex")*0.65)
                        sexmod = 1 if dice(20) else 0
                        analmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "2c analfingering", **kwargs)
                elif act == tags[7]:
                    log.append(choice(["Quite horny, she ordered your girl to finger her anus. \n",
                                                         "Clearly in the mood, she told %s to finger her asshole until she cums. \n"%worker.nickname]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("anal")*0.4 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(25) else 0
                        analmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("anal")*0.2 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(22) else 0
                        analmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("anal")*0.15 + worker.get_skill("sex")*0.65)
                        sexmod = 1 if dice(20) else 0
                        analmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "bc analhandjob", **kwargs)
                elif act == tags[8]:
                    log.append(choice(["Liking your girls breasts, she had some good time caressing them. \n",
                                                         "She enjoyed herself by caressing your girls breasts. \n"]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("sex")*1.1)
                        sexmod = 1 if dice(25) else 0
                    elif "Bisexual" in worker.traits:
                        skill = worker.get_skill("sex")
                        sexmod = 1 if dice(22) else 0
                    else:
                        skill = round(worker.get_skill("sex")*0.9)
                        sexmod = 1 if dice(20) else 0
                    log.img = worker.show("gay", "2c caresstits", **kwargs)
                elif act == tags[9]:
                    log.append(choice(["She asked your girl to caress her tits. \n",
                                                         "She told your girl to put a squeeze on her breasts. \n"]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("sex")*1.1)
                        sexmod = 1 if dice(25) else 0
                    elif "Bisexual" in worker.traits:
                        skill = worker.get_skill("sex")
                        sexmod = 1 if dice(22) else 0
                    else:
                        skill = round(worker.get_skill("sex")*0.9)
                        sexmod = 1 if dice(20) else 0
                    log.img = worker.show("gay", "bc caresstits", **kwargs)
                elif act == tags[10]:
                    log.append(choice(["Girls lost themselves in eachothers embrace.\n",
                                                         "Any good lesbo action should start with a hug, don't you think??? \n"]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("sex")*1.1)
                        sexmod = 1 if dice(25) else 0
                    elif "Bisexual" in worker.traits:
                        skill = worker.get_skill("sex")
                        sexmod = 1 if dice(22) else 0
                    else:
                        skill = round(worker.get_skill("sex")*0.9)
                        sexmod = 1 if dice(20) else 0
                    log.img = worker.show("gay", "bc hug", "2c hug", **kwargs)
                elif act == tags[11]:
                    log.append(choice(["She put on a strapon and fucked your girl in her cunt. \n",
                                                          "Equipping herself with a strap-on, she lustfully shoved it in %ss pussy. \n"%worker.nickname]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("vaginal")*0.9 + worker.get_skill("sex")*0.3)
                        vaginalmod = 1 if dice(25) else 0
                        sexmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("vaginal")*0.75 + worker.get_skill("sex")*0.25)
                        vaginalmod = 1 if dice(22) else 0
                        sexmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("vaginal")*0.7 + worker.get_skill("sex")*0.2)
                        vaginalmod = 1 if dice(20) else 0
                        sexmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "2c vaginal", **kwargs)
                    self.take_virginity(worker, loc, log)
                elif act == tags[12]:
                    log.append(choice(["She ordered %s to put on a strapon and fuck her silly with it. \n"%worker.nickname,
                                                          "She equipped %s with a strapon and told her that she was 'up' for a good fuck! \n" %worker.nickname]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("sex")*0.9 + worker.get_skill("vaginal")*0.3)
                        sexmod = 1 if dice(25) else 0
                        vaginalmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("sex")*0.8 + worker.get_skill("vaginal")*0.2)
                        sexmod = 1 if dice(22) else 0
                        vaginalmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("sex")*0.6 + worker.get_skill("vaginal")*0.15)
                        sexmod = 1 if dice(20) else 0
                        vaginalmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "bc vaginal", **kwargs)
                elif act == tags[13]:
                    log.append(choice(["She put on a strapon and fucked your girl in her butt. \n",
                                                          "Equipping herself with a strapon, she lustfully shoved it in %s's asshole. \n"%worker.nickname]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("anal")*0.9 + worker.get_skill("sex")*0.3)
                        analmod = 1 if dice(25) else 0
                        sexmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("anal")*0.75 + worker.get_skill("sex")*0.25)
                        analmod = 1 if dice(22) else 0
                        sexmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("anal")*0.6 + worker.get_skill("sex")*0.2)
                        analmod = 1 if dice(20) else 0
                        sexmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "2c anal", **kwargs)
                elif act == tags[14]:
                    log.append(choice(["She ordered %s to put on a strapon and butt-fuck her silly with it. \n"%worker.nickname,
                                                         "She equipped %s with a strapon and told her that she was 'up' for a good anal fuck! \n"]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("sex")*0.9 + worker.get_skill("anal")*0.3)
                        sexmod = 1 if dice(25) else 0
                        analmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("sex")*0.8 + worker.get_skill("anal")*0.2)
                        sexmod = 1 if dice(22) else 0
                        analmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("sex")*0.6 + worker.get_skill("anal")*0.15)
                        sexmod = 1 if dice(20) else 0
                        analmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "bc anal", **kwargs)
                elif act == tags[15]:
                    log.append(choice(["She played with a toy and %ss pussy. \n"%worker.nickname,
                                                         "She stuck a toy up %s cunt. \n"%worker.nickname]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("vaginal")*0.4 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(25) else 0
                        vaginalmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("vaginal")*0.2 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(22) else 0
                        vaginalmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("vaginal")*0.15 + worker.get_skill("sex")*0.65)
                        sexmod = 1 if dice(20) else 0
                        vaginalmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "2c vaginaltoy", **kwargs)
                    self.take_virginity(worker, loc, log)
                elif act == tags[16]:
                    log.append(choice(["Without further ado, %s fucked her with a toy. \n"%worker.nickname,
                                                         "She asked your girl to fuck her pussy with a toy. \n"]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("vaginal")*0.4 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(25) else 0
                        vaginalmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("vaginal")*0.2 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(22) else 0
                        vaginalmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("vaginal")*0.15 + worker.get_skill("sex")*0.65)
                        sexmod = 1 if dice(20) else 0
                        vaginalmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "bc toypussy", **kwargs)
                elif act == tags[17]:
                    log.append(choice(["After some foreplay, she stuck a toy up your girls butt. \n",
                                                                                   "For her money, she had some fun playing with a toy and your girls asshole. \n"]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("anal")*0.4 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(25) else 0
                        analmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("anal")*0.2 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(22) else 0
                        analmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("anal")*0.15 + worker.get_skill("sex")*0.65)
                        sexmod = 1 if dice(20) else 0
                        analmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "2c analtoy", **kwargs)
                elif act == tags[18]:
                    log.append(choice(["After some foreplay, she asked %s to shove a toy up her ass. \n"%worker.nickname,
                                                         "This female customer of your brothel clearly believed that there is no greater pleasure than a toy up her butt. \n"]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("anal")*0.4 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(25) else 0
                        analmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("anal")*0.2 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(22) else 0
                        analmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("anal")*0.15 + worker.get_skill("sex")*0.65)
                        sexmod = 1 if dice(20) else 0
                        analmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "bc toyanal", **kwargs)
                elif act == tags[19]:
                    log.append(choice(["She was hoping to get some clit to clit action, and she got it. \n",
                                                         "The female customer asked for a session of hot, sweaty tribadism. \n"]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("anal")*0.4 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(25) else 0
                        analmod = 1 if dice(10) else 0
                    elif "Bisexual" in worker.traits:
                        skill = round(worker.get_skill("anal")*0.2 + worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(22) else 0
                        analmod = 1 if dice(9) else 0
                    else:
                        skill = round(worker.get_skill("anal")*0.15 + worker.get_skill("sex")*0.65)
                        sexmod = 1 if dice(20) else 0
                        analmod = 1 if dice(8) else 0
                    log.img = worker.show("gay", "scissors", **kwargs)
                else:
                    log.append(choice(["She was in the mood for some girl on girl action. \n", "She asked for a good lesbian sex. \n"]))
                    if "Lesbian" in worker.traits:
                        skill = round(worker.get_skill("sex")*1.1)
                        sexmod = 1 if dice(25) else 0
                    elif "Bisexual" in worker.traits:
                        skill = worker.get_skill("sex")
                        sexmod = 1 if dice(22) else 0
                    else:
                        skill = round(worker.get_skill("sex")*0.8)
                        sexmod = 1 if dice(20) else 0
                    log.img = worker.show("gay", **kwargs)
                    # Last fallback!

            else:
                log.append("Whore Job\n\nMissed All acts!\n\n")

                skill = worker.get_skill("sex")
                log.img = worker.show("sex", **kwargs)

            self.check_skills(skill, worker, client, log)

            # Take care of stats mods
            constmod = 1 if dice(12) else 0
            worker.logws("constitution", constmod)
            worker.logws("vitality", -randint(14, 28))
            sexskill = 0
            if 'sexmod' in locals():
                worker.logws("sex", sexmod)
                sexskill += 1
            if 'vaginalmod' in locals():
                worker.logws("vaginal", vaginalmod)
                sexskill += 1
            if 'analmod' in locals():
                worker.logws("anal", analmod)
                sexskill += 1
            if 'oralmod' in locals():
                worker.logws("oral", oralmod)
                sexskill += 1
            if sexskill + constmod > 0:
                log.append("\n%s feels like she learned something! \n"%worker.name)
                worker.logws("joy", 1)


            # Dirt:
            self.logloc("dirt", randint(2, 5))

            # Log income for worker and MC
            log.append("{color=[gold]}\nA total of %d Gold was earned!{/color}" % self.payout)
            worker.fin.log_wage(self.payout, "WhoreJob")
            loc.fin.log_work_income(self.payout, "WhoreJob")

            # self.apply_stats()
            # self.finish_job()

        @staticmethod
        def get_act(worker, tags):
            acts = list()
            for t in tags:
                if isinstance(t, tuple):
                    if worker.has_image(*t):
                        acts.append(t)
                elif isinstance(t, dict):
                    if worker.has_image(*t.get("tags", []), exclude=t.get("exclude", [])) and dice(t.get("dice", 100)):
                        acts.append(t)

            if acts:
                act = choice(acts)
            else:
                act = None

            return act

        @staticmethod
        def take_virginity(worker, loc, log): # let's just assume that dildos are too small to take virginity, otherwise it becomes too complicated in terms of girls control :)
            if traits["Virgin"] in worker.traits and not (worker.effects['Chastity']['active']):
                tips = 100 + worker.charisma * 3 # TODO Slave/Free payouts
                log.append("\n{color=[pink]}%s lost her virginity!{/color} Customer thought that was super hot and left a tip of {color=[gold]}%d Gold{/color} for the girl.\n\n"%(worker.nickname, tips))
                worker.remove_trait(traits["Virgin"])
                worker.fin.log_tips(tips, "WhoreJob")
                loc.fin.log_work_income(tips, "WhoreJob")

        def check_skills(self, skill, worker, client, log):
            # I'm making checks for stats and skills separately, otherwise it will be a nightmare even with an army of writers
            # first is charisma, as initial impression
            if worker.charisma >= 1500:
                log.append("Her supernal loveliness made the customer to shed tears of happiness, comparing %s to ancient goddess of love. Be wary of possible cults dedicated to her..." %worker.name)
                self.loggs("joy", 1)
                self.logloc("fame", choice([0, 1, 1, 1]))
                self.logloc("reputation", choice([0, 1]))
            elif worker.charisma >= 800:
                log.append("%s made the customer fall in love with her unearthly beauty. Careful now girl, we don't need crowds of admires around our businesses..." %worker.name)
                self.loggs("joy", 1)
                self.logloc("fame", choice([0, 1]))
                self.logloc("reputation", choice([0, 0, 1]))
            elif worker.charisma >= 500:
                log.append("%s completely enchanted the customer with her stunning beauty." %worker.name)
                self.logloc("fame", choice([0, 0, 1]))
                self.logloc("reputation", choice([0, 0, 0, 1]))
            elif worker.charisma >= 200:
                log.append("The client was happy to be alone with such a breathtakingly beautiful girl as %s." %worker.name)
                self.logloc("fame", choice([0, 0, 0, 1]))
            elif worker.charisma >= 100:
                log.append("%s good looks clearly was pleasing to the customer." %worker.name)
            elif worker.charisma >= 50:
                log.append("%s did her best to make the customer like her, but her beauty could definitely be enhanced." %worker.name)
                self.logloc("fame", choice([-1, 0, 0, 1]))
            else:
                self.loggs("joy", -2)
                self.logloc("fame", choice([-1, 0]))
                if client.gender == "male":
                    log.append("The customer was unimpressed by %s looks, to say at least. Still, he preferred fucking her over a harpy. Hearing that from him however, was not encouraging for the poor girl at all..." %worker.name)
                else:
                    log.append("The customer was unimpressed by %s looks, to say at least. Still, she preferred fucking her over a harpy. Hearing that from her however, was not encouraging for the poor girl at all..." %worker.name)
            # then a small refinement check, useless with low charisma
            if dice(worker.get_skill("refinement")*0.1) and worker.charisma >= 150:
                log.append(" Her impeccable manners also made a very good impression." %worker.name)
                self.logloc("reputation", choice([0, 0, 1]))
            # then we check for skill level
            log.append("\n")
            if skill >= 4000:
                if client.gender == "male":
                    log.append("The client was at the girls mercy. She brought him to the heavens and left there, unconscious due to sensory overload.")
                else:
                    log.append("The client was at the girls mercy. She brought her to the heavens and left there, unconscious due to sensory overload.")
                self.loggs("exp", randint(250, 500))
                self.logloc("reputation", choice([0, 1]))
                self.loggs("joy", 3)
            elif skill >= 2000:
                if client.gender == "male":
                    log.append("She playfully took the customer into embrace and made him forget about the rest of the world until they were finished.")
                else:
                    log.append("She playfully took the customer into embrace and made her forget about the rest of the world until they were finished.")
                self.loggs("exp", randint(100, 200))
                self.logloc("reputation", choice([0, 0, 1]))
                self.loggs("joy", 2)
            elif skill >= 1000:
                log.append("She performed wonderfully with her unmatched carnal skill, making the customer exhausted and completely satisfied.")
                self.loggs("exp", randint(50, 120))
                self.loggs("joy", 2)
            elif skill >= 500:
                log.append("Her well honed sexual tricks and techniques were very pleasing to the customer, and she was quite pleased in return by client's praises.")
                self.loggs("exp", randint(40, 75))
                self.loggs("joy", 1)
            elif skill >= 200:
                log.append("$s did the job to the best of her ability but her skills could definitely be improved." %worker.name)
                self.loggs("exp", randint(35, 45))
            elif skill >= 50:
                log.append("The girl barely knew what she was doing. Still, %s somewhat managed to provide basic service, following impatient instructions of the client." %worker.name)
                self.loggs("exp", randint(20, 35))
            else:
                self.loggs("exp", randint(15, 25))
                if worker.charisma >= 200:
                    log.append("A cold turkey sandwich would have made a better sex partner than %s. Her performance was however somewhat saved by her looks." %worker.name)
                else:
                    log.append("Unfortunately, %s barely knew what she was doing. Her looks were not likely to be of any help to her either." %worker.name)
            if skill < 500: # with low skill wrong orientation will take some vitality
                if ("Lesbian" in worker.traits) and (client.gender == "male"):
                    log.append(" It was a bit difficult for %s to do it with a man due to her sexual orientation..." %worker.name)
                    self.loggs("vitality", randint(-25, -5))
                elif (client.gender == "female") and not("Lesbian" in worker.traits) and not("Bisexual" in worker.traits):
                    log.append(" It was a bit difficult for %s to do it with a woman due to her sexual orientation..." %worker.name)
                    self.loggs("vitality", randint(-25, -5))
            log.append("\n")


    ####################### Strip Job  ############################
    class StripJob(Job):
        """
        Class for the solving of stripping logic.
        """
        def __init__(self):
            super(StripJob, self).__init__()
            self.id = "Striptease Job"
            self.type = "SIW"

            # Traits/Job-types associated with this job:
            self.occupations = ["SIW"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Stripper"]] # Corresponding traits...

            # Relevant skills and stats:
            self.skills = ["strip", "dancing"]
            self.stats = ["charisma"]

        def __call__(self, char):
            worker, self.loc = char, worker.location
            self.clients = worker.flag("jobs_strip_clients")
            self.strip()

        def is_valid_for(self, char):
            if "Stripper" in worker.traits:
                return True
            if worker.status == 'slave':
                return True

            if worker.disposition >= self.calculate_disposition_level(char):
                return True
            else:
                return False

        def calculate_disposition_level(self, char): # calculating the needed level of disposition
            sub = check_submissivity(char)
            if "Shy" in worker.traits:
                disposition = 800 + 50 * sub
            else:
                disposition = 700 + 50 * sub
            if cgochar(char, "SIW"):
                disposition -= 500
            if "Exhibitionist" in worker.traits:
                disposition -= 200
            if "Nymphomaniac" in worker.traits:
                disposition -= 50
            elif "Frigid" in worker.traits:
                disposition += 50
            if check_lovers(char, hero):
                disposition -= 50
            elif check_friends(hero, char):
                disposition -= 25
            return disposition

        def check_occupation(self, char=None):
            """Checks if the worker is willing to do this job.
            """
            if not("Stripper" in worker.traits) and worker.disposition < self.calculate_disposition_level(char):
                sub = check_submissivity(char)
                if worker.status != 'slave':
                    if sub < 0:
                        if dice(15):
                            self.loggs('character', 1)
                        worker.set_flag("jobs_stripintro", "%s is not very happy with her current job as a stripper, but she will get the job done." % worker.name)
                    elif sub == 0:
                        if dice(25):
                            self.loggs('character', 1)
                        worker.set_flag("jobs_stripintro", "%s shows her goods to customers, but she would prefer to do something else." % worker.nickname)
                    else:
                        if dice(35):
                            self.loggs('character', 1)
                        worker.set_flag("jobs_stripintro", "%s makes it clear that she wants another job before going to the stage." % worker.name)
                    difference = (self.calculate_disposition_level(char) - worker.disposition)/8
                    if difference < 1:
                        difference = 1
                    if sub <0:
                        if dice(15):
                            self.loggs('character', 1)
                    elif sub == 0:
                        if dice(25):
                            self.loggs('character', 1)
                    else:
                        if dice(35):
                            self.loggs('character', 1)
                    worker.logws("joy", -randint(1, 10))
                    worker.logws("disposition", -randint(0, int(difference)))
                    worker.logws('vitality', -randint(5, 15))
                else:
                    sub = check_submissivity(char)
                    if sub<0:
                        worker.set_flag("jobs_stripintro",choice(["%s is a slave so no one really cares but, being forced to work as a stripper, she's quite upset." % worker.name, "%s will do as she is told, but doesn't mean that she'll be happy about showing her body to strangers." % worker.name]))
                        if dice(25):
                            self.loggs('character', 1)
                    elif sub==0:
                        worker.set_flag("jobs_stripintro",choice(["%s was very displeased by her order to work as a stripper, but didn't dare to refuse." % worker.name, "%s will do as you command, but she will hate every second of her stripper shift..." % worker.name]))
                        if dice(35):
                            self.loggs('character', 1)
                    else:
                        worker.set_flag("jobs_stripintro",choice(["%s was very displeased by her order to work as a stripper, and makes it clear for everyone before going to the stage." % worker.name, "%s will do as you command and work as a stripper, but not without a lot of grumbling and complaining." % worker.name]))
                        if dice(45):
                            self.loggs('character', 1)
                    difference = (self.calculate_disposition_level(char) - worker.disposition)/7
                    if difference < 1:
                        difference = 1
                    if worker.joy < 50:
                        difference += randint(0, (50-worker.joy))
                    worker.logws("joy", -randint(10, 15))
                    worker.logws("disposition", -randint(0, int(difference)))
                    worker.logws('vitality', -randint(10, 15))
            else:
                worker.set_flag("jobs_stripintro", choice(["%s is doing her shift as a stripper." % worker.name, "%s shows her goods to clients." % worker.fullname, "%s entertains customers with her body at the stage." % worker.nickname]))

            return True

        def strip(self):
            # Pass the flags from occupation_checks:
            log.append(worker.flag("jobs_stripintro"))
            log.append("\n\n")

            # Determine the amount of clients who seen this girl strip. We check if we can do len because if flag wasn't set during the business execution, we get False instead of a set.
            len_clients = len(self.clients) if self.clients else 0

            tippayout = worker.flag("jobs_" + self.id + "_tips")
            skill = round(worker.get_skill("strip")*0.75 + worker.get_skill("dancing")*0.25)
            charisma = worker.charisma

            if charisma >= 1500:
                log.append("%s supernal loveliness instantly captivated audiences. " %worker.name)
                self.loggs("joy", 1)
            elif worker.charisma >= 1000:
                log.append("The attention of customers was entirely focused on %s thanks to her prettiness. " %worker.name)
                self.loggs("joy", 1)
            elif worker.charisma >= 500:
                log.append("%s enchanted customers with her stunning beauty. " %worker.name)
            elif worker.charisma >= 200:
                log.append("Customers were delighted with %s beauty. " %worker.name)
            elif worker.charisma >= 100:
                log.append("%s good looks was pleasing to audiences. " %worker.name)
            elif worker.charisma >= 50:
                log.append("%s did her best to make customers like her, but her beauty could definitely be enhanced. " %worker.name)
            else:
                self.loggs("joy", -2)
                log.append("Customers clearly were unimpressed by %s looks, to say at least. Such a cold reception was not encouraging for the poor girl at all..." %worker.name)

            log.append("\n")
            if skill >= 4000:
                log.append("She gave an amazing performance, her sexy and elegant moves forced a few customers to come right away to their own embarrassment.")
                self.loggs("exp", randint(250, 500))
                self.logloc("reputation", choice([0, 1]))
                self.loggs("joy", 3)
            elif skill >= 2000:
                log.append("She gave a performance worthy of kings and queens as the whole hall was cheering for her.")
                self.loggs("exp", randint(100, 200))
                self.logloc("reputation", choice([0, 0, 1]))
                self.loggs("joy", 2)
            elif skill >= 1000:
                log.append("She lost all of her clothing piece by piece as she gracefully danced on the floor, the whole hall was cheering for her.")
                self.loggs("exp", randint(50, 120))
                self.loggs("joy", 2)
            elif skill >= 500:
                log.append("She lost all of her clothing piece by piece as she danced on the floor, some mildly drunk clients cheered for her.")
                self.loggs("exp", randint(40, 75))
                self.loggs("joy", 1)
            elif skill >= 200:
                log.append("She danced to the best of her ability but her skills could definitely be improved.")
                self.loggs("exp", randint(35, 45))
            elif skill >= 50:
                log.append("She barely knew what she was doing. Her performance can hardly be called a striptease, but at least she showed enough skin to arouse some men and women in the club.")
                self.loggs("exp", randint(20, 35))
            else:
                self.loggs("exp", randint(15, 25))
                if worker.charisma >= 200:
                    log.append("She tripped several times while trying to undress herself as she 'stripdanced' on the floor. Still, she was pretty enough to arouse some men and women in the club.")
                else:
                    log.append("She certainly did not shine as she clumsily 'danced' on the floor. Neither her looks nor her skill could save the performance...")

                    log.append("\n")

            # Take care of stats mods
            if "Exhibitionist" in worker.traits:
                stripmod = 1 if dice(35) else 0
            else:
                stripmod = 1 if dice(25) else 0
            dancemod = 1 if dice(15) else 0
            agilemod = 1 if dice(9) else 0
            charismamod = 1 if dice(20) else 0

            self.loggs("agility", agilemod)
            self.loggs('vitality', randrange(-31, -15))
            self.loggs("charisma", charismamod)
            self.loggs("dancing", dancemod)
            self.loggs("strip", stripmod)

            if stripmod + agilemod + dancemod + charismamod > 0:
                log.append("\n%s feels like she learned something! \n"%worker.name)
                self.loggs("joy", 1)

            # Finances:
            worker.fin.log_tips(tippayout, "StripJob")
            self.loc.fin.log_work_income(tippayout, "StripJob")

            available = list()
            kwargs = dict(exclude=["sad", "angry", "in pain"], resize=(740, 685), type="first_default", add_mood=False)
            if worker.has_image("stripping", "stage", exclude=["sad", "angry", "in pain"]):
                available.append("stage")
            if worker.has_image("stripping", "simple bg", exclude=["sad", "angry", "in pain"]):
                available.append("simple bg")
            if worker.has_image("stripping", "no bg", exclude=["sad", "angry", "in pain"]):
                available.append("no bg")
            if available:
                self.img = worker.show("stripping", choice(available), **kwargs)
            elif worker.has_image("stripping", "indoors"):
                self.img = worker.show("stripping", "indoors", **kwargs)
            else:
                self.img = worker.show("stripping", **kwargs)

            self.event_type = "jobreport"
            self.kind = self.id
            self.apply_stats()
            self.finish_job()


    ####################### Rest Job  #############################
    class Rest(Job):
        """Resting for character, technically not a job...
        """
        def __init__(self):
            """
            Creates a new Rest.
            worker = The girl to solve for.
            """
            super(Rest, self).__init__()
            self.id = "Rest"
            self.type = "Resting"

        def __call__(self, char):
            worker = char
            self.loc = worker.home
            self.rest()
            self.after_rest()

        def rest(self):
            """Rests the worker.
            """
            # Stat Mods:


            worker.disable_effect('Exhausted')  # rest immediately disables the effect and removes its counter

            available = list()
            if (worker.disposition >= 250) or ("Exhibitionist" in worker.traits):
                kwargs = dict(exclude=["dungeon", "sad", "angry", "in pain", "after sex", "group", "normalsex", "bdsm"], add_mood=False) # with not too low disposition nude pics become available during rest
            else:
                kwargs = dict(exclude=["dungeon", "sad", "nude", "angry", "in pain", "after sex", "group", "normalsex", "bdsm"], add_mood=False)
            if worker.has_image("sleeping", **kwargs):
                available.append("sleeping")
            if worker.has_image("reading", **kwargs):
                available.append("reading")
            if worker.vitality > 50:
                if worker.has_image("shopping", **kwargs) and (worker.gold >= 200): # eventually there should be a real existing event about going to shop and buy a random item there for gold. after all we do have an algorithm for that. but atm it might be broken, so...
                    available.append("shopping")
                if "Nymphomaniac" in worker.traits and worker.disposition >= 300: # if we'll have some kind of high libido flags, they could be used here too
                    if worker.has_image("masturbation", **kwargs):
                        available.append("masturbation")
            if worker.vitality > 150:
                if worker.has_image("sport", **kwargs):
                    available.append("sport")
                if worker.has_image("exercising", **kwargs):
                    available.append("exercising")
            if worker.has_image("eating", **kwargs):
                available.append("eating")
            if worker.has_image("bathing", **kwargs):
                available.append("bathing")
            if worker.has_image("rest", **kwargs):
                available.append("rest") # there always will be a simple rest, providing non-empty list. The only exception is a lack of any non nude pics, in which case we will allow to them with any disposition
            if not(available):
                if worker.has_image("rest"):
                    available.append("rest")
                else:
                    available.append("profile", exclude=["sad", "angry", "in pain"]) # no rest at all? c'mon...

            if ("sleeping" in available) and (worker.vitality <= 50):
                    self.img = worker.show("sleeping", resize=(740, 685), **kwargs)
                    log.append("{} is too tired to do anything but sleep at her free time.".format(worker.name))
            else:
                self.img = worker.show(choice(available), resize=(740, 685), **kwargs)
                image_tags = self.img.get_image_tags()
                if "sleeping" in image_tags:
                    if "living" in image_tags:
                        log.append("{} is enjoying additional bedtime in her room.".format(worker.name))
                    elif "beach" in image_tags:
                        log.append("{} takes a small nap at the local beach.".format(worker.name))
                    elif "nature" in image_tags:
                        log.append("{} takes a small nap in the local park.".format(worker.name))
                    else:
                        log.append("{} takes a small nap during her free time.".format(worker.name))
                elif "masturbation" in image_tags:
                    log.append(choice(["{} has some fun with herself during her free time.".format(worker.name),
                                                 "{} is relieving her sexual tension at free time.".format(worker.name)]))
                elif "onsen" in image_tags:
                    log.append("{} relaxes in the onsen. The perfect remedy for stress!".format(worker.name))
                elif "reading" in image_tags:
                    log.append(choice(["{} spends her free time reading.".format(worker.name),
                                                 "{} is enjoying a book and relaxing.".format(worker.name)]))
                elif "shopping" in image_tags:
                    log.append(choice(["{} spends her free time to visit some shops.".format(worker.name),
                                                 "{} is enjoying a small shopping tour.".format(worker.name)]))
                elif "exercising" in image_tags:
                    log.append("{} keeps herself in shape doing some exercises during her free time.".format(worker.name))
                elif "sport" in image_tags:
                    log.append("{} is in a good shape today, so she spends her free time doing sports.".format(worker.name))
                elif "eating" in image_tags:
                    log.append(choice(["{} has a snack during her free time.".format(worker.name),
                                                 "{} spends her free time enjoying a meal.".format(worker.name)]))
                elif "bathing" in image_tags:
                    if "pool" in image_tags:
                        log.append("{} spends her free time enjoying swimming in the local swimming pool.".format(worker.name))
                    elif "beach" in image_tags:
                        log.append("{} spends her free time enjoying swimming at the local beach. The water is great today!".format(worker.name))
                    elif "living" in image_tags:
                        log.append("{} spends her free time enjoying a bath.".format(worker.name))
                    else:
                        log.append("{} spends her free time relaxing in a water.".format(worker.name))
                else:
                    if "living" in image_tags:
                        log.append(choice(["{} is resting in her room.".format(worker.name),
                                                 "{} is taking a break in her room to recover.".format(worker.name)]))
                    elif "beach" in image_tags:
                            log.append(choice(["{} is relaxing at the local beach.".format(worker.name),
                                                    "{} is taking a break at the local beach.".format(worker.name)]))
                    elif "pool" in image_tags:
                            log.append(choice(["{} is relaxing in the local swimming pool.".format(worker.name),
                                                    "{} is taking a break in the local swimming pool.".format(worker.name)]))
                    elif "nature" in image_tags:
                        if ("wildness" in image_tags):
                            log.append(choice(["{} is resting in the local forest.".format(worker.name),
                                                    "{} is taking a break in the local forest.".format(worker.name)]))
                        else:
                            log.append(choice(["{} is resting in the local park.".format(worker.name),
                                                    "{} is taking a break in the local park.".format(worker.name)]))
                    elif ("urban" in image_tags) or ("public" in image_tags):
                            log.append(choice(["{} is relaxing somewhere in the city.".format(worker.name),
                                                    "{} is taking a break somewhere in the city.".format(worker.name)]))
                    else:
                            log.append(choice(["{} is relaxing during her free time.".format(worker.name),
                                                    "{} is taking a break during her free time.".format(worker.name)]))


            self.loggs('health', randint(2, 3))
            if worker.effects['Drowsy']['active']:
                self.loggs('vitality', (randint(30, 50)*worker.AP))
            else:
                self.loggs('vitality', (randint(15, 30)*worker.AP))
            self.loggs('mp', randint(1, 3))
            self.loggs('joy', randint(1, 2))

            if not self.img:
                self.img = worker.show("rest", resize=(740, 685))

        def is_rested(self):
            if (worker.vitality >= worker.get_max("vitality") - 50) and (worker.health >= worker.get_max('health') - 5):
                return True

        def after_rest(self):
            """
            Solve the final logic.
            """
            self.apply_stats()

            if self.is_rested():
                log.append("\n\nShe is both well rested and healthy so at this point this is simply called: {color=[red]}slacking off :){/color}")

            self.finish_job()


    class AutoRest(Rest):
        """
        Same as Rest but game will try to reset character to it's previos job.
        """
        def __init__(self):
            super(AutoRest, self).__init__()
            self.id = "AutoRest"

        def after_rest(self):
            """
            Solve the final logic.
            """
            self.apply_stats()

            if self.is_rested():
                log.append("\n\nShe is now both well rested and healthy, so she goes back to work as %s!" % worker.previousaction)
                worker.action = worker.previousaction
                worker.previousaction = None

                if worker.autoequip:
                    # **Adapt to new code structure...
                    equip_for(worker, worker.action)

            self.finish_job()


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
    class TestingJob(Job):
        """
        Very Simple job that can be used for testing or as a "Blue Print"
        """
        def __init__(self):
            super(TestingJob, self).__init__()
            self.id = "Testing Job"
            self.type = "Service"

        def __call__(self, char, client):
            # Basic job that takes 1 AP of a girl, removes client from queue and adds random stats/skills.
            # Next thing is to make this work with Rest Job!
            self.reset()

            self.event_type = "jobreport"
            worker, self.loc = char, worker.location

            self.client = client

            char, cl = worker, self.client

            self.loggs("charisma", randint(1, 3))
            self.loggs("Refinement", randint(1, 3))
            self.loggs("refinement", randint(1, 3))
            self.loggs("strip", randint(1, 3))

            worker.AP -= 1
            self.loggs("vitality", 35)

            self.logloc("dirt", 10)

            log.append("Test Job Report: Girl: {}, Location: {}".format(worker.name, self.loc.name))
            self.img = "nude"

            self.apply_stats()
            self.finish_job()

        def get_clients(self):
            # This is never called since we know that it is a one client job without variations.
            return 1


    class Waiting(Job):
        def __init__(self):
            super(Waiting, self).__init__()
            self.id = "Waiting Job"
            self.type = "Service"

            # Traits/Job-types associated with this job:
            self.occupations = [] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [] # Corresponding traits...

            # Relevant skills and stats:
            self.skills = []
            self.stats = []

            workermod = {}
            self.locmod = {}

        def __call__(self, char):
            pass

        def club_task(self):
            """
            Solve the job as a waitress.
            """
            clientsmax = self.APr * (2 + (worker.agility * 0.05 + worker.serviceskill * 0.05 + worker.refinement * 0.01))

            if self.loc.servicer['clubclientsleft'] - clientsmax <= 0:
                clientsserved = self.loc.servicer['clubclientsleft']
                log.append("She finished serving drinks and snacks to tables of %d remaining customers. At least she got a break.  \n"%self.loc.servicer['clubclientsleft'])
                self.loc.servicer['clubclientsleft'] -= clientsserved

            elif self.loc.servicer['clubclientsleft'] - clientsmax > 0:
                clientsserved = clientsmax
                log.append("She served snacks and drinks to tables of %d clients. \n"%(clientsmax))
                self.loc.servicer['clubclientsleft'] = self.loc.servicer['clubclientsleft'] - clientsserved

            clubfees = clientsserved * self.loc.rep * 0.08 + clientsserved * 0.5 * (worker.refinement * 0.1 + worker.charisma * 0.1 + worker.service * 0.025)
            tips = 0

            log.append("\n")

            # Skill Checks
            if worker.serviceskill > 2000:
                self.locmod['reputation'] += choice([0, 1])
                clubfees = clubfees * 1.5
                tips = clubfees * 0.10
                log.append("She is an excellent waitress, customers didn't notice how they've just kept spending their money as she offered them more and more house specials. \n")

            elif worker.serviceskill >= 1000:
                self.locmod['reputation'] += choice([0,0,0,1])
                clubfees = clubfees * 1.2
                tips = clubfees * 0.07
                log.append("Customers were pleased with such a skilled waitress serving them. \n")

            elif worker.serviceskill >= 500:
                tips = clubfees * 0.03
                self.locmod['reputation'] += choice([0,0,0,0,0,1])
                log.append("She was skillful enough not to mess anything up during her job. \n")

            elif worker.serviceskill >= 100:
                self.locmod['reputation'] += choice([0,0,-1,0,0,-1])
                clubfees = clubfees * 0.8
                log.append("Her performance was rather poor and it most definitely has cost you income. \n")

            if worker.charisma > 300:
                tips = tips + clubfees*0.05
                self.locmod['fame'] += choice([0, 1, 1])
                log.append("Your girl was stunningly pretty, customers couldn't keep their eyes off her. \n")

            elif worker.charisma > 150:
                tips = tips + clubfees*0.03
                self.locmod['fame'] += choice([0 ,0, 1])
                log.append("Your girl looked beautiful, this will not go unnoticed. \n")

            elif worker.charisma > 45:
                tips = tips + clubfees*0.02
                self.locmod['fame'] += choice([0, 0, 0, 1])
                log.append("Your girl was easy on the eyes, not bad for a bartender. \n")

            elif worker.charisma > 0:
                self.locmod['fame'] += choice([0, -1, -1])
                log.append("Customers did not appreciate a hag serving them. Consider sending this girl to a beauty school. \n")

            log.append("\n")

            # Stat Mods
            workermod['vitality'] -= clientsserved * 5
            workermod['service'] += choice([0, 0, 1]) * self.APr
            workermod['agility'] += choice([0, 0, 1]) * self.APr
            workermod['exp'] += self.APr * randint(15, 25)

            self.locmod['dirt'] += clientsserved * 6

            # Integers:
            clubfees = int(round(clubfees))
            tips = int(round(tips))

            log.append("{color=[gold]}%s earned %d Gold during this shift"%(worker.nickname, clubfees))

            if tips:
                log.append(" and got %d in tips" % tips)

            log.append(".{/color}\n")

            self.img = worker.show("bunny", "waitress", exclude=["sex"], resize=(740, 685), type="any")

            # Finances:
            worker.fin.log_wage(clubfees, "Waitress")
            worker.fin.log_tips(tips, "Waitress")
            self.loc.fin.log_work_income(clubfees + tips, "Waitress")

            self.apply_stats()
            self.finish_job()


    class BarJob(Job):
        def __init__(self):
            super(BarJob, self).__init__()
            self.id = "Bartending"
            self.type = "Service"

            # Traits/Job-types associated with this job:
            self.occupations = ["Server"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Bartender"]] # Corresponding traits...

            # Relevant skills and stats:
            self.skills = ["bartending"]
            self.stats = ["charisma"]

            workermod = {}
            self.locmod = {}

        def __call__(self, char):
            worker, self.loc = char, worker.location
            self.clients = worker.flag("jobs_bar_clients")
            self.bar_task()

        def check_occupation(self, char):
            """Checks the workers occupation against the job.
            """
            if not [t for t in self.all_occs if t in worker.occupations]:
                if worker.status == 'slave':
                    temp = choice(["%s has no choice but to agree to tend the bar."%worker.fullname,
                                            "She'll tend the bar for customer, does not mean she'll enjoy it.",
                                            "%s is a slave so she'll do as she is told. However you might want to consider giving her work fit to her profession."%worker.name])
                    worker.set_flag("jobs_barintro", temp)
                    worker.set_flag("jobs_introjoy", -3)

                elif worker.disposition < 800:
                    temp = choice(["%s refused to serve! It's not what she wishes to do in life."%worker.name,
                                             "%s will not work as a Service Girl, find better suited task for her!"%worker.fullname])
                    temp = set_font_color(temp, "red")
                    log.append(temp)

                    worker = char
                    self.loc = worker.location
                    self.event_type = "jobreport"

                    self.loggs('disposition', -50)
                    self.img = worker.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")
                    worker.action = None

                    self.apply_stats()
                    self.finish_job()
                    return False

                else: # worker.disposition > 800:
                    temp = "%s reluctantly agreed to be a servicer. It's not what she wishes to do in life but she admires you to much to refuse. " % worker.name
                    worker.set_flag("jobs_barintro", temp)

            else:
                temp = choice(["%s will work as a Bartender!"%worker.name,
                                         "Tending the Bar:"])
                worker.set_flag("jobs_barintro", temp)
            return True

        def bar_task(self):
            # Pass the flags from occupation_checks:
            log.append(worker.flag("jobs_barintro"))
            log.append("\n\n")

            flag = worker.flag("jobs_introdis")
            if flag:
                self.loggs('disposition', flag)
                worker.del_flag("jobs_introdis")

            flag = worker.flag("jobs_introjoy")
            if flag:
                self.loggs('joy', flag)
                worker.del_flag("jobs_introjoy")

            # Old Code:
            # beer = self.loc.get_upgrade_mod("bar") == 2
            # tapas = self.loc.get_upgrade_mod("bar") == 3
            # clientsmax = self.APr * (4 + (worker.agility * 0.1 + worker.serviceskill * 0.08))
            # clients = plural("customer", clientsmax)
            # if self.loc.servicer['barclientsleft'] - clientsmax <= 0:
                # clientsserved = self.loc.servicer['barclientsleft']
                # if tapas:
                    # log.append("Your girl finished serving cold beer and tasty snacks to customers for the day! She even managed a small break at the end of her shift! \n")
                # elif beer:
                    # log.append("Remaining bar customers enjoyed cold draft beer. %s got a little break at the end of her shift! \n"%worker.nickname)
                # else:
                    # log.append("Your girl wrapped up the day at the bar by serving drinks to %d remaining customers. At least she got a small break.  \n"%self.loc.servicer['barclientsleft'])
                # self.loc.servicer['barclientsleft'] = 0
                # workermod['vitality'] += self.APr * randint(1, 5)

            # elif self.loc.servicer['barclientsleft'] - clientsmax > 0:
                # clientsserved = clientsmax
                # if tapas:
                    # log.append("She served cold draft beer and mouthwatering snacks to %d %s. \n"%(clientsmax, clients))
                # elif beer:
                    # log.append("She served cold and refreshing tapbeer to %d %s. \n"%(clientsmax, clients))
                # else:
                    # log.append("She served snacks and drinks at the bar to %d %s. \n" % (clientsmax, clients))
                # self.loc.servicer['barclientsleft'] = self.loc.servicer['barclientsleft'] - clientsserved
                # workermod['vitality'] -= 4 * clientsmax

            len_clients = len(self.clients)

            serviceskill = worker.get_skill("bartending")
            charisma = worker.charisma

            # Skill checks
            if serviceskill > 2000:
                self.logloc('reputation', choice([0, 1, 2]))
                log.append("She was an excellent bartender, customers kept spending their money just for the pleasure of her company. \n")

            elif serviceskill >= 1000:
                self.logloc('reputation', choice([0, 1]))
                log.append("Customers were pleased with her company and kept asking for more booze. \n")

            elif serviceskill >= 500:
                self.logloc('reputation', choice([0, 0, 0, 0, 0, 1]))
                log.append("She was skillful enough not to mess anything up during her job. \n")

            elif serviceskill >= 100:
                self.logloc('reputation', -1)
                log.append("Her performance was rather poor and it most definitely has cost you income. \n")

            else:
                self.logloc('reputation', -2)
                log.append("She is a very unskilled bartender, this girl definitely needs training \n")

            if charisma > 300:
                self.logloc('fame', choice([0,1,1]))
                log.append("Your girl was stunningly pretty, customers couldn't keep their eyes off her. \n")

            elif charisma > 150:
                self.logloc('fame', choice([0,0,1]))
                log.append("Your girl looked beautiful, this will not go unnoticed. \n")

            elif charisma > 45:
                self.logloc('fame', choice([0, 0, 0, 1]))
                log.append("Your girl was easy on the eyes, not bad for a bartender. \n")

            else:
                self.logloc('fame', -2)
                log.append("Customers did not appreciate a hag serving them. Consider sending this girl to a beauty school. \n")

            log.append("\n")

            #Stat Mods
            self.loggs('exp', randint(15, 25))
            self.loggs('bartending', choice([1, 2]))
            self.loggs('refinement', choice([0, 0, 0, 1]))
            self.loggs('vitality', len_clients * -3)

            # Integers:
            # barfees = int(round(worker.earned_cash))
            tips = int(round(worker.flag("jobs_" + self.id + "_tips")))

            if tips:
                log.append("She got %d in tips! " % tips)

            if worker.has_image("waitress", exclude=["sex"]):
                self.img = worker.show("waitress", exclude=["sex"], resize=(740, 685))
            elif worker.has_image("maid", exclude=["sex"]):
                self.img = worker.show("maid", exclude=["sex"], resize=(740, 685))
            else:
                self.img = worker.show("profile", exclude=["sex", "nude"], resize=(740, 685))

            # Finances:
            # worker.fin.log_wage(barfees, "Barmaid")
            if tips:
                worker.fin.log_tips(tips, "Barmaid")

            self.loc.fin.log_work_income(tips, "Barmaid")

            self.apply_stats()
            self.finish_job()


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
                self.loggs('vitality', -randint(15, 25), w)  # = ? What to do here?
                self.loggs('exp', randint(15, 25), w) # = ? What to do here?
                if dice(33):
                    self.loggs('service', 1, w) # = ? What to do here?
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

                    self.loggs("joy", -3)

                elif worker.disposition < 700:
                    log.append(choice(["%s refused to serve! It's not what she wishes to do in life."%worker.name,
                                            "%s will not work as a Service Girl, find better suited task for her!"%worker.fullname]))

                    self.loggs('disposition', -50)
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


    class GuardJob(Job):
        def __init__(self):
            """Creates reports for GuardJob.
            """
            super(GuardJob, self).__init__()
            self.id = "Guarding"
            self.type = "Combat"

            # Traits/Job-types associated with this job:
            self.occupations = ["Warrior"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Warrior"], traits["Mage"], traits["Knight"], traits["Shooter"]] # Corresponding traits...

            # Relevant skills and stats:
            self.skills = ["cleaning"]
            self.stats = ["agility"]

            workermod = {}
            self.locmod = {}

        def __call__(self, workers_original, workers, location, action, flag=None):
            self.all_workers = workers_original
            workers = workers
            self.loc = location
            self.flag = flag

            if action == "patrol":
                self.patrol()
            elif action == "intercept":
                self.intercept()

        def patrol(self):
            """Builds ND event for Guard Job.

            This one is simpler... it just logs the stats, picks an image and builds a report...
            """
            self.img = Fixed(xysize=(820, 705))
            self.img.add(Transform(self.loc.img, size=(820, 705)))
            vp = vp_or_fixed(self.all_workers, ["fighting"], {"exclude": ["sex"], "resize": (150, 150)}, xmax=820)
            self.img.add(Transform(vp, align=(.5, .9)))

            self.team = self.all_workers

            log = ["{} intercepted {} today!".format(", ".join([w.nickname for w in self.all_workers]), self.loc.name)]

            # Stat mods
            self.logloc('dirt', 25 * len(self.all_workers)) # 25 per guard? Should prolly be resolved in SimPy land...
            for w in self.all_workers:
                self.loggs('vitality', -randint(15, 25), w)  # = ? What to do here?
                self.loggs('exp', randint(15, 25), w) # = ? What to do here?
                for stat in ['attack', 'defence', 'magic', 'joy']:
                    if dice(20):
                        self.loggs(stat, 1, w)

            self.event_type = "jobreport" # Come up with a new type for team reports?
            self.apply_stats()
            self.finish_job()

        def intercept(self):
            """Builds ND event for Guard Job.

            This one is simpler... it just logs the stats, picks an image and builds a report...
            """
            self.img = Fixed(xysize=(820, 705))
            self.img.add(Transform(self.loc.img, size=(820, 705)))
            vp = vp_or_fixed(self.all_workers, ["fighting"], {"exclude": ["sex"], "resize": (150, 150)}, xmax=820)
            self.img.add(Transform(vp, align=(.5, .9)))

            self.team = self.all_workers

            log = ["{} intercepted a bunch of drunk miscreants in {}! ".format(", ".join([w.nickname for w in self.all_workers]), self.loc.name)]
            if self.flag.flag("result"):
                log.append("They managed to subdue them!")
            else:
                log.append("They failed to subdue them, that will cause you some issues with your clients and {} reputation will suffer!".format(self.loc.name))

            # Stat mods (Should be moved/split here).
            self.logloc('dirt', 25 * len(self.all_workers)) # 25 per guard? Should prolly be resolved in SimPy land...
            for w in self.all_workers:
                self.loggs('vitality', -randint(15, 25), w)  # = ? What to do here?
                self.loggs('exp', randint(15, 25), w) # = ? What to do here?
                for stat in ['attack', 'defence', 'magic', 'joy']:
                    if dice(20):
                        self.loggs(stat, 1, w)

            self.event_type = "jobreport" # Come up with a new type for team reports?
            self.apply_stats()
            self.finish_job()

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
                hero.add_money(cash, "Fighters Guild")
                fg.fin.log_work_income(cash, "Fighters Guild")

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
