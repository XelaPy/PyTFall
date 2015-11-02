init -9 python:
    """
    # Alex Notes (Code Implemented by Thewlis):
    PytWhoringManager: Building a advanced dictionary:
    male: {male.client.act: PytWhoring Instances}
    female: {female.client.act: PytWhoring Instances}
    with custom special methods
    
    PytWhoring usually contains ceveral PytWhoringVariant()
    
    PytWhoringCase() Builds/Solves the actual data for the job event.
    
    ====
    # Alex: I've decided to fall back to old setup until we figure out the job. This seems too difficut to advance and upgrade, especially for content creators who are not versed in Python.
    Such structures should be avoided in the future (in favor of plain liniar code) if only for sake of modders who may want to freely expand on these jobs.
    Complex Python structures should be used to simplefy addition/expansion of content and never to complicate it.
    - If someone wanted to add client info to strings, extra interpolation code is required.
    - If someone wanted to check effects, flags or any other attribute of character/client, significant modifications to the code are required.
    - Female/Male acts can also have the same name (especially under the new, changed system).
    - Syntax for adding new content is also very confusing for anyone who is not well versed in python.
    
    ***We may fall back to this setup after jobs are more mature and we know whats what but before version 1.0, this is too much! :)
    ====
    """
    
    class PytWhoringManager(_object):
        """
        Class (Custom Container) that holds the whoring acts in male/female dicts (instances of PytWhoring or PytWhoringVariant) and allows global access to both.
        """
        def __init__(self):
            """
            Creates a new PytWhoringManager.
            """
            self.male = dict()
            self.female = dict()
        
        def __contains__(self, act):
            """
            Whether this manager contains an act.
            """
            if isinstance(act, PytWhoring): act = act.act
            return act in self.female or act in self.male
        
        def __getitem__(self, act):
            """
            Returns an act from this manager.
            """
            if act in self.male: return self.male[act]
            elif act in self.female: return self.female[act]
            else:
                raise IndexError, "No such act %s"%act
        
        def __iter__(self):
            """
            Iterates over the contents.
            """
            for a in self.male:
                yield a
            
            for a in self.female:
                yield a
        
        def __len__(self):
            """
            The length of the manager.
            """
            return len(self.male) + len(self.female)
        
        def __reversed__(self):
            """
            Iterates over the contents backwards.
            """
            for a in reversed(self.female):
                yield a
            
            for a in reversed(self.male):
                yield a
        
        def add(self, act, female=False):
            """
            Adds an act to this manager.
            act = The PytWhoring to add.
            female = Whether the act is for females.
            """
            if female: self.female[act.act] = act
            else: self.male[act.act] = act
        
        def items(self):
            """
            Returns a list of (name, act) pairs.
            """
            return [i for i in self.iteritems()]
        
        def iterkeys(self):
            """
            Iterates over the act names.
            """
            for i in iter(self):
                yield i
        
        def iteritems(self):
            """
            Iterates over the (name, act) pairs.
            """
            for a in self.male:
                yield (a, self.male[a])
            
            for a in self.female:
                yield (a, self.female[a])
        
        def itervalues(self):
            """
            Iterates over the acts.
            """
            for a in self.male:
                yield self.male[a]
            
            for a in self.female:
                yield self.female[a]
        
        def keys(self):
            """
            Returns a list of the act names.
            """
            return [i for i in self.iterkeys()]
        
        def remove(self, act):
            """
            Removes an act from this manager.
            act = The act to remove.
            """
            if isinstance(act, PytWhoring): act = act.act
            if act in self.female: self.female.remove(act)
            if act in self.male: self.male.remove(act)
        
        def values(self):
            """
            Returns a list of acts.
            """
            return [i for i in self.itervalues()]
        
    
    class PytWhoring(_object):
        """
        Class that holds the content for a sex act.
        """
        
        SKILL_TEXT = dict(
            perfect="The client was at your girls mercy. Her beauty enchanting, she playfully took him into her embrace and made him forget about the rest of the world until they were finished. \n",
            great="Your girl performed wonderfully with her breathtaking beauty and matching carnal skill. \n",
            good="Her well honed skills and good looks both were pleasing to the customer. \n",
            ok="Your girl did the job to the best of her ability but her skills could definitely be improved and her beauty enhanced. \n",
            bad="Your girl barely knew what she was doing. Her looks were not likely to be of any help to her either. \n" + \
                "Still, the customer explained that he preferred fucking her over a horse. Hearing that from him however, was not encouraging for your girl at all... \n",
            pretty="A cold turkey sandwich would have made a better sex partner than her. Her performance was however saved by her somewhat pleasing looks. \n",
            ugly="Her ability to please him sexually managed to help the client overlook the fact that she looked like a hag. \n"
        )
        
        def __init__(self, act, is_vaginal=False, sex_skill=None, preface=None, variants=None, **skill_text):
            """
            Creates a new PytWhoring instance.
            act = The type of act.
            is_vaginal = Whether the act involves the vagina.
            sex_skill = The skill involved with the act.
            variants = A dict of variant->text or variant->(texta, textb, etc) entries.
                Uses the variant keyword to find images for the act. All variants have an equal chance of being chosen.
                If more complex implementation of a variant is needed a PytWhoringVariant can be used instead of a string.
            skill_text = A dict to replace entries in the SKILL_TEXT dict.
                Can have the keywords: perfect, great, good, ok, bad, pretty, ugly
            """
            self.act = act
            self.is_vaginal = is_vaginal
            self.sex_skill = sex_skill or "vaginal"
            self.preface = preface
            self.variants = variants or dict()
            self.skill_text = skill_text
        
        def get_skill_text(self, level):
            """
            Returns the skill text.
            level = The level to return.
            """
            if level in self.skill_text: return self.skill_text[level]
            else: return self.SKILL_TEXT[level]
        
        def for_girl(self, girl):
            """
            Creates a PytWhoringCase for a girl.
            girl = The girl to create the case for.
            """
            return PytWhoringCase(self, girl)
        
    
    class PytWhoringVariant(_object):
        """
        A class to handle more complex logic for PytWhoring variants.
        """
        
        def __init__(self, text, dice=100, traits=None, noTraits=None, tags=None, noTags=None, is_vaginal=None):
            """
            Creates a new PytWhoringVariant.
            text = The text to display for the variant, or a tuple of choices.
            dice = The chance the variant will be considered.
            traits = The traits the girl requires for this variant to be chosen.
                The girl requires the trait (or all traits if a tuple) of 1 index for a successful check.
                [option1, (option2a, option2b)]
            noTraits = The traits the girl musn't have for this variant to be chosen.
                The girl musn't have the trait (or all traits if a tuple) of 1 index for a successful check.
                [option1, (option2a, option2b)]
            tags = The tags to use for the image check.
            noTags = Tags the image check can't use.
            is_vaginal = Override for the vaginal flag.
            """
            self.text = text
            self.dice = dice
            self.traits = traits
            self.noTraits = noTraits
            self.tags = tags
            self.noTags = noTags
            self.is_vaginal = is_vaginal
        
        def __call__(self, act, girl):
            """
            Checks whether this variant is possible.
            act = The act.
            girl = The girl.
            """
            if dice(self.dice):
                if self.traits:
                    for i in self.traits:
                        if isinstance(i, (list, tuple)):
                            for j in i:
                                if j not in girl.traits: break
                            
                            else:
                                break
                        
                        elif i in girl.traits: break
                    
                    else:
                        return None, None
                
                if self.noTraits:
                    for i in self.noTraits:
                        if isinstance(i, (list, tuple)):
                            for j in i:
                                if j in girl.traits: break
                            
                            else:
                                break
                        
                        elif i not in girl.traits: break
                    
                    else:
                        return None, None
                
                img = self.get_image(act, girl, has=True, exclude=["bdsm", "mast", "group"])
                
                if img:
                    if self.is_vaginal is not None:
                        return img, self.is_vaginal
                    
                    else:
                        return img, None
                
                else:
                    return None, None
                
            else:
                return None, None
        
        def get_image(self, act, girl, has=False, exclude=None, **kwargs):
            """
            Gets the image for the variant.
            act = The act.
            girl = The girl.
            has = Whether to return using the has_image or show function.
            kwargs = Arguments to pass to the functions.
            """
            if has: f = girl.has_image
            else: f = girl.show
            
            if exclude:
                if self.noTags: exclude += self.noTags
            
            elif self.noTags: exclude = self.noTags
            
            if self.tags:
                if exclude: return f(*self.tags, exclude=exclude, **kwargs)
                
                else: return f(*self.tags, **kwargs)
            
            else:
                if exclude: return f(act, exclude=exclude, **kwargs)
                
                else: return f(act, **kwargs)
        
    
    class PytWhoringCase(_object):
        """
        Class that solves individual act logic.
        """
        def __init__(self, job, girl):
            """
            Creates a new PytWhoringCase instance.
            job = The PytWhoring instance.
            girl = The girl the job is for.
            """
            self.job = job
            self.worker = girl
            self.is_vaginal = self.job.is_vaginal
            self.is_variant = False
            
            choices = list()
            for i in self.job.variants:
                if isinstance(self.job.variants[i], PytWhoringVariant):
                    b,v = self.job.variants[i](self.job.act, self.worker)
                    if b: choices.append((i,v))
                
                elif self.worker.has_image(self.job.act, i):
                    choices.append(i)
            
            if choices:
                self.act = choice(choices)
            else:
                self.act = "_"
            
            if isinstance(self.act, (list, tuple)):
                self.act, self.is_vaginal = self.act
                self.is_variant = True
        
        def get_image(self):
            """
            Returns the image.
            """
            if self.act == "_":
                return self.worker.show(self.job.act, exclude=["bdsm", "mast", "group"], resize=(740, 685))
            
            elif self.is_variant:
                return self.job.variants[self.act].get_image(self.job.act, self.worker, exclude=["bdsm", "mast", "group"], resize=(740, 685))
            
            else:
                return self.worker.show(self.job.act, self.act, exclude=["bdsm", "mast", "group"], resize=(740, 685))
        
        def get_preface(self):
            """
            Gets the preface text for the act.
            """
            t = self.job.preface
            if isinstance(t, (list,tuple)): t = choice(t)
            if "%s" in t:
                return t%self.worker.nickname
            
            else:
                return t
        
        def get_skill(self):
            """
            Gets the skill text and modifier.
            """
            skill = self.worker.get_skill(self.sex_skill)
            char = self.worker.charisma
            
            if skill > 300 and char > 300:
                return self.job.get_skill_text("perfect"), 3
            
            elif skill > 200 and char > 200:
                return self.job.get_skill_text("great"), 2
            
            elif skill > 80 and char > 80:
                return self.job.get_skill_text("good"), 1
            
            elif skill > 30 and char > 30:
                return self.job.get_skill_text("ok"), 0
            
            elif skill < 30 and char > 30:
                return self.job.get_skill_text("pretty"), -1
            
            elif skill > 30 and char < 30:
                return self.job.get_skill_text("ugly"), -1
            
            else:
                return self.job.get_skill_text("bad"), -2
            
            #else:
            #    devlog.error("PytWhoringCase.get_skill encountered an unknown condition. %s = %s, charisma = %s."%(self.sex_skill, skill, char))
            #    return self.job.get_skill_text("ok"), 0
        
        def get_text(self):
            """
            Returns the description.
            """
            # Get text
            t = self.job.variants[self.act]
            
            # If variant, get text
            if isinstance(t, PytWhoringVariant): t = t.text
            
            # If list...
            if isinstance(t, (list,tuple)):
                i = 0
                while i < len(t):
                    # If the index is a tuple
                    if isinstance(t[i], (list,tuple)):
                        # If it doesn't pass the roll remove it
                        if not dice(t[i][0]): t.pop(i)
                        else: i += 1
                    
                    else: i+= 1
                
                # Get the choice
                t = choice(t)
            
            # Interpolate
            if "%s" in t:
                return t%self.worker.nickname
            
            else:
                return t
        
        @property
        def has_preface(self):
            return self.job.preface is not None
        
        @property
        def sex_skill(self):
            """
            The skill the act uses.
            """
            return self.job.sex_skill
        
    
    def build_whoring_acts():
        """
        Function that builds the whoring acts for brothels.
        Used so the dict is saved.
        """
        man = PytWhoringManager()
        
        ###############################################################
        #
        # SEX ACTS FOR MALES
        #
        
        # Vaginal sex acts
        man.add(
            # is_vaginal is used to flag whether the girl loses her virginity from a sex act.
            # The WhoreJob class checks if the girl has the 'Virgin' trait and this flag, then runs the virgin removal/tip.
            PytWhoring("sex", is_vaginal=True, sex_skill="vaginal",
                       variants=dict(ontop="He invited her to 'sit' on his lap as he unsheathed his cock. They've continued along the same lines in 'girl ontop' position. \n",
                                     doggy="He ordered %s to bend over and took her from behind. \n",
                                     missionary="He pushed %s on her back, shoved his cock in, screaming: 'Oh, Your pussy is wrapping around me so tight!' \n",
                                     onside="%s lay on her side inviting the customer to fuck her. He was more than happy to oblige.\n",
                                     standing="Not even bothering getting into a position, he took her standing up. \n",
                                     spooning="Customer felt cuddly so he spooned the girl until they both cummed. \n",
                                     _=("He wanted some old-fashioned straight fucking. \n",
                                        "He was in the mood for some pussy pounding. \n",
                                        "He asked for some playtime with her vagina.\n")
                                     )
                       )
        )
        
        # Anal sex acts
        man.add(
            PytWhoring("anal", sex_skill="anal",
                       preface=("Anal sex is the best, customer thought... ",
                                "I am in the mood for a good anal fuck, customer said. ",
                                "Customer's dick got harder and harder just from the thought of %s's asshole! "),
                       variants=dict(ontop="He invited her to 'sit' on his lap as he unsheathed his cock. They've continued along the same lines in 'girl on top' position. \n",
                                     doggy="He ordered %s to bend over and took her from behind. \n",
                                     missionary="He pushed %s on her back, shoved his cock in, screaming: 'Oh, Your anus is wrapping around me so tight!' \n",
                                     onside="%s lay on her side inviting the customer to fuck her. He was more than happy to oblige.\n",
                                     standing="Not even bothering getting into a position, he took her standing up. \n",
                                     spooning="Customer felt cuddly so he spooned the girl until they both cummed. \n",
                                     _=('He took her in the ass right there and then. \n',
                                        'He got his dose of it. \n',
                                        'And so he took her in her butt. \n')
                                     )
                       )
        )
        
        # Oral sex acts
        man.add(
            PytWhoring("blowjob", sex_skill="oral",
                       variants=dict(deepthroat=("He shoved his cock all the way into her throat! \n",
                                                 "Deepthroat is definitely my style, thought the customer... \n"),
                                     
                                     handjob="He told %s to give him a good handjob.\n",
                                     
                                     footjob=PytWhoringVariant(("He asked her for a foodjob.\n",
                                                                "Footjob might be a weird fetish but that's what the customer wanted...\n"),
                                                               dice=80, tags=["footjob"]),
                                     
                                     titsjob_big=PytWhoringVariant(("He went straight for her big boobs. \n", "Seeing her knockers, customer wanted notning else then to park his dick between them. \n",
                                                                    "Lustfully gazing on your girl's burst, he asked for a titsjob. \n",
                                                                    "He put his manhood between her big tits. \n",
                                                                    "He showed his cock between %s's enormous breasts. \n"),
                                                                   traits=["Big Boobs", "Abnormally Large Boobs"], tags=["titsjob"]),
                                     
                                     titsjob_flat=PytWhoringVariant(( (7,"With a smirk on his face, customer asked for a titsjob. He was having fun from her vain effords. \n"),
                                                                     "He placed his cock between her breasts, clearly enyoing her flat chest. \n",
                                                                     "Even when knowing that her breasts are small, he wanted to be carresed by them. \n"),
                                                                    dice=50, traits=["Small Boobs"], tags=["titsjob"]),
                                     
                                     titsjob=PytWhoringVariant(("He asked for a titsjob. \n", "He let %s to carres him with her breasts. \n",
                                                                "He showed his cock between %s's tits. \n"),
                                                               noTraits=["Big Boobs", "Abnormally Large Boobs", "Small Boobs"], tags=["titsjob"]),
                                     
                                     bukkake=PytWhoringVariant(("Customer wanted nothing else then to jerk himself in from of her and ejactuate on her face. \n",
                                                                "He wanked himself hard in effort to cover her with his cum. \n"),
                                                               dice=20, tags=["bukkake"]),
                                     
                                     blowjob=PytWhoringVariant(("Client was in mood for some oral sex. \n",
                                                                "Client was in the mood for a blowjob. \n",
                                                                "He asked her to lick his dick. \n"),
                                                               noTags=["deepthroat", "handjob", "footjob", "titsjob", "bukkake"]),
                                     
                                     _=("Client was in mood for some oral sex. \n",
                                        "Client was in the mood for a blowjob. \n",
                                        "He asked her to lick his dick. \n")
                                     )
                       )
        )
        
        ###############################################################
        #
        # SEX ACTS FOR FEMALES
        #
        
        # Vaginal sex acts
        man.add(
            PytWhoring("sex", sex_skill="vaginal",
                       variants=dict(les=PytWhoringVariant(("She was in the mood for some girl on girl action. \n",
                                                            "She asked for a good lesbian sex. \n")),
                                     
                                     dildo_joined=PytWhoringVariant(("She'd asked your girl to lend her a double-ended dildo.\n",
                                                                     "She brought a twin-ended dildo for the party so %s could have some fun as well.\n"),
                                                                    tags=["les", "dildo joined"],
                                                                    is_vaginal=True),
                                     
                                     finger_pussy=PytWhoringVariant(("In mood for a hot lesbo action, she stuck her fingers in your girls pussy. \n",
                                                                     "She watched %s moan as she stuck fingers in her pussy. \n"),
                                                                    tags=["les", "finger pussy"]),
                                     
                                     do_finger_pussy=PytWhoringVariant(("Quite horny, she ordered your girl to finger her cunt. \n",
                                                                        "Clearly in the mood, she told %s to finger her until she cums. \n"),
                                                                       tags=["les", "do finger pussy"]),
                                     
                                     strapon=PytWhoringVariant(("She put on a strapon and fucked your girl in her cunt. \n",
                                                                "Equipping herself with a strap-on, she lustfully shoved it in %ss pussy. \n"),
                                                               tags=["les", "strapon"],
                                                               is_vaginal=True),
                                     
                                     do_strapon=PytWhoringVariant(("She ordered %s to put on a strapon and fuck her silly with it. \n",
                                                                   "She equipped %s with a strapon and told her that she was 'up' for a good fuck! \n"),
                                                                  tags=["les", "do strapon"]),
                                     
                                     dildo_pussy=PytWhoringVariant(("She played with a dildo and %ss pussy. \n",
                                                                    "She stuck a dildo up %s cunt. \n"),
                                                                   tags=["les", "dildo pussy"],
                                                                   is_vaginal=True),
                                     
                                     do_dildo_pussy=PytWhoringVariant(("Without further ado, %s fucked her with a dildo. \n",
                                                                       "She asked your girl to fuck her pussy with a dildo. \n"),
                                                                      tags=["les", "do dildo pussy"]),
                                     
                                     hug=PytWhoringVariant(("Girls lost themselves in eachothers embrace.\n",
                                                            "Any good lesbo action should start with a hug, don't you think??? \n"),
                                                           tags=["les", "hug"]),
                                     
                                     _=("She was in the mood for some girl on girl action. \n",
                                        "She asked for a good lesbian sex. \n")
                                     ),
                       ),
            female=True
        )
        
        # Anal sex acst
        man.add(
            PytWhoring("anal", sex_skill="anal",
                       variants=dict(finger_anus=PytWhoringVariant(("In mood for a hot lesbo action, she stuck her fingers in your girls anus. \n",
                                                                    "She watched %s moan as she stuck fingers in her asshole. \n"),
                                                                   tags=["les", "finger anus"]),
                                     
                                     do_finger_anus=PytWhoringVariant(("Quite horny, she ordered your girl to finger her anus. \n",
                                                                       "Clearly in the mood, she told %s to finger her asshole until she cums. \n"),
                                                                      tags=["les", "do finger anus"]),
                                     
                                     anal_strapon=PytWhoringVariant(("She put on a strapon and fucked your girl in her butt. \n",
                                                                     "Equipping herself with a strapon, she lustfully shoved it in %ss asshole. \n"),
                                                                    tags=["les", "anal strapon"]),
                                     
                                     do_anal_strapon=PytWhoringVariant(("She ordered %s to put on a strapon and butt-fuck her silly with it. \n",
                                                                        "She equipped %s with a strapon and told her that she was 'up' for a good anal fuck! \n"),
                                                                       tags=["les", "do anal strapon"]),
                                     
                                     anal_beads=PytWhoringVariant(("They got their hands on some anal beads and shoved it up %ss butt. \n",
                                                                   "She had some fun with your girls asshole and some anal beads \n"),
                                                                  tags=["les", "anal beads"]),
                                     
                                     do_anal_beads=PytWhoringVariant(("She had %s stick some anal beads up her butt. \n",
                                                                      "She told %s to get some anal beads to play with her anus. \n"),
                                                                     tags=["les", "do anal beads"]),
                                     
                                     dildo_anal=PytWhoringVariant(("After some foreplay, she stuck a dildo up your girls butt. \n",
                                                                   "For her money, she had some fun playing with a dildo and your girls asshole. \n"),
                                                                  tags=["les", "dildo anal"]),
                                     
                                     do_dildo_anal=PytWhoringVariant(("After some foreplay, she asked %s to shove a dildo up her ass. \n",
                                                                      "This female customer of your brothel clearly believed that there is no greater pleasure than a dildo up her butt. \n"),
                                                                     tags=["les", "do dildo anal"]),
                                     
                                     _=("She was in the mood for some girl on girl action. \n",
                                        "She asked for a good lesbian sex. \n")
                                     )
                       ),
            female=True
        )
        
        # Oral sex acts
        man.add(
            PytWhoring("oral", sex_skill="oral",
                       variants=dict(lick_pussy=PytWhoringVariant(("Clearly in the mood for some cunt, she licked %ss pussy clean.\n",
                                                                   "Hungry for a cunt, she told %s to be still and started licking her soft pussy with her hot tong. \n"),
                                                                  tags=["les", "lick pussy"]),
                                     
                                     do_lick_pussy=PytWhoringVariant(("All hot and bothered, she ordered %s to lick her cunt. \n",
                                                                      "As if she had an itch, she quickly told %s to tong her pussy. \n"),
                                                                     tags=["les", "do lick pussy"]),
                                     
                                     lick_anus=PytWhoringVariant(("She licked %ss anus clean.\n",
                                                                  "She told %s to be still and started licking her asshole with her hot tong. \n"),
                                                                 tags=["les", "lick anus"]),
                                     
                                     do_lick_anus=PytWhoringVariant(("All hot and bothered, she ordered %s to lick her asshole. \n",
                                                                     "As if she had an itch, she quickly told %s to tong her anus. \n"),
                                                                    tags=["les", "do lick anus"]),
                                     
                                     # Put these here as they don't really fit into vaginal/anal/oral, and oral was short
                                     #
                                     caress_tits=PytWhoringVariant(("Liking your girls breasts, she had some good time caressing them. \n",
                                                                    "She enjoyed herself by caressing your girls breasts. \n"),
                                                                   tags=["les", "caress tits"]),
                                     
                                     do_caress_tits=PytWhoringVariant(("She asked your girl to caress her tits. \n",
                                                                       "She told your girl to put a squeeze on her breasts. \n"),
                                                                      tags=["les", "do squeezes tits"]),
                                     
                                     _=("She was in the mood for some girl on girl action. \n",
                                        "She asked for a good lesbian sex. \n")
                                     )
                       ),
            female=True
        )
        
        return man
    
    # WhoreJob:
    # solve_job_guard_event(self, "whore_event", enemies=self.client)
    #
    # ServiceJob
    # solve_job_guard_event(self, "bar_event", clients=self.loc.servicer["barclientsleft"], enemies=aggressive_clients, no_guard_occupation="ServiceGirl") 
    #
    def solve_job_guard_event(event, relay, clients=0, enemies=None, no_guard_occupation=None):
        """
        Solves a client vs. guard fight during a job.
        event = The job instance.
        relay = The event relay to use in the guards.
        clients = The number of clients if a selection should be used from enemies.
        enemies = The list of enemies to fight.
        no_guard_occupation = The girls who get hurt during the fight if not the event specific girl.
        
        Returns: Whether or not the 'fight' should end the job.
        """
        resolved = False
        
        # Get the guards
        guards = event.loc.get_girls("Guard")
        guardlist = list()
        totalpayoff = 0
        
        if guards:
            for guard in guards:
                if guard.AP > 0 and guard.health > 40 and guard.vitality > 40:
                    guard.guard_relay[relay]["count"] += 1
                    guard.guard_relay[relay]["helped"].append(event.girl.name)
                    guardlist.append(guard)
                    totalpayoff += int(guard.fin.expects_wage()/2) + event.girl.fin.expects_wage()*2
        
        if hero.location == event.loc and hero.AP > 0:
            guardlist.append(hero)
        
        # Get the enemies
        if not isinstance(enemies, list):
            enemylist = [enemies]
            enemies = None
        
        elif clients:
            enemylist = enemies[:]
            if clients > 50: clients = min(randint(8, 12), len(enemylist))
            elif clients > 30: clients = min(randint(4, 8), len(enemylist))
            elif clients > 20: clients = min(randint(3, 6), len(enemylist))
            elif clients > 10: clients = min(randint(2, 3), len(enemylist))
            else:
                # Nothing happens, no clients
                return True
            
            while len(enemylist) > clients:
                enemylist.pop(0)
        
        if len(enemylist) > 1: pronoun = "they"
        else: pronoun = enemylist[0].pronoun
        
        # If there are guards on duty
        if guardlist:
            if len(guardlist) >= 3:
                event.txt.append(", ".join(girl.name for girl in guardlist[:-1]) + " and %s responded to %s's calls for help! \n"%(guardlist[-1].nickname, event.girl.name))
            
            elif len(guardlist) == 2:
                event.txt.append("%s and %s responded to %s's calls for help! \n"%(guardlist[0].name, guardlist[1].name, event.girl.name))
            
            else:
                event.txt.append("%s responded to %s's calls for help! \n"%(guardlist[0].name, event.girl.name))
            
            ##### RESULTS
            cresult, cexp = s_conflict_resolver(guardlist, enemylist, new_results=True)
            
            # Overwealing victory
            if cresult == "OV":
                event.txt.append("{color=[lawngreen]}Facing the overwheling odds, the customer surrendered.{/color} %s paid off your guards to prevent further escalation. "%pronoun + \
                                 "You recieve a compensation of {color=[gold]}%d Gold{/color}! \n"%totalpayoff)
                
                hero.add_money(totalpayoff, reason="GuardJob")
                event.loc.fin.log_work_income(totalpayoff, "GuardJob")
                event.flag_green = True
                
                for guard in guardlist:
                    statdict = dict(attack=choice([0,0,0,0,1]),
                                    defence=choice([0,0,0,0,1]),
                                    agility=choice([0,0,0,0,1]),
                                    intelligence=choice([0,0,1]),
                                    exp=cexp
                                    )
                    
                    gset = set(guard.guard_relay[relay]["stats"])|set(statdict)
                    guard.guard_relay[relay]["stats"] = dict( (n, guard.guard_relay[relay]["stats"].get(n, 0)+statdict.get(n, 0)) for n in gset )
                    guard.guard_relay[relay]["won"] += 1
                    guard.AP -= choice([0,1])
            
            # Desisive victory
            elif cresult == "DV":
                event.txt.append("{color=[lawngreen]}Seeing how the odds do not favor a positive outcome, customer decided to pay rather than fight.{/color} " + \
                                 "%s paid off your guards to prevent further escalation. You recieve a compensation of {color=[gold]}%d Gold{/color}! \n"%(pronoun, totalpayoff))
                
                hero.add_money(totalpayoff, reason="GuardJob")
                event.loc.fin.log_work_income(totalpayoff, "GuardJob")
                event.flag_green = True
                
                for guard in guardlist:
                    statdict = dict(attack=choice([0,0,0,0,1]),
                                    defence=choice([0,0,0,0,1]),
                                    agility=choice([0,0,0,0,1]),
                                    intelligence=choice([0,0,1]),
                                    vitality=randint(-30, -20),
                                    exp=cexp
                                    )
                    
                    gset = set(guard.guard_relay[relay]["stats"])|set(statdict)
                    guard.guard_relay[relay]["stats"] = dict( (n, guard.guard_relay[relay]["stats"].get(n, 0)+statdict.get(n, 0)) for n in gset )
                    guard.guard_relay[relay]["won"] += 1
                    guard.AP -= choice([0,1])
            
            # Combat
            else:
                event.txt.append("Not being impressed with your security at all, client decided to attack your guards! \n")
                
                # (Lucky) Victory
                if cresult == "V" or cresult == "LV":
                    if cresult == "LV": event.txt.append("{color=[lawngreen]}It was a hard fight, but ")
                    else: event.txt.append("{color=[lawngreen]}But ")
                    
                    event.txt.append("%s was defeated and was given a choice to pay up or face the authorities.{/color} "%pronoun)
                    event.flag_green = True
                    
                    if dice(80):
                        totalpayoff = totalpayoff * 2
                        event.txt.append("Customer payed up a hefty sum of {color=[gold]}%d Gold {/color} as compensation for troubles caused. "%(totalpayoff))
                        hero.add_money(totalpayoff, reason="GuardJob")
                        event.loc.fin.log_work_income(totalpayoff, "GuardJob")
                    
                    else:
                        event.txt.append("Customer didn't have the funds to pay you off and after many cries for mercy, was handed over to the authorities to face an uncertain fate. ")
                    
                    for guard in guardlist:
                        statdict = dict(attack=choice([0,1,1]),
                                        defence=choice([0,1,1]),
                                        agility=choice([0,1,1]),
                                        magic=choice([0,1,1]),
                                        intelligence=choice([0,1,1]),
                                        mp=choice([0,1,1]),
                                        health=randint(-10, -3),
                                        vitality=randint(-60, -30),
                                        exp=cexp
                                        )
                        
                        gset = set(guard.guard_relay[relay]["stats"])|set(statdict)
                        guard.guard_relay[relay]["stats"] = dict( (n, guard.guard_relay[relay]["stats"].get(n, 0)+statdict.get(n, 0)) for n in  gset)
                        guard.guard_relay[relay]["won"] += 1
                        guard.AP -= randint(1,2)
                
                # Overwhealing defeat
                elif cresult == "OD":
                    event.txt.append("{color=[red]}Easily defeating security, the customer slapped your girl around a little bit and swaggered "+ \
                                     "out of the building like %s owned the place.{/color} "%pronoun)
                    
                    event.girlmod["health"] -= randint(10, 15)
                    event.flag_red = True
                    
                    for guard in guardlist:
                        statdict = dict(health=randint(-70, -50),
                                        vitality=randint(-100, -50),
                                        mp=randint(-30, -10)
                                        )
                        
                        gset = set(guard.guard_relay[relay]["stats"])|set(statdict)
                        guard.guard_relay[relay]["stats"] = dict( (n, guard.guard_relay[relay]["stats"].get(n, 0)+statdict.get(n, 0)) for n in gset )
                        guard.guard_relay[relay]["lost"] += 1
                        guard.AP -= 3
                
                # Defeat
                else:
                    event.txt.append("{color=[red]}Customer managed to defeat security but quickly left the establishment in the mood for nothing but healing. {/color}")
                    event.flag_red = True
                    
                    for guard in guardlist:
                        statdict = dict(attack=choice([0,0,0,0,1]),
                                        defence=choice([0,0,0,0,1]),
                                        agility=choice([0,0,0,0,1]),
                                        magic=choice([0,1,0,0,0]),
                                        health=randint(-30, -15),
                                        vitality=randint(-50, -25),
                                        mp=randint(-15, -5)
                                        )
                        
                        gset = set(guard.guard_relay[relay]["stats"])|set(statdict)
                        guard.guard_relay[relay]["stats"] = dict( (n, guard.guard_relay[relay]["stats"].get(n, 0)+statdict.get(n, 0)) for n in gset )
                        guard.guard_relay[relay]["lost"] += 1
                        guard.AP -= 2
            
            # Removing customers from the main list
            # Only happens if security was present
            if enemies:
                for enemy in enemylist:
                    enemies.remove(enemy)
            
            event.img = "profile"
        
        # Else no guards
        else:
            event.txt.append("Your establishment lacked active security guards so customer was free to do as %s pleased. "%pronoun.lower())
            
            # If we should use simple logic
            if no_guard_occupation:
                event.txt.append("Your staff got hurt in the process. {/color}\n")
                event.flag_red = True
                
                for entry in event.loc.get_girls(occupation=no_guard_occupation):
                    entry.disposition -= randint(25, 50)
                    entry.health -= randint(10, 25)
                    entry.vitality -= randint(30, 60)
                    entry.AP -= 3
                
                if event.girl.has_image("hurt", exclude=["sex"]):
                    event.img = event.girl.show("hurt", exclude=["sex"], resize=(740, 685))
                
                else:
                    event.img = event.girl.show("profile", "sad", resize=(740, 685))
            
            # Else complex logic
            else:
                # Trait lists to be used in checks:
                aggro = ["Fighter", "Assasin", "Fearless", "Aggressive", "Tsundere", "Malicious", "Strong"]
                body = ["Abnormally Large Boobs", "Big Boobs", "Elegant", "Long Legs", "Great Arse", "Sexy Air", "Great Figure"]
                good_mind = ["Smart", "Genius"]
                bad_mind = ["Broken Will", "Shy", "Meek", "Nerd", "Kind", "Mind Fucked"]
                
                # Any girl with negative mind traits
                if set(bad_mind).intersection(event.girl.traits):
                    event.txt.append("{color=[red]}Your girl did not resist and just took a beating. That seemed to piss off customer a bit as well... {/color}")
                    event.flag_red = True
                    event.girlmod["health"] -= randint(40, 70)
                    event.girlmod["vitality"] -= randint(150, 250)
                    event.girlmod["disposition"] -= 50
                    event.girl.AP = 0
                    if event.girl.has_image("hurt", exclude=["sex"]):
                        event.img = event.girl.show("hurt", exclude=["sex"], resize=(740, 685))
                
                    else:
                        event.img = event.girl.show("profile", "sad", resize=(740, 685))
                    
                    # End
                    event.girls.remove(event.girl)
                
                # Free girls with aggressive traits
                elif event.girl.status != "slave" and set(aggro).intersection(event.girl.traits):
                    event.txt.append("%s tried to fight back herself! "%(event.girl.name))
                    
                    totaldef = 0
                    totaloff = 0
                    
                    totaldef += event.girl.attack + event.girl.defence + event.girl.agility + event.girl.magic
                    totaloff += event.client.attack + event.client.defence + event.client.agility + event.client.magic
                    
                    if totaldef > totaloff:
                        event.txt.append("{color=[green]}She proved to be better at combat than customer expected so %s ran away. {/color}"%pronoun.lower())
                        event.flag_green = True
                        event.girl.exp += int(totaloff/10)
                        event.girlmod["attack"] += choice([0,1,2])
                        event.girlmod["defence"] += choice([0,1,2])
                        event.girlmod["agility"] += choice([0,1,2])
                        event.girlmod["intelligence"] += choice([0,1])
                        event.girlmod["health"] -= randint(3,10)
                        event.girlmod["vitality"] -= randint(30,60)
                        event.girlmod["mp"] -= randint(3,10)
                        event.girl.AP -= 2
                        event.img = event.girl.show("profile", "happy", resize=(740, 685))
                    
                    else:
                        event.txt.append("{color=[red]}But it was in vain, client was just too strong for her to handle. So pissed off at your girl's arrogance, "+ \
                                        "%s raped and beat her to near death. {/color}"%pronoun.lower())
                        event.flag_red = True
                        event.girlmod["health"] -= randint(50, 80)
                        event.girlmod["vitality"] -= randint(150, 250)
                        event.girlmod["disposition"] -= 200
                        event.girl.AP = 0
                        if event.girl.has_image("hurt", exclude=["sex"]):
                            event.img = event.girl.show("hurt", exclude=["sex"], resize=(740, 685))
                
                        else:
                            event.img = event.girl.show("profile", "sad", resize=(740, 685))
                        
                        # End
                        event.girls.remove(event.girl)
                
                # Any girl with positive body traits
                elif set(body).intersection(event.girl.traits):
                    event.txt.append("%s decided to use her natural charm in order to calm the customer down. "%event.girl.name)
                    
                    if dice(80):
                        event.txt.append("{color=[green]}Mesmerized by her heavenly body traits, customer calmed down and they proceeded as usual.{/color} \n")
                        event.flag_green = True
                        resolved = True
                    
                    else:
                        event.txt.append("{color=[red]}Customer however did not care and went on beating the crap out of your girl.{/color} ")
                        event.flag_red = True
                        event.girlmod["health"] -= randint(50, 80)
                        event.girlmod["vitality"] -= randint(150, 250)
                        event.girlmod["disposition"] -= 100
                        event.girl.AP = 0
                        if event.girl.has_image("hurt", exclude=["sex"]):
                            event.img = event.girl.show("hurt", exclude=["sex"], resize=(740, 685))
                
                        else:
                            event.img = event.girl.show("profile", "sad", resize=(740, 685))
                        
                        # End
                        event.girls.remove(event.girl)
                
                # Any girl with "brainy" traits
                elif set(good_mind).intersection(event.girl.traits):
                    event.txt.append("%s tryed to reason with customer in order to calm %s down. "%(event.girl.name, pronoun.lower()))
                    
                    if dice(50):
                        event.txt.append("{color=[green]}It was a success so they returned to 'business as usual' {/color}\n")
                        event.flag_green = True
                        resolved = True
                    
                    else:
                        event.txt.append("{color=[red]}Client did not even stop for a moment to consider her words and just attacked. {/color}\n")
                        event.flag_red = True
                        event.girlmod["health"] -= randint(50, 80)
                        event.girlmod["vitality"] -= randint(150, 250)
                        event.girlmod["disposition"] -= 100
                        event.girl.AP = 0
                        if event.girl.has_image("hurt", exclude=["sex"]):
                            event.img = event.girl.show("hurt", exclude=["sex"], resize=(740, 685))
                
                        else:
                            event.img = event.girl.show("profile", "sad", resize=(740, 685))
                        
                        # End
                        event.girls.remove(event.girl)
                
                # Slave girl with Tsundere traits.
                # TODO: Should cause some form of trouble for the player!
                #elif event.girl.status == "slave" and "Tsundere" in event.girl.traits:
                #    event.txt.append("Tsundere slavegirls are a pain in the world of PyTFall. She attacked a customer, " + \
                #                     "and a slave fighting even in event-defense may cause trouble for you later. Abashed by a slavegirl's attack, customer ran away, " + \
                #                     "in all likelihood to report you and her to the authorities. ")
                #    event.img = "profile"
                
                # No specific traits
                else:
                    event.payout = event.payout * choice([1.5, 1.5, 2, 2.5, 3])
                    
                    event.txt.append("{color=[red]}Your girl tried to scream but customer quickly shut her mouth and punched her in the stomach. " + \
                                    "Threatening to kill her otherwise %s raped and beat her, making every twisted thought a reality. "%pronoun.lower())
                    
                    event.txt.append("After what seemed like hours (at least to your girl), client looking very satisfied, threw some coints on the pillow near her and left the establishment." + \
                                    "{/color} \n")
                    
                    event.txt.append("You later find out that it was sum of {color=[gold]}%d Gold{/color}. "%event.payout)
                    
                    event.flag_red = True
                    event.girlmod["health"] -= randint(30, 50)
                    event.girlmod["vitality"] -= randint(150, 250)
                    event.girlmod["disposition"] -= 200
                    event.girl.AP = 0
                    
                    hero.add_money(event.payout, "WhoreJob")
                    event.loc.fin.log_work_income(event.payout, "WhoreJob")
                    if event.girl.has_image("hurt", exclude=["sex"]):
                        event.img = event.girl.show("hurt", exclude=["sex"], resize=(740, 685))
                
                    else:
                        event.img = event.girl.show("profile", "sad", resize=(740, 685))
        
        return resolved
    
