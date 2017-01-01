##### dice poker logic:            
label city_tavern_play_poker_another_round: # additional rounds continue from here
label wot:
    $ player_passed = False # becomes true once player passed, after that he cannot throw dices any longer
    $ ai_passed = False # same for the opponent

    python:
        dice_1 = []
        dice_2 = []
        selected_dice = 0 # number of selected by player dice - goes from 1 to 5; 0 means no selected
        selected_ai_dice = 0 # same for ai
        while len(dice_1) < 5: # both sides throw 5 dices in the beginning
            dice_1.append(throw_a_normal_dice())
        while len(dice_2) < 5:
            dice_2.append(throw_a_normal_dice())
            
label city_tavern_show_poker_dices_loop:
    hide drunkards with dissolve
    show screen city_tavern_show_poker_dices(dice_1, dice_2)
    play events "events/dice_" + str(randint(1, 3)) +".mp3"
    while 1:
        $ result = ui.interact()
        if result != selected_dice:
            $ selected_dice = result
        else:
            $ selected_dice = 0
        show screen city_tavern_show_poker_dices(dice_1, dice_2)
        

        
screen city_tavern_show_poker_dices(dice_1, dice_2): # main poker screen, shows dices themselves as imagebuttons
    on "show":
        action Show("city_tavern_show_poker_status", dissolve)
    on "hide":
        action Hide("city_tavern_show_poker_status")

    hbox:
        align .5, .4
        spacing 5
        $ number = 0
        for i in dice_1:
            $ number += 1
            $ img = "content/events/tavern_dice/"+str(i)+".png"
            # add "content/events/tavern_dice/"+str(i)+".png" at dice_roll_from_left()
            if number != selected_ai_dice:
                imagebutton:
                    idle img
                    action None 
            else:
                imagebutton:
                    idle im.Recolor(img, 0, 255, 0, 255)
                    action None 
    hbox:
        align .5, .6
        spacing 5
        $ number = 0 # since dices could have the same value, we cannot use index() here to return the number of selected dice in the list; so there will be artificial counter
        for i in dice_2:
            $ number += 1
            $ img = "content/events/tavern_dice/"+str(i)+".png"
            # add "content/events/tavern_dice/"+str(i)+".png" at dice_roll_from_right()
            if number != selected_dice:
                imagebutton:
                    idle img
                    hover (im.MatrixColor(img, im.matrix.brightness(0.15)))
                    action Return(number)
            else:
                imagebutton:
                    idle im.Recolor(img, 0, 255, 0, 255)
                    hover (im.MatrixColor(im.Recolor(img, 0, 255, 0, 255), im.matrix.brightness(0.15)))
                    action Return(number)
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
            action [Hide("city_tavern_show_poker_dices"), Jump("tavern_town")]
            text "Give Up" size 15
            
label city_tavern_show_poker_shuffle:
    $ selected_ai_dice = dice_poker_ai_decision(dice_1, dice_2)
    if selected_ai_dice not in [1, 2, 3, 4, 5]:
        $ selected_ai_dice = 0
    show screen city_tavern_show_poker_dices(dice_1, dice_2)
    pause 1.0
    if selected_dice != 0 or selected_ai_dice != 0:
        play events "events/dice_" + str(randint(1, 3)) +".mp3"
        if selected_dice != 0:
            $ dice_2[selected_dice-1] = throw_a_normal_dice()
            $ selected_dice = 0
        if selected_ai_dice != 0:
            $ dice_1[selected_ai_dice-1] = throw_a_normal_dice()
            $ selected_ai_dice = 0
    show screen city_tavern_show_poker_dices(dice_1, dice_2)

    if dice_poker_decide_winner(dice_1, dice_2) == 1:
        $ narrator("You lost!")
    elif dice_poker_decide_winner(dice_1, dice_2) == 2:
        $ narrator("You won!")
    else:
        $ narrator("It's a draw!")
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
