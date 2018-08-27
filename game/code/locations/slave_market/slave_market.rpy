init:
    image slave_market_slaves = "content/gfx/bg/locations/slave_podium.webp"

label slave_market:
    # Music related:
    if not "slavemarket" in ilists.world_music:
        $ ilists.world_music["slavemarket"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("slavemarket")]
    if not global_flags.has_flag("came_from_sc"):
        play world choice(ilists.world_music["slavemarket"]) fadein 1.5
    $ global_flags.del_flag("came_from_sc")

    if not global_flags.has_flag("visited_sm"):
        $ global_flags.set_flag("visited_sm")
        scene bg slave_market
        with dissolve
        show slave_market_slaves at truecenter

        "What's this?"
        extend " WHAT THE HELL IS THIS???"

        play sound "content/sfx/sound/be/whip_attack_2.mp3"

        "What's that look on your faces? Unhappiness? Doubt? Defiance?!?!"

        play sound "content/sfx/sound/be/whip_attack_2.mp3"

        "This lot requires more training, get them out of here!"

        play sound "content/sfx/sound/be/whip_attack_2.mp3"
        pause .1
        play sound "content/sfx/sound/be/whip_attack_2.mp3"

        "{color=[red]} Yes, Ma'am! Yes, Ma'am! Yes, Ma'am!"
        "And bring out some decent slaves to shop!"

        hide slave_market_slaves with fade
        show expression npcs["Blue_slavemarket"].get_vnsprite() as blue with dissolve

        $ g = Character("?????", color=aliceblue, show_two_window=True)

        menu:
            g "Hah? And who might you be?!"
            "Just want to check out the slave market":
                g "Oh? We didn't expect to see any customers here so early."
            "You should not be so hard on those girls":
                g "DON'T TELL ME HOW TO DO MY JOB YOU @$$#^*!!!"
                extend " ... but I guess that since you had to witness that, I'll let this slide."
            "Omg stfu I just need to test something!" if config.developer:
                jump slavel_market_controls
        g "Everyone calls me Blue. Original isn't it?"

        $ g = npcs["Blue_slavemarket"].say

        g "We usually try to prevent customers from seeing anything they might find unpleasant."
        g "But that weasel Stan is always trying to push 'unfinished' products."
        g "I mean what's the point? Reputation is much more important!"

        $ s = npcs["Stan_slavemarket"].say

        show expression npcs["Stan_slavemarket"].get_vnsprite() as stan at mid_left with dissolve

        s "Hey, hey there!"
        s "Is there anyone here talking about me?"
        s "Just the cool things I assume!?"
        g "What the hell are you talking about? Those slaves were a disgrace to our good rep!"
        s "Temper, temper my dear... the quality of those slaves are your problem."
        s "Keeping the cash flowing, gold rolling, so Mr. Big is satisfied, is mine!"
        s "I am going to get some measure of today's lots and what we can get for them!"
        s "Don't bother our prospective clients and play with your slaves while {color=[red]}I{/color} take care of real work! <Smirks>"

        hide stan with dissolve
        show expression npcs["Blue_slavemarket"].get_vnsprite() as blue at center with move

        g "That damn baboon only thinks about money! No sense of duty or love for the craft!"
        g "You see it too, don't you?"
        g "In any case, if you're looking to whip some slave into shape or get a fair deal on one. Find me. I'll set you up!"
        g "Ah, visit our club as well, we do presentations, and you can do 'some sampling' if you have the Gold."
        g "You won't be disappointed!"
        g "Goodbye!"

