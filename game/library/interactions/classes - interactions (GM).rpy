init -1 python:
    class GmCell(_object):
        """
        Simple custom container for girls to be displayed to the player.
        Also responsible for sorting.
        Occupation = condition on which to sort.
        """
        def __init__(self, name, curious_priority=True, **kwargs):
            goodoccupations = kwargs.get("goodoccupations", set())
            badoccupations = kwargs.get("badoccupations", set())
            has_tags = kwargs.get("has_tags", set())
            has_no_tags = kwargs.get("has_no_tags", set())
            goodtraits = kwargs.get("goodtraits", set())
            if goodtraits:
                goodtraits = set(traits[t] for t in goodtraits)
                
            badtraits = kwargs.get("badtraits", set())
            if badtraits:
                badtraits = set(traits[t] for t in badtraits)
                
            self.name = name
            self.curious_priority = curious_priority
            self.girls = list()
            # Get available girls and check occupation
            if not(has_tags):
                choices = list(i for i in chars.values() if i not in hero.chars and not i.arena_active and i.location in ["city", "girl_meets_quest"] and i not in gm.get_all_girls())
            else:
                choices = list(i for i in chars.values() if i not in hero.chars and not i.arena_active and i.location in ["city", "girl_meets_quest"] and i not in gm.get_all_girls() and i.has_image(*has_tags, exclude=has_no_tags))
            # We remove all chars with badtraits:
            if badtraits:
                choices = list(i for i in choices if not any(trait in badtraits for trait in i.traits))
            if badoccupations:
                choices = list(i for i in choices if not i.occupations.intersection(badoccupations))
            conditioned_choices = set(choices)
            
            if self.curious_priority:
                goodtraits.add(traits["Curious"])
            gt = list(i for i in conditioned_choices if any(trait in goodtraits for trait in i.traits)) if goodtraits else list()
            occs = list(i for i in conditioned_choices if i.occupations.intersection(goodoccupations)) if goodoccupations else list()
            conditioned_choices = list(conditioned_choices.intersection(gt + occs)) if gt or occs else list(conditioned_choices)
            
            # Sort the list based on disposition:
            conditioned_choices.sort(key=attrgetter("disposition"))
            choices.sort(key=attrgetter("disposition"))
            
            # =====================================>>>
            # We add an absolute overwrite for any character that has the location string set as the name:
            # Make sure that we do not get the char in two locations on the same day:
            local_chars = list()
            for c in chars.values():
                if c.location == name:
                    if c in gm.get_all_girls():
                        gm.remove_girl(c)
                    local_chars.append(c)
            shuffle(local_chars)
            while local_chars and len(self.girls) < 3:
                self.girls.append(local_chars.pop())
            
            # Append to the list (1st girl) Best disposition:
            # This whole codebit needs to be rewritten when Interactions are restructured.
            if conditioned_choices and len(self.girls) < 3:
                if not conditioned_choices[len(conditioned_choices)-1].disposition:
                    shuffle(conditioned_choices)
                    self.girls.append(conditioned_choices.pop())
                else:
                    self.girls.append(conditioned_choices.pop())
            elif choices and len(self.girls) < 3:
                if not choices[len(choices)-1].disposition:
                    shuffle(choices)
                    self.girls.append(choices.pop())
                else:
                    self.girls.append(choices.pop())
                
            # Last two, Second one should be an Unique char, Third = Any char:
            shuffle(conditioned_choices)
            while conditioned_choices and len(self.girls) < 3:
                for i in conditioned_choices:
                    if i.__class__ == Char:
                        self.girls.append(i)
                        conditioned_choices.remove(i)
                        break
                if conditioned_choices and len(self.girls) < 3:
                    self.girls.append(conditioned_choices.pop())
                # In the perfect world, we'd be done... yet...
                    
            # This last bit we do in case conditioned choices had failed:
            if len(self.girls) < 3:
                choices = list(i for i in choices if i not in self.girls)
                shuffle(choices)
                while choices and len(self.girls) < 3:
                    for i in choices:
                        if i.__class__ == Char:
                            self.girls.append(i)
                            choices.remove(i)
                            break
                    if len(self.girls) < 3:        
                        self.girls.append(choices.pop())
                    
            if len(self) > 3:
                raise Exception("Something went wrong during girls sorting in {}.\n List: {}".format(self.__class__.__name__, ", ".join(c.name for c in self)))
            self.termination_day = day + randint(3, 5)
            self.creation_day = day
            
        # and easy access:
        def __len__(self):
            return len(self.girls)
            
        def __iter__(self):
            return iter(self.girls)
            
        def __getitem__(self, index):
            return self.girls[index]
            
        def __nonzero__(self):
            return bool(self.girls)
        
    
    class GirlsMeets(_object):
        """
        Girlsmeets control system, handles all related logic
        """
        
        # List of modes to use the girl_interactions label with.
        USE_GI = ["girl_meets", "girl_interactions", "girl_trainings"]
        
        def __init__(self):
            """
            Creates a new GirlsMeets.
            There should be no lists in this classes dictionary except for girl_meets ones.
            """
            # Mode and caches
            self.mode = None
            self.img_size = (600, 515) # Img size we automatically use for girlsmeets.
            self.label_cache = ""
            self.bg_cache = ""
            self.jump_cache = ""
            self.img_cache = Null()
            
            # Current interaction
            self.char = None
            self.img = ""
            self.gm_points = 0
            
            # Cells
            self.girlcells = dict()
            
            # Display flags
            self.see_greeting = True
            self.show_girls = False
            self.show_menu = False
            self.show_menu_givegift = False
        
        # Charcters Control:
        def display_girls(self):
            """
            Should simply return a list of girls for display.
            """
            if self.label_cache in self.girlcells:
                return self.girlcells[self.label_cache]
            
            else:
                return list()
        
        def get_all_girls(self):
            """
            Returns a list of all girls currently in girl_meets.
            """
            l = list()
            
            for cell in self.girlcells.values():
                for girl in cell:
                    l.append(girl)
            
            return l
            
        def remove_girl(self, char):
            """
            Removes a girl from the girl_meets.
            """
            for cell in self.girlcells.values():
                if char in cell:
                    cell.girls.remove(char)
        
        # Image Controls:
        def set_img(self, *args, **kwargs):
            """Sets the image, leaving the image cache untouched.
            """
            kwargs["resize"] = kwargs.get("resize", self.img_size)
            self.img = self.char.show(*args, **kwargs)
            
        def restore_img(self): 
            """Restores the image to the cached one.
            """   
            self.img = self.img_cache
        
        # Interactions/GM Flow Controls:
        def jump(self, label, free=False, allow_unique=True, **kwargs):
            """Jumps to a GMIT label with the most specific name.
            
            label = The label to jump to.
            free = Whether the interaction is free.
            allow_unique Whether to allow girl.id specific labels.
            kwargs = Holder of the "allow_mode" arguments.
            """
            ls = list()
            
            # If we are allowed mode specific labels
            if kwargs.pop("allow_" + self.mode, True):
                # If we are allowed unique labels
                if allow_unique:
                    # Add the mode specific girl unique label
                    ls.append("{}_{}_{}".format(self.mode, label, self.char.id))
                
                # Add the mode specific label
                ls.append("{}_{}".format(self.mode, label))
            
            # If we are allowed unique labels
            if allow_unique:
                # Add the girl unique label
                ls.append("{}_{}".format(label, gm.char.id))
            
            # Add the generic label
            ls.append("interactions_{}".format(label))
            
            # If we have labels
            for l in ls:
                # If the label exists
                if renpy.has_label(l):
                    self.jump_cache = l
                    break
            else:
                # Try just the label name...:
                if renpy.has_label(label):
                    self.jump_cache = label
                    l = label
                else:
                    # Notify and stop:
                    notify("Unable to find GM label {}.".format(label))
                    self.jump_cache = ""
                    return
            
            # If the action costs AP:
            if not free:
                # If we have no more points
                if not self.gm_points and hero.AP <= 0:
                    renpy.show_screen("message_screen", "You have no Action Points left!")
                    return
                else:
                    # Take AP
                    if not self.gm_points:
                        hero.take_ap(1)
                        self.gm_points = 3
                
                # Take points
                self.gm_points -= 1
            
            # Notify and jump
            self.show_menu = False
            renpy.jump(l)
            
        def start(self, mode, girl, img=None, exit=None, bg=None):
            """Starts a girl meet scenario.
            
            mode = The mode to use.
            girl = The girl to use.
            img = The image to use.
            exit = The exit label to use. Overrides enter_location.
            """
            self.mode = mode
            self.char = girl
            
            hs() # Kill the current screen...
            
            if exit is not None:
                self.label_cache = exit
                self.bg_cache = "bg " + (bg or exit)
            
            elif bg is not None:
                self.bg_cache = bg
            
            # Routine to get the correct image for this interaction:
            if img is None:
                self.img = self.char.get_img_from_cache(str(last_label))
                if not self.img:
                    self.img = self.char.show("profile", resize=self.img_size, exclude=["nude", "bikini", "swimsuit", "beach", "angry", "scared", "ecstatic"])
            else:
                self.img = img
            self.img_cache = self.img
            
            store.char = girl
            
            if mode in self.USE_GI:
                jump("girl_interactions")
            else:
                jump(mode)
        
        def start_gm(self, girl, img=None, exit=None, bg=None):
            """
            Starts the girlsmeet scenario.
            girl = The girl to use.
            img = The image for the girl.
            exit = The exit label to use. Use to override enter_location function.
            bg = The background to use. Use to override enter_location function.
            """
            if girl.flag("_day_countdown_interactions_blowoff"):
                renpy.call("interactions_blowoff", char=girl, exit=last_label)
            
            if girl.location == "girl_meets_quest":
                self.start(girl.id, girl, img, exit, bg)
            else:
                self.start("girl_meets", girl, img, exit, bg)
        
        def start_int(self, girl, img=None, exit="char_profile", bg="gallery"):
            """
            Starts the interaction scenario.
            girl = The girl to use.
            img = The image for the girl.
            exit = The exit label to use. Defaults to "char_profile".
            bg = The background to use. Defaults to "gallery".
            """
            if girl.flag("_day_countdown_interactions_blowoff"):
                renpy.call("interactions_blowoff", char=girl, exit=last_label)
            
            self.start("girl_interactions", girl, img, exit, bg)
        
        def start_tr(self, girl, img=None, exit="char_profile", bg="bg sex_dungeon_1"):
            """
            Starts the training scenario.
            girl = The girl to use.
            img = The image for the girl.
            exit = The exit label to use. Defaults to "char_profile".
            bg = The background to use. Defaults to "dungeon".
            """
            self.start("girl_trainings", girl, img, exit, bg)
            
        def enter_location(self, **kwargs):
            """
            Enters the current location for the GM system.
            """
            self.label_cache = str(last_label)
            self.bg_cache = " ".join(["bg", self.label_cache])
            self.show_girls = False
            
            # Creation:
            if self.label_cache not in self.girlcells:
                cell = GmCell(self.label_cache, **kwargs)
                if cell:
                    self.girlcells[self.label_cache] = cell
        
        def end(self, safe=False):
            """
            Ends the current scenario.
            safe = Whether to prevent the label jump.
            """
            # Music flag:
            if not self.mode in self.USE_GI and renpy.music.get_playing(channel='world'):
                global_flags.set_flag("keep_playing_music")
            
            # Reset GM counters
            gm_disp_mult = 1
            
            # Reset scene
            renpy.scene()
            renpy.hide_screen("girl_interactions")
            
            self.see_greeting = True
            self.show_menu = False
            self.show_menu_givegift = False
            if not safe:
                renpy.jump(self.label_cache)
    
                
    class GMJump(Action):
        """
        Class to handle the jump logic for GM as an action.
        """
        def __init__(self, label, free=False, allow_unique=True, **kwargs):
            """
            Creates a new GMJump.
            label = The label to jump to.
            free = Whether the interaction is free.
            allow_unique = Whether to allow girl-specific labels.
            kwargs = Holder of the "allow_mode" arguments.
            """
            self.label = label
            self.free = free
            self.allow_unique = allow_unique
            self.kwargs = kwargs
        
        def __call__(self):
            """
            Functions the jump.
            """
            gm.jump(self.label, free=self.free, allow_unique=self.allow_unique, **self.kwargs)
