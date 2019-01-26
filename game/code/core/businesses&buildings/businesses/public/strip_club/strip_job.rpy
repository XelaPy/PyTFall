init -5 python:
    ####################### Strip Job  ############################
    class StripJob(Job):
        """
        Class for the solving of stripping logic.
        """
        def __init__(self):
            super(StripJob, self).__init__()
            self.id = "Striptease Job"
            self.type = "SIW"

            self.per_client_payout = 8

            # Traits/Job-types associated with this job:
            self.occupations = ["SIW"] # General Strings likes SIW, Combatant, Server...
            self.occupation_traits = [traits["Stripper"]] # Corresponding traits...
            self.aeq_purpose = 'Striptease'

            self.base_skills = {"strip": 100, "dancing": 40, "sex": 5}
            self.base_stats = {"charisma": 70, "agility": 30}

            self.desc = "Strippers dance half-naked on the stage, keeping customers hard and ready to hire more whores"

            self.allowed_genders = ["female"]

        def traits_and_effects_effectiveness_mod(self, worker, log):
            """Affects worker's effectiveness during one turn. Should be added to effectiveness calculated by the function below.
               Calculates only once per turn, in the very beginning.
            """
            # Special check to prevent crashing
            if log is None:
                log = []

            effectiveness = 0
             # effects always work
            if 'Food Poisoning' in worker.effects:
                log.append("%s suffers from Food Poisoning, and is very far from her top shape." % worker.name)
                effectiveness -= 50
            elif 'Exhausted' in worker.effects:
                log.append("%s is exhausted and is in need of some rest." % worker.name)
                effectiveness -= 75
            elif 'Down with Cold' in worker.effects:
                log.append("%s is not feeling well due to colds..." % worker.name)
                effectiveness -= 15
            elif 'Horny' in worker.effects:
                log.append("%s is horny. A positive mindset for her job!" % worker.name)
                effectiveness += 10
            elif 'Drunk' in worker.effects:
                log.append("%s is drunk, which affects her coordination. Not the best thing when you need to dance around pole." % worker.name)
                effectiveness -= 20
            elif 'Revealing Clothes' in worker.effects:
                log.append("Her revealing clothes are perfect for her job!")
                effectiveness += 40

            if locked_dice(65): # traits don't always work, even with high amount of traits there are normal days when performance is not affected
                # This cannot work comparing strings to trait objects:
                traits = list(i.id for i in worker.traits if i.id in ["Abnormally Large Boobs",
                        "Small Boobs", "Scars", "Not Human", "Flat Ass", "Exhibitionist",
                        "Sexy Air", "Clumsy", "Flexible", "Psychic", "Manly", "Artificial Body",
                        "Lesbian", "Shy", "Aggressive", "Big Boobs", "Great Arse", "Long Legs",
                        "Strange Eyes", "Natural Follower"])
                if traits:
                    trait = choice(traits)
                else:
                    return effectiveness

                if trait == "Abnormally Large Boobs":
                    if dice(65):
                        log.append("%s makes a big splash today playing with her massive boobs to customers delight." % worker.name)
                        effectiveness += 50
                    else:
                        log.append("Handling massive boobs on daily basis is a tiresome job, even more so when %s has to dance at the stage." % worker.name)
                        worker.logws('vitality', -randint(5, 10))
                elif trait == "Small Boobs":
                    if not "Lolita" in worker.traits:
                        log.append("%s tries her best, but most customers are not very impressed by her modest forms." % worker.name)
                        effectiveness -= 25
                    else:
                        log.append("%s may not have many fans due to her forms, but there are always lolicons among customers." % worker.name)
                        effectiveness += 20
                elif trait == "Scars":
                    log.append("Poor %s does her best, but many customers turn away when they see her scars..." % worker.name)
                    effectiveness -= 35
                elif trait == "Not Human":
                    log.append("%s's inhuman features attract more attention than usual, and that is never a bad thing in striptease." % worker.name)
                    effectiveness += 15
                elif trait == "Flat Ass":
                    log.append("%s tries her best, but skill alone cannot replace a fine ass." % worker.name)
                    effectiveness -= 15
                elif trait == "Exhibitionist":
                    log.append("%s is at least as aroused as the customers and isn't afraid to show it." % worker.name)
                    effectiveness += 50
                elif trait == "Sexy Air":
                    log.append("%s's sexiness attracts the views all day. She has an air about her that makes her a natural at stripping." % worker.name)
                    effectiveness += 10
                elif trait == "Clumsy":
                    log.append("Sadly, %s ruins the show when she trips and falls from the stage. At least customers had a good laugh." % worker.name)
                    effectiveness -= 25
                elif trait == "Flexible":
                    log.append("%s makes a good use of her flexibility, bending around the pole in impossible ways." % worker.name)
                    effectiveness += 20
                elif trait == "Psychic":
                    log.append("Every customer wants different things, which is quite confusing for psychics like %s when so many people watching her." % worker.name)
                    effectiveness -= 20
                elif trait == "Manly":
                    log.append("It looks like %s is a bit too muscular for this job, intimidating some customers." % worker.name)
                    effectiveness -= 25
                elif trait == "Artificial Body":
                    log.append("Sadly, customers figured out that her body is a construct and booed %s off the stage." % worker.name)
                    effectiveness -= 50
                elif trait == "Lesbian":
                    log.append("%s is somewhat disgusted by the idea of letting so many MEN see her naked." % worker.name)
                    effectiveness -= 30
                elif trait == "Shy":
                    log.append("%s is too nervous and stiff, making customers bored." % worker.name)
                    effectiveness -= 30
                elif trait == "Aggressive":
                    log.append("%s slaps customers who get too close, ruining the mood." % worker.name)
                    effectiveness -= 20
                elif trait == "Big Boobs":
                    log.append("The customers' eyes are glued to her tits all the time.")
                    effectiveness += 15
                elif trait == "Great Arse":
                    log.append("%s shakes her sexy ass to great effect. It's like her curves were made for stripping." % worker.name)
                    effectiveness += 15
                elif trait == "Long Legs":
                    log.append("Today the customers go nuts for those sexy legs of hers.")
                    effectiveness += 15
                elif trait == "Strange Eyes":
                    log.append("Her exotic eyes hold the customers in a trance.")
                    effectiveness += 10
                elif trait == "Natural Follower":
                    log.append("%s is quick to figure out how a crowd likes her to move, making a great show." % worker.name)
                    effectiveness += 20
            return effectiveness

        def calculate_disposition_level(self, worker):
            """
            calculating the needed level of disposition;
            since it's whoring we talking about, values are really close to max,
            or even higher than max in some cases, making it impossible
            """
            sub = check_submissivity(worker)
            if "Shy" in worker.traits:
                disposition = 700 + 50 * sub
            else:
                disposition = 600 + 50 * sub
            if cgochar(worker, "SIW"):
                disposition -= 500
            if "Exhibitionist" in worker.traits:
                disposition -= 200
            if "Nymphomaniac" in worker.traits:
                disposition -= 50
            elif "Frigid" in worker.traits:
                disposition += 50
            if check_lovers(hero, worker):
                disposition -= 50
            elif check_friends(hero, worker):
                disposition -= 25
            if "Natural Follower" in worker.traits:
                disposition -= 50
            elif "Natural Leader" in worker.traits:
                disposition += 50
            return disposition

        def settle_workers_disposition(self, worker, log):
            """
            Handles penalties in case of wrong job

            Note:
            "jobs_stripintro" flag is unused.
            """
            # Formerly check_occupation
            if not("Stripper" in worker.traits) and worker.disposition < self.calculate_disposition_level(worker):
                sub = check_submissivity(worker)
                if worker.status != 'slave':
                    if sub < 0:
                        if dice(15):
                            log.logws('character', 1)
                        worker.set_flag("jobs_stripintro", "%s is not very happy with her current job as a stripper, but she will get the job done." % worker.name)
                    elif sub == 0:
                        if dice(25):
                            log.logws('character', 1)
                        worker.set_flag("jobs_stripintro", "%s shows her goods to customers, but she would prefer to do something else." % worker.nickname)
                    else:
                        if dice(35):
                            log.logws('character', 1)
                        worker.set_flag("jobs_stripintro", "%s makes it clear that she wants another job before going to the stage." % worker.name)
                    worker.logws("joy", -randint(1, 10))
                    worker.logws("disposition", -randint(10, 15))
                    worker.logws('vitality', -randint(5, 10))
                else:
                    sub = check_submissivity(worker)
                    if sub< 0:
                        if worker.disposition < self.calculate_disposition_level(worker):
                            log.append("%s is a slave so no one really cares but, being forced to work as a stripper, she's quite upset." % worker.name)
                        else:
                            log.append("%s will do as she is told, but doesn't mean that she'll be happy about showing her body to strangers." % worker.name)
                        if dice(25):
                            log.logws('character', 1)
                    elif sub == 0:
                        if worker.disposition < self.calculate_disposition_level(worker):
                            log.append("%s will do as you command, but she will hate every second of her stripper shift..." % worker.name)
                        else:
                            log.append("%s was very displeased by her order to work as a stripper, but didn't dare to refuse." % worker.name)
                        if dice(35):
                            log.logws('character', 1)
                    else:
                        if worker.disposition < self.calculate_disposition_level(worker):
                            log.append("%s was very displeased by her order to work as a stripper, and makes it clear for everyone before going to the stage." % worker.name)
                        else:
                            log.append("%s will do as you command and work as a stripper, but not without a lot of grumbling and complaining." % worker.name)
                        if dice(45):
                            log.logws('character', 1)

                    if worker.disposition < self.calculate_disposition_level(worker):
                        worker.logws("joy", -randint(5, 10))
                        worker.logws("disposition", -randint(15, 30))
                        worker.logws('vitality', -randint(10, 15))
                    else:
                        worker.logws("joy", -randint(2, 4))
                        worker.logws('vitality', -randint(2, 6))
            else:
                worker.set_flag("jobs_stripintro",
                    choice(["%s is doing her shift as a stripper." % worker.name,
                    "%s shows her goods to clients." % worker.fullname,
                    "%s entertains customers with her body at the stage." % worker.nickname]))

            return True

        def work_strip_club(self, worker, clients, effectiveness, log):
            len_clients = len(clients)
            building = log.loc

            strip = self.normalize_required_skill(worker, "strip", effectiveness, building.tier)
            dancing = self.normalize_required_skill(worker, "dancing", effectiveness, building.tier)
            skill = (strip*1.3 + dancing)/2
            charisma = self.normalize_required_stat(worker, "charisma", effectiveness, building.tier)

            if charisma >= 170:
                log.append("%s supernal loveliness instantly captivated audiences. " % worker.name)
                log.logws("joy", 2)
            elif charisma >= 150:
                log.append("The attention of customers was entirely focused on %s thanks to her prettiness. " % worker.name)
                log.logws("joy", 1)
            elif charisma >= 120:
                log.append("%s enchanted customers with her stunning beauty. " % worker.name)
            elif charisma >= 100:
                log.append("Customers were delighted with %s beauty. " % worker.name)
            elif charisma >= 75:
                log.append("%s good looks was pleasing to audiences. " % worker.name)
            elif charisma >= 50:
                log.append("%s did her best to make customers like her, but her beauty could definitely be enhanced. " % worker.name)
            else:
                log.logws("joy", -2)
                log.append("Customers clearly were unimpressed by %s looks, to say at least. Such a cold reception was not encouraging for the poor girl at all..." % worker.name)

            # Award EXP:
            if effectiveness >= 90:
                log.logws("exp", exp_reward(worker, building.tier))
            else:
                log.logws("exp", exp_reward(worker, building.tier, final_mod=.5))

            log.append("\n")
            if skill >= 170:
                log.append("She gave an amazing performance, her sexy and elegant moves forced a few customers to come right away to their own embarrassment.")
                # log.logws("exp", randint(250, 500))
                log.logloc("reputation", choice([0, 1]))
                log.logws("joy", 3)
            elif skill >= 150:
                log.append("She gave a performance worthy of kings and queens as the whole hall was cheering for her.")
                # log.logws("exp", randint(100, 200))
                log.logloc("reputation", choice([0, 0, 1]))
                log.logws("joy", 2)
            elif skill >= 130:
                log.append("She lost all of her clothing piece by piece as she gracefully danced on the floor, the whole hall was cheering for her.")
                # log.logws("exp", randint(50, 120))
                log.logws("joy", 2)
            elif skill >= 100:
                log.append("She lost all of her clothing piece by piece as she danced on the floor, some mildly drunk clients cheered for her.")
                # log.logws("exp", randint(40, 75))
                log.logws("joy", 1)
            elif skill >= 75:
                log.append("She danced to the best of her ability but her skills could definitely be improved.")
                # log.logws("exp", randint(35, 45))
            elif skill >= 50:
                log.append("She barely knew what she was doing. Her performance can hardly be called a striptease, but at least she showed enough skin to arouse some men and women in the club.")
                # log.logws("exp", randint(20, 35))
            else:
                # log.logws("exp", randint(15, 25))
                if worker.charisma >= 200:
                    log.append("She tripped several times while trying to undress herself as she 'stripdanced' on the floor. Still, she was pretty enough to arouse some men and women in the club.")
                else:
                    log.append("She certainly did not shine as she clumsily 'danced' on the floor. Neither her looks nor her skill could save the performance...")
                    log.append("\n")

            # Take care of stats mods
            if dice(9):
                log.logws("agility", 1)
                learned = True
            if dice(20):
                log.logws("charisma", 1)
                learned = True
            if dice(15):
                log.logws("dancing", 1)
                learned = True
            if dice(35 if "Exhibitionist" in worker.traits else 25):
                log.logws("strip", 1)
                learned = True

            log.logws('vitality', round_int(len_clients*-.5))

            if "learned" in locals():
                log.append("\n%s feels like she learned something! \n"%worker.name)
                log.logws("joy", 1)

            excluded = ["sad", "angry", "in pain"]
            kwargs = dict(exclude=excluded, resize=ND_IMAGE_SIZE, type="reduce", add_mood=False)
            tags = (["stripping", "stage"], ["stripping", "simple bg"], ["stripping", "no bg"])

            result = get_simple_act(worker, tags, excluded)
            if result:
                log.img = worker.show(*result, **kwargs)
            else:
                log.img = worker.show("stripping", "indoors", **kwargs)
