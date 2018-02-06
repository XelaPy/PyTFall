init python:
    register_event("peevish_meeting", locations=["forest_entrance"], simple_conditions=["hero.magic >= 50"],  priority=500, start_day=1, jump=True, dice=100, max_runs=1)

label peevish_meeting:
    $ p = Character("???", color=lawngreen, what_color=lawngreen, show_two_window=True)

    stop world

    hide screen forest_entrance
    with dissolve

    show bg forest_entrance:
        size (config.screen_width, config.screen_height)
        crop (0, 0, config.screen_width, config.screen_height)
        easein 4.0 crop (100, 100, config.screen_width/4, 200)

    play sound "content/sfx/sound/events/get.mp3" fadein 1.0

    $ renpy.pause(5.0, hard=True)

    show expression npcs["Peevish"].get_vnsprite() as peevish
    with dissolve

    play world "irish.mp3" fadein 2.0
    # with vpunch
    p "Hello dumbass!"
    p "Wow. Can you see me? There aren't many who can!"
    extend " Like that old crone living up that damn hobbit hole..."

    p "I am the great and powerful Peevish McSpud!"

    $ p = npcs["Peevish"].say

    menu:
        "Old crone? That witch looks young and kinda hot?":
            p "Haha! Shows how much you know!"
            p "Let me get down from here."
        "Hey! Are you the midget who lives up in a tree?":
            p "Amn't!"
            p "I am a genuine leprechaun!"
            extend " Well... almost. I wish that I had that damn pile of gold under the rainbow..."
            p "But the rest of me is 100%% you mother-frecker! Just wait till I come down there!" #not swearing on purpose?

    hide peevish
    hide bg forest_entrance
    show bg forest_entrance
    with dissolve

    show expression npcs["Peevish"].get_vnsprite() as peevish:
        pos (0.4, 0.2)
        linear 1.0 pos (0.4, 0.25)
        linear 1.0 pos (0.4, 0.2)
        repeat
    with dissolve

    p "Haha, you're a lot uglier from this angle!"
    p "But you're in luck today! Since you can see me, you aren't entirely hopeless..."
    extend " and I just happen to teach {color=[tan]}Earth{/color} and {color=[blue]}Water{/color} magic!"
    p "Normally I wouldn't bother with a shitty pipsqueak like you, but my greatness requires a good pile of {color=[gold]}gold{/color} to become a real genuine and authentic leprechaun."
    p "I could use a rainbow too..."
    p "Well, don't expect it to be cheap!"
    extend " Talk to me when you have some G's on you!"

    $ global_flags.set_flag("met_peevish")
    $ global_flags.del_flag("keep_playing_music")
    jump forest_entrance

label peevish_menu:
    $ p = npcs["Peevish"].say

    hide screen forest_entrance
    show expression npcs["Peevish"].get_vnsprite() as peevish:
        pos (0.4, 0.2)
        linear 1.0 pos (0.4, 0.25)
        linear 1.0 pos (0.4, 0.2)
        repeat
    with dissolve

    p "Haha, look who's back!"
    p "Got some gold on ya?"
    $ peevish_shop = ItemShop("Peevish Shop", 18, ["Peevish Shop"], gold=5000, sells=["scroll"], sell_margin=0.25, buy_margin=5.0)

    p "Well? What do you want?"
    python:
        focus = False
        item_price = 0
        filter = "all"
        amount = 1
        shop = pytfall.peevish_shop
        shop.inventory.apply_filter(filter)
        char = hero
        char.inventory.set_page_size(18)
        char.inventory.apply_filter(filter)
    show screen shopping(left_ref=hero, right_ref=shop)
    with dissolve
    call shop_control
    hide screen shopping
    with dissolve

    p "Come back when you have more {color=[gold]}gold{/color}!"
    if not global_flags.has_flag("revealed_aine_location"):
        p "Oh! Before I forget!"
        p "I have a goodie, goodie sis that usually hangs around the park area. She is magical too so you might not be able to see her until you train up a bit..."
        p "Sure wish you weren't such a wuss..."
        extend " Now you can get the hell out of here!"
        $ global_flags.set_flag("revealed_aine_location")
    hide peevish with dissolve
    $ global_flags.set_flag("keep_playing_music")
    jump forest_entrance
