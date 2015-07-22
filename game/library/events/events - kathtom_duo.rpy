# Events File

init -9 python:    
    register_event("maria_tulip_1_event", locations=["arena_outside"], priority=1, dice=20, max_runs=1)
 
#just a small introduction
label maria_tulip_1_event(event):

    scene bg arena_quarters
    with dissolve

    define maria_c = Character("Maria Custard", show_two_window=True)
    define shizuka = Character('Masou Shizuka',
                window_left_padding=160,
                show_side_image= im.Scale("content/npc/arena/Masou Shizuka/portrait 0.png",150,150, xalign=0.0, yalign=1.0, show_two_window=True))
    
    
    "You walked around the arena quarters, when you saw a girl with an unusual weapon." 
    "She was going in your direction, so you decided to approach her and satisfy your curiosity."
    
    show npc maria_custard_novel
    with dissolve
    
    maria_c "Hi!"

    $ asked_fight_M = False    
    $ menuM_skip = False
    while not menuM_skip:
        menu:
            "Ask her about...?"
            "Are you one of the fighters?" if not asked_fight_M:
                $ asked_fight_M = True
                maria_c "Yup. I do participate with my friend Shizuka, but we usually stay out of the official ladders. {p}We are not here for the popularity."

            "So... what's the deal with that weapon of yours?":
                maria_c "That's Tulip Cannon, my own invention. <looks proudly>"
                maria_c "It's fueled with compound made primarily from Hirara Alloy, which helps the projectile to acquire a better muzzle velocity."
                maria_c "The PytFall representatives allowed me to test the new non-lethal ammunition in the city arena. \nIt seems to be working most of the time, it's so exciting!!"
                $ menuM_skip = True
            "<don't bother her anymore>":
                hide npc
                with dissolve
                "Nothing else caught your attention, so you left."
                return
    
    maria_c "And there's also..."
    shizuka "Maria! It's time to go!"
    maria_c "Coming! {w}Sorry..."
    
    hide npc
    with moveoutright
    
    "... {p}(most of the time, huh?)"
    "There was nothing else to do, so you left too."
    
    $ del menuM_skip
    $ del asked_fight_M
    return