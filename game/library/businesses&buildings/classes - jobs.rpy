init -9 python:
    def check_char(c):
        """Checks whether the character is injured and sets her/him to auto rest.
        """
        if c.health < c.get_max("health")*0.25:
            # self.txt.append("%s is injured and in need of medical attention! "%c.name)
            # self.img = c.show("profile", "sad", resize=(740, 685))
            if c.autocontrol['Rest']:
                c.previousaction = c.action
                c.action = AutoRest()
                # self.txt.append("She is going to take few days off to heal her wounds. ")
            return    
        if c.vitality < 30:
            # self.txt.append("%s is to tired to work today! "%c.name)
            # self.img = c.show("profile", "sad", resize=(740, 685))
            if c.autocontrol['Rest']:
                c.previousaction = c.action
                c.action = AutoRest()
                # self.txt.append("She's going to take few days off to recover her stamina. ")
            return
        if c.AP <= 0:
            return
            
        return True
    
    class Job(_object):
        """ Baseclass for jobs and other next day actions with some defaults.
        
        - Older class used with Schools and Training.
        """
        def __init__(self, girl=None, girls=None, loc=None, event_type="jobreport"):
            """Creates a new Job.
            
            girl = The girl doing the job.
            girls = A container with all the girls. (May not be useful anymore)
            """
            self.id = "Base Job"
            self.girls = girls
            self.girl = girl
            self.girlmod = {} # Logging all stats/skills changed during the job.
            
            self.loc = loc
            self.locmod = {}
            
            # Traits/Job-types associated with this job:
            self.occupations = list() # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = list() # Corresponing traits...
            
            self.txt = list()
            self.img = ""
            self.finished = False
            
            self.flag_red = False
            self.flag_green = False
            
            self.event_type = event_type
            
        def __call__(self, girl, girls, loc=None, event_type="jobreport"):
            self.girl = girl
            self.girls = girls
            self.loc = loc
            self.event_type = event_type
            
            self.finished = False
            
        def __str__(self):
            return str(self.id)
            
        def reset(self):
            self.girl = None
            self.loc = None
            self.client = None
            self.event_type = None
            self.finished = False
            self.txt = list()
            self.img = ""
            
            self.flag_red = False
            self.flag_green = False
            
            self.girlmod = {}
            self.locmod = {}
            
            
        @property
        def all_occs(self):
            # All Occupations:
            return set(self.occupations + self.occupation_traits)
            
        def get_clients(self):
            # This returns a correct amount of clients used for the job
            return 0
        
        def create_event(self):
            """
            Returns an event depicting the current state of this job.
            """
            if isinstance(self.txt, (list, tuple)):
                try:
                    self.txt = "".join(self.txt)
                except TypeError:
                    self.txt = "".join(str(i) for i in self.txt)
            
            return NDEvent(type=self.event_type,
                                 img=self.img,
                                 txt=self.txt,
                                 char=self.girl,
                                 charmod=self.girlmod,
                                 loc=self.loc,
                                 locmod=self.locmod,
                                 green_flag=self.flag_green,
                                 red_flag=self.flag_red)
            
        def check_occupation(self, char=None):
            """
            Checks the girls occupation.
            """
            return True
        
        def check_life(self):
            """
            Checks whether the girl is alive.
            Might be deprecated, needs updating.
            """
            if not self.girl.alive:
                self.txt.append("%s is dead. \n"%self.girl.fullname)
                self.girls.remove(self.girl)
                self.img = im.Sepia(self.girl.show('profile'), resize=(740, 685))
                self.finish_job()
        
        def finish_job(self):
            """
            Finish the job and adds it to NextDayList.
            """
            self.finished = True
            NextDayList.append(self.create_event())
            
            # Reset all attrs:
            # Redundant?
            self.girlmod = {}
            self.locmod = {}
            self.txt = list()
            self.img = ""
            self.flag_red = False
            self.flag_green = False
        
        def check_injury(self):
            """Checks whether the girl is injured and sets her to auto rest.
            """
            if self.girl.health < self.girl.get_max("health")*0.25:
                self.txt.append("%s is injured and in need of medical attention! "%self.girl.name)
                self.img = self.girl.show("profile", "sad", resize=(740, 685))
                
                if self.girl.autocontrol['Rest']:
                    self.girl.previousaction = self.girl.action
                    self.girl.action = 'AutoRest'
                    self.txt.append("She is going to take few days off to heal her wounds. ")
                
                self.girls.remove(self.girl)
                self.finish_job()
        
        def check_vitality(self):
            """
            Checks whether the girl is tired and sets her to auto rest.
            """
            if self.girl.vitality < 30:
                self.txt.append("%s is to tired to work today! "%self.girl.name)
                self.img = self.girl.show("profile", "sad", resize=(740, 685))
                
                if self.girl.autocontrol['Rest']:
                    self.girl.previousaction = self.girl.action
                    self.girl.action = 'AutoRest'
                    self.txt.append("She's going to take few days off to recover her stamina. ")
                
                self.girls.remove(self.girl)
                self.finish_job()
        
        def apply_stats(self):
            """
            Applies the stat changes generated by this job to the girl.
            """
            for stat in self.girlmod:
                if stat == "exp":
                    self.girlmod[stat] = self.girl.adjust_exp(self.girlmod[stat])
                    self.girl.exp += self.girlmod[stat]
                
                # After a long conversation with Dark and CW, we've decided to prevent girls dieing during jobs
                # I am leaving the code I wrote before that decision was reached in case
                # we change our minds or add jobs like exploration where it makes more sense.
                # On the other hand just ignoring it is bad, so let's at least reduce some stuff, pretending that she lost consciousness for example.
                elif stat == 'health' and (self.girl.health + self.girlmod[stat]) <= 0:
                    self.girl.health = 1
                    if self.girl.constitution > 5:
                        self.girl.constitution -= 5
                
                else:
                    if self.girl.stats.is_stat(stat):
                        self.girl.stats.mod(stat, self.girlmod[stat])
                        
                    elif self.girl.stats.is_skill(stat):
                        setattr(self.girl, stat, self.girlmod[stat])
                        # self.girl.stats.mod_skill(stat, self.girlmod[stat])
            
            for stat in self.locmod:
                if stat == 'fame':
                    self.loc.modfame(self.locmod[stat])    
                
                elif stat == 'dirt':
                    if self.locmod[stat] < 0:
                        self.loc.clean(self.locmod[stat]*-1)
                    
                    else:
                        self.loc.dirt += self.locmod[stat]
                
                elif stat == 'reputation':
                    self.loc.modrep(self.locmod[stat])
                
                else:
                    raise Exception("Stat: {} does not exits for Brothels".format(stat))
        
        def auto_clean(self):
            """
            Auto cleans the building if needed.
            """
            if isinstance(self.loc, DirtyBuilding):
                if self.loc.auto_clean and self.loc.get_dirt_percentage()[0] > 80:
                    price = self.loc.get_cleaning_price()
                    if hero.take_money(price, reason="Pro-Cleaning"):
                        self.loc.fin.log_expense(price, "Pro-Cleaning")
                        self.loc.dirt = 0
                        self.txt.append("Cleaners were hired to tidy up your building. Cost: {color=[gold]} %s Gold.{/color}\n\n"%price)
                    
                    else:
                        self.txt.append("You did not have enough funds to pay for the professional cleaning service (%d Gold).\n\n"%price)
        
        def check_dirt(self):
            """
            Checks the dirt for the building and reports it.
            """
            if isinstance(self.loc, DirtyBuilding):
                if self.loc.get_dirt_percentage()[0] > 80:
                    self.txt.append(choice(["Your building looks like a pigstall, fix this or keep losing your clients!",
                                                         "Your building is to dirty to do business!",
                                                         "Clean your damn establishment or keep losing money and rep!"]))
                    
                    if dice(self.loc.get_dirt_percentage()[0]):
                        self.locmod["reputation"] -= randint(2, 5)
                    
                    self.apply_stats()
                    self.img = self.girl.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")
                    self.finish_job()
                    
                    return True
                
                else:
                    return False
            
            else:
                return False
        
        def loggs(self, s, value):
            # Logs girls stat/skill to a dict:
            self.girlmod[s] = self.girlmod.get(s, 0) + value
            
        def logloc(self, s, value):
            # Logs a stat for the building:
            self.locmod[s] = self.girlmod.get(s, 0) + value
            
    class NewStyleJob(Job):
        """Baseclass for jobs and other next day actions with some defaults.
        
        - Presently is used in modern Job Classes. Very similar to Job.
        """
        def __init__(self, event_type="jobreport"):
            """Creates a new Job.
            
            worker = The worker doing the job.
            workers = A container with all the workers. (May not be useful anymore)
            """
            self.id = "Base Job"
            
            self.workermod = {} # Logging all stats/skills changed during the job.
            self.locmod = {}
            
            # Traits/Job-types associated with this job:
            self.occupations = list() # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = list() # Corresponing traits...
            
            self.txt = list()
            self.img = ""
            self.flag_red = False
            self.flag_green = False
            
            self.event_type = event_type
            
        def __call__(self, worker, event_type="jobreport"):
            self.worker = worker
            self.loc = worker.location
            self.event_type = event_type
            
        def __str__(self):
            return str(self.id)
            
        def reset(self):
            # New, we reset any flags that start with "job_" that a character might have.
            for f in self.worker.flags.keys():
                if f.startswith("jobs"):
                    self.worker.del_flag(f)
            self.worker = None
            self.loc = None
            self.client = None
            self.event_type = None
            self.txt = list()
            self.img = ""
            
            self.flag_red = False
            self.flag_green = False
            
            self.workermod = {}
            self.locmod = {}
            
        @property
        def all_occs(self):
            # All Occupations:
            return set(self.occupations + self.occupation_traits)
            
        def get_clients(self):
            # This returns a correct amount of clients used for the job
            return 0
        
        def create_event(self):
            """
            Returns an event depicting the current state of this job.
            """
            if isinstance(self.txt, (list, tuple)):
                try:
                    self.txt = "".join(self.txt)
                except TypeError:
                    self.txt = "".join(str(i) for i in self.txt)
            
            return NDEvent(type=self.event_type,
                                      img=self.img,
                                      txt=self.txt,
                                      char=self.worker,
                                      charmod=self.workermod,
                                      loc=self.loc,
                                      locmod=self.locmod,
                                      green_flag=self.flag_green,
                                      red_flag=self.flag_red)
            
        def check_occupation(self, char=None):
            """Checks if a worker is willing to do this job.
            """
            return True
        
        def check_life(self):
            """
            Checks whether the worker is alive.
            Might be deprecated, needs updating.
            """
            if not self.worker.alive:
                self.txt.append("%s is dead. \n"%self.worker.fullname)
                self.workers.remove(self.worker)
                self.img = im.Sepia(self.worker.show('profile'), resize=(740, 685))
                self.finish_job()
        
        def finish_job(self):
            """
            Finish the job and adds it to NextDayList.
            """
            NextDayList.append(self.create_event())
            self.reset()
        
        def apply_stats(self):
            """
            Applies the stat changes generated by this job to the worker.
            """
            for stat in self.workermod:
                if stat == "exp":
                    self.workermod[stat] = self.worker.adjust_exp(self.workermod[stat])
                    self.worker.exp += self.workermod[stat]
                
                # After a long conversation with Dark and CW, we've decided to prevent workers dieing during jobs
                # I am leaving the code I wrote before that decision was reached in case
                # we change our minds or add jobs like exploration where it makes more sense.
                # On the other hand just ignoring it is bad, so let's at least reduce some stuff, pretending that she lost consciousness for example.
                elif stat == 'health' and (self.worker.health + self.workermod[stat]) <= 0:
                    self.worker.health = 1
                    if self.worker.constitution > 5:
                        self.worker.constitution -= 5
                else:
                    if self.worker.stats.is_stat(stat):
                        self.worker.stats.mod(stat, self.workermod[stat])
                        
                    elif self.worker.stats.is_skill(stat):
                        setattr(self.worker, stat, self.workermod[stat])
                        # self.worker.stats.mod_skill(stat, self.workermod[stat])
            
            for stat in self.locmod:
                if stat == 'fame':
                    self.loc.modfame(self.locmod[stat])
                
                elif stat == 'dirt':
                    if self.locmod[stat] < 0:
                        self.loc.clean(self.locmod[stat]*-1)
                    
                    else:
                        self.loc.dirt += self.locmod[stat]
                
                elif stat == 'reputation':
                    self.loc.modrep(self.locmod[stat])
                
                else:
                    raise Exception("Stat: {} does not exits for Brothels".format(stat))
        
        def loggs(self, s, value):
            # Logs workers stat/skill to a dict:
            self.workermod[s] = self.workermod.get(s, 0) + value
            
        def logloc(self, s, value):
            # Logs a stat for the building:
            self.locmod[s] = self.workermod.get(s, 0) + value
    ####################### Whore Job  ############################
    class WhoreJob(NewStyleJob):
        #Temporarily restored for reference!
        def __init__(self):
            super(WhoreJob, self).__init__()
            self.id = "Whore Job"
            
            # Traits/Job-types associated with this job:
            self.occupations = list() # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Prostitute"]] # Corresponding traits...
            
            self.workermod = {}
            self.locmod = {}
            
        def __call__(self, char, client):
            self.event_type = "jobreport"
            self.worker, self.client, self.loc = char, client, char.location
            self.worker.AP -= 1
            self.payout_mod()
            self.acts()

        def check_occupation(self, char=None):
            """Checks if the worker is willing to do this job.
            """
            if not [t for t in self.all_occs if t in char.occupations]:
                if char.status != 'slave':
                    if "Shy" in char.traits and dice(50):
                        self.txt.append("When %s found out that she has to do it with a stranger even though it's not a part of her job, she blushed and ran away." % char.nickname)
                        self.loggs('joy', -5)
                        self.loggs('disposition', -30)
                        self.worker = char
                        self.loc = char.location
                        self.event_type = "jobreport"
                        self.img = char.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")
                        char.action = None
                    
                        self.apply_stats()
                        self.finish_job()
                        return
                    if "Nymphomaniac" in char.traits:
                        if char.disposition >= 650 and joy >= 50:
                            char.set_flag("jobs_whoreintro", "It's not really a part of her job, but on the other hand %s doesn't mind to have some fun." % char.nickname)
                            char.set_flag("jobs_introdis", -randint(5, 10))
                            char.set_flag("jobs_introjoy", randint(4, 7))
                        elif char.disposition >= 650:
                            self.txt.append("Normally she wouldn't mind to have some fun even though it's not a part of her job, but %s is not in the mood for that right now." % char.nickname)
                            self.loggs('disposition', -20)
                            self.worker = char
                            self.loc = char.location
                            self.event_type = "jobreport"
                            self.img = char.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")
                            char.action = None
                    
                            self.apply_stats()
                            self.finish_job()
                            return
                        else:
                            self.txt.append("%s refuses to do it with some stranger since it's not a part of her job. Oh well, at least she is not mad at you." % char.nickname)
                            self.loggs('disposition', -30)
                            self.worker = char
                            self.loc = char.location
                            self.event_type = "jobreport"
                            self.img = char.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")
                            char.action = None
                    
                            self.apply_stats()
                            self.finish_job()
                            return
                    elif check_lovers(char, hero):
                        char.set_flag("jobs_whoreintro", "%s doesn't like the idea to do it with some stranger when she has a lover, but she doesn't want to argue with you." % char.nickname)
                        char.set_flag("jobs_introdis", -randint(5, 15))
                    elif "Frigid" in char.traits:
                        self.txt.append("%s angrily refuses to work as a whore for you, especially since it's not a part of her job.")
                        self.loggs('disposition', -80)
                        self.loggs('joy', -15)
                        self.worker = char
                        self.loc = char.location
                        self.event_type = "jobreport"
                        self.img = char.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")
                        char.action = None
                    
                        self.apply_stats()
                        self.finish_job()
                        return
                    elif char.disposition >= 800:
                        char.set_flag("jobs_whoreintro", "%s is not thrilled about having some stranger 'do' her, but she likes you too much to refuse." % char.nickname)
                        char.set_flag("jobs_introdis", -randint(10, 35))
                    else:
                        self.txt.append("%s refuses to do it with strangers since it's not a part of her job." % char.nickname)
                        self.loggs('disposition', -50)
                        self.worker = char
                        self.loc = char.location
                        self.event_type = "jobreport"
                        self.img = char.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")
                        char.action = None
                    
                        self.apply_stats()
                        self.finish_job()
                        return
                else:
                    if check_lovers(char, hero):
                        char.set_flag("jobs_whoreintro", "%s obediently follows the order, even though she prefers to do it with you rather than with some stranger." % char.nickname)
                        char.set_flag("jobs_introjoy", -randint(5, 15))
                    elif "Nymphomaniac" in char.traits:
                        if char.disposition >= 600:
                            char.set_flag("jobs_whoreintro", "Even though she's not a whore, %s doesn't mind to have some fun sometimes, so she obeys you." % char.nickname)
                            char.set_flag("jobs_introjoy", randint(4, 8))
                            char.set_flag("jobs_introdis", -randint(5, 15))
                        else:
                            self.txt.append("%s is a slave so noone really cares but doing something that's not a part of her job has upset her a little bit." % char.nickname)
                            char.set_flag("jobs_introjoy", -randint(5, 15))
                    elif check_lovers(char, hero):
                        char.set_flag("jobs_whoreintro", "%s doesn't like the idea to do it with some stranger when she has a lover, but she likes you too much to complain." % char.nickname)
                        char.set_flag("jobs_introjoy", -randint(3, 10))
                    elif "Frigid" in char.traits:
                        char.set_flag("jobs_whoreintro", "%s will do as you command, but she will hate every second of it..." % char.nickname)
                        char.set_flag("jobs_introdis", -randint(15, 25))
                    else: 
                        char.set_flag("jobs_whoreintro", "%s will do as she is told, but doesn't mean that she'll be happy about." % char.nickname)
                        char.set_flag("jobs_introdis", -randint(15, 25))
            else:
                char.set_flag("jobs_whoreintro", choice(["{} is doing her shift as Prostitute:".format(char.name),
                                                                                "%s gets busy with a client:" % char.fullname,
                                                                                "Whore Job:"]))
            return True
               

                    
        def payout_mod(self):
            self.payout = 1
            
        def acts(self):
            # Pass the flags from occupation_checks:
            self.txt.append(self.worker.flag("jobs_whoreintro"))
            self.txt.append("\n\n")
            
            flag = self.worker.flag("jobs_introdis")
            if flag:
                self.loggs('disposition', flag)
                self.worker.del_flag("jobs_introdis")
                
            flag = self.worker.flag("jobs_introjoy")
            if flag:
                self.loggs('joy', flag)
                self.worker.del_flag("jobs_introjoy")
                
            
            width = 820
            height = 705
            
            size = (width, height)
            kwargs = dict(exclude=["rape", "angry", "in pain"], resize=size, type="reduce", add_mood=False)
            # Acts, Images, Tags and things Related:
            # Straight Sex Act
            if self.client.act == 'sex':
                
                self.skill = "vaginal"
                
                # Temporarily done here, should be moved to game init and after_load to improve performance:
                tags = (("2c vaginal", "ontop"), ("2c vaginal", "doggy"), ("2c vaginal", "missionary"), ("2c vaginal", "onside"), ("2c vaginal", "standing"), ("2c vaginal", "spooning"))
                act = self.get_act(tags)
                if act == tags[0]:
                    self.txt.append("He invited her to 'sit' on his lap as he unsheathed his cock. They've continued along the same lines in 'girl ontop' position. \n")
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[1]:
                    self.txt.append("He ordered %s to bend over and took her from behind. \n"%self.worker.nickname)
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[2]:
                    self.txt.append("He pushed %s on her back, shoved his cock in, screaming: 'Oh, Your pussy is wrapping around me so tight!' \n"%self.worker.nickname)
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[3]:
                    self.txt.append("%s lay on her side inviting the customer to fuck her. He was more than happy to oblige.\n"%self.worker.nickname)
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[4]:
                    self.txt.append("Not even bothering getting into a position, he took her standing up. \n")
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[5]:
                    self.txt.append("Customer felt cuddly so he spooned the girl until they both cummed. \n")
                    self.img = self.worker.show(*act, **kwargs)
                else:
                    self.txt.append(choice(['He wanted some old-fashioned straight fucking. \n',
                                                         'He was in the mood for some pussy pounding. \n',
                                                         'He asked for some playtime with her vagina.\n']))
                    self.img = self.worker.show("2c vaginal", **kwargs)
                # Virgin trait check:
                self.take_virginity()


            # Anal Sex Act
            elif self.client.act == 'anal':
                
                self.skill = "anal"
                
                self.txt.append(choice(["Anal sex is the best, customer thought... ",
                                                      "I am in the mood for a good anal fuck, customer said. ",
                                                      "Customer's dick got harder and harder just from the thought of %s's asshole! "%self.worker.nickname]))
                
                # Temporarely done here, should be moved to game init and after_load to improve performance:
                tags = (("2c anal", "ontop"), ("2c anal", "doggy"), ("2c anal", "missionary"), ("2c anal", "onside"), ("2c anal", "standing"), ("2c anal", "spooning"))
                act = self.get_act(tags)
                
                if act == tags[0]:
                    self.txt.append("He invited her to 'sit' on his lap as he unsheathed his cock. They've continued along the same lines in 'girl on top' position. \n")
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[1]:
                    self.txt.append("He ordered %s to bend over and took her from behind. \n"%self.worker.nickname)
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[2]:
                    self.txt.append("He pushed %s on her back, shoved his cock in, screaming: 'Oh, Your anus is wrapping around me so tight!' \n"%self.worker.nickname)
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[3]:
                    self.txt.append("%s lay on her side inviting the customer to fuck her. He was more than happy to oblige.\n"%self.worker.nickname)
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[4]:
                    self.txt.append("Not even bothering getting into a position, he took her standing up. \n")
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[5]:
                    self.txt.append("Customer felt cuddly so he spooned the girl until they both cummed. \n")
                    self.img = self.worker.show(*act, **kwargs)
                else:
                    self.txt.append(choice(['He took her in the ass right there and then. \n',
                                                          'He got his dose of it. \n',
                                                          'And so he took her in her butt. \n']))
                    self.img = self.worker.show("2c anal", **kwargs)
                
            # Suck a Dick act    
            elif self.client.act == 'blowjob':
                
                self.skill = "oral"
                
                tags = (('bc deepthroat'), ('bc handjob'), {"tags": ['bc footjob'], "dice": 80}, ('bc titsjob'), {"tags": ["after sex"], "dice": 10}, ("bc blowjob"))
                act = self.get_act(tags)
                
                if act == tags[0]:
                    self.txt.append(choice(["He shoved his cock all the way into her throat! \n", "Deepthroat is definitely my style, thought the customer... \n"]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[1]:
                    self.txt.append("He told %s to give him a good handjob.\n"%self.worker.nickname)
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[2]:
                    self.txt.append(choice(["He asked her for a foodjob.\n", "Footjob might be a weird fetish but that's what the customer wanted...\n"]))
                    self.img = self.worker.show(*act["tags"], **kwargs)                    
                elif act == tags[3]:
                    if trats["Big Boobs"] in self.worker.traits or traits["Abnormally Large Boobs"] in self.worker.traits:
                        self.txt.append(choice(["He went straight for her big boobs. \n", "Seeing her knockers, customer wanted notning else then to park his dick between them. \n", "Lustfully gazing on your girl's burst, he asked for a titsjob. \n", "He put his manhood between her big tits. \n" , "He showed his cock between %s's enormous breasts. \n"%self.worker.nickname]))
                    elif traits["Small Boobs"] in self.worker.traits:
                        if dice(7):
                            self.txt.append("With a smirk on his face, customer asked for a titsjob. He was having fun from her vain effords. \n")
                        else:    
                            self.txt.append(choice(["He placed his cock between her breasts, clearly enyoing her flat chest. \n", "Even when knowing that her breasts are small, he wanted to be carresed by them. \n"]))
                    else:
                        self.txt.append(choice(["He asked for a titsjob. \n", "He let %s to carres him with her breasts. \n", "He showed his cock between %s's tits. \n"%self.worker.nickname]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[4]:
                    self.txt.append(choice(["Customer wanted nothing else then to jerk himself in from of her and ejactuate on her face. \n", "He wanked himself hard in efford to cover her with his cum. \n"]))
                    self.img = self.worker.show(*act["tags"], **kwargs)        
                elif act == tags[5]:
                    self.txt.append(choice(['Client was in mood for some oral sex. \n', 'Client was in the mood for a blowjob. \n', 'He asked her to lick his dick. \n']))
                    self.img = self.worker.show(*act, **kwargs)
                else: # I do not thing that this will ever be reached...
                    self.txt.append(choice(['Client was in mood for some oral sex. \n', 'Client was in the mood for a blowjob. \n', 'He asked her to lick his dick. \n']))
                    self.img = self.worker.show("bc blowjob", **kwargs)

            # Lesbian Act
            elif self.client.act == 'lesbian':
                
                self.skill = "vaginal" # May be overwriten!...
                
                tags = (("gay", '2c lickpussy'),
                            ("gay", "bc lickpussy"),
                            ("gay", "2c lickanus"),
                            ("gay", "bc lickanus"),
                            ("gay", "2c vaginalfingering"),
                            ("gay", "bc vagnalhandjob"), # @Inconsistent tagnames!
                            ("gay", "2c analfingering"),
                            ("gay", "bc analhandjob"),  # @Inconsistent tagnames!
                            ("gay", "2c caresstits"),
                            ("gay", "bc caresstits"),
                            ("gay", "bc hug", "2c hug"),
                            ("gay", "2c vaginal"),
                            ("gay", "bc vaginal"),
                            ("gay", "2c anal"),
                            ("gay", "bc anal"),
                            ("gay", "2c vaginaltoy"),
                            ("gay", "bc toypussy"),  # @Inconsistent tagnames!
                            ("gay", "2c analtoy"),
                            ("gay", "bc toyanal"),  # @Inconsistent tagnames!
                            {"tags": ["gay"], "exclude": ["2c vaginal", "2c vaginaltoy"]}
                    )
                act = self.get_act(tags)
                # We'll be adding "les" here as Many lesbian pics do not fall in any of the categories and will never be called...
                # if self.worker.has_image("gay", "dildo joined"):
                    # acts.append("dildo joined")
                # if self.worker.has_image("gay", "anal beads"):
                    # acts.append("les_anal_beads")
                # if self.worker.has_image("gay", "do anal beads"):
                    # acts.append("les_do_anal_beads")
                    
                # act = choice(acts)

                # if act == "dildo joined":
                    # self.txt.append(choice(["She've asked your girl to lend her a double-ended dildo.\n",
                                                         # "She brought a twin-ended dildo for the party so %s could have some fun as well.\n"%self.worker.nickname]))
                    # self.img = self.worker.show("les", "dildo joined", resize=size)
                if act == tags[0]:
                    self.txt.append(choice(["Clearly in the mood for some cunt, she licked %ss pussy clean.\n"%self.worker.nickname,
                                                         "Hungry for a cunt, she told %s to be still and started licking her soft pussy with her hot tong. \n"%self.worker.nickname]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[1]:
                    self.txt.append(choice(["All hot and bothered, she ordered %s to lick her cunt. \n"%self.worker.nickname,
                                                         "As if she had an itch, she quickly told %s to tong her pussy. \n"%self.worker.nickname]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[2]:
                    self.txt.append(choice(["She licked %ss anus clean.\n"%self.worker.nickname,
                                                                                    "She told %s to be still and started licking her asshole with her hot tong. \n"%self.worker.nickname]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[3]:
                    self.txt.append(choice(["All hot and bothered, she ordered %s to lick her asshole. \n"%self.worker.nickname,
                                                         "As if she had an itch, she quickly told %s to tong her anus. \n"%self.worker.nickname]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[4]:
                    self.txt.append(choice(["In mood for a hot lesbo action, she stuck her fingers in your girls pussy. \n",
                                                         "She watched %s moan as she stuck fingers in her pussy. \n"%self.worker.nickname]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[5]:
                    self.txt.append(choice(["Quite horny, she ordered your girl to finger her cunt. \n",
                                                         "Clearly in the mood, she told %s to finger her until she cums. \n"%self.worker.nickname]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[6]:
                    self.txt.append(choice(["In mood for a hot lesbo action, she stuck her fingers in your girls anus. \n",
                                                         "She watched %s moan as she stuck fingers in her asshole. \n"%self.worker.nickname]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[7]:
                    self.txt.append(choice(["Quite horny, she ordered your girl to finger her anus. \n",
                                                         "Clearly in the mood, she told %s to finger her asshole until she cums. \n"%self.worker.nickname]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[8]:
                    self.txt.append(choice(["Liking your girls breasts, she had some good time caressing them. \n",
                                                         "She enjoyed herself by caressing your girls breasts. \n"]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[9]:
                    self.txt.append(choice(["She asked your girl to caress her tits. \n",
                                                         "She told your girl to put a squeeze on her breasts. \n"]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[10]:
                    self.txt.append(choice(["Girls lost themselves in eachothers embrace.\n",
                                                         "Any good lesbo action should start with a hug, don't you think??? \n"]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[11]:
                    self.txt.append(choice(["She put on a strapon and fucked your girl in her cunt. \n",
                                                          "Equipping herself with a strap-on, she lustfully shoved it in %ss pussy. \n"%self.worker.nickname]))
                    self.img = self.worker.show(*act, **kwargs)
                    self.take_virginity()
                elif act == tags[12]:
                    self.txt.append(choice(["She ordered %s to put on a strapon and fuck her silly with it. \n"%self.worker.nickname,
                                                          "She equipped %s with a strapon and told her that she was 'up' for a good fuck! \n"]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[13]:
                    self.txt.append(choice(["She put on a strapon and fucked your girl in her butt. \n",
                                                          "Equipping herself with a strapon, she lustfully shoved it in %ss asshole. \n"%self.worker.nickname]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[14]:
                    self.txt.append(choice(["She ordered %s to put on a strapon and butt-fuck her silly with it. \n"%self.worker.nickname,
                                                         "She equipped %s with a strapon and told her that she was 'up' for a good anal fuck! \n"]))
                    self.img = self.worker.show(*act, **kwargs)
                # elif act == "les_anal_beads":
                    # self.txt.append(choice(["They got their hands on some anal beads and shoved it up %ss butt. \n"%self.worker.nickname,
                                                          # "She had some fun with your girls asshole and some anal beads \n"]))
                    # self.img = self.worker.show("les", "anal beads", resize=size)
                # elif act == "les_do_anal_beads":
                    # self.txt.append(choice(["She had %s stick some anal beads up her butt. \n"%self.worker.nickname,
                                                         # "She told %s to get some anal beads to play with her anus. \n"%self.worker.nickname]))
                    # self.img = self.worker.show("les", "do anal beads", resize=size)
                elif act == tags[15]:
                    self.txt.append(choice(["She played with a dildo and %ss pussy. \n"%self.worker.nickname,
                                                         "She stuck a dildo up %s cunt. \n"%self.worker.nickname]))
                    self.img = self.worker.show(*act, **kwargs)
                    self.take_virginity()
                elif act == tags[16]:
                    self.txt.append(choice(["Without further ado, %s fucked her with a dildo. \n"%self.worker.nickname,
                                                         "She asked your girl to fuck her pussy with a dildo. \n"]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[17]:
                    self.txt.append(choice(["After some foreplay, she stuck a dildo up your girls butt. \n",
                                                                                   "For her money, she had some fun playing with a dildo and your girls asshole. \n"]))
                    self.img = self.worker.show(*act, **kwargs)
                elif act == tags[18]:
                    self.txt.append(choice(["After some foreplay, she asked %s to shove a dildo up her ass. \n"%self.worker.nickname,
                                                         "This female customer of your brothel clearly believed that there is no greater pleasure than a dildo up her butt. \n"]))
                    self.img = self.worker.show(*act, **kwargs)
                else:
                    self.txt.append(choice(["She was in the mood for some girl on girl action. \n", "She asked for a good lesbian sex. \n"]))
                    self.img = self.worker.show("gay", **kwargs)
                    # Last fallback!
            
            else:
                self.txt.append("Whore Job\n\nMissed All acts!\n\n")
                self.skill = "vaginal"
                self.img = self.worker.show("sex", **kwargs)
                
            self.check_skills(self.skill)
                
            # Take care of stats mods
            sexmod = 1 if dice(20) else 0
            constmod = 1 if dice(12) else 0
            self.loggs(self.skill, sexmod)
            self.loggs("constitution", constmod)
            self.loggs("vitality", -randint(18, 28))
            
            if sexmod + constmod > 0:
                self.txt.append("\n%s feels like she learned something! \n"%self.worker.name)
                self.loggs("joy", 1)
            
            # Dirt:
            self.logloc("dirt", randint(2, 5))
            
            # Log income for worker and MC
            self.txt.append("{color=[gold]}\nA total of %d Gold was earned!{/color}" % self.payout)
            self.worker.fin.log_wage(self.payout, "WhoreJob")
            self.loc.fin.log_work_income(self.payout, "WhoreJob")
            
            self.apply_stats()
            self.finish_job()
            
        def get_act(self, tags):
            acts = list()
            for t in tags:
                if isinstance(t, tuple):
                    if self.worker.has_image(*t):
                        acts.append(t)
                elif isinstance(t, dict):
                    if self.worker.has_image(*t.get("tags", []), exclude=t.get("exclude", [])) and dice(t.get("dice", 100)):
                        acts.append(t)
                
            if acts:
                act = choice(acts)
            else:
                act = None
                
            return act
            
        def take_virginity(self):
            if traits["Virgin"] in self.worker.traits:
                tips = 100 + self.worker.charisma * 3
                self.txt.append("\n{color=[pink]}%s lost her virginity!{/color} Customer thought that was super hot so she left a tip of {color=[gold]}%d Gold{/color} for your girl.\n\n"%(self.worker.nickname, tips))
                self.worker.remove_trait(traits["Virgin"])
                self.worker.fin.log_tips(tips, "WhoreJob")
                self.loc.fin.log_work_income(tips, "WhoreJob")
            
        def check_skills(self, skill=None):
            if not skill:
                skill = self.skill
            if skill > 300 and self.worker.charisma > 300:

                self.txt.append("The client was at your girls mercy. Her beauty enchanting, she playfully took him into her embrace and made him forget about the rest of the world until they were finished. \n")

                self.loggs("exp", randint(15, 25))
                self.loggs("joy", 3)
                
            elif 200 <= skill and 200 <= self.worker.charisma:
                
                self.txt.append("Your girl performed wonderfully with her breathtaking beauty and matching carnal skill. \n")

                self.loggs("exp", randint(15, 25))
                self.loggs("joy", 2)
                
            elif 80 <= skill and 80 <= self.worker.charisma:

                self.txt.append("Her well honed sexual skills and good looks both were pleasing to the customer. \n")

                self.loggs("exp", randint(15, 25))
                self.loggs("joy", 1)
                
            elif 30 <= skill and 30 <= self.worker.charisma:

                self.txt.append("Your girl did the job to the best of her ability but her skills could definitely be improved and her beauty enhanced. \n")

                self.loggs("exp", randint(15, 25))
                
            elif -100 <= skill <= 30 and -100 <= self.worker.charisma <= 30:

                self.txt.append("Your girl barely knew what she was doing. Her looks were not likely to be of any help to her either. \n")
                self.txt.append("Still, the customer explained that he preferred fucking her over a horse. Hearing that from him however, was not encouraging for your girl at all... \n")

                self.loggs("exp", randint(15, 25))
                self.loggs("joy", -2)
                
            elif skill < 30 and self.worker.charisma > 30:

                self.txt.append("A cold turkey sandwich would have made a better sex partner than her. Her performance was however saved by her somewhat pleasing looks. \n")

                self.loggs("exp", randint(15, 25))
                self.loggs("joy", -2)
                
            elif skill > 30 and self.worker.charisma < 30:

                self.txt.append("Her ability to please him sexually managed to help the client overlook the fact that she looked like a hag. \n")

                self.loggs("exp", randint(15, 25))
                self.loggs("joy", -1)
                
            else:
                self.txt.append('Dev Note: >>>I missed something!<<< Charisma = %d, Sex = %d \n'%(self.worker.charisma, skill))
               
            self.txt.append("\n")
    
    class AnalWhore(NewStyleJob):
        pass
    
    
    class StraightWhore(NewStyleJob):
        pass
    
    
    class GayWhore(NewStyleJob):
        pass
    
    
    ####################### Strip Job  ############################
    class StripJob(NewStyleJob):
        """
        Class for the solving of stripping logic.
        """
        def __init__(self):
            super(StripJob, self).__init__()
            self.id = "Striptease Job"
            
            # Traits/Job-types associated with this job:
            self.occupations = ["SIW"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Stripper"]] # Corresponing traits...
            
            # Relevant skills and stats:
            self.skills = ["strip"]
            self.stats = ["charisma"]
            
            self.workermod = {}
            self.locmod = {}
            
        def __call__(self, char):
            self.worker, self.loc = char, char.location
            self.clients = char.flag("jobs_strip_clients")
            self.strip()
            
        def check_occupation(self, char=None):
            """Checks if the worker is willing to do this job.
            """
            if not [t for t in self.all_occs if t in char.occupations]:
                if char.status != 'slave' and char.disposition > 800: # Free char with very high disposition.
                    char.set_flag("jobs_stripintro", "%s: I am not thrilled about having to dance in front of a bunch of pervs, but you've been really good to me so I owe you a favor... "%char.nickname)
                    char.set_flag("jobs_introdis", -randint(10, 15))
                    char.set_flag("jobs_introjoy", -randint(3, 6))
                
                elif char.status != 'slave':
                    temp = choice(["%s refuses to do work as a Stripper!"%char.nickname,
                                             "Stripping? You're kidding me right?",
                                             "Find someone else to strip for those perves!"])
                    temp = set_font_color(temp, "red")
                    self.txt.append(temp)
                    
                    self.worker = char
                    self.loc = char.location
                    self.event_type = "jobreport"
                    
                    self.loggs('disposition', -50)
                    self.img = char.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")
                    char.action = None
                    
                    self.apply_stats()
                    self.finish_job()
                    return False
                    
                else:
                    char.set_flag("jobs_stripintro", choice(["%s is a slave so she'll do as she's told. Doesn't mean that she's happy about it... \n"%char.name,
                                                                                 "Being a slave, %s had no choice but to do as she's told."%char.name,
                                                                                 "Even though %s is a slave and will do as she's told, consider giving poor girl a task better suited to her profession."%char.name]))
                    char.set_flag("jobs_introjoy", -randint(5, 10))
            
            else:
                char.set_flag("jobs_stripintro", choice(["{} is doing her thing as a Stripper:".format(char.fullname),
                                                                             "{} works as a Stripper:".format(char.fullname),
                                                                             "Striptease Job:"]))
            return True
        
        def strip(self):
            # Pass the flags from occupation_checks:
            self.txt.append(self.worker.flag("jobs_stripintro"))
            self.txt.append("\n\n")
            
            flag = self.worker.flag("jobs_introdis")
            if flag:
                self.loggs('disposition', flag)
                self.worker.del_flag("jobs_introdis")
                
            flag = self.worker.flag("jobs_introjoy")
            if flag:
                self.loggs('joy', flag)
                self.worker.del_flag("jobs_introjoy")
            
            len_clients = len(self.clients)
            tippayout = self.worker.flag("jobs_" + self.id + "_tips")
            cl_strip = 0
            cl_char = 0
            stripskill = self.worker.get_skill("strip")
            charisma = self.worker.charisma
            
            for c in self.clients:
                # We get the highest skills a character has to match vs strip skill, assumption is that proffessional can appriciate another profi :)
                cl_strip = cl_strip + max(list(getattr(c, s + "skill") for s in c.stats.skills))
                cl_char = cl_char + c.charisma
            cl_strip = cl_strip / len_clients
            cl_char = cl_char / len_clients
            
            if stripskill > cl_strip*1.5 and charisma > cl_char*1.5:
                self.txt.append("{} gave a performance worthy of kings and queens as the whole hall was cheering for her. \n".format(self.worker.name))
                self.loggs('joy', 3)
            elif cl_strip*1.3 <= stripskill and cl_char*1.3 <= charisma:
                self.txt.append("Your girl lost all of her clothing piece by piece as she stripdanced on the floor, the whole hall was cheering for her. \n")
                self.loggs('joy', 2)
            elif cl_strip*1.15 <= stripskill and cl_char*1.15 <= charisma:
                self.txt.append("Your girl lost all of her clothing piece by piece as she stripdanced on the floor, the whole hall was cheering for her. "+ \
                                         "Overall it was a more than decent performance.  \n")
                self.loggs('joy', 1)
            elif cl_strip <= stripskill and cl_char <= charisma:
                self.txt.append("Your girl lost all of her clothing piece by piece as she stripdanced on the floor, some mildly drunk clients cheered for her. Overall it was a decent performance. \n")
            elif 0 <= stripskill <= cl_strip and 0 <= charisma <= cl_char:
                self.txt.append("%s certainly did not shine as she clumsily 'danced' on the floor. Neither her looks nor her skill could save the performance... "%self.worker.nickname + \
                                        "calls for a different stripper could be heard from all over the club! ")
                self.loggs('joy', -2)
            elif stripskill < cl_strip and charisma > cl_char:
                self.txt.append("Your girl tripped several times while trying to undress herself as she 'stripdanced' on the floor, noone really complained because even if her skill was inadequate, " + \
                                        "she was pretty enough to arouse most men and women in the club. Overall it was a decent performance. \n")
                self.loggs('joy', -1)
            elif stripskill > cl_strip and charisma < cl_char:
                self.txt.append("%s may not be the prettiest girl in town but noone really complained because what she lacked in looks, she made up in skill. "%self.worker.name + \
                                        "Overall it was a decent performance. \n")
                self.loggs('joy', -1)
            else:
                self.txt.append('Dev Note: >>>I missed something!<<< Charisma = %d, Strip = %d \n'%(charisma, stripskill))
            
            self.txt.append("\n")
            
            # Girl
            if dice(25):
                self.loggs('charisma', 1)
                self.txt.append("\nYour workers charisma increased as she learned a new trick on how to make herself pretty before the show! \n")
            
            if dice(35):
                self.loggs('strip', 1)
            
            self.loggs('reputation', choice([0, 0, 0, 0, 0, 1, 0]) + int(round(0.01 * charisma)) + int(round(0.005 * stripskill)))
            self.loggs('fame', choice([0, 0, 1, 1, 0, 0, 0]) + int(round(0.02 * charisma)) + int(round(0.02 * stripskill)))
            self.loggs('agility', choice([0, 0, 0, 1]))
            self.loggs('vitality', randrange(-31, -15))
            
            # Finances:
            self.worker.fin.log_tips(tippayout, "StripJob")
            self.loc.fin.log_work_income(tippayout, "StripJob")
            
            available = list()
            kwargs = dict(exclude=["sad", "angry", "in pain"], resize=(740, 685), type="first_default", add_mood=False)
            if self.worker.has_image("stripping", "stage", exclude=["sad", "angry", "in pain"]):
                available.append("stage")
            if self.worker.has_image("stripping", "simple bg", exclude=["sad", "angry", "in pain"]):
                available.append("simple bg")
            if self.worker.has_image("stripping", "no bg", exclude=["sad", "angry", "in pain"]):
                available.append("no bg")
            if available:
                self.img = self.worker.show("stripping", choice(available), **kwargs)
            elif self.worker.has_image("stripping", "indoors"):
                self.img = self.worker.show("stripping", "indoors", **kwargs)
            else:
                self.img = self.worker.show("stripping", **kwargs)
                
            self.event_type = "jobreport"
            self.kind = self.id
            self.apply_stats()
            self.finish_job()
        
    
    ####################### Rest Job  #############################
    class Rest(NewStyleJob):
        """Resting for character, technically not a job...
        """
        def __init__(self):
            """
            Creates a new Rest.
            worker = The girl to solve for.
            """
            super(Rest, self).__init__()
            self.id = "Rest Job"
                
        def __call__(self, char):
            self.worker = char
            self.loc = self.worker.home
            self.rest()
            self.after_rest()
            
        def rest(self):
            """Rests the worker.
            """
            # Stat Mods:

                                                 
            available = list()
            if (self.worker.disposition >= 250) or ("Exhibitionist" in self.worker.traits):
                kwargs = dict(exclude=["dungeon", "sad", "angry", "in pain", "after sex", "group", "normalsex", "bdsm"], add_mood=False) # with not too low disposition nude pics become available during rest
            else:
                kwargs = dict(exclude=["dungeon", "sad", "nude", "angry", "in pain", "after sex", "group", "normalsex", "bdsm"], add_mood=False)
            if self.worker.has_image("sleeping", **kwargs):
                available.append("sleeping")
            if self.worker.has_image("reading", **kwargs):
                available.append("reading")
            if self.worker.vitality > 50:
                if self.worker.has_image("shopping", **kwargs) and (self.worker.gold >= 200): # eventually there should be a real existing event about going to shop and buy a random item there for gold. after all we do have an algorithm for that. but atm it might be broken, so...
                    available.append("shopping")
                if "Nymphomaniac" in self.worker.traits and self.worker.disposition >= 300: # if we'll have some kind of high libido flags, they could be used here too
                    if self.worker.has_image("masturbation", **kwargs):
                        available.append("masturbation")
            if self.worker.vitality > 150:
                if self.worker.has_image("sport", **kwargs):
                    available.append("sport")
                if self.worker.has_image("exercising", **kwargs):
                    available.append("exercising")
            if self.worker.has_image("eating", **kwargs):
                available.append("eating")
            if self.worker.has_image("bathing", **kwargs):
                available.append("bathing")
            if self.worker.has_image("rest", **kwargs):
                available.append("rest") # there always will be a simple rest, providing non-empty list. The only exception is a lack of any non nude pics, in which case we will allow to them with any disposition
            if not(available):
                if self.worker.has_image("rest"):
                    available.append("rest")
                else:
                    available.append("profile", exclude=["sad", "angry", "in pain"]) # no rest at all? c'mon...
            
            if ("sleeping" in available) and (self.worker.vitality <= 50):
                    self.img = self.worker.show("sleeping", resize=(740, 685), **kwargs)
                    self.txt.append("{} is too tired to do anything but sleep at her free time.".format(self.worker.name))
            else:
                self.img = self.worker.show(choice(available), resize=(740, 685), **kwargs)
                image_tags = self.img.get_image_tags()
                if "sleeping" in image_tags:
                    if "living" in image_tags:
                        self.txt.append("{} is enjoying additional bedtime in her room.".format(self.worker.name))
                    elif "beach" in image_tags:
                        self.txt.append("{} takes a small nap at the local beach.".format(self.worker.name))
                    elif "nature" in image_tags:
                        self.txt.append("{} takes a small nap in the local park.".format(self.worker.name))
                    else:
                        self.txt.append("{} takes a small nap during her free time.".format(self.worker.name))
                elif "masturbation" in image_tags:
                    self.txt.append(choice(["{} has some fun with herself during her free time.".format(self.worker.name),
                                                 "{} is relieving her sexual tension at free time.".format(self.worker.name)]))
                elif "onsen" in image_tags:
                    self.txt.append("{} relaxes in the onsen. The perfect remedy for stress!".format(self.worker.name))
                elif "reading" in image_tags:
                    self.txt.append(choice(["{} spends her free time reading.".format(self.worker.name),
                                                 "{} is enjoying a book and relaxing.".format(self.worker.name)]))
                elif "shopping" in image_tags:
                    self.txt.append(choice(["{} spends her free time to visit some shops.".format(self.worker.name),
                                                 "{} is enjoying a small shopping tour.".format(self.worker.name)]))
                elif "exercising" in image_tags:
                    self.txt.append("{} keeps herself in shape doing some exercises during her free time.".format(self.worker.name))
                elif "sport" in image_tags:
                    self.txt.append("{} is in a good shape today, so she spends her free time doing sports.".format(self.worker.name))
                elif "eating" in image_tags:
                    self.txt.append(choice(["{} has a snack during her free time.".format(self.worker.name),
                                                 "{} spends her free time enjoying a meal.".format(self.worker.name)]))
                elif "bathing" in image_tags:
                    if "pool" in image_tags:
                        self.txt.append("{} spends her free time enjoying swimming in the local swimming pool.".format(self.worker.name))
                    elif "beach" in image_tags:
                        self.txt.append("{} spends her free time enjoying swimming at the local beach. The water is great today!".format(self.worker.name))
                    elif "living" in image_tags:
                        self.txt.append("{} spends her free time enjoying a bath.".format(self.worker.name))
                    else:
                        self.txt.append("{} spends her free time relaxing in a water.".format(self.worker.name))
                else:
                    if "living" in image_tags:
                        self.txt.append(choice(["{} is resting in her room.".format(self.worker.name),
                                                 "{} is taking a break in her room to recover.".format(self.worker.name)]))
                    elif "beach" in image_tags:
                            self.txt.append(choice(["{} is relaxing at the local beach.".format(self.worker.name),
                                                    "{} is taking a break at the local beach.".format(self.worker.name)]))
                    elif "pool" in image_tags:
                            self.txt.append(choice(["{} is relaxing in the local swimming pool.".format(self.worker.name),
                                                    "{} is taking a break in the local swimming pool.".format(self.worker.name)]))
                    elif "nature" in image_tags:
                        if ("wildness" in image_tags):
                            self.txt.append(choice(["{} is resting in the local forest.".format(self.worker.name),
                                                    "{} is taking a break in the local forest.".format(self.worker.name)]))
                        else:
                            self.txt.append(choice(["{} is resting in the local park.".format(self.worker.name),
                                                    "{} is taking a break in the local park.".format(self.worker.name)]))
                    elif ("urban" in image_tags) or ("public" in image_tags):
                            self.txt.append(choice(["{} is relaxing somewhere in the city.".format(self.worker.name),
                                                    "{} is taking a break somewhere in the city.".format(self.worker.name)]))
                    else:
                            self.txt.append(choice(["{} is relaxing during her free time.".format(self.worker.name),
                                                    "{} is taking a break during her free time.".format(self.worker.name)]))
            while self.worker.AP and not all([(self.worker.vitality + self.workermod.get('vitality', 0) >= self.worker.get_max("vitality") - 50),
                                                          (self.worker.health + self.workermod.get('health', 0) >= self.worker.get_max('health') - 5)]):
                self.loggs('health', randint(2, 3))
                self.loggs('vitality', randint(35, 40))
                self.loggs('mp', randint(1, 3))
                self.loggs('joy', randint(1, 2))
                self.loggs('libido', randint(1, 3))
                self.worker.AP -= 1
            
            if not self.img:
                self.img = self.worker.show("rest", resize=(740, 685))
                
        def is_rested(self):
            if (self.worker.vitality >= self.worker.get_max("vitality") - 50) and (self.worker.health >= self.worker.get_max('health') - 5):
                return True
        
        def after_rest(self):
            """
            Solve the final logic.
            """
            self.apply_stats()
            
            if self.is_rested():
                self.txt.append("\n\nShe is both well rested and healthy so at this point this is simply called: {color=[red]}slacking off :){/color}")
            
            self.finish_job()
            
    class AutoRest(Rest):
        """
        Same as Rest but game will try to reset character to it's previos job.
        """
        def __init__(self):
            super(AutoRest, self).__init__()
            self.id = "Auto Rest"
        
        def after_rest(self):
            """
            Solve the final logic.
            """
            self.apply_stats()
            
            if self.is_rested():
                self.txt.append("\n\nShe is now both well rested and healthy, so she goes back to work as %s!" % self.worker.previousaction)
                self.worker.action = self.worker.previousaction
                self.worker.previousaction = None
                
                if self.worker.autoequip:
                    # **Adapt to new code structure...
                    equip_for(self.worker, self.worker.action)
            
            self.finish_job()
    
    ####################### Service Job  ##########################
    class TestingJob(NewStyleJob):
        """
        Very Simple job that can be used for testing or as a "Blue Print"
        """
        def __init__(self):
            super(TestingJob, self).__init__()
            self.id = "Testing Job"
        
        def __call__(self, char, client):
            # Basic job that takes 1 AP of a girl, removes client from queue and adds random stats/skills.
            # Next thing is to make this work with Rest Job!
            self.reset()
            
            self.event_type = "jobreport"
            self.worker, self.loc = char, char.location
            
            self.client = client
            
            char, cl = self.worker, self.client
            
            self.loggs("charisma", randint(1, 3))
            self.loggs("Refinement", randint(1, 3))
            self.loggs("refinement", randint(1, 3))
            self.loggs("strip", randint(1, 3))
            
            char.AP -= 1
            self.loggs("vitality", 35)
            
            self.logloc("dirt", 10)
            
            self.txt.append("Test Job Report: Girl: {}, Location: {}".format(char.name, self.loc.name))
            self.img = "nude"
            
            self.apply_stats()
            self.finish_job()
            
        def get_clients(self):
            # This is never called since we know that it is a one client job without variations.
            return 1
            
            
    class Waiting(NewStyleJob):
        def __init__(self):
            super(Waiting, self).__init__()
            self.id = "Waiting Job"
            
            # Traits/Job-types associated with this job:
            self.occupations = [] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [] # Corresponing traits...
            
            # Relevant skills and stats:
            self.skills = []
            self.stats = []
            
            self.workermod = {}
            self.locmod = {}
        
        def __call__(self, char):
            pass
            
        def club_task(self):
            """
            Solve the job as a waitress.
            """
            clientsmax = self.APr * (2 + (self.worker.agility * 0.05 + self.worker.serviceskill * 0.05 + self.worker.refinement * 0.01))
            
            if self.loc.servicer['clubclientsleft'] - clientsmax <= 0:
                clientsserved = self.loc.servicer['clubclientsleft']
                self.txt.append("She finished serving drinks and snacks to tables of %d remaining customers. At least she got a break.  \n"%self.loc.servicer['clubclientsleft'])
                self.loc.servicer['clubclientsleft'] -= clientsserved
            
            elif self.loc.servicer['clubclientsleft'] - clientsmax > 0:
                clientsserved = clientsmax
                self.txt.append("She served snacks and drinks to tables of %d clients. \n"%(clientsmax))
                self.loc.servicer['clubclientsleft'] = self.loc.servicer['clubclientsleft'] - clientsserved
            
            clubfees = clientsserved * self.loc.rep * 0.08 + clientsserved * 0.5 * (self.worker.refinement * 0.1 + self.worker.charisma * 0.1 + self.worker.service * 0.025)
            tips = 0
            
            self.txt.append("\n")
            
            # Skill Checks
            if self.worker.serviceskill > 2000:
                self.locmod['reputation'] += choice([0, 1])
                clubfees = clubfees * 1.5
                tips = clubfees * 0.10
                self.txt.append("She is an exellent waitress, customers didn't notice how they've just kept spending their money as she offered them more and more house specials. \n")
            
            elif self.worker.serviceskill >= 1000:
                self.locmod['reputation'] += choice([0,0,0,1])
                clubfees = clubfees * 1.2
                tips = clubfees * 0.07
                self.txt.append("Customers were pleased with such a skilled waitress serving them. \n")
            
            elif self.worker.serviceskill >= 500:
                tips = clubfees * 0.03
                self.locmod['reputation'] += choice([0,0,0,0,0,1])
                self.txt.append("She was skillful enough not to mess anything up during her job. \n")
            
            elif self.worker.serviceskill >= 100:
                self.locmod['reputation'] += choice([0,0,-1,0,0,-1])
                clubfees = clubfees * 0.8
                self.txt.append("Her performance was rather poor and it most definitely has cost you income. \n")
            
            if self.worker.charisma > 300:
                tips = tips + clubfees*0.05
                self.locmod['fame'] += choice([0, 1, 1])
                self.workermod['fame'] += choice([0, 0, 1])
                self.txt.append("Your girl was stunningly pretty, customers couldn't keep their eyes off her. \n")
            
            elif self.worker.charisma > 150:
                tips = tips + clubfees*0.03
                self.locmod['fame'] += choice([0 ,0, 1])
                self.workermod['fame'] +=  choice([0, 0, 0, 1])
                self.txt.append("Your girl looked beautiful, this will not go unnoticed. \n")
            
            elif self.worker.charisma > 45:
                tips = tips + clubfees*0.02
                self.locmod['fame'] += choice([0, 0, 0, 1])
                self.workermod['fame'] +=  choice([0, 0, 0, 0, 1])
                self.txt.append("Your girl was easy on the eyes, not bad for a bartender. \n")
            
            elif self.worker.charisma > 0:
                self.locmod['fame'] += choice([0, -1, -1])
                self.workermod['fame'] +=  choice([0, 0, -1])
                self.txt.append("Customers did not appreciate a hag serving them. Consider sending this girl to a beauty school. \n")
            
            self.txt.append("\n")
            
            # Stat Mods
            self.workermod['vitality'] -= clientsserved * 5
            self.workermod['service'] += choice([0, 0, 1]) * self.APr
            self.workermod['agility'] += choice([0, 0, 1]) * self.APr
            self.workermod['exp'] += self.APr * randint(15, 25)
            
            self.locmod['dirt'] += clientsserved * 6
            
            # Integers:
            clubfees = int(round(clubfees))
            tips = int(round(tips))
            
            self.txt.append("{color=[gold]}%s earned %d Gold during this shift"%(self.worker.nickname, clubfees))
            
            if tips:
                self.txt.append(" and got %d in tips" % tips)
            
            self.txt.append(".{/color}\n")
            
            self.img = self.worker.show("bunny", "waitress", exclude=["sex"], resize=(740, 685), type="any")
            
            # Finances:
            self.worker.fin.log_wage(clubfees, "Waitress")
            self.worker.fin.log_tips(tips, "Waitress")
            self.loc.fin.log_work_income(clubfees + tips, "Waitress")
            
            self.apply_stats()
            self.finish_job()
    
    class BarJob(NewStyleJob):
        def __init__(self):
            super(BarJob, self).__init__()
            self.id = "Bartending"
            
            # Traits/Job-types associated with this job:
            self.occupations = ["Server"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Bartender"]] # Corresponing traits...
            
            # Relevant skills and stats:
            self.skills = ["bartending"]
            self.stats = ["charisma"]
            
            self.workermod = {}
            self.locmod = {}
            
        def __call__(self, char):
            self.worker, self.loc = char, char.location
            self.clients = char.flag("jobs_bar_clients")
            self.bar_task()
            
        def check_occupation(self, char):
            """Checks the workers occupation against the job.
            """
            if not [t for t in self.all_occs if t in char.occupations]:
                if char.status == 'slave':
                    temp = choice(["%s has no choice but to agree to tend the bar."%char.fullname,
                                            "She'll tend the bar for customer, does not mean she'll enjoy it.",
                                            "%s is a slave so she'll do as she is told. However you might want to concider giving her work fit to her profession."%char.name])
                    char.set_flag("jobs_barintro", temp)
                    char.set_flag("jobs_introjoy", -3)
                
                elif self.worker.disposition < 800:
                    temp = choice(["%s refused to serve! It's not what she wishes to do in life."%char.name,
                                             "%s will not work as a Service Girl, find better suited task for her!"%char.fullname])
                    temp = set_font_color(temp, "red")
                    self.txt.append(temp)
                    
                    self.worker = char
                    self.loc = char.location
                    self.event_type = "jobreport"
                    
                    self.loggs('disposition', -50)
                    self.img = char.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")
                    char.action = None
                    
                    self.apply_stats()
                    self.finish_job()
                    return False
                
                else: # self.worker.disposition > 800:
                    temp = "%s reluctently agreed to be a servicer. It's not what she wishes to do in life but she admires you to much to refuse. " % char.name
                    char.set_flag("jobs_barintro", temp)
            
            else:
                temp = choice(["%s will work as a Bartender!"%char.name,
                                         "Tending the Bar:"])
                char.set_flag("jobs_barintro", temp)
            return True
            
        def bar_task(self):
            # Pass the flags from occupation_checks:
            self.txt.append(self.worker.flag("jobs_barintro"))
            self.txt.append("\n\n")
            
            flag = self.worker.flag("jobs_introdis")
            if flag:
                self.loggs('disposition', flag)
                self.worker.del_flag("jobs_introdis")
                
            flag = self.worker.flag("jobs_introjoy")
            if flag:
                self.loggs('joy', flag)
                self.worker.del_flag("jobs_introjoy")
                
            # Old Code:
            # beer = self.loc.get_upgrade_mod("bar") == 2
            # tapas = self.loc.get_upgrade_mod("bar") == 3
            # clientsmax = self.APr * (4 + (self.worker.agility * 0.1 + self.worker.serviceskill * 0.08))
            # clients = plural("customer", clientsmax)
            # if self.loc.servicer['barclientsleft'] - clientsmax <= 0:
                # clientsserved = self.loc.servicer['barclientsleft']
                # if tapas:
                    # self.txt.append("Your girl finished serving cold beer and tasty snacks to customers for the day! She even managed a small break at the end of her shift! \n")
                # elif beer:
                    # self.txt.append("Remaining bar customers enjoyed cold draft beer. %s got a little break at the end of her shift! \n"%self.worker.nickname)
                # else:
                    # self.txt.append("Your girl wrapped up the day at the bar by serving drinks to %d remaining customers. At least she got a small break.  \n"%self.loc.servicer['barclientsleft'])
                # self.loc.servicer['barclientsleft'] = 0
                # self.workermod['vitality'] += self.APr * randint(1, 5)
            
            # elif self.loc.servicer['barclientsleft'] - clientsmax > 0:
                # clientsserved = clientsmax
                # if tapas:
                    # self.txt.append("She served cold draft beer and mouthwatering snacks to %d %s. \n"%(clientsmax, clients))
                # elif beer:
                    # self.txt.append("She served cold and refreshing tapbeer to %d %s. \n"%(clientsmax, clients))
                # else:
                    # self.txt.append("She served snacks and drinks at the bar to %d %s. \n" % (clientsmax, clients))
                # self.loc.servicer['barclientsleft'] = self.loc.servicer['barclientsleft'] - clientsserved
                # self.workermod['vitality'] -= 4 * clientsmax
            
            len_clients = len(self.clients)
            
            serviceskill = self.worker.get_skill("bartending")
            charisma = self.worker.charisma
            
            # Skill checks
            if serviceskill > 2000:
                self.logloc('reputation', choice([0, 1, 2]))
                self.txt.append("She was an excellent bartender, customers kept spending their money just for the pleasure of her company. \n")
            
            elif serviceskill >= 1000:
                self.logloc('reputation', choice([0, 1]))
                self.txt.append("Customers were pleased with her company and kept asking for more booze. \n")
            
            elif serviceskill >= 500:
                self.logloc('reputation', choice([0, 0, 0, 0, 0, 1]))
                self.txt.append("She was skillful enough not to mess anything up during her job. \n")
            
            elif serviceskill >= 100:
                self.logloc('reputation', -1)
                self.txt.append("Her performance was rather poor and it most definitely has cost you income. \n")
            
            else:
                self.logloc('reputation', -2)
                self.txt.append("She is a very unskilled bartender, this girl definitely needs training \n")
                
            if charisma > 300:
                self.logloc('fame', choice([0,1,1]))
                self.loggs('fame', choice([0,0,1]))
                self.txt.append("Your girl was stunningly pretty, customers couldn't keep their eyes off her. \n")
            
            elif charisma > 150:
                self.logloc('fame', choice([0,0,1]))
                self.loggs('fame', choice([0,0,0,1]))
                self.txt.append("Your girl looked beautiful, this will not go unnoticed. \n")
            
            elif charisma > 45:
                self.logloc('fame', choice([0, 0, 0, 1]))
                self.loggs('fame',  choice([0, 0, 0, 0, 1]))
                self.txt.append("Your girl was easy on the eyes, not bad for a bartender. \n")
            
            else:
                self.logloc('fame', -2)
                self.loggs('fame', -2)
                self.txt.append("Customers did not appreciate a hag serving them. Consider sending this girl to a beauty school. \n")
            
            self.txt.append("\n")
            
            #Stat Mods
            self.loggs('exp', randint(15, 25))
            self.loggs('bartending', choice([0, 0, 1]))
            self.loggs('refinement', choice([0, 0, 0, 0, 1]))
            self.loggs('vitality', len_clients * 3)
            
            # Integers:
            # barfees = int(round(self.worker.earned_cash))
            tips = int(round(self.worker.flag("jobs_" + self.id + "_tips")))
            
            if tips:
                self.txt.append("She got %d in tips! " % tips)
            
            if self.worker.has_image("waitress", exclude=["sex"]):
                self.img = self.worker.show("waitress", exclude=["sex"], resize=(740, 685))
            elif self.worker.has_image("maid", exclude=["sex"]):
                self.img = self.worker.show("maid", exclude=["sex"], resize=(740, 685))
            else:
                self.img = self.worker.show("profile", exclude=["sex", "nude"], resize=(740, 685))
            
            # Finances:
            # self.worker.fin.log_wage(barfees, "Barmaid")
            if tips:
                self.worker.fin.log_tips(tips, "Barmaid")
            
            self.loc.fin.log_work_income(tips, "Barmaid")
            
            self.apply_stats()
            self.finish_job()
    
    
    class Cleaning(NewStyleJob):
        def cleaning_task(self):
            """
            Solve the job as a cleaner.
            """
            if self.task == 'Cleaning':
                # Stats checks
                cleffect = int(round(self.APr * (12 + self.worker.serviceskill * 0.025 + self.worker.agility * 0.3)))
                
                if self.loc.dirt - cleffect <= 0:
                    self.txt.append("She finished cleaning the building and took a break for the remaining time. \n")
                    self.workermod['joy'] += choice([0, 0, 1])
                
                elif self.loc.dirt - cleffect > 0:
                    self.txt.append("She spent a good amount of time cleaning the building so workers and customers would be happy. \n")
                
                self.img = self.worker.show("maid", "cleaning", exclude=["sex"], resize=(740, 685), type="any")
                
                # Stat mods
                self.locmod['dirt'] -= cleffect
                self.workermod['vitality'] -= randint(15, 25) * self.APr
                self.workermod['exp'] += self.APr * randint(15, 25)
                self.workermod['service'] += choice([0,0,1])
                
                self.apply_stats()
                self.finish_job()
    

    class ServiceJob(NewStyleJob):
        """The class that solves Bartending, Waitressing and Cleaning.
        
        TODO: Rewrite to work with SimPy! *Or this actually should prolly be split into three Jobs...
        """
        def __init__(self):
            """
            This is meant to pick a job that makes most sence out if Cleaning, Service and Bartending
            """
            super(ServiceJob, self).__init__()
            
            # Traits/Job-types associated with this job:
            self.occupations = ["Server"] # General Strings likes SIW, Warrior, Server...
            # self.occupation_traits = [traits["Service"]] # Corresponing traits...
            
        def __call__(self, char, loc):
            self.worker, self.loc = char, loc
            
            self.task = None # Service task
            
            # Get the ap cost and cash it
            if self.worker.AP >= 2:
                aprelay = choice([1, 2])
                self.APr = aprelay
                self.worker.AP -= aprelay
            else:
                self.APr = self.worker.AP 
                self.worker.AP = 0
                
            self.workermod = {}
            self.locmod = {}
            
            # tl.timer("Life/Injury/Vitality")
            self.check_life()
            if not self.finished: self.check_injury()
            if not self.finished: self.check_vitality()
            # tl.timer("Life/Injury/Vitality")
            
            # tl.timer("Occupation")
            if not self.finished: self.check_occupation()
            # tl.timer("Occupation")
            
            # tl.timer("Client Relay")
            if not self.finished: self.client_relay()
            # tl.timer("Client Relay")
            
            # tl.timer("Setting task")
            if not self.finished: self.set_task()
            # tl.timer("Setting task")
            
            # tl.timer("Bar")
            if self.task == "Bar" and not self.finished: self.bar_task()
            # tl.timer("Bar")
            
            # tl.timer("Club")
            if self.task == 'Club' and not self.finished: self.club_task()
            # tl.timer("Club")
            
            # tl.timer("Clean")
            if not self.finished: self.cleaning_task()
            # tl.timer("Clean")
        
        def check_occupation(self):
            """Checks the workers occupation against the job.
            """
            if [t for t in self.all_occs if t in self.worker.occupations]:
                if self.worker.status == 'slave':
                    self.txt.append(choice(["%s has no choice but to agree to clean and serve tables."%self.worker.fullname,
                                                        "She'll clean and tend to customer needs for you, does not mean she'll enjoy it.",
                                                        "%s is a slave so she'll do as she is told. However you might want to concider giving her work fit to her profession."%self.worker.name]))
                    
                    self.loggs("joy", -3) 
                
                elif self.worker.disposition < 700:
                    self.txt.append(choice(["%s refused to serve! It's not what she wishes to do in life."%self.worker.name,
                                            "%s will not work as a Service Girl, find better suited task for her!"%self.worker.fullname]))
                    
                    self.loggs('disposition', -50)
                    self.img = self.worker.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")
                    
                    self.worker.action = None
                    self.apply_stats()
                    self.finish_job()
                
                else:
                    self.txt.append("%s reluctently agreed to be a servicer. It's not what she wishes to do in life but she admires you to much to refuse. "%self.worker.name)
            
            else:
                self.txt.append(choice(["%s will work as a service girl!"%self.worker.name,
                                        "Cleaning, cooking, bartending...",
                                        "%s will clean or tend to customers next!"%self.worker.fullname]))
                
            if isinstance(self.txt, list):
                self.txt.append("\n")
        
        def set_task(self):
            """
            Sets the task for the girl.
            """
            if self.loc.servicer['second_round']:
                if not self.worker.autocontrol['S_Tasks']['clean']:
                    self.txt.append("%s will not clean (check her profile for more information)." % self.worker.nickname)
                    self.img = 'profile'
                    self.apply_stats()
                    self.workers.remove(self.worker)
                    self.finish_job()
                elif self.loc.dirt > 0:
                    self.task = "Cleaning"
                else:
                    self.workers.remove(self.worker)
            
            elif self.loc.get_dirt_percentage()[0] > 80 and not self.worker.autocontrol['S_Tasks']['clean']:
                if self.loc.auto_clean:
                    self.auto_clean()
                    if self.loc.get_dirt_percentage()[0] <= 80:
                        self.set_task()
                        return
                    else:
                        self.txt.append("%s doesn't clean and you do not have the fund to pay proffesional cleaners!" % self.worker.nickname)
                        self.img = 'profile'
                        self.apply_stats()
                        self.workers.remove(self.worker)
                        self.finish_job()
                        return
                        
                elif self.worker.autocontrol['S_Tasks']['clean']:
                    self.txt.append("Your brothel was too dirty for any task but cleaning!")
                    self.task = "Cleaning"
            
            elif self.loc.servicer['barclientsleft'] > 0 or self.loc.servicer['clubclientsleft'] > 0:
                if self.loc.servicer['barclientsleft'] > 0 and self.loc.servicer['clubclientsleft'] > 0:
                    if self.worker.autocontrol['S_Tasks']['bar'] and self.worker.autocontrol['S_Tasks']['waitress']:
                        self.task = choice(['Bar', 'Club'])
                elif self.loc.servicer['barclientsleft'] > 0 and self.worker.autocontrol['S_Tasks']['bar']:
                    self.task = "Bar"
                elif self.loc.servicer['clubclientsleft'] > 0 and self.worker.autocontrol['S_Tasks']['waitress']:
                    self.task = "Club"
                elif self.loc.dirt > 0 and self.worker.autocontrol['S_Tasks']['clean']:
                    self.task = "Cleaning"
                else:
                    self.txt.append("There were no tasks remaining or this girl is not willing to do them (check her profile for more info).")
                    self.img = 'profile'
                    self.apply_stats()
                    self.workers.remove(self.worker)
                    self.finish_job()
            
            elif self.loc.dirt > 0 and self.worker.autocontrol['S_Tasks']['clean']:
                self.task = "Cleaning"
            
            self.txt.append("\n")
        
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
                        self.txt.append("{color=[red]}%s has spotted a number of customers about to start trouble. "%(self.worker.fullname))
                        self.txt.append("She immediately called for security! \n{/color}")
                        
                        if not solve_job_guard_event(self, "bar_event", clients=self.loc.servicer["barclientsleft"], enemies=aggressive_clients, no_guard_occupation="ServiceGirl"):
                            self.apply_stats()
                            self.finish_job()
                
                if not self.finished:
                    self.txt.append("\n")
        

        

    class GuardJob(NewStyleJob):
        """
        The class that solve Building guard jobs.
        """
        def __init__(self, worker, loc, workers):
            """
            Creates a new GuardJob.
            girl = The girl the job is for.
            loc = The brothel the girl is in.
            workers = List of all relevant workers.
            """
            super(GuardJob, self).__init__(girl, workers, loc=loc)
            
            self.check_life()
            if not self.finished: self.get_events()
            if not self.finished: self.check_injury()
            if not self.finished: self.check_vitality()
            if not self.finished: self.post_job_activities()
            if not self.finished: self.check_vitality()
            if not self.finished: self.finish_job()
            self.apply_stats()
            
            try:
                self.workers.remove(self.worker)
            
            except:
                dialog.warning("Silent error during GuardJob.__init__, guard was already removed!")
        
        def get_events(self):
            """
            Get the guard events this girl will respond to.
            """
            self.txt.append(choice(["%s worked as guard in %s! \n"%(self.worker.fullname, self.loc.name),
                                    "%s did guard duty in %s! \n"%(self.worker.fullname, self.loc.name)]))
            
            self.txt.append("\n")
            self.img = "battle"
            
            if self.worker.guard_relay['bar_event']['count']:
                if self.worker.has_image("fighting"):
                    self.img = "fighting"
                
                g_events = plural("event", self.worker.guard_relay["bar_event"]["count"])
                
                self.txt.append("She responded to %d brawl %s. "%(self.worker.guard_relay['bar_event']['count'], g_events))
                self.txt.append("That resulted in victory(ies): %d and loss(es): %d! "%(self.worker.guard_relay['bar_event']['won'], self.worker.guard_relay['bar_event']['lost']))
                self.txt.append("\n")
                
                self.workermod = dict( (n, self.workermod.get(n, 0)+self.worker.guard_relay['bar_event']['stats'].get(n, 0)) for n in set(self.workermod)|set(self.worker.guard_relay['bar_event']['stats']) )
            
            if self.worker.guard_relay['whore_event']['count']:
                if self.worker.has_image("fighting"):
                    self.img = "fighting"
                
                g_events = plural("attack", self.worker.guard_relay["whore_event"]["count"])
                
                self.txt.append("With %d victory(ies) and %d loss(es) she settled %d %s on your prostitutes. \n"%(self.worker.guard_relay['whore_event']['won'],
                                                                                                                  self.worker.guard_relay['whore_event']['lost'],
                                                                                                                  self.worker.guard_relay['whore_event']['count'],
                                                                                                                  g_events))
                
                self.workermod = dict( (n, self.workermod.get(n, 0)+self.worker.guard_relay['whore_event']['stats'].get(n, 0)) for n in set(self.workermod)|set(self.worker.guard_relay['whore_event']['stats']) )
                self.txt.append("\n")
        
        def post_job_activities(self):
            """
            Solve the post job events.
            """
            
            if self.worker.AP <= 0:
                self.txt.append(choice(["Nothing else happened during her shift.", "She didn't have the stamina for anything else today."]))
            
            else:
                gbu = self.loc.get_upgrade_mod("guards")
                if gbu == 3:
                    guardlist = [girl for girl in hero.girls if girl.location == self.loc and girl.action == 'Guard' and girl.health > 60]
                    guards = len(guardlist)
                    
                    if guards > 0:
                        if guards >= 3:
                            self.txt.append(", ".join(girl.name for girl in guardlist[:guards-1]))
                            self.txt.append(" and %s "%guardlist[guards-1].nickname)
                            self.txt.append("spent the rest of the day dualing eachother in Sparring Quarters. \n")
                            
                            while self.worker.AP > 0:
                                self.workermod['attack'] = self.workermod.get('attack', 0) + choice([0, 0, 0, 0, 1, guards])
                                self.workermod['defence'] = self.workermod.get('defence', 0) + choice([0, 0, 0, 0, 1, guards])
                                self.workermod['magic'] = self.workermod.get('magic', 0) + choice([0, 0, 0, 0, 1, guards])
                                self.workermod['joy'] = self.workermod.get('joy', 0) + choice([0, 1, 2, 3]) 
                                self.workermod['vitality'] = self.workermod.get('vitality', 0) - randint(15, 20)
                                self.worker.AP -=  1
                            
                            self.workermod['exp'] = self.workermod.get('exp', 0) + self.worker.AP * randint(8, 12) + 5 * (guards-1) # Moved to prevent insane exp increases at higher levels.    
                        
                        elif guards == 2: 
                            self.txt.append("%s and %s spent time dualing eachother! \n"%(guardlist[0].name, guardlist[1].name))
                            
                            while self.worker.AP > 0:
                                self.workermod['attack'] = self.workermod.get('attack', 0) + choice([0,0,0,0,1,guards])
                                self.workermod['defence'] = self.workermod.get('defence', 0) + choice([0,0,0,0,1,guards])
                                self.workermod['magic'] = self.workermod.get('magic', 0) + choice([0,0,0,0,1,guards])
                                self.workermod['joy'] = self.workermod.get('joy', 0) + choice([0,1,2,3]) 
                                self.workermod['vitality'] = self.workermod.get('vitality', 0) - randint(15, 20)
                                self.worker.AP -=  1
                            
                            self.workermod['exp'] = self.workermod.get('exp', 0) + self.worker.AP * randint(8, 12) + 5
                        
                        elif guards == 1:
                            self.txt.append("%s had the whole Sparring Quarters to herself! \n"%(guardlist[0].name))
                            
                            while self.worker.AP > 0:
                                self.workermod['attack'] = self.workermod.get('attack', 0) + choice([0,0,0,0,1,guards])
                                self.workermod['defence'] = self.workermod.get('defence', 0) + choice([0,0,0,0,1,guards])
                                self.workermod['magic'] = self.workermod.get('magic', 0) + choice([0,0,0,0,1,guards])
                                self.workermod['joy'] = self.workermod.get('joy', 0) + choice([0,1,2,3]) 
                                self.workermod['vitality'] = self.workermod.get('vitality', 0) - randint(15, 20)
                                self.worker.AP -=  1
                            
                            self.workermod['exp'] = self.workermod.get('exp', 0) + self.worker.AP * randint(8, 12)
                
                elif gbu == 2:
                    self.txt.append("She spent remainder of her shift practicing in Training Quarters. \n")
                    
                    while self.worker.AP > 0:
                        self.workermod['attack'] = self.workermod.get('attack', 0) + choice([0,0,0,1])
                        self.workermod['defence'] = self.workermod.get('defence', 0) + choice([0,0,0,1])
                        self.workermod['magic'] = self.workermod.get('magic', 0) + choice([0,0,0,1])
                        self.workermod['joy'] = self.workermod.get('joy', 0) + choice([0,1,1,2]) 
                        self.workermod['vitality'] = self.workermod.get('vitality', 0) - randint(15, 20)
                        self.worker.AP -= 1
                    
                    self.workermod['exp'] = self.workermod.get('exp', 0) + self.worker.AP * randint(8, 12)
                
                elif self.loc.upgrades['guards']['1']['active']:   
                    if dice(50):
                        self.txt.append("She spent time relaxing in Guard Quarters. \n")
                        self.workermod['vitality'] = self.workermod.get('vitality', 0) + randint(15, 20) * self.worker.AP
                        self.worker.AP = 0
                    
                    else:
                        self.txt.append("She did some rudamentory training in Guard Quarters. \n")
                        self.workermod['attack'] = self.workermod.get('attack', 0) + choice([0,0,0,0,1])
                        self.workermod['defence'] = self.workermod.get('defence', 0) + choice([0,0,0,0,1])
                        self.workermod['magic'] = self.workermod.get('magic', 0) + choice([0,0,0,0,1])
                        self.workermod['joy'] = self.workermod.get('joy', 0) + choice([0,1,1,1]) 
                        self.workermod['exp'] = self.workermod.get('exp', 0) +  randint(15, 25)
                        self.workermod['vitality'] = self.workermod.get('vitality', 0) - randint(15, 20)
                        self.worker.AP = 0
                
                else:   
                    if dice(50):
                        self.txt.append("She spent time relaxing. \n")
                        
                        #display rest only if they did not fight
                        if not self.worker.guard_relay['bar_event']['count'] and not self.worker.guard_relay['whore_event']['count']:
                            self.img = "rest"
                        
                        self.workermod['vitality'] = self.workermod.get('vitality', 0) + randint(7, 12) * self.worker.AP
                        self.worker.AP = 0
                    
                    else:
                        self.txt.append("She did some rudamentory training. \n")
                        self.workermod['attack'] = self.workermod.get('attack', 0) + choice([0,0,0,0,0,1])
                        self.workermod['defence'] = self.workermod.get('defence', 0) + choice([0,0,0,0,0,1])
                        self.workermod['magic'] = self.workermod.get('magic', 0) + choice([0,0,0,0,0,1])
                        self.workermod['joy'] = self.workermod.get('joy', 0) + choice([0,1]) 
                        self.workermod['exp'] = self.workermod.get('exp', 0) +  randint(8, 15)
                        self.workermod['vitality'] = self.workermod.get('vitality', 0) - randint(15, 20)
                        self.worker.AP = 0
