label special_items_slime_bottle:
    if not(hero.has_flag("slime_bottle")):
        $ hero.set_flag("slime_bottle", value=True)
    scene bg h_profile with dissolve
    menu:
        "An old bottle with unknown, thick liquid inside. Do you want to open it?"
        "Yes":
            "The seal is durable, but eventually it gives up, and pressurized fluid breaks out."
            if hero.level <= 10:
                $ levels = randint (5,15)
            else:
                $ levels = randint(15, 25) + hero.level/10
            $ new_slime = build_rc(id="Slime", level=levels, pattern=choice(["Warrior", "ServiceGirl"]))
            $ new_slime.disposition += 300
            $ hero.remove_item("Unusual Bottle")
            $ spr = new_slime.get_vnsprite()
            if hero.flag("slime_bottle"):
                $ new_slime.override_portrait("portrait", "happy")
                "The liquid quickly took the form of a girl."
                show expression spr at center with dissolve
                if dice(90):
                    $ new_slime.set_status("free")
                    new_slime.say "Finally someone opened it! Thanks a lot!"
                    new_slime.say "They promised me to smuggle me in the city, but something went gone wrong, and I was trapped there for months!"
                    new_slime.say "All I wanted is a steady job and a roof over my head..."
                    menu:
                        "Propose to work for you":
                            new_slime.say "Gladly!"
                            $ hero.add_char(new_slime)
                            "Looks like you have a new worker."
                        "Leave her be":
                            "Thanks again, [hero.name]."
                            hide expression spr with dissolve
                            "She leaves."
                else:
                    $ new_slime.set_status("slave")
                    new_slime.say "Oh, hello. Are you my new owner? I was told I will be transported to a new owner inside this bottle."
                    menu:
                        "Yes":
                            new_slime.say "It's a pleasure to serve you."
                            $ hero.add_char(new_slime)
                            "Looks like you have a new slave."
                        "No":
                            $ new_slime.override_portrait("portrait", "sad")
                            new_slime.say "Oh, this is bad... What should I do now? I guess I'll try to find my old master then..."
                            menu:
                                "Propose to become her owner":
                                    $ new_slime.override_portrait("portrait", "happy")
                                    $ hero.add_char(new_slime)
                                    new_slime.say "Of course! It's a pleasure to serve you."
                                    "Looks like you have a new slave."
                                "Leave her be":
                                    hide expression spr with dissolve
                                    "She leaves."
            else:
                $ new_slime.override_portrait("portrait", "angry")
                "The liquid quickly took the form of a girl."
                show expression spr at center with dissolve
                new_slime.say "AAAAGHHHHHH!"
                "She attack you!"
                $ new_slime.front_row = True
                $ enemy_team = Team(name="Enemy Team", max_size=3)
                $ enemy_team.add(new_slime)
                $ result = run_default_be(enemy_team, slaves=True, background="content/gfx/bg/be/b_dungeon_1.jpg", track="random", prebattle=True, death=True)
                if not(result):
                    jump game_over
                else:
                    scene bg h_profile
                    "You managed to beat her. Her liquid body quickly decays. Looks like she spent way too much time in that bottle..."
                    $ new_slime.health = 0
                    python:
                        for member in hero.team:
                            member.exp += adjust_exp(member, 200)
                        
        "No":
            "Maybe another time."
            jump char_equip
    $ new_slime.restore_portrait()
    if dice(50): # no easy save scumming
        $ hero.set_flag("slime_bottle", value=True)
    else:
        $ hero.set_flag("slime_bottle", value=False)
    jump char_equip
    
label special_items_empty_extractor:
    scene bg h_profile with dissolve
    if eqtarget.exp <= 2000:
        if eqtarget<>hero:
            $ spr = eqtarget.get_vnsprite()
            show expression spr at center with dissolve
            "Unfortunately, [eqtarget.name] is not experienced enough yet to share her knowledge with anybody."
        else:
            "Unfortunately, you are not experienced enough yet to share your knowledge with anybody."
        jump char_equip
    else:
        if eqtarget<>hero:
            $ spr = eqtarget.get_vnsprite()
            show expression spr at center with dissolve
            "This device will extract some of [eqtarget.name]'s experience."
            if eqtarget.disposition >0:
                $ eqtarget.disposition -= randint(25, 50)
            if eqtarget.joy >=55:
                $ eqtarget.joy -= 10
        else:
            "This device will extract some of your experience."
        menu:
            "Do you want to use it?"
            "Yes":
                if eqtarget<>hero:
                    "She slightly shudders when the device starts to work."
                    $ eqtarget.disposition -= randint(20, 30)
                else:
                    "For a moment you feel weak, but unpleasant pain somewhere inside your head."
                $ eqtarget.exp -= 2000
                $ eqtarget.remove_item("Empty Extractor", 1)
                $ eqtarget.add_item("Full Extractor", 1)
                "The device is full of energy."
            "No":
                $ pass
