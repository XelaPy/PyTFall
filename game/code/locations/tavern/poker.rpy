##### dice poker logic:
label city_tavern_play_poker: # additional rounds continue from here
    if not global_flags.flag('played_poker_in_tavern'):
        $ global_flags.set_flag('played_poker_in_tavern')
        "The goal of the game is to get a better hand than the opponent. The best hand is all five dice showing the same value, and the worst scoring one is one pair. In case of draw wins the one with higher overall dice value. Optionally, after the initial throw, you and your opponent can choose one dice to throw again in hopes to get a better hand."
    if 'Drunk' in hero.effects: # dizzy screen does not look good with dices animation...
        "You are too drunk for games at the moment."
        jump city_tavern_menu
    elif hero.gold < city_tavern_dice_bet:
        "Sadly, you don't have enough money to make a bet."
        jump city_tavern_menu

    python:
        dice_1 = []
        dice_2 = []
        selected_dice = 0 # number of selected by player dice - goes from 1 to 5; 0 means no selected
        selected_ai_dice = 0 # same for ai
        city_tavern_current_dice_bet = city_tavern_dice_bet

label city_tavern_show_poker_dices_start:
    hide drunkards with dissolve
    hide screen city_tavern_show_poker_dices
    python:
        dice_1 = [throw_a_normal_dice() for i in range(5)]
        dice_2 = [throw_a_normal_dice() for i in range(5)]
        rerolls = 0 # we allow to change a dice twice; there could be more complicated rules in the future
    play events "events/dice_" + str(randint(1, 3)) +".mp3"
    show screen city_tavern_show_poker_dices_controls
    show screen city_tavern_show_poker_dices(dice_1, dice_2, dice_roll_zooming, dice_roll_zooming)

label city_tavern_show_poker_dices_loop:
    while 1:
        $ result = ui.interact()
        $ selected_dice = 0 if selected_dice == result else result
        show screen city_tavern_show_poker_dices(dice_1, dice_2, dice_roll_null, dice_roll_unzooming)

screen city_tavern_show_poker_dices(dice_1, dice_2, atl, selected_atl): # main poker screen, shows dices themselves as imagebuttons
    on "show":
        action Show("city_tavern_show_poker_status", dissolve)
    on "hide":
        action Hide("city_tavern_show_poker_status")
    # default atl = dice_roll_unzooming(uniform(.9999, .99999))

    fixed:
        pos 430, 230
        $ xpos = 0
        for index, d in enumerate(dice_1):
            $ index += 1
            python:
                img = "content/events/tavern_dice/"+str(d)+".webp"
                if index != selected_ai_dice:
                    idle_bg = img
                    hover_bg = im.MatrixColor(img, im.matrix.brightness(.10))
                else:
                    idle_bg = im.MatrixColor(img, im.matrix.tint(.0, 1.0, 1.0))
                    hover_bg = im.MatrixColor(idle_bg, im.matrix.brightness(.10))

            imagebutton:
                xpos xpos
                anchor (.5, .5)
                if index == selected_ai_dice:
                    at selected_atl(-150)
                else:
                    at atl
                idle idle_bg
                # hover hover_bg
                action None
            $ xpos += 105

    fixed:
        pos 430, 430
        $ xpos = 0
        for index, d in enumerate(dice_2):
            $ index += 1
            python:
                img = "content/events/tavern_dice/"+str(d)+".webp"
                if index != selected_dice:
                    idle_bg = img
                    hover_bg = im.MatrixColor(img, im.matrix.brightness(.10))
                else:
                    idle_bg = im.MatrixColor(img, im.matrix.tint(.0, 1.0, 1.0))
                    hover_bg = im.MatrixColor(idle_bg, im.matrix.brightness(.10))

            imagebutton:
                xpos xpos
                anchor (.5, .5)
                if index == selected_dice:
                    at selected_atl(150)
                else:
                    at atl
                idle idle_bg
                hover hover_bg
                action Return(index)
            $ xpos += 105

