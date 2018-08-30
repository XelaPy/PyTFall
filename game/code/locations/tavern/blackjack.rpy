##### dice blackjack logic:
screen city_tavern_show_status(d_1, d_2): # additional screen, shows all info related to the dice game
    frame:
        xalign .05
        yalign .05
        xysize (90, 90)
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            xalign .5
            yalign .5
            hbox:
                text str(d_1) xalign .98 style "stats_value_text" color gold
                xalign .5
            hbox:
                if ai_passed and d_1 < 21:
                    text ("Pass") xalign .98 style "stats_value_text" color gold
                elif d_1 > 21:
                    text ("Lost") xalign .98 style "stats_value_text" color gold
                elif d_1 == 21:
                    text ("Score!") xalign .98 style "stats_value_text" color gold
                else:
                    text (" ") xalign .98 style "stats_value_text" color gold
                xalign .5
    frame:
        xalign .05
        yalign .95
        xysize (90, 90)
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            xalign .5
            yalign .5
            hbox:
                text str(d_2) xalign .98 style "stats_value_text" color gold
                xalign .5
            hbox:
                if player_passed and d_2 < 21:
                    text ("Pass") xalign .98 style "stats_value_text" color gold
                elif d_2 > 21:
                    text ("Lost") xalign .98 style "stats_value_text" color gold
                elif d_2 == 21:
                    text ("Score!") xalign .98 style "stats_value_text" color gold
                else:
                    text (" ") xalign .98 style "stats_value_text" color gold
                xalign .5

    frame:
        xalign .5
        yalign .05
        xysize (120, 120)
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
        xpadding 1
        ypadding 1
        vbox:
            xalign .5
            add "content/gfx/interface/images/tavern_gold.png"
            text str(city_tavern_current_dice_bet) xalign .5 style "stats_value_text" color gold

screen city_tavern_show_dices(dice_1, dice_2): # main dice screen, shows dices themselves
    on "hide":
        action Hide("city_tavern_show_status")
    hbox:
        align .55, .4
        spacing 5
        box_reverse True
        for i in dice_1:
            add "content/events/tavern_dice/"+str(i)+".webp" at dice_roll_zooming()
    hbox:
        align .55, .6
        spacing 5
        for i in dice_2:
            add "content/events/tavern_dice/"+str(i)+".webp" at dice_roll_zooming()

label tavern_dice_pass: # player passes, and cannot throw dices anymore
    $ player_passed = True
    jump city_tavern_throw_dice

label city_tavern_play_dice: # starting the dice game
    if not global_flags.flag('played_dice_in_tavern'):
        $ global_flags.set_flag('played_dice_in_tavern')
        "The goal of the game is to reach a final score higher than the opponent without exceeding 21 or let the opponent throw dices until his score exceeds 21."
    if 'Drunk' in hero.effects: # dizzy screen does not look good with dices animation...
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
    pause .4
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
            $ hero.take_money(city_tavern_current_dice_bet, reason="Tavern")
            $ narrator ("You lost!")
        elif game_outcome == 0:
            $ narrator ("It's a draw! You break even.")
        else:
            if hero.gold >= city_tavern_current_dice_bet*2:
                menu:
                    "You won! You can take your money right now or double your bet if you are feeling lucky."
                    "Take the money":
                        $ hero.add_money(city_tavern_current_dice_bet, reason="Tavern")
                    "Double the bet":
                        $ city_tavern_current_dice_bet *= 2
                        hide screen city_tavern_show_dices
                        jump city_tavern_play_dice_another_round
            else:
                "You won!"
                $ hero.add_money(city_tavern_current_dice_bet, reason="Tavern")
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

screen city_tavern_dicing(): # dice game controls menu
    frame:
        xalign .95
        ypos 50
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_group "wood"
            align (.5, .5)
            spacing 10
            button:
                xysize (120, 40)
                yalign .5
                action [Jump("city_tavern_throw_dice")]
                text "Throw dice" size 15
            button:
                xysize (120, 40)
                yalign .5
                action [Jump("tavern_dice_pass")]
                text "Pass" size 15
            button:
                xysize (120, 40)
                yalign .5
                action [Jump("city_tavern_dices_give_up")]
                text "Give up" size 15

label city_tavern_dices_give_up:
    $ hero.take_money(city_tavern_current_dice_bet, reason="Tavern")
    hide screen city_tavern_dicing
    hide screen city_tavern_show_dices
    with dissolve
    jump city_tavern_menu
