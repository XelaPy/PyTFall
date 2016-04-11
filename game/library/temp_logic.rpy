init python:
    def list_files_test():
        t = time.time()
        c = 0
        for fn in renpy.list_files():
            if "content" in fn:
                c = c + 1
        return time.time() - t, c
    
    def set_font_color(s, color):
        """
        @param: color: should be supplied as a string! Not as a variable!
        Sets font color duting interpolation.
        """
        return "".join(["{color=[%s]}" % color, "{}".format(s), "{/color}"])
        
    class BuildingRelay(object):
        """An upgrade has a limited number of rooms to
        run jobs in parallel.
        
        Single Customer handling...
        
        @ TODO: I thinks this bit should be assigned to Building Upgrades!
    
        Clients have to have to request one of the rooms. When they got one, they
        can start the job processes and wait for it to finish (which
        takes jobtime descrete units).
        """
        def __init__(self, env):
            self.env = env
            
            # Bad way of handing Brothel Upgrade:
            self.building = object()
            self.building.res = simpy.Resource(env, 2)
            self.building.time = 5
            self.building.cap = 2
            
            self.sc = object()
            self.sc.res = simpy.Resource(env, 10)
            self.sc.time = 10 # Time it takes to clear one client.
            self.sc.cap = 10 # Capacity
            self.sc.cash = 0
            
        def building_client_dispatcher(self, evn, client):
            """The client_dispatcher process arrives at the building
            and requests a a room.
        
            It then starts the washing process, waits for it to finish and
            leaves to never come back...
            """
            with self.building.res.request() as request:
                yield request
                
                while store.nd_chars:
                    
                    # Here we should attempt to find the best match for the client!
                    store.char = store.nd_chars.pop()
                    
                    # First check is the char is still well and ready:
                    if not check_char(store.char):
                        if store.char in store.nd_chars:
                            store.nd_chars.remove(store.char)
                        temp = set_font_color('{} is done with this job for the day.'.format(store.char.name), "aliceblue")
                        store.building.nd_events_report.append(temp)
                        continue
                    
                    # We to make sure that the girl is willing to do the job:
                    temp = store.char.action.id
                    if not store.char.action.check_occupation(store.char):
                        if store.char in store.nd_chars:
                            store.nd_chars.remove(store.char)
                        temp = set_font_color('{} is not willing to do {}.'.format(store.char.name, temp), "red")
                        store.building.nd_events_report.append(temp)
                        continue
                        
                        # All is well and we create the event
                    temp = "{} and {} enter the room at {}".format(client.name, char.name, env.now)
                    store.building.nd_events_report.append(temp)
                    
                    yield env.process(self.run_building_job(client, char))
                    
                    temp = "{} leaves at {}".format(client.name, env.now)
                    store.building.nd_events_report.append(temp)
                    return
                    
                # devlog.info("Clients: {}, Girls: {}".format(len(store.nd_clients), len(store.nd_girls)))    
                temp = "No girls were availible for {}".format(client.name)
                store.building.nd_events_report.append(temp)
                
                env.process(self.kick_client(client))
                
        def sc_client_dispatcher(self, evn, client):
            """The client_dispatcher process arrives at the building
            and requests a a room.
        
            It then starts the washing process, waits for it to finish and
            leaves to never come back...
            """
            with self.sc.res.request() as request:
                yield request
                
                # All is well and we create the event
                temp = "{} enters the Strip Club at {}".format(client.name, env.now)
                store.building.nd_events_report.append(temp)
                
                yield env.process(self.run_sc_job(client, char))
                
                temp = "{} leaves the Club at {}".format(client.name, env.now)
                store.building.nd_events_report.append(temp)
                # return
                    
                # devlog.info("Clients: {}, Girls: {}".format(len(store.nd_clients), len(store.nd_girls)))    
                # temp = "No girls were availible for {}".format(client.name)
                # store.building.nd_events_report.append(temp)
                # env.process(self.kick_client(client))
            
        def run_building_job(self, client, char):
            """
            This should be a job...
            """
            yield self.env.timeout(self.building.time)
            if config.debug:
                temp = "Debug: {} Brothel Resource in use!".format(set_font_color(self.building.res.count, "red"))
                store.building.nd_events_report.append(temp)
            
            temp = "{} and {} did their thing!".format(set_font_color(char.name, "pink"), client.name)
            store.building.nd_events_report.append(temp)
            store.client = client
            store.char = char
            char.action()
            # We return the char to the nd list
            
            store.nd_chars.insert(0, char)
            
        def run_sc_job(self, client, char):
            """
            This should be a job...
            """
            yield self.env.timeout(self.sc.time)
            self.sc.cash += 100
            if config.debug:
                temp = "Debug: {} Strip Club Resource currently in use/ Cash earned: {}!".format(set_font_color(self.sc.res.count, "red"), self.sc.cash)
                store.building.nd_events_report.append(temp)
            
            # temp = "{} and {} did their thing!".format(set_font_color(char.name, "pink"), client.name)
            # store.building.nd_events_report.append(temp)
            # store.client = client
            # store.char = char
            # char.action()
            # store.nd_clients.remove(store.client)
            # We return the char to the nd list
            # store.nd_chars.insert(0, char)
            
        def kick_client(self, client):
            """
            Gets rid of this client...
            """
            yield self.env.timeout(1)
            temp = "There is not much for the {} to do...".format(client.name)
            store.building.nd_events_report.append(temp)
            temp = "So {} leaves the hotel cursing...".format(client.name)
            store.building.nd_events_report.append(temp)
            # store.nd_clients.remove(store.client)
    
    def setup(env, end=40):
        """
        First attempt at making a jobs loop with SimPy!
        @param: We should draw end from the building.
        """
        # Create the building
        upgrade = BuildingRelay(env)
    
        # for i in xrange(2):
            # store.client = store.nd_clients.pop()
            # store.client.name = "Client {}".format(i)
            # # if self.room.
            # env.process(upgrade.building_client_dispatcher(env, store.client))
        # Create more clients while the simulation is running if such are availible...
        
        i = 0
        while store.nd_clients:
            if env.now + 5 <= end: # This is a bit off... should we decide which action should be taken first?
                if i > 4:
                    yield env.timeout(random.randint(1, 3))
                i += 1
                store.client = store.nd_clients.pop()
                store.client.name = "Client {}".format(i)
                
                # Register the fact that client arrived at the building:
                temp = '{} arrives at the {} at {}.'.format(client.name, store.building.name, env.now)
                store.building.nd_events_report.append(temp)
                
                # Take an action!
                # Must be moved to 
                whores = list(i for i in store.nd_chars if "SIW" in i.occupations)
                strippers = list(i for i in store.nd_chars if traits["Stripper"] in i.occupations)
                servers = list(i for i in store.nd_chars if "Server" in i.occupations)
                if upgrade.building.res.count < upgrade.building.cap and (store.nd_chars):
                    env.process(upgrade.building_client_dispatcher(env, store.client))
                elif upgrade.sc.res.count < upgrade.sc.cap:
                    env.process(upgrade.sc_client_dispatcher(env, store.client))
                else:
                    env.process(upgrade.kick_client(client))
            else:
                break


