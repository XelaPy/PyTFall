label arena_outside:
    $ gm.enter_location(goodtraits=["Manly", "Courageous", "Aggressive"], badtraits=["Coward", "Nerd", "Homebody"], goodoccupations=["Warrior"], curious_priority=False)
    
    # Music related:
    if not "arena_outside" in ilists.world_music:
        $ ilists.world_music["arena_outside"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("arena_outside")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["arena_outside"])
    $ global_flags.del_flag("keep_playing_music")
    
    scene bg arena_outside
    with dissolve
    
    # Texts: ---------------------------------------------------------->
    if not global_flags.flag("visited_arena"):
        $ global_flags.set_flag("visited_arena")
        define ax = Character('Xeona', color=ivory, show_two_window=True)
        'You see a pretty, and confident girl approaching you.'
        show npc xeona
        with dissolve
        
        if "Warrior" in hero.occupations:
            ax "Long time not seen, [hero.nickname]!"
            ax "Where you've been hiding?"
            ax "In any case, can I help you with something?"
        else:
            ax "Hgehe :-)"
            ax "I've never seen you before. What brings you here?"
            ax "Lust for blood? or Fame? Power? Respect?"
            ax "Oh well, is there anything you'd like to know about this place?"
    
        $ a_skip = False
        $ heard_about_arena = False
        $ arena_date = False
        while not a_skip:
            menu:
                ax "Well?"
                "Tell me about Arena." if not heard_about_arena:
                    if "Warrior" in hero.occupations:
                        ax "Did you hit your head and forget???"
                    ax "The arena, other than our sex industry, is the biggest source of entertainment for locals and tourists alike."
                    ax "Many warriors come here to test their mettle against all challengers. Mages come to test their wisdom and training against all kinds of foe. Though most come"
                    extend " just to unwind and see some kickass battles."
                    ax "The arena is devided in two sections, one for the {color=[green]}matches{/color} and one for {color=[green]}Dogfights{/color}."
                    ax "Both pay well, especially if you please the crowd."
                    ax "There is also a survival challenge where you can fight against beasts and monsters from all around."
                    ax "Deaths are rare, due to regulations about pulling gladiators out before the monsters eat them."
                    ax "Most of our gladiators with {color=[green]}arena permits{/color} make a very decent living. However those who are not at that level"
                    extend " usually have some extra source of income, like guard duties or treasure hunting."
                    ax "Well, that about enough for you to form a general picture?"
                    ax "Are you going in?"
                    $ heard_about_arena = True
                    
                "What's an 'arena permit'?" if heard_about_arena:
                    ax "An arena permit is something you get to pay a lot of Gold for when you've managed to gain enough reputation."
                    ax "Then you can fight in official matches and take your place in the ladders."
                    ax "Seems simple enough doesn't it?"
                    
                "And how do I gain arena reputation?" if heard_about_arena:
                    ax "By fighting and winning obviously."
                    ax "Decent rep and some gold just might get you a permit so you could fight in the Arena matches one day."
                    ax "Good teammates are also easier to find if your rep is higher than theirs."
                    
                "Dogfights? Please explain..." if heard_about_arena:
                    ax "It's just the nickname that the arena crowd gave to unofficial matches."
                    ax "To take part in one does not require a permit, just yourself or a capable team."
                    ax "Spectators do enjoy watching a decent Dogfight as well, and you'll get paid so long as you deliver."
                    
                "I've heard rumors about 'Arena King'" if heard_about_arena:
                    if pytfall.arena.king != hero:
                        ax "[pytfall.arena.king.name] you mean?"
                        ax "Well, 'Stay the hell away!', is the best advice I can give you."
                        ax "We mere mortals should not concern ourselves with such things."
                    else:
                        ax "You'll never stop boasting? Will ya?"
                    
                "Official matches and ladders?" if heard_about_arena:
                    ax "Oh, those are the real thing! If you win, you get to be on the official ladders of fame and glory!"
                    ax "All gladiators who seek recognition try to get on them. few succeed."
                    ax "It's a great honor to be listed in any of the ladders. If you have the skills and tools required you should definetly give it a go."
                    ax "These types of matches are scheduled in advance. The loser goes down one position and the winner gains a position."
                    ax "As you've probably figured out, you can loose your place in the ladder without acually losing a fight."
                    ax "But that's the incentive to keep fighting everyone I suppose :)"
                    
                "How does team combat work?" if heard_about_arena:
                    ax "The team 'Leader' is what's really important."
                    ax "Each team has a leader. The leader decides who fights by their side. "
                    ax "There are {color=[red]}2vs2 and 3vs3{/color} fights."
                    ax "Obviously there is dueling as well. Good one on one fights are also adored by the spectators!"
                    
                "Wanna go on a date with me?" if not arena_date:
                    $ arena_date = True
                    ax "Well, PyTFall's arena is a place of great... Wait... What?"
                    ax "Go find some floosy in the park! Why me all of a sudden?"
                    ax "Oh wait, you were kidding. Right?"
                
                "I know all I need to...":
                    ax "If you ever fall on hard times we always have some work that needs to be done."
                    ax "See you around!"
                    hide npc xeona
                    with dissolve
                    $ a_skip = True
                    
        # Keeping global namespace tidy:            
        $ del a_skip
        $ del heard_about_arena
        $ del arena_date
            
    
    
    python:
        # Build the actions
        if pytfall.world_actions.location("arena_outside"):
            pytfall.world_actions.work(Iff(global_flag_complex("visited_arena")))
            pytfall.world_actions.add("xeona", "Find Xeona", Jump("find_xeona"))
            pytfall.world_actions.add("arena", "Enter Arena", Return(["control", "enter_arena"]))
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    show screen arena_outside
    
    # Auto-events
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    $ loop = True    
    while loop:
        
        $ result = ui.interact()
        
        if result[0] == 'jump':
            $ global_flags.set_flag("keep_playing_music")
            $ gm.start_gm(result[1])
            
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
    hide screen arena_outside
    jump city
    
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
            $ renpy.say("", choice(["You cleaned blood off the floors in the training area.", "Pay is crap, but it's still money.", "You helped out by carrying some weapons around!"]))
        else:
            $ hero.say(choice(["What a shitty job.", "There's has to be better way to make money."]))
    $ global_flags.set_flag("keep_playing_music")
    
    return
    
