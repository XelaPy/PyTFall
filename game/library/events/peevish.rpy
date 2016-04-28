init python:
    register_event("peevish_meeting", locations=["forest_entrance"], simple_conditions=["hero.magic > 30"],  priority=500, start_day=1, jump=True, dice=100, max_runs=1)
    

label peevish_meeting:
    
    $ p = Character("???", color=lawngreen, what_color=lawngreen, show_two_window=True)
    
    stop world
    
    hide screen forest_entrance
    with dissolve
    
    show bg forest_entrance:
        size (config.screen_width, config.screen_height)
        crop (0, 0, config.screen_width, config.screen_height)
        easein 4.0 crop (100, 100, config.screen_width/8, 100)
        
    play sound "content/sfx/sound/events/get.mp3" fadein 1.0
        
    $ renpy.pause(5.0, hard=True)
    
    show npc peevish
    with dissolve
    
    play world "irish.mp3" fadein 2.0
    # with vpunch
    p "Hello Dumbass!"
    p "WOW. You can actually see me? There aren't many who can!"
    extend " Like that old crone living up that damn hobbit hole..."
    
    p "I am the great and powerful Peevish McSpud!"
    
    $ p = Character("Peevish", color=lawngreen, what_color=lawngreen, show_two_window=True)
    
    menu:
        "Old crone? That witch looks young and kinda hot?":
            p "Haha! Shows how much you know!"
            p "Let me get down from here."
        "Hey! Are you the midget who lives up in a tree?":
            p "Amn't!"
            p "I am a genuine leprechaun, you b!tch!!!"
            extend " Well... almost... I wish that I had that damn pile of gold under the rainbow..."
            p "But the rest of me is 100%% you mother-frecker! Just wait till I come down there!" #not swearing on purpose?
            
    hide npc peevish
    hide bg forest_entrance
    show bg forest_entrance
    with dissolve
    
    show npc peevish:
        pos (0.4, 0.2)
        linear 1.0 pos (0.4, 0.3)
        linear 1.0 pos (0.4, 0.2)
        repeat
    with dissolve
    
    p "Haha, you're a lot uglier from this angle!"
    p "But you're in luck today! Since you can see me, you aren't entirely hopeless..."
    extend " and I just happen to teach {color=[brown]}Earth{/color} and {color=[blue]}Water{/color} magic!"
    p "Normally I wouldn't bother with a shitty pipsqueak like you, but my greatness requires a good pile of {color=[gold]}gold{/color} to become a real genuine and authentic leprechaun."
    p "I could use a rainbow too..."
    p "Well, come find me if you're interested!"
    
    menu:
        "Earth and Water magic? You? Don't make me laugh!":
            p "Hah? A sceptic, I see?"
            hide npc
            with dissolve
            
            show expression Image("content/events/peevish/tsunami.png") as tsunami:
                pos (0.45, 0.5)
                linear 1.0 zoom 5.0
            play sound "content/sfx/sound/be/water4.mp3"
            $ renpy.pause(1.0, hard=True)
            hide tsunami
            
            show bg humans
            show expression (hero.show("battle_sprite", resize=(100, 100))) as _hero:
                parallel:
                    xalign 0.0 yalign 0.5
                    linear 2.0 xalign 1.0
                parallel:
                    rotate 0
                    linear 0.3 rotate 360
                    repeat
            $ renpy.pause(1.4, hard=True)        
            hide bg humans
            hide _hero
            with dissolve
            
            scene black
            show bg forest_entrance:
                alpha 1.0
                linear 10 alpha 0.0
                
            show npc peevish
            with dissolve
            
            p "Damn it to hell! There goes another potential customer :("
            p "Oh well... maybe I didn't hit him that hard..."
            
            $ global_flags.set_flag("met_peevish")
            jump city
            
        "I'll keep that in mind!":
            p "Well, don't expect it to be cheap!"
            extend " Talk to me when you have some G's on you!"
        
    $ global_flags.set_flag("met_peevish")
    jump forest_entrance