label temp_jobs_loop:
    $ tl.timer("Temp Jobs Loop")
    # Setup and start the simulation
    $ store.building.nd_events_report.append("\n\n")
    $ store.building.nd_events_report.append(set_font_color("===================", "lawngreen"))
    $ store.building.nd_events_report.append("{}".format(set_font_color("Starting the simulation:", "lawngreen")))
    $ store.building.nd_events_report.append("{}".format(set_font_color("Testing a Building with two rooms:", "lawngreen")))
    # $ random.seed(RANDOM_SEED)  # This helps reproducing the results
    
    # Create an environment and start the setup process
    $ env = simpy.Environment()
    $ env.process(setup(env, end=100))
    $ env.run(until=100)
    $ store.building.nd_events_report.append("{}".format(set_font_color("Ending the First Stage:", "red")))
    $ env.run(until=110)
    $ store.building.nd_events_report.append("{}".format(set_font_color("Ending the simulation:", "red")))
    $ store.building.nd_events_report.append("{}".format(set_font_color("===================", "red")))
    $ store.building.nd_events_report.append("\n\n")
    $ tl.timer("Temp Jobs Loop")
    
    return
    
label reg_H_event:
    $ chars["Hinata"].set_flag("event_to_interactions_10012adacx2134s", value={"label": "some_Hinata_label", "button_name": "Hinata Q", "condition": "True"})
    return
    
label some_Hinata_label:
    "Event Goes here..."
    "Don't forget to delete/change the flag one you're done!"
    $ chars["Hinata"].del_flag("event_to_interactions_10012adacx2134s")
    jump girl_interactions
    
