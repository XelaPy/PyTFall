default clone_id = 0

label time_temple:
    if not global_flags.has_flag("time_healing_day"):
        $ global_flags.set_flag("time_healing_day", 0)
    if not "cemetery" in ilists.world_music:
        $ ilists.world_music["cemetery"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("cemetery")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["cemetery"]) fadein .5

    $ global_flags.del_flag("keep_playing_music")

    scene bg time_temple
    with dissolve
    show screen time_temple

    if not global_flags.has_flag("visited_time_temple"):
        $ global_flags.set_flag("visited_time_temple")
        "You enter a massive dimly lit building. Strange voiceless figures in the hoods sweep the floor and replace burned-out candles."
        show expression npcs["time_miel"].get_vnsprite() as npc
        with dissolve
        $ t = npcs["time_miel"].say
        "A strange girl of unknown race approaches you. Most of her belly is a giant, working hourglass."
        t "Welcome to the Temple of Time, stranger. I'm Miel, its caretaker."
        t "If you need something, I'm here to help. Please don't bother others."
    else:
        show expression npcs["time_miel"].get_vnsprite() as npc
        with dissolve
        $ t = npcs["time_miel"].say
        t "Welcome to the Temple. May I help you?"

    menu time_temple_menu:
        "Healing":
            if global_flags.flag("time_healing_day") >= day:
                t "I'm sorry, it's impossible to perform the procedure twice per day."
                jump time_temple_menu

            if not global_flags.has_flag("asked_miel_about_healing"):
                $ global_flags.set_flag("asked_miel_about_healing")
                t "Indeed, like any other temple we can heal your body and soul, as well as remove most negative effects."
                t "Or rather, reverse the time and restore them to former condition."
                t "But we do it only once per day. Such is the natural limitation of time flow."

            python:
                temp_charcters = 0
                for i in hero.team:
                    if any([i.health < i.get_max("health"), i.mp< i.get_max("mp"), i.vitality < i.get_max("vitality"), "Food Poisoning" in i.effects, "Poisoned" in i.effects, "Down with Cold" in i.effects, "Injured" in i.effects]):
                        if i.health < i.get_max("health"):
                            temp_charcters += i.get_max("health") - i.health
                        if i.mp < i.get_max("mp"):
                            temp_charcters += i.get_max("mp") - i.mp
                        if i.vitality < i.get_max("vitality"):
                            temp_charcters += i.get_max("vitality") - i.vitality
                            
                        if "Food Poisoning" in i.effects:
                            temp_charcters += 100
                        if "Poisoned" in i.effects:
                            temp_charcters += 100
                        if "Down with Cold" in i.effects:
                            temp_charcters += 50
                        if "Injured" in i.effects:
                            temp_charcters += 150

                    
                    
                    
                    
            if temp_charcters <= 0:
                t "I don't see the need in healing right now."
                "Miel can only restore characters in your team, including the main hero."
                jump time_temple_menu
            else:
                t "I see your team could use our services. It will be [temp_charcters] gold."
                if hero.gold < temp_charcters:
                    "Unfortunately, you don't have enough money."
                    $ del temp_charcters
                    jump time_temple_menu

                menu:
                    "Pay":
                        $ global_flags.set_flag("time_healing_day", day)
                        play sound "content/sfx/sound/events/clock.ogg"
                        with Fade(.5, .2, .5, color=goldenrod)
                        $ hero.take_money(temp_charcters, reason="Time Temple")
                        python:
                            for i in hero.team:
                                i.health = i.get_max("health")
                                i.mp = i.get_max("mp")
                                i.vitality = i.get_max("vitality")
                                i.disable_effect("Poisoned")
                                i.disable_effect("Food Poisoning")
                                i.disable_effect("Down with Cold")
                                i.disable_effect("Injured")
                        t "Done. Please come again if you need our help."
                        $ del temp_charcters
                        jump time_temple_menu
                    "Don't Pay":
                        t "Very well."
                        $ del temp_charcters
                        jump time_temple_menu
                        
        "Restore AP":
            if not global_flags.has_flag("asked_miel_about_ap"):
                $ global_flags.set_flag("asked_miel_about_ap")
                t "I can return you the time you spent. But it's an expensive procedure."
                "Miel can restore your action points, as long as you can pay for it."
                "Only the hero can use this option, his teammates are not affected."
            if hero.AP >= hero.baseAP:
                "Your action points are maxed out already at the moment."
                jump time_temple_menu
            if hero.gold < 10000:
                "Unfortunately, you don't have 10000 gold coins to pay."
            else:
                "Do you wish to pay 10000 gold to restore AP for [hero.name]?"
                menu:
                    "Yes":
                        play sound "content/sfx/sound/events/clock.ogg"
                        with Fade(.5, .2, .5, color=goldenrod)
                        $ hero.take_money(10000, reason="Time Temple")
                        $ hero.AP = hero.baseAP
                        t "Your time has been returned to you. Come again if you need me."
                    "No":
                        $ pass
            jump time_temple_menu
            
        "Remove injures":
            if not global_flags.has_flag("asked_miel_about_wounds"):
                $ global_flags.set_flag("asked_miel_about_wounds")
                t "I can remove injures from everyone who works for you. It's a common problem among adventurers these days."
            $ temp_charcters = list(c for c in hero.chars if (c.is_available and "Injured" in c.effects))
            $ p = len(temp_charcters)*150
            if len(temp_charcters) <= 0:
                t "I don't think you need this service at the moment."
            elif hero.gold < p:
                "Unfortunately, you don't have [len(temp_charcters)*150] gold coins to pay."
            else:
                menu:
                    "Do you wish to pay [p] gold to heal all injures for your girls?"
                    "Yes":
                        play sound "content/sfx/sound/events/clock.ogg"
                        with Fade(.5, .2, .5, color=goldenrod)
                        $ hero.take_money(p, reason="Time Temple")
                        python:
                            for i in temp_charcters:
                                i.disable_effect("Injured")
                        t "Done. Come again if you need me."
                    "No":
                        $ pass
            $ del temp_charcters
            $ del p
            jump time_temple_menu
                        
        "Ask about this place":
            t "This is the Temple of Time. Locals come here to to pray to almighty gods of time and space."
            t "We also provide additional services, for a fee."
            jump time_temple_menu
        "Ask about her" if not global_flags.has_flag("asked_about_miel"):
            $ global_flags.set_flag("asked_about_miel")
            t "Me? I'm just a servant of time."
            t "I will exist forever with this temple as long as I'm taking care of it."
            t "This is all you need to know."
            jump time_temple_menu
        "Leave":
            t "See you soon."

    hide npc
    with dissolve
    hide screen time_temple
    $ global_flags.set_flag("keep_playing_music")
    stop sound
    jump graveyard_town


screen time_temple():

    use top_stripe(True, None, False, True, False)

label clone_character(character, add_to_hero=True):
    python:
        char = copy_char(character)
        store.chars[char.id + str(clone_id)] = char
        char.init() # Normalize.
        char.apply_trait("Temporal Clone")
        if add_to_hero:
            store.hero.add_char(char)
        clone_id += 1
    return
