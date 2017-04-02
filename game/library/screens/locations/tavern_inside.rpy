define tavern_rita = Character('Rita', color=honeydew, show_two_window=True)

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


    $ tavern_event_list = []
    if hero.flag("fought_in_tavern") == day: # after a brawl tavern will be unavailable until the next turn
        show npc tavern_rita_novel
        with dissolve
        tavern_rita "I'm sorry, we are closed for maintenance. Please come tomorrow."
        jump city

    if not global_flags.flag('visited_tavern'):
        $ global_flags.set_flag('visited_tavern')
        $ city_tavern_dice_bet = 5 # default dice bet
        show npc tavern_rita_novel
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
                if not file.endswith("db"):
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
                if not file.endswith("db"):
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

label city_tavern_menu: # "lively" status is limited by drunk effect; every action rises drunk counter, and every action with drunk effect active decreases AP
    if hero.effects['Drunk']['active'] and not(tavern_dizzy):
        $ tavern_dizzy = True
        "You feel a little dizzy... Perhaps you should go easy on drinks."
        $ double_vision_on("bg tavern_inside")
        $ renpy.show("drunkards", what=img, at_list=[Position(ypos = 0.5, xpos = 0.5, yanchor = 0.5, xanchor = 0.5)])
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
    use top_stripe(True)
    frame:
        xalign 0.95
        ypos 50
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_prefix "wood"
            align (0.5, 0.5)
            spacing 10
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_tavern_inside"), Jump("city_tavern_shopping")]
                text "Buy a drink" size 15
            if hero.AP > 0 and global_flags.flag("tavern_status")[1] == "lively":
                button:
                    xysize (120, 40)
                    yalign 0.5
                    action [Hide("city_tavern_inside"), Jump("tavern_look_around")]
                    text "Look around" size 15
            if hero.AP > 0 and global_flags.flag("tavern_status")[1] == "cozy" and hero.flag("rest_in_tavern") != day:
                button:
                    xysize (120, 40)
                    yalign 0.5
                    action [Hide("city_tavern_inside"), Jump("tavern_relax")]
                    text "Relax" size 15
            if hero.AP > 0 and global_flags.flag("tavern_status")[1] == "cozy":
                button:
                    xysize (120, 40)
                    yalign 0.5
                    action [Hide("city_tavern_inside"), Jump("city_tavern_play_dice")]
                    text "Blackjack" size 15
            if hero.AP > 0 and global_flags.flag("tavern_status")[1] == "cozy":
                button:
                    xysize (120, 40)
                    yalign 0.5
                    action [Hide("city_tavern_inside"), Jump("city_tavern_play_poker")]
                    text "Poker" size 15
            if global_flags.flag("tavern_status")[1] == "cozy":
                button:
                    xysize (120, 40)
                    yalign 0.5
                    action [Hide("city_tavern_inside"), Jump("city_tavern_choose_label")]
                    text "Set dice bet" size 15
            button:
                xysize (120, 40)
                yalign 0.5
                action [Hide("city_tavern_inside"), Jump("city")]
                text "Leave" size 15

label tavern_relax:
    hide drunkards with dissolve
    if len(hero.team) < 2:
        $ hero.set_flag("rest_in_tavern", value = day)
        "You relax for awhile, but there is not much to do here. Perhaps if would be less boring if you wouldn't be alone..."
        $ hero.vitality += 5
    else:
        if hero.take_money(randint(30, 50)):
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


label tavern_look_around: # various bonuses to theoretical skills for drinking with others in the lively mode
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

label city_tavern_thugs_fight: # fight with random thugs in the brawl mode
    python:
        enemies = ["Thug", "Assassin", "Barbarian"]
        enemy_team = Team(name="Enemy Team", max_size=3)
        for j in range(randint(2, 3)):
            mob = build_mob(id=random.choice(enemies), level=randint(5, 25))
            mob.front_row = True
            mob.controller = BE_AI(mob)
            enemy_team.add(mob)
        back = interactions_pick_background_for_fight("tavern")
        result = run_default_be(enemy_team, background=back, skill_lvl=3)

    scene bg tavern_inside
    with dissolve

    if result is True:
        python:
            for member in hero.team:
                member.exp += adjust_exp(member, 150)

    else:
        $ hero.set_flag("fought_in_tavern", value = day)
    return


