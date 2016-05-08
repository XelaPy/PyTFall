# Library of functions
init -11 python:
    # ---------------------- Game related:
    # Assists:
    # Function are not named according to PEP8 because we'll be using the living shit out of them in the game:
    def weighted_choice(choices):
        values, weights = zip(*choices)
        total = 0
        cum_weights = []
        for w in weights:
            total += w
            cum_weights.append(total)
        if total <= 0:
            return None
        x = random.random() * total
        i = bisect.bisect(cum_weights, x)
        return values[i]
    
    def plural(string, amount):
        """
        Returns the string as a plural if amount isn't above 1.
        string = The word to pluralise.
        amount = The amount of the 'word' as either a number or a string.
        """
        if isinstance(amount, str):
            try:
                if int(amount) == 1: return string
                elif string[-1:] == "x" or string[-2:] in ("ch", "sh", "ss"): return string + "es"
                else: return string + "s"
            
            except:
                # No valid number
                return string
        
        else:
            if amount == 1: return string
            elif string[-1:] == "x" or string[-2:] in ("ch", "sh", "ss"): return string + "es"
            else: return string + "s"
    
    def aoran(string, *overrides):
        """
        Returns "a" or "an" depending on if string begins with a vowel.
        string = The word to base the "a" or "an" on.
        overrides = A list of words to return "an" for, overriding the default logic.
        """
        string = string.lower()
        if string[:1] in ("a", "e", "i", "o", "u"): return "an"
        else:
            if overrides is not None:
                for i in overrides:
                    if string.startswith(i): return "an"
            
            return "a"
    
    def hs():
        # Hides the current renpy screen.
        renpy.hide_screen(renpy.current_screen().tag)
        
        

            


