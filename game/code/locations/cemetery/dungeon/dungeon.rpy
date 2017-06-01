init -1 python:
    from collections import deque
    from pygame import scrap, SCRAP_TEXT
    import time
    class Dungeon(object):

        def __init__(self, **kwargs):
            for k in kwargs:
                if k != "r" and k != "map":
                    super(Dungeon, self).__setattr__(k, kwargs[k])
            self._map = kwargs['map']
            self.said = None
            self.next_events = deque()
            self.show_map = False
            self.can_move = True
            self.timer = None
            self.light = ""
            self.timed = {}

        def say(self, arguments, timer=None, function=None, sound=None):
            # a message will be displayed for a time, dependent on its length
            if sound:
                renpy.play(*sound)

            if not timer:
                timer = max(float(len(arguments[1])) / 30.0, 0.5)

            self.said = arguments
            while len(self.said) != 4:
                self.said.append(None)

            self.add_timer(timer, [{"function": "dungeon.__setattr__", "arguments": ["said", None] }])

        def add_timer(self, timer, functions):

            self.timer = min(self.timer, timer) if self.timer is not None else timer
            timestr = timer + time.time()
            funclist = list(functions)
            funclist.append({"function": "dungeon.timed.__delitem__", "arguments": [timestr]})
            self.timed[timestr] = funclist

        def enter(self, at=None, function=None, load=None):
            if at:
                self.hero = at

            if not hasattr(self, "smallMap"):
                self.smallMap = SpriteManager(ignore_time=True)
                self._mapped = []
                for n,i in enumerate(self._map):
                    solids = []
                    for m in range(len(i)):
                        solid = Solid("#0000", xysize=(6,6))
                        solids.append(solid)
                        s = self.smallMap.create(solid)
                        s.x = 6*m + 3
                        s.y = 6*n + 43
                    self._mapped.append(solids)

                self.arrowtext = Text(" ", size=10)
                self.arrow = self.smallMap.create(self.arrowtext)
                self.arrow.x = (self.hero['x'] - .2)*6 + 9
                self.arrow.y = (self.hero['y'] - .4)*6 + 49

                for p, m in self.spawn.iteritems():
                    m['mob'] = build_mob(id=m['name'], level=m['level'])

                    self.add_timer(m['timer'], [{"function": "dungeon._move_npc", "arguments": [p, m] }])

            return self.hero

        def _move_npc(self, at_str, m):

            if not at_str in self.spawn:
                devlog.warn("spawn at %s already died?" % at_str)
                return

            hero_loc = (self.hero['x'], self.hero['y'])
            at = eval(at_str)

            # if within 5 of hero move about.
            for i in [0, 1]:
                if hero_loc[i] > at[i]:
                    if hero_loc[i] - at[i] > 5:
                        to = at
                        break
                    to = (at[0], at[1] + 1) if i else (at[0] + 1, at[1])
                    access_denied = self.no_access(at, to, 0 if i else 1, is_spawn=True)
                    if not access_denied:
                        break
                elif hero_loc[i] < at[i]:
                    if at[i] - hero_loc[i] > 5:
                        to = at
                        break
                    to = (at[0], at[1] - 1) if i else (at[0] - 1, at[1])
                    access_denied = self.no_access(at, to, 2 if i else 3, is_spawn=True)
                    if not access_denied:
                        break
                else:
                    continue
            else:
                to = at

            to_str = str(to)
            if to != at:
                del(self.spawn[at_str])
                self.spawn[to_str] = m

            self.add_timer(m['timer'], [{"function": "dungeon._move_npc", "arguments": [to_str, m] }])

        def map(self, x, y, color=None):
            if y < 0 or y >= len(self._map) or x < 0 or x >= len(self._map[y]):
                return "#"

            if color:
                self._mapped[y][x].color = color

            return self._map[y][x]

        def teleport(self, pt=None):

            if not pt: # using map hotspot
                pt = renpy.get_mouse_pos()
                pt = ((pt[0] - 3) / 6, (pt[1]-43) / 6)

            self.hero['x'] = pt[0]
            self.hero['y'] = pt[1]
            if len(pt) > 2: # to also set rotation: -1 for left/up, non-current direction is zero
                self.her['dx'] = pt[2]
                self.her['dy'] = pt[3]

        def play(self, sound, channel="sound", condition=True):
            if condition and not renpy.music.is_playing(channel):
                renpy.play(sound, channel)


        def no_access(self, at, to, ori, is_spawn=False):

            if pc['x'] == to[0] and pc['y'] == to[1]:
                return "hero collision" # for spawn movement

            tostr = str(to)
            if tostr in self.spawn:
                return "spawn collision"

            (src, dest) = (self.map(*at), self.map(*to))

            if dest in self.access[ori]:
                if src in self.access[ori] or (not is_spawn and src in self.conditional_access[ori]):
                    return
                self.play(self.sound['locked'], condition=not is_spawn, channel="sound")
                return "access denied"

            if is_spawn:
                return "spawn moment denied"

            if dest in self.conditional_access[ori]:
                if tostr not in self.access_condition:
                    return
                elif 'access' in self.access_condition[tostr] and self.access_condition[tostr]['access']:
                    return
                else:
                    # TODO: check for condition(s), key..? (requires inventory)
                    self.play(self.sound['locked'], condition=not is_spawn, channel="sound")
                    return "access denied"

            self.play(self.sound['bump'], condition=not is_spawn, channel="sound")
            return "wall collision"

        def function(self, function, arguments, set_var=None, **kwargs):

            # only allow particular functions
            if all(function[:len(f)] != f for f in ('renpy.', 'dungeon.', 'devlog.')):
                # may want to add more exceptions if necessary and safe
                raise Exception("calling function %s not allowed" % function)

            ret = eval(function)(*arguments, **kwargs)
            if set_var:
                self.__setattr__(set_var, ret)

