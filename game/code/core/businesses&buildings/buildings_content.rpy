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

        def __contains__(self, char):
            return char in self.chars_list

        def add_prisoner(self, char, flag=None):
            """Adds a char to the jail.

            char: Character to throw into Jail
            flag: Sentence type (reason to put in Jail)
            """
            if char not in self:
                hero.remove_from_teams(char)
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

        # Deals with girls captured during SE:
        def auto_sell_captured(self, char):
            # Flat price of 1500 Gold - the fees:
            """
            Sells off captured char from the jail.
            """
            fee = 1500 - self.get_fees4captured(girl)
            if fee > 0:
                hero.add_money(fee, "Slave Purchase")
                self.remove_prisoner(char)
                char.location = pytfall.sm
                char.home = pytfall.sm

            return fee

        def next_day(self):
            reports = []
            for i in self.chars_list:
                i.up_counter("days_in_jail")
                if i.flag("sentence_type") == "SE_capture":
                    if i.status == "slave" and i.flag("days_in_jail") >= randint(15, 20):
                        fee = self.auto_sell_captured(i)
                        if dice(45):
                            temp = "Slave {} captured at badlands was sold off to the slave market and is now available for purchase!".format(i.name)
                            if fee > 0:
                                temp += " Guilds owner was compensated with a small reward of {color=[gold]}%d Gold{/color}." % fee
                        else:
                            temp = "Captured slave {} was sent off to the Slave Market!".format(i.name)
                        reports.append(temp)
                    elif i.status == "free" and i.flag("days_in_jail") >= randint(10, 15):
                        if dice(45):
                            temp = "Identity and status of {} captured in badlands was confirmed by the efficient staff of our city prison!".format(i.name)
                            temp += " She was released after spending a short {} days in custody of our jailers.".format(i.flag("days_in_jail"))
                        else:
                            temp = "{} was released from jail after her identity was established!".format(i.name)
                        self.remove_prisoner(i)
                        reports.append(temp)

            if reports:
                gazette.jail.extend(reports)

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

            locmod = self.nd_log_stats()
            evt = NDEvent(locmod=locmod, type=type,
                          red_flag=self.flag_red, loc=self, char=char,
                          img=img, txt=txt)
            NEXT_DAY_EVENTS.append(evt)

            self.nd_events_report = list()
            self.logged_clients = False

        def nd_log_income(self):
            """
            Log the next day income for this building.
            """
            self.fin.next_day()
