init -999 python:
    ##################### Import Modules #####################
    import os
    import sys
    import re
    import pygame
    import time
    import string
    import logging
    import fnmatch
    import json
    import math
    from math import sin, cos, radians
    import random
    from random import randrange, randint, choice, shuffle
    import copy
    from copy import deepcopy, copy as shallowcopy
    import itertools
    from itertools import chain, izip_longest
    import operator
    from operator import attrgetter, itemgetter
    import collections
    from collections import OrderedDict
    import xml.etree.ElementTree as ET
    sys.path.append(renpy.loader.transfn("library")) # May fail if we ever post to Android, there is now a new python folder for imports in newer Ren'Py version that can be used instead. SimPy.__init__ may have to be adjusted.
    import simpy
    import cPickle as pickle
                
    ############## Settings and other useful stuff ###############
    # absolute path to the pytfall/game directory, which is formatted according
    # to the conventions of the local OS
    gamedir = os.path.normpath(config.gamedir)
    
    def content_path(path):
        '''Returns proper path for a file in the content directory *To be used with os module.'''
        return renpy.loader.transfn('content/' + path)
    
    # enable logging via the 'logging' module
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(name)-15s %(message)s')
    devlog = logging.getLogger(" ".join([config.name, config.version]))
    devlogfile = logging.FileHandler(os.path.join(gamedir, "devlog.txt"))
    devlogfile.setLevel(logging.DEBUG)
    devlog.addHandler(devlogfile)
    devlog.critical("\n--- launch game ---")
    fm = logging.Formatter('%(levelname)-8s %(name)-15s %(message)s')
    devlogfile.setFormatter(fm)
    del fm
    devlog.info("game directory: %s" % str(gamedir)) # Added str() call to avoid cp850 encoding
    
    class TimeLog(_object):
        '''
        Uses Devlog log to time execustion time between the two points.
        Failed to use RenPy log, switching to dev.
        '''
        def __init__(self):
            self.log = dict()
            
        def timer(self, msg="default"):
            if config.developer:
                if msg in self.log:
                    devlog.info("%s took %s secs to run!"%(msg, time.time() - self.log[msg]))
                    del(self.log[msg])
                else:
                    self.log[msg] = time.time()
                    devlog.info("Starting timer: %s"%msg)
                    
    tl = TimeLog()
    tl.timer("Ren'Py User Init!")

    # setting the window on center
    # useful if game is launched in the window mode
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Best I can tell, does nothing, but looks kinda nice :)
    sys.setdefaultencoding('utf-8')
    
    # Getting rid of annoying saves before the menus
    def choice_for_skipping():
        """
        :doc: other
    
        Tells Ren'Py that a choice is coming up soon. This currently has
        two effects:
    
        * If Ren'Py is skipping, and the Skip After Choices preferences is set
          to stop skipping, skipping is terminated.
    
        * An auto-save is triggered. (No Longer!)
        """
    
        if renpy.config.skipping and not renpy.game.preferences.skip_after_choices:
            renpy.config.skipping = None
    
    renpy.choice_for_skipping = choice_for_skipping
    
    # Object to specify a lack of value when None can be considered valid.
    # Use as "x is undefined".
    undefined = object()
    
    # Prepping a list to append all events for the registration.
    world_events = list()
    
    # Prepping a list to append all quests for the registration.
    world_quests = list()
    
    # Getting rid of Ren'Py's containers since we don't require rollback.
    dict = _dict
    set = _set
    list = _list
    # object = _object # We are not using Ren'Pys object anywhere but it will throw errors if initiated this early because layout cannot be built with Pythons one.
    _rollback = False
    
    # Registration of extra music channels:
    renpy.music.register_channel("events", "sfx", False, file_prefix="content/sfx/sound/")
    renpy.music.register_channel("events2", "sfx", False,  file_prefix="content/sfx/sound/")
    renpy.music.register_channel("world", "music", True, file_prefix="content/sfx/music/world/")
    renpy.music.register_channel("gamemusic", "music", True, file_prefix="content/sfx/music/")
    
    ######################## Classes/Functions ###################################
    # Auto Animation from a folder:
    def animate(path, delay=0.25, function=None, transition=None, loop=False):
        # Build a list of all images:
        files = os.listdir("".join([gamedir, path]))
        images = list("".join([path[1:], "/", fn]) for fn in files if fn.endswith(('.png', '.gif', ".jpg", ".jpeg")))
        # Build a list of arguments
        args = list()
        # for image in images:
            # args.extend([image, delay, transition])
        # return anim.TransitionAnimation(*args)
        for image in images:
            args.append([image, delay])
        return AnimateFromList(args, loop=loop)

    class Flags(_object):
        """Simple class to log all variables into a single namespace
        
        Now and count...
        """
        def __init__(self):
            self.flags = dict()
            
        def __iter__(self):
            return iter(self.flags)
        
        def set_flag(self, flag, value=True):
            self.flags[flag] = value
            
        def up_counter(self, flag, value=1, max=None, delete=False):
            """A more advanced version of a counter than mod_flag.
            
            This can keep track of max and min.
            """
            if flag in self.flags:
                f = self.flags[flag]
                new_value = f + value
                if (max is not None) and new_value >= max:
                    self.flags[flag] = max
                    if delete:
                        self.del_flag(flag)
                else:
                    self.flags[flag] = new_value
            else:
                self.flags[flag] = value
                
        def down_counter(self, flag, value=1, min=None, delete=False):
            """A more advanced version of a counter than mod_flag.
            
            This can keep track of max and min.
            """
            if flag in self.flags:
                f = self.flags[flag]
                new_value = f - value
                if (min is not None) and new_value <= min:
                    self.flags[flag] = min
                    if delete:
                        self.del_flag(flag)
                else:
                    self.flags[flag] = new_value
            else:
                self.flags[flag] = value
            
        def mod_flag(self, flag, value):
            """Can be used as a simple counter for integer based flags.
            
            Simply changes the value of the flag otherwise.
            """
            if not flag in self.flags:
                self.flags[flag] = value
                if config.debug and "next" not in last_label: # Not logged during last day for clearer logs.
                    devlog.warning("{} flag modded before setting it's value!".format(flag))
                return
                
            if isinstance(value, int):
                self.flags[flag] += value
            else:
                self.flags[flag] = value
                
        def set_union(self, flag, value):
            """Can be used to create sets.
            
            If a flag exists, expects it to be a set() and creates a union with it.
            """
            if not flag in self.flags:
                self.flags[flag] = set(value)
                if config.debug and "next" not in last_label: # Not logged during last day for clearer logs.
                    devlog.warning("{} flag modded before setting it's value!".format(flag))
                return
                
            if isinstance(value, (set, list, tuple)):
                self.flags[flag] = self.flags[flag].union(value)
            else:
                self.flags[flag] = self.flags[flag].union(set(value))
                
        def flag(self, flag):
            if flag in self.flags:
                return self.flags[flag]
            else:
                return False
                
        def del_flag(self, flag):
            if flag in self.flags:
                del(self.flags[flag])
                
        def has_flag(self, flag):
            """Check if flag exists at all (not just set to False).
            """
            return flag in self.flags
            
        
    def dice(value):
        """Randomly generated percentage chance to return a bool"""
        return (value / 100.0) > random.random()
    
    # "wrapper" around the notify
    def notify(message, style=False):
        if config.developer:
            if style:
                msg = "{=%s}%s"%(style, str(message))
                renpy.notify(u"%s"%msg) 
            else:
                renpy.notify(u"{size=+10}%s"%str(message))

    # Safe jump, if label doesn't exists, game will notify about it
    def jump(labelname):
        if renpy.has_label(labelname):
            notify("jump %s" % labelname)
            renpy.jump(labelname)
        else:
            notify(u"Label '%s' does not exist." % labelname)

    # Useful methods for path        
    def listdir(dir):
        return os.listdir(os.path.join(gamedir, dir))

    def exist(path):
        return os.path.exists(os.path.join(gamedir, path))

    # Analizis of strings and turning them into int, float or bool.
    # Useful for importing data from xml.
    def parse(string):
        try:
            value = int(string)
        except TypeError:
            value = string
        except AttributeError:
            value = string
        except ValueError:
            try:
                value = float(string)
            except ValueError:
                if string.lower() in ['true', 'yes', 'on']:
                    value = True
                elif string.lower() in ['false', 'no', 'off', 'none']:
                    value = False
                else:
                    value = string
        return value
        
    # Returns the position of cursor if show cursorPosition is called
    # show cursorPosition on bottom
    def dd_cursor_position(st, at):
        x, y = renpy.get_mouse_pos()
        return Text("{size=-5}%d - %d"%(x, y)), .1
        # -------------------------------------------------------------------------------------------------------- Ends here    
    
    ########################## Images ##########################
    # Colors are defined in colors.rpy to global namespace, prolly was not the best way but file was ready to be used.
    
    # Setting default town path to persistent:
    # if not persistent.town_path:
        # persistent.town_path = "content/gfx/bg/locations/map_buttons/dark/"
    # renpy.image("bg humans", "".join([persistent.town_path, "humans.jpg"]))
    renpy.image("bg humans", "content/gfx/bg/locations/map_buttons/gismo/humans.jpg")
    
    renpy.image('bg black', Solid((0, 0, 0, 255)))
    renpy.image('bg blood', Solid((150, 6, 7, 255)))
    
    ##################### Autoassociation #####################
    # Backrounds are automatically registered in the game and set to width/height of the default screen
    # displayed by "show bg <filename>" or similar commands
    # file name without the extention
    for fname in os.listdir(gamedir + '/content/gfx/bg'):
        if fname.endswith('.jpg') or fname.endswith(".png"):
            tag = 'bg ' + fname[:-4]
            image = 'content/gfx/bg/' + fname
            renpy.image(tag, im.Scale(image, config.screen_width,
                        config.screen_height))
    
    for fname in os.listdir(gamedir + '/content/gfx/bg/locations'):
        if fname.endswith('.jpg') or fname.endswith(".png"):
            tag = 'bg ' + fname[:-4]
            image = 'content/gfx/bg/locations/' + fname
            renpy.image(tag, im.Scale(image, config.screen_width,
                        config.screen_height))
            
    for fname in os.listdir(gamedir + '/content/gfx/bg/story'):
        if fname.endswith(('.jpg', ".png")):
            tag = 'bg ' + "story " + fname[:-4]
            image = 'content/gfx/bg/story/' + fname
            renpy.image(tag, im.Scale(image, config.screen_width,
                        config.screen_height))
           
    for fname in os.listdir(gamedir + '/content/gfx/bg/be'):
        if fname.endswith('.jpg'):
            tag = 'bg ' + fname[:-4]
            image = 'content/gfx/bg/be/' + fname
            renpy.image(tag, im.Scale(image, config.screen_width,
                        config.screen_height))

    # Same thing for sprites and NPC        
    for fname in os.listdir(gamedir + '/content/gfx/sprites'):
        if fname.endswith('.png'):
            tag = fname[:-4]
            image = 'content/gfx/sprites/' + fname
            renpy.image(tag, image)
            
    for fname in os.listdir(gamedir + '/content/gfx/sprites/npc'):
        if fname.endswith('.png'):
            tag = 'npc ' + fname[:-4]
            image = 'content/gfx/sprites/npc/' + fname
            renpy.image(tag, ProportionalScale(image, 400,
                        600))
            tag = 'npc ' + fname[:-4] + '_novel'
            image = 'content/gfx/sprites/npc/' + fname
            renpy.image(tag, ProportionalScale(image, 600,
                        700))
            
    # We'll define same images again so multiple npcs could be placed on the screen at the same time.        
    for fname in os.listdir(gamedir + '/content/gfx/sprites/npc'):
        if fname.endswith('.png'):
            tag = 'npc2 ' + fname[:-4]
            image = 'content/gfx/sprites/npc/' + fname
            renpy.image(tag, ProportionalScale(image, 400,
                        600))
            tag = 'npc ' + fname[:-4] + '_novel'
            image = 'content/gfx/sprites/npc/' + fname
            renpy.image(tag, ProportionalScale(image, 600,
                        700))
            
    # Auto-Animations are last
    def load_frame_by_frame_animations_from_dir(folder):
        path = content_path(folder)
        for dir in os.listdir(path):
            split_dir = dir.split(" ")
            len_split = len(split_dir)
            
            folder_path = "/".join(["/content", folder, dir])
            img_name = split_dir[0]
            delay = float(split_dir[1]) if len_split > 1 else 0.25
            loop = bool(int(split_dir[2])) if len_split > 2 else False
            
            renpy.image(img_name, animate(folder_path, delay, loop=loop))
            
    load_frame_by_frame_animations_from_dir("gfx/animations")
    load_frame_by_frame_animations_from_dir("gfx/be/auto-animations")
            