label find_xeona:
    define ax = Character('Xeona', color=ivory, show_two_window=True)
    show npc xeona
    with dissolve
    
    ax "Hi again! Is there something you want?"
    # $ devlog.info("renpy.is_seen returned: %s (%s)" % (renpy.is_seen(), renpy.game.context().current))
    $ a_skip = True
    while a_skip:
        menu:
            ax "Anytime now..."
            "Xeona Main":
                $ pass
            "How about that Arena Permit?" if not hero.arena_permit:
                if hero.arena_rep > 15000:
                    ax "Looks like you've managed to gain enough reputation!"
                    ax "Congratulations!"
                    menu:
                        ax "Would you like to buy an arena permit? It's priced at {color=[gold]}10 000 Gold{/color}."
                        "Yes":
                            if hero.take_money(10000, reason="Arena Permit"):
                                $ hero.arena_permit = True
                                ax "There you go! You can now participate in official Arena Matches!"
                            else:
                                ax "Do you really have {color=[gold]}10 000 Gold{/color} on you?"
                                ax "Didn't think so..."
                        "No":
                            $ pass
                elif hero.arena_rep > 7500:
                    ax "You've managed to improve your reputation, but you're not there yet :)"
                else:
                    ax "With the amount of reputation you have? No chance in hell!!!"
                    
            "How about some training?":
                if len(hero.team) > 1:
                    ax "Sure thing! Who will it be?"
                    call screen character_pick_screen
                    $ char = _return
                else:
                    $ char = hero
                    
                if not global_flags.has_flag("xeona_training_explained"):    
                    ax "As you may have known, I train battle skills."
                    ax "It will cost you 1000 (+1000 per 5 levels) Gold per training session."
                    ax "Don't expect to learn any magic though."
                    extend " But I can teach you how to fight on level with any silly mage!"
                    ax "Due to my the nature of training, there is always a chance of your consitution increasing as well."
                    ax "Potions we drink to increase stamina during the training might also increase your HP!"
                    $ global_flags.set_flag("xeona_training_explained")
                else:
                    ax "I am ready if you are!"
                    
                $ training_price = char.get_training_price()    
                menu:
                    "Pay [training_price] Gold" if hero.AP > 0:
                        if hero.take_money(training_price, "Training"):
                            $ char.AP -= 1
                            $ char.auto_training("train_with_xeona")
                            ax "All done! Be sure to think of me whenever you kick @ss! :)"
                        else:
                            ax "No cash Huh?"
                            extend " You could always go and beat the crap out of some loosers in the Arena!"
                            ax "Who knows, you might even learn something while at it :)"
                        
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
                    "Pick a character."
                    call screen character_pick_screen
                    $ char = _return
                else:
                    $ char = hero
                    
                menu:
                    "Setup sessions" if not char.has_flag("train_with_xeona"):
                        $ char.set_flag("train_with_xeona")
                    "Cancel sessions" if char.flag("train_with_xeona"):
                        $ char.del_flag("train_with_xeona")
                    "Do Nothing...":
                        $ pass
                            
            "Talk about weather...":
                ax "Err... this is getting really awkward..."
                ax "Is there anything else???"
                            
            "That's all for now.":
                ax "Goodbye :)"
                $ a_skip = False
                
    hide npc xeona
    with dissolve
    $ del a_skip
    
    $ jump("arena_outside")
 
screen arena_outside:
    
    use top_stripe(True)
    
    use location_actions("arena_outside")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5,0.3)
            spacing 70
                        
            for entry in gm.display_girls():
                 
                    use rg_lightbutton(img=entry.show("girlmeets", "armor", exclude=["swimsuit", "beach", "pool", "onsen", "bunny"], label_cache=True, resize=(300, 400), type="reduce"), return_value=['jump', entry])
