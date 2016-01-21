init python:
    if config.debug:
        register_event("angelica_menu", locations=["mages_tower"], priority=1000, start_day=1, jump=True, dice=100, max_runs=1)
    else:
        register_event("angelica_menu", locations=["mages_tower"], simple_conditions=["global_flags.flag('mt_counter') > 3"], priority=100, start_day=1, jump=True, dice=80, max_runs=1)
    
label angelica_menu:
    
    $ a = Character("Angelica", color=blue, what_color=cornflowerblue, show_two_window=True)
    
    hide screen mages_tower
    show npc angelica
    with dissolve
    
    if not global_flags.flag("met_angelica"):
        $ global_flags.set_flag("met_angelica")
        
        a "Hi! I am Angelica!"
        a "I noticed you've been hanging around the Tower."
        menu:
            a "Are you interested in magic?"
            "Yes!":
                a "Great! You cannot join us in the tower at the moment but there are things I can help you with!"
                a "I for once am one of the very few people in this part of the world who can unlock add and remove elemental alignments from a person."
                a "It is not an easy task so don't think that you will be able to get away with being a cheapskate!"
                a "It takes a lot out of me so I want to be very well compensated. If you believe that you can find a better deal anywhere... I do dare you to try :)"
                $ global_flags.set_flag("angelica_free_alignment")
                a "You look like you have some potencial... so I'll give you one freebie. "
                extend "Do not expect that to happen again!"
                a "I charge 10 000 Gold for the first element if you do not have any alignment at all and 10 000 and 5 000 more for every one that you already have!"
                a "If you want to loose one, it is a lot trickier... elements are not shoes you can put on and off."
                a "That will cost you 50 000 per elements and expect to suffer some damage to your magical powers and health..."
                
                a "I can also teach you basics of Thunder and Ice magic!"
            "Not really...":
                a "Oh? Well, never mind then..."
                a "I'll be around if you change your mind."
                jump mages_tower
                
    $ angelica_thunder_spells = {"Thunder": [3000], "Thundara": [6000], "Thundaga": [10000], "Thundaja": [30000]}
    $ angelica_ice_spells = {"Blizzard": [3000], "Blizzara": [6000], "Blizzarga": [10000], "Blizzarja": [30000]}
    
    $ loop = True
    while loop:
        menu:
            a "How can I be of assistance today?"
            
            "Ask her to teach magic!":
                a "Well!"
                extend " Ice or Thunder! Which will it be?"
                
                if len(hero.team) > 1:
                    if len(hero.team) == 3:
                        a "Will it be you or one of your allies?"
                    else:
                        a "Will it be you or your ally?"
                    call screen character_pick_screen
                    $ char = _return
                else:
                    $ char = hero
                    
                call screen magic_purchase_screen(angelica_thunder_spells, "#7DF9FF", angelica_ice_spells, "#74BBFB")
                $ spell = _return
                
                if spell == "Nothing":
                    a "Anything else?!"
                else:
                    if hero.take_money(spell[1][0], reason="Spells"):
                        a "Magic is knowledge and knowledge is power!"
                        
                        hide npc
                        play sound "content/sfx/sound/events/go_for_it.mp3" fadein 1.0
                        show expression im.Twocolor("content/gfx/images/magic.png", "#74BBFB", "#7DF9FF") as magic:
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
                        
                        show npc angelica
                        with dissolve
                        
                        $ spell = spell[0]
                        $ char.magic_skills.append(spell)
                        
                        a "Use your new skill responsibly!"
                        
                        "[char.nickname] learned [spell]!!!"
                        $ del spell
                        
                    else:
                        a "You do not have enough Gold!"
            
            "Add Alignment!":
                a "Lets take a look!"
                if len(hero.team) > 1:
                    if len(hero.team) == 3:
                        a "Who is it going to be?"
                    call screen character_pick_screen
                    $ char = _return
                else:
                    $ char = hero
                    
                call screen alignment_choice
                
                $ alignment = _return
                        
                if alignment:
                    if alignment in char.traits:
                        a "You already have [alignment] alignment... "
                        extend "did you really think I wasn't going to notice or do you have that much money to burn?"
                    else:
                        if "Neutral" in char.traits:
                            $ price = 10000
                        else:
                            $ price = 10000 + len([e for e in char.traits if e.elemental])*5000
                        if global_flags.flag("angelica_free_alignment") or hero.take_money(price, reason="Element Purchase"):
                            a "There! All done!"
                            a "Don't let these new powers go into your head and use them responsibly!"
                            python:
                                global_flags.del_flag("angelica_free_alignment")
                                char.apply_trait(alignment)
                            $ char.say(choice(["What a weird feeling...", "Awesome!", "This is cool!"]))
                        else:
                            a "You don't have enought money..."
                            a " but come back when you do! I will be around here somewhere!"
                $ del alignment
            
            "Remove Alignments!":
                a "Lets take a look!"
                if len(hero.team) > 1:
                    if len(hero.team) == 3:
                        a "Who is it going to be?"
                    call screen character_pick_screen
                    $ char = _return
                else:
                    $ char = hero
                    
                if not "Neutral" in char.traits:
                    
                    call screen alignment_removal_choice(char)
                    
                    $ alignment = _return
                    
                    if alignment:
                        if alignment == "clear_all":
                            $ price = 50000 * len(list(el for el in char.traits if el.elemental))
                            if hero.take_money(price, reason="Element Purchase"):
                                a "There! All done!"
                                a "All elements removed!"
                                python:
                                    for el in list(el for el in char.traits if el.elemental):
                                        char.remove_trait(el)
                            else:
                                a "You don't have enought money..."
                                a " but come back when you do! I will be around here somewhere!"
                        else:
                            $ price = 50000
                            if hero.take_money(price, reason="Element Purchase"):
                                a "There! All done!"
                                $ char.remove_trait(alignment)
                            else:
                                a "You don't have enought money..."
                                a " but come back when you do! I will be around here somewhere!"
                    
                else:
                    a "I can't remove an element if you don't have any..."
                      
                if hasattr(store, "alignment"):
                    $ del alignment
                
            "Goodbye!":
                $ loop = False
            
    a "See you around!"
    jump mages_tower
    
