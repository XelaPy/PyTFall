init -10 python:
    def convert_ap_to_jp(char):
        # Do not convert AP when Char is in school.
        char.jobpoints += char.AP*100 # += is safer here.
        char.AP = 0

    def payout(job, effectiveness, difficulty, building, business, worker, clients, log):
        """
        Calculates payout for jobs based of effectiveness and other modifications.
        Writes to log accordingly.
        """
        earned = pytfall.economy.get_clients_pay(job, difficulty)

        if isinstance(clients, (set, list, tuple)):
            if len(clients) > 1:
                plural = True
                client_name = "clients"
                earned *= len(clients) # Make sure we adjust the payout to the actual number of clients served.
            else:
                plural = False
                client_name = "client"
        else:
            plural = False
            client_name = clients.name

        me = building.manager_effectiveness
        if effectiveness <= 33: # Worker sucked so much, client just doesn't pay.
            if plural:
                temp = "Clients leave the {} refusing to pay for the inadequate service {} provided.".format(
                                business.name, worker.name)
            else:
                temp = "{} leaves the {} refusing to pay for the inadequate service {} provided.".format(
                                set_font_color(client_name.capitalize(), "beige"), business.name, worker.name)
            log.append(temp)
            earned = 0
        elif effectiveness <= 90: # Worker sucked but situation may be salvageable by Manager.
            if plural:
                temp = "Due to inadequate service provided by {} clients refuse to pay the full price.".format(worker.name)
            else:
                temp = "Due to inadequate service provided by {} client refuses to pay the full price.".format(worker.name)
            log.append(temp)
            if me >= 90 and building.help_ineffective_workers and building.manager.jobpoints >= 1:
                temp = "Your skilled manager {} intervened and straitened things out.".format(building.manager.name)
                building.mlog.append("\n{} helped to calm a client down after {}'s poor performance and salvaged part of the payment!".format(
                                                    building.manager.name, worker.name))
                building.manager.jobpoints -= 1

                if me >= 150 and dice(85):
                    if plural:
                        temp += " Client were so pleased for the attention and ended up paying full price."
                    else:
                        temp += " Client was so pleased for the attention and ended up paying full price."
                    log.append(temp)
                    earned *= .75
                elif dice(75):
                    if plural:
                        temp += " Clients agree to pay three quarters of the price."
                    else:
                        temp += " Client agreed to pay three quarters of the price."
                    log.append(temp)
                    earned *= .75
                else:
                    earned *= .6
                    temp = " You will get 60%..."
                    log.append(temp)
            else:
                earned *= .5
                temp = " You will get half..."
                log.append(temp)
        elif effectiveness <= 150:
            if plural:
                temp = "Clients are very happy with {} service and pay the full price.".format(worker.name)
            else:
                temp = "Client is very happy with {} service and pays the full price.".format(worker.name)
            log.append(temp)
        else:
            if plural:
                temp = "Clients are ecstatic! {} service was beyond any expectations. +20% to payout!".format(worker.name)
            else:
                temp = "Client is ecstatic! {} service was beyond any expectations. +20% to payout!".format(worker.name)
            log.append(temp)
            earned *= 1.2

        # Passive manager effect:
        if me >= 120 and dice(50):
            if plural:
                temp = "Manager paid some extra attention to clients. +20% to payout!"
            else:
                temp = "Manager paid some extra attention to the client. +20% to payout!"
            log.append(temp)
            earned *= 1.2
            building.mlog.append("\n"+temp)

        earned = round_int(earned)
        if earned:
            temp = "You've earned {} Gold!".format(earned)
            log.append(temp)
            log.earned += earned

        return earned

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

    def can_do_work(c, check_ap=True, log=None):
        """Checks whether the character is injured/tired/has AP and sets her/him to auto rest.

        AP check is optional and if True, also checks for jobpoints.
        """
        # We do not want girls in school to AutoRest,
        # Idea is that the school is taking care of this.
        if isinstance(c.action, SchoolCourse):
            return True

        if c.health < c.get_max("health")*.25:
            if log:
                log.append("%s is injured and in need of medical attention! "%c.name)
            # self.img = c.show("profile", "sad", resize=(740, 685))
            if c.autocontrol['Rest']:
                c.previousaction = c.action
                c.action = simple_jobs["AutoRest"]
                if log:
                    log.append("And going to take few days off to heal. ")
            return False
        if c.vitality <= c.get_max("vitality")*.2:
            if log:
                log.append("%s is too tired! "%c.name)
            # self.img = c.show("profile", "sad", resize=(740, 685))
            if c.autocontrol['Rest']:
                c.previousaction = c.action
                c.action = simple_jobs["AutoRest"]
                if log:
                    log.append("And going to take few days off to recover. ")
            return False
        if "Exhausted" in c.effects:
            if log:
                log.append("%s is exhausted! " % c.name)
            # self.img = c.show("profile", "sad", resize=(740, 685))
            if c.autocontrol['Rest']:
                c.previousaction = c.action
                c.action = simple_jobs["AutoRest"]
                if log:
                    log.append("And needs a day to recover. ")
            return False
        if 'Food Poisoning' in c.effects:
            if log:
                log.append("%s is suffering from Food Poisoning! "%c.name)
            # self.img = c.show("profile", "sad", resize=(740, 685))
            if c.autocontrol['Rest']:
                c.previousaction = c.action
                c.action = simple_jobs["AutoRest"]
                if log:
                    log.append("And going to take few days off to recover. ")
        if check_ap:
            if c.AP <= 0 and c.jobpoints <= 0:
                return False

        return True

    def slave_siw_check(c): # slaves-SIWs allow more than other characters
        if c.status == "slave" and ("SIW" in c.gen_occs) and c.disposition >= -150:
            return True
        else:
            return False

    def check_submissivity(c):
        """Here we determine how submissive the character is, thus if she's willing to do something she doesn't want to, or for example take the initiative in certain cases.
        """
        if not c.get_max("character"):
            return -1

        mult = 1.0*c.character/c.get_max("character") # the idea is based on the character stat, we check how close is she to max possible character at her level
        if "Impersonal" in c.traits: # and traits, they can make mult more or less, so for example even low character tsundere might be more stubborn than high character dandere
            mult -= .1
        elif "Imouto" in c.traits:
            mult -= .05
        elif "Dandere" in c.traits:
            mult -= .15
        elif "Tsundere" in c.traits:
            mult += .2
        elif "Kuudere" in c.traits:
            mult += .15
        elif "Kamidere" in c.traits:
            mult += .23
        elif "Bokukko" in c.traits:
            mult += .2
        elif "Ane" in c.traits:
            mult += .05
        elif "Yandere" in c.traits: # in case of yandere disposition is everything
            if c.disposition <= 500:
                mult += .25
            else:
                mult -= .25
        if "Courageous" in c.traits:
            mult += .05
        elif "Coward" in c.traits:
            mult -= .05
        if "Shy" in c.traits:
            mult -= .05
        if "Aggressive" in c.traits:
            mult += .05
        if "Natural Leader" in c.traits:
            mult += .05
        elif "Natural Follower" in c.traits:
            mult -= .05

        if c.status == "slave":
            mult -= .1

        if mult < .35: # there are 3 levels of submissiveness, we return -1, 0 or 1, it's very simple to use in further calculations
            return -1
        elif mult > .67:
            return 1
        else:
            return 0
