label tavern_town:
    if not "tavern_inside" in ilists.world_music:
        $ ilists.world_music["tavern_inside"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("tavern")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["tavern_inside"])
    $ global_flags.del_flag("keep_playing_music")


    scene bg tavern_inside
    with dissolve

    $ tavern_dizzy = False

    $ tavern_rita = npcs["Rita_tavern"].say

    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")


    $ tavern_event_list = []
    if hero.flag("fought_in_tavern") == day: # after a brawl tavern will be unavailable until the next turn
        show expression npcs["Rita_tavern"].get_vnsprite() as npc
        with dissolve
        tavern_rita "I'm sorry, we are closed for maintenance. Please return tomorrow."
        jump city

    if not global_flags.flag('visited_tavern'):
        $ global_flags.set_flag('visited_tavern')
        $ city_tavern_dice_bet = 5 # default dice bet
        show expression npcs["Rita_tavern"].get_vnsprite() as npc
        with dissolve
        tavern_rita "Oh, hello! Welcome to our tavern! We will always have a seat for you! *wink*"
        hide npc
        with dissolve
        $ global_flags.set_flag("tavern_status", value=[day, "cozy"])
    else:
        if global_flags.flag("tavern_status")[0] != day: # every day tavern can randomly have one of three statuses, depending on the status it has very different activities available
            $ tavern_status = weighted_choice([["cozy", 40], ["lively", 40], ["brawl", 20]])
            $ global_flags.set_flag("tavern_status", value=[day, tavern_status])
    if global_flags.flag("tavern_status")[1] == "cozy":
        python:
            for file in os.listdir(content_path("events/tavern_entry/cozy/")):
                if check_image_extension(file):
                    tavern_event_list.append('content/events/tavern_entry/cozy/%s' % (file))
            img = ProportionalScale(choice(tavern_event_list), 1000, 600)
            renpy.show("drunkards", what=img, at_list=[Position(ypos = .5, xpos = .5, yanchor = .5, xanchor = .5)])
            renpy.with_statement(dissolve)
            narrator ("The tavern is warm and cozy with only a handful of drunkards enjoying the stay.")
    elif global_flags.flag("tavern_status")[1] == "lively":
        python:
            for file in os.listdir(content_path("events/tavern_entry/lively/")):
                if check_image_extension(file):
                    tavern_event_list.append('content/events/tavern_entry/lively/%s' % (file))
            img = ProportionalScale(choice(tavern_event_list), 1000, 600)
            renpy.show("drunkards", what=img, at_list=[Position(ypos = .5, xpos = .5, yanchor = .5, xanchor = .5)])
            renpy.with_statement(dissolve)
            narrator ("The place is loud and lively today, with townsmen drinking and talking at every table.")
    else:
        python:
            for file in os.listdir(content_path("events/tavern_entry/brawl/")):
                if check_image_extension(file):
                    tavern_event_list.append('content/events/tavern_entry/brawl/%s' % (file))
            img = ProportionalScale(choice(tavern_event_list), 1000, 600)
            renpy.show("event", what=img, at_list=[Position(ypos = .5, xpos = .5, yanchor = .5, xanchor = .5)])
            renpy.with_statement(dissolve)
            renpy.music.stop(channel="world")
            renpy.music.play("brawl.mp3",channel="world")
            narrator ("You step into the room... right into a fierce tavern brawl!")
        menu:
            "Join it!":
                jump city_tavern_brawl_fight
            "Leave while you can":
                jump city

label city_tavern_menu: # "lively" status is limited by drunk effect; every action rises drunk counter, and every action with drunk effect active decreases AP
    scene bg tavern_inside
    if 'Drunk' in hero.effects and not(tavern_dizzy):
        $ tavern_dizzy = True
        "You feel a little dizzy... Perhaps you should go easy on drinks."
        $ double_vision_on("bg tavern_inside")
        $ renpy.show("drunkards", what=img, at_list=[Position(ypos = .5, xpos = .5, yanchor = .5, xanchor = .5)])
    show screen city_tavern_inside
    while 1:
        $ result = ui.interact()