screen alignment_choice():
    default tt = Tooltip("I changed my mind...!")
    
    textbutton "[tt.value]":
        style "yesno_button"
        align(0.1, 0.05)
        action Return("")
    
    python:
        elements = list(el for el in traits.values() if el.elemental and el != traits["Neutral"])
        step = 360 / len(elements)
        var = 0
        
    for el in elements:
        python:
            img = ProportionalScale(el.icon, 120, 120)
            angle = var
            var = var + step
        imagebutton at circle_around(t=10, angle=angle, radius=250):
            idle img
            hover im.MatrixColor(img, im.matrix.brightness(0.25))
            action Return(el)
            hovered tt.Action(el.id)
            
screen alignment_removal_choice(char):
    default tt = Tooltip("I changed my mind...!")
    
    textbutton "[tt.value]":
        style "yesno_button"
        align(0.1, 0.05)
        action Return("")
    
    python:
        elements = list(el for el in char.traits if el.elemental)
        xpos = 200
        
    hbox:
        xsize 600
        box_wrap True
        align (0.5, 0.2)
        spacing 50
        for el in elements:
            $ img = ProportionalScale(el.icon, 120, 120)
            imagebutton:
                idle img
                hover Transform(im.MatrixColor(img, im.matrix.brightness(0.25)), zoom=1.2)
                action Return(el)
                hovered tt.Action(el.id)
        $ img = ProportionalScale(traits["Neutral"].icon, 120, 120)
        imagebutton:
            idle img
            hover Transform(im.MatrixColor(img, im.matrix.brightness(0.25)), zoom=1.2)
            action Return("clear_all")
            hovered tt.Action("Clear all elements!")
