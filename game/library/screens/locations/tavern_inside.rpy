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
    
    if not global_flags.flag('visited_tavern'):
        show npc tavern_rita_novel
        with dissolve
        $ global_flags.set_flag('visited_tavern')
        tavern_rita "Oh, hello! Welcome to our tavern! We will always have a seat for you! *wink*"
        hide npc
        with dissolve
    
    elif dice(0):
        python:
            tavern_status = "cozy"
            for file in os.listdir(content_path("events/tavern_entry/cozy/")):
                tavern_event_list.append('content/events/tavern_entry/cozy/%s' % (file))
            img = ProportionalScale(choice(tavern_event_list), 1000, 600)
            renpy.show("drunkards", what=img, at_list=[Position(ypos = 0.5, xpos = 0.5, yanchor = 0.5, xanchor = 0.5)])
            renpy.with_statement(dissolve)
            narrator ("The tavern is warm and cozy with only a handfull of drunkards enjoying the stay.") 
    elif dice(0):
        python:
            tavern_status = "lively"
            for file in os.listdir(content_path("events/tavern_entry/lively/")):
                    tavern_event_list.append('content/events/tavern_entry/lively/%s' % (file))
            img = ProportionalScale(choice(tavern_event_list), 1000, 600)
            renpy.show("drunkards", what=img, at_list=[Position(ypos = 0.5, xpos = 0.5, yanchor = 0.5, xanchor = 0.5)])
            renpy.with_statement(dissolve)
            narrator ("The place is loud and lively today, with townsmen drinking and talking at every table.") 
    else:
        python:
            tavern_status = "brawl"
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
                jump city_tavern_thugs_fight
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
                
               
label tavern_look_around:
    if (day >= hero.flag("tavern_thugs")) and dice(50):
        if hero.gold < 50:
            "A group of thugs surrounded you and proposed to pay for their drinks. You don't have so much money, so the fight is unavoidable..."
            jump city_tavern_thugs_fight
        else:
            menu:
                "A group of thugs surround you and propose to pay for their drinks."
                       
                "Pay":
                    if hero.take_money(50):
                        "You avoid confrontation and pay for their drinks."
                        $ hero.set_flag("tavern_thugs", value=day+1)
                        jump city_tavern_menu
                    else:
                        "You don't have so much money, so the fight is unavoidable..."
                        jump city_tavern_thugs_fight
                "Refuse":
                    "You refuse to pay and prepare for a fight."
                    jump city_tavern_thugs_fight
    jump city_tavern_menu
                
label city_tavern_thugs_fight:
    python:
        enemies = ["Thug", "Assassin", "Barbarian"]
        enemy_team = Team(name="Enemy Team", max_size=3)
        for i in range(randint(2, 3)):
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
                narrator ("After you beat the thugs, you found a few coins in their pockets. It will teach them a lesson.")
                hero.set_flag("tavern_thugs", value=day+randint(4,7))
                hero.add_money(randint(50, 150))
        jump city_tavern_menu
    else:
        $ hero.set_flag("tavern_thugs", value=day+1)
        if hero.take_money(randint(150, 500)):
            "You were beaten and robbed..."
        else:
            "You were beaten..."
        jump city
    
                
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
