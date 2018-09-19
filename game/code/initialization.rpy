init -999 python:
    ##################### Import Modules #####################
    import os
    import sys
    import inspect
    from inspect import isclass
    import re
    import pygame
    from pygame import scrap, SCRAP_TEXT
    import time
    import string
    import logging
    import fnmatch
    import json
    import math
    from math import sin, cos, radians
    import random
    from random import randrange, randint, choice, shuffle, uniform
    import copy
    from copy import deepcopy, copy as shallowcopy
    import itertools
    from itertools import chain, izip_longest
    import functools
    from functools import partial
    import operator
    from operator import attrgetter, itemgetter, methodcaller
    import collections
    from collections import OrderedDict, defaultdict, deque
    import xml.etree.ElementTree as ET
    import simpy
    import cPickle as pickle
    import bisect
    import types

    ############## Settings and other useful stuff ###############
    # absolute path to the pytfall/game directory, which is formatted according
    # to the conventions of the local OS
    gamedir = os.path.normpath(config.gamedir)

    # Binding for easy access to major gfx folders.
    gfxpath = "content/gfx/"
    gfxframes = "content/gfx/frame/"
    gfximages = "content/gfx/images/"
    interfaceimages = "content/gfx/interface/images/"
    interfacebuttons = "content/gfx/interface/buttons/"

    if persistent.use_quest_popups is None:
        persistent.use_quest_popups = True
    if persistent.tooltips is None:
        persistent.tooltips = True
    if persistent.unsafe_mode is None:
        persistent.unsafe_mode = True
    if persistent.battle_results is None:
        persistent.battle_results = True
    if persistent.auto_saves is None:
        persistent.auto_saves = False
    if persistent.intro is None:
        persistent.intro = False
    if persistent.use_be_menu_targeting is None:
        persistent.use_be_menu_targeting = False

    def content_path(path):
        '''Returns proper path for a file in the content directory *To be used with os module.'''
        if os.pathsep+"content"+os.pathsep in path:
            renpy.error("content already in path: "+path)
        return renpy.loader.transfn('content/' + path)

    # enable logging via the 'logging' module
    if DEBUG_LOG:
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
        Uses Devlog to log execution time between the two statements.
        Failed to use RenPy log, switching to dev.
        '''
        def __init__(self):
            # dict of msg: start_time
            self.log = {}
            self.logged = {} # (History) We may want to view it later...

        def start(self, msg, report_start=False):
            if DEBUG_PROFILING:
                if msg not in self.log:
                    self.log[msg] = time.time()
                    if report_start:
                        devlog.info("Starting timer: {}".format(msg))
                else:
                    devlog.warning("!!! Tried to start before finishing a timer: {}!".format(msg))

        def end(self, msg):
            if DEBUG_PROFILING:
                if msg not in self.log:
                    devlog.warning("!!! Tried to end before starting a timer: {}!".format(msg))
                    return

                duration = time.time() - self.log[msg]
                duration = round(duration, 2)
                self.logged[msg] = duration
                devlog.info("{} completes in {}s.".format(msg, duration))
                del(self.log[msg])

    tl = TimeLog()
    tl.start("Ren'Py User Init!")

    # setting the window on center
    # useful if game is launched in the window mode
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Best I can tell, does nothing, but looks kinda nice :)
    sys.setdefaultencoding('utf-8')

    def resolve_lib_file(badf, l=1):

        m = re.match(r'^(?:.*[\\/])?(library[\\/].*\.rpy)c?$', badf)
        if m:
            f = m.group(1).replace('\\','/')
            try:
                return (renpy.loader.transfn(f), l)

            except Exception: pass

    def get_screen_src(name):

        for n, f, l in renpy.dump.screens:

            if isinstance(name, basestring) and n == name or n == name+"_screen":

                return resolve_lib_file(f, l)

    def get_label_src(name):

        for n, r in renpy.game.script.namemap.iteritems():

            if isinstance(name, basestring) and n == name or n == name+"_label":

                return resolve_lib_file(r.filename, r.linenumber)

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
    IMAGE_EXTENSIONS = (".png", ".jpg", ".gif", ".jpeg", ".webp")

    def check_image_extension(fn):
        return fn.lower().endswith(IMAGE_EXTENSIONS)

    # Auto Animation from a folder:
    def animate(path, delay=.25, function=None, transition=None, loop=False):
        # Build a list of all images:
        files = os.listdir("".join([gamedir, path]))
        images = list("".join([path[1:], "/", fn]) for fn in files if check_image_extension(fn))
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

        PF Flags:
        starts with "jobs": Reset internally in SimPy land! Usually at the end of Env.
        starts with "ndd": Deleted at the very end of next day logic!
        """
        def __init__(self):
            self.flags = dict()

        def __iter__(self):
            return iter(self.flags)

        def flag(self, flag):
            return self.flags.get(flag, False)

        def mod_flag(self, flag, value):
            """Can be used as a simple counter for integer based flags.

            Simply changes the value of the flag otherwise.
            """
            if DEBUG_LOG:
                if not self.has_flag(flag) and "next" not in last_label:
                    devlog.warning("{} flag modded before setting it's value!".format(flag))

            if isinstance(value, int):
                self.flags[flag] = self.flags.get(flag, 0) + value
            else:
                self.set_flag(flag, value)

        def get_flag(self, flag, default=None):
            # works similar to dicts .get method
            return self.flags.get(flag, default)

        def set_flag(self, flag, value=True):
            self.flags[flag] = value

        def del_flag(self, flag):
            if flag in self.flags:
                del(self.flags[flag])

        def has_flag(self, flag):
            """Check if flag exists at all (not just set to False).
            """
            return flag in self.flags

        def up_counter(self, flag, value=1, max=None, delete=False):
            """A more advanced version of a counter than mod_flag.

            This can keep track of max and delete a flag upon meeting it.
            """
            result = self.flags.get(flag, 0) + value
            if max is not None and result >= max:
                if delete:
                    self.del_flag(flag)
                else:
                    self.set_flag(flag, max)
            else:
                self.set_flag(flag, result)

        def down_counter(self, flag, value=1, min=None, delete=False):
            """A more advanced version of a counter than mod_flag.

            This can keep track of min and delete a flag upon meeting it.
            """
            result = self.flags.get(flag, 0) - value

            if min is not None and result <= min:
                if delete:
                    self.del_flag(flag)
                else:
                    self.set_flag(flag, min)
            else:
                self.set_flag(flag, result)

        def set_union(self, flag, value):
            """Can be used to create sets.

            If a flag exists, expects it to be a set() and creates a union with it.
            """
            if DEBUG_LOG:
                if not self.has_flag(flag) and "next" not in last_label:
                    devlog.warning("{} flag modded before setting it's value!".format(flag))

            if not isinstance(value, (set, list, tuple)):
                value = set([value])

            self.flags.setdefault(flag, set()).union(value)

        def add_to_set(self, flag, value):
            """Creates a set with flags"""
            self.flags.setdefault(flag, set()).add(value)

        def remove_from_set(self, flag, value):
            """Removes from flag which is a set"""
            if value in self.flags[flag]:
                self.flags[flag].remove(value)


    def dice(percent_chance):
        """ returns randomly True with given % chance, or False """
        return random.random() * 100 <= percent_chance

    def locked_dice(percent_chance):
        # Same as above, only using locked seed...
        return locked_random("random") * 100 <= percent_chance

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
        if isinstance(path, basestring):
            return os.path.exists(os.path.join(gamedir, path))

        return all(exist(x) for x in path)

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

    # -------------------------------------------------------------------------------------------------------- Ends here

    ########################## Images ##########################
    # Colors are defined in colors.rpy to global namespace, prolly was not the best way but file was ready to be used.

    # Setting default town path to persistent:
    # if not persistent.town_path:
        # persistent.town_path = "content/gfx/bg/locations/map_buttons/dark/"
    # renpy.image("bg humans", "".join([persistent.town_path, "humans.jpg"]))
    renpy.image("bg humans", "content/gfx/bg/locations/map_buttons/gismo/humans.webp")

    ##################### Autoassociation #####################
    # Backrounds are automatically registered in the game and set to width/height of the default screen
    # displayed by "show bg <filename>" or similar commands
    # file name without the extention
    # for fname in os.listdir(gamedir + '/content/gfx/be/webm'):
        # if fname.endswith(".webm") and not "mask" in fname:
            # tag = fname[:-5]
            # image = 'content/gfx/bg/' + fname
            # renpy.image(tag, im.Scale(image, config.screen_width,
                        # config.screen_height))

    for fname in os.listdir(gamedir + '/content/gfx/bg'):
        if check_image_extension(fname):
            tag = 'bg ' + fname.rsplit(".", 1)[0]
            image = 'content/gfx/bg/' + fname
            renpy.image(tag, im.Scale(image, config.screen_width,
                        config.screen_height))

    for fname in os.listdir(gamedir + '/content/gfx/bg/locations'):
        if check_image_extension(fname):
            tag = 'bg ' + fname.rsplit(".", 1)[0]
            image = 'content/gfx/bg/locations/' + fname
            renpy.image(tag, im.Scale(image, config.screen_width,
                        config.screen_height))

    for fname in os.listdir(gamedir + '/content/gfx/bg/story'):
        if check_image_extension(fname):
            tag = 'bg ' + 'story ' + fname.rsplit(".", 1)[0]
            image = 'content/gfx/bg/story/' + fname
            renpy.image(tag, im.Scale(image, config.screen_width,
                        config.screen_height))

    for fname in os.listdir(gamedir + '/content/gfx/bg/be'):
        if check_image_extension(fname):
            tag = 'bg ' + fname.rsplit(".", 1)[0]
            image = 'content/gfx/bg/be/' + fname
            renpy.image(tag, im.Scale(image, config.screen_width,
                        config.screen_height))

    # Dungeon:
    for light in ('', '_torch'):
        # 4 sided symmetry (or symmetry ignored)
        for blend in ('bluegrey', 'door', 'barrel', 'mossy', 'pilar', 'more_barrels', 'barrel_crate',
                      'portal', 'portal_turned', 'ladderdownf', 'mossy_alcove', 'dagger', 'ring'):
            for fname in os.listdir('%s/content/dungeon/%s%s' % (gamedir, blend, light)):
                if check_image_extension(fname):
                    renpy.image(fname[:-5], 'content/dungeon/%s%s/%s' % (blend, light, fname))

        # 2 sided symmetry and no symmetry
        for blend, orientations in [('portal', ['', '_turned']), ('ladder', "lrfb")]:
            for ori in orientations:
                for fname in os.listdir('%s/content/dungeon/%s%s%s' % (gamedir, blend, ori, light)):
                    if check_image_extension(fname):
                        renpy.image(fname[:-5], 'content/dungeon/%s%s%s/%s' % (blend, ori, light, fname))

        #composite images
        for wall in ('bluegrey', 'mossy'):
            for bgfname in os.listdir('%s/content/dungeon/%s%s' % (gamedir, wall, light)):
                if check_image_extension(bgfname):
                    bg_img = 'content/dungeon/%s%s/%s' % (wall, light, bgfname)
                    for blend in ('door2','button'):
                        fn_end = bgfname[len('dungeon_'+wall):-5]
                        tag = 'dungeon_%s_%s%s' % (wall, blend, fn_end)
                        fg_img = 'content/dungeon/%s%s/dungeon_%s%s.webp' % (blend, light, blend, fn_end)

                        if os.path.isfile('%s/%s' % (gamedir, fg_img)):
                            renpy.image(tag, im.Composite((1280,720), (0, 0), bg_img, (0, 0), fg_img))
                        else:
                            renpy.image(tag, bgfname[:-5])

    # Auto-Animations are last
    def load_frame_by_frame_animations_from_dir(folder):
        path = content_path(folder)
        for dir in os.listdir(path):
            split_dir = dir.split(" ")
            len_split = len(split_dir)

            folder_path = "/".join(["/content", folder, dir])
            img_name = split_dir[0]
            delay = float(split_dir[1]) if len_split > 1 else .25
            loop = bool(int(split_dir[2])) if len_split > 2 else False

            renpy.image(img_name, animate(folder_path, delay, loop=loop))

    load_frame_by_frame_animations_from_dir("gfx/animations")
    load_frame_by_frame_animations_from_dir("gfx/be/auto-animations")


init -1 python: # Constants:
    # for f in renpy.list_files():
        # if check_image_extension(f):
            # renpy.image(f, At(f, slide(so1=(600, 0), t1=.7, eo2=(1300, 0), t2=.7)))
    EQUIP_SLOTS = ['body', 'head', 'feet', 'wrist', 'amulet',
                   'cape', 'weapon', 'misc', 'ring', 'smallweapon']
    SLOTALIASES = {"smallweapon": "Left Hand", "weapon": "Right Hand",
                   "amulet": "Neck", "feet": "Legs", "quest": "Special"}
    AUTO_OVERLAY_STAT_LABELS = ("mc_action_", "interactions_", "girl_interactions_aboutjob")
    BLOCKED_OVERLAY_STATS = ("health", "mp", "vitality",
                             'mood', 'alignment')
    UNBLOCK_OVERLAY_STATS_LABELNAME_SUFFIX = ("cafe_invitation", )
    ND_IMAGE_SIZE = (820, 705)

    equipSlotsPositions = dict()
    equipSlotsPositions['head'] = [u'Head', .2, .1]
    equipSlotsPositions['body'] = [u'Body', .2, .3]
    equipSlotsPositions['amulet'] = [u'Amulet', 1.0, .3]
    equipSlotsPositions['cape'] = [u'Cape', 1.0, .1]
    equipSlotsPositions['weapon'] = [u'Weapon', .2, .5]
    equipSlotsPositions['smallweapon'] = [u'Small Weapon', 1.0, .5]
    equipSlotsPositions['feet'] = [u'Feet', 1.0, .7]
    equipSlotsPositions['misc'] = [u'Misc', .025, .41]
    equipSlotsPositions['wrist'] = [u'Wrist', .2, .7]
    equipSlotsPositions['ring'] = [u'Ring', 1.18, .2]
    equipSlotsPositions['ring1'] = [u'Ring', 1.18, .4]
    equipSlotsPositions['ring2'] = [u'Ring', 1.18, .6]

init python: # Locking random seed of internal renpys random
    def locked_random(type, *args, **kwargs):
        rv = getattr(renpy.random, type)(*args, **kwargs)
        store.stored_random_seed = renpy.random.getstate()
        return rv

init:
    default SKILLS_MAX = {k: 5000 for k in PytCharacter.SKILLS}
    default SKILLS_THRESHOLD = {k: 2000 for k in PytCharacter.SKILLS} # Must be exceeded before skills becomes harder to gain.
    $ DAILY_EXP_CORE = 100 # 1 lvl per 10 days give or take. This is a simple way to rebalance.
    default just_view_next_day = False
    default char = None
    default char_equip = None
    default girls = None
    default reset_building_management = True
    default block_say = False
    define PytPix = renpy.display.transition.Pixellate
    default last_label_pure = ""

    default special_save_number = 1

init 999 python:
    # ensure that all initialization debug messages have been written to disk
    if DEBUG_LOG:
        devlogfile.flush()

    # Build Maps:
    # tilemap = TileMap("my_map.json")
    # map_image = tilemap.build_map()

    tl.end("Ren'Py User Init!")
