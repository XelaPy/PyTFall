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
                a "How Rude! I go wherever I please and I can take care of myself!"
                a "Not mentioning that this is a really nice place and very few people can see me!"
            "I've met someone called Peevish...":
                a "That rude, good for nothing, useless excuse for a brother... well, you don't get to choose family..."

        a "I can teach you {color=[lightblue]}Ice{/color} and {color=[yellow]}Electricity{/color} spells if you're interested,"
        extend " it will cost you but you'll never have to hear a word about no pile of gold from me."
    else:
        a "Hello again. How are you today?"


    $ loop = True
    while loop:
        menu:
            a "Anything interesting my dear?"
            "Ask her about spells":
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
                
            "Ask her to train you": # TODO: update training stuff
                if len(hero.team) > 1:
                    a "Who will it be?"
                    call screen character_pick_screen
                    $ char = _return
                else:
                    $ char = hero

                if not global_flags.has_flag("aine_training_explained"):
                    a "Well dear, I can teach you manners and proper care so to increase your charisma."
                    a "It will cost you 1000 (+1000 per 5 levels) Gold per training session."
                    a "Being thought by a leprechaun Princess has it's perks!"
                    a "You vitality will be boosted and your fame and reputation may also increase."
                    extend " Due to my magical nature, there is a really small chance that you will get luckier in your life endeavours!!!"
                    a "That I dare say is a truly rare feat!"
                    $ global_flags.set_flag("aine_training_explained")
                else:
                    a "I am ready if you are!"

                $ training_price = char.get_training_price()
                menu:
                    "Pay [training_price] Gold" if hero.AP > 0:
                        if hero.take_money(training_price, "Training"):
                            $ char.AP -= 1
                            $ char.auto_training("train_with_aine")
                            a "All done! Don't you dare misuse skills you've learned here!"
                        else:
                            a "Payment is still required I am afraid."
                            extend " It is only fair!"


                    "Maybe next time...":
                        $ pass
                $ del training_price

            "Schedule training sessions":
                if not global_flags.has_flag("training_sessions_explained"):
                    "Here you can arrange for daily training sessions at cost of 1AP and 1000 (+1000 per 5 levels) Gold per day."
                    "This will be automatically terminated if you lack the gold to continue."
                    "Sessions can be arranged with multiple trainers at the same day"
                    extend " however you'd be running a risk of not leaving AP to do anything else!"
                    $ global_flags.set_flag("training_sessions_explained")

                if len(hero.team) > 1:
                    "Pick a character!"
                    call screen character_pick_screen
                    $ char = _return
                else:
                    $ char = hero

                menu:
                    "Setup sessions" if not char.has_flag("train_with_aine"):
                        $ char.set_flag("train_with_aine")
                    "Cancel sessions" if char.flag("train_with_aine"):
                        $ char.del_flag("train_with_aine")
                    "Do Nothing...":
                        $ pass

            "Thanks for your time":
                $ loop = False

    a "Good luck!"
    $ global_flags.set_flag("keep_playing_music")
    hide aine with dissolve
    jump city_park