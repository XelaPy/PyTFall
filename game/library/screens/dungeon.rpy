init -1 python:
    class Dungeon(object):
        def __init__(self, **kwargs):
            for k in kwargs:
                if k != "r" and k != "map":
                    super(Dungeon, self).__setattr__(k, kwargs[k])
            self._map = kwargs['map']

        def enter(self, at=None):
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
                        self._smadd(solid, 6*n, 6*m)
                    self._mapped.append(solids)

                self.arrowtext = Text(" ", size=10)
                self.arrow = self.smallMap.create(self.arrowtext)
                self.arrow.x = (self.hero['x'] - .3)*6 + 6
                self.arrow.y = (self.hero['y'] - .2)*6 + 6

            for p in self.point:
                if p['id'] == "spawn":
                    p['mob'] = build_mob(id=p['name'], level=p['level'])

            return self.hero

        def _smadd(self, d, n, m):
            s = self.smallMap.create(d)
            s.x = m + 1
            s.y = n + 1

        def map(self, i, j, color=None):
            if i < 0 or i >= len (self._map) or j < 0 or j >= len(self._map[i]):
                return "#"

            if color:
                self._mapped[i][j].color = color

            return self._map[i][j]

        def has_access(self, at, to, ori):
            (src, dest) = (dungeon.map(*at), dungeon.map(*to))

            if (src in dungeon.access[ori] or src in dungeon.conditional_access[ori]) and dest in dungeon.access[ori]:
                return True
            if dest in dungeon.conditional_access[ori]:
                tostr = str(to)
                if tostr not in dungeon.access_condition:
                    return True
                elif 'access' in dungeon.access_condition[tostr] and dungeon.access_condition[tostr]['access']:
                    return True

            return False

transform sprite_default(xx, yy, xz, yz, rot=None):
    xpos xx
    ypos yy
    xzoom xz
    yzoom yz
    rotate rot
    subpixel True