screen testing_new_filmstrip():
    hbox:
        pos (10, 200)
        textbutton "Done":
            action Return()
        add FilmStrip('content/gfx/be/filmstrips/SyrusSpriteSheet.png', (95, 65), (7, 8), 0.06, include_frames=range(3), loop=True)
        add FilmStrip('content/gfx/be/filmstrips/SyrusSpriteSheet.png', (95, 65), (7, 8), 0.06, include_frames=range(7, 14), loop=True)
        add FilmStrip('content/gfx/be/filmstrips/SyrusSpriteSheet.png', (95, 65), (7, 8), 0.06, include_frames=range(14, 20), loop=True)
        add FilmStrip('content/gfx/be/filmstrips/SyrusSpriteSheet.png', (95, 65), (7, 8), 0.06, include_frames=range(21, 25), loop=True)
        add FilmStrip('content/gfx/be/filmstrips/SyrusSpriteSheet.png', (95, 65), (7, 8), 0.06, include_frames=range(28, 35), loop=True)
        
image exl_01:
    anchor (0.5, 0.5)
    "content/gfx/be/animations/explosion_0/00.png"
    pause 0.1
    "content/gfx/be/animations/explosion_0/01.png"
    pause 0.1
    "content/gfx/be/animations/explosion_0/02.png"
    pause 0.1
    "content/gfx/be/animations/explosion_0/03.png"
    pause 0.1
    "content/gfx/be/animations/explosion_0/04.png"
    pause 0.1
    "content/gfx/be/animations/explosion_0/05.png"
    pause 0.1
    "content/gfx/be/animations/explosion_0/06.png"
    pause 0.1
    "content/gfx/be/animations/explosion_0/07.png"
    pause 0.1
    "content/gfx/be/animations/explosion_0/08.png"
    pause 0.1
    repeat
    
image cst_01:
    anchor (0.5, 1.0)
    "content/gfx/be/animations/cast_effect_0/00.png"
    pause 0.1
    "content/gfx/be/animations/cast_effect_0/01.png"
    pause 0.1
    "content/gfx/be/animations/cast_effect_0/02.png"
    pause 0.1
    "content/gfx/be/animations/cast_effect_0/03.png"
    pause 0.1
    "content/gfx/be/animations/cast_effect_0/04.png"
    pause 0.1
    "content/gfx/be/animations/cast_effect_0/05.png"
    pause 0.1
    "content/gfx/be/animations/cast_effect_0/06.png"
    pause 0.1
    "content/gfx/be/animations/cast_effect_0/07.png"
    pause 0.1
    "content/gfx/be/animations/cast_effect_0/08.png"
    pause 0.1
    "content/gfx/be/animations/cast_effect_0/09.png"
    pause 0.1
    "content/gfx/be/animations/cast_effect_0/10.png"
    pause 0.1
    "content/gfx/be/animations/cast_effect_0/11.png"
    pause 0.1
    repeat
    
image exl_02:
    Fixed(Image("content/gfx/be/animations/explosion_0/00.png", anchor=(0.5, 1.0)), xysize=(259, 218))
    pause 0.1
    Fixed(Image("content/gfx/be/animations/explosion_0/01.png", anchor=(0.5, 1.0)), xysize=(259, 218))
    pause 0.1
    Fixed(Image("content/gfx/be/animations/explosion_0/02.png", anchor=(0.5, 1.0)), xysize=(259, 218))
    pause 0.1
    Fixed(Image("content/gfx/be/animations/explosion_0/03.png", anchor=(0.5, 1.0)), xysize=(259, 218))
    pause 0.1
    Fixed(Image("content/gfx/be/animations/explosion_0/04.png", anchor=(0.5, 1.0)), xysize=(259, 218))
    pause 0.1
    Fixed(Image("content/gfx/be/animations/explosion_0/05.png", anchor=(0.5, 1.0)), xysize=(259, 218))
    pause 0.1
    Fixed(Image("content/gfx/be/animations/explosion_0/06.png", anchor=(0.5, 1.0)), xysize=(259, 218))
    pause 0.1
    Fixed(Image("content/gfx/be/animations/explosion_0/07.png", anchor=(0.5, 1.0)), xysize=(259, 218))
    pause 0.1
    Fixed(Image("content/gfx/be/animations/explosion_0/08.png", anchor=(0.5, 1.0)), xysize=(259, 218))
    pause 0.1
    repeat
        
