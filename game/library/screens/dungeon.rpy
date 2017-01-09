init -1 python:

    class Stage(object):

        '''
        Class which contains map itself, auto mapping record, and encounter enemy.
        '''

        def __init__(self, map, enemy=None):
            self.map=map
            self.enemy=enemy
            self.mapped=[[0] * len(i) for i in map]

    class Dungeon_Coordinate(object):

        '''
        Class used for calculating relative coordinate.
        '''

        def __init__(self, stage=None, y=0, x=0, dy=0, dx=0):
            self.stage=stage
            self.y=y
            self.x=x
            self.dy=dy
            self.dx=dx

    class Dungeon_Minimap(object):

        '''
        A minimap. Minimap(current_coordinate).sm is a displayable to show this minimap.
        '''

        def __init__(self,child):
            self.sm = SpriteManager(ignore_time=True)
            for n,i in enumerate(child.stage.map):
                for m, j in enumerate(i):
                    if child.stage.mapped[n][m]==1:
                        if j in ["1"]:
                            d = Solid("#4444", xysize=(6,6))
                        else:
                            d = Solid("#fff4", xysize=(6,6))
                    else:
                        d = Solid("#0000", xysize=(6,6))
                    self.add(d,n,m)
            if child.dy==-1:
                self.add(Text("↑",size=10),child.y-.3,child.x-.2)
            elif child.dx==1:
                self.add(Text("→",size=10),child.y-.5,child.x-.3)
            elif child.dy==1:
                self.add(Text("↓",size=10),child.y-.3,child.x-.2)
            else:
                self.add(Text("←",size=10),child.y-.5,child.x-.3)

        def add(self, d,n,m):
            s = self.sm.create(d)
            s.x = m*6+6
            s.y = n*6+6

screen dungeon_move:
    # Screen which shows move buttons and a minimap

    fixed style_group "move":
        textbutton "↓" action Return(value=2) xcenter .2 ycenter .9
        textbutton "←" action Return(value=4) xcenter .1 ycenter .8
        textbutton "→" action Return(value=6) xcenter .3 ycenter .8
        textbutton "<" action Return(value=7) xcenter .1 ycenter .9
        textbutton "↑" action Return(value=8)  xcenter .2 ycenter .7
        textbutton ">" action Return(value=9) xcenter .3 ycenter .9

        key "K_KP2" action Return(value=2)
        key "K_KP4" action Return(value=4)
        key "K_KP6" action Return(value=6)
        key "K_KP7" action Return(value=7)
        key "K_KP8" action Return(value=8)
        key "K_KP9" action Return(value=9)
        key "K_l" action Return(value=100) # light
        key "K_LEFT" action Return(value=4)
        key "K_UP" action Return(value=8)
        key "K_RIGHT" action Return(value=6)
        key "K_DOWN" action Return(value=2)

        if not bumped:
            key "repeat_K_KP2" action Return(value=2)
            key "repeat_K_KP7" action Return(value=7)
            key "repeat_K_KP8" action Return(value=8)
            key "repeat_K_KP9" action Return(value=9)
            key "repeat_K_UP" action Return(value=8)
            key "repeat_K_DOWN" action Return(value=2)

    add Dungeon_Minimap(here).sm

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
#                 left0,  here , right0