screen dungeon_move:
    # Screen which shows move buttons and a minimap
    for s in reversed(show):
        if isinstance(s, list):
            if s[2]:
                python:
                    light_matrix = im.matrix.brightness(-math.sqrt(s[3]**2 + s[2]**2)/(5.8 if light else 4.5))
                    if isinstance(s[0], Item):
                        mco = im.MatrixColor(s[0].icon, light_matrix)
                        (width, height) = mco.image.load().get_size()

                        xz=1.0/(1.5 + math.log(s[2], 2))
                        xx=int(float(renpy.config.screen_width - (width/2)*xz) * (0.5 + float(s[3]) / float(1 + s[2])))

                        yz = xz/1.75
                        yy=int((renpy.config.screen_height - height*xz) * (0.5 + 1.0 / float(1.0 + s[2])))
                        rot = s[1]['rot'] if 'rot' in s[1] else None #15.0+float(abs(s[3])*distance)
                    elif isinstance(s[0], Mob):
                        mco = im.MatrixColor(s[0].battle_sprite, light_matrix)
                        (width, height) = mco.image.load().get_size()

                        sz = float(s[1]['size']) if 'size' in s[1] else 1.3
                        xz=2.0/(1.5 + math.log(s[2], 2))
                        xx=int(float(renpy.config.screen_width - width*xz) * (0.5 + float(s[3]) / float(1 + s[2])))


                        yz = xz
                        lowness = float(renpy.config.screen_height)
                        if 'yoffs' in s[1]:
                            lowness += float(s[1]['yoffs'])
                        yy=int(float(lowness - height*xz) * (0.5 + 0.5 / float(.0001 + s[2])))
                        rot=None

                add mco at [sprite_default(xx, yy, xz, yz, rot)]
        elif not isinstance(s, basestring) or renpy.has_image(s):
            add s
        else:
            $ devlog.warn("missing image: "+s)

    fixed style_group "move":
        textbutton "↓" action Return(value=2) xcenter .2 ycenter .9
        textbutton "←" action Return(value=4) xcenter .1 ycenter .8
        textbutton "→" action Return(value=6) xcenter .3 ycenter .8
        textbutton "<" action Return(value=7) xcenter .1 ycenter .9
        textbutton "↑" action Return(value=8)  xcenter .2 ycenter .7
        textbutton ">" action Return(value=9) xcenter .3 ycenter .9

        if config.developer:
            textbutton "U" action Return(value=1000) xcenter .2 ycenter .8
            key "K_u" action Return(value=1000)

        key "K_KP2" action Return(value=2)
        key "K_KP4" action Return(value=4)
        key "K_KP6" action Return(value=6)
        key "K_KP7" action Return(value=7)
        key "K_KP8" action Return(value=8)
        key "K_KP9" action Return(value=9)
        key "K_l" action Return(value=100) # light
        key "K_p" action Function(devlog.warn, str(pc))
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

    add dungeon.smallMap

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
    # To start exploring, call or jump to this label
    # To exit, create an event which has return or jump statement.
    "You enter the mausoleum. The door shuts behind you; you cannot get out this way!"
    python:

        # Create skills (name, type, hit, power)
        #attack = Dungeon_Skill("Attack", "attack", 70, 20)
        #escape = Dungeon_Skill("Escape", "escape")

        # Create battle actors (name, max_hp, skills)
        #party = Actor("Hero",100, [attack,escape])
        #goblin = Actor("Goblin",40, [attack])

        # Create a dungeon stage (map,enemy)
        # "1" means wall, "0" means path.
        #file = open(content_path("db/dungeon/mausoleum1.txt"))
        #stage1=Stage(file.read().splitlines())#,enemy=goblin)
        #file.close()
        dungeon = dungeons['Mausoleum1']
        pc = dungeon.enter()
        light=""


    # Place a player position on a dungeon stage (stage,y,x,dy,dx).
    # dx,dy means direction. If dy=1, it's down. If dx=-1, it's left.

    while True:
        # Composite background images.
        scene
        python:
            # compile front to back, a list of what area are walls to be shown, behind wall we don't show.
            sided = ["%s%s_left%dc", "%s%s_left%db", "%s%s_left%d", "%s%s_front%d", "%s%s_right%d", "%s%s_right%db", "%s%s_right%dc"]
            blend = dungeon.area
            areas = [[0, 0]]
            show = []
            access_denied = {}
            renpy.show(dungeon.background % light)

            while areas:
                (distance, lateral) = areas.pop(0)

                y = pc['y'] + lateral*pc['dx'] + distance*pc['dy']
                x = pc['x'] + distance*pc['dx'] - lateral*pc['dy']
                situ = dungeon.map(y, x)

                if situ in dungeon.container:
                    #FIXME use position lookup, for some container may first have to add front (cover) image

                    for p in dungeon.point:
                        if p['y'] == y and p['x'] == x:
                            if p['id'] == "renderitem":

                                img_name = sided[lateral+3] % ('dungeon_'+p['item'], light, distance)
                                if 'function' in p and p['function'][:10] == "im.matrix.":

                                    img_name = 'content/dungeon/'+p['item']+light+'/'+img_name+'.png'
                                    if os.path.isfile(gamedir + '/'+img_name):
                                        # distance darkening
                                        brightness = im.matrix.brightness(-math.sqrt(lateral**2 + distance**2)/(5.8 if light else 4.5))
                                        show.append(im.MatrixColor(img_name, eval(p["function"])(*p["arguments"]) * brightness))
                                else:
                                    show.append(img_name)

                            elif p['id'] == "item":
                                show.append([items[p['item']], p, distance, lateral])

                            elif p['id'] == "spawn":
                                if distance == 0 and abs(lateral) == 1:
                                    access_denied.add(7 if lateral == -1 else 9)
                                if distance == 1 and lateral == 0:
                                    access_denied.add(8)
                                show.append([p['mob'], p, distance, lateral])

                # also record for minimap
                for k in dungeon.minimap:
                    if k != "ground" and situ in dungeon.minimap[k]['area']:
                        dungeon.map(y, x, renpy.easy.color(dungeon.minimap[k]['color']))
                        break
                else:
                    dungeon.map(y, x,renpy.easy.color(dungeon.minimap['ground']['color']))

                if pc['dy'] == -1:
                    dungeon.arrowtext.set_text("↑")
                    dungeon.arrow.y = (pc['y'] - .2)*6
                elif pc['dx'] == 1:
                    dungeon.arrowtext.set_text("→")
                    dungeon.arrow.y = (pc['y'] - .3)*6
                elif pc['dy'] == 1:
                    dungeon.arrowtext.set_text("↓")
                    dungeon.arrow.y = (pc['y'] - .2)*6
                else:
                    dungeon.arrowtext.set_text("←")
                    dungeon.arrow.y = (pc['y'] - .3)*6
                dungeon.arrow.x = (pc['x'])*6

                if situ in dungeon.visible: # a wall or so, need to draw.

                    if isinstance(blend[situ], list):

                        if len(blend[situ]) == 2: # left-right symmetry
                            show.append(sided[lateral+3] % ('dungeon_'+blend[situ][abs(pc['dx'])], light, distance))

                        else: # no symmetry, 4 images.
                            ori = 1 - pc['dx'] - pc['dy'] + (1 if pc['dx'] > pc['dy'] else 0)
                            show.append(sided[lateral+3] % ('dungeon_'+blend[situ][ori], light, distance))

                    else: # symmetric, or simply rendered in only one symmetry
                        show.append(sided[lateral+3] % ('dungeon_'+blend[situ], light, distance))

                transparent_area = dungeon.transparent[abs(pc['dx'])]
                if situ in transparent_area or (situ in dungeon.visible and not renpy.has_image(show[-1])): # need to draw what's behind it.

                    # after `or' prevents adding areas twice. If the area diagonally nearer to hero is
                    # a wall, the area is not yet drawn, draw it, unless we cannot see it.
                    (by, bx) = (y-pc['dy'], x-pc['dx'])
                    if lateral >= 0 and (distance == lateral*2 or distance > lateral*2
                                         and dungeon.map(by+pc['dx'],bx-pc['dy']) not in transparent_area
                                         and ((distance == 1 and lateral == 0) or dungeon.map(by,bx) in transparent_area)):
                        areas.append([distance, lateral + 1])

                    if lateral <= 0 and (distance == -lateral*2 or distance > -lateral*2
                                         and dungeon.map(by-pc['dx'],bx+pc['dy']) not in transparent_area
                                         and ((distance == 1 and lateral == 0) or dungeon.map(by,bx) in transparent_area)):
                        areas.append([distance, lateral - 1])

                    if distance < 5:
                        areas.append([distance + 1, lateral])

        # Check events. If it happens, call a label or jump out to a label.
        # XXX: this probably should change
        #if here.stage.enemy is not None and renpy.random.random()< .2:
        #    call dungeon_battle(player=party, enemy=here.stage.enemy)

        # Otherwise, call the move screen
        $ renpy.block_rollback()
        call screen dungeon_move

        python:
            at = (pc['y'], pc['x'])
            ori = 1 - pc['dx'] - pc['dy'] + (1 if pc['dx'] > pc['dy'] else 0)
            to = None
            if _return in access_denied:
                # Walking into NPC. dfferent sound or action ?
                pass

            elif _return == 2:
                to = (pc['y']-pc['dy'], pc['x']-pc['dx'])
                for npc in dungeon.point:
                    if npc['id'] == "spawn" and npc['y'] == to[0] and npc['x'] == to[1]:
                        # Walking into NPC. dfferent sound or action ?
                        break
                else:
                    if dungeon.has_access(at, to, ori):
                        (pc['y'], pc['x']) = to

                    elif not renpy.music.is_playing(channel="sound"):
                        renpy.play(dungeon.sound['bump'], channel="sound")

            elif _return == 4:
                (pc['dy'], pc['dx']) = (-pc['dx'], pc['dy'])

            elif _return == 6:
                (pc['dy'], pc['dx']) = (pc['dx'], -pc['dy'])

            elif _return == 7:
                to = (pc['y']-pc['dx'], pc['x']+pc['dy'])

                if dungeon.has_access(at, to, ori ^ 2):
                    (pc['y'], pc['x']) = to

                elif not renpy.music.is_playing(channel="sound"):
                    renpy.play(dungeon.sound['bump'], channel="sound")

            elif _return == 8:
                to = (pc['y']+pc['dy'], pc['x']+pc['dx'])

                if dungeon.has_access(at, to, ori):
                    (pc['y'], pc['x']) = to

                elif not renpy.music.is_playing(channel="sound"):
                    renpy.play(dungeon.sound['bump'], channel="sound")

            elif _return == 9:
                to = (pc['y']+pc['dx'], pc['x']-pc['dy'])

                if dungeon.has_access(at, to, ori ^ 2):
                    (pc['y'], pc['x']) = to

                elif not renpy.music.is_playing(channel="sound"):
                    renpy.play(dungeon.sound['bump'], channel="sound")

            elif _return == 100:
                light = "" if light != "" else "_torch"

            elif _return == 1000:
                dungeons = load_dungeons()
                dungeon = dungeons[dungeon.id]
                dungeon.enter()

            if to and dungeon.map(*to) in dungeon.event and str(at) in dungeon.event[to]:
                for event in dungeon.event[to][str(at)]:
                    if "function" in event and event["function"][:6] == "renpy.":
                        eval("%s%s"%(event["function"], str(tuple(event["arguments"]))))

                    elif "load" in event:
                        dungeon = dungeons[event["load"]]
                        pc = dungeon.enter(at=event["at"] if "at" in event else None)