transform sprite_default(xx, yy, xz, yz, rot=None):
    xpos xx
    ypos yy
    xzoom xz
    yzoom yz
    rotate rot
    subpixel True

screen dungeon_move(hotspots):
    tag dungeon
    # Screen which shows move buttons and a minimap
    for sw in reversed(show):
        if isinstance(sw, list):
            if sw[2]:
                python:
                    light_matrix = im.matrix.brightness(-math.sqrt(sw[3]**2 + sw[2]**2)/(5.8 if dungeon.light else 4.5))
                    if isinstance(sw[0], Item):
                        mco = im.MatrixColor(sw[0].icon, light_matrix)
                        (width, height) = mco.image.load().get_size()

                        xz=1.0/(1.5 + math.log(sw[2], 2))
                        xx=int(float(renpy.config.screen_width - (width/2)*xz) * (0.5 + float(sw[3]) / float(1 + sw[2])))

                        yz = xz/1.75
                        yy=int((renpy.config.screen_height - height*xz) * (0.5 + 1.0 / float(1.0 + sw[2])))
                        rot = sw[1]['rot'] if 'rot' in sw[1] else None #15.0+float(abs(sw[3])*distance)
                    elif isinstance(sw[0], Mob):
                        mco = im.MatrixColor(sw[0].battle_sprite, light_matrix)
                        (width, height) = mco.image.load().get_size()

                        sz = float(sw[1]['size']) if 'size' in sw[1] else 1.3
                        xz=2.0/(1.5 + math.log(sw[2], 2))
                        xx=int(float(renpy.config.screen_width - width*xz) * (0.5 + float(sw[3]) / float(1 + sw[2])))


                        yz = xz
                        lowness = float(renpy.config.screen_height)
                        if 'yoffs' in sw[1]:
                            lowness += float(sw[1]['yoffs'])
                        yy=int(float(lowness - height*xz) * (0.5 + 0.5 / float(.0001 + sw[2])))
                        rot=None

                add mco at [sprite_default(xx, yy, xz, yz, rot)]

        elif not isinstance(sw, basestring):
            add sw
        elif renpy.has_image(sw):
            add sw

    use top_stripe(show_return_button=False)

    if dungeon.show_map:
        add dungeon.smallMap

    if hotspots:
        imagemap:
            alpha False
            ground "content/dungeon/bluegrey/dungeon_blank.png"
            for hs in hotspots:
                hotspot (hs['spot'][0], hs['spot'][1], hs['spot'][2], hs['spot'][3]) action Return(value=hs['actions'])

    if dungeon.said:
        use say(dungeon.said[0], dungeon.said[1], dungeon.said[2], dungeon.said[3])
        key "K_RETURN" action Return(value="event_list")
        key "mousedown_1" action Return(value="event_list")

    elif dungeon.can_move:
        fixed style_group "move":
            textbutton "↓" action Return(value=2) xcenter .2 ycenter .9
            textbutton "←" action Return(value=4) xcenter .1 ycenter .8
            textbutton "→" action Return(value=6) xcenter .3 ycenter .8
            textbutton "<" action Return(value=7) xcenter .1 ycenter .9
            textbutton "↑" action Return(value=8)  xcenter .2 ycenter .7
            textbutton ">" action Return(value=9) xcenter .3 ycenter .9

            if config.developer:
                textbutton "U" action Return(value="update map") xcenter .2 ycenter .8
                key "K_u" action Return(value="update map")
                key "K_p" action Function(scrap.put, SCRAP_TEXT, str((pc['x'], pc['y'])))
                key "K_o" action Return(value="mpos")
                key "K_g" action SetField(dungeon, "show_map", "teleport")
                key "K_m" action ToggleField(dungeon, "show_map")

    if dungeon.can_move:
        key "K_KP2" action Return(value=2)
        key "K_KP4" action Return(value=4)
        key "K_KP6" action Return(value=6)
        key "K_KP7" action Return(value=7)
        key "K_KP8" action Return(value=8)
        key "K_KP9" action Return(value=9)
        key "K_l" action ToggleField(dungeon, "light", "_torch", "")
        key "K_LEFT" action Return(value=4)
        key "K_UP" action Return(value=8)
        key "K_RIGHT" action Return(value=6)
        key "K_DOWN" action Return(value=2)

        if not renpy.music.is_playing(channel="sound"):
            key "repeat_K_KP2" action Return(value=2)
            key "repeat_K_KP7" action Return(value=7)
            key "repeat_K_KP8" action Return(value=8)
            key "repeat_K_KP9" action Return(value=9)
            key "repeat_K_UP" action Return(value=8)
            key "repeat_K_DOWN" action Return(value=2)

    if dungeon.timer:
        timer dungeon.timer action Return(value="event_list")

