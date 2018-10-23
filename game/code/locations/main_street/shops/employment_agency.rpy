default employment_agency_chars = {
        "SIW": [],
        "Specialist": [],
        "Combatant": [],
        "Server": [],
        "Healer": []}

default employment_agency_reroll_day = 0

init python:
    def calc_hire_price_for_ea(char):
        return round_int(char.expected_wage*30)

    def populate_ea():
        global employment_agency_reroll_day
        global employment_agency_chars

        if day >= employment_agency_reroll_day:
            employment_agency_reroll_day = day + randint(7, 14)
            for k, v in employment_agency_chars.items():
                employment_agency_chars[k] = []
                for i in range(randint(2, 4)):
                    if dice(1): # Super char!
                        tier = hero.tier + uniform(2.5, 4.0)
                    elif dice(20): # Decent char.
                        tier = hero.tier + uniform(1.0, 2.5)
                    else: # Ok char...
                        tier = hero.tier + uniform(.1, 1.0)
                    char = build_rc(bt_group=k,
                                    set_locations=True,
                                    set_status="free",
                                    tier=tier, tier_kwargs=None,
                                    give_civilian_items=True,
                                    give_bt_items=True,
                                    spells_to_tier=False)
                    employment_agency_chars[k].append(char)

            # Gazette:
            c = npcs["Charla_ea"]
            temp = "{} informs all Business People of PyTFall that new workers are available for hire!".format(c.fullname)
            gazette.other.append(temp)

label employment_agency:
    # Music related:
    if not "shops" in ilists.world_music:
        $ ilists.world_music["shops"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("shops")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["shops"]) fadein 1.5

    hide screen main_street

    scene bg realtor_agency
    with dissolve

    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")

    show expression npcs["Charla_ea"].get_vnsprite() at Transform(align=(.9, 1.0)) as charla with dissolve

    $ ea = npcs["Charla_ea"].say

    if not global_flags.flag("visited_employment_agency"):
        $ global_flags.set_flag("visited_employment_agency", True)
        ea "Welcome to my Employment Agency, my name is Charla."
        ea "I am always on a lookout for perspective Employees and Employers."
        ea "You certainly look like one of the Employers!"
        ea "My fee for hooking you up with a capable worker is one month worth of their wages."
        ea "Take a look at the files I got on hand!"

    # Populate when needed:
    $ populate_ea()

    show screen employment_agency
    while 1:
        $ result = ui.interact()

        if result[0] == 'hire':
            $ char = result[1]
            $ cost = calc_hire_price_for_ea(char) # Two month of wages to hire.
            $ container = result[2]
            if hero.gold >= cost:
                jump employment_agency_hire
            else:
                $ block_say = True
                ea "You look a bit light on the Gold [hero.name]..."
                $ block_say = False

        if result[0] == 'control':
            if result[1] == 'return':
                jump employment_agency_exit

label employment_agency_exit:
    $ renpy.music.stop(channel="world")
    hide screen employment_agency
    jump main_street

label employment_agency_hire:
    $ block_say = True
    menu:
        ea "The fee to hire [char.name] is [cost]! What do you say?"
        "Yes":
            $ renpy.play("content/sfx/sound/world/purchase_1.ogg")
            $ hero.take_money(cost, reason="Hiring Workers")
            $ hero.chars.append(char)
            $ container.remove(char)
        "No":
            "Would you like to pick someone else?"
    $ block_say = False
    jump employment_agency


screen employment_agency():
    modal True
    zorder 1

    vbox:
        spacing 5
        yalign .5
        for k, v in sorted(employment_agency_chars.items(), key=itemgetter(0)):
            if v:
                hbox:
                    spacing 5
                    frame:
                        background Frame("content/gfx/frame/frame_bg.png", 10, 10)
                        xysize 200, 100
                        yalign .5
                        text k align .5, .5
                    for entry in v:
                        $ img = entry.show("portrait", cache=True, resize=(90, 90))
                        vbox:
                            frame:
                                padding(2, 2)
                                background Frame("content/gfx/frame/MC_bg3.png")
                                imagebutton:
                                    idle (img)
                                    hover (im.MatrixColor(img, im.matrix.brightness(.15)))
                                    action [SetVariable("char_profile_entry", "employment_agency"),
                                            SetVariable("girls", v),
                                            SetVariable("char", entry),
                                            Hide("employment_agency"),
                                            Jump("char_profile")]
                                    tooltip "View {}'s Detailed Info.\nClasses: {}".format(entry.fullname, entry.traits.base_to_string)
                            button:
                                padding(2, 2)
                                xsize 94
                                background Frame("content/gfx/frame/gm_frame.png")
                                hover_background Frame("content/gfx/frame/gm_frame.png")
                                label "Tier [entry.tier]" xalign .5 text_color "#DAA520"
                                action Return(['hire', entry, v])
                                tooltip "Hire {}.\nFee: {}G".format(entry.fullname, calc_hire_price_for_ea(entry))

    use exit_button()
