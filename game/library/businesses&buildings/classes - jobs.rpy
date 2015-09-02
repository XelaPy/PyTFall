init -9 python:
    def check_char(c):
        """
        Checks whether the girl is injured and sets her to auto rest.
        """
        if c.health < 60:
            # self.txt.append("%s is injured and in need of medical attention! "%c.name)
            # self.img = c.show("profile", "sad", resize=(740, 685))
            if c.autocontrol['Rest']:
                c.previousaction = c.action
                c.action = AutoRest()
                # self.txt.append("She is going to take few days off to heal her wounds. ")
            return    
        if c.vitality < 35:
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
        """
        Baseclass for jobs and other next day actions with some defaults.
        """
        def __init__(self, girl=None, girls=None, loc=None, event_type="girlreport"):
            """
            Creates a new Job.
            girl = The girl the job is for.
            girls = The list of girls the girl is in.
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
            
        def __call__(self, girl, girls, loc=None, event_type="girlreport"):
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
            
        def get_upgrade(self):
            # This returns a correct upgrade girl is working atm.
            # In case none was logged to her, upgrade that makes the most sense should be picked.
            return
        
        def create_event(self):
            """
            Returns an event depicting the current state of this job.
            """
            if isinstance(self.txt, (list, tuple)):
                self.txt = "".join(self.txt)
            
            return Event(type=self.event_type,
                                 img=self.img,
                                 txt=self.txt,
                                 girl=self.girl,
                                 girlmod=self.girlmod, 
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
            """
            Checks whether the girl is injured and sets her to auto rest.
            """
            if self.girl.health < 60:
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
            if self.girl.vitality < 35:
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
                
                # After a long conversation with Dark and CW, we've decided to prevent girls death during jobs
                # I am leaving the code I wrote before that decision was reached in case
                # we change our minds or add jobs like exploration where it makes more sense.
                elif stat == 'health' and (self.girl.health + self.girlmod[stat]) <= 0:
                    self.girl.health = 1
                
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
                    raise Error, "Stat: %s does not exits for Brothels"%stat
        
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
                    self.img = self.girl.show("profile", "angry", resize=(740, 685))
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
    ####################### Whore Job  ############################
    # class NewStyleJob(Job):
        # """
        # Class created to facilitate SimPy type of job loops.
        # Since events are now called by the SimPy, there is no general loop in a new style Job.3
        # """
        # def __init__(self):
            # pass
        # def __str__(self):
            # return str(self.id)
    
    
    class WhoreJob(Job):
        #Temporarily restored for reference!
        def __init__(self):
            super(WhoreJob, self).__init__()
            self.id = "Whore Job"
            
            # Traits/Job-types associated with this job:
            self.occupations = list() # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Prostitute"]] # Corresponing traits...
            
            # TODO: Rewrite for skills? Or simply leave it like this and add skills with a check in this dict...
            self.girlmod = {}
            self.locmod = {}
            
        def __call__(self, char, client):
            self.reset()
            
            self.event_type = "girlreport"
            self.char, self.client, self.loc = char, client, char.location
            self.girl = self.char
            # self.char = self.girl
            self.girlmod, self.locmod = {}, {}
            
            # if not self.finished: self.check_injury()
            # if not self.finished: self.check_vitality()
            
            # Returning client to the list if girl wasn't actually availible TODO:
            # if self.finished:
                # self.client.traitmatched = False
                # self.clients.append(client)
                # return
            
            # if self.check_dirt(): TODO:
                # global stop_whore_job
                # stop_whore_job = True
                
            # We no longer check for occupation from inside of this method!
            # if not self.finished: self.check_occupation()
            
            # AP cost of the job if all checks for refusals have failed.
            if not self.finished:
                self.char.AP -= 1
                self.payout_mod()
            
            # if not self.finished: self.guard_event()
            
            if not self.finished: self.acts()

            # self.payout = self.char.fin.get_whore_price()
            
            # Upgrades (main hall branch)
            # if self.brothel.upgrades['mainhall']['3']['active']:
                # self.payout = int(self.payout * 1.4)
                # self.txt.append("Sex goddess statue in your brothel influences the minds of your customers to pay something extra for your girls services. \n")
            # elif self.brothel.upgrades['mainhall']['2']['active']:
                # self.payout = int(self.payout * 1.2)
                # self.txt.append("Customer will pay extra because of the services promised to him at the reception.\n")
            # elif self.brothel.upgrades['mainhall']['2']['active']:
                # self.payout = int(self.payout * 1.1)
                # self.txt.append("Client had a nice time relaxing in the main hall. Expect some tips :) \n")
                
        def check_rank(self):
            """
            @Review: We are disabling ranks until better times :)
            Checks the whore rank against the client rank.
            """
            if self.char.rank < self.client.rank - 2 and self.char.status == 'free':
                self.txt.append("The customer quickly realized that %s was too poor of a whore rank to bother with her, "%self.char.name + \
                                "%s pushed her out of the way as if she was not even there and left pissed at the establishment... \n"%self.client.pronoun)
                
                self.txt.append("You should not forget that people in PyTFall take prostitute ranks very seriously and all girls who choose that lifestyle or were forced into it, "+ \
                                "should strive to improve rank. Being told that she was not good enough is not likely to increase your girls happiness... ")
                
                self.locmod['reputation'] -= (randint(1, 5) + self.client.rank)
                self.girlmod['joy'] -= randint(4, 10)
                
                self.img = self.char.show("profile", "sad", resize=(740, 685))
                
                self.apply_stats()
                self.finish_job()
                return
            
            elif self.client.rank < self.char.rank - 2 and self.char.status != 'slave':
                self.txt.append("This customer of yours can go to hell! %s is not worthy of even kissing my feet!  \n"%self.client.pronoun)
                self.txt.append("Even if an event like this was to damage your brothels reputation, such damage would be insignificant because noone would want to brag about a girl refusing them. \n")
                
                self.locmod['reputation'] -= randint(0, 1)
                
                self.img = self.char.show("profile", "angry", resize=(740, 685))
                
                self.apply_stats()
                self.finish_job()
                return
            
            elif self.client.rank < self.char.rank - 2 and self.char.status == 'slave':
                self.txt.append("%s didn't want to fuck someone so far below her own hard earned rank, but slaves have little choice...' "%self.char.name)
                self.girlmod['joy'] -= 10
                
        def check_occupation(self, char=None):
            """
            Checks the girls occupation.
            # TODO: We need to check this when assigning to Job! Not during it!
            # TODO: This will no longer make it to reports under the new code! Rewrite!!!
            # Still, we'll check this...
            """
            if not char:
                char = self.char
            
            if [t for t in self.occupation_traits if t in char.occupations]:
                if char.status != 'slave' and char.disposition > 900:
                    self.txt.append("%s: I am not thrilled about having some stranger 'do' me but you've been really good to me so... " % char.nickname)
                    self.loggs('disposition', -randint(10, 30))
                
                elif char.status != 'slave':
                    self.txt.append(choice(["%s: I am not some cheap whore that will do whatever you please! Find someone else for this debauchery! " % char.nickname,
                                                         "Don't be absurd, I am not fucking anyone for you!"]))
                    # TODO: Very Clumsy!
                    self.char = char
                    self.girl = char
                    self.loc = store.building
                    self.event_type = "girlreport"
                    self.girlmod, self.locmod = {}, {}
                    
                    self.loggs('disposition', -50)
                    self.img = char.show("profile", "angry", resize=(740, 685))
                    char.action = None
                    
                    self.apply_stats()
                    self.finish_job()
                    return
                
                else:
                    self.txt.append(choice(["%s is a slave so noone really cares but doing something that's not a part of her job has upset her a little bit." % char.name,
                                                         "She'll do as she is told, doesn't mean that she'll be happy about.",
                                                         "%s will do as you command but you cannot expect her to enjoy this..." % char.fullname]))
                    
                    self.loggs('joy', -randint(1, 3))
            
            else:
                self.txt.append(choice(["{} is doing her shift as Prostitute!".format(char.name),
                                                     "%s does her shift as a Prostitute!" % char.fullname,
                                                     "{color=[red]}Whore?{/color} WTF?? I am a {color=[pink]}Fancy Girl!!!{/color}"]))
                
            
            self.txt.append("\n\n")
            return True
                    
        # I need to rebuild relay so it makes more sense and then rewrite this method
        # Doing it now :)
        def payout_mod(self):
            # No matched traits
            self.payout = 1
            
            # TODO: UPDATE THIS TO BE WRITTEN FROM LOOP AND WITH likes AND dislikes
            # if not self.client.traitmatched:
                # if self.client.favtraits:
                    # self.txt.append("%s came to the %s looking for a girl with a %s traits but didn't find one so %s picked %s randomly. \n"%(self.client.caste,
                                                                                                                                              # self.loc.name, ", ".join(self.client.favtraits),
                                                                                                                                              # self.client.pronoun.lower(),
                                                                                                                                              # self.char.fullname))
                # else:
                    # self.txt.append("%s came to the %s brothel. Not wanting any kind of girl in particular %s went for %s. \n"%(self.client.caste,
                                                                                                                                # self.loc.name,
                                                                                                                                # self.client.pronoun.lower(),
                                                                                                                                # self.char.name))
            # else:
                # self.txt.append("%s came into %s and was looking for a girl with %s traits so %s went straight for %s. \n"%(self.client.caste,
                                                                                                                            # self.loc.name,
                                                                                                                            # ", ".join(self.client.favtraits),
                                                                                                                            # self.client.pronoun.lower(),
                                                                                                                            # self.char.name))
                # self.payout = int(self.payout * 1.3)
            
            # Brothel room upgrades modifiers, simple version for now
            # Might have to be improved to match customers expectations based on their castes later
            # bru = self.loc.get_upgrade_mod("room_upgrades")
            # if bru == 3:
                # self.txt.append("Any of your customers would be willing to chop off a finger just to spend a couple of hours in room so fine. "+ \
                                # "The companionship that %s provides is just a bonus. \n"%self.char.nickname)
                # self.girlmod['joy'] += choice([0,0,3])
                # self.girlmod['refinement'] += choice([0,0,0,0,3])
                # self.payout = int(self.payout * 1.6)
            # elif bru == 2:
                # self.txt.append("Luxury rooms had every convenience that could possibly spice up the upcoming intercource, this was definitely a sound investment on your part. \n")
                # self.girlmod['joy'] += choice([0,0,2])
                # self.girlmod['refinement'] += choice([0,0,0,0,2])
                # self.payout = int(self.payout * 1.3)
            # elif bru == 1:
                # self.txt.append("Improved rooms interior with an exotic sexual theme were much appreciated by your girl and her client. \n")
                # self.girlmod['joy'] += choice([0,0,1])
                # self.girlmod['refinement'] += choice([0,0,0,1])
                # self.payout = int(self.payout * 1.2)
            
            # self.txt.append("\n")
            
        def guard_event(self):
            """
            Solves guard events for agressive clients.
            """
            if "Aggressive" in self.client.traits and self.loc.guardevents["prostituteattackedevents"] < int(self.loc.id * 1.5) and not dice(self.loc.security_rating/10):
                # Relay
                self.loc.guardevents["prostituteattackedevents"] += 1
                self.txt.append("{color=[red]}Getting ready for some action with %s, %s became violent and threatened to beat the shit out of your girl.{/color} \n"%(self.char.name,
                                                                                                                                                                      self.client.pronoun.lower()))
                
                # If conflict is not resolved, act ends here, else act goes on to interactions.
                # Function calls girls.remove(girl) for us. # TODO: Get Rid of this!
                if not solve_job_guard_event(self, "whore_event", enemies=self.client):
                    self.apply_stats()
                    self.finish_job()
                        
                        
        def acts(self):
            # Blocks by girl/player
            # if self.client.act == 'lesbian' and not self.char.autocontrol["Acts"]["lesbian"]:
                # txt += "%s refused to perform lesbian, unblock it in her control options or raise disposition until she allows you to do so. \n"%(self.char.nickname)
                # txt += "You've otherwise lost this customer :( "
                # self.img = "profile"
                # self.apply_stats()
                # self.finish_job()
                # return
                 

            width = 820
            height = 705
            
            size = (width, height)
                
            # Straight Sex Act
            if self.client.act == 'sex':
                
                self.skill = "vaginal"
                
                # Temporarely done here, should be moved to game init and after_load to improve performance:
                tags = (("2c vaginal", "ontop"), ("2c vaginal", "doggy"), ("2c vaginal", "missionary"), ("2c vaginal", "onside"), ("2c vaginal", "standing"), ("2c vaginal", "spooning"))
                act = self.get_act(tags)

                if act == tags[0]:
                    self.txt.append("He invited her to 'sit' on his lap as he unsheathed his cock. They've continued along the same lines in 'girl ontop' position. \n")
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[1]:
                    self.txt.append("He ordered %s to bend over and took her from behind. \n"%self.char.nickname)
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[2]:
                    self.txt.append("He pushed %s on her back, shoved his cock in, screaming: 'Oh, Your pussy is wrapping around me so tight!' \n"%self.char.nickname)
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[3]:
                    self.txt.append("%s lay on her side inviting the customer to fuck her. He was more than happy to oblige.\n"%self.char.nickname)
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[4]:
                    self.txt.append("Not even bothering getting into a position, he took her standing up. \n")
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[5]:
                    self.txt.append("Customer felt cuddly so he spooned the girl until they both cummed. \n")
                    self.img = self.char.show(*act, resize=size)
                else:
                    self.txt.append(choice(['He wanted some old-fashioned straight fucking. \n',
                                                         'He was in the mood for some pussy pounding. \n',
                                                         'He asked for some playtime with her vagina.\n']))
                    self.img = self.char.show("2c vaginal", resize=size)
                    
                # Virgin trait check:
                self.take_virginity()


            # Anal Sex Act
            elif self.client.act == 'anal':
                
                self.skill = "anal"
                
                self.txt.append(choice(["Anal sex is the best, customer thought... ",
                                                      "I am in the mood for a good anal fuck, customer said. ",
                                                      "Customer's dick got harder and harder just from the thought of %s's asshole! "%self.char.nickname]))
                
                # Temporarely done here, should be moved to game init and after_load to improve performance:
                tags = (("2c anal", "ontop"), ("2c anal", "doggy"), ("2c anal", "missionary"), ("2c anal", "onside"), ("2c anal", "standing"), ("2c anal", "spooning"))
                act = self.get_act(tags)
                
                if act == tags[0]:
                    self.txt.append("He invited her to 'sit' on his lap as he unsheathed his cock. They've continued along the same lines in 'girl on top' position. \n")
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[1]:
                    self.txt.append("He ordered %s to bend over and took her from behind. \n"%self.char.nickname)
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[2]:
                    self.txt.append("He pushed %s on her back, shoved his cock in, screaming: 'Oh, Your anus is wrapping around me so tight!' \n"%self.char.nickname)
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[3]:
                    self.txt.append("%s lay on her side inviting the customer to fuck her. He was more than happy to oblige.\n"%self.char.nickname)
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[4]:
                    self.txt.append("Not even bothering getting into a position, he took her standing up. \n")
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[5]:
                    self.txt.append("Customer felt cuddly so he spooned the girl until they both cummed. \n")
                    self.img = self.char.show(*act, resize=size)
                else:
                    self.txt.append(choice(['He took her in the ass right there and then. \n',
                                                          'He got his dose of it. \n',
                                                          'And so he took her in her butt. \n']))
                    self.img = self.char.show("2c anal", resize=size)
                
            # Suck a Dick act    
            elif self.client.act == 'blowjob':
                
                self.skill = "oral"
                
                tags = (('bc deepthroat'), ('bc handjob'), {"tags": ['bc footjob'], "dice": 80}, ('bc titsjob'), {"tags": ["after sex"], "dice": 10}, ("bc blowjob"))
                act = self.get_act(tags)
                
                if act == tags[0]:
                    self.txt.append(choice(["He shoved his cock all the way into her throat! \n", "Deepthroat is definitely my style, thought the customer... \n"]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[1]:
                    self.txt.append("He told %s to give him a good handjob.\n"%self.char.nickname)
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[2]:
                    self.txt.append(choice(["He asked her for a foodjob.\n", "Footjob might be a weird fetish but that's what the customer wanted...\n"]))
                    self.img = self.char.show(*act["tags"], resize=size)                    
                elif act == tags[3]:
                    if trats["Big Boobs"] in self.char.traits or traits["Abnormally Large Boobs"] in self.char.traits:
                        self.txt.append(choice(["He went straight for her big boobs. \n", "Seeing her knockers, customer wanted notning else then to park his dick between them. \n", "Lustfully gazing on your girl's burst, he asked for a titsjob. \n", "He put his manhood between her big tits. \n" , "He showed his cock between %s's enormous breasts. \n"%self.char.nickname]))
                    elif traits["Small Boobs"] in self.char.traits:
                        if dice(7):
                            self.txt.append("With a smirk on his face, customer asked for a titsjob. He was having fun from her vain effords. \n")
                        else:    
                            self.txt.append(choice(["He placed his cock between her breasts, clearly enyoing her flat chest. \n", "Even when knowing that her breasts are small, he wanted to be carresed by them. \n"]))
                    else:
                        self.txt.append(choice(["He asked for a titsjob. \n", "He let %s to carres him with her breasts. \n", "He showed his cock between %s's tits. \n"%self.char.nickname]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[4]:
                    self.txt.append(choice(["Customer wanted nothing else then to jerk himself in from of her and ejactuate on her face. \n", "He wanked himself hard in efford to cover her with his cum. \n"]))
                    self.img = self.char.show(*act["tags"], resize=size)        
                elif act == tags[5]:
                    self.txt.append(choice(['Client was in mood for some oral sex. \n', 'Client was in the mood for a blowjob. \n', 'He asked her to lick his dick. \n']))
                    self.img = self.char.show(*act, resize=size)
                else: # I do not thing that this will ever be reached...
                    self.txt.append(choice(['Client was in mood for some oral sex. \n', 'Client was in the mood for a blowjob. \n', 'He asked her to lick his dick. \n']))
                    self.img = self.char.show("bc blowjob", resize=size)

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
                # if self.char.has_image("gay", "dildo joined"):
                    # acts.append("dildo joined")
                # if self.char.has_image("gay", "anal beads"):
                    # acts.append("les_anal_beads")
                # if self.char.has_image("gay", "do anal beads"):
                    # acts.append("les_do_anal_beads")
                    
                # act = choice(acts)

                # if act == "dildo joined":
                    # self.txt.append(choice(["She've asked your girl to lend her a double-ended dildo.\n",
                                                         # "She brought a twin-ended dildo for the party so %s could have some fun as well.\n"%self.char.nickname]))
                    # self.img = self.char.show("les", "dildo joined", resize=size)
                if act == tags[0]:
                    self.txt.append(choice(["Clearly in the mood for some cunt, she licked %ss pussy clean.\n"%self.char.nickname,
                                                         "Hungry for a cunt, she told %s to be still and started licking her soft pussy with her hot tong. \n"%self.char.nickname]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[1]:
                    self.txt.append(choice(["All hot and bothered, she ordered %s to lick her cunt. \n"%self.char.nickname,
                                                         "As if she had an itch, she quickly told %s to tong her pussy. \n"%self.char.nickname]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[2]:
                    self.txt.append(choice(["She licked %ss anus clean.\n"%self.char.nickname,
                                                                                    "She told %s to be still and started licking her asshole with her hot tong. \n"%self.char.nickname]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[3]:
                    self.txt.append(choice(["All hot and bothered, she ordered %s to lick her asshole. \n"%self.char.nickname,
                                                         "As if she had an itch, she quickly told %s to tong her anus. \n"%self.char.nickname]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[4]:
                    self.txt.append(choice(["In mood for a hot lesbo action, she stuck her fingers in your girls pussy. \n",
                                                         "She watched %s moan as she stuck fingers in her pussy. \n"%self.char.nickname]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[5]:
                    self.txt.append(choice(["Quite horny, she ordered your girl to finger her cunt. \n",
                                                         "Clearly in the mood, she told %s to finger her until she cums. \n"%self.char.nickname]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[6]:
                    self.txt.append(choice(["In mood for a hot lesbo action, she stuck her fingers in your girls anus. \n",
                                                         "She watched %s moan as she stuck fingers in her asshole. \n"%self.char.nickname]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[7]:
                    self.txt.append(choice(["Quite horny, she ordered your girl to finger her anus. \n",
                                                         "Clearly in the mood, she told %s to finger her asshole until she cums. \n"%self.char.nickname]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[8]:
                    self.txt.append(choice(["Liking your girls breasts, she had some good time caressing them. \n",
                                                         "She enjoyed herself by caressing your girls breasts. \n"]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[9]:
                    self.txt.append(choice(["She asked your girl to caress her tits. \n",
                                                         "She told your girl to put a squeeze on her breasts. \n"]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[10]:
                    self.txt.append(choice(["Girls lost themselves in eachothers embrace.\n",
                                                         "Any good lesbo action should start with a hug, don't you think??? \n"]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[11]:
                    self.txt.append(choice(["She put on a strapon and fucked your girl in her cunt. \n",
                                                          "Equipping herself with a strap-on, she lustfully shoved it in %ss pussy. \n"%self.char.nickname]))
                    self.img = self.char.show(*act, resize=size)
                    self.take_virginity()
                elif act == tags[12]:
                    self.txt.append(choice(["She ordered %s to put on a strapon and fuck her silly with it. \n"%self.char.nickname,
                                                          "She equipped %s with a strapon and told her that she was 'up' for a good fuck! \n"]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[13]:
                    self.txt.append(choice(["She put on a strapon and fucked your girl in her butt. \n",
                                                          "Equipping herself with a strapon, she lustfully shoved it in %ss asshole. \n"%self.char.nickname]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[14]:
                    self.txt.append(choice(["She ordered %s to put on a strapon and butt-fuck her silly with it. \n"%self.char.nickname,
                                                         "She equipped %s with a strapon and told her that she was 'up' for a good anal fuck! \n"]))
                    self.img = self.char.show(*act, resize=size)
                # elif act == "les_anal_beads":
                    # self.txt.append(choice(["They got their hands on some anal beads and shoved it up %ss butt. \n"%self.char.nickname,
                                                          # "She had some fun with your girls asshole and some anal beads \n"]))
                    # self.img = self.char.show("les", "anal beads", resize=size)
                # elif act == "les_do_anal_beads":
                    # self.txt.append(choice(["She had %s stick some anal beads up her butt. \n"%self.char.nickname,
                                                         # "She told %s to get some anal beads to play with her anus. \n"%self.char.nickname]))
                    # self.img = self.char.show("les", "do anal beads", resize=size)
                elif act == tags[15]:
                    self.txt.append(choice(["She played with a dildo and %ss pussy. \n"%self.char.nickname,
                                                         "She stuck a dildo up %s cunt. \n"%self.char.nickname]))
                    self.img = self.char.show(*act, resize=size)
                    self.take_virginity()
                elif act == tags[16]:
                    self.txt.append(choice(["Without further ado, %s fucked her with a dildo. \n"%self.char.nickname,
                                                         "She asked your girl to fuck her pussy with a dildo. \n"]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[17]:
                    self.txt.append(choice(["After some foreplay, she stuck a dildo up your girls butt. \n",
                                                                                   "For her money, she had some fun playing with a dildo and your girls asshole. \n"]))
                    self.img = self.char.show(*act, resize=size)
                elif act == tags[18]:
                    self.txt.append(choice(["After some foreplay, she asked %s to shove a dildo up her ass. \n"%self.char.nickname,
                                                         "This female customer of your brothel clearly believed that there is no greater pleasure than a dildo up her butt. \n"]))
                    self.img = self.char.show(*act, resize=size)
                else:
                    self.txt.append(choice(["She was in the mood for some girl on girl action. \n", "She asked for a good lesbian sex. \n"]))
                    self.img = self.char.show("gay", resize=size)
                    # Last fallback!
            
            else:
                self.txt.append("Whore Job\n\nMissed All acts!\n\n")
                self.skill = "vaginal"
                self.img = self.char.show("sex", resize=size)
                
            self.check_skills(self.skill)
                
            # Take care of stats mods
            sexmod = 1 if dice(20) else 0
            constmod = 1 if dice(12) else 0
            self.loggs(self.skill, sexmod)
            self.loggs("constitution", constmod)
            self.loggs("vitality", -randint(18, 28))
            
            if sexmod + constmod > 0:
                self.txt.append("\n%s feels like she learned something! \n"%self.char.name)
                self.loggs("joy", 1)       
            
            # Dirt:
            self.logloc("dirt", randint(2, 5))
            
            # Log income for girl and MC
            self.txt.append("{color=[gold]}\nA total of %d Gold was earned!{/color}" % self.payout)
            self.char.fin.log_wage(self.payout, "WhoreJob")
            self.loc.fin.log_work_income(self.payout, "WhoreJob")
            
            self.apply_stats()
            self.finish_job()
            
        def get_act(self, tags):
            acts = list()
            for t in tags:
                if isinstance(t, tuple):
                    if self.char.has_image(*t):
                        acts.append(t)
                elif isinstance(t, dict):
                    if self.char.has_image(*t.get("tags", []), exclude=t.get("exclude", [])) and dice(t.get("dice", 100)):
                        acts.append(t)
                
            if acts:
                act = choice(acts)
            else:
                act = None
                
            return act
            
        def take_virginity(self):
            if traits["Virgin"] in self.char.traits:
                tips = 100 + self.char.charisma * 3
                self.txt.append("\n{color=[pink]}%s lost her virginity!{/color} Customer thought that was super hot so she left a tip of {color=[gold]}%d Gold{/color} for your girl.\n\n"%(self.char.nickname, tips))
                self.char.remove_trait(traits["Virgin"])
                self.char.fin.log_tips(tips, "WhoreJob")
                self.loc.fin.log_work_income(tips, "WhoreJob")
            
        def check_skills(self, skill=None):
            if not skill:
                skill = self.skill
            if skill > 300 and self.char.charisma > 300:

                self.txt.append("The client was at your girls mercy. Her beauty enchanting, she playfully took him into her embrace and made him forget about the rest of the world until they were finished. \n")

                self.loggs("exp", randint(15, 25))
                self.loggs("joy", 3)
                
            elif 200 <= skill and 200 <= self.char.charisma:
                
                self.txt.append("Your girl performed wonderfully with her breathtaking beauty and matching carnal skill. \n")

                self.loggs("exp", randint(15, 25))
                self.loggs("joy", 2)
                
            elif 80 <= skill and 80 <= self.char.charisma:

                self.txt.append("Her well honed sexual skills and good looks both were pleasing to the customer. \n")

                self.loggs("exp", randint(15, 25))
                self.loggs("joy", 1)
                
            elif 30 <= skill and 30 <= self.char.charisma:

                self.txt.append("Your girl did the job to the best of her ability but her skills could definitely be improved and her beauty enhanced. \n")

                self.loggs("exp", randint(15, 25))
                
            elif -100 <= skill <= 30 and -100 <= self.char.charisma <= 30:

                self.txt.append("Your girl barely knew what she was doing. Her looks were not likely to be of any help to her either. \n")
                self.txt.append("Still, the customer explained that he preferred fucking her over a horse. Hearing that from him however, was not encouraging for your girl at all... \n")

                self.loggs("exp", randint(15, 25))
                self.loggs("joy", -2)
                
            elif skill < 30 and self.char.charisma > 30:

                self.txt.append("A cold turkey sandwich would have made a better sex partner than her. Her performance was however saved by her somewhat pleasing looks. \n")

                self.loggs("exp", randint(15, 25))
                self.loggs("joy", -2)
                
            elif skill > 30 and self.char.charisma < 30:

                self.txt.append("Her ability to please him sexually managed to help the client overlook the fact that she looked like a hag. \n")

                self.loggs("exp", randint(15, 25))
                self.loggs("joy", -1)
                
            else:
                self.txt.append('Dev Note: >>>I missed something!<<< Charisma = %d, Sex = %d \n'%(self.char.charisma, skill))
               
            self.txt.append("\n")
    
    class AnalWhore(Job):
        pass
    
    
    class StraightWhore(Job):
        pass
    
    
    class GayWhore(Job):
        pass
    
    
    class NextGenWhoreJob(Job):
        """
        The class that solves whoring jobs.
        @ Abandoned until 1.0 due to complexity of adding new content.
        """
        def __init__(self):
            """
            Creates a new WhoreJob.
            girl = The girl this job is for.
            client = The client this girl is servicing.
            loc = The brothel this girl is in.
            girls = The list of girls this girl is in.
            clients = The list of clients this client is in.
            """
            super(WhoreJob, self).__init__()
            self.id = "Whore Job"
            
            # Traits/Job-types associated with this job:
            self.occupations = list() # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Prostitute"]] # Corresponing traits...
            
            # TODO: Rewrite for skills? Or simply leave it like this and add skills with a check in this dict...
            self.girlmod = {}
            
            self.locmod = 0
            
        def __call__(self):
            self.reset()
            
            self.event_type = "girlreport"
            self.girl, self.client, self.loc = store.char, store.clients.pop(), store.char.location
            self.girlmod, self.locmod = {}, {}
            self.skill = None
            
            # if not self.finished: self.check_injury()
            # if not self.finished: self.check_vitality()
            
            # Returning client to the list if girl wasn't actually availible TODO:
            # if self.finished:
                # self.client.traitmatched = False
                # self.clients.append(client)
                # return
            
            # if self.check_dirt(): TODO:
                # global stop_whore_job
                # stop_whore_job = True
            
            if not self.finished: self.check_occupation()
            
            # AP cost of the job if all checks for refusals have failed.
            if not self.finished:
                self.girl.AP -= 1
                self.payout_mod()
            
            # if not self.finished: self.guard_event()
            
            if not self.finished: self.acts()
        
        def check_rank(self):
            """
            @Review: We are disabling ranks until better times :)
            Checks the whore rank against the client rank.
            """
            if self.girl.rank < self.client.rank - 2 and self.girl.status == 'free':
                self.txt.append("The customer quickly realized that %s was too poor of a whore rank to bother with her, "%self.girl.name + \
                                "%s pushed her out of the way as if she was not even there and left pissed at the establishment... \n"%self.client.pronoun)
                
                self.txt.append("You should not forget that people in PyTFall take prostitute ranks very seriously and all girls who choose that lifestyle or were forced into it, "+ \
                                "should strive to improve rank. Being told that she was not good enough is not likely to increase your girls happiness... ")
                
                self.locmod['reputation'] -= (randint(1, 5) + self.client.rank)
                self.girlmod['joy'] -= randint(4, 10)
                
                self.img = self.girl.show("profile", "sad", resize=(740, 685))
                
                self.apply_stats()
                self.finish_job()
                return
            
            elif self.client.rank < self.girl.rank - 2 and self.girl.status != 'slave':
                self.txt.append("This customer of yours can go to hell! %s is not worthy of even kissing my feet!  \n"%self.client.pronoun)
                self.txt.append("Even if an event like this was to damage your brothels reputation, such damage would be insignificant because noone would want to brag about a girl refusing them. \n")
                
                self.locmod['reputation'] -= randint(0, 1)
                
                self.img = self.girl.show("profile", "angry", resize=(740, 685))
                
                self.apply_stats()
                self.finish_job()
                return
            
            elif self.client.rank < self.girl.rank - 2 and self.girl.status == 'slave':
                self.txt.append("%s didn't want to fuck someone so far below her own hard earned rank, but slaves have little choice...' "%self.girl.name)
                self.girlmod['joy'] -= 10
        
        def check_occupation(self):
            """
            Checks the girls occupation.
            # TODO: We need to check this when assigning to Job! Not during it!
            # Still, we'll check this...
            """
            if [t for t in self.occupation_traits if t in self.girl.occupations]:
                if self.girl.status != 'slave' and self.girl.disposition > 900:
                    self.txt.append("%s: I am not thrilled about having some stranger 'do' me but you've been really good to me so... " % self.girl.nickname)
                    self.loggs('disposition', -randint(10, 30))
                
                elif self.girl.status != 'slave':
                    self.txt.append(choice(["%s: I am not some cheap whore that will do whatever you please! Find someone else for this debauchery! " % self.girl.nickname,
                                                         "Don't be absurd, I am not fucking anyone for you!"]))
                    
                    self.loggs('disposition', -50)
                    self.img = self.girl.show("profile", "angry", resize=(740, 685))
                    self.girl.action = None
                    
                    self.apply_stats()
                    self.finish_job()
                    return
                
                else:
                    self.txt.append(choice(["%s is a slave so noone really cares but doing something that's not a part of her job has upset her a little bit." % self.girl.name,
                                                         "She'll do as she is told, doesn't mean that she'll be happy about.",
                                                         "%s will do as you command but you cannot expect her to enjoy this..." % self.girl.fullname]))
                    
                    self.loggs('joy', -randint(1, 3))
            
            else:
                self.txt.append(choice(["{} is doing her shift as Prostitute!".format(self.girl.name),
                                                     "%s does her shift as a Prostitute!" % self.girl.fullname,
                                                     "{color=[red]}Whore?{/color} WTF?? I am a {color=[pink]}Fancy Girl!!!{/color}"]))
            
            self.txt.append("\n\n")
        
        # I need to rebuild relay so it makes more sense and then rewrite this method
        # Doing it now :)
        def payout_mod(self):
            # No matched traits
            self.payout = 1
            
            if not self.client.traitmatched:
                if self.client.favtraits:
                    self.txt.append("%s came to the %s looking for a girl with a %s traits but didn't find one so %s picked %s randomly. \n"%(self.client.caste,
                                                                                                                                              self.loc.name, ", ".join(self.client.favtraits),
                                                                                                                                              self.client.pronoun.lower(),
                                                                                                                                              self.girl.fullname))
                else:
                    self.txt.append("%s came to the %s brothel. Not wanting any kind of girl in particular %s went for %s. \n"%(self.client.caste,
                                                                                                                                self.loc.name,
                                                                                                                                self.client.pronoun.lower(),
                                                                                                                                self.girl.name))
            else:
                self.txt.append("%s came into %s and was looking for a girl with %s traits so %s went straight for %s. \n"%(self.client.caste,
                                                                                                                            self.loc.name,
                                                                                                                            ", ".join(self.client.favtraits),
                                                                                                                            self.client.pronoun.lower(),
                                                                                                                            self.girl.name))
                self.payout = int(self.payout * 1.3)
            
            # Brothel room upgrades modifiers, simple version for now
            # Might have to be improved to match customers expectations based on their castes later
            # bru = self.loc.get_upgrade_mod("room_upgrades")
            # if bru == 3:
                # self.txt.append("Any of your customers would be willing to chop off a finger just to spend a couple of hours in room so fine. "+ \
                                # "The companionship that %s provides is just a bonus. \n"%self.girl.nickname)
                # self.girlmod['joy'] += choice([0,0,3])
                # self.girlmod['refinement'] += choice([0,0,0,0,3])
                # self.payout = int(self.payout * 1.6)
            # elif bru == 2:
                # self.txt.append("Luxury rooms had every convenience that could possibly spice up the upcoming intercource, this was definitely a sound investment on your part. \n")
                # self.girlmod['joy'] += choice([0,0,2])
                # self.girlmod['refinement'] += choice([0,0,0,0,2])
                # self.payout = int(self.payout * 1.3)
            # elif bru == 1:
                # self.txt.append("Improved rooms interior with an exotic sexual theme were much appreciated by your girl and her client. \n")
                # self.girlmod['joy'] += choice([0,0,1])
                # self.girlmod['refinement'] += choice([0,0,0,1])
                # self.payout = int(self.payout * 1.2)
            
            self.txt.append("\n")
            
            # Statisfaction is determined by dividing total satisfaction by the number of strippers.
            # Can run high since strippers can go more than for one round a day but that shouldn't be a problem or can be balanced out later.
            # if self.client.seenstrip:
                # satisfaction = self.client.stripsatisfaction / self.loc.servicer['strippers']
                # if satisfaction <= 0:
                    # self.txt.append('Customer seemed really put off by an earlier stripper performance, this will cost you a lot of income, consider doing something about your strippers! \n ')
                    # self.payout = int(self.payout*0.5)
                # elif satisfaction <= 25:
                    # self.client.libido -= 80 
                    # self.txt.append("Client is in a bad mood due to a strippers poor performance in your club! This will cost you some income. \n")
                    # self.payout = int(self.payout*0.7)
                # elif satisfaction <= 50:
                    # self.txt.append("Client is definitely not disappointed with the strippers performance in your club! This means a bit of extra income for you. \n")
                    # self.payout = int(self.payout*1.1)
                # elif satisfaction <= 75:
                    # self.txt.append("Client was really pleased with the strippers performance in the club and craving for a good fuck as a result! This means extra income for you. \n")
                    # self.payout = int(self.payout*1.2) 
                # elif satisfaction <= 100:
                    # self.txt.append("Customer was crazed with passion after seeing the most amazing stripper performance in your club! This means a lot of extra income for you. \n")
                    # self.payout = int(self.payout*1.5)
                # self.txt.append("\n")
        
        def guard_event(self):
            """
            Solves guard events for agressive clients.
            """
            if "Aggressive" in self.client.traits and self.loc.guardevents["prostituteattackedevents"] < int(self.loc.id * 1.5) and not dice(self.loc.security_rating/10):
                # Relay
                self.loc.guardevents["prostituteattackedevents"] += 1
                self.txt.append("{color=[red]}Getting ready for some action with %s, %s became violent and threatened to beat the shit out of your girl.{/color} \n"%(self.girl.name,
                                                                                                                                                                      self.client.pronoun.lower()))
                
                # If conflict is not resolved, act ends here, else act goes on to interactions.
                # Function calls girls.remove(girl) for us. # TODO: Get Rid of this!
                if not solve_job_guard_event(self, "whore_event", enemies=self.client):
                    self.apply_stats()
                    self.finish_job()
        
        def acts(self):
            """
            Solves the sexual acts performed by the girl.
            """
            # Get the unique sex case
            if self.client.act in pytWhoringActs: act = pytWhoringActs[self.client.act].for_girl(self.girl)
            else: act = pytWhoringActs["sex"].for_girl(self.girl)
            
            # Act text and image
            if act.has_preface: self.txt.append(act.get_preface())
            self.txt.append(act.get_text())
            self.img = act.get_image()
            
            # Virginity checks
            if act.is_vaginal and "Virgin" in self.girl.traits:
                tips = self.girl.charisma * 10
                self.txt.append("\n{color=[pink]}%s lost her virginity!{/color} The customer thought it was super hot so he left a tip of {color=[gold]}%d Gold{/color}.\n\n"%(self.girl.nickname, tips))
                self.girl.remove_trait(traits["Virgin"])
                self.girl.fin.log_tips(tips, "WhoreJob")
                self.loc.fin.log_work_income(tips, "WhoreJob")
            
            else:
                self.txt.append("\n")
            
            # Skill
            t, m = act.get_skill()
            self.txt.append(t + "\n")
            self.loggs("exp", randint(15, 25))
            self.loggs("joy", m)
            
            # Improvement:
            sexmod = 1 if dice(20) else 0
            constmod = 1 if dice(12) else 0
            # TODO: Rewrite to work with skillz!
            self.loggs("normalsex", sexmod)
            self.loggs("constitution", constmod)
            self.loggs("vitality", -randint(18, 28))
            
            if sexmod + constmod > 0:
                self.txt.append("\n%s feels like she learned something! \n"%self.girl.name)
                self.loggs("joy", 1)
            
            # Dirt:
            self.logloc("dirt", randint(2, 5))
            
            # Log income for girl and MC:
            self.txt.append("{color=[gold]}\nA total of %d Gold was earned!{/color}"%self.payout)
            self.girl.fin.log_wage(self.payout, "WhoreJob")
            self.loc.fin.log_work_income(self.payout, "WhoreJob")
            
            self.apply_stats()
            self.finish_job()
        
    
    ####################### Strip Job  ############################
    class StripJob(Job):
        """
        Class for the solving of stripping logic.
        """
        def __init__(self):
            """
            Creates a new StripJob.
            girl = The girl the job is for.
            loc = The loc the girl is in.
            girls = The list the girl is in.
            clients = The clients the girl can service.
            """ 
            super(StripJob, self).__init__()
            self.id = "Striptease Job"
            
            # Traits/Job-types associated with this job:
            self.occupations = ["SIW"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Prostitute"], traits["Stripper"]] # Corresponing traits...
            
            # Relevant skills and stats:
            self.skills = ["strip"]
            self.stats = ["charisma"]
            
            self.girlmod = {}
            self.locmod = {}
            
        def __call__(self, girl, loc):
            self.girl, self.loc = girl, loc
            
            # Get the cost of the job and cash it
            if self.girl.AP >= 3:
                aprelay = choice([2, 3])
                self.APr = aprelay
                self.girl.AP -= aprelay
            else:
                self.APr = self.girl.AP
                self.girl.AP = 0
                
            self.check_life()
            self.auto_clean()
            self.check_dirt()
            
            if not self.clients:
                self.txt.append("No clients wanted to see strippers today.")
                self.img = self.girl.show("profile", "sad", resize=(740, 685))
                self.finish_job()
                return
            
            if not self.finished: self.check_injury()
            if not self.finished: self.check_vitality()
            if not self.finished: self.check_occupation()
            if not self.finished: self.check_ap()
            if not self.finished: self.clients_relays()
            if not self.finished: self.strip()
            
        def check_occupation(self):
            """
            Checks the girls occupation against the job.
            """
            if [t for t in self.all_occs if t in self.girl.occupations]:
                if self.girl.status != 'slave' and self.girl.disposition > 900:
                    self.txt.append("%s: I am not thrilled about having to dance in front of a bunch of pervs, but you've been really good to me so I owe you a favor... "%self.girl.nickname)
                    self.loggs('disposition', -randint(5, 10))
                    self.loggs('joy', -randint(3, 6)) 
                
                elif self.girl.status != 'slave':
                    self.txt.append(choice(["%s: I refuse to do work as a Stripper!"%self.girl.nickname,
                                                        "Stripping? You're kidding me right?",
                                                        "Find someone else to strip for those perves!"]))
                    self.loggs('disposition', -50)
                    self.img = self.girl.show("profile", "angry", resize=(740, 685))
                    
                    self.girl.action = None
                    self.apply_stats()
                    self.girls.remove(self.girl)
                    self.finish_job()
                
                else:
                    self.txt.append(choice(["%s is a slave so she'll do as she's told. Doesn't mean that she's happy about it... \n"%self.girl.name,
                                                        "Being a slave, %s had no choice but to do as she's told."%self.girl.name,
                                                        "Even though %s is a slave and will do as she's told, consider giving poor girl a task better suited to her profession."%self.girl.name]))
                    self.loggs('joy', -randint(5, 10))
            
            else:
                self.txt.append(choice(["%s is doing her thing as a stripper!"%self.girl.fullname, "Your girl works as a stripper!", "Go Strippers!"]))
            
            if isinstance(self.txt, list): # TODO, Raise an Error!
                self.txt.append("\n\n")
        
        def check_ap(self):
            """
            Checks the girls ap for the job.
            TODO: Review this method!
            """
            if self.APr < 2:
                self.txt.append("%s did not have enough stamina left to throw a decent show, instead she "%(self.girl.name))
                if dice(50):
                    self.txt.append("went into the club, chatting with and entertaining customers. \n")
                    for i in xrange(self.APr * 3):
                        customer = choice(self.clients)
                        customer.stripsatisfaction += int(self.girl.charisma * 0.2 + self.girl.refinement * 0.2)
                        # self.loc.clientsr['club'] += 1
                    
                    if dice(7):
                        self.loggs('refinement', 1)
                    
                    if dice(33):
                        self.loggs('joy', 1)
                    
                    self.img = self.girl.show("profile", "happy", resize=(740, 685))
                    self.loggs('vitality', -self.APr * randint(15, 25))
                
                elif self.girl.strip < 800 and dice(50):
                    self.txt.append('tried to learn new moves to improve her striptease skills. \n')
                    if dice(50):
                        self.loggs('strip', 1)
                        self.loggs('joy', 2)
                        self.img = self.girl.show("profile", "happy", resize=(740, 685))
                        self.txt.append("She did well and got better! \n")
                    
                    else:
                        self.loggs('joy', -1)
                        self.img = self.girl.show("profile", "sad", resize=(740, 685))
                        self.txt.append("It was however a failed attempt. \n")
                    
                    self.loggs('vitality', -self.APr * randint(15, 25))
                
                else:
                    self.txt.append("took a little break. \n")
                    self.loggs('vitality', self.APr * randint(15, 25))
                    self.img = self.girl.show("rest", resize=(740, 685))
                
                self.loggs("exp", randint(15, 25))
                
                self.apply_stats()
                self.finish_job()
        
        # def clients_relays(self):
            # """
            # Gets the clients that the girl strips for.
            # """
            # total_clients = len(store.clients)
            # clients = len(self.clients)
            # c_cnt = plural("client", clients)
             
            # # Get proper text for the amount of clients
            # if clients > int(total_clients * 0.7):
                # self.txt.append('%d %s came to see her strip and dance in the club! It is a most impressive feat for one girl to attract so many! \n '%(clients, c_cnt))
            # elif int(total_clients * 0.5) <= clients <= int(total_clients * 0.7):
                # self.txt.append('%d %s came to see her strip and dance in the club! This is a very respectable amount of fans for one girl to have! \n '%(clients, c_cnt))
            # elif int(total_clients * 0.25) <= clients <= int(total_clients * 0.5):
                # self.txt.append('%d %s came to see her strip and dance in the club! Not bad at all considering the size of the brothel! \n'%(clients, c_cnt))
            # elif int(total_clients * 0.1) <= clients <= int(total_clients * 0.25):
                # self.txt.append("%d %s came to see her strip, not the most impressive amount, but everyone has to start somewhere. \n"%(clients, c_cnt))
            # else:
                # self.txt.append("Just a couple of clients came to check your girl out, very poor result indeed. ")
        
        def strip(self):
            """
            Solves the main job logic.
            Applies effects to the girl, runs at the end of the job.
            """
            
            # tippayout = 0
            # len_clients = len(self.clients)
            
            # Upgrades
            # scbu = self.loc.get_upgrade_mod("stipclub")
            # if scbu == 3:
                # if dice(50):
                    # self.txt.append("Customers enjoyed the presence of golden cages and the awesome podium in your establishment! \n")
                    # self.locmod['fame'] += 1
                # tippayout += int(len_clients/4)*3
                # sat = int(((self.girl.strip / 2 + self.girl.charisma) / 2)*1.5)
                # for client in self.clients: client.stripsatisfaction += sat
            # elif scbu == 2:
                # if dice(50):
                    # self.txt.append("Large podium will ensure better tips and higher customer satisfaction!  \n")
                # tippayout += int(len_clients/4)*2
                # sat = int(((self.girl.strip / 2 + self.girl.charisma) / 2)*1.2)
                # for client in self.clients: client.stripsatisfaction += sat
            # else:
                # sat = int((self.girl.strip / 2 + self.girl.charisma) / 2)
                # for client in self.clients:
                    # client.stripsatisfaction += sat

            self.txt.append("\n")
            
            # TODO: Rewrite this bit:
            cl_strip = 0
            cl_char = 0
            for c in self.clients:
                # We get the highest skills a character has to match vs strip skill, assumption is that proffessional can appriciate another profi :)
                cl_strip = cl_strip + max(list(getattr(c, s + "skill") for s in c.stats.skills))
                cl_char = cl_char + c.charisma
                
            cl_strip = cl_strip / len_clients
            cl_char = cl_char / len_clients
            
            if self.girl.strip > cl_strip*1.5 and self.girl.charisma > cl_char*1.5:
                tippayout += int(len_clients / 5) + 1 * int(len_clients * self.girl.refinement * 0.01 * self.girl.charisma * 0.01 + len_clients * self.girl.strip * 0.01) + \
                                                        int(self.APr  * (self.girl.charisma * 0.01 + self.girl.strip * 0.005))
                self.txt.append("Your girl gave a performance worthy of kings and queens as the whole hall was cheering for her. \n")
                self.loggs('joy', 3)
            elif cl_strip*1.3 <= self.girl.strip and cl_char*1.3 <= self.girl.charisma:
                tippayout += int(len_clients / 5) + 1 * int(len_clients * self.girl.refinement*0.005 * self.girl.charisma*0.01 + len_clients * self.girl.strip * 0.015) + \
                                                        int(self.APr * (self.girl.charisma * 0.01 + self.girl.strip * 0.005))
                self.txt.append("Your girl lost all of her clothing piece by piece as she stripdanced on the floor, the whole hall was cheering for her. \n")
                self.loggs('joy', 2)
            elif cl_strip*1.15 <= self.girl.strip and cl_char*1.15 <= self.girl.charisma:
                tippayout += int(len_clients / 5) + 1 * int(len_clients * self.girl.refinement * 0.005 * self.girl.charisma * 0.005 + len_clients * self.girl.strip * 0.005) + \
                                                        int(self.APr * (self.girl.charisma * 0.01 + self.girl.strip * 0.005))
                self.txt.append("Your girl lost all of her clothing piece by piece as she stripdanced on the floor, the whole hall was cheering for her. "+ \
                                         "Overall it was a more than decent performance.  \n")
                self.loggs('joy', 1)
            elif cl_strip <= self.girl.strip and cl_char <= self.girl.charisma:
                tippayout += int(len_clients / 5) + 1 * int(len_clients * self.girl.refinement * 0.005 * self.girl.charisma * 0.003 + len_clients * self.girl.strip * 0.0025) + \
                                                        int(self.APr * (self.girl.charisma*0.01 + self.girl.strip*0.005) )
                self.txt.append("Your girl lost all of her clothing piece by piece as she stripdanced on the floor, some mildly drunk clients cheered for her. Overall it was a decent performance. \n")
            elif 0 <= self.girl.strip <= cl_strip and 0 <= self.girl.charisma <= cl_char:
                tippayout += int(len_clients / 5) + 1 * int(len_clients * self.girl.refinement * 0.0001 * self.girl.charisma * 0.0001 + len_clients * self.girl.strip * 0.0003) + \
                                                        int(self.APr * (self.girl.charisma * 0.001 + self.girl.strip * 0.001) )
                self.txt.append("%s certainly did not shine as she clumsily 'danced' on the floor. Neither her looks nor her skill could save the performance... "%self.girl.nickname + \
                                        "calls for a different stripper could be heard from all over the club! ")
                self.loggs('joy', -2)
            elif self.girl.strip < cl_strip and self.girl.charisma > cl_char:
                tippayout += int(len_clients/ 5 ) + 1 * int(len_clients * self.girl.refinement * 0.002 * self.girl.charisma * 0.003 + len_clients * self.girl.strip * 0.005) + \
                                                        int(self.APr * (self.girl.charisma * 0.01 + self.girl.strip * 0.005) )
                self.txt.append("Your girl tripped several times while trying to undress herself as she 'stripdanced' on the floor, noone really complained because even if her skill was inadequate, " + \
                                        "she was pretty enough to arouse most men and women in the club. Overall it was a decent performance. \n")
                self.loggs('joy', -1)
            elif self.girl.strip > cl_strip and self.girl.charisma < cl_char:
                tippayout += int(len_clients / 5) + 1 * int(len_clients * self.girl.refinement * 0.002 * self.girl.charisma * 0.002 + len_clients * self.girl.strip*0.003) + \
                                                        int(self.APr * (self.girl.charisma * 0.01 + self.girl.strip * 0.005) )
                self.txt.append("%s may not be the prettiest girl in town but noone really complained because what she lacked in looks, she made up in skill. "%self.girl.name + \
                                        "Overall it was a decent performance. \n")
                self.loggs('joy', -1)
            else:
                self.txt.append('Dev Note: >>>I missed something!<<< Charisma = %d, Strip = %d \n'%(self.girl.charisma, self.girl.strip))
            
            self.txt.append("\n")
            
            # Girl
            if dice(25):
                self.loggs('charisma', 1)
                self.txt.append("\nYour girls charisma increased as she learned a new trick on how to make herself pretty before the show! \n")
            
            if dice(35):
                self.loggs('strip', 1)
            
            self.loggs('exp', int(self.APr * randint(15, 25)))
            self.loggs('reputation', choice([0, 0, 0, 0, 0, 1, 0]) + int(round(0.01 * self.girl.charisma)) + int(round(0.005 * self.girl.strip)))
            self.loggs('fame', choice([0, 0, 1, 1, 0, 0, 0]) + int(round(0.02 * self.girl.charisma)) + int(round(0.02 * self.girl.strip)))
            self.loggs('agility', choice([0, 0, 0, 1]) * self.APr)
            self.girl.AP -= self.APr
            self.girlmod('vitality', randrange(15, 31))
            
            # Finances:
            self.girl.fin.log_tips(tippayout, "StripJob")
            self.loc.fin.log_work_income(tippayout, "StripJob")
            
            # Brothel
            self.logloc('dirt', min(300, len_clients * 4))
            
            # Clients
            # matchedclients = 0
            # sat = int(self.girl.charisma / 4 + self.girl.strip / 8)
            # for client in self.clients:
                # if client.favtraits & set(self.girl.traits):
                    # client.stripsatisfaction += sat
                    # matchedclients += 1
            # self.txt.append("\n{color=[blue]}Extra satisfaction bonus for %d %s on behalf of matched traits!!! {/color}"%(matchedclients, plural("client", matchedclients)))
            
            self.img = 'strip'
            self.apply_stats()
            self.finish_job()
        
    
    ####################### Rest Job  #############################
    class Rest(Job):
        """
        Class to solve resting girls.
        """
        def __init__(self):
            """
            Creates a new Rest.
            girl = The girl to solve for.
            """
            super(Rest, self).__init__()
            self.id = "Rest Job"
                
        def __call__(self, girl):
            self.girl = girl
            self.loc = self.girl.home
            
            self.img = None
            self.txt = list()
            self.girlmod = {}
            self.locmod = {}
            
            self.check_life()
            if not self.finished:
                self.rest()
                # self.trait_events()
                self.after_rest()
            
        def rest(self):
            """
            Rests the girl.
            """
            # If there is garden/landscape design:
            # gbu = self.loc.get_upgrade_mod("garden")
            # if gbu == 3:
                # self.girlmod['vitality'] += self.girl.AP * randint(9, 15)
                # self.girlmod['joy'] += self.girl.AP * randint(1, 2)
                # self.txt.append("Breathtaking landscape design had a very positive effects on all resting girls! \n")
                # if dice(70):
                    # self.img = self.girl.show("rest", "generic outdoor", "forest", "meadow", "park", resize=(740, 685))
                # else:
                    # self.img = "rest"
            # elif gbu == 2:
                # self.girlmod['vitality'] += self.girl.AP * randint(5, 10)
                # self.girlmod['joy'] += self.girl.AP
                # self.txt.append("Taking a walk in the garden had a very positive effect on your girl! \n")
                # if dice(70):
                    # self.img = self.girl.show("rest", "generic outdoor", "forest", "meadow", resize=(740, 685))
                # else:
                    # self.img = "rest"
            # else:
                # # If there is no garden...
                # self.img = "rest"
            # Stat Mods:
            self.txt.append(choice(["{} is resting.".format(self.girl.name), "{} is taking a break to recover.".format(self.girl.name)]))
            
            while self.girl.AP and not all([(self.girl.vitality + self.girlmod.get('vitality', 0) >= self.girl.get_max("vitality") - 50),
                                                          (self.girl.health + self.girlmod.get('health', 0) >= self.girl.get_max('health') - 5)]):
                self.loggs('health', randint(2, 3))
                self.loggs('vitality', randint(35, 40))
                self.loggs('mp', randint(1, 3))
                self.loggs('joy', randint(1, 2))
                self.loggs('libido', randint(1, 3))
                self.girl.AP -= 1
            
            if not self.img:
                self.img = self.girl.show("rest", resize=(740, 685))
                
        def is_rested(self):
            if (self.girl.vitality >= self.girl.get_max("vitality") - 50) and (self.girl.health >= self.girl.get_max('health') - 5):
                return True
        
        def trait_events(self):
            """
            Solve events for certain traits.
            TODO: Currently disabled due to being useless anyhow... restore when ready.
            """
            # Prepear the lists:
            rgList = list(entry for entry in hero.girls if entry.location == self.loc and entry.action in ['Rest', 'AutoRest'])
            rgList.remove(self.girl)
            gl = rgList * 1
            
            evcount = 0
            loopcount = 0
            
            while self.girl.traits and evcount == 0 and loopcount < 5:
                tgl = list() # Temporary Girls List...
                rt = choice(self.girl.traits)
                
                if evcount < 1: # rt = randomtrait
                    if "Magic Gift" == rt:
                        for girl in gl:
                            if set(["Magic Gift" , "Magic Talent"]).intersection(girl.traits) and girl.action in ["Rest", "AutoRest"]:
                                tgl.append(girl)
                        
                        if tgl:
                            secondgirl = choice(tgl)
                            self.txt.append("She took some time idly discussing the finer aspects of magic with %s. \n"%secondgirl.name)
                            self.img = self.girl.show("profile", "happy", resize=(740, 685))
                            secondgirl.magic += choice([0, 0, 0, 1])
                        
                        elif dice(75) and self.loc.upgrades['garden']['2']['active']:
                            self.txt.append("She used her day off to harvest ingredients for her spells in the garden. \n")
                            self.img = self.girl.show("rest", "generic outdoor", "forest", "meadow", resize=(740, 685))
                        
                        elif self.girl.reputation > 75 and self.girl.status != "slave":
                            self.txt.append("She decided to take a walk in the city, ending up showing magic tricks to local children. \n")
                            self.img = self.girl.show("profile", "urban", resize=(740, 685))
                            
                            if dice(20):
                                self.girlmod["reputation"] += 1
                            
                            self.girlmod["joy"] += 1
                        
                        else:
                            self.txt.append("She spent her time reading her Arcane book and unfriendly staring at passersby. \n")
                            self.img = self.girl.show("reading", resize=(740, 685))
                        
                        evcount += 1
                    
                    elif "Magic Talent" == rt:
                        for girl in gl:
                            if "Magic Talent" in girl.traits:
                                tgl.append(girl)
                        
                        if tgl:
                            secondgirl = choice(tgl)
                            self.txt.append("With a little reluctance she shared a bit of her Arcane knowledge with %s in exchange for an evening dessert. \n"%secondgirl.name)
                            self.img = self.girl.show("profile", "happy", resize=(740, 685))
                            secondgirl.magic += choice([0, 0, 0, 1])
                        
                        elif self.girl.status != 'slave' and self.loc.upgrades['garden']['2']['active']:
                            self.txt.append("Some customer tried to get it on with her and wouldn't leave her alone as she was resting in the garden, "+ \
                                            "until she summoned a small fireball and threatened to burn his hair. \n")
                            self.img = self.girl.show("rest", "generic outdoor", "forest", "meadow", resize=(740, 685), type="first_default")
                        
                        else:
                            self.txt.append("She spent her day in her pocket dimension with every possible comfort. \n")
                            self.img = "rest"
                        
                        evcount += 1
                    
                    elif "Athletic" == rt:
                        if self.girl.status != 'slave':
                            self.txt.append("She spent her resting day on the beach taking occasional swims in the ocean. \n")
                            self.img = self.girl.show("beach", "bikini", "topless", exclude=main_sex_tags, resize=(740, 685))
                            self.girlmod['constitution'] += choice([0, 0, 0, 0, 1])
                        
                        else:
                            self.txt.append("She spent her day off exercising, occasionally taking a break, believing that to be the best rest for her.  \n")                          
                            self.img = self.girl.show("exercising", "sport", resize=(740, 685), type="any")
                            self.girlmod['constitution'] += choice([0, 0, 0, 0, 1])
                        
                        evcount += 1
                    
                    elif "Smart" == rt:
                        for girl in gl:
                            if set(["Smart" , "Genius"]).intersection(girl.traits) and girl.action in ["Rest", 'AutoRest']:
                                tgl.append(girl)
                        
                        if tgl:
                            secondgirl = choice(tgl)
                            self.txt.append("She spent some time playing board games with %s. \n"%secondgirl.name)
                            self.img = self.girl.show("profile", "happy", resize=(740, 685))
                            self.girlmod['intelligence'] += choice([0, 0, 0, 0, 1])
                            secondgirl.intelligence += choice([0, 0, 0, 0, 1])
                        
                        else:
                            self.txt.append("She spent part of her rest day translating some runes from ancient looking books. \n")
                            self.img = self.girl.show("reading", "studying", resize=(740, 685), type="any")
                        
                        evcount += 1    
                    
                    elif "Nerd" == rt:
                        if dice(60) and self.loc.upgrades['garden']['2']['active']:
                            self.txt.append("She used her day off trying to get some strange device in the garden to work. \n")
                            self.img = self.girl.show("rest", "generic outdoor", "forest", "meadow", resize=(740, 685), type="first_default")
                        
                        else:
                            self.txt.append("She spent all day reading books in her room. \n")
                            self.img = self.girl.show("reading", "studying", resize=(740, 685), type="any")
                        
                        evcount += 1
                    
                    elif "Genius" == rt:
                        for girl in gl:
                            if set(["Smart", "Genius"]).intersection(girl.traits) and girl.action in ["Rest", 'AutoRest']:
                                tgl.append(girl)
                        
                        if len(tgl) > 0:
                            secondgirl = choice(tgl)
                            self.txt.append("She spent some time playing board games with %s. \n"%secondgirl.name)
                            self.img = self.girl.show("profile", "happy", resize=(740, 685))
                            self.girlmod['intelligence'] += choice([0,0,0,0,1])
                            secondgirl.intelligence += choice([0,0,0,0,1])
                        
                        else:
                            self.txt.append("She spent part of her rest day translating some runes from ancient looking books. \n")
                            self.img = self.girl.show("reading", "studying", resize=(740, 685))
                        
                        evcount += 1
                    
                    elif rt in ['Long legs', 'Big Boobs', 'Abnormally Large Boobs', 'Great Arse', 'Great Figure']:
                        if self.girl.status != 'slave':
                            self.txt.append("She spent her time enjoying sunbathing as well as receiving envious and admiring glances on a local beach. Too bad you were too busy to join her. \n")
                            self.img = self.girl.show("beach", "bikini", "topless", exclude=main_sex_tags, resize=(740, 685))
                            self.girlmod['reputation'] += choice([0, 0, 0, 0, 1])
                        
                        else:
                            self.txt.append("She spent better part of her rest day trying to figure out how to use her heavenly body features to her advantage. \n")
                            self.img = self.girl.show("profile", "exposed", "beauty", resize=(740, 685))
                            if dice(10):
                                self.girlmod['charisma'] += 1
                        
                        evcount += 1
                    
                    elif "Nymphomaniac" == rt:
                        self.girlmod['libido'] += 20
                        self.txt.append("She spent some of her day having fun with herself in her room. \n")
                        self.img = 'mast'
                        evcount += 1
                    
                    elif "Exhibitionist" == rt:
                        if dice(70):
                            self.txt.append("Since she is going to walk around with barely any clothes on anyway, you asked her to do it around the brothel this time. "+ \
                                            "Free advertising is good for business, and she will have less problems with the city guards this way. \n")
                            self.img = self.girl.show("strip", "exposed", "topless", "nude", "undress", exclude=main_sex_tags, resize=(740, 685), type="any")
                            
                            if dice(10):
                                self.girlmod['strip'] += 1
                            
                            if dice(25):
                                self.girlmod['joy'] += 3
                            
                            if dice(75):
                                self.locmod["fame"] += 1
                            
                            evcount += 1
                        
                        else:
                            evcount += 1
                    
                    elif "Professional Maid" == rt:
                        self.txt.append("Even though today is her day off, she insisted on doing some cleaning. \n")
                        self.img = self.girl.show("cleaning", resize=(740, 685))
                        
                        if dice(10):
                            self.girlmod['service'] += 1
                        
                        self.locmod['dirt'] -= int(self.girl.serviceskill*0.2)
                        
                        evcount += 1
                    
                    loopcount += 1
            
            # If girl is down with cold:
            if self.girl.effects['Down with Cold']['active']:
                self.girl.effects['Down with Cold']['count'] += 2
                self.txt.append("Allowing her to rest is a really good idea considering that she has a cold! \n ")
            
            if self.girl.effects['Food Poisoning']['active']:
                self.girl.effects['Food Poisoning']['count'] += 2
                self.txt.append("Allowing her to rest is a really good idea considering that she has food poisoning! \n ")
            
            if evcount == 0:
                self.txt.append(choice(['%s took a break today. '%(self.girl.name),
                                        'She spent the day relaxing. ',
                                        '%s comfortably rested in her room. '%(self.girl.name)]))
        
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
            
            # TODO: A REWRITE???? *Check if previous action is availible and act accordingly!
            if self.is_rested():
                self.txt.append("\n\nShe is now both well rested and healthy, so she goes back to work as %s!" % self.girl.previousaction)
                self.girl.action = self.girl.previousaction
                self.girl.previousaction = None  # This is redundant but just in case
                
                if self.girl.autoequip:
                    # **Adapt to new code structure...
                    equip_for(self.girl, self.girl.action)
            
            self.finish_job()
    
    ####################### Service Job  ##########################
    class TestingJob(Job):
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
            
            self.event_type = "girlreport"
            self.girl, self.loc = char, char.location
            
            self.client = client
            
            char, cl = self.girl, self.client
            
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
            
            
    class Waiting(Job):
        def __init__(self):
            super(Waiting, self).__init__()
        
        def __call__(self, girl):
            pass
            
        def club_task(self):
            """
            Solve the job as a waitress.
            """
            clientsmax = self.APr * (2 + (self.girl.agility * 0.05 + self.girl.serviceskill * 0.05 + self.girl.refinement * 0.01))
            
            if self.loc.servicer['clubclientsleft'] - clientsmax <= 0:
                clientsserved = self.loc.servicer['clubclientsleft']
                self.txt.append("She finished serving drinks and snacks to tables of %d remaining customers. At least she got a break.  \n"%self.loc.servicer['clubclientsleft'])
                self.loc.servicer['clubclientsleft'] -= clientsserved
            
            elif self.loc.servicer['clubclientsleft'] - clientsmax > 0:
                clientsserved = clientsmax
                self.txt.append("She served snacks and drinks to tables of %d clients. \n"%(clientsmax))
                self.loc.servicer['clubclientsleft'] = self.loc.servicer['clubclientsleft'] - clientsserved
            
            clubfees = clientsserved * self.loc.rep * 0.08 + clientsserved * 0.5 * (self.girl.refinement * 0.1 + self.girl.charisma * 0.1 + self.girl.service * 0.025)
            tips = 0
            
            self.txt.append("\n")
            
            # Skill Checks
            if self.girl.serviceskill > 2000:
                self.locmod['reputation'] += choice([0, 1])
                clubfees = clubfees * 1.5
                tips = clubfees * 0.10
                self.txt.append("She is an exellent waitress, customers didn't notice how they've just kept spending their money as she offered them more and more house specials. \n")
            
            elif self.girl.serviceskill >= 1000:
                self.locmod['reputation'] += choice([0,0,0,1])
                clubfees = clubfees * 1.2
                tips = clubfees * 0.07
                self.txt.append("Customers were pleased with such a skilled waitress serving them. \n")
            
            elif self.girl.serviceskill >= 500:
                tips = clubfees * 0.03
                self.locmod['reputation'] += choice([0,0,0,0,0,1])
                self.txt.append("She was skillful enough not to mess anything up during her job. \n")
            
            elif self.girl.serviceskill >= 100:
                self.locmod['reputation'] += choice([0,0,-1,0,0,-1])
                clubfees = clubfees * 0.8
                self.txt.append("Her performance was rather poor and it most definitely has cost you income. \n")
            
            if self.girl.charisma > 300:
                tips = tips + clubfees*0.05
                self.locmod['fame'] += choice([0, 1, 1])
                self.girlmod['fame'] += choice([0, 0, 1])
                self.txt.append("Your girl was stunningly pretty, customers couldn't keep their eyes off her. \n")
            
            elif self.girl.charisma > 150:
                tips = tips + clubfees*0.03
                self.locmod['fame'] += choice([0 ,0, 1])
                self.girlmod['fame'] +=  choice([0, 0, 0, 1])
                self.txt.append("Your girl looked beautiful, this will not go unnoticed. \n")
            
            elif self.girl.charisma > 45:
                tips = tips + clubfees*0.02
                self.locmod['fame'] += choice([0, 0, 0, 1])
                self.girlmod['fame'] +=  choice([0, 0, 0, 0, 1])
                self.txt.append("Your girl was easy on the eyes, not bad for a bartender. \n")
            
            elif self.girl.charisma > 0:
                self.locmod['fame'] += choice([0, -1, -1])
                self.girlmod['fame'] +=  choice([0, 0, -1])
                self.txt.append("Customers did not appreciate a hag serving them. Consider sending this girl to a beauty school. \n")
            
            self.txt.append("\n")
            
            # Stat Mods
            self.girlmod['vitality'] -= clientsserved * 5
            self.girlmod['service'] += choice([0, 0, 1]) * self.APr
            self.girlmod['agility'] += choice([0, 0, 1]) * self.APr
            self.girlmod['exp'] += self.APr * randint(15, 25)
            
            self.locmod['dirt'] += clientsserved * 6
            
            # Integers:
            clubfees = int(round(clubfees))
            tips = int(round(tips))
            
            self.txt.append("{color=[gold]}%s earned %d Gold during this shift"%(self.girl.nickname, clubfees))
            
            if tips:
                self.txt.append(" and got %d in tips" % tips)
            
            self.txt.append(".{/color}\n")
            
            self.img = self.girl.show("bunny", "waitress", exclude=main_sex_tags, resize=(740, 685), type="any")
            
            # Finances:
            self.girl.fin.log_wage(clubfees, "Waitress")
            self.girl.fin.log_tips(tips, "Waitress")
            self.loc.fin.log_work_income(clubfees + tips, "Waitress")
            
            self.apply_stats()
            self.finish_job()
    
    class Bartending(Job):
        def bar_task(self):
            """
            Solves the job as a bar server.
            """
            self.auto_clean()
            if self.check_dirt():
                return
            
            # Business as usual
            beer = self.loc.get_upgrade_mod("bar") == 2
            tapas = self.loc.get_upgrade_mod("bar") == 3
            
            clientsmax = self.APr * (4 + (self.girl.agility * 0.1 + self.girl.serviceskill * 0.08))
            clients = plural("customer", clientsmax)
            
            if self.loc.servicer['barclientsleft'] - clientsmax <= 0:
                clientsserved = self.loc.servicer['barclientsleft']
                
                if tapas:
                    self.txt.append("Your girl finished serving cold beer and tasty snacks to customers for the day! She even managed a small break at the end of her shift! \n")
                
                elif beer:
                    self.txt.append("Remaining bar customers enjoyed cold draft beer. %s got a little break at the end of her shift! \n"%self.girl.nickname)
                
                else:    
                    self.txt.append("Your girl wrapped up the day at the bar by serving drinks to %d remaining customers. At least she got a small break.  \n"%self.loc.servicer['barclientsleft'])
                
                self.loc.servicer['barclientsleft'] = 0
                self.girlmod['vitality'] += self.APr * randint(1, 5)
            
            elif self.loc.servicer['barclientsleft'] - clientsmax > 0:
                clientsserved = clientsmax
                
                if tapas:
                    self.txt.append("She served cold draft beer and mouthwatering snacks to %d %s. \n"%(clientsmax, clients))
                
                elif beer:
                    self.txt.append("She served cold and refreshing tapbeer to %d %s. \n"%(clientsmax, clients))
                
                else:    
                    self.txt.append("She served snacks and drinks at the bar to %d %s. \n" % (clientsmax, clients))
                
                self.loc.servicer['barclientsleft'] = self.loc.servicer['barclientsleft'] - clientsserved
                self.girlmod['vitality'] -= 4 * clientsmax
            
            barfees = clientsserved * self.loc.rep * 0.05 + clientsserved * 0.5*(self.girl.refinement * 0.05 + self.girl.charisma * 0.1 + self.girl.serviceskill * 0.05)
            tips = 0 # Will be 0 - 15% of the total bill depending on girls skillz and looks.
            
            if tapas:
                barfees = barfees * 1.5
            
            elif beer:
                barfees = barfees * 1.2
            
            self.txt.append("\n")
            
            # Skill checks
            if self.girl.serviceskill > 2000:
                self.locmod['reputation'] += choice([0, 1])
                barfees = barfees * 1.5
                tips = barfees * 0.10
                self.txt.append("She was a godlike bartender, customers kept spending their money just for the pleasure of her company. \n")
            
            elif self.girl.serviceskill >= 1000:
                self.locmod['reputation'] += choice([0, 1])
                barfees = barfees * 1.2
                tips = barfees * 0.07
                self.txt.append("Customers were pleased with her company and kept asking for more booze. \n")
            
            elif self.girl.serviceskill >= 500:
                tips = barfees * 0.03
                self.locmod['reputation'] += choice([0, 0, 0, 0, 0, 1])
                self.txt.append("She was skillful enough not to mess anything up during her job. \n")
            
            elif self.girl.serviceskill >= 100:
                self.locmod['reputation'] += choice([0, 0, -1, 0, 0, -1])
                barfees = barfees * 0.8
                self.txt.append("Her performance was rather poor and it most definitely has cost you income. \n")
            
            if self.girl.charisma > 300:
                tips = tips + barfees*0.05
                self.locmod['fame'] += choice([0,1,1])
                self.girlmod['fame'] += choice([0,0,1])
                self.txt.append("Your girl was stunningly pretty, customers couldn't keep their eyes off her. \n")
            
            elif self.girl.charisma > 150:
                tips = tips + barfees * 0.03
                self.locmod['fame'] += choice([0,0,1])
                self.girlmod['fame'] += choice([0,0,0,1])
                self.txt.append("Your girl looked beautiful, this will not go unnoticed. \n")
            
            elif self.girl.charisma > 45:
                tips = tips + barfees*0.02
                self.locmod['fame'] += choice([0,0,0,1])
                self.girlmod['fame'] += choice([0,0,0,0,1])
                self.txt.append("Your girl was easy on the eyes, not bad for a bartender. \n")
            
            elif self.girl.charisma > 0:
                self.locmod['fame'] += choice([0,-1,-1])
                self.girlmod['fame'] += choice([0,0,-1])
                self.txt.append("Customers did not appreciate a hag serving them. Consider sending this girl to a beauty school. \n")
            
            self.txt.append("\n")
            
            #Stat Mods
            self.girlmod['exp'] += self.APr * randint(15, 25)
            self.girlmod['service'] += choice([0, 0, 1]) * self.APr
            self.girlmod['refinement'] += choice([0, 0, 0, 0, 1]) * self.APr
            self.girlmod['vitality'] -= clientsserved * 3
            
            self.locmod['dirt'] += clientsserved * 2
            
            # Integers:
            barfees = int(round(barfees))
            tips = int(round(tips))
            
            self.txt.append("{color=[gold]}%s brought in %d Gold during her shift"%(self.girl.nickname, barfees))
            
            if tips:
                self.txt.append(" and got %d in tips" % tips)
            
            self.txt.append(".{/color}")
            
            self.img = self.girl.show("waitress", "maid", exclude=main_sex_tags, resize=(740, 685), type="any")
            
            # Finances:
            self.girl.fin.log_wage(barfees, "Barmaid")
            
            if tips:
                self.girl.fin.log_tips(tips, "Barmaid")
            
            self.loc.fin.log_work_income(barfees + tips, "Barmaid")
            
            self.apply_stats()
            self.finish_job()
    
    
    class Cleaning(Job):
        def cleaning_task(self):
            """
            Solve the job as a cleaner.
            """
            if self.task == 'Cleaning':
                # Stats checks
                cleffect = int(round(self.APr * (12 + self.girl.serviceskill * 0.025 + self.girl.agility * 0.3)))
                
                if self.loc.dirt - cleffect <= 0:
                    self.txt.append("She finished cleaning the building and took a break for the remaining time. \n")
                    self.girlmod['joy'] += choice([0, 0, 1])
                
                elif self.loc.dirt - cleffect > 0:
                    self.txt.append("She spent a good amount of time cleaning the building so girls and customers would be happy. \n")
                
                self.img = self.girl.show("maid", "cleaning", exclude=main_sex_tags, resize=(740, 685), type="any")
                
                # Stat mods
                self.locmod['dirt'] -= cleffect
                self.girlmod['vitality'] -= randint(15, 25) * self.APr
                self.girlmod['exp'] += self.APr * randint(15, 25)
                self.girlmod['service'] += choice([0,0,1])
                
                self.apply_stats()
                self.finish_job()
    

    class ServiceJob(Job):
        """
        The class that solves Bartending, Waitressing and Cleaning.
        """
        def __init__(self):
            """
            This is meant to pick a job that makes most sence out if Cleaning, Service and Bartending
            """
            super(ServiceJob, self).__init__()
            
            # Traits/Job-types associated with this job:
            self.occupations = ["Server"] # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Service"]] # Corresponing traits...
            
        def __call__(self, girl, loc):
            self.girl, self.loc = girl, loc
            
            self.task = None # Service task
            
            # Get the ap cost and cash it
            if self.girl.AP >= 2:
                aprelay = choice([1, 2])
                self.APr = aprelay
                self.girl.AP -= aprelay
            else:
                self.APr = self.girl.AP 
                self.girl.AP = 0
                
            self.girlmod = {}
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
            
            # tl.timer("Bar Brawl Event")
            # if not self.finished: self.bar_brawl_event() TODO: Restore
            # tl.timer("Bar Brawl Event")
            
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
            """
            Checks the girls occupation against the job.
            """
            if [t for t in self.all_occs if t in self.girl.occupations]:
                if self.girl.status == 'slave':
                    self.txt.append(choice(["%s has no choice but to agree to clean and serve tables."%self.girl.fullname,
                                                        "She'll clean and tend to customer needs for you, does not mean she'll enjoy it.",
                                                        "%s is a slave so she'll do as she is told. However you might want to concider giving her work fit to her profession."%self.girl.name]))
                    
                    self.loggs("joy", -3) 
                
                elif self.girl.disposition < 800:
                    self.txt.append(choice(["%s refused to serve! It's not what she wishes to do in life."%self.girl.name,
                                            "%s will not work as a Service Girl, find better suited task for her!"%self.girl.fullname]))
                    
                    self.loggs('disposition', -50)
                    self.img = self.girl.show("profile", "angry", resize=(740, 685))
                    
                    self.girl.action = None
                    self.apply_stats()
                    self.finish_job()
                
                elif self.girl.disposition > 800:
                    self.txt.append("%s reluctently agreed to be a servicer. It's not what she wishes to do in life but she admires you to much to refuse. "%self.girl.name)
            
            else:
                self.txt.append(choice(["%s will work as a service girl!"%self.girl.name,
                                        "Cleaning, cooking, bartending...",
                                        "%s will clean or tend to customers next!"%self.girl.fullname]))
                
            if isinstance(self.txt, list): # TODO: Raised an Error
                self.txt.append("\n")
        
        def set_task(self):
            """
            Sets the task for the girl.
            TODO: Rewrite this whole bit!
            """
            if self.loc.servicer['second_round']:
                if not self.girl.autocontrol['S_Tasks']['clean']:
                    self.txt.append("%s will not clean (check her profile for more information)." % self.girl.nickname)
                    self.img = 'profile'
                    self.apply_stats()
                    self.girls.remove(self.girl)
                    self.finish_job()
                elif self.loc.dirt > 0:
                    self.task = "Cleaning"
                else:
                    self.girls.remove(self.girl)
            
            elif self.loc.get_dirt_percentage()[0] > 80 and not self.girl.autocontrol['S_Tasks']['clean']:
                if self.loc.auto_clean:
                    self.auto_clean()
                    if self.loc.get_dirt_percentage()[0] <= 80:
                        self.set_task()
                        return
                    else:
                        self.txt.append("%s doesn't clean and you do not have the fund to pay proffesional cleaners!" % self.girl.nickname)
                        self.img = 'profile'
                        self.apply_stats()
                        self.girls.remove(self.girl)
                        self.finish_job()
                        return
                        
                elif self.girl.autocontrol['S_Tasks']['clean']:
                    self.txt.append("Your brothel was too dirty for any task but cleaning!")
                    self.task = "Cleaning"
            
            elif self.loc.servicer['barclientsleft'] > 0 or self.loc.servicer['clubclientsleft'] > 0:
                if self.loc.servicer['barclientsleft'] > 0 and self.loc.servicer['clubclientsleft'] > 0:
                    if self.girl.autocontrol['S_Tasks']['bar'] and self.girl.autocontrol['S_Tasks']['waitress']:
                        self.task = choice(['Bar', 'Club'])
                elif self.loc.servicer['barclientsleft'] > 0 and self.girl.autocontrol['S_Tasks']['bar']:
                    self.task = "Bar"
                elif self.loc.servicer['clubclientsleft'] > 0 and self.girl.autocontrol['S_Tasks']['waitress']:
                    self.task = "Club"
                elif self.loc.dirt > 0 and self.girl.autocontrol['S_Tasks']['clean']:
                    self.task = "Cleaning"
                else:
                    self.txt.append("There were no tasks remaining or this girl is not willing to do them (check her profile for more info).")
                    self.img = 'profile'
                    self.apply_stats()
                    self.girls.remove(self.girl)
                    self.finish_job()
            
            elif self.loc.dirt > 0 and self.girl.autocontrol['S_Tasks']['clean']:
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
                        self.txt.append("{color=[red]}%s has spotted a number of customers about to start trouble. "%(self.girl.fullname))
                        self.txt.append("She immediately called for security! \n{/color}")
                        
                        if not solve_job_guard_event(self, "bar_event", clients=self.loc.servicer["barclientsleft"], enemies=aggressive_clients, no_guard_occupation="ServiceGirl"):
                            self.apply_stats()
                            self.finish_job()
                
                if not self.finished:
                    self.txt.append("\n")
        

        

    class GuardJob(Job):
        """
        The class that solve Brothel guard jobs.
        """
        def __init__(self, girl, loc, girls):
            """
            Creates a new GuardJob.
            girl = The girl the job is for.
            loc = The brothel the girl is in.
            girls = The list the girl belongs in.
            """
            super(GuardJob, self).__init__(girl, girls, loc=loc)
            
            self.check_life()
            if not self.finished: self.get_events()
            if not self.finished: self.check_injury()
            if not self.finished: self.check_vitality()
            if not self.finished: self.post_job_activities()
            if not self.finished: self.check_vitality()
            if not self.finished: self.finish_job()
            self.apply_stats()
            
            try:
                self.girls.remove(self.girl)
            
            except:
                dialog.warning("Silent error during GuardJob.__init__, guard was already removed!")
        
        def get_events(self):
            """
            Get the guard events this girl will respond to.
            """
            self.txt.append(choice(["%s worked as guard in %s! \n"%(self.girl.fullname, self.loc.name),
                                    "%s did guard duty in %s! \n"%(self.girl.fullname, self.loc.name)]))
            
            self.txt.append("\n")
            self.img = "battle"
            
            if self.girl.guard_relay['bar_event']['count']:
                if self.girl.has_image("fighting"):
                    self.img = "fighting"
                
                g_events = plural("event", self.girl.guard_relay["bar_event"]["count"])
                
                self.txt.append("She responded to %d brawl %s. "%(self.girl.guard_relay['bar_event']['count'], g_events))
                self.txt.append("That resulted in victory(ies): %d and loss(es): %d! "%(self.girl.guard_relay['bar_event']['won'], self.girl.guard_relay['bar_event']['lost']))
                self.txt.append("\n")
                
                self.girlmod = dict( (n, self.girlmod.get(n, 0)+self.girl.guard_relay['bar_event']['stats'].get(n, 0)) for n in set(self.girlmod)|set(self.girl.guard_relay['bar_event']['stats']) )
            
            if self.girl.guard_relay['whore_event']['count']:
                if self.girl.has_image("fighting"):
                    self.img = "fighting"
                
                g_events = plural("attack", self.girl.guard_relay["whore_event"]["count"])
                
                self.txt.append("With %d victory(ies) and %d loss(es) she settled %d %s on your prostitutes. \n"%(self.girl.guard_relay['whore_event']['won'],
                                                                                                                  self.girl.guard_relay['whore_event']['lost'],
                                                                                                                  self.girl.guard_relay['whore_event']['count'],
                                                                                                                  g_events))
                
                self.girlmod = dict( (n, self.girlmod.get(n, 0)+self.girl.guard_relay['whore_event']['stats'].get(n, 0)) for n in set(self.girlmod)|set(self.girl.guard_relay['whore_event']['stats']) )
                self.txt.append("\n")
        
        def post_job_activities(self):
            """
            Solve the post job events.
            """
            
            if self.girl.AP <= 0:
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
                            
                            while self.girl.AP > 0:
                                self.girlmod['attack'] = self.girlmod.get('attack', 0) + choice([0, 0, 0, 0, 1, guards])
                                self.girlmod['defence'] = self.girlmod.get('defence', 0) + choice([0, 0, 0, 0, 1, guards])
                                self.girlmod['magic'] = self.girlmod.get('magic', 0) + choice([0, 0, 0, 0, 1, guards])
                                self.girlmod['joy'] = self.girlmod.get('joy', 0) + choice([0, 1, 2, 3]) 
                                self.girlmod['vitality'] = self.girlmod.get('vitality', 0) - randint(15, 20)
                                self.girl.AP -=  1
                            
                            self.girlmod['exp'] = self.girlmod.get('exp', 0) + self.girl.AP * randint(8, 12) + 5 * (guards-1) # Moved to prevent insane exp increases at higher levels.    
                        
                        elif guards == 2: 
                            self.txt.append("%s and %s spent time dualing eachother! \n"%(guardlist[0].name, guardlist[1].name))
                            
                            while self.girl.AP > 0:
                                self.girlmod['attack'] = self.girlmod.get('attack', 0) + choice([0,0,0,0,1,guards])
                                self.girlmod['defence'] = self.girlmod.get('defence', 0) + choice([0,0,0,0,1,guards])
                                self.girlmod['magic'] = self.girlmod.get('magic', 0) + choice([0,0,0,0,1,guards])
                                self.girlmod['joy'] = self.girlmod.get('joy', 0) + choice([0,1,2,3]) 
                                self.girlmod['vitality'] = self.girlmod.get('vitality', 0) - randint(15, 20)
                                self.girl.AP -=  1
                            
                            self.girlmod['exp'] = self.girlmod.get('exp', 0) + self.girl.AP * randint(8, 12) + 5
                        
                        elif guards == 1:
                            self.txt.append("%s had the whole Sparring Quarters to herself! \n"%(guardlist[0].name))
                            
                            while self.girl.AP > 0:
                                self.girlmod['attack'] = self.girlmod.get('attack', 0) + choice([0,0,0,0,1,guards])
                                self.girlmod['defence'] = self.girlmod.get('defence', 0) + choice([0,0,0,0,1,guards])
                                self.girlmod['magic'] = self.girlmod.get('magic', 0) + choice([0,0,0,0,1,guards])
                                self.girlmod['joy'] = self.girlmod.get('joy', 0) + choice([0,1,2,3]) 
                                self.girlmod['vitality'] = self.girlmod.get('vitality', 0) - randint(15, 20)
                                self.girl.AP -=  1
                            
                            self.girlmod['exp'] = self.girlmod.get('exp', 0) + self.girl.AP * randint(8, 12)
                
                elif gbu == 2:
                    self.txt.append("She spent remainder of her shift practicing in Training Quarters. \n")
                    
                    while self.girl.AP > 0:
                        self.girlmod['attack'] = self.girlmod.get('attack', 0) + choice([0,0,0,1])
                        self.girlmod['defence'] = self.girlmod.get('defence', 0) + choice([0,0,0,1])
                        self.girlmod['magic'] = self.girlmod.get('magic', 0) + choice([0,0,0,1])
                        self.girlmod['joy'] = self.girlmod.get('joy', 0) + choice([0,1,1,2]) 
                        self.girlmod['vitality'] = self.girlmod.get('vitality', 0) - randint(15, 20)
                        self.girl.AP -= 1
                    
                    self.girlmod['exp'] = self.girlmod.get('exp', 0) + self.girl.AP * randint(8, 12)
                
                elif self.loc.upgrades['guards']['1']['active']:   
                    if dice(50):
                        self.txt.append("She spent time relaxing in Guard Quarters. \n")
                        self.girlmod['vitality'] = self.girlmod.get('vitality', 0) + randint(15, 20) * self.girl.AP
                        self.girl.AP = 0
                    
                    else:
                        self.txt.append("She did some rudamentory training in Guard Quarters. \n")
                        self.girlmod['attack'] = self.girlmod.get('attack', 0) + choice([0,0,0,0,1])
                        self.girlmod['defence'] = self.girlmod.get('defence', 0) + choice([0,0,0,0,1])
                        self.girlmod['magic'] = self.girlmod.get('magic', 0) + choice([0,0,0,0,1])
                        self.girlmod['joy'] = self.girlmod.get('joy', 0) + choice([0,1,1,1]) 
                        self.girlmod['exp'] = self.girlmod.get('exp', 0) +  randint(15, 25)
                        self.girlmod['vitality'] = self.girlmod.get('vitality', 0) - randint(15, 20)
                        self.girl.AP = 0
                
                else:   
                    if dice(50):
                        self.txt.append("She spent time relaxing. \n")
                        
                        #display rest only if they did not fight
                        if not self.girl.guard_relay['bar_event']['count'] and not self.girl.guard_relay['whore_event']['count']:
                            self.img = "rest"
                        
                        self.girlmod['vitality'] = self.girlmod.get('vitality', 0) + randint(7, 12) * self.girl.AP
                        self.girl.AP = 0
                    
                    else:
                        self.txt.append("She did some rudamentory training. \n")
                        self.girlmod['attack'] = self.girlmod.get('attack', 0) + choice([0,0,0,0,0,1])
                        self.girlmod['defence'] = self.girlmod.get('defence', 0) + choice([0,0,0,0,0,1])
                        self.girlmod['magic'] = self.girlmod.get('magic', 0) + choice([0,0,0,0,0,1])
                        self.girlmod['joy'] = self.girlmod.get('joy', 0) + choice([0,1]) 
                        self.girlmod['exp'] = self.girlmod.get('exp', 0) +  randint(8, 15)
                        self.girlmod['vitality'] = self.girlmod.get('vitality', 0) - randint(15, 20)
                        self.girl.AP = 0