jump char_equip

label special_items_full_extractor:
    scene bg h_profile with dissolve
    if not(eqtarget.has_flag("exp_extractor")):
        $ eqtarget.set_flag("exp_extractor", value=day)
    elif eqtarget.flag("exp_extractor") == day:
        "You already transferred experience to this person today. It's very dangerous to do too often."
        jump char_equip
    if eqtarget<>hero:
        $ spr = eqtarget.get_vnsprite()
        show expression spr at center with dissolve
        "The energy of knowledge slowly flows inside [eqtarget.name]. She became more experienced."
        if eqtarget.disposition < 750:
            $ eqtarget.disposition += randint(25, 50)
        if eqtarget.joy <50:
            $ eqtarget.joy += 10
    else:
        "The energy of knowledge slowly flows inside you. You became more experienced."
    $ eqtarget.exp += 1500
    $ eqtarget.remove_item("Full Extractor", 1)
jump char_equip

label special_items_one_for_all:
    scene bg h_profile with dissolve
    if eqtarget.status <> "slave":
        "It would be unwise to use it on a free girl, unless you'd like to spend the rest of your live in prison."
        jump char_equip
    if eqtarget.health < 50 and eqtarget.mp < 50 and eqtarget.vitality < 50:
        "[eqtarget.name]'s body is in a poor condition. It will be a waste to use this item on her."
        jump char_equip
    $ health = eqtarget.health
    $ n=health/100
    if n>0:
        $ hero.add_item("Great Healing Potion", amount = n)
        $ health -= n*100
    $ n=health/50
    if n>0:
        $ hero.add_item("Healing Potion", amount = n)
        $ health -= n*50
    $ n=health/25
    if n>0:
        $ hero.add_item("Small Healing Potion", amount = n)
        $ health -= n*25
    if health > 0:
        $ hero.add_item("Small Healing Potion")
        
    $ mp = eqtarget.mp
    $ n=mp/100
    if n>0:
        $ hero.add_item("Great Mana Potion", amount = n)
        $ mp -= n*100
    $ n=mp/50
    if n>0:
        $ hero.add_item("Mana Potion", amount = n)
        $ mp -= n*50
    $ n=mp/25
    if n>0:
        $ hero.add_item("Small Mana Potion", amount = n)
        $ mp -= n*25
    if mp > 0:
        $ hero.add_item("Small Mana Potion")
        
    $ vitality = eqtarget.vitality
    $ n=vitality/100
    if n>0:
        $ hero.add_item("Great Potion of Serenity", amount = n)
        $ vitality -= n*100
    $ n=vitality/50
    if n>0:
        $ hero.add_item("Potion of Serenity", amount = n)
        $ vitality -= n*50
    $ n=vitality/25
    if n>0:
        $ hero.add_item("Small Potion of Serenity", amount = n)
        $ vitality -= n*25
    if vitality > 0:
        $ hero.add_item("Small Potion of Serenity")
    "[eqtarget.name]'s body crumbles as her life energies turn into potions."
    $ eqtarget.disposition -= 700
    $ eqtarget.health = 0
jump mainscreen

label special_items_herbal_extract:
    $ h = eqtarget.get_max("health")-eqtarget.health
    if h <= 0:
        scene bg h_profile with dissolve
        "There is no need to use it at the moment."
        jump char_equip
    if eqtarget.vitality <= 10:
        scene bg h_profile with dissolve
        "Not enough vitality to use it."
        jump char_equip
    if h<=eqtarget.vitality:
        $ eqtarget.health = eqtarget.get_max("health")
        $ eqtarget.vitality -= h
    else:
        $ eqtarget.health += eqtarget.vitality
        $ eqtarget.vitality = 0
$ eqtarget.remove_item("Herbal Extract", 1)
jump char_equip

label special_items_emerald_tincture:
    $ h = eqtarget.get_max("health")-eqtarget.health
    $ eqtarget.health += int(0.5*h)
    $ h = eqtarget.get_max("vitality")-eqtarget.vitality
    $ eqtarget.vitality += int(0.5*h)
    $ eqtarget.mp = 0
    jump char_equip
