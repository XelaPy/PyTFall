label tavern_town:
    if not "tavern_inside" in ilists.world_music:
        $ ilists.world_music["tavern_inside"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("tavern")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["tavern_inside"])
    $ global_flags.del_flag("keep_playing_music")

    
    scene bg tavern_inside   
    with dissolve
    
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto") 
    

    define tavern_rita = Character('Rita', color=honeydew, show_two_window=True)
    $ tavern_event_list = []
    if hero.flag("fought_in_tavern") == day:
        show npc tavern_rita_novel
        with dissolve
        tavern_rita "I'm sorry, we are closed for maintenance. Please come tomorrow."
        jump city
        
    if not global_flags.flag('visited_tavern'):
        $ global_flags.set_flag('visited_tavern')
        show npc tavern_rita_novel
        with dissolve
        tavern_rita "Oh, hello! Welcome to our tavern! We will always have a seat for you! *wink*"
        hide npc
        with dissolve
        $ global_flags.set_flag("tavern_status", value=[day, "cozy"])
    else:
        if global_flags.flag("tavern_status")[0] != day:
            $ tavern_status = weighted_choice([["cozy", 40], ["lively", 40], ["brawl", 20]])
            $ global_flags.set_flag("tavern_status", value=[day, tavern_status])
    if global_flags.flag("tavern_status")[1] == "cozy":
        python:
            for file in os.listdir(content_path("events/tavern_entry/cozy/")):
                tavern_event_list.append('content/events/tavern_entry/cozy/%s' % (file))
            img = ProportionalScale(choice(tavern_event_list), 1000, 600)
            renpy.show("drunkards", what=img, at_list=[Position(ypos = 0.5, xpos = 0.5, yanchor = 0.5, xanchor = 0.5)])
            renpy.with_statement(dissolve)
            narrator ("The tavern is warm and cozy with only a handful of drunkards enjoying the stay.") 
    elif global_flags.flag("tavern_status")[1] == "lively":
        python:
            for file in os.listdir(content_path("events/tavern_entry/lively/")):
                    tavern_event_list.append('content/events/tavern_entry/lively/%s' % (file))
            img = ProportionalScale(choice(tavern_event_list), 1000, 600)
            renpy.show("drunkards", what=img, at_list=[Position(ypos = 0.5, xpos = 0.5, yanchor = 0.5, xanchor = 0.5)])
            renpy.with_statement(dissolve)
            narrator ("The place is loud and lively today, with townsmen drinking and talking at every table.") 
    else:
        python:
            for file in os.listdir(content_path("events/tavern_entry/brawl/")):
                    tavern_event_list.append('content/events/tavern_entry/brawl/%s' % (file))
            img = ProportionalScale(choice(tavern_event_list), 1000, 600)
            renpy.show("event", what=img, at_list=[Position(ypos = 0.5, xpos = 0.5, yanchor = 0.5, xanchor = 0.5)])
            renpy.with_statement(dissolve)
            renpy.music.stop(channel="world")
            renpy.music.play("brawl.mp3",channel="world") 
            narrator ("You step into the room... right into a fierce tavern brawl!")
        menu:
            "Join it!":
                jump city_tavern_brawl_fight
            "Leave while you can":
                jump city
label city_tavern_menu:
    show screen city_tavern_inside
    while 1:
        $ result = ui.interact()

screen city_tavern_inside():
    use top_stripe(True)
    frame:
        xalign 0.95
        ypos 50
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
                action [Hide("city_tavern_inside"), Jump("tavern_shopping")]
                text "Buy a drink" size 15
            if hero.AP > 0:
                button:
                    xysize (120, 40)
                    yalign 0.5
                    action [Hide("city_tavern_inside"), Jump("tavern_look_around")]
                    text "Look around" size 15
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_tavern_inside"), Jump("city")]
                text "Leave" size 15
                
label city_tavern_brawl_fight:
    if len(hero.team) == 1:
        "You go inside, and a few thugs immediately notice you."
    else:
        "You nod to your teammates and go inside. A few thugs immediately notice you."
    call city_tavern_thugs_fight
    if hero.flag("fought_in_tavern") == day:
        if hero.take_money(randint(50, 250)):
            "You were beaten and robbed..."
        else:
            "You were beaten..."
        jump city
    $ i = 1
    while i < randint(2, 5):
        if hero.flag("fought_in_tavern") == day:
            if hero.take_money(randint(150, 250)):
                "You were beaten and robbed..."
            else:
                "You were beaten..."
                jump city

        scene bg tavern_inside   
        with dissolve
        "Another group is approaching you!"
        menu:
            "Fight!":
                $ pass
            "Run away":
                "You quickly leave the tavern."
                $ hero.set_flag("fought_in_tavern", value = day)
                jump city
        call city_tavern_thugs_fight
        $ i += 1
    "The fight is finally over. You found a few coins in thugs pockets."
    $ hero.add_money(randint(50, 150)*i)
    $ hero.set_flag("fought_in_tavern", value = day)
    jump city
label tavern_look_around:
    $ pass
    jump city_tavern_menu
                
label city_tavern_thugs_fight:
    python:
        enemies = ["Thug", "Assassin", "Barbarian"]
        enemy_team = Team(name="Enemy Team", max_size=3)
        for j in range(randint(2, 3)):
            mob = build_mob(id=random.choice(enemies), level=randint(5, 25))
            mob.front_row = True
            mob.controller = BE_AI(mob)
            enemy_team.add(mob)
        back = interactions_pick_background_for_fight("tavern")
        result = run_default_be(enemy_team, background=back)
        
    scene bg tavern_inside   
    with dissolve

    if result is True:
        python:
            for member in hero.team:
                member.exp += adjust_exp(member, 250)

    else:
        $ hero.set_flag("fought_in_tavern", value = day)
    return
    
                
label tavern_shopping:
    show npc tavern_rita_novel
    with dissolve
    tavern_rita "Do you want something?"
    python:
        focus = None
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.tavern
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter(filter)

    show screen shopping(left_ref=hero, right_ref=shop)
    with dissolve
    
    call shop_control from _call_shop_control_6
                    
    $ global_flags.del_flag("keep_playing_music")      
    hide screen shopping
    hide npc tavern_rita_novel
    with dissolve
    jump city_tavern_menu
                


    
screen tavern_inside():

    use top_stripe(True)
    
    use location_actions("tavern_inside")
