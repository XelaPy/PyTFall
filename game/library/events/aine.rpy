init python:
    register_event("aine_menu", locations=["city_park"], simple_conditions=["global_flags.flag('met_peevish')", "hero.magic > 40"], priority=100, start_day=1, jump=True, dice=100, max_runs=1)

label aine_menu:
    
    $ a = Character("Aine", color=green, what_color=azure, show_two_window=True)
    
    hide screen city_park
    show npc aine:
        pos (0.4, 0.2)
        linear 1.0 pos (0.4, 0.3)
        linear 1.0 pos (0.4, 0.2)
        repeat
    with dissolve
    
    if not global_flags.flag("met_aine"):
        $ global_flags.set_flag("met_aine")
        
        a "Well now, a magic practitioner... "
        extend " Hello dear, I am Aine!"
        
        menu:
            "A leprechaun? In the park?":
                a "How Rude! I go wherever I please and I can take of myself!"
                a "Not mentioning that this is a really nice place and very few people can see me!"
            "I've met one of your kind already, someone called Peevish.":
                a "That rude, good for nothing, useless excuse for a brother... well, you don't get to choose family..."
                
        a "I can teach light or dark magic if you're interested,"
        extend " it will cost you but you'll never have to hear a word about no pile of gold from me."
    else:
        a "Hello again. How are you today?"
    
    
    $ aine_light_spells = {"Holy": [3000], "Holyra": [6000], "Holyda": [10000], "Holyja": [30000]}
    $ aine_darkness_spells = {"Dark": [3000], "Darkra": [6000], "Darkga": [10000], "Darkja": [30000]}
    
    $ loop = True
    while loop:
        menu:
            a "Anything interesting my dear?"
            "Ask her to teach magic!":
                a "Of course!"
                a "Just pick a spell!"
                
                if len(hero.team) > 1:
                    if len(hero.team) == 3:
                        a "Will it be you or one of your lovely friends?"
                    else:
                        a "Will it be you or your lovely friend?"
                    call screen character_pick_screen
                    $ char = _return
                else:
                    $ char = hero
                    
                call screen magic_purchase_screen(aine_light_spells, azure, aine_darkness_spells, black)
                $ spell = _return
                
                if spell == "Nothing":
                    a "No biggie..."
                    a "Is there anything else?!"
                else:
                    if hero.take_money(spell[1][0], reason="Spells"):
                        a "Just take a long breath and let the magic flow through you!"
                        
                        hide npc
                        play sound "content/sfx/sound/events/go_for_it.mp3" fadein 1.0
                        show expression im.Twocolor("content/gfx/images/magic.png", green, green) as magic:
                            yalign .5 subpixel True
                    
                            parallel:
                                xalign .5
                                linear 3.0 xalign .75
                                linear 6.0 xalign .25
                                linear 3.0 xalign .5
                                repeat
                    
                            parallel:
                                alpha 1.0 zoom 1.0
                                linear .75 alpha .5 zoom .8
                                linear .75 alpha 1.0 zoom 1.0
                                repeat
                    
                            parallel:
                                rotate 0
                                linear 5 rotate 360
                                repeat
                    
                        with dissolve
                        $ renpy.pause(3.0, hard=True)
                        hide magic
                        
                        show npc aine:
                            pos (0.4, 0.2)
                            linear 1.0 pos (0.4, 0.3)
                            linear 1.0 pos (0.4, 0.2)
                            repeat
                            
                        with dissolve
                        
                        $ spell = spell[0]
                        $ char.magic_skills.append(spell)
                        
                        a "Use your new powers wisely!"
                        
                        "[char.nickname] learned [spell]!!!"
                        $ del spell
                        
                    else:
                        a "I know that I'm nice but don't even thing if taking advantage!"
                        extend " Come back with more gold!"
                        
            "Ask her to train you!":
                if len(hero.team) > 1:
                    a "Who will it be?"
                    call screen character_pick_screen
                    $ char = _return
                else:
                    $ char = hero
                    
                if not global_flags.has_flag("aine_training_explained"):    
                    a "Well dear, I can teach you manners and proper care so to increase your charisma."
                    a "It will cost you 1000 (+1000 per 5 levels) Gold per training session."
                    a "Being thought by a leprechaun Princess has it's perks!"
                    a "You vitality will be boosted and your fame and reputation may also increase."
                    extend " Due to my magical nature, there is a really small chance that you will get luckier in your life endeavours!!!"
                    a "That I dare say is a truly rare feat!"
                    $ global_flags.set_flag("aine_training_explained")
                else:
                    a "I am ready if you are!"
                    
                $ training_price = char.get_training_price()    
                menu:
                    "Pay [training_price] Gold" if hero.AP > 0:
                        if hero.take_money(training_price, "Training"):
                            $ char.AP -= 1
                            $ char.auto_training("train_with_aine")
                            a "All done! Don't you dare misuse skills you've learned here!"
                        else:
                            a "Payment is still required I am afraid."
                            extend " It is only fair!"
                            
                        
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
                    $ char = _return
                else:
                    $ char = hero
                    
                menu:
                    "Setup sessions" if not char.has_flag("train_with_aine"):
                        $ char.set_flag("train_with_aine")
                    "Cancel sessions" if char.flag("train_with_aine"):
                        $ char.del_flag("train_with_aine")
                    "Do Nothing...":
                        $ pass
                    
            "Thanks for your time.":
                $ loop = False
            
    a "Good luck!"    
    jump city_park
