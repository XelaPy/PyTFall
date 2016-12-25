init python:
    """
    These are used to track current location of any actor and some other object in the game.
    Assumption we make here is that no actor can be at two places at once.
    """

init -20 python:
    # Core Logic:
    def change_location(actor, loc):
        """
        All actors have (or should have) a location property.
        This functions attempts to remove them from their present location and put them in a new one.
        """
        try:
            actor.location.remove(actor)
            actor.location = loc
            if isinstance(loc, Location):
                loc.add(actor)
        except:
            devlog.warning("Could not properly relocate actor: {} to from location: {} to location: {}".format(actor.id, actor.location, loc))
            actor.location = loc
            
    def set_location(actor, loc):
        """
        This plainy forces a location on an actor.
        """
        actor.location = loc
        if isinstance(loc, Location):
            loc.add(actor)
        
    class Location(_object):
        """
        Usually a place or a building.
        This simply holds references to actors that are present @ the location.
        If a location is not a member of this class, it is desirable for it to have a similar setup or to be added to change_location() function manually.
        """
        def __init__(self):
            self.id = self.__class__
            self.actors = set()
            
        def __str__(self):
            if hasattr(self, "name"):
                return str(self.name)
            else:
                return str(self.id)
            
        def add(self, actor):
            self.actors.add(actor)
        
        def remove(self, actor):
            self.actors.remove(actor)
            
            
    # Content:
    class Streets(Location):
        """
        Dummy location for actors that have no place to live...
        """
        def __init__(self):
            super(Streets, self).__init__()
            self.id = "Streets"
            
    class Apartments(Location):
        """
        Another Dummy Location, this one is used for free characters that have a place to live of their own.
        This maybe replaced later by actual apartments for every character.
        """
        def __init__(self):
            super(Apartments, self).__init__()
            self.id = "City Apartment"
            
            
