label swimming_pool:
    $ gm.enter_location(has_tags=["swimsuit", "sfw"], has_no_tags=["beach", "sleeping"], curious_priority=False)
    if not "swimming_pool" in ilists.world_music:
        $ ilists.world_music["swimming_pool"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("swimming_pool")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["swimming_pool"])
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        if pytfall.world_actions.location("swimming_pool"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    scene bg swimming_pool
    with dissolve
   
    if not global_flags.flag('visited_swimming_pool'):
        $ global_flags.set_flag('visited_swimming_pool')
        show npc trainer with dissolve
        "Welcome to the swimming pool!"
        "It's not free, but we don't have sea monsters and big waves here, so it's perfect for a novice swimmer!"
        "We also provide swimming lessons at a reasonable price. Feel free to ask anytime!"
        hide npc trainer with dissolve
    show screen swimming_pool
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
                
                
screen swimming_pool():
    use top_stripe(True)

    $ img = im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True)
    imagebutton:
        align (0.01, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("swimming_pool"), Jump("city_beach")]
    
    use location_actions("swimming_pool")
    $ img_swim_pool = ProportionalScale("content/gfx/interface/icons/sp_swimming.png", 90, 90)
    imagebutton:
        pos(290, 510)
        idle (img_swim_pool)
        hover (im.MatrixColor(img_swim_pool, im.matrix.brightness(0.15)))
        action [Hide("swimming_pool"), Show("swimmong_pool_swim"), With(dissolve)]
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
        
        hbox:
            align(0.5, 0.3)
            spacing 70
            
            for entry in gm.display_girls():
                use rg_lightbutton(img=entry.show("sfw", "swimsuit", "pool", exclude=["beach"], type="reduce", label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 
                
screen swimmong_pool_swim():
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
                xysize (240, 40)
                yalign 0.5
                action [Hide("swimmong_pool_swim"), Jump("single_swim_pool")]
                text "Swim (10 G)" size 15
            button:
                xysize (240, 40)
                yalign 0.5
                action [Hide("swimmong_pool_swim"), Jump("instructor_swim_pool")]
                text "Hire an instructor (50 G)" size 15
            if hero.get_skill("swimming") >= 100:
                button:
                    xysize (240, 40)
                    yalign 0.5
                    action [Hide("swimmong_pool_swim"), Jump("work_swim_pool")]
                    text "Work as instructor" size 15
            button:
                xysize (240, 40)
                yalign 0.5
                action [Hide("swimmong_pool_swim"), Show("swimming_pool"), With(dissolve)]
                text "Leave" size 15
                
label single_swim_pool:
    if hero.vitality < 50 or hero.AP <= 0:
        "You are too tired at the moment."
    elif hero.health < hero.get_max("health")*0.5:
        "You are too wounded at the moment."
    elif hero.take_money(10):
        play world "underwater.mp3"
        scene bg pool_swim
        with dissolve
        call hero_swimming_pool_skill_checks
    else:
        "You don't have enough gold."
    jump swimming_pool
    
label instructor_swim_pool:
    if hero.vitality < 50 or hero.AP <= 0:
        "You are too tired at the moment."
    elif hero.health < hero.get_max("health")*0.5:
        "You are too wounded at the moment."
    elif hero.take_money(50):
        play world "underwater.mp3"
        scene bg pool_swim
        with dissolve
        call instructor_swimming_pool_skill_checks
    else:
        "You don't have enough gold."
    jump swimming_pool
        
label hero_swimming_pool_skill_checks:
    $ hero.AP -= 1
    if hero.get_skill("swimming") < 20:
        if dice(60):
            "You barely stay afloat. Clearly more practice is needed."
            $ hero.swimming += randint(1,2)
        else:
            "You barely stay afloat. At some point you lose you cool and start drowning, but the swimming instructor immediately come to your aid."
            $ hero.swimming += 1
            $ hero.health -= 5
        $ hero.vitality -= randint (40, 50)
    elif hero.get_skill("swimming") < 50:
        "You can swim well enough to not drown in a swimming pool, but more practice is needed."
        $ hero.swimming += randint(2,3)
        $ hero.vitality -= randint (35, 45)
    elif hero.get_skill("swimming") < 100:
        "You are somewhat confident about your swimming skills, but big waves and playful dolphins are still bad news."
        $ hero.swimming += randint(2,4)
        $ hero.vitality -= randint (30, 40)
    else:
        "It feels nice swimming in the pool, but the sea is more suitable to learn something new."
        $ hero.swimming += randint(0,1)
        $ hero.vitality -= randint (20, 30)
    if dice(75) and hero.get_skill("swimming") >= 50:
        $ hero.mod_stat("constitution", 1)
    return
    
label instructor_swimming_pool_skill_checks:
    $ hero.AP -= 1
    if hero.get_skill("swimming") < 20:
        "He teaches you water safety to prevent mouth-to-mouth accidents once and for all."
        $ hero.swimming += randint(2,4)
        $ hero.SWIMMING += randint(2,4) # theoretical part
        $ hero.vitality -= randint (35, 45)
    elif hero.get_skill("swimming") < 50:
        "He shows you the most basic swimming styles."
        $ hero.swimming += randint(4,6)
        $ hero.SWIMMING += randint(4,6)
        $ hero.vitality -= randint (30, 40)
    elif hero.get_skill("swimming") < 100:
        "He shows you common swimming styles and the very basics of underwater swimming."
        $ hero.swimming += randint(4,8)
        $ hero.SWIMMING += randint(4,8)
        $ hero.vitality -= randint (25, 35)
    elif hero.get_skill("swimming") < 250:
        "He shows you advanced swimming styles, including underwater ones."
        $ hero.swimming += randint(1,3)
        $ hero.SWIMMING += randint(5,10)
        $ hero.vitality -= randint (20, 30)
    else:
        "There is not much he can show you now, but his knowledge about behavior on the water is second to none."
        $ hero.swimming += randint(0,1)
        $ hero.SWIMMING += randint(5,10)
        $ hero.vitality -= randint (20, 25)
    if dice(65) and hero.get_skill("swimming") >= 50:
        $ hero.mod_stat("constitution", 1)
    return

label work_swim_pool: # here we could use an option to meet characters with a certain probability
    $ result = randint(5, round(hero.get_skill("swimming")*0.1))
    if result > 200:
        $ result = randint (190, 220)
    $ hero.AP -= 1
    $ hero.swimming += randint(0,2)
    $ hero.SWIMMING += randint(1,2)
    $ hero.vitality -= randint (40, 50)
    $ picture = "content/gfx/images/swim_kids/sk_" + str(renpy.random.randint(1, 4)) + ".jpg"
    show expression picture at truecenter with dissolve
    $ narrator ("You teach local kids to swim. The payment is low, but at least you can use the pool for free. (+ %d) G" %result)
    $ hero.add_money (result)
    hide expression picture with dissolve
    $ del result
    jump swimming_pool