label enter_dungeon:
    # To start exploring, call or jump to this label
    # To exit, create an event which has return or jump statement.
    "You enter the mausoleum. The door shuts behind you; you cannot get out this way!"
    python:

        # Create skills (name, type, hit, power)
        attack = Dungeon_Skill("Attack", "attack", 70, 20)
        escape = Dungeon_Skill("Escape", "escape")

        # Create battle actors (name, max_hp, skills)
        party = Actor("Hero",100, [attack,escape])
        #goblin = Actor("Goblin",40, [attack])

        # Create a dungeon stage (map,enemy)
        # "1" means wall, "0" means path.
        file = open(content_path("db/dungeon/mausoleum1.txt"))
        stage1=Stage(file.read().splitlines())#,enemy=goblin)
        file.close()
        bumped = False
        accesible_area = set(["0","2","3","7"])
        visible_area = set(["1","3","4","5","6","7"])
        transparent_area = set(["0","2","4","6","7"])
        light=""


    # Place a player position on a dungeon stage (stage,y,x,dy,dx).
    # dx,dy means direction. If dy=1, it's down. If dx=-1, it's left.
    $ here=Dungeon_Coordinate(stage1,2,2,0,1)

    while True:
        # Composite background images.
        scene
        python:
            # compile front to back, a list of what area are walls to be shown, behind wall we don't show.
            sided = ["%s%sleft%dc", "%s%sleft%db", "%s%sleft%d", "%s%sfront%d", "%s%sright%d", "%s%sright%db", "%s%sright%dc"]
            blend = {"1": "dungeon_mossy_", "3": "dungeon_door_", "4": "dungeon_barrel_", "5": "dungeon_",
                     "6": "dungeon_more_barrels_", "7": "dungeon_barrel_crate_"}
            areas = [[0, -1], [0, 1], [1, 0]]
            show = []
            renpy.show("%s%sbackground"%(blend["1"], light))

            while areas:
                (distance, lateral) = areas.pop(0)

                y = here.y + lateral*here.dx + distance*here.dy
                if y >= len(here.stage.map):
                    continue

                x = here.x + distance*here.dx - lateral*here.dy
                if x >= len(here.stage.map[y]):
                    continue

                # also record for minimap
                here.stage.mapped[y][x]=1

                if here.stage.map[y][x] in visible_area:

                    show.append(sided[lateral+3] % (blend[here.stage.map[y][x]], light, distance)) # a wall or so, need to draw.

                if here.stage.map[y][x] in transparent_area: # need to draw what's behind it.

                    # after `or' prevents adding areas twice. If the area diagonally nearer to hero is
                    # a wall, the area is not yet drawn, draw it, unless we cannot see it.
                    if lateral >= 0 and (distance == lateral*2 or distance > lateral*2
                                         and here.stage.map[y+here.dx-here.dy][x-here.dy-here.dx] not in transparent_area
                                         and ((distance == 1 and lateral == 0) or here.stage.map[y-here.dy][x-here.dx] in transparent_area)):
                        areas.append([distance, lateral + 1])

                    if lateral <= 0 and (distance == -lateral*2 or distance > -lateral*2
                                         and here.stage.map[y-here.dx-here.dy][x+here.dy-here.dx] not in transparent_area
                                         and ((distance == 1 and lateral == 0) or here.stage.map[y-here.dy][x-here.dx] in transparent_area)):
                        areas.append([distance, lateral - 1])

                    if distance < 5:
                        areas.append([distance + 1, lateral])

            # finally draw walls, back to front, lateral to central.
            for s in reversed(show):
                renpy.show(s)

        # Check events. If it happens, call a label or jump out to a label.
        # XXX: this probably should change
        if here.stage.enemy is not None and renpy.random.random()< .2:
            call dungeon_battle(player=party, enemy=here.stage.enemy)

        # Otherwise, call the move screen
        $ renpy.block_rollback()
        call screen dungeon_move

        python:
            if _return == 2:
                if here.stage.map[here.y-here.dy][here.x-here.dx] in accesible_area:
                    here.y -= here.dy
                    here.x -= here.dx

                elif not bumped:
                    renpy.play("content/sfx/sound/dungeon/bump.ogg")
                    bumped = True

            elif _return == 4:
                (here.dy, here.dx) = (-here.dx, here.dy)

            elif _return == 6:
                (here.dy, here.dx) = (here.dx, -here.dy)

            elif _return == 7:
                if here.stage.map[here.y-here.dx][here.x+here.dy] in accesible_area:
                    here.y -= here.dx
                    here.x += here.dy

                elif not bumped:
                    renpy.play("content/sfx/sound/dungeon/bump.ogg")
                    bumped = True

            elif _return == 8:
                if here.stage.map[here.y+here.dy][here.x+here.dx] in accesible_area:
                    here.y += here.dy
                    here.x += here.dx

                elif not bumped:
                    renpy.play("content/sfx/sound/dungeon/bump.ogg")
                    bumped = True

            elif _return == 9:
                if here.stage.map[here.y+here.dx][here.x-here.dy] in accesible_area:
                    here.y += here.dx
                    here.x -= here.dy

                elif not bumped:
                    renpy.play("content/sfx/sound/dungeon/bump.ogg")
                    bumped = True

            elif _return == 100:
                light = "" if light != "" else "torch_"

            if here.stage.map[here.y][here.x] == "2":
                renpy.say("", "Finally, there's a hatch here, you climb out of the catacombs.")
                renpy.jump("graveyard_town")
                bumped = False


