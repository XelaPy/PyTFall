# The generic event for recapturing slaves that have escaped during look around actions.
#
label escaped_girl_recapture(event):
    # Get the specific girl
    $ char = pytfall.ra.get_look_around_girl(event)
    
    # If something goes wrong
    if char == None:
        hero.say "Wait is that?.."
        hero.say "Must be my imagnination..."
        return
    
    else:
        hero.say "Wait is that?..{w} It is!"
        
        "You sneak forwards carefully, trying hard not to alert your pray.\nWhen you get close enough..."
        
        hero.say "Ah ha!{nw}"
        
        char.say "Ah! What? No!{nw}"
        
        "You grab [char.name]'s arm and hold on tightly as she tries to struggle."
        
        hero.say "Found you. You won't be escaping again."
        
        char.say "..."
        
        # Return the girl to the player
        $ pytfall.ra.retrieve(char)
        
        return
    
