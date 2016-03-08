###### j0
# quick navigation, search "j" + number, example: j0 - this panel
# 
#  1 - scold - insult (dumb, boring ugly, etc)
#  2 - scold - slut

###### j1
label interactions_insult:
    if char.disposition > 600:
        $ gm_disp_mult = 0.2
    elif char.disposition > 300:
        $ gm_disp_mult = 0.4
    elif char.disposition > 200:
        $ gm_disp_mult = 0.5
    elif char.disposition > 100:
        $ gm_disp_mult = 0.7
    elif char.disposition > 50:
        $ gm_disp_mult = 1
    elif char.disposition > 20:
        $ gm_disp_mult = 1
    elif char.disposition > -1:
        $ gm_disp_mult = 1
    elif char.disposition > -20:
        $ gm_disp_mult = 1        
    else:
        $ gm_disp_mult = 1
    
    $ char.disposition -= (randint(10, 22)*(gm_disp_mult))
    
    if ct("Mind Fucked"):
        $rc("<She ignores you.>")
    elif ct("Shy"):
        $ rc("Pl-please ... stop...", "Don't ... make fun of me.", "Uuuuuh <She starts crying>", "Well ... that ... <she looks like she wants to run away>", "Ah, I-I'm not… S-sorry…", "Really? I don't think… I-I'm sorry.", "<looks uncomfortable> No, I... umn... sorry.", "P-please, leave me be...")
    elif ct("Optimist") and ct("Lolita"):
        $rc("Eh? You sound like a perv!", "Booring!")
    elif ct("Kuudere"):
        $rc("You can stop talking now.", "Can't find something better to say?", "All talk and nothing to back it up. What are you even trying to do?")
    elif ct("Dandere"):
        $rc("...?", "That's...not true.", "I find that extremely hard to believe.", "Not funny.")
    elif ct("Tsundere"):
        $rc("What? I have no idea what you're talking about.", "Lay off the jokes; there's already one attached to the front of your head!")
    elif ct("Well-mannered"):
        $rc("Can we talk about something else?", "What a supremely boring joke. You've got awful taste.", "<looks unimpressed> Thank you...", "Thanks, but please leave me alone, I'm not interested", "I'm sorry, but I don't have time for this.", "*sigh*… thank you...<looks bored>", "Please, drop this flattery.", "I don't think you are being sincere.")
    elif ct("Strict Morals"):
        $rc("Don't try to pull the wool over my eyes. I know what you're after.", "Don't you have something better to do?", "What do you want, anyway?", "Are you making fun of me?")
    elif ct("Protective"):
        $rc("Whatever are you saying?", "That is simply not true.")
    elif ct("Energetic"):
        $rc("Eeh♪, I wouldn't say that ♪", "That can't be right, hey?", "Eh? But that's wrong, right?", "But that's not true at all?", "Eh? What are you talking about?")
    elif ct("Outgoing"):
        $rc("That's definitely not true, so relax, okay?")
    elif ct("Kind"):
        $rc("That's not true!", "Um... what are you talking about?")
    elif ct("Silly"):
        $rc("I don't understand, what?")
    elif ct("Loner"):
        $rc("Bigmouth.", "...What'd you want?", "…?", "What a bother...", "...You talk too much.", "Pathetic...", "<She completely ignores you>", "...and?")
    else:
        $ rc("Sorry, not interested.", "How many girls have you said that to today?", "Please, stop.", "Does that usually work?", "Don't mock me.", "...I'm sorry, did you say something?", "Can we end this conversation here?", "That doesn't sound sincere at all.", "U-um, you were talking to me? Oh ... <she's embarassed>", "You don't have to say things you don't mean.", "Don't try too hard, you'll hurt yourself.", "Settle down, slick.", "Too bad. I'm not going to fall for that.", "I've heard it all.", "Huhn, you're far too obvious.", "...What? Don't look at me", "Stop that. Empty praises won't do you any good.", "What is it? I don't get what you mean.", "Stop it already...", "Well... guess so. <unimpressed>", "You don't sound as if you mean it.", "......What?", "*sigh*…  I don't really have time for this.", "Huhn, who would fall for a line like that?", "And so?", "That gets you nowhere!", "I won't be fooled by beautiful words.", "Save your breath!", "Please, don't bother me.", "I couldn't care less about what you think.")
    
    jump girl_interactions
    

###### j2
label interactions_slut:
    
    if char.disposition > 400:
        $ gm_disp_mult = 0.2
    elif char.disposition > 550:
        $ gm_disp_mult = 0.4
    elif char.disposition > 450:
        $ gm_disp_mult = 0.7
    elif char.disposition > 400:
        $ gm_disp_mult = 1
    elif char.disposition > 350:
        $ gm_disp_mult = 1
    elif char.disposition > 200:
        $ gm_disp_mult = 1
    elif char.disposition > 100:
        $ gm_disp_mult = 1
    elif char.disposition > 20:
        $ gm_disp_mult = 1
    else:
        $ gm_disp_mult = 1
    
    $ char.disposition -= (randint(15, 35)*(gm_disp_mult))
    
    if ct("Mind Fucked"):
        $rc("Um..?")
    elif ct("Shy"):
        $rc("Ummm... Please don't look....", "D...don't... say that!", "D-don't say such strange things...", "Uu... Don't say such a thing...", "Uwaa! T-this is, that's... I'm, that's… Ugh…")
    elif ct("Well-mannered"):
        $rc("I can't really say I'm pleased.", "You are being weird. <Looks uncomfortable>", "Would you please refrain from commenting on me?")
    elif ct("Strict Morals"):
        $rc("It's a good idea to not talk like that, got it?", "Wipe that smug expression from your face.", "Cut that perverted talk.", "*sigh* Just be quiet, okay?")
    elif ct("Tsundere"):
        $rc("Y-you were thinking about something weird, weren't you?", "What are you talking about, geez...?")
    elif ct("Kuudere"):
        $rc("...Perv.", "Shut up. That's disgusting.")
    elif ct("Energetic"):
        $rc("D-don't stare! It's totally embarrassing...")    
    elif ct("Protective"):
        $rc("That's no good, you'll dampen the mood like that.")
    elif ct("Loner"):
        $rc("...Pervert.", "Weirdo...", "...annoying.", "...Shut up.", "Not for you.")
    elif ct("Frigid"):
        $rc("Wh-why are you looking at me with such perverted eyes...")
    else:
        $rc("What are you looking at, you idiot.", "I'll shut that annoying mouth of yours, physically.", "That was really kinky.", "What? Stop staring.", "*sigh*… Okay, that's enough…", "That was a bit over the top for a compliment.", "What are you saying, geez!", "Get lost, pervert!", "Hey, look at my eyes not my chest. OK?", "You're annoying...")    
    
    jump girl_interactions
    