label slavel_market_controls:
    hide blue
    with dissolve
    show bg slave_market

    $ global_flags.set_flag("visited_sm")

    python:
        # Build the actions
        if pytfall.world_actions.location("slave_market"):
            pytfall.world_actions.add("blue", "Find Blue", Jump("blue_menu"), condition=Iff(global_flag_complex("visited_sm")))
            pytfall.world_actions.work(Iff(global_flag_complex("visited_sm")))
            pytfall.world_actions.work(Iff(global_flag_complex("visited_sm")), index="work_all", name="Work all day", returned="mc_action_work_in_slavemarket_all_day")
            pytfall.world_actions.slave_market(pytfall.sm, "Get these girls while they're still Young and Hot!")
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()

    scene bg slave_market

    $ pytfall.sm.set_index()

    show screen slavemarket
    with fade

    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")

    $ loop = True
    while loop:
        $ result = ui.interact()

        if result[0] == "buy":
            $ char = pytfall.sm.girl
            if hero.take_ap(1):
                if hero.take_money(char.fin.get_price(), reason="Slave Purchase"):
                    play sound "content/sfx/sound/world/purchase_1.ogg"
                    $ hero.add_char(char)
                    $ char.action = char.workplace = None
                    $ char.home = locations["Streets"]
                    $ pytfall.sm.chars_list.remove(char)

                    if pytfall.sm.chars_list:
                        $ pytfall.sm.girl = choice(pytfall.sm.chars_list)
                        $ pytfall.sm.index = pytfall.sm.chars_list.index(pytfall.sm.girl)
                    else:
                        $ pytfall.sm.girl = None
                else:
                    call screen message_screen("You don't have enough money for this purchase!")
            else:
                call screen message_screen("You don't have enough AP left for this action!!")

            if not pytfall.sm.chars_list:
                hide screen slave_shopping

        if result[0] == "control":
            if result[1] == "work":
                jump mc_action_work_in_slavemarket
            elif result[1] == "mc_action_work_in_slavemarket_all_day":
                jump mc_action_work_in_slavemarket_all_day
            elif result[1] == "jumpclub":
                hide screen slavemarket
                jump slave_market_club
            elif result[1] == "return":
                if not renpy.get_screen("slave_shopping"):
                    $ loop = False

        $ renpy.hide("_tag")

    $ renpy.music.stop(channel="world")
    hide screen slavemarket
    jump city

label mc_action_work_in_slavemarket:
    python:
        wage = randint(5, 12) + hero.charisma/7 + hero.sex/20 + hero.level*5
        if dice(hero.luck*.1):
            wage += hero.level*5

        if dice(.5 + hero.luck*.1):
            hero.charisma += 1
            hero.sex += 1

    $ hero.add_money(wage, reason="Job")
    $ gfx_overlay.random_find(wage, 'work')
    $ hero.exp += exp_reward(hero, hero)

    $ hero.take_ap(1)

    pause 0.01

    python:
        if dice(50):
            renpy.say("", choice(["You did some chores around the slavemarket!",
                      "Pay might be crap, but it's still money.",
                      "You've helped out in da Club!"]))
        else:
            hero.say(choice(["What a shitty job...",
            "There's gotta be better way to make money..."]))

    $ global_flags.set_flag("came_from_sc")
    jump slavel_market_controls

label blue_menu:
    $ g = npcs["Blue_slavemarket"].say
    scene bg slave_market with fade
    show expression npcs["Blue_slavemarket"].get_vnsprite() as blue with dissolve
    g "[hero.nickname]!"
    g "Welcome back to our fine establishment!"
    $ loop = True
    while loop:
        menu:
            g "Slave Training is an Art!"
            "Tell me about Slave Training.":
                "PlaceHolder until we figure out how ST works :)"
            "Ask about Captured Girls." if False: # fg in hero.buildings:
                if not global_flags.flag("blue_cg"):
                    g "So, you now own an Exploration Guild?"
                    g "Well done, it's a well-known source of slaves of all kinds."
                    g "Once a fresh girl is processed in the jail and registered with the authorities, I can train her to obey and do her job."
                    g "I don't train for any specific task but rather uncover their hidden talents. My price is 2000 Gold to be paid up front."
                    g "The training will take 30 days, and you don't have to worry because I always deliver :)"
                    $ global_flags.set_flag("blue_cg")
                else:
                    if pytfall.sm.blue_girls:
                        $ var = plural("girl", len(pytfall.sm.blue_girls))
                        g "I am currently training [var] girls for you."
                        g "Don't worry. They'll all be ready as promised."
                    else:
                        g "I'll train anyone, without fail! Just send them my way!"
            "That will be all":
                g "Goodbye!"
                $ loop = False

    jump slave_market

screen slavemarket():

    use top_stripe(True)

    use r_lightbutton(img=im.Flip(im.Scale("content/gfx/interface/buttons/blue_arrow.png", 80, 80), horizontal=True), return_value =['control', 'jumpclub'], align=(.01, .5))

    use location_actions("slave_market")

