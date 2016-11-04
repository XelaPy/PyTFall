label city_beach:
    $ gm.enter_location(goodtraits=["Energetic", "Exhibitionist"], badtraits=["Scars", "Undead", "Furry", "Monster", "Not Human"], curious_priority=False)
    # Music related:
    if not "beach_main" in ilists.world_music:
        $ ilists.world_music["beach_main"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("beach_main")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["beach_main"])
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("city_beach"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_beach
    with dissolve
    show screen city_beach
    
    if not global_flags.flag('visited_city_beach'):
        $ global_flags.set_flag('visited_city_beach')
        "Welcome to the beach!"
        "Sand, sun and girls in bikinis, what else did you expect?"
        "Oh, we might have a kraken hiding somewhere as well :)"

    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
    
    while 1:
        $ result = ui.interact()
        
        if result[0] == 'jump':
            $ gm.start_gm(result[1])
        
        if result[0] == 'control':
            if result[1] == 'return':
                hide screen city_beach
                jump city
                
                
screen city_beach():
    
    use top_stripe(True)
    
    # Jump buttons:
    $ img = im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80)
    imagebutton:
        id "meow"
        align (0.99, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("city_beach"), Jump("city_beach_right")]
        
    $ img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
    imagebutton:
        align (0.01, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("city_beach"), Function(global_flags.set_flag, "keep_playing_music"), Jump("city_beach_left")]
    
    use location_actions("city_beach")
    $ img_pool = ProportionalScale("content/gfx/interface/icons/swimming_pool.png", 60, 60)
    imagebutton:
        pos(1040, 80)
        idle (img_pool)
        hover (im.MatrixColor(img_pool, im.matrix.brightness(0.15)))
        action [Hide("city_beach"), Jump("swimming_pool")]
        
    $ img_beach_swim = ProportionalScale("content/gfx/interface/icons/sp_swimming.png", 90, 90)
    imagebutton:
        pos(280, 240)
        idle (img_beach_swim)
        hover (im.MatrixColor(img_beach_swim, im.matrix.brightness(0.15)))
        action [Hide("city_beach"), Show("city_beach_swim"), With(dissolve)]
        
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
        
        hbox:
            align(0.5, 0.3)
            spacing 70
            
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show("girlmeets", "swimsuit", "beach", exclude=["urban", "wildness", "suburb", "nature", "winter", "night", "formal", "indoor", "indoors"], type="reduce", label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 
                
screen city_beach_swim():
    frame:
        xalign 0.95
        ypos 20
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_group "wood"
            align (0.5, 0.5)
            spacing 10
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_beach_swim"), Jump("city_beach_swimming_checks")]
                text "Swim" size 15
            if hero.get_skill("swimming") >= -100: # FOR TESTING! do not forget to change back to >= 100
                button:
                    xysize (120, 40)
                    yalign 0.5
                    action [Hide("city_beach_swim"), Jump("city_beach_diving_checks")]
                    text "Diving" size 15
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_beach_swim"), Show("city_beach"), With(dissolve)]
                text "Leave" size 15
                
label city_beach_swimming_checks:   
    if not global_flags.flag('swam_city_beach'):
        $ global_flags.set_flag('swam_city_beach')
        "The city is washed by the ocean. The water is quite warm all year round, but it can be pretty dangerous for a novice swimmers due to big waves and sea monsters."
        "Those who are not confident in their abilities prefer the local swimming pool, although it's not free unlike the sea."
        "In general, the swimming skill will increase faster in the ocean, unless you drown immediately due to low skill."
        scene bg open_sea
        with dissolve
        "You stay in shallow water not too far from land to get used to the water. It feels nice, but the real swimming will require some skills next time."
    else:
        if hero.vitality < 50 or hero.AP <= 0:
            "You are too tired at the moment."
        elif hero.health < hero.get_max("health")*0.5:
            "You are too wounded at the moment."
        else:
            scene bg open_sea with dissolve
            call hero_ocean_skill_checks
    $ global_flags.set_flag("keep_playing_music")
    jump city_beach
    
label hero_ocean_skill_checks:
    $ hero.AP -= 1
    if hero.get_skill("swimming") < 50:
        if dice(50):
            $ narrator ("You trying to swim, but strong tide keeps you away {color=[red]}(no bonus to swimming skill this time){/color}.")
        else:
            scene bg ocean_underwater with dissolve
            "Waves are pretty big today. You trying to fight them, but they quickly win, sending you under the water."
            $ narrator ("Nearly drowned, you get out of the ocean {color=[red]}(-25% health){/color}.")
            $ hero.health -= int(hero.get_max("health")*0.25) # we don't allow MC to do it unless his health is more than 50%, so it's fine to take 25% due to low skill
            $ hero.swimming += randint(1, 2)
        $ hero.vitality -= randint (40, 50)
    elif hero.get_skill("swimming") < 100:
        "You trying to swim, but rapid underwater currents make it very difficult for a novice swimmer."
        if dice(30):
            scene bg ocean_underwater with dissolve
            "Waves are pretty big today. You trying to fight them, but they win, sending you under the water."
            $ narrator ("Nearly drowned, you get out of the ocean {color=[red]}(-20% health){/color}.")
            $ hero.health -= int(hero.get_max("health")*0.2)
        $ hero.swimming += randint(3, 5)
        $ hero.vitality -= randint (40, 50)
    elif hero.get_skill("swimming") < 150:
        "You cautiously swim in the ocean, trying to stay close to the shore just in case."
        if dice(10):
            scene bg ocean_underwater with dissolve
            "Waves are pretty big today. You trying to fight them, but eventually they win, sending you under the water."
            $ narrator ("Nearly drowned, you get out of the ocean {color=[red]}(-15% health){/color}.")
            $ hero.health -= int(hero.get_max("health")*0.15)
        $ hero.swimming += randint(4, 8)
        $ hero.vitality -= randint (30, 40)
    else:
        "You take your time enjoying the water. Even big ocean waves are no match for your swimming skill."
        $ hero.swimming += randint(6, 10)
        $ hero.vitality -= randint (20, 30)
    return
    
transform alpha_dissolve:
    alpha 0.0
    linear 0.5 alpha 1.0
    on hide:
        linear 0.5 alpha 0
    
screen diving_progress_bar(o2, max_o2): # oxygen bar for diving
    default oxigen = o2
    default max_oxigen = max_o2
    
    timer .1 repeat True action If(oxigen > 0, true=SetScreenVariable('oxigen', oxigen - 1), false=(Hide("diving_progress_bar"), Return("All out of Air!")))
    
    if config.debug:
        vbox:
            xalign .5
            text str(oxigen)
            text str(max_oxigen)
    
    bar:
        right_bar im.Scale("content/gfx/interface/bars/oxigen_bar_empty.png", 300, 50)
        left_bar im.Scale("content/gfx/interface/bars/oxigen_bar_full.png", 300, 50)
        value oxigen
        range max_oxigen
        thumb None
        xysize (300, 50)
        at alpha_dissolve
    
label city_beach_diving_checks:
    if not global_flags.flag('diving_city_beach'):
        $ global_flags.set_flag('diving_city_beach')
        "With high enough swimming skill you can try diving. Every action consumes your vitality, and the amount of oxygen is based on your swimming skill."
        "You cannot continue if your vitality is too low. The goal is to find invisible items the screen."
    if hero.AP <= 0:
        "You don't have Action Points at the moment. Try again tomorrow."
        jump city_beach
    elif hero.vitality < 10:
        "You're too tired at the moment."
        jump city_beach
    elif hero.health < hero.get_max("health")*0.5:
        "You are too wounded at the moment."
        jump city_beach
    play world "underwater.mp3"
    $ hero.AP -= 1
    scene bg ocean_underwater_1 with dissolve
    if has_items("Snorkel Mask", [hero]):
        $ i = int(hero.get_skill("swimming")+1) + 50
    else:
        $ i = int(hero.get_skill("swimming")+1)
    
    if has_items("Underwater Lantern", [hero]):
        $ j = 90
    else:
        $ j = 60
        
    show screen diving_progress_bar(i, i)
    while hero.vitality > 10:
        if not renpy.get_screen("diving_progress_bar"):
            hide screen hidden_area
            "You've ran out of air!"
            jump city_beach
        
        $ underwater_loot = tuple([choice(list(i for i in items.values() if "Diving" in i.locations and dice(i.chance)) or [False]), (j, j), (random.random(), random.random())] for i in range(4))
        show screen hidden_area(underwater_loot)
        
        $ result = ui.interact()
        
        if result == "All out of Air!":
            hide screen hidden_area
            "You've ran out of air!"
            jump city_beach
        
        if isinstance(result, Item):
            hide screen hidden_area
            $ item = result
            $ hero.add_item(item)
            $ our_image = ProportionalScale(item.icon, 150, 150)
            show expression our_image at truecenter with dissolve
            $ hero.say("I caught %s!" % item.id)
            hide expression our_image with dissolve
        else:
            $ hero.say("There is nothing there.")
            
        $ hero.vitality -= randint(10, 20) 
        
    hide screen hidden_area
    hide screen diving_progress_bar
    "You're too tired to continue!"
    jump city_beach