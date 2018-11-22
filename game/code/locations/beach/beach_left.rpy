label city_beach_left:
    $ gm.enter_location(goodtraits=["Athletic", "Dawdler"], badtraits=["Scars", "Undead", "Furry", "Monster"], curious_priority=False)
    $ coords = [[.15, .5], [.5, .45], [.7, .8]]
    # Music related:
    if not "beach_main" in ilists.world_music:
        $ ilists.world_music["beach_main"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("beach_main")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["beach_main"])
    $ global_flags.del_flag("keep_playing_music")

    python:
        # Build the actions
        if pytfall.world_actions.location("city_beach_left"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()

    scene bg city_beach_left
    show screen city_beach_left

    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")

    while 1:

        $ result = ui.interact()

        if result[0] == 'jump':
            $ gm.start_gm(result[1])

        if result[0] == 'control':
            if result[1] == 'return':
                $ global_flags.set_flag("keep_playing_music")
                hide screen city_beach_left
                jump city_beach


screen city_beach_left():

    use top_stripe(True)
    if not gm.show_girls:
        # Jump buttons:
        $img = ProportionalScale("content/gfx/interface/icons/beach_cafe.png", 80, 80)
        imagebutton:
            pos(380, 300)
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(.15)))
            action [Hide("city_beach_left"), Jump("city_beach_cafe_main")]
            tooltip "Beach Café"

        $ img = im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80)
        imagebutton:
            align (.99, .5)
            idle (img)
            hover (im.MatrixColor(img, im.matrix.brightness(.15)))
            action [Hide("city_beach_left"), Function(global_flags.set_flag, "keep_playing_music"), Jump("city_beach")]

        $ img_beach_fish = ProportionalScale("content/gfx/interface/icons/beach_fishing.png", 90, 90)
        imagebutton:
            pos(960, 400)
            idle (img_beach_fish)
            hover (im.MatrixColor(img_beach_fish, im.matrix.brightness(.15)))
            action [Hide("city_beach_left"), Jump("fishing_logic"), With(dissolve)]
            tooltip "Fishing Docks"


        $ img_beach_swim = ProportionalScale("content/gfx/interface/icons/beach_resting.png", 90, 90)
        imagebutton:
            pos(400, 545)
            idle (img_beach_swim)
            hover (im.MatrixColor(img_beach_swim, im.matrix.brightness(.15)))
            action [Hide("city_beach_left"), Jump("mc_action_city_beach_rest")]
            tooltip "Rest"

    use location_actions("city_beach_left")

    if gm.show_girls:
        key "mousedown_3" action ToggleField(gm, "show_girls")

        add "content/gfx/images/bg_gradient.webp" yalign .45

        $ j = 0
        for entry in gm.display_girls():
            hbox:
                align (coords[j])
                $ j += 1
                if not entry.flag("beach_left_tags") or entry.flag("beach_left_tags")[0] < day:
                    $ beach_left_tags_list = []
                    # main set
                    if entry.has_image("girlmeets","beach"):
                        $ beach_left_tags_list.append(("girlmeets","beach"))
                    if entry.has_image("girlmeets","swimsuit","simple bg"):
                        $ beach_left_tags_list.append(("girlmeets","swimsuit","simple bg"))
                    if entry.has_image("girlmeets","swimsuit","outdoors"):
                        $ beach_left_tags_list.append(("girlmeets","swimsuit","outdoors"))
                    # secondary set if nothing found
                    if not beach_left_tags_list:
                        if entry.has_image("girlmeets","outdoors"):
                            $ beach_left_tags_list.append(("girlmeets","outdoors"))
                        if entry.has_image("girlmeets","simple bg"):
                            $ beach_left_tags_list.append(("girlmeets","simple bg"))
                    # giveup
                    if not beach_left_tags_list:
                        $ beach_left_tags_list.append(("girlmeets"))

                    $ entry.set_flag("beach_left_tags", (day, choice(beach_left_tags_list)))

                use rg_lightbutton(img=entry.show(*entry.flag("beach_left_tags")[1], exclude=["urban", "wildness", "suburb", "nature", "winter", "night", "formal", "indoor", "indoors"], type="first_default", label_cache=True, resize=(300, 400), gm_mode=True),
                             return_value=['jump', entry])