screen slave_shopping(store, tt_text, buy_button, buy_tt):
    modal True
    zorder 1

    # Tooltip
    default tt = Tooltip("%s"%tt_text)

    frame:
        background Frame("content/gfx/frame/black_frame.png", 10, 10)
        align(.977, 1.0)
        xysize (1003, 92)
        vbox:
            text "{=proper_stats_text}%s"%tt.value style "proper_stats_text" outlines [(1, "#3a3a3a", 0, 0)]

    if store.chars_list:
        # Stats and Info (Left Frame):
        frame:
            background Frame(Transform("content/gfx/frame/p_frame53.png", alpha=.98), 10, 10)
            xysize(270, 678)
            ypos 41
            style_group "content"
            has vbox
            null height 15
            vbox:
                # Name:
                frame:
                    xanchor -0.01
                    xysize (250, 50)
                    background Frame(Transform("content/gfx/frame/namebox5.png", alpha=.95), 250, 50)
                    label "{color=[gold]}[store.girl.fullname]":
                        text_color ivory text_outlines [(2, "#424242", 0, 0)]
                        align (.5, .5)
                        if len(store.girl.fullname) < 20:
                            text_size 21

                null height 5

                if False and traits['Prostitute'] in store.girl.occupations:
                    frame:
                        xanchor -0.01
                        xysize(253, 47)
                        background Frame("content/gfx/frame/rank_frame.png", 10, 10)
                        text ('%s:'%store.girl.wranks['r%s'%store.girl.rank]['name'][0]) align (.1, .2) color ivory size 16
                        text ('%s'%store.girl.wranks['r%s'%store.girl.rank]['name'][1]) align (.5, .96) color ivory size 16
                else:
                    null height -5

                label (u"{size=20}{color=[ivory]}{b}Info:") xalign(.5) text_outlines [(2, "#424242", 0, 0)]

                null height -10

                vbox:
                    style_group "stats"
                    spacing 5
                    pos(.015, 10)
                    frame:
                        background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
                        #xysize (317, 10)
                        xsize 258
                        xanchor 5
                        xpadding 6
                        ypadding 6
                        xmargin 1
                        ymargin 1
                        style_group "proper_stats"
                        has vbox spacing 1
                        vbox:
                            spacing -1
                            xmaximum 246
                            frame:
                                xysize 244, 20
                                text ("{color=#79CDCD}{size=-1}Class:") pos (1, -4)
                                label "{size=-3}[store.girl.traits.base_to_string]" align (1.0, .5) ypos 10
                            frame:
                                xysize 244, 20
                                text "{color=#79CDCD}{size=-1}Market Price:" pos (1, -4)
                                label (u"{color=[gold]}{size=-5}%s"%store.girlfin.get_price()) align (1.0, .5) ypos 10
                            frame:
                                xysize 244, 20
                                text "{color=#79CDCD}{size=-1}Upkeep:" pos (1, -4)
                                label (u"{size=-5}%s"%store.girlfin.get_upkeep()) align (1.0, .5) ypos 10

                null height 8

                label (u"{size=20}{color=[ivory]}{b}Stats:") xalign(.5) text_outlines [(2, "#424242", 0, 0)]

                null height -12

                vbox:
                    style_group "stats"
                    pos(.015, 10)
                    frame:
                        background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
                        #xysize (317, 10)
                        xsize 258
                        xanchor 5
                        xpadding 6
                        ypadding 6
                        xmargin 1
                        ymargin 1
                        style_group "proper_stats"
                        has vbox spacing 1
                        vbox:
                            spacing -1
                            xmaximum 246
                            frame:
                                xysize 245, 20
                                text "{color=#79CDCD}{size=-1}Health:" pos (1, -4)
                                label (u"{size=-5}%s/%s"%(store.girl.health, store.girl.get_max("health"))) align (1.0, .5) ypos 10
                            frame:
                                xysize 245, 20
                                text "{color=#79CDCD}{size=-1}Vitality:" pos (1, -4)
                                label (u"{size=-5}%s/%s"%(store.girl.vitality, store.girl.get_max("vitality"))) align (1.0, .5) ypos 10
                            frame:
                                xysize 245, 20
                                text "{color=#79CDCD}{size=-1}Charisma:" pos (1, -4)
                                label (u"{size=-5}%s/%s"%(store.girl.charisma, store.girl.get_max("charisma"))) align (1.0, .5) ypos 10
                            frame:
                                xysize 245, 20
                                text "{color=#79CDCD}{size=-1}Character:" pos (1, -4)
                                label (u"{size=-5}%s/%s"%(store.girl.character, store.girl.get_max("character"))) align (1.0, .5) ypos 10
                            frame:
                                xysize 245, 20
                                text "{color=#79CDCD}{size=-1}Constitution:" pos (1, -4)
                                label (u"{size=-5}%s/%s"%(store.girl.constitution, store.girl.get_max("constitution"))) align (1.0, .5) ypos 10
                            frame:
                                xysize 245, 20
                                text "{color=#79CDCD}{size=-1}Intelligence:" pos (1, -4)
                                label (u"{size=-5}%s/%s"%(store.girl.intelligence, store.girl.get_max("intelligence"))) align (1.0, .5) ypos 10
                            #text (u"| %d"%store.girl.goal)
                    frame:
                        background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
                        #xysize (317, 10)
                        xsize 258
                        xanchor 5
                        xpadding 6
                        ypadding 6
                        xmargin 1
                        ymargin 1
                        style_group "proper_stats"
                        has vbox spacing 1
                        vbox:
                            spacing -1
                            xmaximum 246
                            frame:
                                xysize 245, 20
                                text "{color=#79CDCD}{size=-1}Level:" pos (1, -4)
                                label (u"{size=-5}%s"%store.girl.level) align (1.0, .5) ypos 10

                null height 8

                label (u"{size=20}{color=[ivory]}{b}Prof Stats:") xalign(.5) text_outlines [(2, "#424242", 0, 0)]

                null height -12

                vbox:
                    style_group "stats"
                    pos(.015, 10)
                    frame:
                        background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
                        #xysize (317, 10)
                        xsize 258
                        xanchor 5
                        xpadding 6
                        ypadding 6
                        xmargin 1
                        ymargin 1
                        style_group "proper_stats"
                        has vbox spacing 1
                        vbox:
                            spacing -7
                            xmaximum 246
                            frame:
                                xsize 245

        # Picture:
        frame:
            pos(265, 41)
            xysize (669, 423)
            background Frame(Transform("content/gfx/frame/p_frame53.png", alpha=1.0), 10, 10)
            frame:
                align (.5, .5)
                background Frame("content/gfx/frame/MC_bg.png", 10, 10)
                add (store.girl.show("nude","no clothes", resize=(560, 400), exclude=["rest", "outdoors", "onsen", "beach", "pool", "living"], type="first_default", label_cache=True)) align(.5, .5)

        # Traits:
        frame:
            pos (928, 41)
            style_group "content"
            xysize (350, 334)
            background Frame(Transform("content/gfx/frame/p_frame53.png", alpha=.98), 10, 10)
            has vbox align (.5, .5)
            null height 5
            label (u"{size=20}{color=[ivory]}{b}Visible Traits") xalign .5 text_outlines [(2, "#424242", 0, 0)]
            null height 5
            frame:
                left_padding 15
                ypadding 10
                xsize 226
                background Frame(Transform("content/gfx/frame/p_frame4.png", alpha=.6), 10, 10)
                has viewport xysize (210, 253) draggable True mousewheel True scrollbars "vertical"
                vbox:
                    xalign .5
                    style_group "proper_stats"
                    spacing 1
                    for trait in list(t for t in store.girl.traits if any([t.market])):
                        if not trait.hidden:
                            frame:
                                xysize (195, 25)
                                button:
                                    background Null()
                                    xysize (195, 25)
                                    action NullAction()
                                    if len(trait.id) < 15:
                                        text trait.id idle_color bisque size 18 align .5, .5 hover_color crimson text_align .5
                                    else:
                                        text trait.id idle_color bisque size 15 align .5, .5 hover_color crimson text_align .5
                                    hovered tt.Action(trait.desc)
                                    hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(.10)), 5, 5)

        # Buttons:
        frame:
            background Frame(Transform("content/gfx/frame/p_frame53.png", alpha=.98), 10, 10)
            xpadding 5
            pos(928, 370)
            xsize 350
            hbox:
                xalign .5
                $ img=im.Scale("content/gfx/interface/buttons/arrow_button_metal_gold_left.png", 50, 50)
                imagebutton:
                    align(.5, .5)
                    idle img
                    hover (im.MatrixColor(img, im.matrix.brightness(.15)))
                    action (Function(store.previous_index))
                    hovered tt.Action("<== Previous Girl")

                null width 10

                frame:
                    align(.5, .5)
                    style_group "dropdown_gm"
                    has vbox

                    # Decided to handle it on screen level since code required for this can get a bit messy when going through actions:
                    if store == jail and store.girl.flag("sentence_type") == "SE_capture":
                        textbutton "Retrieve":
                            xsize 150
                            action Show("se_captured_retrieval")
                            hovered tt.Action("Retrieve %s for % gold." % (store.girl.name, store.get_fees4captured()))
                    else:
                        textbutton "[buy_button]":
                            xsize 150
                            action Return(["buy"])
                            hovered tt.Action("" + buy_tt % store.girlfin.get_price())
                    textbutton "Back":
                        xsize 150
                        action Hide("slave_shopping", transition=Dissolve(1.0))
                        hovered tt.Action("Exit Market")

                null width 10

                $ img=im.Scale("content/gfx/interface/buttons/arrow_button_metal_gold_right.png", 50, 50)
                imagebutton:
                    align(.5, .5)
                    idle img
                    hover (im.MatrixColor(img, im.matrix.brightness(.15)))
                    action (Function(store.next_index))
                    hovered tt.Action("Next Girl ==>")

        # Girl choice:
        frame:
            # pos 265, 459
            pos 265, 455
            background Frame(Transform("content/gfx/frame/p_frame53.png", alpha=.98), 10, 10)
            side "c t":
                yoffset -2
                viewport id "sm_vp_glist":
                    xysize 1001, 150
                    draggable True
                    mousewheel True
                    edgescroll [60, 100]
                    has hbox spacing 5
                    for c in store.chars_list:
                        $ img = c.show("vnsprite", resize=(180, 138), cache=True)
                        frame:
                            background Frame("content/gfx/frame/Mc_bg3.png", 10, 10)
                            imagebutton:
                                idle img
                                hover (im.MatrixColor(img, im.matrix.brightness(.15)))
                                action Function(store.set_girl, c)
                                hovered tt.Action(u"{=proper_stats_text}%s\n{size=-5}{=proper_stats_value_text}%s"%(c.name, c.desc))
                bar value XScrollValue("sm_vp_glist")

    use top_stripe(show_return_button=True, return_button_action=Hide("slave_shopping"), show_lead_away_buttons=False)