screen testing_image_quality():
    add "black"
    textbutton "Done":
        align (0.5, 0)
        action Return()
    # add FilmStrip('content/gfx/be/filmstrips/cataclysm_sideways.png', (481, 453), (5, 4), 0.1, include_frames=range(17), loop=True) align (0.3, 0.2)
    # add Transform(FilmStrip('content/gfx/be/filmstrips/cataclysm_sideways2x.png', (240, 226), (5, 4), 0.1, include_frames=range(17), loop=True), zoom=2) align (0.5, 0.2)
    # add Transform(FilmStrip('content/gfx/be/filmstrips/cataclysm_sideways4x.png', (120, 113), (5, 4), 0.1, include_frames=range(17), loop=True), zoom=4) align (0.7, 0.2)
    
    # add "explosion_0" align (0.5, 0.5)
    # add "exl_01" pos (150, 400)
    # add "exl_02" pos (1100, 400)
    add "water_combined" pos (400, 400)
    add Transform("water_combined", zoom=-1) pos (400, 400)
    # Adding for testing and tweaking:
    # add "thunder_storm_3" align (0.5, 0.5)
        
transform battle_bounce_normal(pos):
    alpha 1
    pos pos # Initial position.
    xanchor 0.5
    easein 0.3 yoffset -250
    easeout 0.3 yoffset 0
    easein 0.3 yoffset -150
    easeout 0.3 yoffset 0
    linear 0.5 alpha 0
    repeat
        
transform battle_bounce_quad(pos):
    alpha 1
    pos pos # Initial position.
    xanchor 0.5
    easein_quad 0.3 yoffset -250
    easeout_quad 0.3 yoffset 0
    easein_quad 0.3 yoffset -150
    easeout_quad 0.3 yoffset 0
    linear 0.5 alpha 0
    repeat
        
transform battle_bounce_cubic(pos):
    alpha 1
    pos pos # Initial position.
    xanchor 0.5
    easein_cubic 0.3 yoffset -250
    easeout_cubic 0.3 yoffset 0
    easein_cubic 0.3 yoffset -150
    easeout_cubic 0.3 yoffset 0
    linear 0.5 alpha 0
    repeat
        
transform battle_bounce_quart(pos):
    alpha 1
    pos pos # Initial position.
    xanchor 0.5
    easein_quart 0.3 yoffset -250
    easeout_quart 0.3 yoffset 0
    easein_quart 0.3 yoffset -150
    easeout_quart 0.3 yoffset 0
    linear 0.5 alpha 0
    repeat
        
transform battle_bounce_quint(pos):
    alpha 1
    pos pos # Initial position.
    xanchor 0.5
    easein_quint 0.3 yoffset -250
    easeout_quint 0.3 yoffset 0
    easein_quint 0.3 yoffset -150
    easeout_quint 0.3 yoffset 0
    linear 0.5 alpha 0
    repeat
        
transform battle_bounce_expo(pos):
    alpha 1
    pos pos # Initial position.
    xanchor 0.5
    easein_expo 0.3 yoffset -250
    easeout_expo 0.3 yoffset 0
    easein_expo 0.3 yoffset -150
    easeout_expo 0.3 yoffset 0
    linear 0.5 alpha 0
    repeat
        
transform battle_bounce_circ(pos):
    alpha 1
    pos pos # Initial position.
    xanchor 0.5
    easein_circ 0.3 yoffset -250
    easeout_circ 0.3 yoffset 0
    easein_circ 0.3 yoffset -150
    easeout_circ 0.3 yoffset 0
    linear 0.5 alpha 0
    repeat
        
transform battle_bounce_back(pos):
    alpha 1
    pos pos # Initial position.
    xanchor 0.5
    easein_back 0.3 yoffset -250
    easeout_back 0.3 yoffset 0
    easein_back 0.3 yoffset -150
    easeout_back 0.3 yoffset 0
    linear 0.5 alpha 0
    repeat
        
transform battle_bounce_elasctic(pos):
    alpha 1
    pos pos # Initial position.
    xanchor 0.5
    easein_elastic 0.3 yoffset -250
    easeout_elastic 0.3 yoffset 0
    easein_elastic 0.3 yoffset -150
    easeout_elastic 0.3 yoffset 0
    linear 0.5 alpha 0
    repeat
        
transform battle_bounce_bounce(pos):
    alpha 1
    pos pos # Initial position.
    xanchor 0.5
    easein_bounce 0.3 yoffset -250
    easeout_bounce 0.3 yoffset 0
    easein_bounce 0.3 yoffset -150
    easeout_bounce 0.3 yoffset 0
    linear 0.5 alpha 0
    repeat
        
screen test_penners_easing():
    $ x = 60
    for i in [battle_bounce_normal, battle_bounce_quad, battle_bounce_cubic, battle_bounce_quart, battle_bounce_quint, 
                battle_bounce_expo, battle_bounce_circ, battle_bounce_back, battle_bounce_elasctic, battle_bounce_bounce]:
        text "100" color "F00" size 50 at i((x, 400))
        $ x = x + 110
    textbutton "All Done":
        align (0.5, 0.9)
        action Return()
