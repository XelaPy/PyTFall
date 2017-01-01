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
        textbutton "→" action Return(value=turnright) xcenter .3 ycenter .8
        textbutton "↓" action Return(value=turnback) xcenter .2 ycenter .9
        textbutton "←" action Return(value=turnleft) xcenter .1 ycenter .8
        textbutton "↑" action Return(value=front1.stage.map[front1.y][front1.x])  xcenter .2 ycenter .7
        #strafe
        textbutton ">" action Return(value=right0.stage.map[front1.y][front1.x]) xcenter .3 ycenter .9
        textbutton "<" action Return(value=left0.stage.map[front1.y][front1.x]) xcenter .1 ycenter .9
        key "K_KP7" action Return(value=right0.stage.map[front1.y][front1.x])
        key "K_KP9" action Return(value=left0.stage.map[front1.y][front1.x])

        key "K_UP" action Return(value=front1.stage.map[front1.y][front1.x])
        key "K_KP8" action Return(value=front1.stage.map[front1.y][front1.x])

        key "K_DOWN" action Return(value=turnback)
        key "K_KP2" action Return(value=turnback)

        key "K_RIGHT" action Return(value=turnright)
        key "K_KP6" action Return(value=turnright)
        key "K_LEFT" action Return(value=turnleft)
        key "K_KP4" action Return(value=turnleft)
        key "repeat_K_RIGHT" action Return(value=turnright)
        key "repeat_K_KP6" action Return(value=turnright)
        key "repeat_K_LEFT" action Return(value=turnleft)
        key "repeat_K_KP4" action Return(value=turnleft)

        if not bumped:
            key "repeat_K_UP" action Return(value=front1.stage.map[front1.y][front1.x])
            key "repeat_K_KP8" action Return(value=front1.stage.map[front1.y][front1.x])
            key "repeat_K_KP7" action Return(value=right0.stage.map[front1.y][front1.x])
            key "repeat_K_KP9" action Return(value=left0.stage.map[front1.y][front1.x])
            key "repeat_K_DOWN" action Return(value=turnback)
            key "repeat_K_KP2" action Return(value=turnback)

    add Dungeon_Minimap(here).sm

style move_button_text:
    size 60

# Assign background images.
# "left0" means a wall on the lefthand, "front2" means a further wall on the front, and so on.