style move_button_text:
    size 60

# Assign background images.
# "left0" means a wall on the lefthand, "front2" means a further wall on the front, and so on. field of view:
#
# left5c, left5b, left5, front5, right5, right5b, right5c
# left4c, left4b, left4, front4, right4, right4b, right4c
#         left3b, left3, front3, right3, right3b
#         left2b, left2, front2, right2, right2b
#                 left1, front1, right1
#                 left0, <hero>, right0



label enter_dungeon:
    python:

        # Create a dungeon stage
        dungeon = dungeons['Mausoleum1']
        if hasattr(dungeon, "hero"):
            pc = dungeon.enter()
        else:
            pc = dungeon.enter(at={ "x": 1, "y": 1, "dx": 1, "dy": 0 })
            dungeon.say(arguments=["", "You enter the mausoleum. The door shuts behind you; you cannot get out this way!"])
        mpos = None
        if not "dungeon" in ilists.world_music:
            ilists.world_music["dungeon"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("dungeon")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["dungeon"]) fadein 0.5
    $ global_flags.del_flag("keep_playing_music")

    # Place a player position on a dungeon stage.
    # dx,dy means direction. If dy=1, it's down. If dx=-1, it's left.

    while True:
        # Composite background images.
        scene
        python:
            # compile front to back, a list of what area are walls to be shown, behind wall we don't show.
            sided = ["%s%s_left%dc", "%s%s_left%db", "%s%s_left%d", "%s%s_front%d", "%s%s_right%d", "%s%s_right%db", "%s%s_right%dc"]
            blend = dungeon.area
            areas = deque([[0, 0]])
            show = []
            hotspots = []
            if config.developer and dungeon.show_map == "teleport":
                hs = [3, 43, len(dungeon._map[0])*6, len(dungeon._map)*6]
                hotspots.append({ 'spot': hs, 'actions': [{ "function": "dungeon.teleport", "arguments": [] }] })

            renpy.show(dungeon.background % dungeon.light)

            while areas:
                (distance, lateral) = areas.popleft()

                x = pc['x'] + distance*pc['dx'] - lateral*pc['dy']
                y = pc['y'] + lateral*pc['dx'] + distance*pc['dy']

                if distance == 1 and lateral == 0: # actions can be apply to front
                    front_str = str((x, y))
                    if front_str in dungeon.area_hotspots:
                        hotspots.extend(dungeon.area_hotspots[front_str])

                    for k in ["item", "renderitem", "spawn"]:

                        d_items = getattr(dungeon, k)
                        d_hotspots = getattr(dungeon, "%s_hotspots" % k)

                        if front_str in d_items:
                            actions = []
                            for ri in [d_items[front_str]] if k == "spawn" else d_items[front_str]:
                                n = ri['name']
                                if n in d_hotspots:
                                    e = d_hotspots[n].copy()
                                    actions.extend(e['actions'])
                                    e['actions'] = actions
                                    hotspots.append(e)
                            if actions:
                                actions.insert(0, { "function": "dungeon.%s.__delitem__" % k, "arguments": [front_str]})

                situ = dungeon.map(x, y)
                if situ in dungeon.container:
                    #FIXME use position lookup, for some container may first have to add front (cover) image (or modify image)

                    pt = str((x, y))
                    if pt in dungeon.renderitem:
                        for ri in dungeon.renderitem[pt]:
                            img_name = sided[lateral+3] % ('dungeon_'+ri['name'], dungeon.light, distance)
                            if 'function' in ri and ri['function'][:10] == "im.matrix.":

                                img_name = 'content/dungeon/'+ri['name']+dungeon.light+'/'+img_name+'.png'
                                if os.path.isfile(gamedir + '/'+img_name):
                                    # distance darkening
                                    brightness = im.matrix.brightness(-math.sqrt(lateral**2 + distance**2)/(5.8 if dungeon.light else 4.5))
                                    show.append(im.MatrixColor(img_name, eval(ri["function"])(*ri["arguments"]) * brightness))
                            else:
                                show.append(img_name)

                    if pt in dungeon.item:
                        for it in dungeon.item[pt]:
                            show.append([items[it['name']], it, distance, lateral])

                    if pt in dungeon.spawn:
                        spawn = dungeon.spawn[pt]
                        show.append([spawn['mob'], spawn, distance, lateral])

                # also record for minimap
                for k in dungeon.minimap:
                    if situ in k:
                        dungeon.map(x, y, renpy.easy.color(dungeon.minimap[k]))
                        break
                else:
                    dungeon.map(x, y, renpy.easy.color(dungeon.minimap['ground']))

                if pc['dy'] == -1:
                    dungeon.arrowtext.set_text("↑")
                    dungeon.arrow.y = (pc['y'] - .4)*6 + 43
                elif pc['dx'] == 1:
                    dungeon.arrowtext.set_text("→")
                    dungeon.arrow.y = (pc['y'] - .5)*6 + 43
                elif pc['dy'] == 1:
                    dungeon.arrowtext.set_text("↓")
                    dungeon.arrow.y = (pc['y'] - .4)*6 + 43
                else:
                    dungeon.arrowtext.set_text("←")
                    dungeon.arrow.y = (pc['y'] - .5)*6 + 43
                dungeon.arrow.x = (pc['x'] - .2)*6 + 3

                if situ in dungeon.visible: # a wall or so, need to draw.

                    if isinstance(blend[situ], list):

                        if len(blend[situ]) == 2: # left-right symmetry
                            show.append(sided[lateral+3] % ('dungeon_'+blend[situ][abs(pc['dx'])], dungeon.light, distance))

                        else: # no symmetry, 4 images.
                            ori = 1 - pc['dx'] - pc['dy'] + (1 if pc['dx'] > pc['dy'] else 0)
                            show.append(sided[lateral+3] % ('dungeon_'+blend[situ][ori], dungeon.light, distance))

                    else: # symmetric, or simply rendered in only one symmetry
                        show.append(sided[lateral+3] % ('dungeon_'+blend[situ], dungeon.light, distance))

                transparent_area = dungeon.transparent[abs(pc['dx'])]
                if situ in transparent_area or (situ in dungeon.visible and not renpy.has_image(show[-1])): # need to draw what's behind it.

                    # after `or' prevents adding areas twice. If the area diagonally nearer to hero is
                    # a wall, the area is not yet drawn, draw it, unless we cannot see it.
                    (bx, by) = (x-pc['dx'], y-pc['dy'])
                    if lateral >= 0 and (distance == lateral*2 or distance > lateral*2
                                         and dungeon.map(bx-pc['dy'], by+pc['dx']) not in transparent_area
                                         and ((distance == 1 and lateral == 0) or dungeon.map(bx, by) in transparent_area)):
                        areas.append([distance, lateral + 1])

                    if lateral <= 0 and (distance == -lateral*2 or distance > -lateral*2
                                         and dungeon.map(bx+pc['dy'], by-pc['dx']) not in transparent_area
                                         and ((distance == 1 and lateral == 0) or dungeon.map(bx, by) in transparent_area)):
                        areas.append([distance, lateral - 1])

                    if distance < 5:
                        areas.append([distance + 1, lateral])

        $ renpy.block_rollback()
        call screen dungeon_move(hotspots)

        python:
            at = (pc['x'], pc['y'])
            ori = 1 - pc['dx'] - pc['dy'] + (1 if pc['dx'] > pc['dy'] else 0)
            to = None

            if isinstance(_return, list):
                dungeon.next_events.extend(_return)
                _return = "event_list"

            elif _return == 2:
                to = (pc['x']-pc['dx'], pc['y']-pc['dy'])

                access_denied = dungeon.no_access(at, to, ori)
                if not access_denied:
                    (pc['x'], pc['y']) = to

            elif _return == 4:
                (pc['dx'], pc['dy']) = (pc['dy'], -pc['dx'])

            elif _return == 6:
                (pc['dx'], pc['dy']) = (-pc['dy'], pc['dx'])

            elif _return == 7:
                to = (pc['x']+pc['dy'], pc['y']-pc['dx'])

                access_denied = dungeon.no_access(at, to, ori ^ 2)
                if not access_denied:
                    (pc['x'], pc['y']) = to

            elif _return == 8:
                to = (pc['x']+pc['dx'], pc['y']+pc['dy'])

                access_denied = dungeon.no_access(at, to, ori)
                if not access_denied:
                    (pc['x'], pc['y']) = to

            elif _return == 9:
                to = (pc['x']-pc['dy'], pc['y']+pc['dx'])

                access_denied = dungeon.no_access(at, to, ori ^ 2)
                if not access_denied:
                    (pc['x'], pc['y']) = to

            elif _return == "update map":
                dungeon_location = dungeon.hero
                dungeons = load_dungeons()
                dungeon = dungeons[dungeon.id]
                dungeon.enter(at=dungeon_location)

            elif _return == "mpos": #XXX: dev mode
                if mpos:
                    mpos2 = renpy.get_mouse_pos()
                    scrap.put(SCRAP_TEXT, str((mpos[0], mpos[1], mpos2[0] - mpos[0], mpos2[1] - mpos[1])))
                    mpos = None
                else:
                    mpos = renpy.get_mouse_pos()

            if to:
                if str(to) in dungeon.event:
                    dungeon.next_events.extend(dungeon.event[str(to)])
                    _return = "event_list"

            if _return == "event_list":

                while dungeon.next_events:
                    event = dungeon.next_events.popleft()
                    if "load" in event:
                        dungeon = dungeons[event["load"]]
                        pc = dungeon.enter(**event)
                    elif event["function"] == "dungeon.say":
                        dungeon.say(**event)
                        # rest of next_events is postponed until after say is done.
                        break
                    else:
                        dungeon.function(**event)

            # do any expired timer events
            if dungeon.timer is not None:
                dungeon.timer = None
                current_time = time.time()
                for t in dungeon.timed.keys():
                    if not dungeon.timer or t - current_time < dungeon.timer:
                        if t < current_time:
                            for event in list(dungeon.timed[t]): # copy: key may be removed
                                dungeon.function(**event)
                        else:
                            dungeon.timer = t - current_time

