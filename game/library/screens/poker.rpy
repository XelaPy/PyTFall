##### dice poker logic:            
label city_tavern_play_poker_another_round: # additional rounds continue from here
label wot:
    $ player_passed = False # becomes true once player passed, after that he cannot throw dices any longer
    $ ai_passed = False # same for the opponent

    python:
        dice_1 = []
        dice_2 = []
        selected_dice = [] # numbers of selected by player dices - go from 1 to 5
        while len(dice_1) < 5: # both sides throw 5 dices in the beginning
            dice_1.append(throw_a_normal_dice())
        while len(dice_2) < 5:
            dice_2.append(throw_a_normal_dice())
            
label city_tavern_show_poker_dices_loop:
            
    show screen city_tavern_show_poker_dices(dice_1, dice_2)
    while 1:
        $ result = ui.interact()
        if result not in selected_dice:
            $ selected_dice.append(result)
        else:
            $ selected_dice.remove(result)
        show screen city_tavern_show_poker_dices(dice_1, dice_2)
        

        
screen city_tavern_show_poker_dices(dice_1, dice_2): # main poker screen, shows dices themselves as imagebuttons
    on "show":
        action Show("city_tavern_show_poker_status", dissolve)
    on "hide":
        action Hide("city_tavern_show_poker_status")

    hbox:
        align .5, .4
        spacing 5
        box_reverse True
        for i in dice_1:
            $ img = "content/events/tavern_dice/"+str(i)+".png"
            # add "content/events/tavern_dice/"+str(i)+".png" at dice_roll_from_left()
            imagebutton:
                idle img
                action None 
    hbox:
        align .5, .6
        spacing 5
        $ number = 0 # since dices could have the same value, we cannot use index() here to return the number of selected dice in the list; so there will be artificial counter
        for i in dice_2:
            $ number += 1
            $ img = "content/events/tavern_dice/"+str(i)+".png"
            # add "content/events/tavern_dice/"+str(i)+".png" at dice_roll_from_right()
            if number not in selected_dice:
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
            text "Shuffle" size 15
        button:
            xysize (120, 40)
            yalign 0.5
            action [Hide("city_tavern_show_poker_dices")]
            text "Exit" size 15
            
label city_tavern_show_poker_shuffle:
    if selected_dice:
        python:
            for i in selected_dice:
                dice_2[i-1] = throw_a_normal_dice()
    $ selected_dice = []
    jump city_tavern_show_poker_dices_loop
    
    
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