screen se_captured_retrieval(pos=(900, 300)):
    # Not Used atm.
    zorder 3
    modal True

    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()

    python:
        x, y = pos
        xval, yval = 1.0, 0
    frame:
        style_group "dropdown"
        pos (x, y)
        anchor (xval, yval)
        vbox:
            textbutton "Sell!":
                action jail.sell_captured, renpy.restart_interaction, Hide("se_captured_retrieval")
            if global_flags.flag("blue_cg"):
                textbutton "Train with Blue!":
                    action Function(jail.retrieve_captured, direction="Blue"), Hide("se_captured_retrieval")
            textbutton "Close":
                action Hide("se_captured_retrieval")

label mc_action_work_in_slavemarket_all_day:
    $ temp = hero.AP
    python:
        wage = (randint(5, 12) + hero.charisma/7 + hero.sex/20 + hero.level*5)*temp
        if dice(hero.luck*.1):
            wage += (hero.level*5)*temp

        if dice(.5 + hero.luck*.1):
            hero.charisma += 1*temp
            hero.sex += 1*temp

        hero.add_money(wage, reason="Job")
        gfx_overlay.random_find(wage, 'work')
        hero.exp += temp*exp_reward(hero, hero)

        hero.take_ap(temp)
        del temp

    python:
        if dice(50):
            renpy.say("", choice(["You did some chores around the slavemarket!",
                      "Pay might be crap, but it's still money.",
                      "You've helped out in da Club!"]))
        else:
            hero.say(choice(["What a shitty job...",
            "There's gotta be better way to make money..."]))

    $ global_flags.set_flag("came_from_sc")
    jump slavel_market_controls
