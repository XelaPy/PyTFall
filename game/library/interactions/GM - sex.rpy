###### j0
# quick navigation, search "j" + number, example: j0 - this panel
# 
#  1 - sex - fuck - GI
#  2 - sex - blowjob - GI
#  3 - sex - anal - GI
#  4 - sex - lesbo - GI
#  5 - sex - sex - GM

###### j1
label interactions_virgin_check:
    $ char.set_flag("raped", value="false")
    if check_lovers(hero, char) or char.disposition >= 700 or (char.flag("allowed_sex") == "True" and char.disposition >= 400):
        menu:
            "Looks like this is her first time. Do you want to continue?"
                        
            "Yes":
                call girl_virgin
                "You deflower her. Congratulations!"
                jump interactions_virgin_check_goon
                        
            "No":
                jump interaction_scene_choice
                    
    elif char.status == "slave" and (char.flag("allowed_sex") == "True" or char.disposition >= 250 or (cgo("SIW") and char.disposition >= 50)):
        menu: 
            "She warns you that this is her first time. She does not mind, but her value at the market might decrease. Do you want to continue?"
            
            "Yes":
                call girl_virgin
                "You deflower her. Congratulations!"
                jump interactions_virgin_check_goon
                        
            "No":
                jump interaction_scene_choice
                    
    elif char.status == "slave":
        menu: 
            "She tells you that this is her first time, and asks plaintively to do something else instead. You can force her, but it will not be without consequences. Do you want to use force?"
            
            "Yes":
                "You violated her."
                $ char.set_flag("raped", value="true")
                if ct("Masochist"):
                    $ libido += 10
                    $ char.joy += 5
                    $ char.disposition += 10
                else:
                    $ char.disposition -= 150
                    $ char.joy -= 50
                jump interactions_virgin_check_good
                        
            "No":
                jump interaction_scene_choice
    else:
        "Unfortunately she's still a virgin, and she's not ready to cease to be her yet."
        jump interaction_scene_choice
    
    label interactions_virgin_check_good:
        $ char.disposition += 20
        $ char.removetrait(traits["Virgin"])
        if char.health >=20:
            $ char.health -= 10
        else:
            $ char.vitality -= 20
        if char.flag("s_bg") == "beach":
            jump interactions_virgin_ok_beach
        elif char.flag("s_bg") == "park":
            jump interactions_virgin_ok_park
        else:
            jump interactions_virgin_ok_room
    jump interaction_scene_choice
    
label interactions_hireforsex:
    "You propose to pay her for sex."
    call interactions_check_for_bad_stuff
    if calling_interactions_end == 1:
        jump girl_interactions_end
    if char.flag("quest_no_sex") == "True":
        call int_sex_nope
        jump girl_interactions
    if char.disposition < -500:
        call int_sex_nope
        $ char.disposition -= randint(25, 45)
        jump girl_interactions
    if char.health < char.get_max("health")*0.5 or char.effects["Food Poisoning"]['active']:
        "But she is not feeling well."
        jump girl_interactions
    elif char.vitality < 60:
        "But she is too tired."
        jump girl_interactions
    $ price = round((char.oral + char.anal + char.vaginal + char.sex) * 0.5) - hero.charisma + char.charisma*5 - round(char.disposition * 0.1)
    if ct("Lesbian"):
        $ price = round((price+100) * 1.5)
    if price <= 0:
        "You managed to charm her and get free service."
        jump scene_sex_hired
    else:
        if hero.gold < price:
            "It will be [price] G. You don't have so much money."
            jump girl_interactions
        else:
            menu:
                "It will be [price] G. Continue?"
            
                "Yes":
                    if hero.take_money(price):
                        $ char.add_money(price)
                    $ char.set_flag("forced", value="false")
                    jump scene_sex_hired
                "No":
                    jump girl_interactions
label interactions_sex:
    "You proposing to have sex."
    call interactions_check_for_bad_stuff
    call interactions_check_for_minor_bad_stuff
    if char.flag("quest_cannot_be_fucked") == "True":
        call int_sex_nope
        jump girl_interactions
    if ct("Lesbian"):
        "But she is not interested in men."
        jump girl_interactions
    if (char.disposition >= 650 and check_friends(char, hero)) or (ct("Nymphomaniac") and char.disposition >= 400) or check_lovers(char, hero) or (char.flag("allowed_sex") == "True" and char.disposition >= 350):
        if char.vitality < 60:
            "But she is too tired."
            jump girl_interactions
        elif char.health < char.get_max("health")*0.5 or char.effects["Food Poisoning"]['active']:
            "But she is not feeling well."
            jump girl_interactions
    else:
        call int_sex_nope
        $ char.disposition -= randint(25, 45)
        jump girl_interactions
    $ char.set_flag("forced", value="false")

    if (char.disposition >= 600 and check_friends(char, hero)) or ct("Nymphomaniac") or check_lovers(char, hero):
        label scene_sex_hired:
        menu:
            "Where would you like to do it?"
            
            "Beach":
                show bg city_beach with fade
                $ char.set_flag("s_bg", value="beach")
            "Park":
                show bg city_park with fade
                $ char.set_flag("s_bg", value="park")
            "Room":
                show bg girl_room with fade
                $ char.set_flag("s_bg", value="room")
    elif (char.status == "slave") and (ct("Shy") or ct("Dandere")):
        "She is too shy to it anywhere. You can force her nevertheless, but the prefers her room."
        menu:
            "Where would you like to do it?"
            
            "Beach":
                show bg city_beach with fade
                $ char.set_flag("s_bg", value="beach")
                $ char.set_flag("forced", value="true")
            "Park":
                show bg city_park with fade
                $ char.set_flag("s_bg", value="park")
                $ char.set_flag("forced", value="true")
            "Room":
                show bg girl_room with fade
                $ char.set_flag("s_bg", value="room")
    elif char.status == "slave":
        "She is not comfortable with doing it outdoors. You can force her nevertheless, but the prefers her room."
        menu:
            "Where would you like to do it?"
            
            "Beach":
                show bg city_beach with fade
                $ char.set_flag("s_bg", value="beach")
                $ char.set_flag("forced", value="true")
            "Park":
                show bg city_park with fade
                $ char.set_flag("s_bg", value="park")
                $ char.set_flag("forced", value="true")
            "Room":
                show bg girl_room with fade
                $ char.set_flag("s_bg", value="room")
    elif ct("Shy") or ct("Dandere"):
        "She's too shy to do it anywhere. You go into her room."
        show bg girl_room with fade
        $ char.set_flag("s_bg", value="room")
    elif ct("Homebody"):
        "She doesn't want to do it outdoors, so you go into her room."
        show bg girl_room with fade
        $ char.set_flag("s_bg", value="room")
    else:
        "She wants to do it in her room."
        show bg girl_room with fade
        $ char.set_flag("s_bg", value="room")

    if char.flag("s_bg") == "beach":
        if dice(50):
            $ gm.generate_img("beach", "nude", "swimsuit", exclude=["sex", "sleeping", "angry", "in pain", "indoors", "onsen", "pool", "stage", "dungeon", "bathing"], type="first_default")
        else:
            $ gm.generate_img("swimsuit", "nude", "simple bg",  exclude=["sex", "sleeping", "angry", "in pain", "indoors", "onsen", "pool", "stage", "dungeon", "bathing"], type="first_default")
    elif char.flag("s_bg") == "park":
        if dice(50):
            $ gm.generate_img("nature", "nude", exclude=["sex", "sleeping", "angry", "in pain", "indoors", "beach", "onsen", "pool", "stage", "dungeon", "bathing"], type="first_default")
        else:
            $ gm.generate_img("nude", "simple bg", exclude=["sex", "sleeping", "angry", "in pain", "indoors", "beach", "onsen", "pool", "stage", "dungeon", "bathing"], type="first_default")
    else:
        if dice(30):
            $ gm.generate_img("living", "nude", "lingerie", exclude=["sex", "sleeping", "angry", "in pain", "outdoors", "beach", "onsen", "pool", "stage", "dungeon", "public", "bathing"], type="first_default")
        elif dice(30):
            $ gm.generate_img("living", "no clothes", exclude=["sex", "sleeping", "angry", "in pain", "outdoors", "beach", "onsen", "pool", "stage", "dungeon", "public", "bathing"], type="first_default")
        else:
            $ gm.generate_img("nude", "no clothes", "simple bg", exclude=["sex", "sleeping", "angry", "in pain", "outdoors", "beach", "onsen", "pool", "stage", "dungeon", "public", "bathing"], type="first_default")
            
    $ sex_count = 0
    $ les_count = 0
    $ guy_count = 0
    $ girl_count = 0
    $ together_count = 0
    $ cum_count = 0
    if ct("Nymphomaniac"):
        $libido = 55
    elif ct("Frigid"):
        $libido = 20
    else:
        $libido = 35
    if ct ("Messy"):
        $libido += 5
    if check_lovers(hero, char):
        $libido += 20
    if char.flag("forced") == "true" and ct("Masochist"):
        $libido += 10
    elif char.flag("forced") == "true":
        $libido -= 10
        $ char.joy -= 15
    if cgo("SIW"):
        $libido += 10
    call int_sex_ok    
