init -1 python:

    class Stage(object):

        '''
        Class which contains map itself, auto mapping record, and encounter enemy.
        '''

        def __init__(self, map, enemy=None):
            self.map=map
            self.enemy=enemy
            self.mapped=[]
            for n,i in enumerate(map):
                self.mapped.append([])
                for j in i:
                    self.mapped[n].append(0)

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
                            d = Solid("#666", xysize=(12,12))
                        else:
                            d = Solid("#fff9", xysize=(12,12))
                    else:
                        d = Solid("#0000", xysize=(12,12))
                    self.add(d,n,m)
            if child.dy==-1:
                self.add(Text("↑",size=12),child.y,child.x)
            elif child.dx==1:
                self.add(Text("→",size=12),child.y,child.x)
            elif child.dy==1:
                self.add(Text("↓",size=12),child.y,child.x)
            else:
                self.add(Text("←",size=12),child.y,child.x)

        def add(self, d,n,m):
            s = self.sm.create(d)
            s.x = m*12+12
            s.y = n*12+12

screen dungeon_move:
    # Screen which shows move buttons and a minimap

    fixed style_group "move":
        if front1.stage.map[front1.y][front1.x] is not "1":
            textbutton "↑" action Return(value=front1)  xcenter .2 ycenter .7
        textbutton "→" action Return(value=turnright) xcenter .3 ycenter .8
        textbutton "↓" action Return(value=turnback) xcenter .2 ycenter .9
        textbutton "←" action Return(value=turnleft) xcenter .1 ycenter .8

    add Dungeon_Minimap(here).sm

style move_button_text:
    size 60

# Assign background images.
# "left0" means a wall on the lefthand, "front2" means a further wall on the front, and so on.

# left2, front2, right2
# left1, front1, right1
# left0,  here , right0

image floor = "content/dungeon/floor.png"
image left0 = "content/dungeon/left0.png"
image right0 = Transform("content/dungeon/left0.png", xzoom=-1)
image front1 ="content/dungeon/front1.png"
image left1 = "content/dungeon/left1.png"
image right1 = Transform("content/dungeon/left1.png", xzoom=-1)
image front2 = "content/dungeon/front2.png"
image left2 = "content/dungeon/left2.png"
image right2 = Transform("content/dungeon/left2.png", xzoom=-1)

label enter_dungeon:
    # To start exploring, call or jump to this label
    # To exit, create an event which has return or jump statement.
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
        stage1 = file.read().splitlines()
        file.close()
        stage1=Stage(stage1)#,enemy=goblin)

    # Place a player position on a dungeon stage (stage,y,x,dy,dx).
    # dx,dy means direction. If dy=1, it's down. If dx=-1, it's left.
    $ here=Dungeon_Coordinate(stage1,2,2,0,1)

    while True:
        # Calculate relative coordinates
        python:
            turnright=Dungeon_Coordinate(here.stage, here.y,here.x, here.dx,-here.dy)
            turnleft=Dungeon_Coordinate(here.stage, here.y, here.x, -here.dx,here.dy)
            turnback=Dungeon_Coordinate(here.stage, here.y,here.x, -here.dy,-here.dx)
            right0=Dungeon_Coordinate(here.stage, here.y+here.dx,here.x-here.dy, here.dy,here.dx)
            left0=Dungeon_Coordinate(here.stage, here.y-here.dx,here.x+here.dy, here.dy,here.dx)
            front1=Dungeon_Coordinate(here.stage, here.y+here.dy,here.x+here.dx, here.dy,here.dx)
            right1=Dungeon_Coordinate(here.stage, front1.y+front1.dx,front1.x-front1.dy, here.dy,here.dx)
            left1=Dungeon_Coordinate(here.stage, front1.y-front1.dx,front1.x+front1.dy, here.dy,here.dx)
            front2=Dungeon_Coordinate(here.stage, front1.y+front1.dy,front1.x+front1.dx, here.dy,here.dx)
            right2=Dungeon_Coordinate(here.stage, front2.y+front2.dx,front2.x-front2.dy, here.dy,here.dx)
            left2=Dungeon_Coordinate(here.stage, front2.y-front2.dx,front2.x+front2.dy, here.dy,here.dx)

        # Composite background images. Try-except clauses are used to prevent the List Out of Index Error
        scene
        show floor
        python:
            for i in ["left2", "right2", "front2", "left1", "right1", "front1", "left0", "right0"]:
                try:
                    j=globals()[i]
                    if j.stage.map[j.y][j.x]=="1":
                        renpy.show(i)
                except:
                    pass

        # Record maps
        python:
            for i in [left1, right1, front1, left0, right0, here]:
                here.stage.mapped[i.y][i.x]=1

        # Check events. If it happens, call a label or jump out to a label.
        if here.stage.enemy is not None and renpy.random.random()< .2:
            call dungeon_battle(player=party, enemy=here.stage.enemy)

        # Otherwise, call the move screen
        $ renpy.block_rollback()
        call screen dungeon_move
        $ here=_return