label city_tavern_shopping: # tavern shop with alcohol, available in all modes except brawl
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

screen city_tavern_dicing(): # dice game controls menu
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
                action [Jump("city_tavern_throw_dice")]
                text "Throw dice" size 15
            button:
                xysize (120, 40)
                yalign 0.5
                action [Jump("tavern_dice_pass")]
                text "Pass" size 15
            button:
                xysize (120, 40)
                yalign 0.5
                action [Jump("city_tavern_dices_give_up")]
                text "Give up" size 15
                
label city_tavern_dices_give_up:
    $ hero.take_money(city_tavern_current_dice_bet)
    hide screen city_tavern_dicing
    hide screen city_tavern_show_dices
    with dissolve
    jump city_tavern_menu

screen city_tavern_show_status(d_1, d_2): # additional screen, shows all info related to the dice game
    frame:
        xalign 0.05
        yalign 0.05
        xysize (90, 90)
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            xalign 0.5
            yalign 0.5
            hbox:
                text str(d_1) xalign 0.98 style "stats_value_text" color gold
                xalign 0.5
            hbox:
                if ai_passed and d_1 < 21:
                    text ("Pass") xalign 0.98 style "stats_value_text" color gold
                elif d_1 > 21:
                    text ("Lost") xalign 0.98 style "stats_value_text" color gold
                elif d_1 == 21:
                    text ("Score!") xalign 0.98 style "stats_value_text" color gold
                else:
                    text (" ") xalign 0.98 style "stats_value_text" color gold
                xalign 0.5
    frame:
        xalign 0.05
        yalign 0.95
        xysize (90, 90)
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            xalign 0.5
            yalign 0.5
            hbox:
                text str(d_2) xalign 0.98 style "stats_value_text" color gold
                xalign 0.5
            hbox:
                if player_passed and d_2 < 21:
                    text ("Pass") xalign 0.98 style "stats_value_text" color gold
                elif d_2 > 21:
                    text ("Lost") xalign 0.98 style "stats_value_text" color gold
                elif d_2 == 21:
                    text ("Score!") xalign 0.98 style "stats_value_text" color gold
                else:
                    text (" ") xalign 0.98 style "stats_value_text" color gold
                xalign 0.5
                
    frame:
        xalign 0.5
        yalign 0.05
        xysize (120, 120)
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 1
        ypadding 1
        vbox:
            xalign 0.5
            add "content/gfx/interface/images/tavern_gold.png"
            text str(city_tavern_current_dice_bet) xalign 0.5 style "stats_value_text" color gold

screen city_tavern_show_dices(dice_1, dice_2): # main dice screen, shows dices themselves
    on "hide":
        action Hide("city_tavern_show_status")
    hbox:
        align .5, .4
        spacing 5
        box_reverse True
        for i in dice_1:
            add "content/events/tavern_dice/"+str(i)+".png" at dice_roll_zooming()
    hbox:
        align .5, .6
        spacing 5
        for i in dice_2:
            add "content/events/tavern_dice/"+str(i)+".png" at dice_roll_zooming()

label tavern_dice_pass: # player passes, and cannot throw dices anymore
    $ player_passed = True
    jump city_tavern_throw_dice

label city_tavern_play_dice: # starting the dice game
    if not global_flags.flag('played_dice_in_tavern'):
        $ global_flags.set_flag('played_dice_in_tavern')
        "The goal of the game is to reach a final score higher than the opponent without exceeding 21, or let the opponent throw dices until his score exceeds 21."
    if hero.effects['Drunk']['active']: # dizzy screen does not look good with dices animation...
        "You are too drunk for games at the moment."
        jump city_tavern_menu
    elif hero.gold < city_tavern_dice_bet:
        "Sadly, you don't have enough money to make a bet."
        jump city_tavern_menu
        
    hide drunkards with dissolve
    $ city_tavern_current_dice_bet = city_tavern_dice_bet # current bet may increase after every victory
    
    
