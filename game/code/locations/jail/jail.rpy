label city_jail:

    # Music related:
    if not "cityjail" in ilists.world_music:
        $ ilists.world_music["cityjail"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("cityjail")]

    python:
        # Build the actions
        if pytfall.world_actions.location("city_jail"):
            pytfall.world_actions.menu("cells", "Cells")
            # pytfall.world_actions.slave_market(pytfall.ra, "Claim an escaped slave by paying off their fine.",
            #                                    button="Browse Escapees", null_button="No Escapees",
            #                                    buy_button="Retrieve", buy_tt="Claim this girl by paying her fine of %s Gold.",
            #                                    index=("cells", "sm_ra"))
            pytfall.world_actions.slave_market(jail, "Acquire the services of a prisoner buy paying their bail.",
                                               button="Browse Prisoners", null_button="No Prisoners",
                                               buy_button="Bail", buy_tt="Acquire this girl by paying her bail of %s Gold.",
                                               index=0,
                                               null_condition="not jail.chars_list or not hero.AP")
            # pytfall.world_actions.slave_market(jail, "Acquire the services of a prisoner buy paying their bail.",
            #                                    button="Browse Prisoners", null_button="No Prisoners",
            #                                    buy_button="Bail", buy_tt="Acquire this girl by paying her bail of %s Gold.",
            #                                    index=("cells", "sm_cj"))

            pytfall.world_actions.add(("cells", "browse"), "Browse Cells", "browse_jail_cells", label="_no_jail_event")
            pytfall.world_actions.look_around()
            pytfall.world_actions.finish()

    scene bg jail
    with dissolve

    if not global_flags.flag('visited_city_jail'):
        $ global_flags.set_flag('visited_city_jail')
        "The city jail..."
        "Temporary home of miscreants and lawbreakers."
        "Not to mention an occasional escaped slave."

    $ jail.set_focus()
    show screen city_jail

    $ pytfall.world_quests.run_quests("auto")
    $ pytfall.world_events.run_events("auto")

    while True:
        $ result = ui.interact()

        if result[0] == "jail_action":
            if result[1] == "buy": # Dealing with slave:
                $ char = jail.focused
                $ price = jail.get_fees4captured(char)
                $ Notify("{} was kept in jail for {} days".format(char.name, char.flag("days_in_jail")))

                if hero.AP > 0 and hero.take_money(price, reason="Slave Purchase"):
                    play sound "content/sfx/sound/world/purchase_1.ogg"

                    $ jail.remove_prisoner(char)

                    $ hero.AP -= 1
                    $ hero.add_char(char)
                    $ jail.set_focus()

                    call screen message_screen("You've retrieved {} from jail!".format(char.name))
                else:
                    call screen message_screen("You don't have enough money for this purchase!")

                if not jail.chars_list or not hero.AP:
                    hide screen slave_shopping
                    $ Return(("control", "return"))()
            elif result[1] == "retrieve": # Dealing with a free char:
                $ char = jail.focused
                $ price = jail.get_fees4captured(char)
                $ Notify("{} was kept in jail for {} days".format(char.name, char.flag("days_in_jail")))

                $ speaker = char.say
                $ chars_sprite = char.get_vnsprite()

                hide screen slave_shopping
                show expression chars_sprite

                $ char.override_portrait("portrait", "angry")
                $ char.show_portrait_overlay("angry", "reset")
                speaker "These bastards are keeping me here against my will!"
                speaker "I keep telling them that I am a free citizen but they claim that it 'takes time' to confirm that!"
                $ char.show_portrait_overlay("sweat", "reset")
                speaker "I bet they just enjoy peeping at me... damned pervs!"
                $ char.restore_portrait()

                menu:
                    speaker "Can you help me?"
                    "Bribe the guards {color=[gold]}(1000G)" if hero.gold >= 1000:
                        $ hero.take_money(1000, "Bribes")
                        menu:
                            "Hire [char.name].":
                                speaker "Work for you?"
                                speaker "Sure, I'd love that!"

                                $ jail.remove_prisoner(char)

                                $ hero.AP -= 1
                                $ hero.add_char(char)
                                $ jail.set_focus()

                                $ char.disposition += 200

                                show screen message_screen("You've retrieved {} from jail!".format(char.name))
                            "Walk away":
                                # We should get her to pay the bribe back in Interactions!
                                $ jail.remove_prisoner(char)
                                $ jail.set_focus()

                                $ char.location = "city"

                                $ char.disposition += 400

                                $ temp = "{} was released from Jail! You might meet her in the city one day!".format(char.name)
                                $ renpy.show_screen("message_screen", temp)
                    "Walk away":
                        $ pass

                hide expression chars_sprite
                jump city_jail
        elif result[0] == "control":
            if result[1] == "return":
                hide screen city_jail
                jump city


label _no_jail_event:
    $ hero.say(choice(["Nothing to see.",
                       "Not implemented yet :(",
                       "Nothing."]))
    return


screen city_jail():

    use top_stripe(True)

    use location_actions("city_jail")
