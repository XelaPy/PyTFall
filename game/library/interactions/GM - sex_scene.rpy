init python:
    def get_simple_act(char, tags, excluded): # copypaste from jobs without the self part, allows to randomly select one of existing tags sets
        acts = list()
        for t in tags:
            if char.has_image(*t, exclude=excluded):
                acts.append(t)
        if acts:
            act = choice(acts)
        else:
            act = None
        return act
        
        
    def get_single_sex_picture(char=None, act="stripping", location="any", hidden_partner=False):
        """A universal function that returns most suitable sex picture depending on arguments.
        char - character id
        act - sex act; list of possible acts can be seen in the first check here
        location - location where is happens; the function supports following locations: park, forest, beach, room, any (aka simple bg/no bg)
        all other cases are too rare anyway, and should be handled manually
        hidden_partner - should it try to show the hidden partner pictures first, or it doesn't matter; doesn't work for strip and after_sex, obviously
        """

        if act not in ["blowjob", "titsjob", "handjob", "footjob", "vaginal", "anal", "stripping", "masturbation"]:
            act = "stripping"
            
        if act == "stripping":
            excluded = ["in pain", "scared", "sad", "sleeping", "bathing", "stage", "sex"]
            if location == "beach":
                excluded.extend(["indoors"])
                if dice(50):
                    included = ["beach"]
                else:
                    included = ("beach", "swimsuit")
                if char.has_image("stripping", "beach", exclude=excluded):
                    gm.set_img("stripping", *included, exclude=excluded, type="reduce")
                elif char.has_image("nude", "beach", exclude=excluded):
                    gm.set_img("nude", *included, exclude=excluded, type="reduce")
                elif char.has_image("lingerie", "beach", exclude=excluded):
                    gm.set_img("lingerie", *included, exclude=excluded, type="reduce")
                else:
                    tags = (["simple bg", "stripping"], ["no bg", "stripping"], ["simple bg", "nude"], ["no bg", "nude"], ["no bg", "lingerie"], ["simple bg", "lingerie"])
                    result = get_simple_act(char, tags, excluded)
                    if result:
                        gm.set_img(*result, exclude=excluded)
                    else:
                        if char.has_image ("stripping"):
                            gm.set_img("stripping", "outdoors", *included, type="reduce")
                        else:
                            gm.set_img("nude", "outdoors", *included, exclude=["sex"], type="reduce")
            
            elif location in ["park", "forest"]:
                excluded.extend(["indoors", "onsen", "pool", "beach"])
                if location == "forest":
                    included = ("nature", "wildness")
                else:
                    included = ("nature", "urban")
                if char.has_image("stripping", "nature", exclude=excluded):
                    gm.set_img("stripping", *included, exclude=excluded, type="reduce")
                elif char.has_image("nude", "nature", exclude=excluded):
                    gm.set_img("nude", *included, exclude=excluded, type="reduce")
                elif char.has_image("lingerie", "nature", exclude=excluded):
                    gm.set_img("lingerie", *included, exclude=excluded, type="reduce")
                else:
                    tags = (["simple bg", "stripping"], ["no bg", "stripping"], ["simple bg", "nude"], ["no bg", "nude"], ["no bg", "lingerie"], ["simple bg", "lingerie"])
                    result = get_simple_act(char, tags, excluded)
                    if result:
                        gm.set_img(*result, exclude=excluded)
                    else:
                        if char.has_image ("stripping"):
                            gm.set_img("stripping", "outdoors", *included, type="reduce")
                        else:
                            gm.set_img("nude", "outdoors", *included, exclude=["sex"], type="reduce")

            elif location == "room":
                included = ("indoors", "living")
                excluded.extend(["outdoors", "onsen", "pool", "beach", "dungeon", "public"])
                if char.has_image("stripping", "indoors", exclude=excluded):
                    gm.set_img("stripping", *included, exclude=excluded, type="reduce")
                elif char.has_image("nude", "indoors", exclude=excluded):
                    gm.set_img("nude", *included, exclude=excluded, type="reduce")
                elif char.has_image("lingerie", "indoors", exclude=excluded):
                    gm.set_img("lingerie", *included, exclude=excluded, type="reduce")
                else:
                    tags = (["simple bg", "stripping"], ["no bg", "stripping"], ["simple bg", "nude"], ["no bg", "nude"], ["no bg", "lingerie"], ["simple bg", "lingerie"])
                    result = get_simple_act(char, tags, excluded)
                    if result:
                        gm.set_img(*result, exclude=excluded, type="reduce")
                    else:
                        if char.has_image ("stripping"):
                            gm.set_img("stripping", *included, type="reduce")
                        else:
                            gm.set_img("nude", *included, exclude=["sex"], type="reduce")
            else:
                tags = (["simple bg", "stripping"], ["no bg", "stripping"], ["simple bg", "nude"], ["no bg", "nude"], ["no bg", "lingerie"], ["simple bg", "lingerie"])
                result = get_simple_act(char, tags, excluded)
                if result:
                    gm.set_img(*result, exclude=excluded)
                else:
                    if char.has_image ("stripping"):
                        gm.set_img("stripping")
                    else:
                        gm.set_img("nude", exclude=["sex"])
        
        elif act == "masturbation":
            excluded=["forced", "normalsex", "group", "bdsm", "after sex", "in pain", "sad", "scared"]
            if location == "beach":
                excluded.extend(["indoors"])
                if dice(50):
                    included = ["beach"]
                else:
                    included = ("beach", "swimsuit")
                if char.has_image("masturbation", "beach", exclude=excluded):
                    gm.set_img("masturbation", *included, exclude=excluded, type="reduce")
                else:
                    tags = (["simple bg", "masturbation"], ["no bg", "masturbation"])
                    result = get_simple_act(char, tags, excluded)
                    if result:
                        gm.set_img(*result, exclude=excluded)
                    elif char.has_image("nude", "beach", exclude=["sleeping", "bathing", "stage", "sex"]):
                        gm.set_img("nude", "beach", exclude=["sleeping", "bathing", "stage", "sex"], type="reduce")
                    else:
                        gm.set_img("nude", "outdoors", exclude=["sleeping", "bathing", "stage", "sex"], type="reduce")
                        
            elif location in ["park", "forest"]:
                excluded.extend(["indoors", "onsen", "pool", "beach"])
                if location == "forest":
                    included = ("nature", "wildness")
                else:
                    included = ("nature", "urban")
                if char.has_image("masturbation", "nature", exclude=excluded):
                    gm.set_img("masturbation", *included, exclude=excluded, type="reduce")
                else:
                    tags = (["simple bg", "masturbation"], ["no bg", "masturbation"])
                    result = get_simple_act(char, tags, excluded)
                    if result:
                        gm.set_img(*result, exclude=excluded)
                    elif char.has_image("nude", "nature", exclude=["sleeping", "bathing", "stage", "sex"]):
                        gm.set_img("nude", *included, exclude=["sleeping", "bathing", "stage", "sex"], type="reduce")
                    else:
                        gm.set_img("nude", "outdoors", exclude=["sleeping", "bathing", "stage", "sex"], type="reduce")
                            
            elif location == "room":
                excluded.extend(["outdoors", "onsen", "pool", "beach", "dungeon", "public"])
                if char.has_image("masturbation", "indoors", exclude=excluded):
                    gm.set_img("masturbation", "indoors", "living", exclude=excluded, type="reduce")
                else:
                    tags = (["simple bg", "masturbation"], ["no bg", "masturbation"])
                    result = get_simple_act(char, tags, excluded)
                    if result:
                        gm.set_img(*result, exclude=excluded)
                    elif char.has_image("masturbation", "indoors", exclude=excluded):
                        gm.set_img("masturbation", "indoors", exclude=excluded)
                    elif char.has_image("nude", "indoors", exclude=["sleeping", "bathing", "stage", "sex"]):
                        gm.set_img("nude", "indoors", "living", exclude=["sleeping", "bathing", "stage", "sex"], type="reduce")
            else:
                tags = (["simple bg", "masturbation"], ["no bg", "masturbation"])
                result = get_simple_act(char, tags, excluded)
                if result:
                    gm.set_img(*result, exclude=excluded)
                else:
                    if char.has_image("masturbation", exclude=excluded):
                        gm.set_img("masturbation", exclude=excluded)
                    else:
                        gm.set_img("nude", exclude=["sex"])
                        
        elif act in ["blowjob", "titsjob", "handjob", "footjob", "vaginal", "anal"]:
            if act in ["vaginal", "anal"]:
                act_tag = "2c " + act
                excluded=["in pain", "scared", "sad", "rape", "restrained", "angry", "gay"]
                excluded_1=["sad", "in pain", "scared", "rape", "gay"]
            else:
                act_tag = "bc " + act
                excluded=["in pain", "scared", "sad", "rape", "restrained", "angry"]
                excluded_1=["in pain", "scared", "rape", "sad"]
            
            if location in ["beach", "park", "forest", "room"]:
                included = []
                if location == "beach":
                    excluded.extend(["indoors", "dungeon"])
                    excluded_1.extend(["indoors", "dungeon"])
                    included.extend(["beach"])
                elif location in ["park", "forest"]:
                    excluded.extend(["indoors", "pool", "beach"])
                    excluded_1.extend(["indoors", "pool", "beach"])
                    included.extend(["nature"])
                elif location == "room":
                    excluded.extend(["outdoors", "onsen", "pool", "beach", "dungeon", "public"])
                    excluded_1.extend(["outdoors", "pool", "beach", "dungeon"])
                    included = (["indoors"])
                    
                if char.has_image(act_tag, *included, exclude=excluded):
                    if location == "forest":
                        included.extend(["wildness"])
                    elif location == "park":
                        included.extend(["urban"])
                    elif location == "room":
                        included.extend(["living"])
                    if hidden_partner:
                        included.extend(["partnerhidden"])
                    gm.set_img(act_tag, *included, exclude=excluded, type="reduce")
                elif char.has_image(act_tag, *included, exclude=excluded_1):
                    if location == "forest":
                        included.extend(["wildness"])
                    elif location == "park":
                        included.extend(["urban"])
                    elif location == "room":
                        included.extend(["living"])
                    if hidden_partner:
                        included.extend(["partnerhidden"])
                    gm.set_img(act_tag, *included, exclude=excluded_1, type="reduce")
                elif char.has_image("after sex", *included, exclude=excluded):
                    if location == "forest":
                        included.extend(["wildness"])
                    elif location == "park":
                        included.extend(["urban"])
                    elif location == "room":
                        included.extend(["living"])
                    gm.set_img("after sex", *included, exclude=excluded, type="reduce")
                elif char.has_image("after sex", *included, exclude=excluded_1):
                    if location == "forest":
                        included.extend(["wildness"])
                    elif location == "park":
                        included.extend(["urban"])
                    elif location == "room":
                        included.extend(["living"])
                    gm.set_img("after sex", *included, exclude=excluded_1, type="reduce")
                else:
                    tags = ([act_tag, "simple bg"], ["no bg", act_tag])
                    result = get_simple_act(char, tags, excluded)
                    if result:
                        if hidden_partner:
                            result.extend(["partnerhidden"])
                        gm.set_img(*result, exclude=excluded, type="reduce")
                    else:
                        tags = (["after sex", "simple bg"], ["no bg", "after sex"])
                        result = get_simple_act(char, tags, excluded)
                        if result:
                            if hidden_partner:
                                result.extend(["partnerhidden"])
                            gm.set_img(*result, exclude=excluded, type="reduce")
                        else:
                            excluded.extend(["sex"])
                            gm.set_img("nude", *included, exclude=excluded, type="reduce")
                            
            else:
                tags = ([act_tag, "simple bg"], ["no bg", act_tag], ["no bg", "after sex"], ["simple bg", "after sex"])
                result = get_simple_act(char, tags, excluded)
                if result:
                    if hidden_partner:
                        result.extend(["partnerhidden"])
                    gm.set_img(*result, exclude=excluded, type="reduce")
                else:
                    result = get_simple_act(char, tags, excluded_1)
                    if result:
                        if hidden_partner:
                            result.extend(["partnerhidden"])
                        gm.set_img(*result, exclude=excluded, type="reduce")
                    else:
                        excluded.extend(["sex"])
                        gm.set_img("nude", *included, exclude=excluded, type="reduce")
                    

        return
            
        
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