label city_tavern_choose_label:
    "Here you can set how much to bet to avoid doing it before every game in the tavern. The more your level, the higher bets are available."
    "The current bet is [city_tavern_dice_bet] G."
    menu:
        "How much do you wish to bet?"
        "5 G":
            $ city_tavern_dice_bet = 5
        "10 G":
            $ city_tavern_dice_bet = 10
        "50 G" if hero.level >= 20:
            $ city_tavern_dice_bet = 50
        "100 G" if hero.level >= 50:
            $ city_tavern_dice_bet = 50
        "200 G" if hero.level >= 100:
            $ city_tavern_dice_bet = 200
        "500 G" if hero.level >= 200:
            $ city_tavern_dice_bet = 500
    jump city_tavern_menu

screen city_tavern_inside():
    use top_stripe(False)
    frame:
        xalign .95
        ypos 50
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_prefix "wood"
            align (.5, .5)
            spacing 10
            button:
                xysize (120, 40)
                yalign .5
                action [Hide("city_tavern_inside"), Jump("city_tavern_shopping")]
                text "Buy a drink" size 15
            if hero.AP > 0 and global_flags.flag("tavern_status")[1] == "lively":
                button:
                    xysize (120, 40)
                    yalign .5
                    action [Hide("city_tavern_inside"), Jump("mc_action_tavern_look_around")]
                    text "Look around" size 15
            if hero.AP > 0 and global_flags.flag("tavern_status")[1] == "cozy" and hero.flag("rest_in_tavern") != day:
                button:
                    xysize (120, 40)
                    yalign .5
                    action [Hide("city_tavern_inside"), Jump("mc_action_tavern_relax")]
                    text "Relax" size 15
            if hero.AP > 0 and global_flags.flag("tavern_status")[1] == "cozy":
                button:
                    xysize (120, 40)
                    yalign .5
                    action [Hide("city_tavern_inside"), Jump("city_tavern_play_dice")]
                    text "Blackjack" size 15
            if hero.AP > 0 and global_flags.flag("tavern_status")[1] == "cozy":
                button:
                    xysize (120, 40)
                    yalign .5
                    action [Hide("city_tavern_inside"), Jump("city_tavern_play_poker")]
                    text "Poker" size 15
            if global_flags.flag("tavern_status")[1] == "cozy":
                button:
                    xysize (120, 40)
                    yalign .5
                    action [Hide("city_tavern_inside"), Jump("city_tavern_choose_label")]
                    text "Set dice bet" size 15
            button:
                xysize (120, 40)
                yalign .5
                action [Hide("city_tavern_inside"), Jump("city")]
                text "Leave" size 15
                keysym "mousedown_3"

label mc_action_tavern_relax:
    hide drunkards with dissolve
    if len(hero.team) < 2:
        $ hero.set_flag("rest_in_tavern", value = day)
        "You relax for awhile, but there isn't much to do here. Perhaps it would be more fun if you weren't alone."
        $ hero.vitality += 5
    else:
        if hero.take_money(randint(30, 50), reason="Tavern"):
            $ hero.set_flag("rest_in_tavern", value = day)
            $ members = list(x for x in hero.team if (x != hero))
            if len(members) == 1:
                show expression members[0].get_vnsprite() at center as temp1
                with dissolve
            else:
                show expression members[0].get_vnsprite() at center_left as temp1
                show expression members[1].get_vnsprite() at center_right as temp2
                with dissolve
            "You ordered a few drinks and spent some time together."
            python:
                for member in members:
                    member.joy += randint(2, 4)
                    member.disposition += randint(3, 5)
                    interactions_drinking_outside_of_inventory(character=member, count=randint(15, 40))
                interactions_drinking_outside_of_inventory(character=hero, count=randint(15, 25))
            hide temp1
            hide temp2
            with dissolve
        else:
            "You could spend time with your team, but sadly you are too poor to afford it at the moment."
    jump city_tavern_menu

