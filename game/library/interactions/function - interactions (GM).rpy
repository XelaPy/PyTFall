init -11 python:
    # Interactions (Girlsmeets Helper Functions):
    def interactions_set_repeating_lines_limit(c): # returns the number of character "patience", ie how many repeating lines she's willing to listen in addition to default value
        patience = 0
        if "Impersonal" in c.traits:
            patience += randint(1,3)
        elif "Imouto" in c.traits:
            patience -= randint(1,2)
        elif "Dandere" in c.traits:
            patience += randint(1,2)
        elif "Tsundere" in c.traits:
            patience -= randint(0,2)
        elif "Kuudere" in c.traits:
            patience += randint(0,1)
        elif "Kamidere" in c.traits:
            patience -= randint(0,1)
        elif "Bokukko" in c.traits:
            patience += randint(-1, 1)
        elif "Ane" in c.traits and dice(70):
            patience += 1
        elif "Yandere" in c.traits: 
            if c.disposition <= 500:
                patience -= (0,1)
            else:
                patience += (2,3)
        if patience <= 1 and "Shy" in c.traits and dice(50):
            patience += 1
        if patience <= 2 and "Well-mannered" in c.traits and dice(50):
            patience += 1
        if patience >= 2 and "Ill-mannered" in c.traits and dice(50):
            patience -= 1
        return patience
    def interactions_flag_count_checker(char_name, char_flag): # this function is used to check how many times a certain interaction was used during the current turn; every interaction should have a unique flag name and call this function after every use
        global day
        if not(char_name.flag(char_flag)) or char_name.flag(char_flag)["day"] != day:
            char_name.set_flag(char_flag, {"day": day, "times": 1})
        else:
            char_name.set_flag(char_flag, {"day": day, "times": char_name.flag(char_flag)["times"] + 1})
        return char_name.flag(char_flag)["times"]
    def interactions_silent_check_for_bad_stuff(char_name): # we check issues without outputting any lines or doing something else, and just return True/False
        if char_name.effects["Food Poisoning"]['active']:
            return False
        elif char_name.vitality < 50:
            return False
        elif char_name.health < (round(char_name.get_max("health")*0.2)):
            return False
        elif (not("Pessimist" in char_name.traits) and char_name.joy <= 25) or (("Pessimist" in char_name.traits) and char_name.joy < 10):
            return False
        else:
            return True
    def interactions_check_for_bad_stuff(char_name): # we check major issues when the character will refuse almost anything
        if char_name.effects["Food Poisoning"]['active']:
            char_name.override_portrait("portrait", "indifferent")
            rc("But she was too ill to pay any serious attention to you.", "But her aching stomach completely occupies her thoughts.")
            char_name.restore_portrait()
            char_name.disposition -= randint(1, 2)
            renpy.jump("girl_interactions_end")
        elif char_name.vitality <= 20:
            char_name.override_portrait("portrait", "indifferent")
            rc("But she was too tired to even talk.", "She was not very happy that you interrupted her rest.")
            char_name.restore_portrait()
            char_name.disposition -= randint(1, 2)
            char_name.vitality -= 2
            renpy.jump("girl_interactions_end")
        elif char_name.health < (round(char_name.get_max("health")*0.2)):
            char_name.override_portrait("portrait", "indifferent")
            rc("But she is too wounded for that.", "But her wounds completely occupy her thoughts.")
            char_name.restore_portrait()
            char_name.disposition -= randint(2, 5)
            char_name.vitality -= 2
            renpy.jump("girl_interactions_end")
    
    def interactions_check_for_minor_bad_stuff(char_name): # we check minor issues when character might refuse to do something based on dice
        if (not("Pessimist" in char_name.traits) and char_name.joy <= 15) or (("Pessimist" in char_name.traits) and char_name.joy < 5):
            if dice(60):
                narrator(choice(["She is in a bad mood today, however you managed to cheer her up."]))
                char_name.disposition += 1
                char_name.joy += randint(3, 6)
            else:
                narrator(choice(["She is in a bad mood today and not does not want to do anything."]))
                renpy.jump("girl_interactions_end")
        elif char_name.effects["Down with Cold"]['active']: #if she's ill, there is a chance that she will disagree to chat
            if dice(60):
                narrator(choice(["She is not feeling well today, however you managed to cheer her up."]))
                char_name.disposition += 2
                char_name.joy += randint(3, 6)
            else:
                narrator(choice(["She is not feeling well today and not in the mood to do anything."]))
                renpy.jump("girl_interactions_end")
        elif char_name.vitality < 50 and dice (35):
            narrator(choice(["But she is simply too tired to pay any serious attention to you.", "But she so tired she almost falls asleep on the move."]))
            char_name.disposition -= randint(0, 1)
            char_name.vitality -= randint(1, 3)
            renpy.jump("girl_interactions_end")
            
    def interactions_checks_for_bad_stuff_greetings(char_name): # Special beginnings for greetings if something is off, True/False show that sometimes we even will need to skip a normal greeting altogether
        if char_name.effects["Food Poisoning"]['active']:
            char_name.override_portrait("portrait", "indifferent")
            rc("She does not look good...")
            char_name.restore_portrait()
            return True
        elif char_name.vitality <= 10:
            char_name.override_portrait("portrait", "indifferent")
            rc("She looks very tired...")
            char_name.restore_portrait
            return True
        elif char_name.health < (round(char_name.get_max("health")*0.2)):
            char_name.override_portrait("portrait", "indifferent")
            rc("She does not look good...")
            char_name.restore_portrait()
            return True
        elif char_name.effects["Down with Cold"]['active']:
            char_name.override_portrait("portrait", "indifferent")
            rc("She looks a bit pale...")
            char_name.restore_portrait
            return False
        elif char_name.joy <= 20:
            char_name.override_portrait("portrait", "sad")
            rc("She looks pretty sad...")
            char_name.restore_portrait()
            return False
        else:
            return False
            
    def rc(*args):
        """
        random choice function
        Wrapper to enable simpler girl_meets choices, returns whatever char_gm is set to along with a random line.
        """
        # https://github.com/Xela00/PyTFall/issues/37
        return char.say(choice(list(args)))
        
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
                if key in char.traits:
                    l.extend(d[key])
            else:
                if eval(key):
                    l.extend(d[key])
        # raise Exception, l
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
        return any(i in l for i in char.traits)
        
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
        for occ in char.traits:
            if hasattr(occ, "occupations"):
                gen_occs = gen_occs.union(set(occ.occupations))
        return any(i for i in list(args) if i in gen_occs)
        
    def cgochar(char, *args):
        """
        Checks for General Occupation strings, such as "SIW", "Warrior", "Server", etc. Goes with char argument, thus can be used where the game doesn't recognize default "char"
        """
        gen_occs = set()
        for occ in char.traits:
            if hasattr(occ, "occupations"):
                gen_occs = gen_occs.union(set(occ.occupations))
        return any(i for i in list(args) if i in gen_occs)
        
    def d(value):
        """
        Checks if disposition of the girl is any higher that value.
        """
        return char.disposition >= value
        
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
                    
    # Other:
    def find_les_partners():
        """
        Returns a set with if any partner(s) is availible and willing at the location.
        (lesbian action)
        *We can move this to GM class and have this run once instead of twice! (menu + label)
        """
        # First get a set of all girls at the same location as the current character:
        partners = set()
        for i in chars.values():
            if i.location == char.location:
                partners.add(i)
                
        # Next figure out if disposition of possible partners towards MC is high enough for them to agree and/or they are lovers of char.
        willing_partners = set()
        for i in partners:
            if char != i: # @review: (Alex) make sure we do not pick the girl to fuck herself...
                # @review: (Alex) vitality is a fixed stat but it's best to check health as a percentage of it's max (60%+), 25 can feel like near death for some characters.
                if (check_lovers(i, hero) or check_lovers(char, i)) and not (i.vitality < 25 or i.health < i.get_max("health")*0.6) and not (i.disposition <= -50): # Last check is too make sure partner doesn't dislike the MC.
                    willing_partners.add(i)
        # @review: (Alex) renamed the function. We are returning all choices, nit just the one partner.
        return willing_partners
        
    def interactions_run_gm_anywhere(char, place, background):
        """           
        Runs (or doesn't) gm or interactions with the char based on her status
        """
        if chars[char].status == "slave" or not(chars[char].is_available):
            narrator("Nobody's here...")
            renpy.jump(place)
        elif chars[char] in hero.girls:
            gm.start("girl_interactions", chars[char], chars[char].get_vnsprite(), place, background)
        else:
            gm.start("girl_meets", chars[char], chars[char].get_vnsprite(), place, background)
            
    # Image tag overwrites:
    def get_sex_img_4int(char, *args, **kwargs):
        """Tries to find the best possible sex image following a complex set of logic.
        http://www.pinkpetal.org/index.php?topic=1291.msg37131#msg37131
        
        Coded for interactions module.
        """
        # First check if we have a perfect match of all tags:
        if char.has_image(*args, **kwargs):
            gm.set_img(*args, **kwargs)
            return
        
        tags = list(args)
        exclude = kwargs.get("exclude", None)
            
        # Next we give priority to partner_hidden logic:
        if "partner_hidden" in tags:
            ptags = list(t for t in tags if t not in loc_tags)
            if substitute_show_bg(char, ptags, **kwargs):
                return
            
            # No parter_hidden tags found... we subsitute partner_hidden with after_sex
            ptags = tags[:]
            ptags.remove("partner_hidden")
            if "after_sex" not in ptags:
                ptags.append("after_sex")
                
            if char.has_image(*ptags, **kwargs):
                gm.set_img(*ptags, **kwargs)
                return
                
            ptags = list(t for t in ptags if t not in loc_tags)
            if substitute_show_bg(char, ptags, **kwargs):
                return
                
        # If threre was no partner_hidden or everything failed:
        if "partner_hidden" in tags:
            tags.remove("partner_hidden")
            
        if char.has_image(*tags, **kwargs):
            gm.set_img(*tags, **kwargs)
            return
            
        ptags = list(t for t in tags if t not in loc_tags)
        if substitute_show_bg(char, ptags, **kwargs):
            return
            
        # We could not find an image with the correct location/bgs, so we go with after_sex:
        ptags = list(t for t in tags if t not in sex_action_tags)
        if "after_sex" not in ptags:
            ptags.append("after_sex")
            
        if char.has_image(*ptags, **kwargs):
            gm.set_img(*ptags, **kwargs)
            return
        
        ptags = list(t for t in tags if t not in loc_tags)
        if substitute_show_bg(char, ptags, **kwargs):
            return
            
        # Still nothing... We try to get a picture just with the after_sex and a location followed by no_bg/simple_bg if no loc was found:
        locs = list(t for t in tags if t in loc_tags)
        if char.has_image("after_sex", *locs, **kwargs):
            gm.set_img("after_sex", *locs, **kwargs)
            return
            
        if substitute_show_bg(char, ["after_sex"], **kwargs):
            return
            
        # //This can be cleaned up and refactored one working correctly!!
        # Drop Nature First:
        if any([t for t in ["outdoors", "urban", "wildness", "suburb", "nature"] if t in tags]):
            ptags = [t for t in tags if t not in ["nature"]]
            if char.has_image(*ptags, **kwargs):
                gm.set_img(*ptags, **kwargs)
                return
                
        if any([t for t in ["urban", "wildness", "suburb"] if t in tags]):
            ptags = [t for t in tags if t not in ["urban", "wildness", "suburb"]]
            if "outdoors" not in ptags:
                ptags.append("outdoors")
            if char.has_image(*ptags, **kwargs):
                gm.set_img(*ptags, **kwargs)
                return
                
        if any([t for t in ["dungeon", "living", "public"] if t in tags]):
            ptags = [t for t in tags if t not in ["dungeon", "living", "public"]]
            if "indoors" not in ptags:
                ptags.append("indoors")
            if char.has_image(*ptags, **kwargs):
                gm.set_img(*ptags, **kwargs)
                return
                
        if any([t for t in ["indoors", "outdoors"] if t in tags]):
            ptags = [t for t in tags if t not in ["indoors", "outdoors", "simple bg", "no bg"]]
            if substitute_show_bg(char, ptags, **kwargs):
                return
                
        if any([t for t in ["beach", "onsen", "pool", "stage"] if t in tags]):
            ptags = [t for t in tags if t not in ["beach", "onsen", "pool", "stage", "simple bg", "no bg"]]
            if substitute_show_bg(char, ptags, **kwargs):
                return
        
        # Finally, we just run the normal show:
        gm.set_img(*args, **kwargs)
            
    def substitute_show_bg(char, tags, **kwargs):
        # Try it with the simple_bg:
        _tags = tags[:]
        _tags.append("simple bg")
        if char.has_image(*_tags, **kwargs):
            gm.set_img(*_tags, **kwargs)
            return True
            
        # Try it with no_bg:
        _tags = tags[:]
        _tags.append("no bg")
        if char.has_image(*_tags, **kwargs):
            gm.set_img(*_tags, **kwargs)
            return True