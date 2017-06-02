init -10 python:
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

        AP check is optional here, with True as default, there are cases where char might still have job points even though AP is 0. TODO: report about issues with health/vitality/etc somewhere in the next day report
        """
        if c.health < c.get_max("health")*.25:
            if log:
                log.append("%s is injured and in need of medical attention! "%c.name)
            # self.img = c.show("profile", "sad", resize=(740, 685))
            if c.autocontrol['Rest']:
                c.previousaction = c.action
                c.action = AutoRest()
                if log:
                    log.append("And going to take few days off to heal. ")
            return False
        if c.vitality <= c.get_max("vitality")*.10:
            if log:
                log.append("%s is too tired! "%c.name)
            # self.img = c.show("profile", "sad", resize=(740, 685))
            if c.autocontrol['Rest']:
                c.previousaction = c.action
                c.action = AutoRest()
                if log:
                    log.append("And going to take few days off to recover. ")
            return False
        if c.effects['Food Poisoning']['active']:
            if log:
                log.append("%s is suffering from Food Poisoning! "%c.name)
            # self.img = c.show("profile", "sad", resize=(740, 685))
            if c.autocontrol['Rest']:
                c.previousaction = c.action
                c.action = AutoRest()
                if log:
                    log.append("And going to take few days off to recover. ")
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
