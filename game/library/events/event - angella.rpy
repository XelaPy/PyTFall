init python:
    register_event("angelica_menu", locations=["mages_tower"], simple_conditions=["global_flags.flag('mt_counter') > 3"], priority=100, start_day=1, jump=True, dice=80, max_runs=1)

    
label angelica_menu:
    
    $ a = Character("Angelica", color=blue, what_color=cornflowerblue, show_two_window=True)
    
    hide screen pyt_mages_tower
    show npc angelica
    with dissolve
    
    if not global_flags.flag("met_angelica"):
        $ global_flags.set_flag("met_angelica")
        
        a "Hi! I am Angelica!"
        a "I noticed you've been hanging around the Tower."
        menu:
            a "Are you interested in magic?"
            "Yes!":
                a "Great! I might be of some assistance then. "
                extend "You cannot join us in the tower at the moment but I am capable of helping you picking an alignment."
                $ global_flags.set_flag("angelica_free_alignment")
                a "Guild demands that I charge 10000 Gold for it but I like you, so you get one freebie!"
                a "You can change an alignment only once! So be sure about your choice!"
            "Not really...":
                a "Oh? Well, never mind then..."
                a "On the other hand, keep in mind that I can assign magical alignment. So if you know someone who's in need of my services, please send them in my direction!"
                jump mages_tower
    
    $ loop = True
    while loop:
        menu:
            a "How can I be of assistance today?"
            
            "Change alignment!":
                a "Lets take a look!"
                if len(hero.team) > 1:
                    if len(hero.team) == 3:
                        a "Who is it going to be?"
                    call screen character_pick_screen
                    $ char = _return
                else:
                    $ char = hero
                    
                if char.flag("picked_alignement"):
                    a "Sorry, I cannot change the alignment twice :("
                else:
                    a "Keep in mind that it can only be done once!"
                    
                    call screen alignment_choice
                    
                    $ alignment = _return
                            
                    if alignment:
                        if alignment == char.element.split()[0]:
                            a "Err, you cannot really change from [alignment] to [alignment]."
                            a "Sorry..."
                        else:
                            if global_flags.flag("angelica_free_alignment") or hero.take_money(10000, reason="Alignments"):
                                a "There! All done!"
                                # Animation?
                                python:
                                    global_flags.del_flag("angelica_free_alignment")
                                    char.set_flag("picked_alignement")
                                    char.element = " ".join([alignment, str(choice([1, 2]))])
                                $ char.say(choice(["What a weird feeling...", "Awesome!", "This is cool!"]))
                            else:
                                a "You don't have enought money."
                    $ del alignment
                    
            "Goodbye!":
                $ loop = False
            
    a "See you around!"
    jump mages_tower
    
screen alignment_choice:
    default tt = Tooltip("I changed my mind...!")
    
    textbutton "[tt.value]":
        style "yesno_button"
        align(0.1, 0.05)
        action Return("")
    
    # python:
        # center_x = config.screen_width/2
        # center_y = config.screen_height/2
        # radius = 300
        # button_idx = 0
    
    python:
        elements = list(el for el in traits.values() if el.elemental)
        # for fn in os.listdir(content_path("gfx/interface/images/elements")):
            # path = "content/gfx/interface/images/elements/" + fn
            # elements.append((path, fn.capitalize()))
        step = 360 / len(elements)
        var = 0
        
    for el in elements:
        python:
            img = ProportionalScale(el.icon, 120, 120)
            angle = var
            var = var + step
        imagebutton at circle_around(t=10, angle=angle, radius=250):
            idle img
            hover im.MatrixColor(img, im.matrix.brightness(0.25))
            action Return(el)
            hovered tt.Action(el.id)
        
    # fixed at repeated_rotate(t=15):
        # pos(-100, -350)
        # for alignment in ["air", "earth", "fire", "water", "darkness", "light", "neutral"]:
            # python:
                # angle = button_idx * math.pi * 2 / 7
                # x = cos(angle) * radius + center_x
                # y = sin(angle) * radius + center_y
            # $ img = ProportionalScale("".join(["content/gfx/interface/images/elements/", alignment, ".png"]), 150, 150)
            # imagebutton at elements():
                # idle img
                # hover im.MatrixColor(img, im.matrix.brightness(0.25))
                # action Return(alignment.split()[0].capitalize())
                # anchor (0.5, 0.5)
                # pos (int(x), int(y))
                # hovered tt.Action(alignment.split()[0].capitalize())
            # $ button_idx += 1
