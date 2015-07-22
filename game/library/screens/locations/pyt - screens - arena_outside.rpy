label arena_outside:
    $ pytfall.gm.enter_location(occupation="Warrior")
    
    # Music related:
    if not "arena_outside" in ilists.world_music:
        $ ilists.world_music["arena_outside"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("arena_outside")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["arena_outside"])
    $ global_flags.del_flag("keep_playing_music")
    
    scene bg arena_outside
    with dissolve
    
    # Texts: ---------------------------------------------------------->
    if not global_flags.has_flag("wants_to_see_xeona"):    
        $ global_flags.set_flag("wants_to_see_xeona", value=False)
        
    if not global_flags.flag("visited_arena"):
        $ global_flags.set_flag("visited_arena")
        define ax = Character('Xeona', color=ivory, show_two_window=True)
        'You see a pretty and confident girl approaching you.'
        show npc xeona
        with dissolve
        
        if "Warrior" in hero.occupations:
            ax "Long time not seen, [hero.nickname]!"
            ax "Where you've been hiding?"
            ax "In any case, can I help you with something?"
        else:
            ax "Hgehe :-)"
            ax "I've never seen you before... What brings you here?"
            ax "Lust for blood? or Fame? Power? Respect?"
            ax "Oh well... is there anything you'd like to know about this place?"
    
        $ a_skip = False
        $ heard_about_arena = False
        $ arena_date = False
        while not a_skip:
            menu:
                ax "Well...?"
                "Tell me about Arena." if not heard_about_arena:
                    if "Warrior" in hero.occupations:
                        ax "Did you hit your head and forget???"
                    ax "Arena... other than our sex industry, it is the second biggest source of entertainment for locals and tourists alike!"
                    ax "Many warriors come here to test their metal, mages to test their wisdom and simple folk"
                    extend " just to unwind and see some kickass battles."
                    ax "Arena is devided in two sections, one for the {color=[green]}matches{/color} and the other for {color=[green]}dogfights{/color}."
                    ax "Both pay really well, especially if you do well."
                    ax "There is also a survival challenge where you can try your luck agaist creatures of all sorts."
                    ax "Deaths are rare, specrators might not like that but that's the rule."
                    ax "Most of our gladiators with {color=[green]}arena permits{/color} that fight in matches make a very decent living, however those who are not at that level,"
                    extend " usually have some extra source of income, like guard duties or treasure hunting."
                    ax "Well, that about enough for you to form a general picture."
                    ax "Are you going in?"
                    $ heard_about_arena = True
                    
                "What's an 'arena permit'?" if heard_about_arena:
                    ax "Arena permit is something you get to pay a lot of Gold for when you managed to gain enough reputation."
                    ax "Than you'll be allowed to fight in official matches and take your place in the ladders."
                    ax "Seems simple enought... Doesn't it?"
                    
                "And how do I gain arena reputation?" if heard_about_arena:
                    ax "By fighting and obviously by winning those fights."
                    ax "Decent rep and some gold just might get you a permit so you could fight in the Arena matches one day."
                    ax "Good teammates are also easier to find if you rep is higher than theirs."
                    
                "Dogfights? Please explain..." if heard_about_arena:
                    ax "It's just a nickname that Arena crowd gave to the unofficial matches."
                    ax "To take part in one, you do not require a permit, just yourself or a capable team."
                    ax "Spectrators do enjoy watching a decent dogfight as well, so you'll get paid for as long as you deliver."
                    
                "I've heard rumors about 'Arena King'" if heard_about_arena:
                    if pytfall.arena.king != hero:
                        ax "[pytfall.arena.king.name] you mean?"
                        ax "Well, stay the hell away is the best advice I can give you..."
                        ax "Us, mere mortals should not concirn ourselfs with such matters."
                    else:
                        ax "You'll never stop boasting? Will ya?"
                    
                "Official matches and ladders?" if heard_about_arena:
                    ax "Oh... those are the REAL thing. If you win, you get to be on official ladders of fame and glory!"
                    ax "All warriors who seek recognition try to get on them... few succeed..."
                    ax "It's a great honor to be listed in any of the ladders so if you have the skillz and toolz required, you should definetly give it a go."
                    ax "These types of matches are scheduled in advance. Whoever looses goes down one position and whoever wins gains a position."
                    ax "As you have probably figured out, you can loose your place in the ladder without even being any the wiser."
                    ax "But that's the incentive to keep beating the crap out of everyone I suppose :)"
                    
                "How does team combat work?" if heard_about_arena:
                    ax "Team 'leader' is what's really important, not it's members."
                    ax "Each team has a leader, that leader decided who fights by his or her side. "
                    ax "There are {color=[red]}2vs2 and 3vs3{/color} team fights."
                    ax "Obviously there is dualing as well, good one on one fights are also adored by spectrators!"
                    
                "Wanna go on a date with me?" if not arena_date:
                    $ arena_date = True
                    ax "Well, PyTFall's Arena is a place of great... Wait... What?"
                    ax "Go find some floosy in the park! Why me all of a sudden?"
                    ax "Oh wait, you were kidding. Right?"
                
                "I know all I need to...":
                    ax "If you ever fall on hard times, we always have some work that needs to be done around here."
                    ax "See you around!"
                    hide npc xeona
                    with dissolve
                    $ a_skip = True
                    
        # Keeping global namespace tidy:            
        $ del a_skip
        $ del heard_about_arena
        $ del arena_date
            
    if global_flags.flag("wants_to_see_xeona"):
        $ global_flags.set_flag("wants_to_see_xeona", value=False)
        define ax = Character('Xeona', color=ivory, show_two_window=True)
        show npc xeona
        with dissolve
        
        ax "Hi again! Is there something you want?"
        # $ devlog.info("renpy.is_seen returned: %s (%s)" % (renpy.is_seen(), renpy.game.context().current))
        $ a_skip = True
        while a_skip:
            menu:
                ax "Anytime now..."
                "How about that Arena Permit?" if not hero.arena_permit:
                    if hero.arena_rep > 15000:
                        ax "Looks like you've managed to gain enough reputation!"
                        ax "Congratulations are in order!"
                        menu:
                            ax "Would you like to buy an Arena permit?"
                            "Yes":
                                if hero.take_money(10000, reason="Arena Permit"):
                                    $ hero.arena_permit = True
                                    ax "There you go! You can now participate in official Arena Matches!"
                                else:
                                    ax "It's priced at {color=[gold]}10 000 Gold{/color}. Do you really have that much on you?"
                                    ax "Didn't think so..."
                            "No":
                                $ pass
                    elif hero.arena_rep > 7500:
                        ax "You've managed to improve your reputation, but you are not quite there yet :)"
                    else:
                        ax "With the amount of reputation you have, No chance in hell!!!"
                        
                "How about some training?":
                    if len(hero.team) > 1:
                        ax "Sure thing! Who will it be?"
                        call screen character_pick_screen
                        $ chr = _return
                    else:
                        $ chr = hero
                        
                    if not global_flags.has_flag("xeona_training_explained"):    
                        ax "As you may have already guessed, I train battle skills."
                        ax "It will cost you 1000 (+1000 per 5 levels) Gold per training session."
                        ax "Don't expect to learn any magic, I am not into Arcane Arts..."
                        extend " but I can teach you how to fight on level with any silly magician!"
                        ax "Due to my the nature of training, there is always a chance of your consitution increasing as well."
                        ax "Potions we drink to increase stamina during the training might also increase your HP!"
                        $ global_flags.set_flag("xeona_training_explained")
                    else:
                        ax "I am ready if you are!"
                        
                    $ training_price = chr.get_training_price()    
                    menu:
                        "Pay [training_price] Gold" if hero.AP > 0:
                            if hero.take_money(training_price, "Training"):
                                $ hero.AP -= 1
                                $ hero.auto_training("train_with_xeona")
                                ax "All done! Be sure to think of me whenever you kick @ss! :)"
                            else:
                                ax "No cash Hah?"
                                extend " You could always go and beat the crap out of some looser in the Arena!"
                                ax "Who knows, you may even learn something while at it :)"
                            
                        "Maybe next time...":
                            $ pass
                    $ del training_price
                
                "Schedule training sessions":
                    if not global_flags.has_flag("training_sessions_explained"):
                        "Here you can arrange for daily training sessions at cost of 1AP and 1000 (+1000 per 5 levels) Gold per day."
                        "This will be automatically terminated if you lack the gold to continue."
                        "Sessions can be arranged with multiple trainers at the same day"
                        extend " however you'd be running a risk of not leaving AP to do anything else!"
                        $ global_flags.set_flag("training_sessions_explained")
                    
                    if len(hero.team) > 1:
                        "Pick a character!"
                        call screen character_pick_screen
                        $ chr = _return
                    else:
                        $ chr = hero
                        
                    menu:
                        "Setup sessions" if not chr.has_flag("train_with_xeona"):
                            $ chr.set_flag("train_with_xeona")
                        "Cancel sessions" if chr.flag("train_with_xeona"):
                            $ chr.del_flag("train_with_xeona")
                        "Do Nothing...":
                            $ pass
                                
                "Talk about weather...":
                    ax "Err.. this is getting really awkward..."
                    ax "Is there anything else???"
                                
                "That's all for now.":
                    ax "Goodbye :)"
                    $ a_skip = False
                    
        hide npc xeona
        with dissolve
        $ del a_skip
    
    python:
        # Build the actions
        if pytfall.world_actions.location("arena_outside"):
            pytfall.world_actions.work(Iff(global_flag_complex("visited_arena")))
            pytfall.world_actions.add("xeona", "Find Xeona", [SetField(global_flags, "wants_to_see_xeona", True), Jump("arena_outside")])
            pytfall.world_actions.add("arena", "Enter Arena", Return(["control", "enter_arena"]))
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    show screen pyt_arena_outside
    
    # Auto-events
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    $ loop = True    
    while loop:
        
        $ result = ui.interact()
        
        if result[0] == 'jump':
            $ global_flags.set_flag("keep_playing_music")
            $ pytfall.gm.start_gm(result[1])
            
        if result[0] == 'control':     
            if result[1] == "enter_arena":
                $ renpy.music.stop(channel="gamemusic")
                $ hs()
                $ jump("arena_inside")
                
            elif result[1] == "work":
                call work_in_arena from _call_work_in_arena
                
            if result[1] == 'return':
                $ loop = False
                
        $ renpy.hide("_tag")
                    
    $ renpy.music.stop(channel="gamemusic")                
    hide screen pyt_arena_outside
    jump pyt_city
    
