init -9 python:
    #################################################################
    # UNIQUE BUILDING CLASSES
    # The classes for actual buildings with the customizations they require.
    #
    class CityJail(BaseBuilding):
        """
        The jail where escaped slaves can turn up. May do other things later.
        """

        # TODO lt: Needs recoding!

        def __init__(self):
            super(CityJail, self).__init__()
            self.focused = None
            self.index = 0
            self.chars_list = []
            self.auto_sell_captured = False # Do we auto-sell SE captured slaves?

        def __contains__(self, char):
            return char in self.chars_list

        def add_prisoner(self, char, flag=None):
            """Adds a char to the jail.

            char: Character to throw into Jail
            flag: Sentence type (reason to put in Jail)
            """
            if char not in self:
                if char in hero.team:
                    hero.team.remove(char)
                self.chars_list.append(char)

                # Flag to determine how the girl is handled in the jail:
                if flag:
                    char.set_flag("sentence_type", flag)
                    if flag == "SE_capture":
                        char.set_flag("days_in_jail", 0)

                if self.focused is None:
                    self.focused = char
                    self.index = 0

        def buy_girl(self):
            """Buys an escaped girl from the jail.
            """
            if hero.take_ap(1):
                if hero.take_money(self.get_price(), reason="Slave Repurchase"):
                    renpy.play("content/sfx/sound/world/purchase_1.ogg")
                    self.remove_prisoner(self.worker)
                else:
                    renpy.call_screen('message_screen', "You don't have enough money for this purchase!")

            else:
                renpy.call_screen('message_screen', "You don't have enough AP left for this action!")

            if not self.chars_list:
                renpy.hide_screen("slave_shopping")

        def get_price(self):
            """
            Returns the price to retrieve the girl.
            """
            # In case of non-slave girl, use 3000 as base price
            return (self.worker.fin.get_price() or 3000) / 2

        def get_upkeep(self):
            """
            Return the upkeep cost for the girl.
            """
            return self.worker.fin.get_upkeep()

        @property
        def girlfin(self):
            """
            The property to return the proper financial data for the girl.
            """
            return self

        def next_index(self):
            """
            Sets the next index for the slavemarket.
            """
            self.index = (self.index+1) % len(self.chars_list)
            self.worker = self.chars_list[self.index]

        def previous_index(self):
            """
            Sets the previous index for the slavemarket.
            """
            self.index = (self.index-1) % len(self.chars_list)
            self.worker = self.chars_list[self.index]

        def remove_prisoner(self, char, set_location=True):
            """
            Returns an actor to the player.
            char = The char to return.
            """
            if char in self:
                char.del_flag("sentence_type")
                char.del_flag("days_in_jail")
                self.chars_list.remove(char)

                if self.chars_list:
                    self.index %= len(self.chars_list)
                    self.worker = self.chars_list[self.index]
                else:
                    self.index = 0
                    self.worker = None

                if set_location:
                    if schools[TrainingDungeon.NAME] in hero.buildings:
                        char.location = schools[TrainingDungeon.NAME]
                        char.home = schools[TrainingDungeon.NAME]
                    else:
                        char.home = locations["Streets"]
                        char.action = None
                        char.workplace = None

        def set_girl(self, girl):
            """
            Sets the girl to be the index for the slavemarket.
            girl = The girl to set.
            """
            if self.chars_list and girl in self.chars_list:
                self.worker = girl
                self.index = self.chars_list.index(self.worker)

        # Deals with girls captured during SE:
        def sell_captured(self, girl=None, auto=False):
            # Flat price of 1500 Gold - the fees:
            """
            Sells off captured girl from the jail.
            auto: Auto Selloff during next day.
            """
            if not girl:
                girl = self.worker

            if auto or hero.take_ap(1):
                if not auto:
                    renpy.play("content/sfx/sound/world/purchase_1.ogg")
                hero.add_money(1500 - self.get_fees4captured(girl), "SlaveTrade")
                self.remove_prisoner(girl)
                girl.location = pytfall.sm
                girl.home = pytfall.sm
                girl.action = None
            else:
                renpy.call_screen('message_screen', "You don't have enough AP left for this action!")

            if not auto:
                if not self.chars_list:
                    renpy.hide_screen("slave_shopping")

        def next_day(self):
            for i in self.chars_list:
                if i.flag("sentence_type") == "SE_capture":
                    i.mod_flag("days_in_jail")
                    if self.auto_sell_captured:
                        # Auto-selloff through flag set in SE module
                        # TODO se: Implement the button in SE!
                        self.sell_captured(auto=True)
                        pytfall.temp_text.append("Jail keepers sold off: {color=[red]}%s{/color}!" % i.name)
                    if i.flag("days_in_jail") > 20:
                        # Auto-Selloff in case of 20+ days:
                        self.sell_captured(auto=True)
                        pytfall.temp_text.append("Jail keepers sold off: {color=[red]}%s{/color}!" % i.name)

        def get_fees4captured(self, girl=None):
            # 200 for registration with city hall + 30 per day for "rent"
            if not girl:
                girl = self.worker
            return 200 + girl.flag("days_in_jail") * 30

        def retrieve_captured(self, direction=None):
            """
            Retrieve a captured character (during SE).
            We handle simple sell-off in a different method (self.sell_captured)
            """
            if hero.take_ap(1):
                if hero.take_money(self.get_fees4captured(), reason="Jail Fees"):
                    renpy.play("content/sfx/sound/world/purchase_1.ogg")
                    self.worker.del_flag("sentence_type")
                    self.worker.del_flag("days_in_jail")
                    if direction == "STinTD":
                        self.remove_prisoner()
                    elif direction == "Blue":
                        if hero.take_money(2000, reason="Blue's Fees"):
                            pytfall.sm.blue_girls[self.worker] = 0
                            self.remove_prisoner(set_location=False)
                        else:
                            hero.add_money(self.get_fees4captured(), reason="Jail Fees")
                            renpy.call_screen('message_screen', "You don't have enough money for upfront payment for Blue's services!")
                else:
                    renpy.call_screen('message_screen', "You don't have enough money!")
            else:
                renpy.call_screen('message_screen', "You don't have enough AP left for this action!")

            if not self.chars_list:
                renpy.hide_screen("slave_shopping")


    class School(BaseBuilding):
        """
        Building that represents the school.
        """

        #"primary": [1,1,1,0,1,1,1,1,1,1,1,1,2,0],
        #"secondary": [0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,2],
        #"tprimary": [1,1,1,0,1,1,1,1,1,1,1,1,2,3],
        #"tsecondary": [0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,2,2],
        #"sprimary": [1,1,0,0,1,1,1,1,1,1,0,1,0,2],
        #"ssecondary": [0,0,0,1,0,1,0,0,1,0,0,0,1,1,1,1,0,0,0,0,1,2],

        def __init__(self, id="-PyTFall Educators-", image="content/schools/school.webp",
                     primary=0, secondary=0, skillPrimary=None, skillSecondary=None,
                     options=None, file=None):
            """
            Creates a new schoool.
            id = The name of the school.
            image = The image for the school.
            primary = The primary stat increase.
            secondary = The secondary stat increase.
            options = The courses available.
            file = The json file this school was loaded from.
            """
            super(School, self).__init__(id=id, name=id)

            self.img = image

            self.primary = primary
            self.secondary = secondary
            self.skill_primary = skillPrimary or primary
            self.skill_secondary = skillSecondary or secondary

            self.fin = Finances(self)
            self.income = 0

            # Dict
            self.all_courses = options

            # List
            self.courses = []

            self.income = 0

            self.events_relay = {
                "runaway": [0, 0], # successful, prevented
                "disobey": [0, 0], # successful, prevented
                "obey": [0, 0], # from training success, random
                "finish": [0, 0] # end of course, no longer eligible
            }

            # For one off events
            self.one_off_events = list()

            # For debugging purposes
            self.file = None

        @property
        def available(self):
            """
            Whether this building is available.
            """
            return True

        def create_course(self):
            """
            Creates a random course from the courses dictionary.
            """
            key = choice(self.all_courses.keys())
            course = deepcopy(self.all_courses[key])

            x = dict()
            for i in course["primary"]:
                if i in PytCharacter.SKILLS: x[i] = self.skill_primary
                else: x[i] = self.primary

            course["primary"] = PytStatChanges(mod=x)

            x = dict()
            for i in course["secondary"]:
                if i in PytCharacter.SKILLS: x[i] = self.skill_secondary
                else: x[i] = self.secondary

            course["secondary"] = PytStatChanges(mod=x)

            course = SchoolLesson(key, **course)

            self.courses.append(course)

        @property
        def is_school(self):
            """
            Whether or not this building is a school.
            """
            return True

        def log_income(self, char, value):
            """
            Logs the schools income.
            char = The character who the income is being spent for.
            value = The amount being spent.
            """
            hero.take_money(value, reason=self.name)
            self.income += value
            char.fin.log_logical_expense(value, "Training")

        def next_day(self):
            """
            Solves the next day notifications for schooling.
            """
            # Logic
            type = "schoolndreport"
            img = im.Scale(self.img, int(config.screen_width*0.6), int(config.screen_height*0.8))
            txt = "%s Report: \n"%self.name
            evtlist = []
            char = None

            girls = [girl for girl in hero.chars if girl.location == self.name]

            if not girls:
                txt += "Excellent courses are available today! Remember our Motto: Education is Gold! \n"
            else:
                txt += choice(["You currently have %d girls training with us! \n" % len(girls),
                               "Excellent courses are available today! Remember our Motto: Education is Gold! \n"])

            # Add courses
            tempval = len(self.courses)
            if len(self.courses) < 10:
                self.create_course()

            if dice(50):
                if len(self.courses) < randint(10, 20):
                    self.create_course()

            if dice(10):
                if len(self.courses) < 30:
                    self.create_course()

            if tempval < len(self.courses):
                txt += "We inform you about fresh courses starting today. Please check in with us if you are interested. \n"

            # Checking if girl has completed the course:
            for course in self.courses:
                for girl in girls:
                    if str(girl) in course.chars:
                        cdays = int(course.duration*.7)

                        if course.chars[str(girl)] >= cdays:
                            if str(girl) in course.complete:
                                pass

                            else:
                                course.complete[str(girl)] = True
                                self.events_relay["finish"][0] += 1

                                # Final increase
                                course.primary(girl, mult=course.get_scaling(girl))
                                course.secondary(girl, mult=course.get_scaling(girl))

                                if dice(20):
                                    for stat in course.primary.mod:
                                        girl.stats.max[stat] += choice([0, 1])

                                txt += "\n\n{color=[lawngreen]}%s has successfully completed %s and got a nice extra bonus to her stats! \n{/color}"%(girl.name, course.action)

            # Day Count
            for course in self.courses:
                course._daysLeft -= 1

            # End courses and remove girls
            for course in self.courses:
                if course.daysLeft() <= 0:
                    for girl in girls:
                        if girl_course_id(girl) == course.id:
                            txt += "Course that %s is attending is at it's end! "%girl.name
                            stop_training(girl)

                    self.courses.remove(course)

            # Event summery
            for i in self.events_relay:
                j, k = self.events_relay[i]
                if i == "obey":
                    if j > 0: txt += "%d %s obeyed their trainers perfectly. \n"%(j, plural("girl", j))
                    if k > 0: txt += "%d %s did extra well because of the facilities and equipment. \n"%(k, plural("girl", k))
                elif i == "disobey":
                    if j > 0: txt += "%d %s disobeyed their trainers without punishment. \n"%(j, plural("girl", j))
                    if k > 0: txt += "%d %s disobeyed their trainers and were punished for it. \n"%(k, plural("girl", k))
                elif i == "runaway":
                    if j > 0: txt += "%d %s ran away from their lessons, wasting their day. \n"%(j, plural("girl", j))
                    if k > 0: txt += "%d %s tried to run away, but were caught and punished. \n"%(k, plural("girl", k))
                elif i == "finish":
                    if j > 0: txt += "%d %s have completed their training. \n"%(j, plural("girl", j))
                    if k > 0: txt += "%d %s are no longer eligible for their training. \n"%(k, plural("girl", k))

                self.events_relay[i][0] = 0
                self.events_relay[i][1] = 0

            # Do one off events
            while self.one_off_events:
                NextDayEvents.append(self.one_off_events.pop())

            evt = NDEvent(type=type, txt=txt, img=img, char=char)
            NextDayEvents.append(evt)


    class TrainingDungeon(UpgradableBuilding, BuildingStats):
        """
        Building that represents the hero's dungeon to train girls in.
        Presently unused...
        """

        NAME = "Training Dungeon"

        def __init__(self, courses):
            """
            Creates a new TrainingDungeon.
            """
            super(TrainingDungeon, self).__init__(id=self.NAME, name=self.NAME, desc="A personal dungeon for training and punishing slaves.",
                                                  price=7500, minrooms=5, maxrooms=50, roomprice=500, upgrade_slots=18)

            self.img = "content/buildings/dungeon.webp"

            self.actions = ["Guard", "Train", "Take Course", "Search"]

            self.fin = Finances(self)
            self.income = 0

            # Dict
            self.all_courses = courses

            # List
            self.courses = [courses[i] for i in courses]

            self.events_relay = {
                "runaway": [0, 0], # successful, prevented
                "disobey": [0, 0], # successful, prevented
                "obey": [0, 0], # from training success, random
                "finish": [0, 0] # end of course, no longer eligible
            }

            self.one_off_events = list()

        @property
        def can_advert(self):
            return False

        @property
        def available(self):
            """
            Whether this building is available. Used in training screen.
            """
            return self in hero.buildings

        def get_girls(self, type=None):
            """
            Override get_girls to include proper trainer support.
            """
            if type == "Training":
                return [girl_training_with(girl) for girl in super(TrainingDungeon, self).get_girls("Course")]
            else:
                return super(TrainingDungeon, self).get_girls(type)

        def get_upkeep(self):
            """
            The upkeep cost of the building.
            """
            pass

        @property
        def is_school(self):
            """
            Whether or not this building is a school. Used in training screen.
            """
            return False

        def log_income(self, char, value):
            """
            Logs the training cost.
            char = The character who the income is being spent for.
            value = The amount being spent.
            """
            hero.take_money(value, reason=self.name)
            self.income += value
            char.fin.log_logical_expense(value, "Training")

        def mod_disobey(self):
            """
            The modifier for disobeying.
            """
            return self.get_upgrade_mod("Punishments") # / len(self.upgrades["Punishments"])

        def mod_exp(self):
            """
            The modifier for experience.
            """
            return self.get_upgrade_mod("Equipment") # / len(self.upgrades["Equipment"])

        def mod_housing(self):
            """
            The modifier for the hero's AP.
            """
            return self.get_upgrade_mod("Housing") # / len(self.upgrades["Housing"])

        def mod_obey(self):
            """
            The modifier for obeying.
            """
            return self.get_upgrade_mod("Rewards") # / len(self.upgrades["Rewards"])

        def mod_runaway(self):
            """
            The modifier for running away.
            """
            return self.get_upgrade_mod("Security") # / len(self.upgrades["Security"])

        def mod_skill(self):
            """
            The modifier for trainer ability.
            """
            return self.get_upgrade_mod("Trainers") # / len(self.upgrades["Trainers"])

        def next_day(self):
            """
            Solves the next day logic for the training girls.
            """
            # Logic
            type = "schoolndreport"
            img = im.Scale(self.img, int(config.screen_width*0.6), int(config.screen_height*0.8))
            txt = "%s Report: \n"%self.name
            evtlist = []
            char = None

            girls = self.get_girls("Course")

            if not girls:
                txt += "Your dungeon is currently going unused, maybe some of your girls require training? \n"
            else:
                txt += "You currently have %d %s training in your dungeon. \n"%(len(girls), plural("girl", len(girls)))

            # Checking if girls have completed their courses
            for girl in girls:
                course = char_is_training(girl)
                trainer = girl_training_with(girl)

                if course.daysLeft(girl) > 0:
                    girl_training_left.set(girl, -1, True) # Decrease
                else:
                    stop_training(girl)
                    self.events_relay["finish"][0] += 1

                    # Final stat increase
                    course.primary(girl, mult=course.get_scaling(girl))
                    course.secondary(girl, mult=course.get_scaling(girl))

                    # Bonus stat increase
                    if dice(20) and course.primary.mod is not None:
                        for stat in course.primary.mod:
                            girl.stats.max[stat] += choice([0, 1])

                    txt += "\n\n{color=[lawngreen]}%s has completed her %s training. \n{/color}"%(girl.name, course.type)

            # Security
            self.security_rating -= len(girls) * (1+self.mod_runaway())
            if self.security_rating < 0: self.security_rating = 0

            security_power = 0
            guards = self.get_girls("Guard")
            for guard in guards: security_power += (guard.attack + guard.defence + guard.magic) / 3

            self.security_rating += int(security_power * ((self.security_presence/10)+1))

            if self.security_rating < 0: self.security_rating = 0
            elif self.security_rating > 1000: self.security_rating = 1000

            txt += "Security Rating is now %d out of 1000, you currently have %d guards on duty with security presence of %d%%. \n\n"% (self.security_rating, len(guards), self.security_presence)

            # Event summery
            for i in self.events_relay:
                j,k = self.events_relay[i]

                if i == "obey":
                    if j > 0: txt += "%d %s obeyed their trainers perfectly. \n"%(j, plural("girl", j))
                    if k > 0: txt += "%d %s did extra well because of the facilities and equipment. \n"%(k, plural("girl", k))
                elif i == "disobey":
                    if j > 0: txt += "%d %s disobeyed their trainers without punishment. \n"%(j, plural("girl", j))
                    if k > 0: txt += "%d %s disobeyed their trainers and were punished for it. \n"%(k, plural("girl", k))
                elif i == "runaway":
                    if j > 0: txt += "%d %s ran away from their lessons, wasting their day. \n"%(j, plural("girl", j))
                    if k > 0: txt += "%d %s tried to run away, but were caught and punished. \n"%(k, plural("girl", k))
                elif i == "finish":
                    if j > 0: txt += "%d %s have completed their training. \n"%(j, plural("girl", j))
                    if k > 0: txt += "%d %s are no longer eligible for their training. \n"%(k, plural("girl", k))

                self.events_relay[i][0] = 0
                self.events_relay[i][1] = 0

            # Do one off events
            while self.one_off_events:
                NextDayEvents.append(self.one_off_events.pop())

            evt = NDEvent()
            evt.type = type
            evt.char = char
            evt.img = img
            evt.txt = txt
            NextDayEvents.append(evt)


    class Building(UpgradableBuilding, AdvertableBuilding, FamousBuilding, BuildingStats):
        """
        The building that represents Business Buildings.
        """
        def __init__(self, *args, **kwargs):
            """
            Creates a new Building.
            # maxrank = The maximum rank this brothel can achieve.
            """
            super(Building, self).__init__(*args, **kwargs)
            BuildingStats.__init__(self)

            self.fin = Finances(self)

            # ND Report
            self.nd_events_report = list()
            self.logged_clients = False

        def next_day(self):
            """
            Solves the next day logic for the Building.
            """
            # Local vars
            type = 'buildingreport'
            img = self.img

            txt = self.nd_events_report

            evtlist = []
            char = None
            tmodrep = 0 # Total of rep changed on next day, girl's mod are not included here.
            tmodfame = 0 # Total of fame, same rules.
            spentcash = 0

            # Applies effects of advertisements:
            if self.can_advert:
                for advert in self.adverts:
                    if advert['active']:
                        if 'fame' in advert:
                            modf = randint(*advert['fame'])
                            self.modfame(modf)
                            tmodfame += modf
                        if 'reputation' in advert:
                            modr = randint(*advert['reputation'])
                            self.modrep(modr)
                            tmodrep += modr

                        spentcash += advert['upkeep']
                        if advert['name'] == 'Celebrity':
                            advert['active'] = False
                            txt.append("A celebrity came into your building, raising it's reputation by %d and fame by %d\n" % (modr, modf))

                txt.append("In total you got a bill of %d Gold in advertising fees, reputation was increased through advertising by %d, fame by %d." % (spentcash, tmodrep, tmodfame))

                if spentcash and not hero.take_money(spentcash, reason="Building Ads"):
                    rep_hit = max(10, spentcash/10)
                    self.modrep(-rep_hit)
                    txt.append("{color=[red]}And yet, you did not have enough money to pay your advertisers! They took it out on you by promoting %s as a shitty dump...{/color}" % self.name)
                    self.flag_red = True

                self.fin.log_expense(spentcash, "Ads")

            charmod = self.nd_log_stats()

            evt = NDEvent()
            evt.type = type
            evt.charmod = charmod
            evt.red_flag = self.flag_red
            evt.loc = self
            evt.char = char
            evt.img = img
            evt.txt = txt
            NextDayEvents.append(evt)

            self.nd_events_report = list()
            self.logged_clients = False

        def nd_log_income(self):
            """
            Log the next day income for this building.
            """
            self.fin.next_day()
