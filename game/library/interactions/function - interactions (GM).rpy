init -11 python:
    # Interactions (Girlsmeets Helper Functions):
    def interactions_set_repeating_lines_limit(c): # returns the number of character "patience", ie how many repeating lines she's willing to listen in addition to default value
        if check_lovers(c, hero):
            patience = randint(1,2)
        elif check_friends(c, hero):
            patience = 1
        else:
            patience = 0
            
        if "Well-mannered" in c.traits:
            patience += randint(0,1)
        elif "Ill-mannered" in c.traits:
            patience -= randint(0,1)
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
        elif char_name.vitality <= round(char_name.get_max("vitality")*0.1):
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
            rc("But [char.name] was too ill to pay any serious attention to you.", "But her aching stomach completely occupies her thoughts.")
            char_name.restore_portrait()
            char_name.disposition -= randint(2, 5)
            renpy.jump("girl_interactions_end")
        elif char_name.vitality <= round(char_name.get_max("vitality")*0.1):
            char_name.override_portrait("portrait", "indifferent")
            rc("But [char.name] was too tired to even talk.", "Sadly, [char.name] was not very happy that you interrupted her rest.", "But she is simply too tired to pay any serious attention to you.", "Unfortunately she so tired she almost falls asleep on the move.")
            char_name.restore_portrait()
            char_name.disposition -= randint(5, 10)
            char_name.vitality -= 2
            renpy.jump("girl_interactions_end")
        elif char_name.health < (round(char_name.get_max("health")*0.2)):
            char_name.override_portrait("portrait", "indifferent")
            rc("But [char.name] is too wounded for that.", "But her wounds completely occupy her thoughts.")
            char_name.restore_portrait()
            char_name.disposition -= randint(5, 15)
            char_name.vitality -= 2
            renpy.jump("girl_interactions_end")
    
    def interactions_check_for_minor_bad_stuff(char_name): # we check minor issues when character might refuse to do something based on dice
        if (not("Pessimist" in char_name.traits) and char_name.joy <= 25) or (("Pessimist" in char_name.traits) and char_name.joy < 10):
            if dice(hero.charisma-char.character) and dice(80):
                narrator(choice(["Looks like she is in a bad mood, however you managed to cheer her up."]))
                char_name.disposition += 1
                char_name.joy += randint(3, 6)
            else:
                narrator(choice(["Looks like she is in a bad mood today and not does not want to do anything."]))
                renpy.jump ("girl_interactions")
        elif char_name.effects["Down with Cold"]['active']: #if she's ill, there is a chance that she will disagree to chat
            if dice(hero.charisma-char.character) and dice(80):
                narrator(choice(["Looks like she is not feeling well today, however you managed to cheer her up a bit."]))
                char_name.disposition += 2
                char_name.joy += randint(1, 5)
            else:
                narrator(choice(["She is not feeling well today and not in the mood to do anything."]))
                renpy.jump ("girl_interactions")
        elif char_name.vitality <= round(char_name.get_max("vitality")*0.2) and dice (35):
            char.override_portrait("portrait", "tired")
            if ct("Impersonal"):
                rc("I don't have required endurance at the moment. Let's postpone it.", "No. Not enough energy.")
            elif ct("Shy") and dice(50):
                rc("W-well, I'm a bit tired right now... Maybe some other time...", "Um, I-I don't think I can do it, I'm exhausted. Sorry...")
            elif ct("Imouto"):
                rc("Noooo, I'm tired. I want to sleep.", "Z-z-z *she falls asleep on the feet*") 
            elif ct("Dandere"):
                rc("No. Too tired.", "Not enough strength. I need to rest.")
            elif ct("Tsundere"):
                rc("I must rest at first. Can't you tell?", "I'm too tired, don't you see?! Honestly, some people...")
            elif ct("Kuudere"):
                rc("I'm quite exhausted. Maybe some other time.", "I really could use some rest right now, my body is tired.")
            elif ct("Kamidere"):
                rc("I'm tired, and have to intentions to do anything but rest.", "I need some rest. Please don't bother me.")
            elif ct("Bokukko"):
                rc("Naah, don't wanna. Too tired.", "*yawns* I could use a nap first...")
            elif ct("Ane"):
                rc("Unfortunately I'm quite tired at the moment. I'd like to rest a bit.", "Sorry, I'm quite sleepy. Let's do it another time.")
            elif ct("Yandere"):
                rc("Ahh, my whole body aches... I'm way too tired.", "The only thing I can do properly now is to take a good nap...")
            else:
                rc("*sign* I'm soo tired lately, all I can think about is a cozy warm bed...", "I am ready to drop. Some other time perhaps.")
            char.restore_portrait()
            char_name.disposition -= randint(0, 1)
            char_name.vitality -= randint(1, 2)
            renpy.jump("girl_interactions")
            
    def interactions_checks_for_bad_stuff_greetings(char_name): # Special beginnings for greetings if something is off, True/False show that sometimes we even will need to skip a normal greeting altogether
        if char_name.effects["Food Poisoning"]['active']:
            char_name.override_portrait("portrait", "indifferent")
            rc("She does not look good...")
            char_name.restore_portrait()
            return True
        elif char_name.vitality <= 40:
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
        elif char_name.joy <= 25:
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
        Runs (or doesn't) gm or interactions with the char based on her status; place is where we jump after gm is over
        """
        if chars[char].status == "slave" or not(chars[char].is_available):
            narrator("Nobody's here...")
            renpy.jump(place)
        elif chars[char] in hero.chars:
            gm.start("girl_interactions", chars[char], chars[char].get_vnsprite(), place, background)
        else:
            gm.start("girl_meets", chars[char], chars[char].get_vnsprite(), place, background)
            
    def interactions_prebattle_line(characters):
        """
        Outputs nonrepeatable prebattle lines for provided characters, except hero if s/he was provided.
        """
        characters = [c for c in characters if c != hero]
        if characters:
            said_lines = set()
            for character in characters:
                if "Impersonal" in character.traits:
                    lines = ["Target acquired, initialising battle mode.", "Enemy spotted. Engaging combat.", "Battle phase, initiation. Weapons online.", "Better start running. I'm afraid I can't guarantee your safety.", "Enemy analysis completed. Switching to the combat routine.", "Target locked on. Commencing combat mode."]
                elif "Imouto" in character.traits:
                    lines = ["Ahaha, we'll totally beat you up!", "Behold of my amazing combat techniques, [mc_ref]! ♪", "All our enemies will be punished! ♫", "Activate super duper mega ultra assault mode! ♪", "Huh? Don't they know we're too strong for them?"]
                elif "Dandere" in character.traits:
                    lines = ["Want to fight? We'll make you regret it.", "Let's end this quickly, [mc_ref]. We have many other things to do.", "Of course we'll win.", "This will be over before you know it.", "If something bad happens to the enemy, don't blame me."]
                elif "Tsundere" in character.traits:
                    lines = ["Well-well. Looks like we have some new targets, [mc_ref] ♪", "Hmph! You're about 100 years too early to defeat us!", "We won't go easy on you!", "There's no way you could win!", "[mc_ref], you can stay back if you wish. I'll show you how it's done.", "I won't just defeat you, I'm gonna shatter you!"]
                elif "Kuudere" in character.traits:
                    lines = ["Oh, you dare to stand against us?", "Fine, we accept your challenge. Let's go, [mc_ref].", "Don't worry, [mc_ref]. This battle will be over soon enough.", "Are you prepared to know our power?", "You picked a fight with the wrong girl."]
                elif "Kamidere" in character.traits:
                    lines = ["Get ready, [mc_ref]. We have some lowlife to crash.", "So you want us to teach you some manners, huh?", "You have made a grave error challenging us. Retreat while you can.", "Time to take out the trash.", "You should leave this place and cower in your home. That is the proper course for one so weak.", "You need to be put back in your place."]
                elif "Bokukko" in character.traits:
                    lines = ["Wanna throw hands, huh? Better be ready to catch them!", "I'm gonna beat you silly! Cover me, [mc_ref]!", "You wanna go? Alrighty, eat some of this!", "Time to kick some ass.", "I'm gonna whack you good!", "All right, let's clean this up fast!"]
                elif "Ane" in character.traits:
                    lines = ["Don't worry, [mc_ref]. I'll protect you.", "Can't say I approve of this sort of thing, but we are out of options, [mc_ref].", "Don't feel sorry for them, [mc_ref]. They asked for it.", "We mustn't let our guard down, [mc_ref]."]
                elif "Yandere" in character.traits:
                    lines = ["Please stand aside, [mc_ref]. Or you'll get blood on you...", "Do not worry. The nothingness is gentle ♪", "Here comes the hurt!", "This could get a little rough... Because I like it rough ♫", "Mind if I go a little nuts, [mc_ref]?"]
                else:
                    lines = ["I suppose we have to use force, [mc_ref]. I'll cover you.", "Alright then. If you want a fight, we'll give it to you!", "Ok, let's settle this.", "I'll fight to my last breath!"]
                result = random.sample(set(lines).difference(said_lines), 1)[0]
                said_lines.add(result)
                result = result.replace("[mc_ref]", character.mc_ref)
                character.override_portrait("portrait", "confident")
                character.say(result)
                character.restore_portrait()
                
    def interactions_eating_line(characters):
        """
        Outputs nonrepeatable lines during eating for provided characters, except hero if s/he was provided.
        """
        characters = [c for c in characters if c != hero]
        if characters:
            said_lines = set()
            for character in characters:
                if "Impersonal" in character.traits:
                    lines = ["It's all sticky from the sauce... Nn... *chu* Mm... *slurp*", "Nn... mm... Delicious...", "That looks tasty... *slurp*"]
                elif "Shy" in character.traits and dice(50):
                    lines = ["That looks so good! Ah! That one looks good too... Aww, I can't decide...", "Hehe, sweet tea is so calming, isn't it?", "Uhm, w-were you going to eat that? Er... Y-yes, I'll eat it..."]
                elif "Imouto" in character.traits:
                    lines = ["Custard here and chocolate here. Looks delicious, doesn't it? ♪", "So many sweets! What should I start with? ♪", "Oh, that looks yummy... Diggin' in! Nom!"]
                elif "Dandere" in character.traits:
                    lines = ["*munch munch*... Huh? You want some too? Here.", "Omelette rolls are so sweet and sticky...", "Munch munch... Sugar intake is important.", "Thanks for the food... *munch*"]
                elif "Tsundere" in character.traits:
                    lines = ["Ah, I'm tired from eating too much...", "How long do you plan on staring at my lunch? I'm not sharing any.", "Lately, I am worrying quite a bit about calories... But I just can't help myself... ugh..."]
                elif "Kuudere" in character.traits:
                    lines = ["Mmm, this is actually pretty good.", "They don't have any teacakes today..? A pity.", "You've got a good appetite. It's refreshing to see.", "I don't need any... Well, if you insist... *aaaah*..."]
                elif "Kamidere" in character.traits:
                    lines = ["OK, say ah~n... Yeah right, like I would ever do such a thing.", "Can't you just be quiet and eat? It's improper.", "Don't talk to me when I'm eating."]
                elif "Bokukko" in character.traits:
                    lines = ["Hm, which one tastes better... I wonder...", "Nom nom... Mmm, delishus ♪ Back to full health ♪", "Mm, delicious meat. The meatiest of meats. Om nom.", "Let's dig in! Ehehe, egg omelet, egg omelet ♪"]
                elif "Ane" in character.traits:
                    lines = ["This kind of food is good for your health, you know? It'll fill you with lots of energy ♪", "You don't get to be picky. Come, say aaa... ♪", "Now, why don't we have an enjoyable meal?"]
                elif "Yandere" in character.traits:
                    lines = ["...Here, have this too. I'm finished.", "Mmm... Vanilla milkshakes are the best ♪", "I've been gaining weight, so I'm holding back today... Haah...", "Just go ahead and order whatever. I'll leave it up to you."]
                else:
                    lines = ["This place's tea and cake is amazing. The tarts are good, too.", "Ah, that looks yummy ♪", "Let's eaaaat! But, what should I eat first? Hmm..."]
                result = random.sample(set(lines).difference(said_lines), 1)[0]
                said_lines.add(result)
                result = result.replace("[mc_ref]", character.mc_ref)
                character.override_portrait("portrait", "indifferent")
                character.say(result)
                character.restore_portrait()

    def interactions_eating_propose(character):
        """
        Outputs a line before eating for provided character
        """
        if "Impersonal" in character.traits:
            lines = ["Let's have some tea.", "Hey, I was thinking about grabbing a bite.", "How about lunch?"]
        elif "Shy" in character.traits and dice(50):
            lines = ["H-hey, how about a cup of tea?", "I was just thinking about eating something...", "It's lunch time... S-so maybe we..."]
        elif "Imouto" in character.traits:
            lines = ["I really want some sweets ♪ C'mon!", "My tummy's growling. Wanna grab a bite?", "Woo! Lunch time, lunch time! Hurry!"]
        elif "Dandere" in character.traits:
            lines = ["Snack time?", "Want to have a snack?", "Lunch..?"]
        elif "Tsundere" in character.traits:
            lines = ["C-come on, invite me for tea or something.", "Hey... Do you want to grab some food? O-Or something?", "Y-you're going to join me for lunch... okay?"]
        elif "Kuudere" in character.traits:
            lines = ["Would you like to have some tea together?", "Let's get something to eat.", "Are you hungry? How about lunch?"]
        elif "Kamidere" in character.traits:
            lines = ["I think it's time for tea.", "Are you hungry? I was thinking about eating.", "Let's eat, I'm hungry."]
        elif "Bokukko" in character.traits:
            lines = ["Hey, let's have a snack, alright?", "Let's eat something! I'm starved!", "It's time to eat! Come on, let's go!"]
        elif "Ane" in character.traits:
            lines = ["Shall we sip some drinks and take it easy?", "What would you say to a cup of tea with me?", "Would you like to join me for lunch?"]
        elif "Yandere" in character.traits:
            lines = ["Do you want to take a tea break?", "Hey, aren't you hungry? Want to go get something to eat?", "If you'd like, we could have lunch?"]
        else:
            lines = ["Hey, you got some snacks or something? I'm kinda hungry.", "Shall we take a break? I'm hungry.", "Aaah, I'm hungry... What about you?"]
        result = random.choice(lines)
        character.override_portrait("portrait", "indifferent")
        character.say(result)
        character.restore_portrait()

    def interactions_pick_background_for_fight(place):
        """
        Returns suitable background for battles in various locations. Can be used together with gm.label_cache as a place.
        """
        if "park" in place:
            n = randint(1,4)
            back = "content/gfx/bg/be/b_park_" + str(n) + ".jpg"
        elif "beach" in place:
            n = randint(1,3)
            back = "content/gfx/bg/be/b_beach_" + str(n) + ".jpg"
        elif "forest" in place or "mage" in place:
            n = randint(1,8)
            back = "content/gfx/bg/be/b_forest_" + str(n) + ".jpg"
        elif "village" in place:
            back = "content/gfx/bg/be/b_village_1.jpg"
        elif "grave" in place:
            back = "content/gfx/bg/be/b_grave_1.jpg"
        elif "academy" in place:
            back = "content/gfx/bg/be/b_academy_1.jpg"
        elif "arena" in place:
            back = "content/gfx/bg/be/battle_arena_1.jpg"
        elif "tavern" in place:
            back = "content/gfx/bg/be/b_tavern_1.jpg"
        else:
            n = randint(1,6)
            back = "content/gfx/bg/be/b_city_" + str(n) + ".jpg" # city streets are default backgrounds; always used for hired chars from the characters menu atm.
        return back
        
    def run_default_be(enemy_team, slaves=False, background="content/gfx/bg/be/battle_arena_1.jpg", track="random", prebattle=True, death=False):
        """
        Launches BE with MC team vs provided enemy team, returns True if MC won and vice versa
        - if slaves == True, slaves in MC team will be inside BE with passive AI, otherwise they won't be there
        - background by default is arena, otherwise could be anything, like interactions_pick_background_for_fight(gm.label_cache) for GMs or interactions_pick_background_for_fight(pytfall.world_events.get("event name").label_cache) for events
        - track by default is random, otherwise it could be a path to some track
        - if prebattle is true, there will be prebattle quotes inside BE from characters before battle starts
        - if death == True, characters in MC team will die if defeated, otherwise they will have 1 hp left
        """
        for member in enemy_team:
            member.controller = BE_AI(member)
        
        your_team = Team(name="Your Team")
        if slaves:
            for member in hero.team:
                your_team.add(member)
            your_team.reset_controller() # to make sure everything's fine with AI
            for member in hero.team:
                if member <> hero and member.status == "slave":
                    member.controller = Slave_BE_AI(member)
        else:
            for member in hero.team:
                if member.status != "slave" or member == hero:
                    your_team.add(member)
            your_team.reset_controller()
            
        battle = BE_Core(Image(background), start_sfx=get_random_image_dissolve(1.5), music=track, end_sfx=dissolve, quotes=prebattle)
        store.battle = battle
        battle.teams.append(your_team)
        battle.teams.append(enemy_team)
        battle.start_battle()
        your_team.reset_controller()
        enemy_team.reset_controller()
        for member in your_team:
            if member in battle.corpses:
                if death:
                    member.health = 0
                else:
                    member.health = 1
                    if member <> hero:
                        member.joy -= randint(5, 15)
                        
        if battle.winner != your_team:
            return False
        else:
            return True