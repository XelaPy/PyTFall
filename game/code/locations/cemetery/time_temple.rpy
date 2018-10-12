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
                t "Indeed, like any other temple we can heal your body and soul."
                t "Or rather, reverse the time and restore them to former condition."
                t "But we do it only once per day. Such is the natural limitation of time flow."
            python:
                temp_charcters = {}
                for i in hero.team:
                    if i.health < i.get_max("health") or i.mp< i.get_max("mp") or i.vitality < i.get_max("vitality"):
                        temp_charcters[i] = 0
                        if i.health < i.get_max("health"):
                            temp_charcters[i] += i.get_max("health") - i.health
                        if i.mp < i.get_max("mp"):
                            temp_charcters[i] += i.get_max("mp") - i.mp
                        if i.vitality < i.get_max("vitality"):
                            temp_charcters[i] += i.get_max("vitality") - i.vitality
            if not temp_charcters:
                t "I don't see the need in healing right now."
                "Miel can only restore characters in your team, including the main hero."
                jump time_temple_menu
            else:
                python: 
                    res = 0
                    for i in temp_charcters:
                        res += temp_charcters[i]
                t "I see your team could use our services. It will be [res] gold."
                if hero.gold < res:
                    "Unfortunately, you don't have enough money."
                    $ del res
                    $ del temp_charcters
                    jump time_temple_menu
                menu:
                    "Pay":
                        $ global_flags.set_flag("time_healing_day", day)
                        play sound "content/sfx/sound/events/clock.ogg"
                        with Fade(.5, .2, .5, color=goldenrod)
                        $ hero.take_money(res, reason="Time Temple")
                        python:
                            for i in temp_charcters:
                                i.health = i.get_max("health")
                                i.mp = i.get_max("mp")
                                i.vitality = i.get_max("vitality")
                        t "Done. Please come again if you need our help."
                        $ del res
                        $ del temp_charcters
                        jump time_temple_menu
                    "Don't Pay":
                        t "Very well."
                        $ del res
                        $ del temp_charcters
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