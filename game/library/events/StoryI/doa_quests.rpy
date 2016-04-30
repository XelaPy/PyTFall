init python:
    q = register_quest("Two Sisters", manual=True)
    register_event("two_sisters0", quest="Two Sisters", locations=["all"], trigger_type="doa_quest", dice=100)
    
label two_sisters0(event):
    $ pytfall.world_events.kill_event("two_sisters0", cached=True)
    show bg hiddenvillage_alley with dissolve
    "A distant alley at the far end of the village led you in a small garden."
    "Hearing a slight noise behind, you turn around."
    $ a = chars["Ayane"]
    $ a_spr = chars["Ayane"].get_vnsprite()
    $ a.override_portrait("portrait", "indifferent")
    show expression a_spr at center with dissolve
    a.say "Greetings, [hero.name]. My name is Ayane. Do not be alarmed, I have no intentions to attack you. I'm here to offer you a deal."
    "There was nothing there a moment ago, but now there is a young kunoichi standing before you."
    a.say "I ask for cooperation in a serious matter. Follow my instructions, and you will get a huge reward and my service, if you willing to hire me."
    "Her voice is cold as ice."
    a.say "Tell about it to anyone or follow my instructions incorrectly, and you'll never see me again. Until the moment I kill you."
    $ pytfall.world_quests.get("Two Sisters").next_in_label("Ayane, a cold kunoichi, proposed you a deal.")
    a.say "Or leave now and forget about this conversation."
    menu:
        "She stares at you, waiting for an answer"
        
        "Hear her out":
            a.say "Listen carefully then. Tomorrow you will come to the Pytfall tavern, find there a redhead kunoichi and tell her that her sister wants to talk to her. Then you will bring her here."
            "She hands you a small pill."
            a.say "Swallow it now, it needs time to to start working. Tomorrow it will protect you when you will help me to attack and capture her."
            a.say "Then you will get the following instructions and your reward. Like I said, don't tell anyone about it, unless you wish to die."
            hide expression a_spr with dissolve
            "She quickly leaves. Looks like you will be busy tomorrow."
            $ pytfall.world_quests.get("Two Sisters").next_in_label("You accepted it. Tomorrow you will have to find a redhead kunoichi in the city tavern.")
            $ register_event_in_label("two_sisters1", quest="Two Sisters", locations=["tavern_inside"], start_day=day + 1, dice=100)
            $ register_event_in_label("fail_two_sisters", locations=["all"], start_day=day + 2, run_conditions=["True"], trigger_type="auto")
            
        "Leave her be":
            hide expression a_spr with dissolve
            "Without wasting words you leave the garden. Almost immediately you hear another slight noise behind. The garden is empty again."
            $ pytfall.world_quests.get("Two Sisters").finish_in_label("You refused. You will not see her again.", "complete")
            
    return
    
label fail_two_sisters(event):
    $ pytfall.world_events.kill_event("two_sisters1", cached=True)
    $ pytfall.world_quests.get("Two Sisters").next_in_label("Sadly, you missed you chance to meet her.")
    $ pytfall.world_quests.fail_quest("Two Sisters")
    $ pytfall.world_events.kill_event("two_sisters2", cached=True)
    return