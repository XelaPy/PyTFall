init python:

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
            self.brothel = object()
            self.brothel.res = simpy.Resource(env, 2)
            self.brothel.time = 5
            self.brothel.cap = 2
            
            self.sc = object()
            self.sc.res = simpy.Resource(env, 10)
            self.sc.time = 10 # Time it takes to clear one client.
            self.sc.cap = 10 # Capacity
            self.sc.cash = 0
            
        def brothel_client_dispatcher(self, evn, client):
            """The client_dispatcher process arrives at the building
            and requests a a room.
        
            It then starts the washing process, waits for it to finish and
            leaves to never come back...
            """
            with self.brothel.res.request() as request:
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
                    
                    yield env.process(self.run_brothel_job(client, char))
                    
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
            
        def run_brothel_job(self, client, char):
            """
            This should be a job...
            """
            yield self.env.timeout(self.brothel.time)
            if config.debug:
                temp = "Debug: {} Brothel Resource in use!".format(set_font_color(self.brothel.res.count, "red"))
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
            # env.process(upgrade.brothel_client_dispatcher(env, store.client))
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
                if upgrade.brothel.res.count < upgrade.brothel.cap and (store.nd_chars):
                    env.process(upgrade.brothel_client_dispatcher(env, store.client))
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
    $ store.building.nd_events_report.append("{}".format(set_font_color("Testing a Brothel with two rooms:", "lawngreen")))
    # $ random.seed(RANDOM_SEED)  # This helps reproducing the results
    
    # Create an environment and start the setup process
    $ env = simpy.Environment()
    $ env.process(setup(env, end=100))
    $ env.run(until=100)
    $ store.building.nd_events_report.append("{}".format(set_font_color("Ending the simulation:", "red")))
    $ store.building.nd_events_report.append("{}".format(set_font_color("===================", "red")))
    $ store.building.nd_events_report.append("\n\n")
    $ tl.timer("Temp Jobs Loop")
    
    return