label peevish_menu:
    
    $ p = Character("Peevish", color=lawngreen, what_color=lawngreen, show_two_window=True)
    
    hide screen forest_entrance
    show npc peevish:
        pos (0.4, 0.2)
        linear 1.0 pos (0.4, 0.3)
        linear 1.0 pos (0.4, 0.2)
        repeat
    with dissolve
    
    p "Haha, look who's back!"
    p "Got some gold on ya?"
    
    $ peevish_water_spells = {"Water": [3000], "Watera": [6000], "Waterga": [10000], "Waterja": [30000]}
    $ peevish_earth_spells = {"Stone": [3000], "Stonera": [6000], "Stonega": [10000], "Stoneja": [30000]}
    
    $ loop = True
    while loop:
        menu:
            p "Well? What do you want?"
            "Ask him to teach magic!":
                p "Yeah, baby!"
                p "Won't be long till I have that pile of gold!"
                
                if len(hero.team) > 1:
                    p "Who gets to be awesome today?"
                    call screen character_pick_screen
                    $ char = _return
                else:
                    $ char = hero
                    
                call screen magic_purchase_screen(peevish_water_spells, cornflowerblue, peevish_earth_spells, brown)
                $ spell = _return
                
                if spell == "Nothing":
                    p "Damned shitty brat just wasting my time..."
                    p "Just pick something!"
                else:
                    if hero.take_money(spell[1][0], reason="Spells"):
                        p "Hehe! Awesome, it's a deal then!"
                        extend " Stand back for a bit!!!"
                        
                        hide npc
                        play sound "content/sfx/sound/events/get.mp3" fadein 1.0
                        show expression Image("content/gfx/images/magic.png") as magic:
                            yalign .5 subpixel True
                    
                            parallel:
                                xalign .5
                                linear 3.0 xalign .75
                                linear 6.0 xalign .25
                                linear 3.0 xalign .5
                                repeat
                    
                            parallel:
                                alpha 1.0 zoom 1.0
                                linear .75 alpha .5 zoom .9
                                linear .75 alpha 1.0 zoom 1.0
                                repeat
                    
                            parallel:
                                rotate 0
                                linear 5 rotate 360
                                repeat
                    
                        with dissolve
                        $ renpy.pause(3.0, hard=True)
                        hide magic
                        show npc peevish:
                            pos (0.4, 0.2)
                            linear 1.0 pos (0.4, 0.3)
                            linear 1.0 pos (0.4, 0.2)
                            repeat
                        with dissolve
                        
                        $ spell = spell[0]
                        $ char.magic_skills.append(spell)
                        
                        p "Congratulations! You're a little bit less useless than you were a minute ago."
                        
                        "[char.nickname] learned [spell]!!!"
                        $ del spell
                        
                    else:
                        p "The hell is this? Are you trying to rip me off mother-frecker?"
                        extend "You don't have that much gold on you! I can smell it!"
                    
            "That will be all.":
                $ loop = False
            
    p "Come back when you have more Gold!"
    if not global_flags.has_flag("revealed_aine_location"):
        p "Oh! Before I forget!"
        p "I have a goodie, goodie sis that usually hangs around the park area. She is magical too so you might not be able to see her until you train up a bit..."
        p "Sure wish you weren't such a wuss..."
        extend " Now you can get the hell out of here!"
        $ global_flags.set_flag("revealed_aine_location")
    jump forest_entrance


screen magic_purchase_screen(left_magic, left_magic_color, right_magic, right_magic_color):
    
    frame:
        style_group "dropdown_gm"
        ypos 300
        xpos 100
        has vbox
        for key, v in sorted(left_magic.iteritems(), key=itemgetter(1)):
            $ skill = battle_skills[key]
            if skill not in char.magic_skills:
                $ price = left_magic[key][0]
                button:
                    maximum (350, 30)
                    action Return((skill, left_magic[key]))
                    text "[key]:":
                        xalign 0
                        color left_magic_color
                        drop_shadow [(1, 1)]
                        drop_shadow_color black
                    text "[price]":
                        xalign 1.0
                        color left_magic_color
                        drop_shadow [(1, 1)]
                        drop_shadow_color black
        
    frame:
        style_group "dropdown_gm"
        ypos 300
        xpos (config.screen_width - 100)
        xanchor 1.0
        has vbox
        for key, v in sorted(right_magic.iteritems(), key=itemgetter(1)):
            $ skill = battle_skills[key]
            if skill not in char.magic_skills:
                $ price = right_magic[key][0]
                button:
                    maximum (350, 30)
                    action Return((skill, right_magic[key]))
                    text "[key]:":
                        xalign 0
                        color right_magic_color
                        drop_shadow [(1, 1)]
                        drop_shadow_color black
                    text "[price]":
                        xalign 1.0
                        color right_magic_color
                        drop_shadow [(1, 1)]
                        drop_shadow_color black
                    
    textbutton "I changed my mind...":
        style "dropdown_gm_button"
        align(0.5, 0.1)
        action Return("Nothing")
                    
screen character_pick_screen():
    frame:
        style_group "dropdown_gm"
        ypos 300
        xpos (config.screen_width - 100)
        xanchor 1.0
        has vbox
        for member in hero.team:
            textbutton "[member.nickname]":
                action If(member.status != "slave", Return(member))