label city_tavern_brawl_fight:
    if len(hero.team) == 1:
        "You go inside, and a few thugs immediately notice you."
    else:
        "You nod to your teammates and go inside. A few thugs immediately notice you."

    call city_tavern_thugs_fight from _call_city_tavern_thugs_fight
    if hero.flag("fought_in_tavern") == day:
        if hero.take_money(randint(50, 250), reason="Tavern"):
            "You were beaten and robbed..."
        else:
            "You were beaten..."
        jump city

    $ i = 1
    $ N = randint(2, 5)
    while i < N:
        if hero.flag("fought_in_tavern") == day:
            if hero.take_money(randint(150, 250), reason="Tavern"):
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
        call city_tavern_thugs_fight from _call_city_tavern_thugs_fight_1
        $ i += 1

    "The fight is finally over. You found a few coins in thugs pockets."
    $ hero.add_money(randint(50, 150)*i, reason="Tavern")
    $ hero.set_flag("fought_in_tavern", value = day)
    jump city


label mc_action_tavern_look_around: # various bonuses to theoretical skills for drinking with others in the lively mode
    if hero.take_money(randint(10, 20), reason="Tavern"):
        hide drunkards with dissolve

        $ interactions_drinking_outside_of_inventory(character=hero, count=randint(15, 25))
        $ N = random.choice(["fishing", "sex", "exp"])

        if N == "fishing":
            $ name = "content/gfx/images/tavern/fish_" + str(renpy.random.randint(1, 4)) + ".webp"
            show expression name as sign at truecenter with dissolve
            "A group of local fishermen celebrating a good catch in the corner. You join them, and they share a few secrets about fishing with you."
            $ hero.FISHING += randint(2, 5)
            hide sign with dissolve
        elif N == "sex":
            $ character = random.choice(chars.values())
            $ picture = character.show("sex", resize=(500, 600))
            show expression picture as sign at truecenter with dissolve
            "A group of drunk young men and women boasting about their sexual feats. Most of the feats never happened, but you still got a few interesting ideas."
            $ hero.SEX += randint(1, 3)
            hide sign with dissolve
        else:
            show expression "content/gfx/images/tavern/exp.webp" as sign at truecenter with dissolve
            "You are sharing fresh rumors with patrons over a beer."
            $ hero.exp += exp_reward(hero, hero)
            hide sign with dissolve

        $ del N
    else:
        "You don't have enough money to join others, so there is nothing interesting for you at the moment."

    jump city_tavern_menu

label city_tavern_thugs_fight: # fight with random thugs in the brawl mode
    python:
        enemies = ["Thug", "Assassin", "Barbarian"]
        enemy_team = Team(name="Enemy Team", max_size=3)
        for j in range(randint(2, 3)):
            mob = build_mob(id=random.choice(enemies), level=randint(5, 25))
            mob.front_row = True
            mob.controller = Complex_BE_AI(mob)
            enemy_team.add(mob)
        back = interactions_pick_background_for_fight("tavern")
        result = run_default_be(enemy_team, background=back, skill_lvl=3)

    scene bg tavern_inside
    with dissolve

    if result is True:
        python:
            for member in hero.team:
                member.exp += exp_reward(member, enemy_team)

    else:
        $ hero.set_flag("fought_in_tavern", value = day)
    return


label city_tavern_shopping: # tavern shop with alcohol, available in all modes except brawl
    hide drunkards with dissolve
    show expression npcs["Rita_tavern"].get_vnsprite() as npc
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
    hide npc
    with dissolve
    jump city_tavern_menu

screen tavern_inside():

    use top_stripe(True)

    use location_actions("tavern_inside")