label mc_action_city_beach_rest:
    show bg beach_rest with dissolve
    if hero.flag("rest_at_beach") == day:
        "You already relaxed at the beach today. Doing it again will lead to sunburns."
        jump city_beach_left
    $ hero.set_flag("rest_at_beach", value=day)

    python:
        picture = []
        if len(hero.team) > 1:
            for member in hero.team:
                if member != hero:
                    if member.has_image("rest", "beach", exclude=["sex", "stripping"]) and member.has_image("bathing", "beach", exclude=["sex", "stripping"]):
                        if dice(50):
                            picture.append(member.show("rest", "beach", exclude=["sex", "stripping"], type="reduce", resize=(600, 600)))
                        else:
                            picture.append(member.show("bathing", "beach", exclude=["sex", "stripping"], type="reduce", resize=(600, 600)))
                    elif member.has_image("rest", "beach", exclude=["sex", "stripping"]):
                        picture.append(member.show("rest", "beach", exclude=["sex", "stripping"], type="reduce", resize=(600, 600)))
                    elif member.has_image("bathing", "beach", exclude=["sex", "stripping"]):
                        picture.append(member.show("bathing", "beach", exclude=["sex", "stripping"], type="reduce", resize=(600, 600)))
                    elif member.has_image("bathing", "beach", exclude=["sex", "stripping"]):
                        picture.append(member.show("bathing", "beach", exclude=["sex", "stripping"], type="reduce", resize=(600, 600)))
                    elif member.has_image("beach", exclude=["sex", "stripping"]):
                        picture.append(member.show("beach", "sfw", exclude=["sex", "stripping"], type="reduce", resize=(600, 600)))
                    elif member.has_image("swimsuit", "simple bg", exclude=["sex", "stripping"]):
                        picture.append(member.show("swimsuit", "simple bg", exclude=["sex", "stripping"], type="reduce", resize=(600, 600)))
                    elif member.has_image("swimsuit", "no bg", exclude=["sex", "stripping"]):
                        picture.append(member.show("swimsuit", "simple bg", exclude=["sex", "stripping"], type="reduce", resize=(600, 600)))

    if len(picture) == 1:
        show expression picture[0] at truecenter as temp1
        with dissolve
    elif len(picture) == 2:
        show expression picture[0] at center_left as temp1
        show expression picture[1] at center_right as temp2
        with dissolve

    if len(hero.team) > 1:
        "You're relaxing at the beach with your team."
    else:
        "You're relaxing at the beach."

    $ members = list(x for x in hero.team if (x != hero and 'Horny' in x.effects and (check_lovers(x, hero) or x.disposition >= 500) and interactions_silent_check_for_bad_stuff(x)))
    if members:
        $ char = choice(members)
        hide temp1
        hide temp2
        # Further goes example of running sex scene from anywhere, DO NOT DELETE until it will be implemented elsewhere
        # $ sex_scene_location = "beach"
        # $ interactions_run_gm_anywhere(char, exit="city_beach_left", background="beach_rest", custom=True)

        # # Setup all the required globals:
        # python:
            # picture_before_sex = False
            # sex_scene_location = "beach"

        # hide temp1
        # hide temp2
        # show screen girl_interactions
        # with dissolve

        # jump interactions_sex_scene_begins

        show expression char.show("sex", "beach", exclude=["2c anal", "2c vaginal", "gay", "living", "group", "pool", "stage", "dungeon", "onsen"], type="reduce", resize=(600, 600)) at truecenter with dissolve
        "Unfortunately [char.name] forgot her sunscreen today, so you had no choice but to provide another liquid as a replacement."
        $ char.sex += 1
        $ hero.sex += 1
        $ char.disposition += 3

    python:
        for member in hero.team:
            member.vitality += randint(10, 15)
            if member != hero:
                member.disposition += 1
    jump city_beach_left