label city_tavern_play_dice_another_round: # additional rounds continue from here
    $ player_passed = False # becomes true once player passed, after that he cannot throw dices any longer
    $ ai_passed = False # same for the opponent
    # technically, they also become true once score is 21 or higher since it's useless to continue; but we don't show it in gui
    show screen city_tavern_dicing
    with dissolve
    python:
        dice_1 = []
        dice_2 = []
        while len(dice_1) < 2: # both sides throw 2 dices in the beginning
            dice_1.append(throw_a_normal_dice())
        while len(dice_2) < 2:
            dice_2.append(throw_a_normal_dice())


label city_tavern_play_show_dice:
    show screen city_tavern_show_dices(dice_1, dice_2)
    if not(ai_passed and player_passed):
        play events "events/dice_" + str(randint(1, 3)) +".mp3"
    pause 0.4
    $ d_1 = sum(dice_1) # we use separate values to delay calculation and thus numbers update until dices alt is finished
    $ d_2 = sum(dice_2)
    show screen city_tavern_show_status(d_1, d_2) 
    with dissolve
    if sum(dice_1) == 21:
        $ ai_passed = True
    if sum(dice_2) == 21:
        $ player_passed = True
    if sum(dice_2) > 21 or sum(dice_1) > 21:
        $ ai_passed = player_passed = True
    if ai_passed and player_passed:
        hide screen city_tavern_dicing # we need to hide controls screen immediately after the game ends, or it still be available when it shouldn't be already
        if sum(dice_1) > 21 and sum(dice_2) <= 21:
            $ game_outcome = 1
        elif sum(dice_2) > 21 and sum(dice_1) <= 21:
            $ game_outcome = -1
        elif sum(dice_2) > 21 and sum(dice_1) > 21:
            $ game_outcome = 0
        elif sum(dice_2) == 21 and sum(dice_1) == 21:
            $ game_outcome = 0
        elif sum(dice_2) == sum(dice_1):
            $ game_outcome = 0
        elif sum(dice_2) > sum(dice_1):
            $ game_outcome = 1
        else:
            $ game_outcome = -1
        if game_outcome == -1:
            $ hero.take_money(city_tavern_current_dice_bet)
            $ narrator ("You lost!")
        elif game_outcome == 0:
            $ narrator ("It's a draw! You break even.")
        else:
            if hero.gold >= city_tavern_current_dice_bet*2:
                menu:
                    "You won! You can take your money right now or double your bet if you feeling lucky."
                    "Take the money":
                        $ hero.add_money(city_tavern_current_dice_bet)
                    "Double the bet":
                        $ city_tavern_current_dice_bet *= 2
                        hide screen city_tavern_show_dices
                        jump city_tavern_play_dice_another_round
            else:
                "You won!"
                $ hero.add_money(city_tavern_current_dice_bet)
        hide screen city_tavern_show_dices
        with dissolve
        jump city_tavern_menu
    elif sum(dice_2) == 21:
        jump city_tavern_throw_dice
    else:
        show screen city_tavern_dicing()
        while 1:
            $ result = ui.interact()
            
label city_tavern_throw_dice:
    if not(player_passed):
        $ dice_2.append(throw_a_normal_dice())
        if check_if_should_throw_dice(sum(dice_1), sum(dice_2), player_passed) and not(ai_passed):
            $ dice_1.append(throw_a_normal_dice())
        else:
            $ ai_passed = True
    else:
        while (check_if_should_throw_dice(sum(dice_1), sum(dice_2), player_passed) and not(ai_passed)):
            $ dice_1.append(throw_a_normal_dice())
        $ ai_passed = True
    jump city_tavern_play_show_dice

screen tavern_inside():

    use top_stripe(True)

    use location_actions("tavern_inside")
