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
            
            temp = "{} and {} did their thing!".format(set_font_color(char.name, "pink"), client.name)
            store.building.nd_events_report.append(temp)
            store.client = client
            store.char = char
            char.action()
            
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
            
            if nd_chars:
                char = nd_chars.pop()
                temp = "{} and {} enter the room at {}".format(client.name, char.name, env.now)
                store.building.nd_events_report.append(temp)
                
                yield env.process(upgrade.run_job(client, char))
                
                temp = "{} leaves at {}".format(client.name, env.now)
                store.building.nd_events_report.append(temp)
                
            else:
                temp = "No girls were availible for {}".format(client.name)
                store.building.nd_events_report.append(temp)
                
                yield env.process(upgrade.kick_client(client))
                
                # temp = "{} leaves at {}".format(client.name, env.now)
                # store.building.nd_events_report.append(temp)
    
    def setup(env, rooms=2, ev_time=3):
        """
        First attempt at making a jobs loop with SimPy!
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
            yield env.timeout(random.randint(5, 9))
            i += 1
            store.client = store.nd_clients.pop()
            store.client.name = "client {}".format(i)
            env.process(client_dispatcher(env, store.client, upgrade))


label temp_jobs_loop:
    # Setup and start the simulation
    $ store.building.nd_events_report.append("\n\n")
    $ store.building.nd_events_report.append("{}".format(set_font_color("===================", "lawngreen")))
    $ store.building.nd_events_report.append("{}".format(set_font_color("Starting the simulation:", "lawngreen")))
    $ store.building.nd_events_report.append("{}".format(set_font_color("Testing a Brothel with two rooms:", "lawngreen")))
    # $ random.seed(RANDOM_SEED)  # This helps reproducing the results
    
    # Create an environment and start the setup process
    $ env = simpy.Environment()
    $ env.process(setup(env, 2, 3))
    $ env.run(until=20)
    $ store.building.nd_events_report.append("{}".format(set_font_color("Ending the simulation:", "red")))
    $ store.building.nd_events_report.append("{}".format(set_font_color("===================", "red")))
    $ store.building.nd_events_report.append("\n\n")
    
    
    return