label interaction_scene_choice:
    if char.vitality <=0:
        jump interaction_scene_finish_sex
    if hero.vitality <= 20:
        "You are too tired to continue."
        jump interaction_scene_finish_sex
    if char.status == "slave":
        if libido <= 0:
            "She doesn't want to do it any longer. You can force her, but it will not be without consequences."
        if char.joy <= 10:
            "She looks upset. Not the best mood for sex. You can force her, but it will not be without consequences."
        if char.vitality <= 25:
            "She looks very tired. You can force her, but it's probably for the best to let her rest."
    else:
        if libido <= 0:
            "She doesn't want to do it any longer."
            jump interaction_scene_finish_sex
        elif char.joy <= 10:
            "She looks upset. Not the best mood for sex."
            jump interaction_scene_finish_sex
        if char.vitality < 50:
            "She is too tired to continue."
            jump interaction_scene_finish_sex
    
    menu:
        "What would you like to do now?"
        
        "Ask for striptease" if char.flag("s_bg") == "beach" and (char.has_image("stripping", "beach", type="first_default") or char.has_image("stripping", "simple bg", exclude=["stage"], type="first_default") or char.has_image("nude", "beach", exclude=["sleeping", "angry", "in pain", "sad"], type="first_default")):
            if char.has_image("stripping", "beach", type="first_default"):
                $ gm.set_img("stripping", "beach", type="first_default")
            elif char.has_image("stripping", "simple bg", exclude=["stage"], type="first_default"):
                $ gm.set_img("stripping", "simple bg", type="first_default")
            else:
                $ gm.set_img("nude", "beach", exclude=["sleeping", "angry", "in pain", "sad"], type="first_default")
            jump interaction_scene_strip
        "Ask for striptease" if char.flag("s_bg") == "park" and (char.has_image("stripping", "nature", type="first_default") or char.has_image("stripping", "simple bg", exclude=["stage"], type="first_default") or char.has_image("nude", "nature", exclude=["sleeping", "angry", "in pain", "sad"], type="first_default")):
            if char.has_image("stripping", "nature", type="first_default"):
                $ gm.set_img("stripping", "nature", type="first_default")
            elif char.has_image("stripping", "simple bg", exclude=["stage"], type="first_default"):
                $ gm.set_img("stripping", "simple bg", type="first_default")
            else:
                $ gm.set_img("nude", "nature", exclude=["sleeping", "angry", "in pain", "sad"], type="first_default")
            jump interaction_scene_strip
        "Ask for striptease" if char.flag("s_bg") == "room" and (char.has_image("stripping", "living", type="first_default") or char.has_image("stripping", "simple bg", exclude=["stage"], type="first_default") or char.has_image("nude", "living", exclude=["sleeping", "angry", "in pain", "sad"], type="first_default") or char.has_image("stripping", "indoors", exclude=["sleeping", "angry", "in pain", "sad", "dungeon", "public"], type="first_default")):
            if char.has_image("stripping", "living", type="first_default"):
                $ gm.set_img("stripping", "living", type="first_default")
            elif char.has_image("stripping", "simple bg", exclude=["stage"], type="first_default"):
                $ gm.set_img("stripping", "simple bg", exclude=["stage"], type="first_default")
            elif char.has_image("nude", "living", exclude=["sleeping", "angry", "in pain", "sad"], type="first_default"):
                $ gm.set_img("nude", "living", exclude=["sleeping", "angry", "in pain", "sad"], type="first_default")
            else:
                $ gm.set_img("stripping", "indoors", exclude=["sleeping", "angry", "in pain", "sad", "dungeon", "public"], type="first_default")
            jump interaction_scene_strip
        "Ask to play with herself" if char.flag("s_bg") == "beach" and (char.has_image("masturbation", "beach", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default") or char.has_image("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")):
            if char.has_image("masturbation", "beach", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default"):
                $ gm.set_img("masturbation", "beach", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
            else:
                $ gm.set_img("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
            jump interaction_scene_mast
        "Ask to play with herself" if char.flag("s_bg") == "park" and (char.has_image("masturbation", "nature", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default") or char.has_image("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")):
            if char.has_image("masturbation", "nature", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default"):
                $ gm.set_img("masturbation", "nature", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
            else:
                $ gm.set_img("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
            jump interaction_scene_mast
        "Ask to play with herself" if char.flag("s_bg") == "room" and (char.has_image("masturbation", "living", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default") or char.has_image("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default") or char.has_image("masturbation", "indoors", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered", "dungeon", "public"], type="first_default")):
            if char.has_image("masturbation", "living", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default"):
                $ gm.set_img("masturbation", "living", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
            elif char.has_image("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default"):
                $ gm.set_img("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
            else:
                $ gm.set_img("masturbation", "indoors", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered", "dungeon", "public"], type="first_default")
            jump interaction_scene_mast
        "Ask for blowjob" if char.flag("s_bg") == "beach" and (char.has_image("bc blowjob", "beach", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc blowjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "beach", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("bc blowjob", "beach", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc blowjob", "partnerhidden", "beach", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("bc blowjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc blowjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("after sex", "beach", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("after sex", "beach", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ gm.set_img("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            jump interaction_scene_blowjob
        "Ask for blowjob" if char.flag("s_bg") == "park" and (char.has_image("bc blowjob", "nature", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc blowjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "nature", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("bc blowjob", "nature", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc blowjob", "partnerhidden", "nature", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("bc blowjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc blowjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("after sex", "nature", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("after sex", "nature", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ gm.set_img("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            jump interaction_scene_blowjob
        "Ask for blowjob" if char.flag("s_bg") == "room" and (char.has_image("bc blowjob", "living", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc blowjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc blowjob", "indoors", exclude=["rape", "angry", "in pain", "dungeon", "public"], type="first_default") or char.has_image("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("bc blowjob", "living", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc blowjob", "partnerhidden", "living", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("bc blowjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc blowjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ gm.set_img("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            jump interaction_scene_blowjob
        "Ask for titsjob" if char.flag("s_bg") == "beach" and (char.has_image("bc titsjob", "beach", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc titsjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "beach", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("bc titsjob", "beach", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc titsjob", "partnerhidden", "beach", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("bc titsjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc titsjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("after sex", "beach", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("after sex", "beach", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ gm.set_img("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            jump interaction_scene_titsjob
        "Ask for titsjob" if char.flag("s_bg") == "park" and (char.has_image("bc titsjob", "nature", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc titsjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "nature", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("bc titsjob", "nature", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc titsjob", "partnerhidden", "nature", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("bc titsjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc titsjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("after sex", "nature", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("after sex", "nature", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ gm.set_img("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            jump interaction_scene_titsjob
        "Ask for titsjob" if char.flag("s_bg") == "room" and (char.has_image("bc titsjob", "living", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc titsjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc titsjob", "indoors", exclude=["rape", "angry", "in pain", "dungeon", "public"], type="first_default") or char.has_image("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("bc titsjob", "living", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc titsjob", "partnerhidden", "living", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("bc titsjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc titsjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ gm.set_img("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            jump interaction_scene_titsjob
        "Ask for handjob" if char.flag("s_bg") == "beach" and (char.has_image("bc handjob", "beach", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc handjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "beach", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("bc handjob", "beach", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc handjob", "partnerhidden", "beach", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("bc handjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc handjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("after sex", "beach", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("after sex", "beach", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ gm.set_img("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            jump interaction_scene_handjob
        "Ask for handjob" if char.flag("s_bg") == "park" and (char.has_image("bc handjob", "nature", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc handjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "nature", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("bc handjob", "nature", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc handjob", "partnerhidden", "nature", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("bc handjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc handjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("after sex", "nature", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("after sex", "nature", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ gm.set_img("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            jump interaction_scene_handjob
        "Ask for handjob" if char.flag("s_bg") == "room" and (char.has_image("bc handjob", "living", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc handjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc handjob", "indoors", exclude=["rape", "angry", "in pain", "dungeon", "public"], type="first_default") or char.has_image("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("bc handjob", "living", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc handjob", "partnerhidden", "living", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("bc handjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc handjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ gm.set_img("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            jump interaction_scene_handjob
        "Ask for footjob" if char.flag("s_bg") == "beach" and (char.has_image("bc footjob", "beach", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc footjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "beach", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("bc footjob", "beach", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc footjob", "partnerhidden", "beach", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("bc footjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc footjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("after sex", "beach", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("after sex", "beach", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ gm.set_img("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            jump interaction_scene_footjob
        "Ask for footjob" if char.flag("s_bg") == "park" and (char.has_image("bc footjob", "nature", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc footjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "nature", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("bc footjob", "nature", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc footjob", "partnerhidden", "nature", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("bc footjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc footjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("after sex", "nature", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("after sex", "nature", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ gm.set_img("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            jump interaction_scene_footjob
        "Ask for footjob" if char.flag("s_bg") == "room" and (char.has_image("bc footjob", "living", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc footjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("bc footjob", "indoors", exclude=["rape", "angry", "in pain", "dungeon", "public"], type="first_default") or char.has_image("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("bc footjob", "living", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc footjob", "partnerhidden", "living", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("bc footjob", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("bc footjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            elif char.has_image("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ gm.set_img("after sex", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            jump interaction_scene_footjob
        "Ask for vaginal sex" if char.flag("s_bg") == "beach" and (char.has_image("2c vaginal", "beach", "straight", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("2c vaginal", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default")):
            if ct("Virgin"):
                jump interactions_virgin_check
            label interactions_virgin_ok_beach:
                if char.has_image("2c vaginal", "beach", "straight", exclude=["rape", "angry", "in pain"], type="first_default"):
                    $ gm.set_img("2c vaginal", "partnerhidden", "beach", exclude=["rape", "angry", "in pain", "gay"], type="first_default")
                else:
                    $ gm.set_img("2c vaginal", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain", "gay"], type="first_default")
                jump interaction_scene_vaginal
        "Ask for vaginal sex" if char.flag("s_bg") == "park" and (char.has_image("2c vaginal", "nature", "straight", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("2c vaginal", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default")):
            if ct("Virgin"):
                jump interactions_virgin_check
            label interactions_virgin_ok_park:
                if char.has_image("2c vaginal", "nature", "straight", exclude=["rape", "angry", "in pain"], type="first_default"):
                    $ gm.set_img("2c vaginal", "partnerhidden", "nature", exclude=["rape", "angry", "in pain", "gay"], type="first_default")
                else:
                    $ gm.set_img("2c vaginal", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain", "gay"], type="first_default")
                jump interaction_scene_vaginal
        "Ask for vaginal sex" if char.flag("s_bg") == "room":
            if ct("Virgin"):
                jump interactions_virgin_check
            label interactions_virgin_ok_room:
                if char.has_image("2c vaginal", "living", "straight", exclude=["rape", "angry", "in pain"], type="first_default"):
                    $ gm.set_img("2c vaginal", "partnerhidden", "living", exclude=["rape", "angry", "in pain", "gay"], type="first_default")
                elif char.has_image("2c vaginal", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default"):
                    $ gm.set_img("2c vaginal", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain", "gay"], type="first_default")
                elif char.has_image("2c vaginal", "indoors", "straight", exclude=["rape", "angry", "in pain", "dungeon", "public"], type="first_default"):
                    $ gm.set_img("2c vaginal", "partnerhidden", "indoors", exclude=["rape", "angry", "in pain", "gay", "dungeon", "public"], type="first_default")
                else:
                    $ gm.set_img("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default")
                jump interaction_scene_vaginal
        "Ask for anal sex" if char.flag("s_bg") == "beach" and (char.has_image("2c anal", "beach", "straight", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("2c anal", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("2c anal", "beach", "straight", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("2c anal", "partnerhidden", "beach", exclude=["rape", "angry", "in pain", "gay"], type="first_default")
            else:
                $ gm.set_img("2c anal", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain", "gay"], type="first_default")
            jump interaction_scene_anal
        "Ask for anal sex" if char.flag("s_bg") == "park" and (char.has_image("2c anal", "nature", "straight", exclude=["rape", "angry", "in pain"], type="first_default") or char.has_image("2c anal", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default")):
            if char.has_image("2c anal", "nature", "straight", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("2c anal", "partnerhidden", "nature", exclude=["rape", "angry", "in pain", "gay"], type="first_default")
            else:
                $ gm.set_img("2c anal", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain", "gay"], type="first_default")
            jump interaction_scene_anal
        "Ask for anal sex" if char.flag("s_bg") == "room":
            if char.has_image("2c anal", "living", "straight", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("2c anal", "partnerhidden", "living", exclude=["rape", "angry", "in pain", "gay"], type="first_default")
            elif char.has_image("2c anal", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default"):
                $ gm.set_img("2c anal", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain", "gay"], type="first_default")
            elif char.has_image("2c anal", "indoors", "straight", exclude=["rape", "angry", "in pain", "dungeon", "public"], type="first_default"):
                $ gm.set_img("2c anal", "partnerhidden", "indoors", exclude=["rape", "angry", "in pain", "gay", "dungeon", "public"], type="first_default")
            else:
                $ gm.set_img("after sex", "living", exclude=["rape", "angry", "in pain"], type="first_default")
            jump interaction_scene_anal
        "Ask for some hot lesbo action" if find_les_partners() and char.flag("s_bg") == "room":
            jump interactions_lesbian_choice
        "That's all.":
            "You decided to finish."
            
            # $ sex_count = 0
            # $ guy_count = 0
            # $ girl_count = 0
            # $ together_count = 0
            # $ cum_count = 0
            label interaction_scene_finish_sex:
                if libido >= 15 and char.vitality >= 35:
                    if char.flag("s_bg") == "beach":
                        if dice(50):
                            $ gm.set_img("masturbation", "beach", exclude=["rape", "angry", "in pain"], type="first_default")
                        else:
                            $ gm.set_img("masturbation", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")

                    elif char.flag("s_bg") == "park":
                        if dice(50):
                            $ gm.set_img("masturbation", "nature", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
                        else:
                            $ gm.set_img("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
                    else:
                        if dice(50):
                            $ gm.set_img("masturbation", "living", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
                        else:
                            $ gm.set_img("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
                    "She is not satisfied yet, so she quickly masturbates to decrease libido."
                    $ char.disposition -= round(libido*0.5)
                if char.vitality <=0:
                    if char.flag("s_bg") == "beach":
                        $ gm.set_img("rest", "beach", "sleeping", "tired", exclude=["angry", "in pain"], type="first_default")
                    elif char.flag("s_bg") == "park":
                        $ gm.set_img("rest", "nature", "sleeping", "tired", exclude=["angry", "in pain"], type="first_default")
                    else:
                        $ gm.set_img("rest", "living", "sleeping", "tired", exclude=["angry", "in pain"], type="first_default")
                    "She fainted from fatigue. You cannot continue any longer."
                    $ char.disposition = randint(4, 10)
                if (together_count > 0 and sex_count >=2) or (sex_count >=4 and girl_count >=2 and guy_count >= 2):
                    if char.flag("s_bg") == "beach":
                        $ gm.set_img("profile", "happy", "beach")
                    elif char.flag("s_bg") == "park":
                        $ gm.set_img("profile", "happy", "nature")
                    else:
                        $ gm.set_img("profile", "happy", "indoors", "living")
                    call after_good_sex
                    $ char.set_flag("allowed_sex", value="True")
                    $ char.disposition += randint(40, 70)
                    $ char.joy += randint(20, 50)
                    $ char.vitality -= 30
                elif girl_count < 1 and guy_count > 0:
                    if char.flag("s_bg") == "beach":
                        $ gm.set_img("profile", "sad", "beach")
                    elif char.flag("s_bg") == "park":
                        $ gm.set_img("profile", "sad", "nature")
                    else:
                        $ gm.set_img("profile", "sad", "indoors", "living")
                    "She's not statisfied at all."
                    call girl_never_come
                    $ char.disposition -= randint(20, 50)
                    $ char.joy -= randint(20, 50)
                    $ char.vitality -= 25
                elif girl_count > 0 and guy_count < 1 and cum_count < 1 and sex_count > 0:
                    if char.flag("s_bg") == "beach":
                        $ gm.set_img("profile", "shy", "beach")
                    elif char.flag("s_bg") == "park":
                        $ gm.set_img("profile", "shy", "nature")
                    else:
                        $ gm.set_img("profile", "shy", "indoors", "living")
                    "She was unable to satisfy you."
                    call guy_never_came
                    $ char.disposition += randint(10, 20)
                    $ char.joy -= randint(10, 30)
                    $ char.vitality -= 25
                elif girl_count > 0 and (cum_count >=5 or (cum_count > girl_count)):
                    if char.flag("s_bg") == "beach":
                        $ gm.set_img("profile", "confident", "beach")
                    elif char.flag("s_bg") == "park":
                        $ gm.set_img("profile", "confident", "nature")
                    else:
                        $ gm.set_img("profile", "confident", "indoors", "living")
                    call guy_cum_alot
                    $ char.disposition += randint(20, 40)
                    $ char.joy += randint(20, 40)
                    $ char.vitality -= 20
                elif (sex_count < 1) and (guy_count < 1) and (girl_count < 1) and (les_count < 1):
                    if char.flag("s_bg") == "beach":
                        $ gm.set_img("profile", "sad", "angry", "beach")
                    elif char.flag("s_bg") == "park":
                        $ gm.set_img("profile", "sad", "angry", "nature")
                    else:
                        $ gm.set_img("profile", "sad", "angry", "indoors", "living")
                    if char.status == "slave":
                        "She is puzzled and confused by the fact that you didn't do anything. She quickly leaves, probably thinking that you teased her."
                    else:
                        "She is quite upset and irritated because you didn't do anything. She quickly leaves, probably thinking that you teased her."
                    $ char.disposition -= randint(40, 70)
                    $ char.joy -= randint(20, 50)
                    $ char.vitality -= 5
                elif girl_count > 0 and sex_count < 1 and les_count < 1:
                    if char.flag("s_bg") == "beach":
                        $ gm.set_img("profile", "shy", "beach")
                    elif char.flag("s_bg") == "park":
                        $ gm.set_img("profile", "shy", "nature")
                    else:
                        $ gm.set_img("profile", "shy", "indoors", "living")
                    "She did nothing but masturbated in front of you. Probably better than nothing, but be prepared for rumors about your impotence or orientation."
                    $ char.disposition -= randint(30, 50)
                    $ char.joy -= randint(15, 25)
                    $ char.vitality -= 5
                elif les_count > 0 and sex_count < 1:
                    if char.flag("s_bg") == "beach":
                        $ gm.set_img("profile", "shy", "beach")
                    elif char.flag("s_bg") == "park":
                        $ gm.set_img("profile", "shy", "nature")
                    else:
                        $ gm.set_img("profile", "shy", "indoors", "living")
                    "She wonders why you didn't do a thing except watching her and her partner."
                    if ct("Lesbian") or ct("Bisexual"):
                        "She had her fun though, so no hard feelings."
                        $ char.joy = randint(5, 15)
                        $ char.vitality -= 5
                    else:
                        "Without your involvement she's not satisfied at all."
                        $ char.disposition -= randint(20, 50)
                        $ char.joy -= randint(20, 50)
                        $ char.vitality -= 25
                else:
                    if char.flag("s_bg") == "beach":
                        $ gm.set_img("profile", "happy", "beach")
                    elif char.flag("s_bg") == "park":
                        $ gm.set_img("profile", "happy", "nature")
                    else:
                        $ gm.set_img("profile", "happy", "indoors", "living")
                    "It was pretty good, and she looks quite pleased and satisfied. But there is room for improvement."
                    $ char.set_flag("allowed_sex", value="True")
                    $ char.disposition += randint(20, 40)
                    $ char.joy += randint(20, 30)
                    $ char.vitality -= 20

                $ gm.restore_img()
            jump girl_interactions_end
            
label interactions_lesbian_choice:
    # The interactions itself.
    # Since we called a funciton, we need to do so again (Consider making this func a method so it can be called just once)...
    if ct("Lesbian") or ct("Bisexual"):
        if char.disposition <= 500 or not(check_friends(hero, char) or check_lovers(hero, char)):
            "Unfortunately she does not want to do it for you."
            if char.status == "slave":
                "Even if you force her and some other girl, it won't look natural. Too bad."
            jump interaction_scene_choice
        elif check_lovers(hero, char):
            "She gladly agrees to make a show for you."
        elif check_friends(hero, char) or char.disposition > 600:
            "A bit hesitant, she agrees to do it for you."
    else:
        if char.disposition <= 600 or not(check_friends(hero, char) or check_lovers(hero, char)) or not(cgo("SIW")): 
            "Unfortunately she does not like girls in this way."
            if char.status == "slave":
                "Even if you force her and some other girl, it won't look natural. Too bad."
            jump interaction_scene_choice
        elif check_lovers(hero, char):
                "She gladly agrees to make a show for you if there will be some stright sex as well today."
        elif (check_friends(hero, char) or char.disposition > 600) and cgo("SIW"):
                "She prefers men, but agrees to make a show for you if there will be some straight sex as well today."
    $ les_count += 1
    $ willing_partners = find_les_partners()
    
    # Single out one partner randomly from a set:
    $ char2 = random.sample(willing_partners, 1)[0]
    
    # We painly hide the interactions screen to get rid of the image and gradient:
    hide screen pyt_girl_interactions
    
    $ char_sprite = char.get_vnsprite()
    $ char_sprite2 = char2.get_vnsprite()
    "[char.nickname] decided to call [char2.nickname] for the lesbo action!"
    
    show expression char_sprite at mid_left with dissolve
    char.say "We are going to do 'it'."
    show expression char_sprite at mid_right as char_sprite with move
    show expression char_sprite2 at mid_left as char_sprite2 with dissolve
    char2.say "And..."
    extend "(*looking at you*) Are you planning to watch?"
    
    hide char_sprite
    hide char_sprite2
    with dissolve
    
    # Resize images to be slightly smaller than half a screen in width and the screen in height. ProportionalScale will do the rest.
    $ resize = (config.screen_width/2 - 75, config.screen_height - 75)
    
    
    show expression char.show("nude", "simple bg", resize=resize, exclude=["sex", "sleeping", "angry", "in pain", "beach", "onsen", "pool", "stage", "dungeon", "bathing"], type="first_default") as xxx at Transform(align=(0, 0.5)) with moveinright
    show expression char2.show("nude", "simple bg", resize=resize, exclude=["sex", "sleeping", "angry", "in pain", "beach", "onsen", "pool", "stage", "dungeon", "bathing"], type="first_default") as xxx2 at Transform(align=(1.0, 0.5)) with moveinleft
    
    # Wait for 0.25 secs and add soundbyte:
    pause 0.25
    play events "female/orgasm.mp3"
    $ renpy.pause(5.0)
    hide xxx
    hide xxx2
    

    show expression char2.get_vnsprite() at left as char_sprite2 with dissolve
    show expression char.get_vnsprite() at right as char_sprite with dissolve
    if libido <= 0:
        $ char.vitality -= 20
        $ char.joy -= 5
    if char.joy <= 10:
        $ char.disposition -= 5
    if char.vitality <= 15 and char.health >= 50:
        $ char.health -= 2
    if char.oral < 100 and char.sex < 100 and char2.oral < 100 and char2.sex < 100:
        "They both were not skilled enough to give each other enough pleasure, no matter how they tried. That was quite awkward."
        $ char.oral += randint (0,1)
        $ char2.oral += randint (0,1)
        $ char.sex += randint (0,1)
        $ char2.sex += randint (0,1)
        $ char.vitality -= 20
        $ char2.vitality -= 20
        $ libido -= 5
        char2.say "..."
        char.say "Sorry..."
    elif char.oral < 100 and char.sex < 100:
        "[char.nickname] was not skilled enough to make her partner come. On the bright side, [char2.nickname] made her come a lot."
        $ char.oral += randint (2,4)
        $ char2.oral += randint (2,4)
        $ char.sex += randint (0,1)
        $ char2.sex += randint (0,1)
        $ char.vitality -= 20
        $ char2.vitality -= 15
        $ libido -= 10
        char.say "Sorry..."
        char2.say "Don't worry. You'll become better in time."
    elif char2.oral < 100 and char2.sex < 100:
        "[char2.nickname] was not skilled enough to make her partner come. On the bright side, [char.nickname] made her come a lot."
        $ char.oral += randint (2,4)
        $ char2.oral += randint (2,4)
        $ char.sex += randint (0,1)
        $ char2.sex += randint (0,1)
        $ char.vitality -= 20
        $ char2.vitality -= 15
        $ libido -= 10
        char2.say "I'm sorry..."
        char.say "Don't be. We had our fun (*looking at you*)."
    else:
        "They both come a lot. What a beautiful sight."
        $ char.oral += randint (2,4)
        $ char2.oral += randint (2,4)
        $ char.sex += randint (2,4)
        $ char2.sex += randint (2,4)
        $ char.vitality -= 15
        $ char2.vitality -= 15
        $ libido -= 10
        $ char.joy += 5
        $ char2.joy += 5
        char2.say "That... wasn't so bad."
        char2.say "We should do that again sometime ♪"
    hide char_sprite2 with dissolve
    hide char_sprite with dissolve
    
    # Restore the gm image:
    
    # Show the screen again:
    show screen pyt_girl_interactions
    
    # And finally clear all the variables for global scope:
    python:
        del resize
        del char2
        del willing_partners
        
    stop events
        
    # And we're all done!:
    jump interaction_scene_choice
    
    

label interaction_scene_blowjob:
    if libido <= 0:
        $ char.vitality -= 20
        $ char.joy -= 5
    if char.joy <= 10:
        $ char.disposition -= 5
    if char.vitality <= 15 and char.health >= 50:
        $ char.health -= 2
    "She licks and sucks your dick until you come."
    if char.oral < 50:
        "She clearly needs more training, so it took some time. But at least she learned something new."
        $ char.oral += randint (3, 5)
        $ hero.oral += randint (0, 1)
        $ char.vitality -= 30
        $ hero.vitality -= 30
        $ libido -= 5
    elif char.oral < 300:
        "It was pretty good."
        $ char.oral += randint (2, 4)
        $ hero.oral += randint (0, 2)
        $ char.vitality -= 25
        $ hero.vitality -= 25
        $ char.joy += 1
        $ libido -= 5
    elif char.oral < 1000:
        "It was very good."
        $ char.oral += randint (1, 3)
        $ hero.oral += randint (1, 3)
        $ char.vitality -= 25
        $ hero.vitality -= 25
        $ char.joy += 1
    else:
        "She was so good that you came after a few seconds. Wow."
        $ char.oral += randint (0, 2)
        $ hero.oral += randint (1, 4)
        $ char.vitality -= 20
        $ hero.vitality -= 20
        $ char.joy += 2
        $ libido += 5
        $ sex_count += 1
        $ guy_count +=1
    if (char.oral - hero.oral) > 200:
        "You learned something new about oral as well. A pleasure to deal with professionals."
        $ hero.oral += 2
    elif (hero.oral - char.oral) > 200:
        "You were able to show her some new tricks."
        $ char.oral += 2
    $ sex_count += 1
    $ guy_count +=1
    $ cum_count += 1
    jump interaction_scene_choice
        
label interaction_scene_titsjob:
    if libido <= 0:
        $ char.vitality -= 20
        $ char.joy -= 5
    if char.joy <= 10:
        $ char.disposition -= 5
    if char.vitality <= 15 and char.health >= 50:
        $ char.health -= 2
    "She stimulates your dick with her soft breasts until you come."
    if char.oral < 50 or char.sex < 50:
        "She clearly needs more training, so it took some time. But at least she learned something new."
        $ char.oral += randint (1, 4)
        $ char.sex += randint (1, 4)
        $ hero.sex += randint (0, 1)
        $ char.vitality -= 30
        $ hero.vitality -= 30
        $ libido -= 5
    elif char.oral < 300 or  char.sex < 300:
        "It was pretty good."
        $ char.oral += randint (1, 3)
        $ char.sex += randint (1, 3)
        $ hero.sex += randint (0, 1)
        $ char.vitality -= 25
        $ hero.vitality -= 25
        $ char.joy += 1
        $ libido -= 5
    elif char.oral < 1000 or char.sex < 1000:
        "It was very good."
        $ char.oral += randint (1, 2)
        $ char.sex += randint (1, 2)
        $ hero.sex += randint (1, 2)
        $ char.vitality -= 25
        $ hero.vitality -= 25
        $ char.joy += 1
    else:
        "She was so good that you came after a few seconds. Wow."
        $ char.oral += randint (0, 2)
        $ char.sex += randint (0, 2)
        $ hero.sex += randint (1, 3)
        $ char.vitality -= 20
        $ hero.vitality -= 20
        $ char.joy += 2
        $ libido += 5
    if (char.oral - hero.oral) > 200 or (char.sex - hero.sex) > 200:
        "You learned something new about titsjob as well. A pleasure to deal with professionals."
        $ hero.oral += 1
        $ hero.sex += 1
    elif (hero.oral - char.oral) > 200:
        "You were able to show her some new tricks."
        $ char.oral += 1
        $ char.sex += 1
    $ sex_count += 1
    $ guy_count +=1
    $ cum_count += 1
    jump interaction_scene_choice
    
label interaction_scene_handjob:
    if libido <= 0:
        $ char.vitality -= 20
        $ char.joy -= 5
    if char.joy <= 10:
        $ char.disposition -= 5
    if char.vitality <= 15 and char.health >= 50:
        $ char.health -= 2
    "She stimulates your dick with her hands until you come."
    if char.sex < 50:
        "She clearly needs more training, so it took some time. But at least she learned something new."
        $ char.sex += randint (3, 5)
        $ hero.sex += randint (0, 1)
        $ char.vitality -= 30
        $ hero.vitality -= 30
        $ libido -= 5
    elif char.sex < 300:
        "It was pretty good."
        $ char.sex += randint (2, 4)
        $ hero.sex += randint (0, 2)
        $ char.vitality -= 25
        $ hero.vitality -= 25
        $ char.joy += 1
        $ libido -= 5
    elif char.sex < 1000:
        "It was very good."
        $ char.sex += randint (1, 3)
        $ hero.sex += randint (1, 2)
        $ char.vitality -= 25
        $ hero.vitality -= 25
        $ char.joy += 1
    else:
        "She was so good that you came after a few seconds. Wow."
        $ char.sex += randint (0, 2)
        $ hero.sex += randint (1, 3)
        $ char.vitality -= 20
        $ hero.vitality -= 20
        $ char.joy += 2
        $ libido += 5
    if (char.sex - hero.sex) > 200:
        "You learned something new about handjob as well. A pleasure to deal with professionals."
        $ hero.sex += 2
    elif (hero.sex - char.sex) > 200:
        "You were able to show her some new tricks."
        $ char.sex += 2
    $ sex_count += 1
    $ guy_count +=1
    $ cum_count += 1
    jump interaction_scene_choice
    
label interaction_scene_footjob:
    if libido <= 0:
        $ char.vitality -= 20
        $ char.joy -= 5
    if char.joy <= 10:
        $ char.disposition -= 5
    if char.vitality <= 15 and char.health >= 50:
        $ char.health -= 2
    "She stimulates your dick with her feet until you come."
    if char.sex < 50:
        "She clearly needs more training, so it took some time. But at least she learned something new."
        $ char.sex += randint (3, 5)
        $ hero.sex += randint (0, 1)
        $ char.vitality -= 30
        $ hero.vitality -= 30
        $ libido -= 5
    elif char.sex < 300:
        "It was pretty good."
        $ char.sex += randint (2, 4)
        $ hero.sex += randint (0, 2)
        $ char.vitality -= 25
        $ hero.vitality -= 25
        $ char.joy += 1
        $ libido -= 5
    elif char.sex < 1000:
        "It was very good."
        $ char.sex += randint (1, 3)
        $ hero.sex += randint (1, 2)
        $ char.vitality -= 25
        $ hero.vitality -= 25
        $ char.joy += 1
    else:
        "She was so good that you came after a few seconds. Wow."
        $ char.sex += randint (0, 2)
        $ hero.sex += randint (1, 3)
        $ char.vitality -= 20
        $ hero.vitality -= 20
        $ char.joy += 2
        $ libido += 5
    if (char.sex - hero.sex) > 200:
        "You learned something new about footjob as well. A pleasure to deal with professionals."
        $ hero.sex += 2
    elif (hero.sex - char.sex) > 200:
        "You were able to show her some new tricks."
        $ char.sex += 2
    $ sex_count += 1
    $ guy_count +=1
    $ cum_count += 1
    jump interaction_scene_choice
    
label interaction_scene_mast:
    if libido <= 0:
        $ char.vitality -= 20
        if char.health >= 30:
            $ char.health -= 10
        $ char.joy -= 5
    if char.joy <= 10:
        $ char.disposition -= 5
    if char.vitality <= 15 and char.health >= 50:
        $ char.health -= 2
    "She masturbates in front of you. Although it cannot be considered as a sexual act, you both are more aroused now."
    if libido <= 10:
        $ libido += 10
    else:
        $ libido += 5
    $ char.vitality -= 20
    $ girl_count +=1
    jump interaction_scene_choice
    
label interaction_scene_vaginal:
    if libido <= 0:
        $ char.vitality -= 20
        if char.health >= 30:
            $ char.health -= 10
        $ char.joy -= 5
    if char.joy <= 10:
        $ char.disposition -= 5
    if char.vitality <= 15 and char.health >= 50:
        $ char.health -= 2
    if char.flag("raped") == "true":
        "She crying with pain and grief when you deflower her. Soon, however, her slave training is doing its job, and her hips begin to move in rhythm with you."
    if char.vaginal < 50 and hero.vaginal >= 50:
        "You fuck her pussy until she comes. She's still too inexperienced, so you were unable to come properly. Oh well, at least she learned something new."
        $ char.vaginal += randint (3, 5)
        $ hero.vaginal += randint (0, 1)
        $ char.vitality -= 50
        $ hero.vitality -= 60
        $ libido -= 10
        $ sex_count += 1
        $ girl_count +=1
    elif char.vaginal >= 50 and hero.vaginal < 50:
        "You fuck her pussy until you come. Unfortunately you didn't have enough skill to make her come as well. She looks disappointed."
        $ hero.vaginal += randint (1, 2)
        $ char.vitality -= 60
        $ hero.vitality -= 50
        $ char.joy -= 10
        $ libido -= 5
        $ sex_count += 1
        $ guy_count +=1
    elif char.vaginal < 50 and hero.vaginal < 50:
        "You fuck her pussy for some time until you both realized that you are not skillful enough to make each other properly come. It would be funny if it wasn't so sad."
        $ char.vaginal += randint (0, 1)
        $ hero.vaginal += randint (0, 1)
        $ char.vitality -= 60
        $ hero.vitality -= 60
        $ libido -= 5
        $ char.joy -= 10
        $ sex_count += 1
    elif char.vaginal < 500 and hero.vaginal < 500:
        "You fuck her wet pussy until you both come. It was pretty good."
        $ char.vaginal += randint (2, 4)
        $ hero.vaginal += randint (0, 2)
        $ char.vitality -= 50
        $ hero.vitality -= 50
        $ char.joy += 5
        $ libido -= 10
        $ sex_count += 1
        $ guy_count +=1
        $ girl_count +=1
    elif char.vaginal >= 500 and hero.vaginal < 500:
        "You fuck her wet pussy until you both come. You did it much earlier, and noticed a light self-confident smile on her face."
        $ char.vaginal += randint (1, 4)
        $ hero.vaginal += randint (1, 2)
        $ char.vitality -= 40
        $ hero.vitality -= 50
        $ char.joy += 5
        $ libido -= 10
        $ sex_count += 1
        $ guy_count +=1
        $ girl_count +=1
    elif char.vaginal < 500 and hero.vaginal =< 500:
        "You fuck her wet pussy until you both come. She did it much earlier, looks like she enjoyed it a lot."
        $ char.vaginal += randint (1, 4)
        $ hero.vaginal += randint (1, 2)
        $ char.vitality -= 50
        $ hero.vitality -= 40
        $ char.joy += 10
        $ libido -= 10
        $ sex_count += 1
        $ guy_count +=1
        $ girl_count +=1
    elif char.vaginal < 1000 or hero.vaginal < 1000:
        "You fuck her wet pussy until you both come. It was very good."
        if dice (round((char.vaginal + hero.vaginal)* 0.05)):
            "You managed to come simultaneously!"
            $ char.joy += 5
            $ char.vaginal += randint (0, 1)
            $ hero.vaginal += randint (0, 1)
            $ together_count += 1
        $ char.vaginal += randint (1, 3)
        $ hero.vaginal += randint (1, 3)
        $ char.vitality -= 45
        $ hero.vitality -= 45
        $ char.joy += 10
        $ libido -= 10
        $ sex_count += 1
        $ guy_count +=1
        $ girl_count +=1
    else:
        "You fuck her wet pussy until you both simultaneously come multiple times. It was fabulous."
        $ char.vaginal += randint (1, 2)
        $ hero.vaginal += randint (1, 3)
        $ together_count += 1
        $ char.vitality -= 40
        $ hero.vitality -= 40
        $ char.joy += 15
        $ libido -= 15
        $ sex_count += 1
        $ guy_count +=2
        $ girl_count +=2
    if (char.vaginal - hero.vaginal) > 300:
        "You learned something new about vaginal sex as well. A pleasure to deal with professionals."
        $ hero.vaginal += 2
    elif (hero.vaginal - char.vaginal) > 300:
        "You were able to show her some new tricks."
        $ char.vaginal += 2
    jump interaction_scene_choice
    
label interaction_scene_anal:
    if libido <= 0:
        $ char.vitality -= 20
        if char.health >= 30:
            $ char.health -= 10
        $ char.joy -= 5
    if char.joy <= 10:
        $ char.disposition -= 5
    if char.vitality <= 15 and char.health >= 50:
        $ char.health -= 2
    if char.anal < 50 and hero.anal >= 50:
        "You fuck her ass until she comes. She's still too inexperienced, so you were unable to come properly, and it was quite painful for her. Oh well, at least she learned something new."
        $ char.anal += randint (3, 5)
        $ hero.anal += randint (0, 1)
        $ char.vitality -= 55
        $ hero.vitality -= 60
        $ char.joy -=10
        if char.health > 30:
            $ char.health -= 5
        $ libido -= 5
        $ sex_count += 1
        $ girl_count +=1
    elif char.anal >= 50 and hero.anal < 50:
        "You fuck her ass until you come. Unfortunately you didn't have enough skill to make her come, and it was quite painful for her. She looks disappointed."
        $ hero.anal += randint (1, 2)
        $ char.vitality -= 60
        $ hero.vitality -= 55
        $ char.joy -= 20
        $ libido -= 5
        if char.health > 30:
            $ char.health -= 5
        $ sex_count += 1
        $ guy_count +=1
    elif char.anal < 50 and hero.anal < 50:
        "You fuck her ass for some time until you both realized that you are not skillful enough to make each other properly come. It was an unpleasant and painful experience for both of you."
        $ char.anal += randint (1, 3)
        $ hero.anal += randint (1, 3)
        $ char.vitality -= 60
        $ hero.vitality -= 60
        $ libido -= 5
        $ char.joy -= 25
        $ sex_count += 1
        if char.health > 35:
            $ char.health -= 10
    elif char.anal < 500 and hero.anal < 500:
        "You fuck her tight ass until you both come. It was pretty good."
        $ char.anal += randint (2, 4)
        $ hero.anal += randint (0, 2)
        $ char.vitality -= 50
        $ hero.vitality -= 50
        $ char.joy += 5
        $ libido -= 10
        $ sex_count += 1
        $ guy_count +=1
        $ girl_count +=1
    elif char.anal >= 500 and hero.anal < 500:
        "You fuck her tight ass until you both come. You did it much earlier, and noticed a small self-confident smile on her face."
        $ char.anal += randint (1, 4)
        $ hero.anal += randint (1, 2)
        $ char.vitality -= 45
        $ hero.vitality -= 50
        $ char.joy += 5
        $ libido -= 10
        $ sex_count += 1
        $ guy_count +=1
        $ girl_count +=1
    elif char.anal < 500 and hero.anal =< 500:
        "You fuck her tight ass until you both come. She did it much earlier, looks like she enjoyed it a lot."
        $ char.anal += randint (1, 4)
        $ hero.anal += randint (1, 2)
        $ char.vitality -= 50
        $ hero.vitality -= 45
        $ char.joy += 10
        $ libido -= 10
        $ sex_count += 1
        $ guy_count +=1
        $ girl_count +=1
    elif char.anal < 1000 or hero.anal < 1000:
        "You fuck her tight ass until you both come. It was very good."
        if dice (round((char.anal + hero.anal)* 0.05)):
            "You managed to come simultaneously!"
            $ char.joy += 5
            $ char.anal += randint (0, 1)
            $ hero.anal += randint (0, 1)
            $ together_count += 1
        $ char.anal += randint (1, 3)
        $ hero.anal += randint (1, 3)
        $ char.vitality -= 45
        $ hero.vitality -= 45
        $ char.joy += 10
        $ libido -= 10
        $ sex_count += 1
        $ guy_count +=1
        $ girl_count +=1
    else:
        "You fuck her tight ass until you both simultaneously come multiple times. It was fabulous."
        $ char.anal += randint (1, 2)
        $ hero.anal += randint (1, 3)
        $ together_count += 1
        $ char.vitality -= 40
        $ hero.vitality -= 40
        $ char.joy += 15
        $ libido += -15
        $ sex_count += 1
        $ guy_count +=2
        $ girl_count +=2
    if (char.anal - hero.anal) > 300:
        "You learned something new about anal sex as well. A pleasure to deal with professionals."
        $ hero.anal += 2
    elif (hero.anal - char.anal) > 300:
        "You were able to show her some new tricks."
        $ char.anal += 2
    jump interaction_scene_choice
    
label interaction_scene_strip:
    if libido <= 0:
        $ char.vitality -= 20
        $ char.joy -= 5
    if char.joy <= 10:
        $ char.disposition -= 5
    "You ask her to show you striptease."
    if char.strip < 50:
        "She tried her best, but the moves were clumsy and unnatural. At least she learned something new though."
        $ char.strip += randint (3, 5)
        $ char.joy -= 10
        $ char.vitality -= 30
        $ libido -= 5
    elif char.strip < 300:
        "It's nice to look at her graceful and elegant moves."
        $ char.strip += randint (1, 3)
        $ hero.strip += randint (0, 1)
        $ char.vitality -= 35
        $ libido += 5
    elif char.strip < 1000:
        "Her movements are so fascinating that you cannot look away from her. She looks proud and pleased."
        $ char.strip += randint (1, 2)
        $ hero.strip += randint (1, 2)
        $ char.vitality -= 20
        $ char.joy += 10
        $ libido += 5
    else:
        "She looks unbearably hot and sexy. After a short time you cannot withstand it anymore and begin to masturbate, quickly coming. She looks at you with a smile and superiority in the eyes."
        $ char.strip += randint (0, 1)
        $ hero.strip += randint (1, 4)
        $ char.vitality -= 20
        $ char.joy += 15
        $ libido += 10
        $ guy_count +=1
    if (char.strip - hero.strip) > 200:
        "You learned something new about striptease as well. A pleasure to deal with professionals."
        $ hero.strip += 2
    elif (hero.strip - char.strip) > 200:
        "You were able to show her some new tricks."
        $ char.strip += 2
    jump interaction_scene_choice
        

label int_sex_ok:
    $ char.override_portrait("portrait", "shy")
    if ct("Half-Sister") and dice(40):
        if ct("Impersonal"):
            $rc("I'll take in all your cum, brother.", "Sex with my brother, initiation.", "Let's have incest.", "Even though we're siblings... it's fine to do this, right?", "Let's deepen our bond as siblings.")
        elif ct("Shy") and dice(40):
            $rc("Umm... anything is fine as long as it's you... brother.", "I-if it's you, b-brother, then anything you do makes me feel good.")
        elif ct("Masochist") and dice(40):
            $rc("Are you going to violate me now, brother? Please?", "I'll be your slut any time you wish, brother.", "Hehe, would you prefer your sister to be to be an obedient girl?")
        elif ct("Imouto"):
            $rc("Teach me more things, brother!", "Brother, teach me how to feel good!", "Sis... will try her best.", "Sister's gonna show you her skills as a woman.")
        elif ct("Dandere"):
            $rc("Ah... actually, your sister have been feeling sexually frustrated lately...", "Brother, please do me.", "Even though we're related, we can have sex if we love each other.", "I'm only doing this because you're my brother.", "I'll do whatever you want for you, brother.", "Brother can do anything with me...", "I-is it alright to do something like that with my brother?")
        elif ct("Kuudere"):
            $rc("I... I can't believe I'm doing it with my brother...", "Y-you're lusting for your sister? O-okay, you can be my sex partner.", "I... I don't mind doing it although we're siblings, but...")
        elif ct("Tsundere"):
            $rc("Ugh... I... I have such a lewd brother!", "O... only you are allowed to touch me, brother.", "I... I'm only doing this because you're hard, brother.", "Doing something like this... with my brother... But... truth be told...")
        elif ct("Kamidere"):
            $rc("B...brother...it's... it's wrong to do this...!", "E...even though we're siblings...", "Doing such a thing to my brother. Am I a bad big sister?")
        elif ct("Yandere"):
            $rc("Make love to me, brother. Drive me mad.", "I'm looking forward to see your face writhing in mad ecstacy, bro.", "Shut up and yield yourself to your sister.", "Bro, you're a perv. It runs in the family though.", "Man, who'd have thought that my brother is as perverted as I am...", "My brother is in heat.  That's wonderful.", "As long as the pervy brother has a pervy sis as well, all is right with the world.", "Damn... The thought of incest gets me all excited now...")
        elif ct("Ane"):
            $rc("This is how you've always wanted to claim me, isn't it?", "Doing such things to your sister... Well, it can't be helped...", "Sis will do her best.", "Let sis display her womanly skills.")
        elif ct("Bokukko"):
            $rc("You wanted to have sex with your sister so bad, huh?", "Have you been planning to do this? Man, what a hopeless brother you are...", "I'm gonna show you that I'm a woman too, bro.", "Right on, brother.  Better you just shut up and don't move.", "Leave this to me, you can rely on sis.", "As long as it's for my brother a couple of indecent things is nothing.")
        else:
            $rc("It's alright for siblings to do something like this.", "Make your sister feel good.", "Just for now, we're not siblings... we're just... a man and a woman.", "We're brother and sister. What we're doing now must remain an absolute secret.", "I'll do my best. I want you to feel good, brother.", "I bet our parents would be so mad.")
       
    elif ct("Impersonal"):
        $rc("...Please insert to continue.", "You are authorized so long as it does not hurt.", "You can do me if you want.", "So, I'll begin the sexual interaction...", "Understood. I will... service you…", "I dedicate this body to you.", "Understood. Please demonstrate your abilities.")
    elif ct("Shy") and dice(40):
        $rc("D-do you mean…  Ah, y-yes…  If I'm good enough…", "Eeh?! Th-that's... uh... W- well... I do... want to...", "O...okay. I'll do my best.", "I-I was thinking… That I wanted to be one with you…", "If it's you, I'm fine with anything...", "I too... wanted to be touched by you... ","I want my feelings…  To reach you…", "It's... it's... o-okay to... have... s--s-sex... with me...", "Uh... I... h...how should I say this... It... it'll be great if you could do it gently...", "Aah... p... please... I... I want it... I... I can't think of anything else now!", "I-I'll do my best... for your sake!", "Uhm... I want you... to be gentle...", "Um, I-I want to do it… Please treat me well…", "Uh, uhm, how should I...? Eh? You want it like this...? O-okay! Then, h-here I go…", "Eeh, i-is it ok with someone like me...?", "Sorry if I'm no good at this...", "Uh... p... please... d...do it for me... my whole body's aching right now...", "Umm... anything is fine as long as it's you...", "Umm… please do perverted things to me…", "I don't know how well I will do...")
    elif ct("Nymphomaniac") and dice(40):
        $rc("Come on, I'll do the same for you, so please hurry and do me.", "Ahh, I can't wait anymore... quickly... please do me fast…", "I've been waiting for you all this time, so hurry up.", "Ready anytime you are.", "Please fill my naughty holes with your hot shaft.", " Let's do it all night long, okay? ...What, I'm just a dirty-minded girl~ ♪", "I don't mind. I really loooove to have sex. ♪", "Just watching is boring, right?  So… ♪", "...Shit! Now I'm horny as hell! ...Hey? You up for a go?", "Whenever, wherever…", "If you'd made me wait any longer I would have violated you myself.", "You know, had you kept me waiting any longer I would probably have jumped you myself.", "I hope you know how to handle a pussy...", "Man, who'd have thought that you are as perverted as I am...", "Ah... actually, I have been feeling sexually frustrated lately...", "Aah~~ Geez, I can't hold it anymore! Let's fuck!", "Hyauh…  Geez, do you have any idea how long I've been wet?", "Finally!", "You can ask me as much as you like... We can do it again... and again...", "...These perverted feelings... You can make them go away, can't you...?", "Umm, I-I'm always ready for it, so...!", "Turn me into a sloppy mess...!", "Let's do it! Right now! Take off your clothes! Hurry!", "Hmmm, what should I do～? ...Do you wanna do it THAT much～? I guess there's no stopping it～", "eah, it's okay. If that's what you want. Besides... I kinda like this stuff.", "Whatー, you want to do it tooー... Sure, let's do itー♪", "Mm, I might be able to learn some new tricks... Okay, fine by me!")
    elif ct("Masochist") and dice (25):
        $rc("Feel free to make me your personal bitch slave!", "Geez～, you could have just taken me by force～...", "Kya~... I - am - being - molested -... Oh come on, at least play along a little bit...")
    elif ct("Sadist") and dice(25):
            $rc("Become my... sex slave ♪", "Just shut up and surrender yourself to me. Good boy.", "Stay still and let me violate you.", "Come. I'll be gentle with you.")
    elif ct("Tsundere"):
        $rc("*gulp*… W-well... since you're begging to do it with me, I suppose we can…", "It...it can't be helped, right? It... it's not that I like you or anything!", "I-it's not like I want to do it! It's just that you seem to want to do it so much…", "I'll punish you if I don't feel good, got it?", "Hhmph... if...if you wanna do it... uh... go all the way with it!", "Hm hmm! Be amazed at my fabulous technique!", "If you're asking, then I'll listen… B-but it's not like I actually want to do it, too!", "I-I'm actually really good at sex! So... I-I'd like to show you…", "I...I'm only doing it because of your happy face.", "Humph! I'll show you I can do it!", "If-if you say that you really, really want it… Then I won't turn you down…", "L.... leave it to me... you idiot...", "If you want to do it now, it's okay… I just don't want to do anything weird in front of other people.", "Th-things like that should only happen after marriage… but… fine, I'll do it…", "God, people like you… Are way too honest about what they want…", "T...that can't be helped, right? B...but that doesn't mean you can do anything you like!", "You're hopeless.... Well, fine then....", "...Yes, yes, I'll do it, I'll do it so…  geez, stop making that stupid face…", "Geez, you take anything you can get...")
    elif ct("Dandere"):
        $rc("...Very well then. Please go ahead and do as you like.", "I... want you inside me.", "You're welcome to... do that.", "You can do whatever you want to me.", "I'm going to make you cum. You had better prepare yourself.", "I will not go easy on you.", "I... I'm ready for sex.", "Make me feel good...", "...If you do it, be gentle.", "I will handle... all of your urges...", "Then…  I will do it with you…", "...If you want, do it now.", "...I want to do it, too.", "...How do you want it?  ...Okay, I can do it…", "Now is your chance...")
    elif ct("Kuudere"):
        $rc("...I don't particularly mind.", "Heh. I'm just a girl too, you know. Let's do it.", "...V-Very well. I will neither run nor hide.", "Don't forget that I'm a woman after all...", "What a bothersome guy... Alright, I get it.", "...Fine, just don't use the puppy-dog eyes.", "*sigh* ...Fine, fine! I'll do it as many times as you want!", "Fine with me… Wh-what? ...Even I have times when I want to do it…", "I-I'll make sure to satisfy you...!", "If you wanna do it just do what you want.")
    elif ct("Imouto"):
        $rc("Ehehe... It's ok? Doing it...", "Ehehe, I'm going to move a lot for you... ♪", "[char.name] will show you the power of love♪", "I can do naughty stuff, you know? ...Want to see?", "Uhuhu, Well then, I'll be really nice to you, ok? ♪", "Uhuhu, Well then, what should I tease first~ ♪", "Okayyy! Let's love each other a lot. ♪", "Hey? You want to? You do, don't you? We can do it, if you waaaaant~", "Aah... I want you… To love me lots…", "Ehehe♪ Prepare to receive loads and loads of my love! ♪", "Hold me really tight, kiss me really hard, and make me feel really good. ♪", "Aha, When I am with a certain someone, I do only naughty things~… Uhuhu ♪", "Yeah, let's make lots of love♪", "I-is it okay for me to climb onto you? I'm sorry if I'm heavy...", "I-I'll do my best to pleasure you!", "Yes. I'm happy that I can help make you feel good.", "I don't know how well I will do...", "Geez, you're so forceful...♪")
    elif ct("Ane"):
        $rc("Hmhm, what is going to happen to me, I wonder?", "Come on, show me what you've got...", "This looks like it will be enjoyable.", "If you can do this properly... I'll give you a nice pat on the head.", "Seems like you can't help it, huh...", "Fufufu, please don't overdo it, okay?", "Go ahead and do it as you like, it's okay.", "Very well, I can show you a few things... Hmhm.")
    elif ct("Bokukko"):
        $rc("Right, yeah... As long as you don't just cum on your own, sure, let's do it", "Y-yeah… I sort of want to do it, too... ehehe…", "Wha!? C-can you read my mind...?", "Ah, eh, right now?", "Okay... but I'll do it like I want, kay?" ,"...Okay, that's it! I can't stand it! I've gotta fuck ya!", "S-sure… Ehehe, I'm, uh, kind of interested, too…", "Hey, let's do it while we got some time to kill...?", "Hehee, just leave it all to me! I'll make this awesome!", "Gotcha, sounds like a plan!", "Hey, maybe… The two of us could have an anatomy lesson?", "Is that ok? Ehehe... I wanted to do it too…", "Huhu… I want to do it with a pervert like you.", "Ehehe… In that case, let's go hog wild~", "Ehehe… So... let's do it. ♪", "Hmph... if you'd like, I'll give ya' some lovin'. ♪", "Got'cha. Hehe. Now I won't go easy on you.", "Y-yeah... if we're going to do it, we should do it now...", "Huhuh, I sort of want to do it now...", "Hey, er…  Wanna try doing it with me...?", "Well, I s'pose once in a while wouldn't hurtー♪")
    elif ct("Yandere"):
        $rc("Yes, let's have passionate sex, locked together♪", "Hehe. How should I make you feel good?", "If we have sex you will never forget me, right?♪", "Please do your best... if it's you, it'll be okay.", "Heh heh... You're going to feel a lot of pleasure. Try not to break on me.", "Alright, I'll just kill some time playing around with your body...", "Feel grateful for even having the opportunity to touch my body.", "Huhuh, I'll kill you with my tightness...", "You're lewd～♪")
    elif ct("Kamidere"):
        $rc("*giggle* I'll give you a feeling you'll never get from anyone else…", "Oh? You seem quite confident. I'm looking forward to this. ♪", "You're raring to go, aren't you? Very well, let's see what you've got.", "Now then, show me sex appropriate to someone qualified to be my lover...", "Hhmn... My, my... you love my body so much? Of course you do, it can't be helped.", "Oh, you seem to understand what I want from you,.. Good doggy, good doggy ♪", "Be sure to make me feel good, got it?", "Then you're bored, too.", "Feel grateful for even having the opportunity to touch my body.", "You won't be able to think about anybody else besides me after I'm done with you.", "Huhuhu, having sex with me… pretty cheeky for a pet dog~ ♪", "Hmph, Entertain me the best you can…", "Hmph, I'll prove that I'm the greatest you'll ever have...", "...For now, I'm open to the idea.", "Huhuh, I'll be using you until I'm satisfied...", "Huhu, you can't cum until I give you permission, okay? So, get ready to endure it~ ♪", "I don't really want to, but since you look so miserable I'll allow it.", "For me to get in this state... I can't believe it...", "Haa, in the end, it turned out like this…  Fine then, do as you like…")
    else:
        $rc("Oh... I guess if you like me it's ok.", "Fufu… I hope you are looking forward to this…!", "For you, I'll do my best today as well, okay?", "If it's with you... I'd do it, you know...?", "If you're so fascinated with me, let's do it.", "Hn, I want you to feel really good, okay...", "If we're going to do it, then let's make it the best performance possible. Promise?", "Now, let us discover the shape of our love. ♪", "Let's... feel good together...", "Huhn, if you do it, then… please make sure it feels good…", "Huhu, so here we are…  you can't hold it anymore, right?", "Then… Let's do it? ♪", "Sex... O-okay, let's do it...", "I don't mind. Now get yourself ready before I change my mind.", "Please let me make you feel good...", "What do you think about me, let your body answer for you…", "If you feel like it, do what you want, with my body…", "Ok, I'll serve you! ♪", "Now, [char.name] shall give you some pleasure ~ !", "Want to become one with me? …ok", "You're this horny...? Fine, then…", "If that's what you desire...", "Oh? You've already become like this? Heh, heh... ♪", "Okay… I'd like to.", "That expression on your face... Hehe, do you wanna fuck me that much?", "You insist, hm? Right away, then!", "Heh, how can I say no?", "Hum, What should we do? ...That, there? ..hmm", "I want to do so many dirty things... I can't hold it back...", "Huhuhu, I'll give you a really. Good. Time. ♪", "You can't you think of anything else beside having sex? You're such a perv~", "So you want to do it. Right. Now? Huhu... I very much approve. ♪", "You mean, like, have sex and stuff? ...Hmm~?  Meh, you pass!", "What? You want to do it? Geez, you're so hopeless... ♪", "Come on, I can tell that you're horny… Feel free to partake of me.", "Huhn, fine, do me to your heart's content.", "Um, if you'd like, I can do it for you… I'll do my best!", "I know you wanna feel good too. ...huhu, come here…", "I can't wait any more… Huhu, look how wet I am just thinking about you... ♪", "S-shut up and... entrust your body to me… Okay?", "You've got good intuition. That was just what I had in mind, Huhuh. ♪", "Haa, your lust knows no bounds...", "Huhu, ok then… Surrender yourself to me…", "Now... show me the dirty side of you…", "You really like it, don't you… Huhuh, okay, let's go.", "Y-yes… I don't mind letting you do as you please…", "I want to do it with you...", "Hn…  Looking at you... makes me want to do it…", "If the one corrupting my body is you, then I'll have no regrets.", "Yes. Go ahead and let my body overwhelm you.", "... Leave it to me...", "I'll do it. You better be prepared.", "I wanna do all kinds of dirty things to you. Just let yourself go, okay?", " Leave it to me... I'll make you cum so much.", "All right. Do as you like.", "Let's deepen our love for each other.", "Please, go ahead and do it.", "Are we going... All the way?", "Yup. That's the way. You need more love.", "Not good... I want to do perverted things so badly, I can't stand it...", "Sure, if you want", "Hey... do me...", "I-if it's with you... I'd go skin to skin...") 
    $ char.restore_portrait()
    return


label int_sex_nope:
    $ char.override_portrait("portrait", "angry")
    if ct("Half-Sister") and dice(60):
        if ct("Impersonal"):
            $rc("No... no incest please...")
        elif ct("Yandere"):
            $rc("Wait! We're siblings damnit.", "Hey, ummm... Siblings together... Is that really okay?")
        elif ct("Dandere"):
            $rc("We're siblings. We shouldn't do things like this.", "Do you have sexual desires for your sister...?")
        elif ct("Bokukko"):
            $rc("B... brother! P... please don't say things like that!")
        elif ct("Tsundere"):
            $rc("It's... it's wrong to have sexual desire among siblings, isn't it?", "Brother, you idiot! Lecher! Pervert!")
        elif ct("Kuudere"):
            $rc("...You want your sister's body that much? Pathetic.", "How hopeless can you be to do it with a sibling!")
        elif ct("Ane"):
            $rc("What? But... I'm your sister.", "Don't you know how to behave yourself, as siblings?")
        elif ct("Kamidere"):
            $rc("It's unacceptable for siblings to have sex!", "I can't believe... you do that... with your siblings!", "Having sex with a blood relative? That's wrong!")
        elif ct("Bokukko"):
            $rc("Man, you are weird.", "I'm your sis... Are you really okay with that?")
        else:
            $rc("No! Brother! We can't do this!",  "Don't you think that siblings shouldn't be doings things like that?")
    elif ct("Impersonal"):
        $rc("I see no possible benefit in doing that with you so I will have to decline.", "No.", "So, let's have you explain in full detail why you decided to do that today, hmm?")
    elif ct("Shy") and dice(40):
        $rc("I... I don't want that! ","W-we can't do that. ","I-I don't want to. ...sorry.")
    elif ct("Imouto"):
        $rc("Noooo way!", "I, I think perverted things are bad!", "That only happens after you've made your vows to be together forever, right?", "...I-I'm gonna get mad if you say that stuff, you know? Jeez!", "Y-you dummyー! You should be talking about stuff like s-s-sexー!") 
    elif ct("Dandere"):
        $rc("Keep sexual advances to a minimum.", "No.", "...pathetic.", "...you're no good.")
    elif ct("Tsundere"):
        $rc("I'm afraid I must inform you of your utter lack of common sense. Hmph!", "You are so... disgusting!!", "You pervy little scamp! Not in a million years!", "Hmph! Unfortunately for you, I'm not that cheap!")
    elif ct("Kuudere"):
        $rc("...Perv.", "...Looks like I'll have to teach you about this little thing called reality.", "O-of course the answer is no!", "Hmph, how unromantic!", "Don't even suggest something that awful.")
    elif ct("Kamidere"):
        $rc("Wh-who do you think you are!?", "W-what are you talking about… Of course I'm against that!", "What?! How could you think that I... NO!", "What? Asking that out of the blue? Know some shame!", "You should really settle down.", "What? Dying wish? You want to die?", "The meaning of 'not knowing your place' must be referring to this, eh...?", "I don't know how anyone so despicable as you could exist outside of hell.")
    elif ct("Bokukko"):
        $rc("He- Hey, Settle down a bit, okay?", "You should keep it in your pants, okay?", "Y-you're talking crazy...", "Hmph! Well no duhー!")
    elif ct("Ane"):
        $rc("If I was interested in that sort of thing I might, but unfortunately...", "Sorry... I'm not ready for that...", "Oh my, can't you think of a better way to seduce me?", "No. I have decided that it would not be appropriate.", "I'm sorry, it's too early for that.", "I don't think our relationship has progressed to that point yet.", "I think that you are being way too aggressive.", "I'm not attracted to you in ‘that’ way.")
    elif ct("Yandere"):
        $rc("I've never met someone who knew so little about how pathetic they are.", "...I'll thank you to turn those despicable eyes away from me.")
    else:
        $rc("No! Absolutely NOT!", "With you? Don't make me laugh.", "Yeah right, dickhead.", "Yeah, get the fuck away from me, you disgusting perve.", "Get lost, pervert!", "Woah, hold on there, killer. Maybe after we get to know each other better.", "Don't tell me that you thought I was a slut...?", "I'm just really tired... ok?", "How about you fix that 'anytime's fine' attitude of yours, hmm?")  
    $ char.restore_portrait()
    return
