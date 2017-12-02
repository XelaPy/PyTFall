init python:
    register_event("aine_menu", locations=["city_park"],
        simple_conditions=["global_flags.flag('met_peevish')", "hero.magic >= 100"],
        priority=100, start_day=1, jump=True, dice=100, max_runs=1)

label aine_menu:

    $ a = npcs["Aine"].say

    hide screen city_park
    show expression npcs["Aine"].get_vnsprite() as aine:
        pos (.4, .2)
        linear 1.0 pos (.4, .25)
        linear 1.0 pos (.4, .2)
        repeat
    with dissolve

    if not global_flags.flag("met_aine"):
        $ global_flags.set_flag("met_aine")

        a "Well now, a magic practitioner... "
        extend " Hello dear, I am Aine!"

        menu:
            "A leprechaun? In the park?":
                a "How Rude! I go wherever I please, and I can take care of myself!"
                a "Not mentioning that this is a really nice place and very few people can see me!"
            "I've met someone called Peevish...":
                a "That rude, good for nothing, useless excuse for a brother... well, you don't get to choose family..."

        a "I can teach you {color=[lightblue]}Ice{/color} and {color=[yellow]}Electricity{/color} spells if you're interested,"
        extend " it will cost you, but you'll never have to hear a word about no pile of gold from me."
    else:
        a "Hello again. How are you today?"

label aine_menu_return:
    show screen aine_screen
    with dissolve
    while 1:
        $ result = ui.interact()

label aine_shop:
    a "Of course!"
    python:
        aine_shop = ItemShop("Aine Shop", 18, ["Aine Shop"], gold=5000, sells=["scroll"], sell_margin=0.25, buy_margin=5.0)
        focus = False
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.aine_shop
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter(filter)
    show screen shopping(left_ref=hero, right_ref=shop)
    with dissolve
    call shop_control
    hide screen shopping
    with dissolve
    a " Come back with more gold!"
    jump aine_menu_return

label aine_training:
    if not global_flags.has_flag("aine_training_explained"):
        call about_aine_personal_training
        $ global_flags.set_flag("aine_training_explained")
    else:
        a "Let's see what I can do, dear."

    if len(hero.team) > 1:
        call screen character_pick_screen
        $ char = _return
    else:
        $ char = hero

    if not char:
        jump aine_menu_return
    $ loop = True

    while loop:
        menu:
            "About training sessions":
                call about_personal_training
            "About Aine training":
                call about_aine_personal_training
            "{color=[green]}Setup sessions for [char.name]{/color}" if not char.has_flag("train_with_aine"):
                $ char.set_flag("train_with_aine")
                $ char.apply_trait(traits["Aine Training"])
                $ training_price = char.get_training_price()
                a "It will require [training_price] gold per day. Don't you dare misuse skills you've learned here!"
            "{color=[red]}Cancel sessions for [char.name]{/color}" if char.flag("train_with_aine"):
                $ char.del_flag("train_with_aine")
                $ char.remove_trait(traits["Aine Training"])
                a "Fair enough."
            "Pick another character" if len(hero.team) > 1:
                call screen character_pick_screen
                if _return:
                    $ char = _return
            "Do Nothing":
                $ loop = False
    jump aine_menu_return

label about_personal_training:
    "You can arrange for daily training sessions at the cost of 1 AP and 500 gold pare day, plus 500 gold per 5 levels."
    "It will be automatically terminated if you lack the gold to continue."
    "Sessions can be arranged with multiple trainers on the same day. But you'd be running a risk of not leaving AP to do anything else."
    return

label about_aine_personal_training:
    a "Well dear, I can teach you manners and proper care so to increase your charisma."
    a "Being thought by a leprechaun Princess has its perks!"
    a "Your vitality will be boosted, and your fame and reputation may also increase."
    extend " Due to my magical nature, there is a tiny chance that you will get luckier in your life endeavors!!!"
    a "That I dare say is a truly rare feat!"
    return

label aine_goodbye:
    a "Good luck!"
    $ global_flags.set_flag("keep_playing_music")
    hide aine with dissolve
    jump city_park

screen aine_screen:
    frame:
        xalign 0.95
        ypos 20
        background Frame(Transform("content/gfx/frame/p_frame5.png", alpha=0.98), 10, 10)
        xpadding 10
        ypadding 10
        vbox:
            style_group "wood"
            align (0.5, 0.5)
            spacing 10
            button:
                xysize (150, 40)
                yalign 0.5
                action [Hide("aine_screen"), Jump("aine_shop")]
                text "Spells" size 15
            button:
                xysize (150, 40)
                yalign 0.5
                action [Hide("aine_screen"), Jump("aine_training")]
                text "Training" size 15
            button:
                xysize (150, 40)
                yalign 0.5
                action [Hide("aine_screen"), Jump("aine_goodbye")]
                text "Leave" size 15