screen city_tavern_show_poker_dices_controls:
    vbox:
        style_group "wood"
        align (.9, .9)
        button:
            xysize (120, 40)
            yalign .5
            action [Jump("city_tavern_show_poker_shuffle")]
            text "Next" size 15
        button:
            xysize (120, 40)
            yalign .5
            action [Hide("city_tavern_show_poker_dices"), Jump("city_tavern_poker_give_up")]
            text "Give Up" size 15

transform dice_roll_zooming(x):
    subpixel True
    anchor (.5, .5)
    zoom 0
    easein_back .75 zoom 1.0

transform dice_roll_unzooming(x):
    subpixel True
    anchor (.5, .5)
    zoom 0
    easein_bounce .75 zoom 1.0

transform dice_roll_change(x):
    subpixel True
    anchor (.5, .5) yoffset 0
    zoom 1.0 rotate 0
    easein_bounce .5 zoom .4 yoffset x rotate 3600
    easein_back .5 zoom 1.0 yoffset 0 rotate 0

transform dice_roll_null(x):
    subpixel True
    anchor (.5, .5)

label city_tavern_poker_give_up:
    $ hero.take_money(city_tavern_current_dice_bet, reason="Tavern")
    hide screen city_tavern_show_poker_dices
    hide screen city_tavern_show_poker_dices_controls
    with dissolve
    jump city_tavern_menu

label city_tavern_show_poker_shuffle:
    $ selected_ai_dice = dice_poker_ai_decision(dice_1, dice_2) # ai selects a dice it wants to change
    show screen city_tavern_show_poker_dices(dice_1, dice_2, dice_roll_null, dice_roll_change) # and we show selected by player and ai dices for a second
    $ rerolls += 1
    if selected_dice != 0 or selected_ai_dice != 0:
        $ renpy.pause(1.0, hard=True)
        play events "events/dice_" + str(randint(1, 3)) +".mp3"
        if selected_dice != 0:
            $ dice_2[selected_dice-1] = throw_a_normal_dice()
        if selected_ai_dice != 0:
            $ dice_1[selected_ai_dice-1] = throw_a_normal_dice()
    $ selected_dice = selected_ai_dice = 0
    show screen city_tavern_show_poker_dices(dice_1, dice_2, dice_roll_null, dice_roll_null) # then we reroll selected dices and show new dice sets
    if rerolls < 2:
        jump city_tavern_show_poker_dices_loop

    hide screen city_tavern_show_poker_dices_controls
    if dice_poker_decide_winner(dice_1, dice_2) == 1:
        $ narrator("You lost!")
        $ hero.take_money(city_tavern_current_dice_bet, reason="Tavern")
    elif dice_poker_decide_winner(dice_1, dice_2) == 2:
        if hero.gold >= city_tavern_current_dice_bet*2:
            menu:
                "You won! You can take your money right now or double your bet if you are feeling lucky."
                "Take the money":
                    $ hero.add_money(city_tavern_current_dice_bet, reason="Tavern")
                "Double the bet":
                    $ city_tavern_current_dice_bet *= 2
                    hide screen city_tavern_show_dices
                    jump city_tavern_show_poker_dices_start
        else:
            $ narrator("You won!")
            $ hero.add_money(city_tavern_current_dice_bet, reason="Tavern")
    else:
        $ narrator("It's a draw! You break even.")
    hide screen city_tavern_show_poker_dices
    jump city_tavern_menu

screen city_tavern_show_poker_status(): # additional screen, shows all info related to the dice game
    frame:
        xalign .05
        yalign .05
        xysize (120, 120)
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
        vbox:
            xalign .5
            yalign .5
            if dice_poker_decide_winner(dice_1, dice_2) == 1:
                add "content/gfx/interface/images/poker_winner.png" xalign .5
                spacing 5
            $ result = dice_poker_calculate(dice_1)[0]
            text result xalign .98 style "stats_value_text" color gold size 12
    frame:
        xalign .05
        yalign .95
        xysize (120, 120)
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=.98), 10, 10)
        vbox:
            xalign .5
            yalign .5
            if dice_poker_decide_winner(dice_1, dice_2) == 2:
                add "content/gfx/interface/images/poker_winner.png" xalign .5
                spacing 5
            $ result = dice_poker_calculate(dice_2)[0]
            text result xalign .98 style "stats_value_text" color gold size 12
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