# left2, front2, right2
# left1, front1, right1
# left0,  here , right0



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

    # Place a player position on a dungeon stage (stage,y,x,dy,dx).
    # dx,dy means direction. If dy=1, it's down. If dx=-1, it's left.
    $ here=Dungeon_Coordinate(stage1,2,2,0,1)

    while True:
        # Calculate relative coordinates
        python:
            turnright=Dungeon_Coordinate(here.stage, here.y, here.x, here.dx,-here.dy)
            turnleft=Dungeon_Coordinate(here.stage, here.y, here.x, -here.dx, here.dy)
            turnback=Dungeon_Coordinate(here.stage, here.y, here.x, -here.dy,-here.dx)

            right0=Dungeon_Coordinate(here.stage, here.y+here.dx, here.x-here.dy, here.dy, here.dx)
            left0=Dungeon_Coordinate(here.stage, here.y-here.dx, here.x+here.dy, here.dy, here.dx)

            front1=Dungeon_Coordinate(here.stage, here.y+here.dy, here.x+here.dx, here.dy, here.dx)
            right1=Dungeon_Coordinate(here.stage, front1.y+here.dx, front1.x-here.dy, here.dy, here.dx)
            left1=Dungeon_Coordinate(here.stage, front1.y-here.dx, front1.x+here.dy, here.dy, here.dx)

            front2=Dungeon_Coordinate(here.stage, front1.y+here.dy, front1.x+here.dx, here.dy, here.dx)
            right2=Dungeon_Coordinate(here.stage, front2.y+here.dx, front2.x-here.dy, here.dy, here.dx)
            left2=Dungeon_Coordinate(here.stage, front2.y-here.dx, front2.x+here.dy, here.dy, here.dx)
            right2b=Dungeon_Coordinate(here.stage, right2.y+here.dx, right2.x-here.dy, here.dy, here.dx)
            left2b=Dungeon_Coordinate(here.stage, left2.y-here.dx, left2.x+here.dy, here.dy, here.dx)

            front3=Dungeon_Coordinate(here.stage, front2.y+here.dy, front2.x+here.dx, here.dy, here.dx)
            right3=Dungeon_Coordinate(here.stage, front3.y+here.dx, front3.x-here.dy, here.dy, here.dx)
            left3=Dungeon_Coordinate(here.stage, front3.y-here.dx, front3.x+here.dy, here.dy, here.dx)
            right3b=Dungeon_Coordinate(here.stage, right3.y+here.dx, right3.x-here.dy, here.dy, here.dx)
            left3b=Dungeon_Coordinate(here.stage, left3.y-here.dx, left3.x+here.dy, here.dy, here.dx)

            front4=Dungeon_Coordinate(here.stage, front3.y+here.dy, front3.x+here.dx, here.dy, here.dx)
            right4=Dungeon_Coordinate(here.stage, front4.y+here.dx, front4.x-here.dy, here.dy, here.dx)
            left4=Dungeon_Coordinate(here.stage, front4.y-here.dx, front4.x+here.dy, here.dy, here.dx)
            right4b=Dungeon_Coordinate(here.stage, right4.y+here.dx, right4.x-here.dy, here.dy, here.dx)
            left4b=Dungeon_Coordinate(here.stage, left4.y-here.dx, left4.x+here.dy, here.dy, here.dx)
            right4c=Dungeon_Coordinate(here.stage, right4b.y+here.dx, right4b.x-here.dy, here.dy, here.dx)
            left4c=Dungeon_Coordinate(here.stage, left4b.y-here.dx, left4b.x+here.dy, here.dy, here.dx)

            front5=Dungeon_Coordinate(here.stage, front4.y+here.dy, front4.x+here.dx, here.dy, here.dx)
            right5=Dungeon_Coordinate(here.stage, front5.y+here.dx, front5.x-here.dy, here.dy, here.dx)
            left5=Dungeon_Coordinate(here.stage, front5.y-here.dx, front5.x+here.dy, here.dy, here.dx)
            right5b=Dungeon_Coordinate(here.stage, right5.y+here.dx, right5.x-here.dy, here.dy, here.dx)
            left5b=Dungeon_Coordinate(here.stage, left5.y-here.dx, left5.x+here.dy, here.dy, here.dx)
            right5c=Dungeon_Coordinate(here.stage, right5b.y+here.dx, right5b.x-here.dy, here.dy, here.dx)
            left5c=Dungeon_Coordinate(here.stage, left5b.y-here.dx, left5b.x+here.dy, here.dy, here.dx)
        # Composite background images.
        scene
        show dungeon_floor
        python:
            for i in ["left5c", "right5c", "left5b", "right5b", "left5", "right5", "front5",
                "left4c", "right4c", "left4b", "right4b", "left4", "right4", "front4",
                "left3b", "right3b", "left3", "right3", "front3",
                "left2b", "right2b", "left2", "right2", "front2",
                "left1", "right1", "front1", "left0", "right0"]:
                j=globals()[i]
                if j.y < len(j.stage.map) and j.x < len(j.stage.map[j.y]) and j.stage.map[j.y][j.x] in ("1",):
                    renpy.show("dungeon_"+i)

        # Record maps
        python:
            if front1.stage.map[front1.y][front1.x] in ("0",):
                for i in [left1, right1, front2]:
                    if i.y < len(here.stage.mapped) and i.x < len(here.stage.mapped[i.y]) and i.y >= 0 and i.x >= 0:
                        here.stage.mapped[i.y][i.x]=1

            for i in [front1, left0, right0, here]:
                if i.y < len(here.stage.mapped) and i.x < len(here.stage.mapped[i.y]) and i.y >= 0 and i.x >= 0:
                    here.stage.mapped[i.y][i.x]=1

        # Check events. If it happens, call a label or jump out to a label.
        if here.stage.enemy is not None and renpy.random.random()< .2:
            call dungeon_battle(player=party, enemy=here.stage.enemy)

        # Otherwise, call the move screen
        $ renpy.block_rollback()
        call screen dungeon_move
        python:
            if isinstance(_return, Dungeon_Coordinate):
                here=_return
                bumped = False
            elif _return == "0":
                here=front1
                bumped = False
            elif _return == "1":
                if not bumped:
                    renpy.play("content/sfx/sound/dungeon/bump.ogg")
                bumped = True
            elif _return == "2":
                renpy.say("", "Finally, there's a hatch here, you climb out of the catacombs.")
                renpy.jump("graveyard_town")
                bumped = False


