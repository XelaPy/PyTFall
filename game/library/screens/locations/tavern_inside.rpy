label tavern_town:
    if not "tavern_inside" in ilists.world_music:
        $ ilists.world_music["tavern_inside"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("tavern")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["tavern_inside"])
    $ global_flags.del_flag("keep_playing_music")

    
    scene bg tavern_inside   
    with dissolve
    $ tavern_dizzy = False
    
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
        $ global_flags.set_flag("tavern_status", value=[day, "lively"])
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
                if not file.endswith("db"):
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
    if hero.effects['Drunk']['active'] and not(tavern_dizzy):
        $ tavern_dizzy = True
        "You feel a little dizzy..."
        $ double_vision_on("bg tavern_inside")
        $ renpy.show("drunkards", what=img, at_list=[Position(ypos = 0.5, xpos = 0.5, yanchor = 0.5, xanchor = 0.5)])
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
    $ N = randint(2, 5)
    while i < N:
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
    if hero.take_money(randint(10, 20)):
        $ interactions_drinking_outside_of_inventory(character=hero, count=randint(15, 25))
        if global_flags.flag("tavern_status")[1] == "lively":
            $ N = random.choice(["fishing", "sex", "exp"])
        if N == "fishing":
            show expression "content/gfx/images/tavern/fish.png" as sign at truecenter with dissolve
            "A group of local fishermen celebrating a good catch in the corner. You join them, and they share a few secrets about fishing with you."
            $ hero.FISHING += randint(2, 5)
            hide sign with dissolve
        elif N == "sex":
            show expression "content/gfx/images/tavern/sex.png" as sign at truecenter with dissolve
            "A group of drunk young men boasting about their feats in the bed. Most of the feats never happened, but you still got a few interesting ideas."
            $ hero.SEX += randint(1, 3)
            hide sign with dissolve
        elif N == "exp":
            show expression "content/gfx/images/tavern/exp.png" as sign at truecenter with dissolve
            "You are sharing fresh rumors with patrons over a beer."
            $ hero.adjust_exp(randint(10, 30))
            hide sign with dissolve
    else:
        "You don't have enough money to join others, so there is nothing interesting for you at the moment."
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
