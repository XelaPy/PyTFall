init python:

    def set_font_color(s, color):
        """
        @param: color: should be supplied as a string! Not as a variable!
        Sets font color duting interpolation.
        """
        return "".join(["{color=[%s]}" % color, "{}".format(s), "{/color}"])
        
    class UpgradeRelay(object):
        """An upgrade has a limited number of rooms to
        run jobs in parallel.
        
        Single Customer handling...
        
        @ TODO: I thinks this bit should be assigned to Building Upgrades!
    
        Clients have to have to request one of the rooms. When they got one, they
        can start the job processes and wait for it to finish (which
        takes jobtime descrete units).
        """
        def __init__(self, env, rooms=2, job_time=5):
            self.env = env
            self.room = simpy.Resource(env, rooms)
            self.job_time = job_time
    
        def run_job(self, client, char):
            """
            This should be a job...
            """
            yield self.env.timeout(self.job_time)
            if config.debug:
                temp = "Debug: {} Resource (rooms) currently occupied!".format(set_font_color(self.room.count, "red"))
                store.building.nd_events_report.append(temp)
            
            temp = "{} and {} did their thing!".format(set_font_color(char.name, "pink"), client.name)
            store.building.nd_events_report.append(temp)
            store.client = client
            store.char = char
            char.action()
            # We return the char to the nd list
            store.nd_chars.insert(0, char)
            
        def kick_client(self, client):
            """
            Gets rid of this client...
            """
            yield self.env.timeout(1)
            
            temp = "There is not much for the {} to do...".format(client.name)
            store.building.nd_events_report.append(temp)
            temp = "So {} leaves the hotel cursing...".format(client.name)
            store.building.nd_events_report.append(temp)
    
    
    def client_dispatcher(env, client, upgrade): # , period=7 
        """The client_dispatcher process arrives at the building
        and requests a a room.
    
        It then starts the washing process, waits for it to finish and
        leaves to never come back...
        """
        temp = '{} arrives at the {} at {}.'.format(client.name, store.building.name, env.now)
        store.building.nd_events_report.append(temp)
        
        with upgrade.room.request() as request:
            yield request
            
            while store.nd_chars:
                
                # Here we should attempt to find the best match for the client!
                store.char = store.nd_chars.pop()
                
                # First check is the char is still well and ready:
                if not check_char(store.char):
                    temp = set_font_color('{} is done with this job for the day.'.format(store.char.name), "aliceblue")
                    store.building.nd_events_report.append(temp)
                    continue
                
                # We to make sure that the girl is willing to do the job:
                temp = store.char.action.id
                if not store.char.action.check_occupation(store.char):
                    temp = set_font_color('{} is not willing to do {}.'.format(store.char.name, temp), "red")
                    store.building.nd_events_report.append(temp)
                    continue
                    
                    # All is well and we create the event
                temp = "{} and {} enter the room at {}".format(client.name, char.name, env.now)
                store.building.nd_events_report.append(temp)
                
                yield env.process(upgrade.run_job(client, char))
                
                temp = "{} leaves at {}".format(client.name, env.now)
                store.building.nd_events_report.append(temp)
                return
                
            temp = "No girls were availible for {}".format(client.name)
            store.building.nd_events_report.append(temp)
            
            yield env.process(upgrade.kick_client(client))
                
                # temp = "{} leaves at {}".format(client.name, env.now)
                # store.building.nd_events_report.append(temp)
    
    def setup(env, rooms=2, ev_time=3, end=40):
        """
        First attempt at making a jobs loop with SimPy!
        @param: We should draw end from the building.
        """
        # Create the building
        upgrade = UpgradeRelay(env, rooms, ev_time)
    
        # Create 4 initial clients:
        for i in xrange(4):
            store.client = store.nd_clients.pop()
            store.client.name = "Client {}".format(i)
            env.process(client_dispatcher(env, store.client, upgrade))
    
        # Create more clients while the simulation is running if such are availible...
        while store.nd_clients:
            # Only run if we can have a sucessful event...
            if env.now + ev_time <= end:
                yield env.timeout(random.randint(5, 9))
                i += 1
                store.client = store.nd_clients.pop()
                store.client.name = "client {}".format(i)
                env.process(client_dispatcher(env, store.client, upgrade))
            else:
                break


label temp_jobs_loop:
    # Setup and start the simulation
    $ store.building.nd_events_report.append("\n\n")
    $ store.building.nd_events_report.append(set_font_color("===================", "lawngreen"))
    $ store.building.nd_events_report.append("{}".format(set_font_color("Starting the simulation:", "lawngreen")))
    $ store.building.nd_events_report.append("{}".format(set_font_color("Testing a Brothel with two rooms:", "lawngreen")))
    # $ random.seed(RANDOM_SEED)  # This helps reproducing the results
    
    # Create an environment and start the setup process
    $ env = simpy.Environment()
    $ env.process(setup(env, 2, 3, 40))
    $ env.run(until=40)
    $ store.building.nd_events_report.append("{}".format(set_font_color("Ending the simulation:", "red")))
    $ store.building.nd_events_report.append("{}".format(set_font_color("===================", "red")))
    $ store.building.nd_events_report.append("\n\n")
    
    
    return
