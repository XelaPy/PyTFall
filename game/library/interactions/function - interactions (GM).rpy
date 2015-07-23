init -11 python:
    # Interactions (Girlsmeets Helper Functions):
    def rc(*args):
        """
        random choice function
        Wrapper to enable simpler girl_meets choices, returns whatever chr_gm is set to along with a random line.
        """
        return g(choice(list(args)))
        
    def rts(girl, options):
        """
        Get a random string from a random trait that a girl has.
        girl = The girl to check the traits against.
        options = A dictionary of trait/eval -> (strings,).
        """
        default = options.pop("default", None)
        available = list()
        
        for trait in options.iterkeys():
            if trait in traits:
                if traits[trait] in girl.traits: available.append(options[trait])
            else:
                if eval(trait, globals(), locals()): available.append(options[trait])
        
        if not available: trait = default
        else: trait = choice(available)
        
        if isinstance(trait, (list, tuple)): return choice(trait)
        else: return trait
        
    def ec(d):
        # Not used atm.
        """
        Expects a dict of k/v pairs as argument. If key is a valid trait, the function will check if character has it.
        Else, the key will be evaluated and value added to the choices.
        This will return a single random choice from all that return true (traits and evals).
        """
        l = list()
        for key in d:
            if key in traits:
                if key in chr.traits:
                    l.extend(d[key])
            else:
                if eval(key):
                    l.extend(d[key])
        # raise Error, l
        if l:
            g(choice(l))
            return True
        else:
            return False
        
    def ct(*args):
        """
        Check traits function.
        Checks is character in girl_meets has any trait in entered as an argument.
        """
        l = list(traits[i] for i in list(args))
        return any(i in l for i in chr.traits)
        
    def co(*args):
        """
        Check occupation
        Checks if any of the occupations belong to the character.
        """
        return ct(*args)
        
    def cgo(*args):
        """
        Checks for General Occupation strings, such as "SIW", "Warrior", "Server", etc.
        """
        gen_occs = set()
        for occ in chr.traits:
            if hasattr(occ, "occupations"):
                gen_occs = gen_occs.union(set(occ.occupations))
        return any(i for i in list(args) if i in gen_occs)
        
    def d(value):
        """
        Checks if disposition of the girl is any higher that value.
        """
        return chr.disposition >= value
        
    # Relationships:
    def check_friends(*args):
        friends = list()
        for i in args:
            for z in args:
                if i != z:
                    friends.append(i.is_friend(z))
        return all(friends)
        
    def set_friends(*args):
        for i in args:
            for z in args:
                if i != z:
                    i.friends.add(z)

    def end_friends(*args):
        for i in args:
            for z in args:
                if i != z and z in i.friends:
                    i.friends.remove(z)
        
    def check_lovers(*args):
        lovers = list()
        for i in args:
            for z in args:
                if i != z:
                    lovers.append(i.is_lover(z))
        return all(lovers)

    def set_lovers(*args):
        for i in args:
            for z in args:
                if i != z:
                    i.lovers.add(z)

    def end_lovers(*args):
        for i in args:
            for z in args:
                if i != z and z in i.lovers:
                    i.lovers.remove(z)
