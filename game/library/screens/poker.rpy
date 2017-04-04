##### dice poker logic:            
label city_tavern_play_poker: # additional rounds continue from here
    if not global_flags.flag('played_poker_in_tavern'):
        $ global_flags.set_flag('played_poker_in_tavern')
        "The goal of the game is to get a better hand than opponent. The best hand is all five dice showing the same value, and the worst scoring one is one pair. In case of draw wins the one with higher overall dice value. Optionally, after initial throw you and your opponent can choose one dice to throw again in hopes to get a better hand."
    if hero.effects['Drunk']['active']: # dizzy screen does not look good with dices animation...
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
            
label city_tavern_show_poker_dices_loop:
    hide drunkards with dissolve
    hide screen city_tavern_show_poker_dices
    python:
        dice_1 = []
        dice_2 = []
        rerolls = 0 # we allow to change a dice twice; there could be more complicated rules in the future
        while len(dice_1) < 5: # both sides throw 5 dices in the beginning
            dice_1.append(throw_a_normal_dice())
        while len(dice_2) < 5:
            dice_2.append(throw_a_normal_dice())
    show screen city_tavern_show_poker_dices_controls
    show screen city_tavern_show_poker_dices(dice_1, dice_2, False)
    play events "events/dice_" + str(randint(1, 3)) +".mp3"
    
label city_tavern_show_poker_dices_loop_continue:
    while 1:
        $ result = ui.interact()
        if result != selected_dice:
            $ selected_dice = result
        else:
            $ selected_dice = 0
        show screen city_tavern_show_poker_dices(dice_1, dice_2, False)
        
screen city_tavern_show_poker_dices(dice_1, dice_2, shuffle): # main poker screen, shows dices themselves as imagebuttons; shuffle=True means we want to show all buttons but the selected one without alts
    on "show":
        action Show("city_tavern_show_poker_status", dissolve)
    on "hide":
        action Hide("city_tavern_show_poker_status")
    
    hbox:
        align .5, .4
        spacing 5
        $ number = 0
        if not shuffle:
            for i in dice_1:
                $ number += 1
                $ img = "content/events/tavern_dice/"+str(i)+".png"
                if number != selected_ai_dice:
                    imagebutton:
                        at dice_roll_zooming()
                        idle img
                        action None 
                else:
                    imagebutton:
                        idle im.Recolor(img, 0, 255, 0, 255)
                        action None
        else:
            for i in dice_1:
                $ number += 1
                $ img = "content/events/tavern_dice/"+str(i)+".png"
                if number != selected_ai_dice:
                    imagebutton:
                        idle img
                        action None 
                else:
                    imagebutton:
                        at dice_roll_unzooming()
                        idle img
                        action None
    hbox:
        align .5, .6
        spacing 5
        $ number = 0 # since dices could have the same value, we cannot use index() here to return the number of selected dice in the list; so there will be artificial counter
        if not shuffle:
            for i in dice_2:
                $ number += 1
                $ img = "content/events/tavern_dice/"+str(i)+".png"
                if number != selected_dice:
                    imagebutton:
                        at dice_roll_zooming()
                        idle img
                        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
                        action Return(number)
                else:
                    imagebutton:
                        idle im.Recolor(img, 0, 255, 0, 255)
                        hover (im.MatrixColor(im.Recolor(img, 0, 255, 0, 255), im.matrix.brightness(0.15)))
                        action Return(number)
        else:
            for i in dice_2:
                $ number += 1
                $ img = "content/events/tavern_dice/"+str(i)+".png"
                if number != selected_dice:
                    imagebutton:
                        idle img
                        hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
                        action Return(number)
                else:
                    imagebutton:
                        at dice_roll_unzooming()
                        idle img
                        hover (im.MatrixColor(im.Recolor(img, 0, 255, 0, 255), im.matrix.brightness(0.15)))
                        action Return(number)
                        
screen city_tavern_show_poker_dices_controls:
    vbox:
        style_group "wood"
        align (0.9, 0.9)
        button:
            xysize (120, 40)
            yalign 0.5
            action [Jump("city_tavern_show_poker_shuffle")]
            text "Next" size 15
        button:
            xysize (120, 40)
            yalign 0.5
            action [Hide("city_tavern_show_poker_dices"), Jump("city_tavern_poker_give_up")]
            text "Give Up" size 15
            
transform dice_roll_zooming():
    zoom 0
    easein_back 0.75 zoom 1
    
transform dice_roll_unzooming():
    zoom 0
    easein_bounce 0.75 zoom 1
            
label city_tavern_poker_give_up:
    $ hero.take_money(city_tavern_current_dice_bet)
    hide screen city_tavern_show_poker_dices
    with dissolve
    jump city_tavern_menu
            
label city_tavern_show_poker_shuffle:
    $ selected_ai_dice = dice_poker_ai_decision(dice_1, dice_2) # ai selects a dice it wants to change
    show screen city_tavern_show_poker_dices(dice_1, dice_2, False) # and we show selected by player and ai dices for a second
    $ rerolls += 1
    if selected_dice != 0 or selected_ai_dice != 0:
        pause 0.3
        play events "events/dice_" + str(randint(1, 3)) +".mp3"
        if selected_dice != 0:
            $ dice_2[selected_dice-1] = throw_a_normal_dice()
        if selected_ai_dice != 0:
            $ dice_1[selected_ai_dice-1] = throw_a_normal_dice()
    show screen city_tavern_show_poker_dices(dice_1, dice_2, True) # then we reroll selected dices and show new dice sets
    pause 0.6
    $ selected_dice = selected_ai_dice = 0
    if rerolls < 2:
        jump city_tavern_show_poker_dices_loop_continue
    
    hide screen city_tavern_show_poker_dices_controls
    if dice_poker_decide_winner(dice_1, dice_2) == 1:
        $ narrator("You lost!")
        $ hero.take_money(city_tavern_current_dice_bet)
    elif dice_poker_decide_winner(dice_1, dice_2) == 2:
        if hero.gold >= city_tavern_current_dice_bet*2:
            menu:
                "You won! You can take your money right now or double your bet if you feeling lucky."
                "Take the money":
                    $ hero.add_money(city_tavern_current_dice_bet)
                "Double the bet":
                    $ city_tavern_current_dice_bet *= 2
                    hide screen city_tavern_show_dices
                    jump city_tavern_show_poker_dices_loop
        else:
            $ narrator("You won!")
            $ hero.add_money(city_tavern_current_dice_bet)
    else:
        $ narrator("It's a draw! You break even.")
    hide screen city_tavern_show_poker_dices
    jump city_tavern_menu
    
screen city_tavern_show_poker_status(): # additional screen, shows all info related to the dice game
    frame:
        xalign 0.05
        yalign 0.05
        xysize (120, 120)
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        vbox:
            xalign 0.5
            yalign 0.5
            if dice_poker_decide_winner(dice_1, dice_2) == 1:
                add "content/gfx/interface/images/poker_winner.png" xalign 0.5
                spacing 5
            $ result = dice_poker_calculate(dice_1)[0]
            text result xalign 0.98 style "stats_value_text" color gold size 12
    frame:
        xalign 0.05
        yalign 0.95
        xysize (120, 120)
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        vbox:
            xalign 0.5
            yalign 0.5
            if dice_poker_decide_winner(dice_1, dice_2) == 2:
                add "content/gfx/interface/images/poker_winner.png" xalign 0.5
                spacing 5
            $ result = dice_poker_calculate(dice_2)[0]
            text result xalign 0.98 style "stats_value_text" color gold size 12
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