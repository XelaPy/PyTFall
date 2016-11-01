label city_beach_left:
    $ gm.enter_location(goodtraits=["Athletic", "Dawdler"], badtraits=["Scars", "Undead", "Furry", "Monster"], curious_priority=False)
    
    # Music related:
    if not "beach_main" in ilists.world_music:
        $ ilists.world_music["beach_main"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("beach_main")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["beach_main"])
    $ global_flags.del_flag("keep_playing_music")
    
    python:
        # Build the actions
        if pytfall.world_actions.location("city_beach_left"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()
    
    scene bg city_beach_left
    with dissolve
    show screen city_beach_left
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")
        
    while 1:

        $ result = ui.interact()

        if result[0] == 'jump':
            $ gm.start_gm(result[1])
        
        if result[0] == 'control':
            if result[1] == 'return':
                $ global_flags.set_flag("keep_playing_music")
                hide screen city_beach_left
                jump city_beach
                
                
screen city_beach_left():

    use top_stripe(True)
    
    # Jump buttons:
    $img = ProportionalScale("content/gfx/interface/icons/beach_cafe.png", 80, 80)
    imagebutton:
        pos(380, 300)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("city_beach_left"), Jump("city_beach_cafe_main")]
        
    $img = im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80)
    imagebutton:
        align (0.99, 0.5)
        idle (img)
        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
        action [Hide("city_beach_left"), Function(global_flags.set_flag, "keep_playing_music"), Jump("city_beach")]    
    
    $ img_beach_fish = ProportionalScale("content/gfx/interface/icons/beach_fishing.png", 90, 90)
    imagebutton:
        pos(960, 400)
        idle (img_beach_fish)
        hover (im.MatrixColor(img_beach_fish, im.matrix.brightness(0.15)))
        action [Hide("city_beach_left"), Jump("fishing_logic"), With(dissolve)]
    
    use location_actions("city_beach_left")
    
    if gm.show_girls:
    
        add "content/gfx/images/bg_gradient.png" yalign 0.2
    
        hbox:
            align(0.5, 0.3)
            spacing 70
            
            for entry in gm.display_girls():
                    
                    if not entry.flag("beach_left_tags") or entry.flag("beach_left_tags")[0] < day:
                        $beach_left_tags_list = []  
                        # main set                        
                        if entry.has_image("girlmeets","beach"):
                            $beach_left_tags_list.append(("girlmeets","beach"))
                        if entry.has_image("girlmeets","swimsuit","simple bg"):
                            $beach_left_tags_list.append(("girlmeets","swimsuit","simple bg"))
                        if entry.has_image("girlmeets","swimsuit","outdoors"):
                            $beach_left_tags_list.append(("girlmeets","swimsuit","outdoors"))
                        # secondary set if nothing found
                        if not beach_left_tags_list:
                            if entry.has_image("girlmeets","outdoors"):
                                $beach_left_tags_list.append(("girlmeets","outdoors"))
                            if entry.has_image("girlmeets","simple bg"):
                                $beach_left_tags_list.append(("girlmeets","simple bg"))    
                        # giveup  
                        if not beach_left_tags_list:
                            $beach_left_tags_list.append(("girlmeets"))   
                    
                        $ entry.set_flag("beach_left_tags", (day, choice(beach_left_tags_list)))
            
                    use rg_lightbutton(img=entry.show(*entry.flag("beach_left_tags")[1], exclude=["urban", "wildness", "suburb", "nature", "winter", "night", "formal", "indoor", "indoors"], type="first_default", label_cache=True, resize=(300, 400)), return_value=['jump', entry]) 

screen city_beach_fishing():
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
                
label fishing_logic:
    # during fishing itself only practical part of skill could be improved; theoretical part will be available via items and asking fishermen in tavern
    scene bg fishing_bg with dissolve
    
    if not global_flags.flag('fish_city_beach'):
        $ global_flags.set_flag('fish_city_beach')
        "If you have a fishing rod, you could try to catch something here. With high enough fishing skill you can get valuable items."
        "You can increase your chances to catch something good by using baits which could be bought or found in various places. However, they cannot be used if your fishing skill is too low, so make sure you practice a lot."
        "Bites also increase the amount of attempts you can make for every Action Point."
    menu:
        "Try out fishing?"
        "Yes":
            $ pass
        "Maybe later":
            jump city_beach_left
            
    if not has_items("Fishing Pole", [hero]):
        "You don't have a fishing rode at the moment. Try to get one from local shops."
        jump city_beach_left
    elif hero.AP <= 0:
        "You don't have Action Points left. Try again tomorrow."
        jump city_beach_left
    else:
        $ min_fish_price = 0
        $ fishing_attempts = 2
        if ("Simple Bait" in hero.inventory and hero.get_skill("fishing") >= 30) or ("Good Bait" in hero.inventory and hero.get_skill("fishing") >= 100) or ("Magic Bait" in hero.inventory and hero.get_skill("fishing") >= 200): # bites increase min price of available items; they are useless if skill is too low so they only can be used with more or less high skill
            menu:
                "Use Simple Bite" if ("Simple Bait" in hero.inventory and hero.get_skill("fishing") >= 30):
                    $ min_fish_price += 10
                    $ hero.remove_item("Simple Bait")
                    $ fishing_attempts = 3
                "Use Good Bite" if ("Good Bait" in hero.inventory and hero.get_skill("fishing") >= 100):
                    $ min_fish_price += 50
                    $ hero.remove_item("Good Bait")
                    $ fishing_attempts = 4
                "Use Magic Bite" if ("Magic Bait" in hero.inventory and hero.get_skill("fishing") >= 200):
                    $ min_fish_price += 100
                    $ hero.remove_item("Magic Bait")
                    $ fishing_attempts = 5
                "Don't use baits":
                    $ fishing_attempts = 2
                    
        $ hero.AP -= 1
        
        while fishing_attempts > 0:
            $ fishing_attempts -= 1
            python:
                fish_list = []
                fish = list(i for i in items.values() if "Fishing" in i.locations and min_fish_price <= i.price <= hero.get_skill("fishing")) # Get a list of fishing items player is skilled enough to fish out
                while len(fish_list) < 9:
                    fish_list.append(random.choice(fish))
            if not fish:
                $ hero.say("There is no suitable fish at the moment.")
            else:
                python:
                    item = renpy.call_screen("fishing_area", fish_list)
                    hero.add_item(item)
                    our_image = ProportionalScale(item.icon, 150, 150)
                
                show expression our_image at truecenter with dissolve
                $ hero.say("I caught %s!" % item.id)
                hide expression our_image with dissolve
                $ hero.fishing += round((100-item.chance)*0.1) # the less item's chance field, the more additional bonus to fishing; with 90 chance it will be +1, with less than 1 chance about 10
                
        $ del our_image
        $ del fish_list
        $ del fish
        $ del fishing_attempts
        $ del min_fish_price
        jump city_beach_left