label fishing_logic_mor_quest_part:
    $ m = npcs["Mor"].say
    show expression npcs["Mor"].get_vnsprite() as npc
    if hero.flag("mor_fish_quest") != day: # no more than one quest per day
        if hero.get_skill("fishing") < 10:
            m "Yeah, I have special requests sometimes, but you need to learn something about fishing for a start. Practice a bit, ok?"
        else:
            if hero.flag("mor_fish_dice") != day: # no rerolling quest after asking again at the same day
                $ fish = list(i for i in items.values() if "Fishing" in i.locations and i.type == "fish" and 3 <= i.price <= hero.get_skill("fishing"))
                $ mor_fish = random.choice(fish)
                $ mor_quantity = locked_random("randint", 3, 10)
                $ hero.set_flag("mor_fish_dice", value = day)
            m "I need some [mor_fish.id]. About [mor_quantity] should be enough. Think you can handle it?"
            menu:
                "Yes":
                    m "Awesome!"
                    $ advance_quest("Fishery", "Mor asked you to catch some [mor_fish.id], about [mor_quantity] should be sufficient.", to=1, clear_logs=True)
                    $ hero.set_flag("mor_fish_quest", value = day)
                "No":
                    m "Your choice. You know where to find me."
    return

label fishing_logic_mor_dialogue:
    $ m = npcs["Mor"].say
    show expression npcs["Mor"].get_vnsprite() as npc
    with dissolve
    m "Hey, what's up?"
    menu Mor_dialogue_usual:
        "Fishing Requests" if pytfall.world_quests.check_stage("Fishery") != 1:
            if hero.flag("mor_fish_quest") != day: # no more than one quest per day
                call fishing_logic_mor_quest_part from _call_fishing_logic_mor_quest_part
            else:
                m "Sorry, I don't have anything else at the moment. Maybe tomorrow."
            jump Mor_dialogue_usual
        "Bring the Fish" if pytfall.world_quests.check_stage("Fishery") == 1 and has_items(mor_fish, [hero]) >= mor_quantity:
            $ hero.remove_item(mor_fish, mor_quantity)
            $ price = mor_fish.price * mor_quantity * 5
            $ hero.add_money(price, reason="Quests")
            m "Magnificent. Take your reward, [price] coins, and these baits. It's much more than any city merchant can give you, trust me."
            if dice(20):
                $ hero.add_item("Magic Bait", 3)
                "You've obtained 3 Magic Baits!"
            elif dice(40):
                $ hero.add_item("Good Bait", 6)
                "You've obtained 6 Good Baits!"
            else:
                $ hero.add_item("Simple Bait", 9)
                "You've obtained 9 Simple Baits!"
            $ finish_quest("Fishery", "You brought required fish to Mor and got your reward.", "complete")
            jump Mor_dialogue_usual
        "Buy a Fishing Pole (250G)" if hero.gold >= 250:
            $ hero.take_money(250, reason="Items")
            $ hero.add_item("Fishing Pole")
            m "Nice, there you go! Happy fishing!"
            jump Mor_dialogue_usual
        "Ask about fishing":
            m "Oh, it's very simple. You only need a fishing rod and good eyes."
            m "Of course, you also can try diving to find something good in the water, but trust me, it won't be easy."
            jump Mor_dialogue_usual
        "Ask about fishing skill":
            m "Your catch is as good as your fishing skills. Practice makes perfect, so be sure to fish a lot if want something valuable!"
            m "You won't catch anything useful at first, but don't let it discourage you."
            m "Besides, my dad sometimes drinks in the tavern with his friends, you can ask them for some tips."
            jump Mor_dialogue_usual
        "Ask about bait":
            m "You don't have to use bait. Fishing poles already have a basic lure attached. But the real thing can help a lot."
            m "They allow more attempts than usual, plus the chance to catch something amazing is higher."
            m "But the better the bait, the more skill it requires. You won't be able to use them if your skill is too low."
            m "The General Shop sells them sometimes. But really good bait is not so easy to find."
            jump Mor_dialogue_usual
        "That's all for now":
            m "Okay. Bye!"
            hide npc with dissolve

