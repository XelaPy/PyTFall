# Library of functions
init -11 python:
    def set_font_color(s, color):
        """
        @param: color: should be supplied as a string! Not as a variable!
        Sets font color during interpolation.
        """
        color = getattr(store, color, color)
        return "".join(["{color=%s}" % color, str(s), "{/color}"])

    def add_dicts(*dicts):
        """Does what I originally expected dict.update method to do many years ago...
        This works with dicts where all values are numbers.
        """
        if isinstance(dicts[0], (list, tuple, set)):
            dicts = dicts[0]

        new = {}
        for d in dicts:
            for key, value in d.iteritems():
                new[key] = new.get(key, 0) + value
        return new

    def gold_text(money):
        if money >= 10**12:
            return str(round(float(money)/10**12, 2)) + "T"
        elif money >= 10**9:
            return str(round(float(money)/10**9, 2)) + "B"
        elif money >= 10**6:
            return str(round(float(money)/10**6, 2)) + "M"
        else:
            return str(int(money))

    def get_mean(numbers):
        return float(sum(numbers)) / max(len(numbers), 1)

    def round_int(value):
        return int(round(value))

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
        if isinstance(amount, basestring):
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
        if string[:1] in ("a", "e", "i", "o", "u"):
            return "an"

        if overrides is not None:
            for i in overrides:
                if string.startswith(i): return "an"

        return "a"

    def hs():
        # Hides the current renpy screen.
        scr = renpy.current_screen()
        if scr is not None:
            renpy.hide_screen(scr.tag)

    def clear_screens():
        renpy.scene("screens")

    def digital_screen_logic(string, value):
        # logic for digital input screen
        if len(string) >= 14:
            return string

        if string == "0":
            return value
        else:
            return string + value
