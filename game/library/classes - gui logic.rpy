init -1 python:
    # GUI Logic ---------------------------------------------------------------------------------------------
    class GuiItemsTransfer(_object):
        '''Alex: On Rudis advice and out of common sense
        I want to try and package some of the screen logic into classes
        This will be my first attempt on doing so
        This way we might be able to keep global namespace a little bit cleaner
        And maybe even improve code readability
        This is still used in combination with RenPy screen language as I do not like to code GUI in pure python 
        '''
        def __init__(self, location, char=None, last_label=None):
            '''Takes location (so far we only have brothels) as an argument'''
            self.left_char = None
            self.right_char = None
            self.left_image_cache = None
            self.right_image_cache = None
            
            if location == "personal_transfer":
                self.location = location
                self.select_left_char(hero)
                self.left_char.inventory.apply_filter("all")
                self.select_right_char(char)
                self.right_char.inventory.apply_filter("all")
            else:    
                self.location = location

            self.left_item = None
            self.right_item = None
            self.items_amount = 1
            self.filter = 'all'
            self.item_cache = None
            self.last_label = last_label
            
            
        def populate_character_viewports(self):
            '''Populates viewports with characters if true'''
            if isinstance(self.location, UpgradableBuilding): # Updated to allow TrainingDungeon to work as well, might need to change later
                # Later we may want to call this from girls profile screen/hero profile screen
                # Right now this check is redundant
                members = self.location.get_girls()
                if hero.location == self.location:
                    members.insert(0, hero)
                
                if members: return [True, members]
                else: return [False]
                
            elif self.location == "personal_transfer":
                members = [hero, self.right_char]
                return [True, members]
                
        def show_left_items_selection(self):
            '''Populates left items selection viewport'''
            if self.left_char != None:
                return True
            else: return False
            
        def show_right_items_selection(self):
            '''Populates right items selection viewport'''
            if self.right_char != None:
                return True
            else: return False
            
        def select_left_char(self, char):
            char.inventory.set_page_size(23)
            if char == self.right_char:
                renpy.show_screen('pyt_message_screen', "Same character cannot be chozen from both sides!")
            else:
                self.left_char = char
                self.left_image_cache = self.left_char.show('portrait', resize=(205, 205))
        
        def select_right_char(self, char):
            char.inventory.set_page_size(23)
            if char == self.left_char:
                renpy.show_screen('pyt_message_screen', "Same character cannot be chozen from both sides!")
            else:
                self.right_char = char
                self.right_image_cache = self.right_char.show('portrait', resize=(205, 205))
        
        def select_left_item(self, item):
            self.left_item = item
            self.item_cache = item
        
        def select_right_item(self, item):
            self.right_item = item
            self.item_cache = item
            
        def show_right_transfer_button(self):
            if self.left_item and self.right_char:
                return True
            else:
                return False
                
        def show_left_transfer_button(self):
            if self.right_item and self.left_char:
                return True
            else:
                return False
                
        
        def get_left_inventory(self):
            return [item for item in self.left_char.inventory.getpage()]

            
        def get_right_inventory(self):
            return [item for item in self.right_char.inventory.getpage()]

                
        def transfer_item_right(self):
            item = self.left_item
            source = self.left_char
            target = self.right_char
            for i in range(self.items_amount):
                if item.id in source.inventory.content:
                    if not transfer_items(source, target, item):
                        # Otherwise MC will say this in case of unique/quest items trasnfer refusal.
                        if source != hero:
                            source.say(choice(["Like hell am I giving away!", "Go get your own!", "Go find your own %s!" % item.id,"Would you like fries with that?",
                                                           "Perhaps you would like me to give you the key to my flat where I keep my money as well?"]))
                        break
                else:
                    break
            if item.id not in source.inventory.content:                
                self.left_item = None

        def transfer_item_left(self):
            item = self.right_item
            source = self.right_char
            target = self.left_char
            for i in range(self.items_amount):
                if item.id in source.inventory.content:
                    if not transfer_items(source, target, item):
                        # Otherwise MC will say this in case of unique/quest items trasnfer refusal.
                        if source != hero:
                            source.say(choice(["Like hell am I giving away!", "Go get your own!", "Go find your own %s!" % item.id, "Would you like fries with that?",
                                                           "Perhaps you would like me to give you the key to my flat where I keep my money as well?"]))
                        break
                else:
                    break
            if item.id not in source.inventory.content:                
                self.right_item = None
                
            
    class GuiGirlsList(_object):
        """
        Used for sorting girls in the list and maybe in profile screen in the future
        """
        STATUS_GROUP = 'status'
        OCCUPATION_GROUP = 'occupation'
        ACTION_GROUP = 'action'
        BUILDING_GROUP = 'building'

        def __init__(self):
            self.sorted = list(girl for girl in hero.girls if girl.action != "Exploring")
            self.init_display_filters()
            self.init_active_filters()
            
            self.page = 0
            self.total_pages = 1

        def init_display_filters(self):
            self.display_filters = [
                ('Status', [
                    ['Free', self.STATUS_GROUP, 'free'],
                    ['Slaves', self.STATUS_GROUP, 'slave'],
                    ["Run away", self.ACTION_GROUP, RunawayManager.ACTION] # Put here as "status" makes more sense then "job"
                ]),
                ('Current job', [
                    ['None', self.ACTION_GROUP, None],
                    ['Whore', self.ACTION_GROUP, 'Whore'],
                    ['Guard', self.ACTION_GROUP, 'Guard'],
                    ['Service Girl', self.ACTION_GROUP, 'ServiceGirl'],
                ]),
                ('Courses', [
                    [course_name, self.ACTION_GROUP, course_action] for course_name, course_action in get_all_courses()
                ]),
                ('Occupation', [
                    ['Prostitutes', self.OCCUPATION_GROUP, traits['Prostitute']],
                    ['Strippers', self.OCCUPATION_GROUP, traits['Stripper']],
                    ['Warriors', self.OCCUPATION_GROUP, 'Warrior'],
                    ['Service Girls', self.OCCUPATION_GROUP, 'Server'],
                ]),
                ('Buildings', [
                    [building.name, self.BUILDING_GROUP, building] for building in list(b for b in hero.buildings if b.__class__ != Apartment)
                ]),
            ]

        def init_active_filters(self):
            self.active_filters = {
                self.STATUS_GROUP: set(),
                self.OCCUPATION_GROUP: set(),
                self.BUILDING_GROUP: set(),
                self.ACTION_GROUP: set(),
            }

        def clear(self):
            self.sorted = copy.copy(hero.girls)
            self.init_active_filters()
            renpy.restart_interaction()

        def add_filter(self, group, item):
            if item not in self.active_filters[group]:
                self.active_filters[group] = set([item])
            else:
                self.active_filters[group].remove(item)

        def sort_by_status(self, girl_list):
            for status in self.active_filters[self.STATUS_GROUP]:
                girl_list = list(girl for girl in girl_list if girl.status == status)
            return girl_list

        def sort_by_occupation(self, girl_list):
            for occupation in self.active_filters[self.OCCUPATION_GROUP]:
                girl_list = list(girl for girl in girl_list if occupation in girl.occupations)
            return girl_list

        def sort_by_action(self, girl_list):
            for action in self.active_filters[self.ACTION_GROUP]:
                girl_list = list(girl for girl in girl_list if girl.action == action)
            return girl_list

        def sort_by_brothel(self, girl_list):
            for building in self.active_filters[self.BUILDING_GROUP]:
                girl_list = list(girl for girl in girl_list if girl.location == building)
            return girl_list

        def get_sorted(self):
            return self.sort_by_brothel(
                self.sort_by_occupation(
                    self.sort_by_action(
                        self.sort_by_status(self.sorted)
                    )
                )
            )

        def get_focus(self, filter_group, filter_key):
            return filter_key in self.active_filters[filter_group]

    class SlaveMarket(Location):
        """
        Class for populating and running of the slave market.
        """
        def __init__(self, type = []):
            """
            Creates a new SlaveMarket.
            type = type girls predominatly present in the market. Not used.
            """
            super(SlaveMarket, self).__init__()
            self.id = "PyTFall Slavemarket"
            self.type = type
            
            self.girl = None
            
            self.girls_list = None
            self.blue_girls = dict() # Girls (SE captured) blue is training for you.
            self.restock_day = randint(2, 3)
        
        def get_girls(self):
            """
            Generates a random list of girls.
            """
            candidates = list(self.actors)
            shuffle(candidates)
            sglist = list()
            uniques = 0
            randoms = 0
            for girl in candidates:
                if girl.__class__ == Girl and uniques < 5:
                    sglist.append(girl)
                    uniques += 1
                if girl.__class__ == rGirl and randoms < 5:
                    sglist.append(girl)
                    randoms += 1
            shuffle(sglist)
            return sglist
        
        @property
        def girlfin(self):
            """
            The property to return the proper financial data for the girl.
            """
            return self.girl.fin
        
        def populate_girls_list(self):
            """
            Populates the list of girls that are available.
            """
            girls_list = self.get_girls()
            self.girls_list = list()
            for i in range(randint(6, 8)):
                if girls_list:
                    self.girls_list.append(girls_list.pop())
                    
        def buy_girl(self):
            """
            Buys the focused girl from the market.
            """
            if hero.take_ap(1):
                if hero.take_money(self.girl.fin.get_price(), reason="Slave Purchase"):
                    renpy.play("content/sfx/sound/world/purchase_1.ogg")
                    hero.add_girl(self.girl)
                    self.girls_list.remove(self.girl)
                    
                    if self.girls_list:
                        self.girl = choice(self.girls_list)
                        self.index = self.girls_list.index(self.girl)
                    
                    else:
                        self.girl = None
                
                else:
                    renpy.call_screen('pyt_message_screen', "You don't have enough money for this purchase!")
            
            else:
                renpy.call_screen('pyt_message_screen', "You don't have enough AP left for this action!!")
            
            if not self.girls_list:
                renpy.hide_screen("pyt_slave_shopping")
        
        def next_day(self):
            """
            Solves the next day logic.
            """
            if self.restock_day == day:
                self.populate_girls_list()
                self.restock_day += randint(2, 3)
                
            for g in self.blue_girls.keys():
                self.blue_girls[g] += 1
                if self.blue_girls[g] == 30:
                    hero.add_girl(g)
                    del self.blue_girls[g]
                    pytfall.temp_text.append("Blue has finished training %s! The girl has been delivered to you!" % chars[g].name)
            
        def next_index(self):
            """
            Sets the focus to the next girl.
            """
            if self.girls_list:
                index = self.girls_list.index(self.girl)
                index = (index + 1) % len(self.girls_list)
                self.girl = self.girls_list[index]
                
        def previous_index(self):
            """
            Sets the focus to the previous girl.
            """
            if self.girls_list:
                index = self.girls_list.index(self.girl)
                index = (index - 1) % len(self.girls_list)
                self.girl = self.girls_list[index]
        
        def set_index(self):
            """
            Sets the focus to a random girl.
            """
            if self.girls_list:
                self.girl = choice(self.girls_list)
        
        def set_girl(self, girl):
            """
            Sets the focus to the given girl.
            girl = The girl to set the focus to.
            """
            if self.girls_list and girl in self.girls_list:
                self.girl = girl
        
    
    class GuiHeroProfile(_object):
        '''The idea is to try and turn the while loop into the function
        I want girl_meets and quests to work in similar way
        This is basically practicing :)
        '''
        def __init__(self):
            self.show_item_info = False
            self.item = False
            
            self.finance_filter = "day"
            self.came_from = None # To enable jumping back to where we originally came from.

        def screen_loop(self):
            hero.inventory.set_page_size(18)
            # self.came_from = repr(last_label)

            while 1:
                result = ui.interact()
                
                # To kill input error during team renaming:
                if not result:
                    pass
                
                elif result[0] == 'control':
                    if result[1] == 'return':
                        self.show_item_info = False
                        self.item = False
                        renpy.hide_screen("pyt_hero_profile")
                        renpy.hide_screen("pyt_hero_equip")
                        
                        # Reset filters (prevents crap from happening in shops):
                        hero.inventory.male_filter = False
                        hero.inventory.apply_filter('all')
                        
                        # Taking care of Ren'Pys annoying reserves... <-- Prolly obsolete after I rewrote the last label func.
                        if self.came_from.startswith("_"):
                            jump("mainscreen")
                        else:    
                            jump(self.came_from)
                            
                elif result[0] == "dropdown":
                    if result[1] == "loc":
                        renpy.show_screen("pyt_hero_dropdown_loc", pos=renpy.get_mouse_pos())
                        
                elif result[0] == 'hero':
                    if result[1] == 'equip':
                        if renpy.get_screen('pyt_hero_equip'):
                            renpy.hide_screen('pyt_hero_equip')
                            self.show_item_info = False
                            self.item = False
                        else:    
                            renpy.show_screen('pyt_hero_equip')
                            
                    elif result[1] == 'first_page': hero.inventory.first()
                    elif result[1] == 'last_page': hero.inventory.last()
                    elif result[1] == 'next_page': hero.inventory.next()
                    elif result[1] == 'prev_page': hero.inventory.prev()
                    elif result[1] == 'prev_filter': hero.inventory.apply_filter('prev')
                    elif result[1] == 'next_filter': hero.inventory.apply_filter('next')
                    elif result[1] == 'male_filter':
                        hero.inventory.male_filter = True
                        hero.inventory.apply_filter('all')
                    elif result[1] == 'unisex_filter':
                        hero.inventory.male_filter = False
                        hero.inventory.apply_filter('all')
                    
                elif result[0] == 'item':
                    if result[1] == 'get':
                        self.show_item_info = True
                        self.item = result[2]

                    elif result[1] == 'equip':
                        equip_item(self.item, hero)
                        self.show_item_info = False
                        self.item = False
                        
                    elif result[1] == "transfer":
                        renpy.hide_screen("pyt_hero_profile")
                        pytfall.it = GuiItemsTransfer("personal_transfer", char=ap, last_label=last_label)
                        jump("items_transfer")
                        
                    elif result[1] == 'unequip':
                        hero.unequip(self.item)
                        self.show_item_info = False
                        self.item = False

                elif result[0] == "remove_from_team":
                    hero.team.remove(result[1])
                    
                elif result[0] == "rename_team":
                    if result[1] == "set_name":
                        hero.team.name = renpy.call_screen("pyt_ht_input")
             
        def show_unequip_button(self):
            if self.item and self.item in hero.eqslots.values():
                return True
                
        def show_equip_button(self):
            if self.item and self.item.sex != "female" and self.item.id in hero.inventory.content:
                return True
                
                
    class PytGallery(_object):
        """
        PyTFall gallery to view girl's pictures and controls
        """
        def __init__(self, char):
            self.girl = char
            self.imgsize = (960, 660)
            self.tag = "profile"
            self.tagsdict = tagdb.get_tags_per_character(self.girl)
            self.td_mode = "full" # Tagsdict Mode (full or dev)
            self.pathlist = list(tagdb.get_imgset_with_all_tags(set([char.id, "profile"])))
            self.imagepath = self.pathlist[0]
            self.image = ProportionalScale(self.pathlist[0], 940, 645)
            self.tags = " | ".join([i for i in tagdb.get_tags_per_path(self.imagepath)])
        
        def screen_loop(self):
            while 1:
                result = ui.interact()
                
                if result[0] == "image":
                    index = self.pathlist.index(self.imagepath)
                    if result[1] == "next":
                        index = (index + 1) % len(self.pathlist)
                        self.imagepath = self.pathlist[index]
                        self.set_img()

                    elif result[1] == "previous":
                        index = (index - 1) % len(self.pathlist)
                        self.imagepath = self.pathlist[index]
                        self.set_img()
                    
                elif result[0] == "tag":
                    self.tag = result[1]
                    self.pathlist = list(tagdb.get_imgset_with_all_tags(set([self.girl.id, result[1]])))
                    self.imagepath = self.pathlist[0]                  
                    self.set_img()
                    
                elif result[0] == "view_trans":
                    pyt_gallery.trans_view()
                    
                # This is for the testing option (only in dev mode):
                elif result[0] == "change_dict":
                    if result[1] == "full":
                        self.td_mode = "full"
                        self.tagsdict = tagdb.get_tags_per_character(self.girl)
                    elif result[1] == "dev":
                        self.td_mode = "dev"
                        d = tagdb.get_tags_per_character(self.girl)
                        self.tagsdict = OrderedDict()
                        for i in d:
                            if i in ["portrait", "vnsprite", "battle_sprite"]:
                                self.tagsdict[i] = d[i]
                        
                elif result[0] == "control":
                    if result[1] == 'return':
                        break
                        
        def set_img(self):
            if self.tag in ("vnsprite", "battle_sprite"):
                resize = self.girl.get_sprite_size(self.tag)
            else:
                resize = self.imgsize
                
            self.image = ProportionalScale(self.imagepath, *resize)
            self.tags = " | ".join([i for i in tagdb.get_tags_per_path(self.imagepath)])
                
                
        def trans_view(self):
            """
            I want to try and create some form of automated transitions/pics loading for viewing mechanism.
            Transitions are taken from Ceramic Hearts.
            """
            # Get the list of files for transitions first:
            transitions = list()
            path = content_path("gfx/masks")
            for file in os.listdir(path):
                    transitions.append("/".join([path, file]))
            transitions.reverse()
            transitions_copy = copy.copy(transitions)
            
            # Get the images:
            images = self.pathlist * 1
            shuffle(images)
            images_copy = copy.copy(images)
            
            renpy.hide_screen("pyt_gallery")
            renpy.with_statement(dissolve)
            
            renpy.show_screen("pyt_gallery_trans")
            
            renpy.music.play("content/sfx/music/reflection.mp3", fadein=1.5)
            
            global stop_dis_shit
            stop_dis_shit = False
            
            first_run = True
            
            while not stop_dis_shit:
                
                if not images:
                    images = images_copy * 1
                if not transitions:
                    transitions = transitions_copy * 1
                    
                image = images.pop()
                x, y = renpy.image_size(image)
                rndm = randint(5, 7)
                if first_run:
                    first_run = False
                else:
                    renpy.hide(tag)
                tag = str(random.random())
                
                if x > y:
                    ratio = config.screen_height/float(y)
                    if int(round(x * ratio)) <= config.screen_width:
                        image = ProportionalScale(image, config.screen_width, config.screen_height)
                        renpy.show(tag, what=image, at_list=[center, szoom(1.0, 1.5, rndm)])
                        renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                        renpy.pause(rndm-3)
                    else:
                        image = ProportionalScale(image, 10000, config.screen_height)
                        renpy.show(tag, what=image, at_list=[move_bawl((0.0, 0.5), (1.0, 0.5), rndm)])
                        renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                        renpy.pause(rndm-3)
                elif y > x:
                    ratio = 1366/float(x)
                    if int(round(y * ratio)) <= 768:
                        image = ProportionalScale(image, config.screen_width, config.screen_height)
                        renpy.show(tag, what=image, at_list=[center, szoom(1.0, 1.5, rndm)])
                        renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                        renpy.pause(rndm-3)
                    else:    
                        image = ProportionalScale(image, config.screen_width, 10000)
                        renpy.show(tag, what=image, at_list=[center, move_bawl((0.5, 1.0), (0.5, 0.0), rndm)])
                        renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                        renpy.pause(rndm-3)
                else:
                    image = ProportionalScale(image, config.screen_width, config.screen_height)
                    renpy.show(tag, what=image, at_list=[center, szoom(1.0, 1.5, rndm)])
                    renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                    renpy.pause(rndm-3)
                    
                    
                    
            renpy.hide_screen("pyt_gallery_trans")
            renpy.music.stop(fadeout=1.0)
            renpy.hide(tag)
            renpy.show_screen("pyt_gallery")
            renpy.with_statement(dissolve)