label fishing_logic:
    # during fishing itself only practical part of skill could be improved; theoretical part will be available via items and asking fishermen in tavern
    $ m = npcs["Mor"].say
    scene bg fishing_bg with dissolve

    if not global_flags.flag('visited_fish_city_beach'):
        $ create_quest("Fishery")
        show expression npcs["Mor"].get_vnsprite() as npc
        with dissolve
        "A small boy fishes on the pier. Noticing you, he puts his fishing rod on the ground and approaches."
        m "Hey there, stranger! It looks like it's your first time here. Would you like to buy a Fishing Pole?"
        m "We offer a discount for newbies, so it's only 250 coins!"
        menu Mor_dialogue:
            "Who are you?":
                m "Me? I'm Mor. I'm helping my father. He's a fisherman. He usually takes a boat to catch more fish, and I stay here."
                jump Mor_dialogue
            "Buy the Pole" if hero.gold >= 250:
                $ hero.take_money(250, reason="Items")
                $ hero.add_item("Fishing Pole")
                m "Nice, there you go! Happy fishing!"
                m "If you have any questions about fishing, I'm usually here."
            "Don't buy the Pole":
                m "Fine by me. But you won't find it cheaper! I'm usually here if you change your mind."
        $ global_flags.set_flag('visited_fish_city_beach')
        hide npc with dissolve
    menu beach_fighing_menu:
        "What do you want to do?"

        "Find Mor":
            jump fishing_logic_mor_dialogue
        "Check Mor requests" if pytfall.world_quests.check_stage("Fishery") != 1:
            if hero.flag("mor_fish_quest") != day: # no more than one quest per day
                call fishing_logic_mor_quest_part from _call_fishing_logic_mor_quest_part_1
            else:
                show expression npcs["Mor"].get_vnsprite() as npc
                with dissolve
                m "Sorry, I don't have anything else at the moment. Maybe tomorrow."
            hide npc with dissolve
            jump beach_fighing_menu
        "Bring the Fish" if pytfall.world_quests.check_stage("Fishery") == 1 and has_items(mor_fish, [hero]) >= mor_quantity:
            show expression npcs["Mor"].get_vnsprite() as npc
            with dissolve
            $ hero.remove_item(mor_fish, mor_quantity)
            $ price = mor_fish.price * mor_quantity + randint(2, 8)
            $ hero.add_money(price, reason="Quests")
            m "Magnificent. Take your reward, [price] coins, and these baits. It's much more than any city merchant can give you, trust me."
            if dice(20):
                $ hero.add_item("Magic Bait", 3)
                "You've obtained 3 Magic Baits!"
            elif dice(40):
                $ hero.add_item("Good Bait", 6)
                "You've obtained 6 Good Baits!"
            else:
                $ hero.add_item("Simple Bait", 9)
                "You've obtained 9 Simple Baits!"
            $ finish_quest("Fishery", "You brought required fish to Mor and got your reward.", "complete")
            hide npc with dissolve
            jump beach_fighing_menu
        "Try Fishing (-1 AP)":
            jump mc_action_beach_start_fishing
        "Nothing":
            jump city_beach_left