label work_in_arena:
    $ wage = randint(5, 12) + hero.attack/7 + hero.defence/7 + hero.agility/7 + hero.magic/7 + hero.level * 5
    $ if dice(hero.luck*0.1): wage += hero.level * 5
    if dice(0.5 + hero.luck*0.1):
        $ hero.agility += 1
        $ hero.defence += 1
        $ hero.attack += 1
        $ hero.constitution += 1
    $ hero.exp += hero.adjust_exp(randint(1, 3))    
    $ hero.add_money(wage, "Job")
    
    $ renpy.show("_tag", what=Text("%d" % wage, style="back_serpent", color=gold, size=40, bold=True), at_list=[found_cash(150, 600, 2)])
    
    if hero.take_ap(1):
        if dice(50):
            $ renpy.say("", choice(["You cleaned blood off the floors in the training area!", "Pay might be crap, but it's still money.", "You've helped out carrying some weapons around!"]))
        else:
            $ hero.say(choice(["What a shitty job...", "There's gotta be better way to make money..."]))
    $ global_flags.set_flag("keep_playing_music")
    
    return
    
 
screen pyt_arena_outside:
    
    use pyt_top_stripe(True)
    
    use location_actions("arena_outside")
    
    if pytfall.gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5,0.3)
            spacing 70
                        
            for entry in pytfall.gm.display_girls():
            # """
                    # if not entry.flag("arena_outside_tags") or entry.flag("arena_outside_tags")[0] < day:
                        # $arena_outside_tags_list = []
                        # # primary tags
                        # if entry.has_image("battle","generic outdoor"):
                            # $arena_outside_tags_list.append(("battle","generic outdoor"))
                        # if entry.has_image("battle","simple bg"):
                            # $arena_outside_tags_list.append(("battle","simple bg"))
                        # if entry.has_image("battle","arena"):
                            # $arena_outside_tags_list.append(("battle","arena"))    
                        # if entry.has_image("girl_meets","arena"):
                            # $arena_outside_tags_list.append(("girl_meets","arena"))
                        # if entry.has_image("girl_meets","armor","generic outdoor"):
                            # $arena_outside_tags_list.append(("girl_meets","armor","generic outdoor"))
                        # if entry.has_image("girl_meets","armor","simple bg"):
                            # $arena_outside_tags_list.append(("girl_meets","armor","simple bg"))
                        # if entry.has_image("girl_meets","nurse","generic outdoor"):
                            # $arena_outside_tags_list.append(("girl_meets","nurse","generic outdoor"))
                        # if entry.has_image("girl_meets","nurse","simple bg"):
                            # $arena_outside_tags_list.append(("girl_meets","nurse","simple bg"))
                        # if entry.has_image("girl_meets","weapon","generic outdoor"):
                            # $arena_outside_tags_list.append(("girl_meets","weapon","generic outdoor"))
                        # if entry.has_image("girl_meets","weapon","simple bg"):
                            # $arena_outside_tags_list.append(("girl_meets","weapon","simple bg"))    
                        # # secondary tags if no primary tags    
                        # if not arena_outside_tags_list:
                            # if entry.has_image("girl_meets","generic outdoor"):
                                # $arena_outside_tags_list.append(("girl_meets","generic outdoor"))
                            # if entry.has_image("girl_meets","simple bg"):
                                # $arena_outside_tags_list.append(("girl_meets","simple bg"))    
                        # # giveup    
                        # if not arena_outside_tags_list:
                            # $arena_outside_tags_list.append(("girl_meets"))   
                        
                        # $ entry.set_flag("arena_outside_tags", (day, choice(arena_outside_tags_list)))
                    
                    # use r_lightbutton(img=entry.show(*entry.flag("arena_outside_tags")[1], exclude=["bikini", "swimsuit"], label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 
            # """                   
                    use rg_lightbutton(img=entry.show("weapon", "arena", "armor", "battle", exclude=main_sex_tags + water_selection + ["strip", "nude", "cooking", "waitress", "musician", "singer", "studying", "hurt", "bar", "bathroom", "bedroom", "classroom", "kitchen", "living room", "library", "shop", "park", "fighting" , "magic"], label_cache=True, resize=(300, 400), type="any"), return_value=['jump', entry])
