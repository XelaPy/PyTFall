init -9 python:
    #################################################################
    # UNIQUE BUILDING CLASSES
    # The classes for actual buildings with the customizations they require.
    #
    class CityJail(HabitableLocation, CharsMarketBase):
        """
        The jail where escaped slaves can turn up. May do other things later.
        """
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

        def remove_prisoner(self, char, set_location=True):
            """
            Returns an actor to the player.
            char = The char to return.
            """
            if char in self:
                char.del_flag("sentence_type")
                char.del_flag("days_in_jail")
                self.chars_list.remove(char)

                self.set_focus()

                if set_location:
                    if char.status == "slave":
                        char.home = locations["Streets"]
                    else:
                        char.home = locations["City Apartments"]
                    char.action = char.workplace = None

        def set_girl(self, char):
            """
            Sets the girl to be the index for the slavemarket.
            girl = The girl to set.
            """
            if self.chars_list and girl in self.chars_list:
                self.focused = char
                self.index = self.chars_list.index(self.focused)

        # Deals with girls captured during SE:
        def sell_captured(self, girl=None, auto=False):
            # Flat price of 1500 Gold - the fees:
            """
            Sells off captured girl from the jail.
            auto: Auto Selloff during next day.
            """
            if not girl:
                girl = self.focused

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
                        # pytfall.temp_text.append("Jail keepers sold off: {color=[red]}%s{/color}!" % i.name)
                    if i.flag("days_in_jail") > 20:
                        # Auto-Selloff in case of 20+ days:
                        self.sell_captured(auto=True)
                        # pytfall.temp_text.append("Jail keepers sold off: {color=[red]}%s{/color}!" % i.name)

        def get_fees4captured(self, char=None):
            # 200 for registration with city hall + 30 per day for "rent"
            if not char:
                char = self.focused
            return 200 + char.flag("days_in_jail") * 30


    class Building(UpgradableBuilding, AdvertableBuilding, FamousBuilding):
        """
        The building that represents Business Buildings.
        """
        def __init__(self, *args, **kwargs):
            """
            Creates a new Building.
            # maxrank = The maximum rank this brothel can achieve.
            """
            super(Building, self).__init__(*args, **kwargs)

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

                self.fin.log_logical_expense(spentcash, "Ads")

            charmod = self.nd_log_stats()

            evt = NDEvent()
            evt.type = type
            evt.charmod = charmod
            evt.red_flag = self.flag_red
            evt.loc = self
            evt.char = char
            evt.img = img
            evt.txt = txt
            NEXT_DAY_EVENTS.append(evt)

            self.nd_events_report = list()
            self.logged_clients = False

        def nd_log_income(self):
            """
            Log the next day income for this building.
            """
            self.fin.next_day()