label mc_action_beach_start_fishing:
    if not has_items("Fishing Pole", [hero], equipped=True):
        "You don't have a fishing rode at the moment. Try to get one from local shops."
        jump city_beach_left
    elif hero.AP <= 0:
        "You don't have Action Points left. Try again tomorrow."
        jump city_beach_left
    else:
        $ min_fish_price = 0
        $ fishing_attempts = 3

        # bites increase min price of available items;
        # bites increase min price of available items; they are useless if skill is too low
        # so they only can be used with more or less high skillthey are useless if skill
        # is too low so they only can be used with more or less high skill
        python:
            c0 = (items["Simple Bait"] in hero.inventory and hero.get_skill("fishing") >= 30)
            c1 = (items["Good Bait"] in hero.inventory and hero.get_skill("fishing") >= 100)
            c2 = (items["Magic Bait"] in hero.inventory and hero.get_skill("fishing") >= 200)
            if any([c0, c1, c2]):
                use_baits = True
            else:
                use_baits = False

        if use_baits:
            menu:
                "Don't use any bait":
                    $ fishing_attempts = 3
                "Use Simple Bait" if c0:
                    $ min_fish_price += 10
                    $ hero.remove_item("Simple Bait")
                    $ fishing_attempts = 4
                "Use Good Bait" if c1:
                    $ min_fish_price += 50
                    $ hero.remove_item("Good Bait")
                    $ fishing_attempts = 5
                "Use Magic Bait" if c2:
                    $ min_fish_price += 100
                    $ hero.remove_item("Magic Bait")
                    $ fishing_attempts = 6
                "Cancel":
                    $ global_flags.set_flag("keep_playing_music")
                    jump city_beach_left

        $ hero.AP -= 1

        while fishing_attempts > 0:
            $ fishing_attempts -= 1
            python:
                # Get a list of fishing items player is skilled enough to fish out
                all_fish = list(i for i in items.values() if "Fishing" in i.locations and min_fish_price <= i.price <= hero.get_skill("fishing"))
                if all_fish:
                    selected_fish = random.sample(all_fish, min(9, len(all_fish)))
                else:
                    selected_fish = []

            if not selected_fish:
                $ hero.say("Must be one of those no-bite days...")
            else:
                call screen fishing_area(selected_fish)
                $ item = _return
                $ setattr(config, "mouse", None)

                if item == "Stop Fishing":
                    $ exit_string = "This is tiring, back to the beach!"
                    jump end_fishing
                else:
                    $ hero.add_item(item)
                    $ gfx_overlay.random_find(item, 'fishy')

                $ renpy.pause(.5, hard = True)
                pause .5

                # the less item's chance field, the more additional bonus to fishing;
                # with 90 chance it will be +1, with less than 1 chance about 10
                python hide:
                    temp = round_int((100-item.chance)*.1) + randint(1, 2)
                    hero.fishing += temp

label end_fishing:
    $ temp = getattr(store, "exit_string", "This is all for now.")
    $ hero.say(temp)
    # safe(r) cleanup:
    python hide:
        cleaup = ["all_fish", "selected_fish", "fishing_attempts",
                  "selected_fish", "min_fish_price", "exit_string",
                  "use_baits", "c0", "c1", "c2", "temp"]
        for i in cleaup:
            try:
                delattr(store, i)
            except:
                pass
    $ global_flags.set_flag("keep_playing_music")
    jump city_beach_left

image fishing_circles_webm = Transform(Movie(channel="main_gfx_attacks", play="content/gfx/animations/bubbles_webm/movie.webm", mask="content/gfx/animations/bubbles_webm/mask.webm"), zoom=.4, alpha=.4)
image fishing_circles_webm_alpha = Transform(Movie(channel="main_gfx_attacks", play="content/gfx/animations/bubbles_webm/movie.webm", mask="content/gfx/animations/bubbles_webm/mask.webm"), zoom=.8, alpha=1.0)

screen fishing_area(fishing_items):
    hbox:
        xsize 1280
        box_wrap True
        for i in xrange(15):
            add "water_texture__"

    for i in fishing_items:
        imagebutton:
            at random_fish_movement # Randomization is now done here.
            idle "fishing_circles_webm"
            hover "fishing_circles_webm_alpha"
            action Return(i)
            hovered SetField(config, "mouse", {"default": [("content/gfx/interface/icons/fishing_hook.png", 20, 20)]})
            unhovered SetField(config, "mouse", None)
    key "mousedown_3" action (Hide("fishing_area"), Return("Stop Fishing"))
