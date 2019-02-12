init python:
    def get_rape_picture(char=None, hidden_partner=False):
        """
        This function returns the best possible rape picture, without specifying where or what kind of action it should have since rape pics are not common enough to be so demanding.
        """
        excluded = ["happy", "confident", "suggestive", "ecstatic", "gay"]
        if char.has_image("normalsex", "rape", exclude=["gay"]):
            if hidden_partner:
                gm.set_img("normalsex", "rape", "partnerhidden", exclude=["gay"], type="reduce")
            else:
                gm.set_img("normalsex", "rape", exclude=["gay"], type="reduce")
        elif char.has_image("normalsex", exclude=excluded):
            if hidden_partner:
                gm.set_img("normalsex", "partnerhidden", exclude=excluded, type="first_default")
            else:
                gm.set_img("normalsex", exclude=excluded, type="first_default")
        else:
            gm.set_img("normalsex", "partnerhidden", "ripped", exclude=["gay", "happy", "confident"], type="reduce")
        return
        
    def get_single_sex_picture(char, act="stripping", location="any", hidden_partner=False):
        """A universal function that returns most suitable sex picture depending on arguments.
        char - character id
        act - sex act; list of possible acts can be seen in the first check here
        location - location where is happens; the function supports following locations: park, forest, beach, room, any (aka simple bg/no bg)
        all other cases are too rare anyway, and should be handled manually
        hidden_partner - should it try to show the hidden partner pictures first, or it doesn't matter; doesn't work for strip and after_sex, obviously
        """

        # prepare excludeds
        excluded = ["in pain", "scared", "sad", "rape", "forced", "group"]

        # prepare for location
        loc_tag = location
        optional_included = []
        if location == "room":
            loc_tag = "living"
        elif location == "beach":
            if dice(50):
                optional_included = ["swimsuit"]
        elif location == "park":
            loc_tag = "nature"

            excluded.extend(["beach", "wildness"])
        elif location == "forest":
            loc_tag = "nature"
            excluded.extend(["beach", "urban"])

        if act == "stripping":
            excluded.append("sex")

            # try to find a stripping image
            if char.has_image("stripping", loc_tag, exclude=excluded):
                gm.set_img("stripping", loc_tag, *optional_included, exclude=excluded, type="reduce")
            else:
                tags = (["simple bg", "stripping"], ["no bg", "stripping"])
                result = get_simple_act(char, tags, excluded)
                if result:
                    result.extend(optional_included)
                    gm.set_img(*result, exclude=excluded, type="reduce")
                else:
                    # could not find a stripping image, check for lingerie or nude pictures
                    excluded.extend(["sleeping", "bathing", "stage", "sex"])

                    if char.has_image("lingerie", loc_tag, exclude=excluded):
                        gm.set_img("lingerie", loc_tag, *optional_included, exclude=excluded, type="reduce")
                    elif char.has_image("nude", loc_tag, exclude=excluded):
                        gm.set_img("nude", loc_tag, *optional_included, exclude=excluded, type="reduce")
                    else:
                        tags = (["simple bg", "nude"], ["no bg", "nude"], ["simple bg", "lingerie"], ["no bg", "lingerie"])
                        result = get_simple_act(char, tags, excluded)
                        if result:
                            result.extend(optional_included)
                            gm.set_img(*result, exclude=excluded, type="reduce")
                        else:
                            # whatever...
                            gm.set_img("nude", loc_tag, *optional_included, exclude=excluded, type="reduce")

        elif act == "masturbation":
            excluded.extend(["normalsex", "bdsm", "after sex"])

            if char.has_image("masturbation", loc_tag, exclude=excluded):
                gm.set_img("masturbation", loc_tag, *optional_included, exclude=excluded, type="reduce")
            else:
                tags = (["simple bg", "masturbation"], ["no bg", "masturbation"])
                result = get_simple_act(char, tags, excluded)
                if result:
                    result.extend(optional_included)
                    gm.set_img(*result, exclude=excluded, type="reduce")
                else:
                    # could not find masturbation image, check for nude pictures
                    excluded.extend(["sleeping", "bathing", "stage", "sex"])

                    gm.set_img("nude", loc_tag, *optional_included, exclude=excluded, type="reduce")

        else: # any 2c/bc sexual act
            # prepare base excludeds
            excluded_1 = list(excluded)
            excluded.extend(["restrained", "angry"])
            
            # partner filters
            if char.gender == hero.gender:
                excluded.append("straight")
                excluded_1.append("straight")
            else:
                excluded.append("gay")
                excluded_1.append("gay") 
            if hidden_partner:
                optional_included.append("partnerhidden")
            else:
                optional_included.append("sexwithmc")

            # image selection
            if char.has_image(act, loc_tag, exclude=excluded):
                gm.set_img(act, loc_tag, *optional_included, exclude=excluded, type="reduce")
            elif char.has_image(act, loc_tag, exclude=excluded_1):
                gm.set_img(act, loc_tag, *optional_included, exclude=excluded_1, type="reduce")
            elif char.has_image("after sex", loc_tag, exclude=excluded):
                gm.set_img("after sex", loc_tag, *optional_included, exclude=excluded, type="reduce")
            elif char.has_image("after sex", loc_tag, exclude=excluded_1):
                gm.set_img("after sex", loc_tag, *optional_included, exclude=excluded_1, type="reduce")
            else:
                tags = ([act, "simple bg"], [act, "no bg"], ["after sex", "simple bg"], ["after sex", "no bg"])
                result = get_simple_act(char, tags, excluded)
                if result:
                    result.append(optional_included[-1])
                    gm.set_img(*result, exclude=excluded, type="reduce")
                else:
                    excluded.append("sex")
                    gm.set_img("nude", loc_tag, exclude=excluded, type="reduce")

        return
        
    def get_picture_before_sex(char=None, location="room"): # here we set initial picture before the scene begins depending on location
        excluded = ["sex", "sleeping", "angry", "in pain", "sad", "scared", "bathing"]
        # prepare for location
        loc_tag = location
        underwear = "lingerie"
        if location == "room":
            loc_tag = "living"
        elif location == "beach":
            underwear = "swimsuit"
        elif location == "park":
            loc_tag = "nature"
            excluded.extend(["beach", "wildness"])
        elif location == "forest":
            loc_tag = "nature"
            excluded.extend(["beach", "urban"])

        if char.has_image(loc_tag, underwear, exclude=excluded):
            gm.set_img(loc_tag, underwear, "nude", exclude=excluded, type="reduce")
        elif char.has_image(loc_tag, "nude", exclude=excluded):
            gm.set_img(loc_tag, "nude", exclude=excluded, type="reduce")
        else:
            tags = (["simple bg", underwear], ["no bg", underwear])
            result = get_simple_act(char, tags, excluded)
            if result:
                result.append("nude")
                gm.set_img(*result, exclude=excluded, type="reduce")
            else:
                tags = (["simple bg", "nude"], ["no bg", "nude"])
                result = get_simple_act(char, tags, excluded)
                if result:
                    gm.set_img(*result, exclude=excluded, type="reduce")
                else:
                    gm.set_img("nude", underwear, exclude=excluded, type="reduce")

        return
        
    def get_character_libido(char, mc=True): # depending on character traits returns relative libido level, ie how much the character wishes to have sex with MC
    # has nothing to do with character's willingness to even start sex; if mc = false then we calculate it not for mc, ie ignore some personal traits
    # it's more or less permanent pseudostat compared to many other games where it changes regularly like health, if not more often

        l = locked_random("randint", 3, 5)
        if ct("Nymphomaniac"):
            l += 2
        elif ct("Frigid"):
            l -= 1
        
        if mc:
            if ct("Half-Sister") and not "Sister Lover" in hero.traits:
                if char.disposition >= 700:
                    l += locked_random("randint", 1, 2)
                else:
                    l -= 1
            if check_lovers(hero, char):
                l += 1
            
        if cgo("SIW") and l < 3: # sex workers can't have it less than 3 though
            l = 3
            
        if ct("Virgin"): # or 2 if virgins...
            l -= 1

        if l < 1:
            l = 1 # normalization, in general libido can be from 1 to 7 for frigid ones and from 3 to 10 for nymphomaniacs
        return l
        
    def get_character_wishes(char): # for taking action during sex scenes, returns action that character is willing to commit on her own
        skills = ["sex", "oral", "anal"]
        if (char.status != "slave" and check_lovers(hero, char)) or not(ct("Virgin")):
            skills.extend(["vaginal"])
        skills_values=[]
        for t in skills:
            skills_values.append([t, char.get_skill(t)])
        result = weighted_choice(skills_values)
        if not(result):
            result=choice(skills)
        return result
            
    def get_sex_img_4int(char, *args, **kwargs):
        """Tries to find the best possible sex image following a complex set of logic.
        
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
