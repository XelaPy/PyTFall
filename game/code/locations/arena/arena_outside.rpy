label arena_outside:
    if not global_flags.has_flag("menu_return"):
        $ gm.enter_location(goodtraits=["Manly", "Courageous", "Aggressive"], badtraits=["Coward", "Nerd", "Homebody"], goodoccupations=["Combatant"], curious_priority=False)
        $ coords = [[.1, .6], [.59, .64], [.98, .61]]
        # Music related:
        if not "arena_outside" in ilists.world_music:
            $ ilists.world_music["arena_outside"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("arena_outside")]
        if not global_flags.has_flag("keep_playing_music"):
            play world choice(ilists.world_music["arena_outside"])
        $ global_flags.del_flag("keep_playing_music")

        scene bg arena_outside
        with dissolve

        $ ax = npcs["Xeona_arena"].say

        # Texts: ---------------------------------------------------------->
        if not global_flags.flag("visited_arena"):
            $ global_flags.set_flag("visited_arena")
            $ heard_about_arena = False
            $ arena_date = False
            'You see a pretty, confident girl approaching you.'
            show expression npcs["Xeona_arena"].get_vnsprite() as xeona
            with dissolve
            ax "I've never seen you before. What brings you here?"
            ax "Lust for blood? Fame? Power? Or Respect?"
            ax "Oh well, is there anything you'd like to know about this place?"
            jump xeona_talking
    else:
        $ global_flags.del_flag("menu_return")

    scene bg arena_outside
    python:
        # Build the actions
        if pytfall.world_actions.location("arena_outside"):
            pytfall.world_actions.meet_girls()
            pytfall.world_actions.look_around()
            pytfall.world_actions.add("0xeona", "Find Xeona", Jump("find_xeona"))
            pytfall.world_actions.add("0arena", "Enter Arena", Return(["control", "enter_arena"]))
            pytfall.world_actions.finish()

    show screen arena_outside

    # Auto-events
    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")

    $ loop = True
    while loop:

        $ result = ui.interact()

        if result[0] == 'jump':
            $ global_flags.set_flag("keep_playing_music")
            $ gm.start_gm(result[1])

        if result[0] == 'control':
            if result[1] == "enter_arena":
                $ renpy.music.stop(channel="gamemusic")
                $ hs()
                $ jump("arena_inside")

            if result[1] == 'return':
                $ loop = False

        $ renpy.hide("_tag")

    $ renpy.music.stop(channel="gamemusic")
    hide screen arena_outside
    jump city

label xeona_menu:
    hide screen arena_outside
    show screen xeona_screen
    $ loop = True
    while loop:
        $ result = ui.interact()

label xeona_goodbye:
    ax "Find me if you need anything, I'm always here."
    hide xeona with dissolve
    $ global_flags.set_flag("menu_return")
    jump arena_outside

label xeona_talking:
    $ loop = True

    while loop:
        menu:
            ax "Well?"
            "Xeona Main":
                $ pass

            "Tell me about Arena":
                ax "The arena, other than our sex industry, is the biggest source of entertainment for locals and tourists alike."
                ax "Many warriors come here to test their mettle against all challengers. Mages come to test their wisdom and training against all kinds of a foe."
                ax "Though most come just to unwind and see some kickass battles."
                ax "The arena consists of two sections, one for the {color=[green]}matches{/color} and one for {color=[green]}dogfights{/color}."
                ax "Both pay well, especially if you can please the crowd."
                ax "There is also a survival challenge where you can fight against beasts and monsters from all around."
                ax "Deaths are rare, due to regulations about pulling gladiators out before the monsters eat them."
                ax "Most of our gladiators with {color=[green]}arena permits{/color} make a very decent living."
                ax "However, those who are not at that level usually have some extra source of income, like guard duties or treasure hunting."
                ax "Well, that about enough for you to form a general picture?"
                ax "Are you going in?"
                $ heard_about_arena = True

            "Buy the Arena Permit?" if not hero.arena_permit and heard_about_arena:
                if hero.arena_rep >= 5000:
                    ax "It looks like you've managed to gain enough reputation. Congratulations!"
                    menu:
                        ax "Would you like to buy an arena permit? It's priced at {color=[gold]}10 000 Gold{/color}."
                        "Yes":
                            if hero.take_money(10000, reason="Arena Permit"):
                                $ hero.arena_permit = True
                                ax "There you go! You can now participate in official Arena Matches!"
                            else:
                                ax "Do you really have {color=[gold]}10 000 Gold{/color} on you?"
                                ax "Didn't think so..."
                        "No":
                            $ pass
                elif hero.arena_rep >= 2500:
                    ax "You've managed to improve your reputation, but you're not there yet :)"
                else:
                    ax "With the amount of rep you have? No chance in hell!!!"

            "What's an 'arena permit'?" if heard_about_arena and not hero.arena_permit:
                ax "An arena permit is something you get to pay a lot of Gold for when you've managed to gain enough reputation."
                ax "Then you can fight in official matches and take your place in the ladders."
                ax "Seems simple enough, doesn't it?"

            "How do I gain arena reputation?" if heard_about_arena:
                ax "By fighting and winning obviously."
                ax "Decent rep and some gold just might get you a permit so you could fight in the Arena matches one day."
                ax "Good teammates are also easier to find if your rep is higher than theirs."

            "Dogfights?" if heard_about_arena:
                ax "It's just the nickname that the arena crowd gave to unofficial matches."
                ax "To take part in one does not require a permit, just yourself or a capable team."
                ax "Spectators do enjoy watching a decent Dogfight as well, and you'll get paid so long as you deliver."

            "Official matches and ladders?" if heard_about_arena:
                ax "Oh, those are the real thing! If you win, you get to be on the official ladders of fame and glory!"
                ax "All gladiators who seek recognition try to get on them. Few succeed."
                ax "It's a great honor to be listed in any of the ladders. If you have the skills and tools required you should give it a go."
                ax "These types of matches are scheduled in advance. The loser goes down one position, and the winner gains a position."
                ax "As you've probably figured out, you can lose your place in the ladder without actually losing a fight."
                ax "But that's the incentive to keep fighting everyone, I suppose."

            "How does team combat work?" if heard_about_arena:
                ax "The team 'Leader' is what's really important."
                ax "Each team has a leader. The leader decides who fights by their side. "
                ax "There are {color=[red]}2vs2 and 3vs3{/color} fights."
                ax "Obviously, there is dueling as well. Good one on one fights are also adored by the spectators!"

            "Wanna go on a date with me?" if not arena_date:
                $ arena_date = True
                ax "Well, PyTFall's arena is a place of great... Wait... What?"
                ax "Find some floozy in the park! Why me all of a sudden?"
                ax "Oh wait, you were kidding. Right?"

            "Talk about weather":
                ax "Err... this is getting really awkward..."
                ax "Is there anything else???"

            "I know all I need to":
                $ loop = False
    $ del loop
    jump xeona_menu

