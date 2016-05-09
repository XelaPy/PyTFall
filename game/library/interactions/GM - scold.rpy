label interactions_insult:
    $ char.override_portrait("portrait", "angry")
    if ct("Impersonal"):
        $ rc("...I see that you have a hostility problem.", "I can't believe you can look me in the eyes and say those things.", "...Are you talking about me? I see, so that's what you think of me.")
    elif ct("Shy") and dice(50):
        $ rc("Th-That's terrible! It's way too much!", "Th-that's... so cruel of you to say...", "N-no way... you're horrible...", "T-That's not true!")
    elif ct("Imouto"):
        $ rc("Hah! Y-You think that kind of abuse will have any effect on m-me?", "I'm so pissed off!", "I-I... I'm not like that!", "LA LA I CAN'T HEAR YOU!") 
    elif ct("Dandere"):
        $ rc("...Are you trying to make me angry?", "...Are you teasing me?", "Do you want me to hate you that much?", "All bark and no bite. As they say.", "Was that meant to be an insult just now? How rude.")
    elif ct("Tsundere"):
        $ rc("You... you insolent swine!", "I-I will not forgive you!", "What was that?! Try saying that one more time!", "Hmph, I don't want to hear that from you!", "E-even if you say that, it doesn't mean anything to me, you know!"),
    elif ct("Kuudere"):
        $ rc("...What did you say? Who do you think you are?", "Oooh, it's ok for me to accept this as a challenge, right...?", "Shut your mouth. Or do you want me to shut it for you?", "Oh, do you want to get hurt that badly?")
    elif ct("Kamidere"):
        $ rc("Huhn? It seem you want to make me your enemy.", "Oh? Is your mouth all you know how to use?", "Bring your face over here so I can slap it!", "You're really trash, aren't you...")
    elif ct("Bokukko"):
        $ rc("What's that? Are you picking a fight with me?", "...Hey, you. You're ready for a pounding, yeah?", "Hey fucker, you trying to start a fight?!", "Oh, so talkin's all you're good at, huh...")
    elif ct("Ane"):
        $ rc("You shouldn't say things like that.", "Hmm, I didn't know you were the type to say things like that...", "My, you have some nerve.", "Good grief... Your parents did a terrible job raising you.")
    elif ct("Yandere"):
        $ rc("Hey, it would be better if you didn't talk like that.", "...You should... be careful, when walking at night.", "Please die and come back as a better person, for everyone's sake.")
    else:
        $ rc("Th-that's a terrible thing to say!", "Wh-why would you say that, that's so cruel...", "All talk and nothing to back it up. What are you even trying to do?", "What's your problem? Saying that out of nowhere.")
    $ char.restore_portrait()
    return
    
label interactions_apology_demand:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $ rc("Apologize. Then we'll talk.", "I won't forgive you unless you apologize.")
    elif ct("Shy") and dice(50):
        $ rc("Please apologize...", "Isn't there... something you want to apologize about first?")
    elif ct("Imouto"):
        $ rc("Umm, if you grovel in the dirt for me, I'll forgive you...", "I might consider forgiving you if you grovel pitifully.") 
    elif ct("Dandere"):
        $ rc("I'll forgive you if you apologize.", "Is it impossible for you to give an apology?", "...You should know that I haven't forgiven you just yet.")
    elif ct("Tsundere"):
        $ rc("It'd be nice if you apologized, you know...!", "...Apologize. AーPOーLOーGIZE!"),
    elif ct("Kuudere"):
        $ rc("What, not even a single word of apology?", "Until you apologize I'm not talking to you.")
    elif ct("Kamidere"):
        $ rc("Huh? Apologize first.", "Um... Where is my «I'm sorry»?")
    elif ct("Bokukko"):
        $ rc("Hm, finally feel like apologizin'?", "Hey, don't you think there's something you oughta be apologizing for?", "C'mon now, hurry up and apologize. It's for your own good, y'know?")
    elif ct("Ane"):
        $ rc("Oh dear, do you not know how to apologize?", "I will not forgive you until you reflect on what you've done.")
    elif ct("Yandere"):
        $ rc("Apologize. Did you not hear me? It means tell me you're sorry.", "...I demand an apology.")
    else:
        $ rc("Start apologizing, please! I'll let you know when it's enough.", "Hey, isn't there something you need to apologize for first...?")
    $ char.restore_portrait()
    return
    
label interactions_broken_promise:
    $ char.override_portrait("portrait", "sad")
    if ct("Impersonal"):
        $ rc("I suppose the promise was but lip service... after all.", "You don't keep promises, do you...")
    elif ct("Shy") and dice(50):
        $ rc("It's okay, I'm sure you have your priorities too, right...? But still...", "It's fine... I didn't think you'd show up anyway.")
    elif ct("Imouto"):
        $ rc("I was so lonely, all by myself...", "...I even waited for you.") 
    elif ct("Dandere"):
        $ rc("I was waiting forever...", "You promised...", "It seems I have been thoroughly fooled.")
    elif ct("Tsundere"):
        $ rc("Why didn't you come...? You idiot...", "You idiot! Liar! I can't believe this!"),
    elif ct("Kuudere"):
        $ rc("Tch. I guess a promise with me just isn't worth remembering, huh...", "「Is it too much for you to keep even a single promise?")
    elif ct("Kamidere"):
        $ rc("You're horrible... I was waiting the whole time...", "Jeez, why didn't you show up? Keep your promises!")
    elif ct("Bokukko"):
        $ rc("You're the kind of trash that can't even keep a little promise, aren't you.", "What d'you think promises are for?　Hmm?")
    elif ct("Ane"):
        $ rc("No, no, it's okay. Everyone has times when they can't make it...", "If you couldn't make it, I wish you'd just said so... Otherwise, it's just too cruel.")
    elif ct("Yandere"):
        $ rc("I waited so long for you... ", "...You never came. I waited so long and you never came!")
    else:
        $ rc("That's no good. You have to keep your promises...", "Jeez, how come you never came!")
    $ char.restore_portrait()
    return
