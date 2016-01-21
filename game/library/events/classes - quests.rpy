# Quests

init -9 python:
    
    # Allow easy setting of quest notifications
    USE_QUEST_POPUP = True
    
    def register_quest(*args, **kwargs):
        """
        Registers a new quest in an init block.
        """
        q = WorldQuest(*args, **kwargs)
        world_quests.append(q)
        return q
    
    def register_quest_in_label(*args, **kwargs):
        """
        Registers a new quest in a label.
        """
        q = WorldQuest(*args, **kwargs)
        pytfall.world_quests.quests.append(q)
        return q
    
    class WorldQuestManager(_object):
        """
        Manager for the easy tracking of active, complete, failed and inactive quests.
        """
        
        def __init__(self, data):
            """
            Creates the manager and copies the pre-existsing quests into itself.
            """
            self.active = list()
            self.complete = list()
            self.failed = list()
            self.squelch = list()
            self.quests = deepcopy(data)
        
        def activate_quest(self, quest):
            """
            Activates (starts) a quest.
            """
            if isinstance(quest, str): quest = self.get(quest)
            if quest in self.quests: self.active.append(quest)
            if quest in self.complete: self.complete.remove(quest)
            if quest in self.failed: self.failed.remove(quest)
        
        def add_quest(self, quest, *args, **kwargs):
            """
            Adds a new quest.
            """
            if isinstance(quest, str): quest = WorldQuest(quest, *args, **kwargs)
            self.quest.append(quest)
            if quest.auto is not None: quest.start()
        
        def complete_quest(self, quest):
            """
            Completes a quest.
            """
            if isinstance(quest, str): quest = self.get(quest)
            if quest in self.quests: self.complete.append(quest)
            if quest in self.active: self.active.remove(quest)
            if quest in self.failed: self.failed.remove(quest)
        
        def fail_quest(self, quest):
            """
            Fails a quest.
            """
            if isinstance(quest, str): quest = self.get(quest)
            if quest in self.quests: self.failed.append(quest)
            if quest in self.active: self.active.remove(quest)
            if quest in self.complete: self.complete.remove(quest)
        
        def first_day(self):
            """
            Auto-starts the needed quests on the first day.
            """
            for i in self.quests:
                if i.auto is not None: i.start()
        
        def get(self, name):
            """
            Returns the named quest.
            """
            for i in self.quests:
                if i.name == name: return i
            else: return None
        
        def check_stage(self, quest):
            """Safe way of checking a stage of a quest.
            
            Will return the number of quest stage if quest is active, -1 otherwise.
            """
            return self.get(quest).stage
            
        def check_quest_not_finished(self, *quests):
            """Will return False if at least one quest is completed or failed, True otherwise.
            """
            for quest in quests:
                if self.is_complete(quest) or self.has_failed(quest):
                    return False
            return True
            
        def all_finished(self, *quests):
            """Will return True if all quests provided as arguments are completed or finished.
            False otherwise.
            """
            bools = []
            for quest in quests:
                bools.append(self.is_complete(quest) or self.has_failed(quest))
            if all(bools):
                return True
            else:
                return False
            
        def has_failed(self, quest):
            """Whether a quest has been failed.
            """
            if isinstance(quest, str): quest = self.get(quest)
            return quest in self.failed
        
        def is_active(self, quest):
            """Whether a quest is active.
            """
            if isinstance(quest, str): quest = self.get(quest)
            return quest in self.active
        
        def is_complete(self, quest):
            """Whether a quest is complete.
            """
            if isinstance(quest, str): quest = self.get(quest)
            return quest in self.complete
        
        def is_squelched(self, quest):
            """Whether a quest has been squelched.
            """
            if isinstance(quest, str): quest = self.get(quest)
            return quest in self.squelch
        
        def kill_quest(self, quest):
            """Removes a quest.
            """
            if isinstance(quest, str): quest = self.get(quest)
            if self.is_active(quest): self.active.remove(quest)
            if self.is_complete(quest): self.complete.remove(quest)
            self.quests.remove(quest)
        
        def next_day(self):
            """Fails quests that have no valid events.
            """
            garbage = list()
            
            # Find incomplete quests with no existing events
            for i in self.active:
                for j in pytfall.world_events.events_cache:
                    if j.quest == i.name:
                        break
                
                else:
                    if not i.manual: garbage.append(i)
            
            while len(garbage) > 0:
                devlog.warning("Garbage Quest found! \"%s\" was failed."%garbage[0].name)
                self.fail_quest(garbage.pop())
        
        def run_quests(self, param=None):
            """Unsquelches all quests so they can report for a new location if needed.
            Definition same as WorldEventsManager.run_quests for convenience.
            
            param = Optional for mirroring of WorldEventsManager, currently doesn't do anything.
            """
            del self.squelch[:]
        
        def squelch_quest(self, quest):
            """Squelches a quest so it doesn't provide any more updates.
            """
            if isinstance(quest, str): quest = self.get(quest)
            if self.is_active(quest): self.squelch.append(quest)
        
        def unsquelch_quest(self, quest):
            """Unsquelches a quest so it can provide updates.
            """
            if isinstance(quest, str): quest = self.get(quest)
            if self.is_squelched(quest): self.squelch.remove(quest)
        
    
    class WorldQuest(_object):
        """
        Class to hold the current status of a quest.
        """
        def __init__(self, name, auto=None, manual=None):
            """
            Creates a new Quest.
            name = The name of the quest. Use to refer to this quest, and shows up in the Quest log.
            auto = Whether to automatically start the quest on day 1.
                Valid auto formats:
                    auto="prompt"
                    auto=("prompt",)
                    auto=("prompt", ["flags"])
                    auto=("prompt", 17)
                    auto=("prompt", "flag")
                    auto=("prompt", ["flags"], 17)
                    auto=("prompt", "flag1", "flag2", "flagN", 17)
                    auto=("prompt", "flag1", "flag2", "flagN")
                Note: 17 = 'to' param
            
            manual = Whether the quest will be manually updated, instead of by event. Prevents garbage failing.
            """
            self.name = name
            self.prompts = list()
            self.stage = 0
            self.flags = list()
            self.auto = auto
            self.manual = manual
        
        def __contains__(self, obj):
            """
            Checks for the existance of flags.
            """
            return obj in self.flags
        
        def __str__(self):
            return "Quest(%s)" % self.name
        
        @property
        def active(self):
            """
            Whether this quest is active.
            """
            return pytfall.world_quests.is_active(self)
        
        def check(self, stage, strict, *flags):
            """
            Checks whether the quest is at a certain state.
            Used for easy checking through WorldEvent.run_conditions.
            """
            if strict and self.stage != stage: return False
            if not strict and self.stage < stage: return False
            for i in flags:
                if i not in self: return False
            
            return True
        
        @property
        def complete(self):
            """
            Whether this quest is complete.
            """
            return pytfall.world_quests.is_complete(self)
        
        def condition(self, stage, strict=False, *flags):
            """
            Builds a condition check string for WorldEvent.run_conditions.
            """
            if flags is not None and len(flags) > 0:
                return "pytfall.world_quests.get(\"%s\").check(%s, %s, %s)"%(self.name, str(stage), True if strict else False, "\"" + "\", \"".join(flags) + "\"")
            else:
                return "pytfall.world_quests.get(\"%s\").check(%s, %s)"%(self.name, str(stage), True if strict else False)
        
        @property
        def failed(self):
            """
            Whether this quest has been failed.
            """
            return pytfall.world_quests.has_failed(self)
        
        def finish(self, prompt, *flags, **kwargs):
            """
            Finishes the quest in menus, etc.
            prompt = Prompt to add to the Quest log.
            flags = List of strings to add to the Quest as flags.
            to = Stage to jump to instead of current+1.
            """
            if not self.complete: pytfall.world_quests.complete_quest(self)
            
            self.prompts.append(prompt)
            for i in flags: self.flag(i)
            self.stage = kwargs.get("to", self.stage+1)
            
            devlog.info("Quest Complete: %s"%self.name)
            
            if USE_QUEST_POPUP:
                if "in_label" not in kwargs: renpy.show_screen("message_screen", "Quest Complete:\n%s"%self.name)
                else: renpy.call_screen("message_screen", "Quest Complete:\n%s"%self.name, use_return=True)
                
                # No squelch, as only works on active quests
        
        def finish_in_label(self, *args, **kwargs):
            """
            Finishes the quest in labels.
            prompt = Prompt to add to the Quest log.
            flags = List of strings to add to the Quest as flags.
            """
            self.finish(*args, in_label=True, **kwargs)
        
        def flag(self, tag):
            """
            Adds a flag to the quest.
            """
            if tag not in self: self.flags.append(tag)
        
        def next(self, prompt, *flags, **kwargs):
            """
            Adds a stage to the quest in menus, etc.
            prompt = Prompt to add to the Quest log.
            flags = List of strings to add to the Quest as flags.
            to = Stage to jump to instead of current+1.
            """
            if not self.active: pytfall.world_quests.activate_quest(self)
            
            self.prompts.append(prompt)
            for i in flags: self.flag(i)
            self.stage = kwargs.get("to", self.stage+1)
            self.manual = kwargs.get("manual", self.manual)
            
            devlog.info("Update Quest: %s to %s"%(self.name, str(self.stage)))
            
            if USE_QUEST_POPUP:
                if len(self.prompts) == 1:
                    if "in_label" not in kwargs: renpy.show_screen("message_screen", "New Quest:\n%s"%self.name)
                    else: renpy.call_screen("message_screen", "New Quest:\n%s"%self.name, use_return=True)
                
                elif not self.squelched:
                    if "in_label" not in kwargs: renpy.show_screen("message_screen", "Quest Updated:\n%s"%self.name)
                    else: renpy.call_screen("message_screen", "Quest Updated:\n%s"%self.name, use_return=True)
                
                pytfall.world_quests.squelch_quest(self)
        
        def next_in_label(self, *args, **kwargs):
            """
            Adds a stage to the quest in labels.
            prompt = Prompt to add to the Quest log.
            flags = List of strings to add to the Quest as flags.
            to = Stage to jump to instead of current+1.
            """
            self.next(*args, in_label=True, **kwargs)
        
        @property
        def squelched(self):
            """
            Whether this quest has been squelched.
            """
            return pytfall.world_quests.is_squelched(self)
        
        def start(self):
            """
            Starts a quest using its auto property.
            """
            if not self.active: pytfall.world_quests.activate_quest(self)
            
            if isinstance(self.auto, (tuple,list)):
                if len(self.auto) == 1: self.next(self.auto)
                elif len(self.auto) == 2:
                    if isinstance(self.auto[1], (tuple,list)): self.next(self.auto[0], *self.auto[1])
                    elif isinstance(self.auto[1], int): self.next(self.auto[0], to=self.auto[1])
                    else: self.next(*self.auto)
                
                else:
                    if isinstance(self.auto[1], (tuple,list)): self.next(self.auto[0], *self.auto[1], to=self.auto[2])
                    elif isinstance(self.auto[-1], int): self.next(self.auto[0], *self.auto[1:-1], to=self.auto[-1])
                    else: self.next(*self.auto)
            
            else:
                self.next(self.auto)
            
            devlog.info("Auto-Start Quest: %s"%self.name)
            
            if USE_QUEST_POPUP:
                # Called in mainscreen, show works
                renpy.show_screen("message_screen", "New Quest:\n%s"%self.name, use_return=True)
                pytfall.world_quests.squelch_quest(self)
        
    