label find_xeona:
    hide screen arena_outside
    $ ax = npcs["Xeona_arena"].say
    show expression npcs["Xeona_arena"].get_vnsprite() as xeona
    with dissolve
    ax "Hi again! Is there something you want?"
    jump xeona_menu

label xeona_training:
    if not global_flags.has_flag("xeona_training_explained"):
        ax "I train battle skills."
        ax "Don't expect to learn any magic, but I can teach you how to fight on level with any silly mage!"
        ax "Due to my the nature of training, there is always a chance of your constitution increasing as well."
        ax "Potions we drink to increase stamina during the training might also restore your health."
        "The training will cost you 250 gold per tier of the trained character every day."
        $ global_flags.set_flag("xeona_training_explained")
    else:
        ax "I am ready if you are!"

    if len(hero.team) > 1:
        call screen character_pick_screen
        $ char = _return
    else:
        $ char = hero

    if not char:
        jump xeona_menu
    $ loop = True

    while loop:
        menu:
            "About training sessions":
                call about_personal_training(ax) from _call_about_personal_training
            "About Xeona training":
                ax "I train battle skills."
                ax "Don't expect to learn any magic, but I can teach you how to fight on level with any silly mage!"
                ax "Due to my the nature of training, there is always a chance of your constitution increasing as well."
                ax "Potions we drink to increase stamina during the training might also restore your health."
                "The training will cost you 250 gold per tier of the trained character every day."
            "{color=[green]}Setup sessions for [char.name]{/color}" if not char.has_flag("train_with_xeona"):
                $ char.set_flag("train_with_xeona")
                $ char.apply_trait(traits["Xeona Training"])
                ax "Great, it will be [char.npc_training_price] gold per day."
            "{color=[red]}Cancel sessions for [char.name]{/color}" if char.flag("train_with_xeona"):
                $ char.del_flag("train_with_xeona")
                $ char.remove_trait(traits["Xeona Training"])
                ax "Until next time then."
            "Pick another character" if len(hero.team) > 1:
                call screen character_pick_screen
                if _return:
                    $ char = _return
            "Do Nothing":
                $ loop = False
    jump xeona_menu

screen arena_outside:
    use top_stripe(True)

    use location_actions("arena_outside")

    if gm.show_girls:
        key "mousedown_3" action ToggleField(gm, "show_girls")

        add "content/gfx/images/bg_gradient.png" yalign .45
        $ j = 0

        for entry in gm.display_girls():
            hbox:
                align (coords[j])
                $ j += 1
                use rg_lightbutton(img=entry.show("girlmeets", "armor", exclude=["swimsuit", "beach", "pool", "onsen", "bunny", "indoor", "formal", "wildness"], label_cache=True, gm_mode=True, resize=(300, 400), type="reduce"), return_value=['jump', entry])

screen xeona_screen():
    style_prefix "dropdown_gm"
    frame:
        pos (.98, .98) anchor (1.0, 1.0)
        has vbox
        textbutton "Talk":
            action Hide("xeona_screen"), Jump("xeona_talking")
        textbutton "Train":
            action Hide("xeona_screen"), Jump("xeona_training")
        textbutton "Leave":
            action Hide("xeona_screen"), Jump("xeona_goodbye")
            keysym "mousedown_3"
