init -5 python:
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

            self.desc = "No one can work without taking a break sometimes. Rest restores health, vitality and mp and removes some negative effects."

        def __call__(self, char):
            loc = char.home
            log = NDEvent(job=self, char=char, loc=loc)
            self.rest(char, loc, log)
            self.after_rest(char, log)
            log.after_job()
            NextDayEvents.append(log)

        def rest(self, worker, loc, log):
            """Rests the worker.
            """
            worker.disable_effect('Exhausted')  # rest immediately disables the effect and removes its counter

            # at first we set excluded tags
            if (worker.disposition >= 500) or ("Exhibitionist" in worker.traits) or check_lovers(worker, hero):
                kwargs = dict(exclude=["dungeon", "angry", "in pain", "after sex", "group", "normalsex", "bdsm"], add_mood=False) # with not too low disposition nude pics become available during rest
            else:
                kwargs = dict(exclude=["dungeon", "nude", "angry", "in pain", "after sex", "group", "normalsex", "bdsm"], add_mood=False)

            # if vitality is really low, they try to sleep, assuming there is a sleeping picture
            if worker.vitality < worker.get_max("vitality")*0.2 and worker.has_image("sleeping", **kwargs):
                log.img = worker.show("sleeping", resize=ND_IMAGE_SIZE, **kwargs)
                log.append("{} is too tired to do anything but sleep at her free time.".format(worker.name))
            else:
            # otherwise we build a list of usable tags
                available = list()

                if worker.has_image("sleeping", **kwargs):
                    available.append("sleeping")
                if worker.has_image("reading", **kwargs):
                    available.append("reading")
                if worker.vitality >= worker.get_max("vitality")*0.3: # not too tired for more active rest
                    if worker.has_image("shopping", **kwargs) and (worker.gold >= 200): # eventually there should be a real existing event about going to shop and buy a random item there for gold. after all we do have an algorithm for that. but atm it might be broken, so...
                        available.append("shopping")
                    if "Nymphomaniac" in worker.traits or worker.effects['Horny']['active']:
                        if worker.has_image("masturbation", **kwargs):
                            available.append("masturbation")
                if worker.vitality >= worker.get_max("vitality")*0.5: # not too tired for sport stuff
                    if worker.has_image("sport", **kwargs):
                        available.append("sport")
                    if worker.has_image("exercising", **kwargs):
                        available.append("exercising")
                if worker.has_image("eating", **kwargs):
                    available.append("eating")
                if worker.has_image("bathing", **kwargs):
                    available.append("bathing")
                if worker.has_image("rest", **kwargs):
                    available.append("rest")

                if not(available):
                    available = ["profile"] # no rest at all? c'mon...

                log.img = worker.show(choice(available), resize=ND_IMAGE_SIZE, **kwargs)
                image_tags = log.img.get_image_tags()
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
                                                 "{} is relieving her sexual tension at the free time.".format(worker.name)]))
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

            if not log.img:
                log.img = worker.show("rest", resize=ND_IMAGE_SIZE)

            # Resting effects (Must be calculated over AP so not to allow anything going to waste, however AP themselves cannot restore vitality):

            if worker.effects['Drowsy']['active']:
                log.logws('vitality', worker.baseAP*2)
            else:
                log.logws('vitality', worker.baseAP*5)

            ap_range = worker.AP + round_int(worker.jobpoints/100.0)
            for i in range(ap_range): # every left AP gives additional health, mp and joy
                value = round_int(worker.get_max("health")*.1) or 1
                log.logws('health', value)
                value = round_int(worker.get_max("mp")*.1) or 1
                log.logws('mp', value)
                log.logws('joy', randint(1, 2))

                if worker.effects['Drowsy']['active']:
                    log.logws('vitality', 12)
                else:
                    log.logws('vitality', 8)

                worker.AP -= 1
                worker.jobpoints -= 100

                if self.is_rested(worker):
                    break

        def is_rested(self, worker):
            c0 = worker.vitality >= worker.get_max("vitality")*.95
            c1 = worker.health >= worker.get_max('health')*.95
            c2 = not worker.effects['Food Poisoning']['active']

            if all([c0, c1, c2]):
                return True
            else:
                return False

        def after_rest(self, worker, log):
            # Must check for is_rested first always.
            if self.is_rested(worker):
                log.append("\n\nShe is both well rested and healthy so at this point this is simply called: {color=[red]}slacking off :){/color}")


    class AutoRest(Rest):
        """Same as Rest but game will try to reset character to it's previous job."""
        def __init__(self):
            super(AutoRest, self).__init__()
            self.id = "AutoRest"
            self.desc = "Autorest is a type of rest which automatically return character to previous job after resting is no longer needed."

        def after_rest(self, worker, log):
            if self.is_rested(worker):
                worker.action = action = worker.previousaction
                worker.previousaction = ''

                if action:
                    log.append("\n\n{} is now both well rested and goes back to work as {}!".format(worker.name, action))
                else:
                    log.append("\n\n{} is now both well rested and healthy!".format(worker.name))

                aeq_purpose = getattr(action, "aeq_purpose", "")
                if worker.autoequip and aeq_purpose:
                    if worker.last_known_aeq_purpose != aeq_purpose:
                        worker.equip_for(aeq_purpose)
