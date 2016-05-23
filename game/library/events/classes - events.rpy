init -9 python:
    def get_random_event_image(eventfolder):
        templist = []
        if eventfolder in os.listdir(content_path('events')):
            for file in os.listdir(content_path('events/%s' % eventfolder)):
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    templist.append('content/events/%s/%s' % (eventfolder, file))
            return ProportionalScale(choice(templist), config.screen_width, config.screen_height)
    
    def register_event(*args, **kwargs):
        """
        Registers a new event in an init block (and now in labels as well!).
        """
        if hasattr(store, "pytfall"):
            return register_event_in_label(*args, **kwargs)
            
        event = WorldEvent(*args, **kwargs)
        world_events.append(event)
        return event
    
    def register_event_in_label(*args, **kwargs):
        """
        Registers a new event in a label.
        """
        event = WorldEvent(*args, **kwargs)
        pytfall.world_events.events.append(event)
        return event
    
    class WorldEventsManager(_object):
        """Manager of all events in PyTFall.
        """
        
        def __init__(self, data):
            """
            Manages the events making sure that everything runs smoothly. Basically a smart list :)
            data = A list of WorldEvent instances.
            """
            self.events = deepcopy(data) # all events
            self.events_cache = list() # events that should be acutally checked
            self.garbage = list()
            self.label_cache = None
            
        def get(self, name):
            # Returns the event object with given name.
            for e in self.events:
                if e.name == name:
                    return e
        
        def kill_event(self, event_name, cached=False):
            """
            Stop an event from triggering.
            event_name = The name of the event.
            cached = Whether to also remove cached events.
            """
            for i in self.events[:]:
                if i.name == event_name:
                    self.events.remove(i)
            
            if cached:
                for i in self.events_cache[:]:
                    if i.name == event_name:
                        self.events_cache.remove(i)
        
        def force_event(self, name):
            """
            Forces an event to the daily stack, this should be used with caution as it can mess up the conditioning.
            The best use for this method is adding newly created (during game runtime) event to the stack so they can be accessed on the same day.
            name = The name of the event.
            """
            for event in self.events:
                if event.name == name:
                    if event not in self.events_cache:
                        self.events_cache.append(event)
        
        def run_events(self, trigger_type, default=None, cost=0):
            """
            Functions an available event with the given trigger.
            trigger_type = The trigger to proc.
            default = The label to go to if there are no available events.
            cost = The cost of triggering the event.
            """
            self.label_cache = last_label
            l = list()
            
            for i in self.events_cache:
                if i.trigger_type == trigger_type and ("all" in i.locations or last_label in i.locations): l.append(i)
            
            if hero.AP < cost:
                renpy.show_screen("message_screen", "Not enough AP left")
                return
            else:
                hero.AP -= cost
                for event in l:
                    if event.check_conditions():
                        event.run_event()
                        return
                else:
                    if default: renpy.call_in_new_context(default)
                    return
            
        def finish_event(self):
            """
            Finishes the current event.
            """
            jump(self.label_cache)
        
        def next_day(self):
            """
            Filters events to be triggered and removes the garbage.
            Being called on main screen, NOT during the next day transition.
            """
            self.events_cache = list()
            
            # Clean-up
            for event in self.garbage:
                if event in self.events: self.events.remove(event)
            
            self.garbage = list()
            
            # Prepare the event list:
            for event in self.events:
                # Max runs
                if event.max_runs and event.max_runs <= event.runs:
                    self.garbage.append(event)
                    continue
                
                # Priority skip:
                # This also restores the priority if required
                if not event.priority:
                    if event.day_to_restore_priority <= day:
                        event.priority = event.priority_cache
                    else:
                        continue
                    # else: event.priority = event.priority_cache
                
                # Day range
                if event.end_day <= day:
                    self.garbage.append(event)
                    continue
                
                elif event.start_day > day:
                    continue
                
                # Times per day:
                if event.tpd and not event.resolve_tpd():
                    continue
                
                # Custom Condition:
                # Could simply check is method exists?
                if event.custom_condition and not event.custom_conditions():
                    continue
                
                # Simple Conditions:
                if event.simple_conditions and not all(list(bool(eval(c)) for c in event.simple_conditions)):
                    continue
                
                # We got to the final part:
                self.events_cache.append(event)
            
            # And finally, sorting by priority:
            self.events_cache.sort(key=attrgetter("priority"), reverse=True)
        
    
    class WorldEvent(Flags):
        """Container for the world event.
        """
        def __init__(self, name, label=None, priority=100, restore_priority=5, dice=0, start_day=1, end_day=float('inf'), jump=False, screen=False,
                           times_per_days=(), locations=list(), trigger_type="look_around", custom_condition=False, simple_conditions=None, run_conditions=None, stop_music=False, max_runs=0,
                           quest=None):
            """
            name = name of the event, will be used as label if label if not specified.
            label = if label doesn't equal name.
            dice = chance to execute (check dice function), use run_conditions otherwise
            dice has priority over run_conditions
            run_conditions = evaluated at execution of the event, should be a list of strings.
            priority = higher number will ensure higher priority.
            (Should never be set to 0 by a user!, Anything above 0 is fair game (rate you own events :) ))
            
            restore_priority = how many days should pass until priority is restored after the event is ran,
            0 will ensure that event runs at the same priority until disabled.
            
            start_day = day to start checking triggers for the event.
            end_day = day to stop checking triggers for the event.
            jump = jumps instead of running in new context.
            screen = will show a screen (bound to self.label) if True, ignored if false
            times_per_days = maximum amount of times that event may trigger in an amount of days, expects a tuple/list of amount, days.
            locations = to trigger the event.
            trigger_type = type of interaction that triggers the event, currently we have:
            - look_around - button
            - auto - on label entry
            - custom (custom event trigger)
            custom_condition (Edited condition method) ==> For complex conditioning, inherit from this class and add custom_conditions() method to return True or False
            simple_conditions = container of strings to be evaluated, if all return True, event will run. If any of those returns false, event will skip until all the conditions are met.
            - Note: Custom conditions will overrule simple once!
            max_runs = maximum amount of times this event can run until it is removed from the game.
            stop_music = selfexplanatory, defaults to false.
            
            quest = The name of the quest the event is attached to.
            """
            super(WorldEvent, self).__init__()
            
            # Names/Label
            self.name = name
            self.jump = jump
            self.screen = screen
            if not label: self.label = name
            else: self.label = label
            self.dice = dice
            self.run_conditions = run_conditions
            # Prority related    
            self.priority = priority
            self.priority_cache = priority
            self.restore_priority = restore_priority
            self.day_to_restore_priority = 0
            # Day range
            self.start_day = start_day
            self.end_day = end_day
            self.tpd = times_per_days
            self.last_executed = 0 # Day
            self.days = list() # list of all days when the event has been executed
            # Locations time:
            self.locations = locations
            self.trigger_type = trigger_type
            # Runs
            self.max_runs = max_runs
            self.runs = 0
            
            
            # Quest support
            self.quest = quest
            
            # Rest/Not used
            self.custom_condition = custom_condition
            self.simple_conditions = simple_conditions
            self.stop_music = stop_music
            self.disabled = False
            self.enable_on = 0 # Day to restore the event
            self.label_cache = None # Just for kicks I guess, someone may find it useful
        
        def check_conditions(self):
            """
            Check before the actual run of the event. This should return a boolean.
            """
            if not self.priority: return False
            
            if self.tpd:
                if self.resolve_tpd():
                    if self.dice and dice(self.dice): return True
                    elif self.run_conditions and all(list(bool(eval(c)) for c in self.run_conditions)): return True
                
                else: return False
            
            elif self.dice and dice(self.dice): return True
            
            elif self.run_conditions and all(list(bool(eval(c)) for c in self.run_conditions)): return True
            
            return False
        
        def resolve_tpd(self):
            """
            Resolves the amount many times event has been run in given amount of previous days.
            Returns true to run the event.
            """
            range_of_days = range(day-self.tpd[1], day+1)
            matched_days = list()
            
            for i in self.days[:]:
                if i in range_of_days:
                    matched_days.append(i)
                # and clean-up:
                if i < day-self.tpd[1]: self.days.remove(i)
            
            if len(matched_days) < self.tpd[0]: return True
            else: return False
        
        def run_event(self):
            """
            Runs the event after all conditions have been met.
            """
            if self.tpd: self.days.append(day)
            self.runs += 1    
            self.last_executed = day
            self.label_cache = last_label
            
            if self.restore_priority:
                self.priority = 0
                self.day_to_restore_priority = day + self.restore_priority
            
            if self.stop_music: renpy.music.stop(channel="music", fadeout=1.0)
            
            if self.screen: renpy.show_screen(self.label)
            elif self.jump: jump(self.label)
            else: renpy.call_in_new_context(self.label, self)
        
        def finish_event(self):
            """
            Finishes the cevent.
            """
            jump(self.label_cache)
        
    