# Additional 'constant' definements

# Adds a number of useful development tools to the left buttom corner
# X - Instant Exit
# R - Recompilation of the game
# Shows mouse coordinates
screen debugTools():
    zorder 5
    vbox:
        align (0.02, 0.98)
        hbox:
            xalign 0
            button:
                text "X"
                action Quit(confirm=False)
            button:
                text "R"
                action ui.callsinnewcontext("_save_reload_game")

        add DynamicDisplayable(dd_cursor_position) xpos 10
        text "[last_label]"  xpos 10 size 10


init -1 python: # Constants:
    # for f in renpy.list_files():
        # if f.endswith((".png", ".jpg")):
            # renpy.image(f, At(f, slide(so1=(600, 0), t1=0.7, eo2=(1300, 0), t2=0.7)))
    equipSlotsPositions = dict()
    equipSlotsPositions['head'] = [u'Head', 0.2, 0.2]
    equipSlotsPositions['body'] = [u'Body', 0.2, 0.4]
    equipSlotsPositions['amulet'] = [u'Amulet', 1.0, 0.4]
    equipSlotsPositions['cape'] = [u'Cape', 1.0, 0.2]
    equipSlotsPositions['weapon'] = [u'Weapon', 0.2, 0.6]
    equipSlotsPositions['smallweapon'] = [u'Small Weapon', 1.0, 0.6]
    equipSlotsPositions['feet'] = [u'Feet', 1.0, 0.8]
    equipSlotsPositions['misc'] = [u'Misc', 0.035, 0.51]
    equipSlotsPositions['wrist'] = [u'Wrist', 0.2, 0.8]
    
init:
    default SKILLS_MAX = {k:5000 for k in PytCharacter.SKILLS}
    default SKILLS_THRESHOLD = {k:2000 for k in PytCharacter.SKILLS} # Must be exceeded before skills becomes harder to gain.
    
init 999 python:
    # ensure that all initialization debug messages have been written to disk
    devlogfile.flush()
    
    # Build Maps:
    # tilemap = TileMap("my_map.json")
    # map_image = tilemap.build_map()
    
    tl.timer("Ren'Py User Init!")
