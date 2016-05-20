init -1 python:
    # GUI Logic ---------------------------------------------------------------------------------------------
    # One func:
    def point_in_poly(poly, x, y):
    
        n = len(poly)
        inside = False
    
        p1x, p1y = poly[0]
        for i in xrange(n+1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
            p1x, p1y = p2x, p2y
    
        return inside
    
        
    class GuiGirlsList(_object):
        """
        Used for sorting girls in the list and maybe in profile screen in the future.
        """
        STATUS_GROUP = 'status'
        OCCUPATION_GROUP = 'occupation'
        ACTION_GROUP = 'action'
        BUILDING_GROUP = 'building'

        def __init__(self):
            self.sorted = list(girl for girl in hero.chars if girl.action != "Exploring")
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
            self.sorted = copy.copy(hero.chars)
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
            
            self.chars_list = None
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
                if girl.__class__ == Char and uniques < 5:
                    sglist.append(girl)
                    uniques += 1
                if girl.__class__ == rChar and randoms < 5:
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
        
        def populate_chars_list(self):
            """
            Populates the list of girls that are available.
            """
            chars_list = self.get_girls()
            self.chars_list = list()
            for i in range(randint(6, 8)):
                if chars_list:
                    self.chars_list.append(chars_list.pop())
                    
        def buy_girl(self):
            """
            Buys the focused girl from the market.
            """
            if hero.take_ap(1):
                if hero.take_money(self.girl.fin.get_price(), reason="Slave Purchase"):
                    renpy.play("content/sfx/sound/world/purchase_1.ogg")
                    hero.add_char(self.girl)
                    self.chars_list.remove(self.girl)
                    
                    if self.chars_list:
                        self.girl = choice(self.chars_list)
                        self.index = self.chars_list.index(self.girl)
                    
                    else:
                        self.girl = None
                
                else:
                    renpy.call_screen('message_screen', "You don't have enough money for this purchase!")
            
            else:
                renpy.call_screen('message_screen', "You don't have enough AP left for this action!!")
            
            if not self.chars_list:
                renpy.hide_screen("slave_shopping")
        
        def next_day(self):
            """
            Solves the next day logic.
            """
            if self.restock_day == day:
                self.populate_chars_list()
                self.restock_day += randint(2, 3)
                
            for g in self.blue_girls.keys():
                self.blue_girls[g] += 1
                if self.blue_girls[g] == 30:
                    hero.add_char(g)
                    del self.blue_girls[g]
                    pytfall.temp_text.append("Blue has finished training %s! The girl has been delivered to you!" % chars[g].name)
            
        def next_index(self):
            """
            Sets the focus to the next girl.
            """
            if self.chars_list:
                index = self.chars_list.index(self.girl)
                index = (index + 1) % len(self.chars_list)
                self.girl = self.chars_list[index]
                
        def previous_index(self):
            """
            Sets the focus to the previous girl.
            """
            if self.chars_list:
                index = self.chars_list.index(self.girl)
                index = (index - 1) % len(self.chars_list)
                self.girl = self.chars_list[index]
        
        def set_index(self):
            """
            Sets the focus to a random girl.
            """
            if self.chars_list:
                self.girl = choice(self.chars_list)
        
        def set_girl(self, girl):
            """
            Sets the focus to the given girl.
            girl = The girl to set the focus to.
            """
            if self.chars_list and girl in self.chars_list:
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
            self.default_imgsize = (960, 660)
            self.imgsize = self.default_imgsize
            self.tag = "profile"
            self.tagsdict = tagdb.get_tags_per_character(self.girl)
            self.td_mode = "full" # Tagsdict Mode (full or dev)
            self.pathlist = list(tagdb.get_imgset_with_all_tags(set([char.id, "profile"])))
            self.imagepath = self.pathlist[0]
            self._image = self.pathlist[0]
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
                    gallery.trans_view()
                    
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
                   
        @property
        def image(self):
            return ProportionalScale("/".join([self.girl.path_to_imgfolder, self._image]), self.imgsize[0], self.imgsize[1])
                        
        def set_img(self):
            if self.tag in ("vnsprite", "battle_sprite"):
                self.imgsize = self.girl.get_sprite_size(self.tag)
            else:
                self.imgsize = self.imgsize
                
            self._image = self.imagepath
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
                if file.endswith((".png", ".jpg", ".jpeg")):
                    transitions.append("/".join([path, file]))
            transitions.reverse()
            transitions_copy = copy.copy(transitions)
            
            # Get the images:
            images = self.pathlist * 1
            shuffle(images)
            images_copy = copy.copy(images)
            
            renpy.hide_screen("gallery")
            renpy.with_statement(dissolve)
            
            renpy.show_screen("gallery_trans")
            
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
                image = "/".join([self.girl.path_to_imgfolder, image])
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
                        renpy.show(tag, what=image, at_list=[truecenter, simple_zoom_from_to_with_linear(1.0, 1.5, rndm)])
                        renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                        renpy.pause(rndm-3)
                    else:
                        image = ProportionalScale(image, 10000, config.screen_height)
                        renpy.show(tag, what=image, at_list=[move_from_to_align_with_linear((0.0, 0.5), (1.0, 0.5), rndm)])
                        renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                        renpy.pause(rndm-3)
                elif y > x:
                    ratio = 1366/float(x)
                    if int(round(y * ratio)) <= 768:
                        image = ProportionalScale(image, config.screen_width, config.screen_height)
                        renpy.show(tag, what=image, at_list=[truecenter, simple_zoom_from_to_with_linear(1.0, 1.5, rndm)])
                        renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                        renpy.pause(rndm-3)
                    else:    
                        image = ProportionalScale(image, config.screen_width, 10000)
                        renpy.show(tag, what=image, at_list=[truecenter, move_from_to_align_with_linear((0.5, 1.0), (0.5, 0.0), rndm)])
                        renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                        renpy.pause(rndm-3)
                else:
                    image = ProportionalScale(image, config.screen_width, config.screen_height)
                    renpy.show(tag, what=image, at_list=[truecenter, simple_zoom_from_to_with_linear(1.0, 1.5, rndm)])
                    renpy.with_statement(ImageDissolve(transitions.pop(), 3))
                    renpy.pause(rndm-3)
                    
                    
                    
            renpy.hide_screen("gallery_trans")
            renpy.music.stop(fadeout=1.0)
            renpy.hide(tag)
            renpy.show_screen("gallery")
            renpy.with_statement(dissolve)
            
            
    class CoordsForPaging(_object):
        """ This class setups up x, y coordinates for items in content list.
        
        We use this in DragAndDrop.
        Might be I'll just use this in the future to handle the whole thing.
        For now, this will be used in combination with screen language.
        *Adaptation of Roman's Inv code!
        """
        def __init__(self, content, columns=2, rows=6, size=(100, 100), xspacing=10, yspacing=10, init_pos=(0, 0)):
            # Should be changes to location in the future:    
            self.content = content
            self.page = 0
            self.page_size = columns*rows

            self.pos = list()
            x = init_pos[0]
            for c in xrange(columns):
                y = init_pos[1]
                for r in xrange(rows):
                    self.pos.append((x, y))
                    y = y + size[1] + yspacing
                x = x + size[0] + xspacing
                    
        def __len__(self):
            return len(self.content)
            
        def __iter__(self):
            # We return a list of tuples of [(item, pos), (item, pos), ...] for self.page
            page = self.page_content
            pos = self.pos[:len(page)]
            return iter(zip(page, pos))
            
        def __getitem__(self, index):
            # Minding the page we're on!
            return self.content[self.page * self.page_size + index]
            
        def get_pos(self, item):
            # retruns a pos of an item on current page.
            return self.pos[self.page_content.index(item)]
            
        def __nonzero__(self):
            return bool(self.content)
                
        # Next page
        def next_page(self):
            if self.page < self.max_page:
                self.page += 1

        def last_page(self):
            self.page = self.max_page
                
        # Previous page
        def prev_page(self):
            if self.page > 0:
                self.page -= 1
                
        def first_page(self):
            self.page = 0
                
        @property
        def max_page(self):
            return len(self.content) / self.page_size if len(self.content) % self.page_size not in [0, self.page_size] else (len(self.content) - 1) / self.page_size
                
        @property
        def page_content(self):
            start = self.page * self.page_size
            end = (self.page+1) * self.page_size
            return self.content[start:end]
            
        # group of methods realizing the interface of common listing
        # remove and add an element
        # with recalc of current page
        def add(self, item):
            if item not in self.content:
                self.content.append(item)

        def remove(self, item):
            if item in self.content:
                self.content.remove(item)
                
    def dragged(drags, drop):
        # Simple func we use to manage drag and drop in team setups and maybe moar in the future.
        drag = drags[0]
        char = drags[0].drag_name
        x, y = workers.get_pos(char)
        
        if not drop:
            drags[0].snap(x, y, delay=0.2)
            renpy.restart_interaction()
            return
            
        team = drop.drag_name

        if char.status == "slave":
            drags[0].snap(x, y, delay=0.2)
            renpy.show_screen("message_screen", "Slaves are not allowed to participate in combat!")
            renpy.restart_interaction()
            return

        # for t in fg.teams:
            # if t and t[0] == char:
                # drags[0].snap(x, y, delay=0.2)
                # renpy.show_screen("message_screen", "%s is already a leader of %s!" % (char.nickname, t.name))
                # renpy.restart_interaction()
                # return
            # if not team:
                # for girl in t:
                    # if girl == char:
                        # drags[0].snap(x, y, delay=0.2)
                        # renpy.show_screen("message_screen", "%s cannot lead %s as she's already on %s!" % (char.nickname, team.name, t.name))
                        # renpy.restart_interaction()
                        # return
                        
        # for girl in team:
            # if girl == char:
                # drags[0].snap(x, y, delay=0.2)
                # renpy.show_screen("message_screen", "%s is already on %s!" % (char.nickname, team.name))
                # renpy.restart_interaction()
                # return
                
        if len(team) == 3:
            drags[0].snap(x, y, delay=0.2)
            renpy.restart_interaction()
            return
        else:
            team.add(char)
            workers.remove(char)
            drags[0].snap(x, y)

        return True
