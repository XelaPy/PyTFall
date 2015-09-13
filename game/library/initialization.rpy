init -999 python:
    # TODO:
    """
    This is a general todo list with stuff that needs to get fixed, adapted to modernt done or otherwise improved:
    1) Define contants to use with SL2
    2) Parametarize screens to kwargs instead of globals so they run faster
    3) Modernize Arena screens
    4) Go through the game making sure as many images are predicted before shown whenever sensible (or even possible)
    """
    
    
    ##################### Import Modules #####################
    import os
    import sys
    import re
    import pygame
    import time
    import threading
    import string
    import logging
    import fnmatch
    import json
    from types import * # Star import should be removed (currently used in the BE)
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
    sys.path.append(renpy.loader.transfn("library"))
    import simpy
    
    # def listdir_nohidden(path):
        # for f in os.listdir(path):
            # if not f.startswith('.'):
                # yield f
                
    ############## Settings and other useful stuff ###############
    # absolute path to the pytfall/game directory, which is formatted according
    # to the conventions of the local OS
    gamedir = os.path.normpath(config.gamedir)
    
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
            
    
    # To lazy to write out Capitals
    # true = True
    # false = False
    # none = None
    # result = True
    Error = Exception
    
    # Object to specify a lack of value when None can be considered valid.
    # Use as "x is undefined".
    undefined = object()
    
    # Prepping a list to append all events for the registration.
    world_events = list()
    
    # Prepping a list to append all quests for the registration.
    world_quests = list()
    
    # Setting default town path to persistent:
    # if not persistent.town_path:
        # persistent.town_path = "content/gfx/bg/locations/map_buttons/dark/"
    # renpy.image("bg humans", "".join([persistent.town_path, "humans.jpg"]))
    renpy.image("bg humans", "content/gfx/bg/locations/map_buttons/gismo/humans.jpg")
    
    # Getting rid of Ren'Py's containers since we don't require rollback.
    dict = _dict
    set = _set
    list = _list
    # object = _object # We are not using Ren'Pys object anywhere but it will throw errors if initiated this early because layout cannot be built with Pythons one.
    _rollback = False
    
    # Regestration of extra music channels:
    renpy.music.register_channel("events", "sfx", False, file_prefix="content/sfx/sound/")
    renpy.music.register_channel("events2", "sfx", False,  file_prefix="content/sfx/sound/")
    renpy.music.register_channel("world", "music", True, file_prefix="content/sfx/music/world/")
    renpy.music.register_channel("gamemusic", "music", True, file_prefix="content/sfx/music/")
    
    ######################## Classes/Functions ###################################
    # Auto Animation from a folder:
    def animate(path, delay=0.25, function=None, transition=None):
        # Build a list of all images:
        dirs = os.listdir("".join([gamedir, path]))
        images = list("".join([path[1:], "/", fn]) for fn in dirs if fn.endswith(('.png', '.gif')))
        # Build a list of arguments
        args = list()
        # for image in images:
            # args.extend([image, delay, transition])
        # return anim.TransitionAnimation(*args)
        for image in images:
            args.append([image, delay])
        return AnimateFromList(args)

    class Flags(_object):
        """Simple class to log all variables into a single namespace
        
        Now and count...
        """
        def __init__(self):
            self.flags = dict()
        
        def set_flag(self, flag, value=True):
            self.flags[flag] = value
            
        def mod_flag(self, flag, value):
            """Can be used as counter for integer based flags.
            
            Simply changes the value of the flag otherwise.
            """
            if not flag in self.flags:
                self.flags[flag] = value
                if config.debug:
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
                if config.debug:
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
    def cursorPositionFunction(st, at):
        x,y = pygame.mouse.get_pos()
        return Text("{size=-5}%d - %d"%(x,y)), .1
        # -------------------------------------------------------------------------------------------------------- Ends here    
    
    ########################## Images ##########################
    renpy.image('bg black', Solid((0, 0, 0, 255)))
    renpy.image('bg blood', Solid((150, 6, 7, 255)))
    # Colors are defined in colors.rpy


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
    for dir in os.listdir("".join([gamedir, '/content/gfx/animations/'])):
        if " " in dir:
            renpy.image(dir.split(" ")[0], animate("".join(["/content/gfx/animations/", dir]), float(dir.split(" ")[1])))
        else:
            renpy.image(dir, animate("".join(["/content/gfx/animations/", dir])))
            
    for dir in os.listdir("".join([gamedir, '/content/gfx/be/auto-animations/'])):
        if " " in dir:
            renpy.image(dir.split(" ")[0], animate("".join(["/content/gfx/be/auto-animations/", dir]), float(dir.split(" ")[1])))
        else:
            renpy.image(dir, animate("".join(["/content/gfx/be/auto-animations/", dir])))
            
# Additional 'constant' definements

label _instant_exit:
    $ renpy.quit()

# Adds a number of useful development tools to the left buttom corner
# X - Instant Exit, surpassing the confirmation diologue
# R - Recompilation of the game
# Also shows mouse coordinates
screen debugTools():
    zorder 5
    vbox:
        xalign 0.02
        yalign 0.98
        hbox:
            xalign 0
            button:
                text "X"
                action ui.callsinnewcontext("_instant_exit")
            button:
                text "R"
                action ui.callsinnewcontext("_save_reload_game")

        add (DynamicDisplayable(cursorPositionFunction)) xpos 10
        text("{size=10}[last_label]") xpos 10



init -1 python: # Constants:
    # for f in renpy.list_files():
        # if f.endswith((".png", ".jpg")):
            # renpy.image(f, At(f, slide(so1=(600, 0), t1=0.7, eo2=(1300, 0), t2=0.7)))
    
    blank = "content/gfx/interface/images/blank.png"

    equipSlotsPositions = dict()
    equipSlotsPositions['head'] = [u'Head', 0.4, 0.1]
    equipSlotsPositions['body'] = [u'Body', 0.4, 0.3]
    equipSlotsPositions['amulet'] = [u'Amulet', 0.6, 0.3]
    equipSlotsPositions['cape'] = [u'Cape', 0.2, 0.3]
    equipSlotsPositions['weapon'] = [u'Weapon', 0.2, 0.5]
    equipSlotsPositions['smallweapon'] = [u'Small Weapon', 0.6, 0.5]
    equipSlotsPositions['feet'] = [u'Feet', 0.4, 0.9]
    equipSlotsPositions['misc'] = [u'Misc', 0.4, 0.7] 
    equipSlotsPositions['wrist'] = [u'Wrist', 0.4, 0.5]
    
    # TODO: Remove most of this after retagging effort.
    main_sex_tags = ["sex", "anal", "les", "blowjob", "bdsm", "group", "mast"]
    for_gm_selection = ["sex", "anal", "les", "blowjob", "bdsm", "group", "mast", "strip", "nude", "ripped", "battle", "cosplay", "cooking", "waitress", "musician", "singer", "studying", "hurt", "pajamas", "lingerie", "scared", "angry"]
    water_selection = ["beach", "onsen", "pool", "swimsuit", "bikini"]
    all_indoor_tags = ["generic indoor", "arena", "bar", "bathroom", "bedroom", "classroom", "kitchen", "living room", "library", "shop", "stage"]
    all_outdoor_tags = ["generic outdoor", "beach", "forest", "meadow", "onsen", "park", "pool", "road", "ruin", "urban", "wilderness", "yard"]

init 999 python:
    # ensure that all initialization debug messages have been written to disk
    devlogfile.flush()
    # Build Maps:
    # tilemap = TileMap("my_map.json")
    # map_image = tilemap.build_map()
    tl.timer("Ren'Py User Init!")
