###### j0
# quick navigation, search "j" + number, example: j0 - this panel
# 
#  1 - sex - fuck - GI
#  2 - sex - blowjob - GI
#  3 - sex - anal - GI
#  4 - sex - lesbo - GI
#  5 - sex - sex - GM

###### j1
label interactions_fuck:
    $chr.set_flag("forced", value="false")
    if chr.disposition >= 650 or ct("Nymphomaniac"): #will need to add lover as well!!!
        menu:
            "Where would you like to do it?"
            
            "Beach":
                show bg city_beach with fade
                $chr.set_flag("s_bg", value="beach")
            "Park":
                show bg city_park with fade
                $chr.set_flag("s_bg", value="park")
            "Room":
                show bg girl_room with fade
                $chr.set_flag("s_bg", value="room")
    elif (chr.status == "slave") and (ct("Shy") or ct("Dandere")):
        "She is too shy to it anywhere. You can force her nevertheless, but the prefers her room."
        menu:
            "Where would you like to do it?"
            
            "Beach":
                show bg city_beach with fade
                $chr.set_flag("s_bg", value="beach")
                $chr.set_flag("forced", value="true")
            "Park":
                show bg city_park with fade
                $chr.set_flag("s_bg", value="park")
                $chr.set_flag("forced", value="true")
            "Room":
                show bg girl_room with fade
                $chr.set_flag("s_bg", value="room")
    elif chr.status == "slave":
        "She is not comfortable with doing it outdoors. You can force her nevertheless, but the prefers her room."
        menu:
            "Where would you like to do it?"
            
            "Beach":
                show bg city_beach with fade
                $chr.set_flag("s_bg", value="beach")
                $chr.set_flag("forced", value="true")
            "Park":
                show bg city_park with fade
                $chr.set_flag("s_bg", value="park")
                $chr.set_flag("forced", value="true")
            "Room":
                show bg girl_room with fade
                $chr.set_flag("s_bg", value="room")
    elif ct("Shy") or ct("Dandere"):
        "She's too shy to do it anywhere. You go into her room."
        show bg girl_room with fade
        $chr.set_flag("s_bg", value="room")
    elif ct("Homebody"):
        "She doesn't want to do it outdoors, so you go into her room."
        show bg girl_room with fade
        $chr.set_flag("s_bg", value="room")
    else:
        "She wants to do it in her room."
        show bg girl_room with fade
        $chr.set_flag("s_bg", value="room")

    if chr.flag("s_bg") == "beach":
        if dice(50):
            $ pytfall.gm.img_generate("beach", "nude", "swimsuit", exclude=["sex", "sleeping", "angry", "in pain", "indoors", "onsen", "pool", "stage", "dungeon", "bathing"], type="first_default")
        else:
            $ pytfall.gm.img_generate("swimsuit", "nude", "simple bg",  exclude=["sex", "sleeping", "angry", "in pain", "indoors", "onsen", "pool", "stage", "dungeon", "bathing"], type="first_default")
    elif chr.flag("s_bg") == "park":
        if dice(50):
            $ pytfall.gm.img_generate("nature", "nude", exclude=["sex", "sleeping", "angry", "in pain", "indoors", "beach", "onsen", "pool", "stage", "dungeon", "bathing"], type="first_default")
        else:
            $ pytfall.gm.img_generate("nude", "simple bg", exclude=["sex", "sleeping", "angry", "in pain", "indoors", "beach", "onsen", "pool", "stage", "dungeon", "bathing"], type="first_default")
    else:
        if dice(30):
            $ pytfall.gm.img_generate("living", "nude", "lingerie", exclude=["sex", "sleeping", "angry", "in pain", "outdoors", "beach", "onsen", "pool", "stage", "dungeon", "public", "bathing"], type="first_default")
        elif dice(30):
            $ pytfall.gm.img_generate("living", "no clothes", exclude=["sleeping", "angry", "in pain", "outdoors", "beach", "onsen", "pool", "stage", "dungeon", "public", "bathing"], type="first_default")
        else:
            $ pytfall.gm.img_generate("nude", "no clothes", "simple bg", exclude=["sleeping", "angry", "in pain", "outdoors", "beach", "onsen", "pool", "stage", "dungeon", "public", "bathing"], type="first_default")
    $ sex_count = 0
    $ guy_count = 0
    $ girl_count = 0
    $ together_count = 0
    $ cum_count = 0
    if ct("Nymphomaniac"): #will need to add lover as well!!!
        $libido = 140
    elif ct("Frigid"):
        $libido = 60
    else:
        $libido = 100
    if ct ("Messy"):
        $libido += 10
    if chr.flag("forced") == "true" and ct("Masochist"):
        $libido += 20
    elif chr.flag("forced") == "true":
        $libido -= 20
        $chr.joy -= 15
    if cgo("SIW"):
        $libido += 20
    else:
        $libido -= 20
label choice:
    menu:
        "What would you like to do now?"
        
        "Ask for striptease" if chr.flag("s_bg") == "beach" and (chr.has_image("stripping", "beach", type="first_default") or chr.has_image("stripping", "simple bg", exclude=["stage"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("stripping", "beach", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ pytfall.gm.img_generate("stripping", "simple bg", exclude=["stage"], type="first_default")
            jump stripte
        "Ask for striptease" if chr.flag("s_bg") == "park" and (chr.has_image("stripping", "nature", type="first_default") or chr.has_image("stripping", "simple bg", exclude=["stage"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("stripping", "nature", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
            else:
                $ pytfall.gm.img_generate("stripping", "simple bg", exclude=["stage"], type="first_default")
            jump stripte
        "Ask for striptease" if chr.flag("s_bg") == "room" and (chr.has_image("stripping", "living", type="first_default") or chr.has_image("stripping", "simple bg", exclude=["stage"], type="first_default") or chr.has_image("stripping", "indoors", type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("stripping", "living", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
            else:
                $ pytfall.gm.img_generate("stripping", "simple bg", exclude=["stage"], type="first_default")
            jump stripte
        "Ask to masturbate" if chr.flag("s_bg") == "beach" and (chr.has_image("masturbation", "beach", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default") or chr.has_image("bc footjob", "partnerhidden", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("masturbation", "beach", exclude=["rape", "angry", "in pain"], type="first_default")
            else:
                $ pytfall.gm.img_generate("masturbation", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")
            jump mast
        "Ask to masturbate" if chr.flag("s_bg") == "park" and (chr.has_image("masturbation", "nature", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default") or chr.has_image("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("masturbation", "nature", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
            else:
                $ pytfall.gm.img_generate("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
            jump mast
        "Ask to masturbate" if chr.flag("s_bg") == "room" and (chr.has_image("masturbation", "living", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default") or chr.has_image("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default") or chr.has_image("masturbation", "indoors", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("masturbation", "living", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
            else:
                $ pytfall.gm.img_generate("masturbation", "simple bg", exclude=["forced", "normalsex", "group", "bdsm", "cumcovered"], type="first_default")
            jump mast
        "Ask for blowjob" if chr.flag("s_bg") == "beach" and (chr.has_image("bc blowjob", "partnerhidden", "beach", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc blowjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("bc blowjob", "partnerhidden", "beach", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("bc blowjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump bj
        "Ask for blowjob" if chr.flag("s_bg") == "park" and (chr.has_image("bc blowjob", "partnerhidden", "nature", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc blowjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("bc blowjob", "partnerhidden", "nature", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("bc blowjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump bj
        "Ask for blowjob" if chr.flag("s_bg") == "room" and (chr.has_image("bc blowjob", "partnerhidden", "living", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc blowjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc blowjob", "partnerhidden", "indoors", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("bc blowjob", "partnerhidden", "living", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("bc blowjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump bj
        "Ask for titsjob" if chr.flag("s_bg") == "beach" and (chr.has_image("bc titsjob", "partnerhidden", "beach", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc titsjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("bc titsjob", "partnerhidden", "beach", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("bc titsjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump tj
        "Ask for titsjob" if chr.flag("s_bg") == "park" and (chr.has_image("bc titsjob", "partnerhidden", "nature", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc titsjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("bc titsjob", "partnerhidden", "nature", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("bc titsjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump tj
        "Ask for titsjob" if chr.flag("s_bg") == "room" and (chr.has_image("bc titsjob", "partnerhidden", "living", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc titsjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc titsjob", "partnerhidden", "indoors", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("bc titsjob", "partnerhidden", "living", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("bc titsjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump tj
        "Ask for handjob" if chr.flag("s_bg") == "beach" and (chr.has_image("bc handjob", "partnerhidden", "beach", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc handjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("bc handjob", "partnerhidden", "beach", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("bc handjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump hj
        "Ask for handjob" if chr.flag("s_bg") == "park" and (chr.has_image("bc handjob", "partnerhidden", "nature", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc handjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("bc handjob", "partnerhidden", "nature", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("bc handjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump hj
        "Ask for handjob" if chr.flag("s_bg") == "room" and (chr.has_image("bc handjob", "partnerhidden", "living", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc handjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")or chr.has_image("bc handjob", "partnerhidden", "indoors", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("bc handjob", "partnerhidden", "living", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("bc handjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump hj
        "Ask for footjob" if chr.flag("s_bg") == "beach" and (chr.has_image("bc footjob", "partnerhidden", "beach", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc footjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("bc footjob", "partnerhidden", "beach", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("bc footjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump fj
        "Ask for footjob" if chr.flag("s_bg") == "park" and (chr.has_image("bc footjob", "partnerhidden", "nature", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc footjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("bc footjob", "partnerhidden", "nature", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("bc footjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump fj
        "Ask for footjob" if chr.flag("s_bg") == "room" and (chr.has_image("bc footjob", "partnerhidden", "living", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("bc footjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default")or chr.has_image("bc footjob", "partnerhidden", "indoors", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("bc footjob", "partnerhidden", "living", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("bc footjob", "partnerhidden", "simple bg", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump fj
        "Ask for vaginal sex" if chr.flag("s_bg") == "beach" and (chr.has_image("2c vaginal", "partnerhidden", "beach", "straight", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("2c vaginal", "partnerhidden", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("2c vaginal", "partnerhidden", "swimsuit", "straight", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("2c vaginal", "partnerhidden", "beach", "straight", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump vag_sex
        "Ask for vaginal sex" if chr.flag("s_bg") == "park" and (chr.has_image("2c vaginal", "partnerhidden", "nature", "straight", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("2c vaginal", "partnerhidden", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("2c vaginal", "partnerhidden", "nature", "straight", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("2c vaginal", "partnerhidden", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump vag_sex
        "Ask for vaginal sex" if chr.flag("s_bg") == "room" and (chr.has_image("2c vaginal", "partnerhidden", "living", "straight", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("2c vaginal", "partnerhidden", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default")or chr.has_image("2c vaginal", "partnerhidden", "indoors", "straight", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("2c vaginal", "partnerhidden", "living", "straight", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("2c vaginal", "partnerhidden", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump vag_sex
        "Ask for anal sex" if chr.flag("s_bg") == "beach" and (chr.has_image("2c anal", "partnerhidden", "beach", "straight", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("2c anal", "partnerhidden", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("2c anal", "partnerhidden", "swimsuit", "straight", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("2c anal", "partnerhidden", "beach", "straight", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump anal_sex
        "Ask for anal sex" if chr.flag("s_bg") == "park" and (chr.has_image("2c anal", "partnerhidden", "nature", "straight", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("2c anal", "partnerhidden", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("2c anal", "partnerhidden", "nature", "straight", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("2c anal", "partnerhidden", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump anal_sex
        "Ask for anal sex" if chr.flag("s_bg") == "room" and (chr.has_image("2c anal", "partnerhidden", "straight", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("2c anal", "partnerhidden", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("2c anal", "partnerhidden", "indoors", "straight", exclude=["rape", "angry", "in pain"], type="first_default") or chr.has_image("2c anal", "partnerhidden", "dungeon", "straight", exclude=["rape", "angry", "in pain", "restrained"], type="first_default")):
            if dice(50):
                $ pytfall.gm.img_generate("2c anal", "partnerhidden", "living", "straight", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            else:
                $ pytfall.gm.img_generate("2c anal", "partnerhidden", "simple bg", "straight", exclude=["rape", "angry", "in pain"], type="first_default", default=chr.select_image(chr.id, 'after_sex'))
            jump anal_sex
        "That's all.":
            "You decided to finish."   
    #$ sex_count = 0
    #$ guy_count = 0
    #$ girl_count = 0
    #$ together_count = 0
    #$ cum_count = 0
            if together_count > 0 and sex_count >=3:
                "Placeholder for come together lines from AA"
            if cum_count >= 3:
                "Placeholder for cum lines from AA"
            elif sex_count < 1 and guy_count < 1 and girl_count < 1:
                if chr.status == "slave":
                    "She is puzzled and confused by the fact that you didn't do anything. She quickly leaves, probably thinking that you teased her."
                else:
                    "She is quite upset and irritated because you didn't do anything. She quickly leaves, probably thinking that you teased her."
                $ chr.disposition -= radint(40, 70)
                $ chr.joy -= radint(20, 50)
                $ chr.vitality -= 25
            elif girl_count > 0 and sex_count < 1:
                "She did nothing but masturbated in front of you. Probably better than nothing, but be prepared for rumors about your impotence or orientation."
                $ chr.disposition -= radint(30, 50)
                $ chr.joy -= radint(15, 25)
                $ chr.vitality -= 20
            elif girl_count > 0 and guy_count > 0 and sex_count < 3:
                "Placeholder for small amount of sex lines from AA"
            
            
            jump girl_interactions 

    label bj:
        "She licks and sucks your dick until you come."
        if chr.oral < 50:
            "She clearly needs more training, so it took some time. But at least she learned something new."
            $ chr.oral += randint (3, 5)
            $ hero.oral += randint (0, 1)
            $ chr.vitality -= 15
            $ libido += 5
        elif chr.oral < 300:
            "It was pretty good."
            $ chr.oral += randint (2, 4)
            $ hero.oral += randint (0, 2)
            $ chr.vitality -= 5
            $ chr.joy += 1
            $ libido += 5
        elif chr.oral < 1000:
            "It was very good."
            $ chr.oral += randint (1, 3)
            $ hero.oral += randint (1, 3)
            $ chr.vitality -= 5
            $ chr.joy += 1
            $ libido += 8
        else:
            "She was so good that you came after a few seconds. Wow."
            $ chr.oral += randint (0, 2)
            $ hero.oral += randint (1, 4)
            $ chr.vitality -= 4
            $ chr.joy += 2
            $ libido += 10
            $ sex_count += 1
            $ guy_count +=1
        if (chr.oral - hero.oral) > 200:
            "You learned something new about oral as well. A pleasure to deal with professionals."
            $ hero.oral += 2
        elif (hero.oral - chr.oral) > 200:
            "You were able to show her some new tricks."
            $ chr.oral += 2
        $ sex_count += 1
        $ guy_count +=1
        $ cum_count += 1
        jump choice
            
    label tj:
        "She stimulates your dick with her soft breasts until you come."
        if chr.oral < 50 or chr.sex < 50:
            "She clearly needs more training, so it took some time. But at least she learned something new."
            $ chr.oral += randint (1, 4)
            $ chr.sex += randint (1, 4)
            $ hero.sex += randint (0, 1)
            $ chr.vitality -= 15
            $ libido += 5
        elif chr.oral < 300 or  chr.sex < 300:
            "It was pretty good."
            $ chr.oral += randint (1, 3)
            $ chr.sex += randint (1, 3)
            $ hero.sex += randint (0, 1)
            $ chr.vitality -= 5
            $ chr.joy += 1
            $ libido += 5
        elif chr.oral < 1000 or chr.sex < 1000:
            "It was very good."
            $ chr.oral += randint (1, 2)
            $ chr.sex += randint (1, 2)
            $ hero.sex += randint (1, 2)
            $ chr.vitality -= 5
            $ chr.joy += 1
            $ libido += 8
        else:
            "She was so good that you came after a few seconds. Wow."
            $ chr.oral += randint (0, 2)
            $ chr.sex += randint (0, 2)
            $ hero.sex += randint (1, 3)
            $ chr.vitality -= 4
            $ chr.joy += 2
            $ libido += 10
        if (chr.oral - hero.oral) > 200 or (chr.sex - hero.sex) > 200:
            "You learned something new about titsjob as well. A pleasure to deal with professionals."
            $ hero.oral += 1
            $ hero.sex += 1
        elif (hero.oral - chr.oral) > 200:
            "You were able to show her some new tricks."
            $ chr.oral += 1
            $ chr.sex += 1
        $ sex_count += 1
        $ guy_count +=1
        $ cum_count += 1
        jump choice
    label hj:
        "She stimulates your dick with her hands until you come."
        if chr.sex < 50:
            "She clearly needs more training, so it took some time. But at least she learned something new."
            $ chr.sex += randint (3, 5)
            $ hero.sex += randint (0, 1)
            $ chr.vitality -= 15
            $ libido += 5
        elif chr.sex < 300:
            "It was pretty good."
            $ chr.sex += randint (2, 4)
            $ hero.sex += randint (0, 2)
            $ chr.vitality -= 5
            $ chr.joy += 1
            $ libido += 5
        elif chr.sex < 1000:
            "It was very good."
            $ chr.sex += randint (1, 3)
            $ hero.sex += randint (1, 2)
            $ chr.vitality -= 5
            $ chr.joy += 1
            $ libido += 8
        else:
            "She was so good that you came after a few seconds. Wow."
            $ chr.sex += randint (0, 2)
            $ hero.sex += randint (1, 3)
            $ chr.vitality -= 4
            $ chr.joy += 2
            $ libido += 10
        if (chr.sex - hero.sex) > 200:
            "You learned something new about handjob as well. A pleasure to deal with professionals."
            $ hero.sex += 2
        elif (hero.sex - chr.sex) > 200:
            "You were able to show her some new tricks."
            $ chr.sex += 2
        $ sex_count += 1
        $ guy_count +=1
        $ cum_count += 1
        jump choice
    label fj:
        "She stimulates your dick with her feet until you come."
        if chr.sex < 50:
            "She clearly needs more training, so it took some time. But at least she learned something new."
            $ chr.sex += randint (3, 5)
            $ hero.sex += randint (0, 1)
            $ chr.vitality -= 15
            $ libido += 5
        elif chr.sex < 300:
            "It was pretty good."
            $ chr.sex += randint (2, 4)
            $ hero.sex += randint (0, 2)
            $ chr.vitality -= 5
            $ chr.joy += 1
            $ libido += 5
        elif chr.sex < 1000:
            "It was very good."
            $ chr.sex += randint (1, 3)
            $ hero.sex += randint (1, 2)
            $ chr.vitality -= 5
            $ chr.joy += 1
            $ libido += 8
        else:
            "She was so good that you came after a few seconds. Wow."
            $ chr.sex += randint (0, 2)
            $ hero.sex += randint (1, 3)
            $ chr.vitality -= 4
            $ chr.joy += 2
            $ libido += 10
        if (chr.sex - hero.sex) > 200:
            "You learned something new about footjob as well. A pleasure to deal with professionals."
            $ hero.sex += 2
        elif (hero.sex - chr.sex) > 200:
            "You were able to show her some new tricks."
            $ chr.sex += 2
        $ sex_count += 1
        $ guy_count +=1
        $ cum_count += 1
        jump choice
    label mast:
        "She masturbates in front of you. Although it cannot be considered as a sexual act, you both are more aroused now."
        if libido <= 30:
            $ libido += 10
        else:
            $ libido += 5
        $ chr.vitality -= 10
        $ girl_count +=1
        jump choice
    label vag_sex:
        if chr.vaginal < 50 and hero.vaginal >= 50:
            "You fuck her pussy until she comes. She's still too inexperienced, so you were unable to come properly. Oh well, at least she learned something new."
            $ chr.vaginal += randint (3, 5)
            $ hero.vaginal += randint (0, 1)
            $ chr.vitality -= 20
            $ libido -= 10
            $ sex_count += 1
            $ girl_count +=1
        elif chr.vaginal >= 50 and hero.vaginal < 50:
            "You fuck her pussy until you come. Unfortunately you didn't have enough skill to make her come as well. She looks disappointed."
            $ hero.vaginal += randint (1, 2)
            $ chr.vitality -= 20
            $ chr.joy -= 10
            $ libido += 5
            $ sex_count += 1
            $ guy_count +=1
        elif chr.vaginal < 50 and hero.vaginal < 50:
            "You fuck her pussy for some time until you both realized that you are not skillful enough to make each other properly come. It would be funny if it wasn't so sad."
            $ chr.vaginal += randint (0, 1)
            $ hero.vaginal += randint (0, 1)
            $ chr.vitality -= 10
            $ libido += 5
            $ chr.joy -= 10
            $ sex_count += 1
        elif chr.vaginal < 500 and hero.vaginal < 500:
            "You fuck her wet pussy until you both come. It was pretty good."
            $ chr.vaginal += randint (2, 4)
            $ hero.vaginal += randint (0, 2)
            $ chr.vitality -= 10
            $ chr.joy += 5
            $ libido -= 10
            $ sex_count += 1
            $ guy_count +=1
            $ girl_count +=1
        elif chr.vaginal >= 500 and hero.vaginal < 500:
            "You fuck her wet pussy until you both come. You did it much earlier, and noticed a light self-confident smile on her face."
            $ chr.vaginal += randint (1, 4)
            $ hero.vaginal += randint (1, 2)
            $ chr.vitality -= 10
            $ chr.joy += 5
            $ libido -= 10
            $ sex_count += 1
            $ guy_count +=1
            $ girl_count +=1
        elif chr.vaginal < 500 and hero.vaginal =< 500:
            "You fuck her wet pussy until you both come. She did it much earlier, looks like she enjoyed it a lot."
            $ chr.vaginal += randint (1, 4)
            $ hero.vaginal += randint (1, 2)
            $ chr.vitality -= 10
            $ chr.joy += 10
            $ libido -= 10
            $ sex_count += 1
            $ guy_count +=1
            $ girl_count +=1
        elif chr.vaginal < 1000 or hero.vaginal < 1000:
            "You fuck her wet pussy until you both come. It was very good."
            if dice (round((chr.vaginal + hero.vaginal)* 0.05)):
                "You managed to come simultaneously!"
                $ chr.joy += 5
                $ chr.vaginal += randint (0, 1)
                $ hero.vaginal += randint (0, 1)
                $ together_count += 1
            $ chr.vaginal += randint (1, 3)
            $ hero.vaginal += randint (1, 3)
            $ chr.vitality -= 10
            $ chr.joy += 10
            $ libido -= 10
            $ sex_count += 1
            $ guy_count +=1
            $ girl_count +=1
        else:
            "You fuck her wet pussy until you both simultaneously come multiple times. It was fabulous."
            $ chr.vaginal += randint (1, 2)
            $ hero.vaginal += randint (1, 3)
            $ together_count += 1
            $ chr.vitality -= 10
            $ chr.joy += 15
            $ libido += -20
            $ sex_count += 1
            $ guy_count +=2
            $ girl_count +=2
        if (chr.vaginal - hero.vaginal) > 300:
            "You learned something new about vagianl sex as well. A pleasure to deal with professionals."
            $ hero.vaginal += 2
        elif (hero.vaginal - chr.vaginal) > 300:
            "You were able to show her some new tricks."
            $ chr.vaginal += 2
        jump choice
    label anal_sex:
        if chr.anal < 50 and hero.anal >= 50:
            "You fuck her ass until she comes. She's still too inexperienced, so you were unable to come properly, and it was quite painful for her. Oh well, at least she learned something new."
            $ chr.anal += randint (3, 5)
            $ hero.anal += randint (0, 1)
            $ chr.vitality -= 25
            $ chr.joy -=10
            if chr.health > 30:
                $ chr.health -= 5
            $ libido -= 5
            $ sex_count += 1
            $ girl_count +=1
        elif chr.anal >= 50 and hero.anal < 50:
            "You fuck her ass until you come. Unfortunately you didn't have enough skill to make her come, and it was quite painful for her. She looks disappointed."
            $ hero.anal += randint (1, 2)
            $ chr.vitality -= 20
            $ chr.joy -= 20
            $ libido += 5
            if chr.health > 30:
                $ chr.health -= 5
            $ sex_count += 1
            $ guy_count +=1
        elif chr.anal < 50 and hero.anal < 50:
            "You fuck her ass for some time until you both realized that you are not skillful enough to make each other properly come. It was an unpleasant and painful experience for both of you."
            $ chr.anal += randint (1, 3)
            $ hero.anal += randint (1, 3)
            $ chr.vitality -= 25
            $ libido += 5
            $ chr.joy -= 25
            $ sex_count += 1
            if chr.health > 35:
                $ chr.health -= 10
        elif chr.anal < 500 and hero.anal < 500:
            "You fuck her tight ass until you both come. It was pretty good."
            $ chr.anal += randint (2, 4)
            $ hero.anal += randint (0, 2)
            $ chr.vitality -= 15
            $ chr.joy += 5
            $ libido -= 10
            $ sex_count += 1
            $ guy_count +=1
            $ girl_count +=1
        elif chr.anal >= 500 and hero.anal < 500:
            "You fuck her tight ass until you both come. You did it much earlier, and noticed a small self-confident smile on her face."
            $ chr.anal += randint (1, 4)
            $ hero.anal += randint (1, 2)
            $ chr.vitality -= 15
            $ chr.joy += 5
            $ libido -= 10
            $ sex_count += 1
            $ guy_count +=1
            $ girl_count +=1
        elif chr.anal < 500 and hero.anal =< 500:
            "You fuck her tight ass until you both come. She did it much earlier, looks like she enjoyed it a lot."
            $ chr.anal += randint (1, 4)
            $ hero.anal += randint (1, 2)
            $ chr.vitality -= 15
            $ chr.joy += 10
            $ libido -= 10
            $ sex_count += 1
            $ guy_count +=1
            $ girl_count +=1
        elif chr.anal < 1000 or hero.anal < 1000:
            "You fuck her tight ass until you both come. It was very good."
            if dice (round((chr.anal + hero.anal)* 0.05)):
                "You managed to come simultaneously!"
                $ chr.joy += 5
                $ chr.anal += randint (0, 1)
                $ hero.anal += randint (0, 1)
                $ together_count += 1
            $ chr.anal += randint (1, 3)
            $ hero.anal += randint (1, 3)
            $ chr.vitality -= 15
            $ chr.joy += 10
            $ libido -= 10
            $ sex_count += 1
            $ guy_count +=1
            $ girl_count +=1
        else:
            "You fuck her tight ass until you both simultaneously come multiple times. It was fabulous."
            $ chr.anal += randint (1, 2)
            $ hero.anal += randint (1, 3)
            $ together_count += 1
            $ chr.vitality -= 15
            $ chr.joy += 15
            $ libido += -10
            $ sex_count += 1
            $ guy_count +=2
            $ girl_count +=2
        if (chr.anal - hero.anal) > 300:
            "You learned something new about anal sex as well. A pleasure to deal with professionals."
            $ hero.anal += 2
        elif (hero.anal - chr.anal) > 300:
            "You were able to show her some new tricks."
            $ chr.anal += 2
        jump choice
    label stripte:
        "You ask her to show you striptease."
        if chr.strip < 50:
            "She tried her best, but the moves were clumsy and unnatural. At least she learned something new though."
            $ chr.strip += randint (3, 5)
            $ chr.joy -= 10
            $ chr.vitality -= 10
            $ libido -= 15
        elif chr.strip < 300:
            "It's nice to look at her graceful and elegant moves."
            $ chr.strip += randint (1, 3)
            $ hero.strip += randint (0, 1)
            $ chr.vitality -= 10
            $ libido += 5
        elif chr.strip < 1000:
            "Her movements are so fascinating that you cannot look away from her. She looks proud and pleased."
            $ chr.strip += randint (1, 2)
            $ hero.strip += randint (1, 2)
            $ chr.vitality -= 10
            $ chr.joy += 10
            $ libido += 5
        else:
            "She looks unbearably hot and sexy. After a short time you cannot withstand it anymore and begin to masturbate, quickly coming. She looks at you with a smile and superiority in the eyes."
            $ chr.strip += randint (0, 1)
            $ hero.strip += randint (1, 4)
            $ chr.vitality -= 10
            $ chr.joy += 15
            $ libido += 10
            $ guy_count +=1
        if (chr.strip - hero.strip) > 200:
            "You learned something new about striptease as well. A pleasure to deal with professionals."
            $ hero.strip += 2
        elif (hero.strip - chr.strip) > 200:
            "You were able to show her some new tricks."
            $ chr.strip += 2
        jump choice
 #   "Where would you like to do it?"
 #   menu:
 #       "Beach":
 #           python:
 #               renpy.scene()
 #               hs()
 #          
 #       "Park":
 #           python:
 #               renpy.scene()
 #               hs()
 #           show bg city_park with fade
 #       if chr.has_image("straight", "beach", type="first_default"):
 #   $pytfall.gm.change_img(chr.show("nude", "simple bg", type="first_default", exclude=["sex", "sleeping", "bathing", "cooking", "reading", "pool", "lingerie"]))
    jump girl_interactions
#label interactions_fuck:
    show bg girl_room with fade
    if dice(50):
        $ pytfall.gm.img_generate("nude", "lingerie", exclude=["stripping", "sleeping", "angry", "in pain"])
    else:
        $ pytfall.gm.img_generate("nude", "no clothes", exclude=["stripping", "sleeping"])
    jump girl_interactions
    if chr.status != "slave":
        if co("SIW") and chr.disposition < 400 - hero.charisma/2:
            
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "swimsuit", "beach"])
            $ rc("Not a chance!", "No freebies!", "And why would I want to do that?")
            
            if dice(50):
                $ chr.disposition -= randint(3, 5)
            
            jump girl_interactions
            
        elif chr.disposition < 700 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "swimsuit", "beach"])
            $ rc("No chance in hell!", "I am a bit tired...", "You're kidding? Right?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
    else:
        # Case: Slave
        if chr.disposition < -500 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "defiant", exclude=["nude", "swimsuit", "beach"])
            $ rc("I'd rather die!", "Get away from me!")
            $ chr.disposition -= randint(3, 5)
            
            jump girl_interactions
            
    # If we got here, we're good to go:
    if chr.normalsex < 30:
        
        $ rc("Lets have some fun!", "Lets fuck just like like bunnies!")
        $ pytfall.gm.img_generate("sex", "partner hidden", exclude=["beach", "generic outdoor"], type="first_default")
        
        "[chr.nickname] clearly needs more training..."
        
        if dice(75):
            extend " and she got slightly better."
            $ chr.normalsex += 1
            if dice(50):
                extend " So did you!"
                $ hero.sex += randint(1, 3)
                
    else:
        $ rc("Lets have some fun!", "Lets fuck just like like bunnies!", "Just sit back and relax!")
        $ pytfall.gm.img_generate("sex", "partner hidden", exclude=["beach", "generic outdoor"], type="first_default")
        if dice(75):
            extend "[chr.nickname] has learned a thing or two."
            $ chr.normalsex += 1
            if dice(50):
                extend " So did you!"
                $ hero.sex += randint(1, 3)
                
    if "Virgin" in chr.traits:
        "[chr.name] has lost her virginity."
        $ chr.removetrait(traits["Virgin"])
        
    if dice(int(round(hero.sex*0.3))):
        "You both recieve Extra stats bonus for your l33t skillz! :)"
        $ chr.normalsex += 1
        $ hero.sex += 1
        $ chr.joy += 3
        $ chr.disposition += 1
    $ hero.exp += adjust_exp(hero, randint(5, 10))
    $ chr.exp += adjust_exp(chr, randint(5, 10))
        
    jump girl_interactions
    

###### j2
label interactions_blowjob:
    # Take care of rejections first? Maybe put this on a separate label and use for all acts???
    if chr.status != "slave":
        if co("SIW") and chr.disposition < 300  - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("Not a chance!", "No freebies!", "And why would I want to do that?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
        elif chr.disposition < 500 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("No chance in hell!", "I am a bit tired...", "You're kidding? Right?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
    else:
        # Case: Slave
        if chr.disposition < -500 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "defiant", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("I'd rather die!", "Get away from me!")
            $ chr.disposition -= randint(3, 5)
            
            jump girl_interactions
            
    # If we got here, we're good to go:
    if chr.blowjob < 30:
        $ rc("Lets have some fun!", "Take off your pants!")
        $ pytfall.gm.img_generate("blowjob", "partner hidden", exclude=["beach", "generic outdoor"], type="first_default")
        "[chr.nickname] clearly needs more training..."
        if dice(75):
            extend " and she got slightly better."
            $ chr.blowjob += 1
            if dice(50):
                extend " So did you!"
                $ hero.sex += randint(1, 3)
                
    else:
        $ rc("Lets have some fun!", "Take off your pants!",  "Just sit back and relax!")
        $ pytfall.gm.img_generate("blowjob", "partner hidden", exclude=["beach", "generic outdoor"], type="first_default")
        if dice(75):
            extend "[chr.nickname] has learned a thing or two."
            $ chr.blowjob += 1
            if dice(50):
                extend " So did you!"
                $ hero.sex += randint(1, 3)
                
    if dice(int(round(hero.sex*0.3))):
        "You both recieve Extra stats bonus for your l33t skillz! :)"
        $ chr.blowjob += 1
        $ hero.sex += 1
        $ chr.joy += 3
        $ chr.disposition += 1
    $ hero.exp += adjust_exp(hero, randint(5, 10))
    $ chr.exp += adjust_exp(chr, randint(5, 10))
                
    jump girl_interactions
    

###### j3
label interactions_anal:
    # Take care of rejections first? Maybe put this on a separate label and use for all acts???
    if chr.status != "slave":
        if co("SIW") and chr.disposition < 500 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("Not a chance!", "No freebies!", "And why would I want to do that?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
        elif chr.disposition < 700 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("No chance in hell!", "I am a bit tired...", "You're kidding? Right?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
    else:
        # Case: Slave
        if chr.disposition < -500 - hero.charisma/2:
            $ pytfall.gm.img_generate("profile", "defiant", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("I'd rather die!", "Get away from me!")
            $ chr.disposition -= randint(3, 5)
            
            jump girl_interactions
            
    # If we got here, we're good to go:
    if chr.analskill < 60:
        $ rc("Lets have some fun!", "Please be gentle, this is new to me...!")
        $ pytfall.gm.img_generate("anal", "partner hidden", exclude=["beach", "generic outdoor"], type="first_default")
        "[chr.nickname] clearly needs more training..."
        if dice(75):
            extend " and she got slightly better."
            $ chr.anal += 1
            if dice(50):
                extend " So did you!"
                $ hero.sex += randint(1, 3)
    else:
        $ rc("Lets have some fun!", "Anything to make us both feel good!", "Just sit back and relax!")
        $ pytfall.gm.img_generate("anal", "partner hidden", exclude=["beach", "generic outdoor"], type="first_default")
        if dice(75):
            extend "[chr.nickname] has learned a thing or two."
            $ chr.anal += 1
            if dice(50):
                extend " So did you!"
                $ hero.sex += randint(1, 3)
                
    if dice(int(round(hero.sex*0.3))):
        "You both recieve Extra stats bonus for your l33t skillz! :)"
        $ chr.anal += 1
        $ hero.sex += 1
        $ chr.joy += 3
        $ chr.disposition += 1
    $ hero.exp += adjust_exp(hero, randint(5, 10))
    $ chr.exp += adjust_exp(chr, randint(5, 10))
        
    jump girl_interactions
    

###### j4
label interactions_lesbo:
    # Take care of rejections first? Maybe put this on a separate label and use for all acts???
    if chr.status != "slave":
        if co("SIW") and chr.disposition < 300:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("Not a chance!", "And why would I want to do that?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
        elif chr.disposition < 400:
            $ pytfall.gm.img_generate("profile", "angry", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("No chance in hell!", "I am a bit tired...", "You're kidding? Right?")
            if dice(50):
                $ chr.disposition -= randint(3, 5)
                
            jump girl_interactions
            
    else:
        # Case: Slave
        if chr.disposition < - 500:
            $ pytfall.gm.img_generate("profile", "defiant", exclude=["nude", "bikini", "swimsuit", "exposed", "beach"])
            $ rc("I'd rather die!", "While you watch? Not a chance!")
            $ chr.disposition -= randint(3, 5)
            jump girl_interactions
            
    # If we got here, we're good to go:
    if chr.vaginalskill < 60:
        $ rc("Kinda pervy? Watching two girls go at it?!", "Well, I am willing to try new things!")
        $ pytfall.gm.img_generate("les", exclude=["beach", "generic outdoor"], type="first_default")
        "[chr.nickname] clearly needs more training..."
        if dice(75):
            extend " and she got slightly better."
            $ chr.vaginal += 1
    else:
        $ rc("Kinda pervy? Watching two girls go at it?!", "Just sit back and enjoy the show!")
        $ pytfall.gm.img_generate("les", exclude=["beach", "generic outdoor"], type="first_default")
        if dice(75):
            g "[chr.nickname] has learned a thing or two."
            $ chr.vaginal += 1
            
    $ chr.exp += adjust_exp(chr, randint(5, 10))
        
    jump girl_interactions
    

###### j5
label interactions_sex:   
    
    if chr.disposition > 700:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 20
            $ gm_disp_mult = 0.3
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 99
            $ gm_disp_mult = 0.3
        else:
            $ gm_dice = 95
            $ gm_disp_mult = 0.3

    elif chr.disposition > 650:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 15
            $ gm_disp_mult = 0.5
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 99
            $ gm_disp_mult = 0.4
        else:
            $ gm_dice = 92
            $ gm_disp_mult = 0.5

    elif chr.disposition > 600:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 10
            $ gm_disp_mult = 0.8
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 98
            $ gm_disp_mult = 0.6
        else:
            $ gm_dice = 90
            $ gm_disp_mult = 0.8

    elif chr.disposition > 550:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 5
            $ gm_disp_mult = 1
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 98
            $ gm_disp_mult = 0.7
        else:
            $ gm_dice = 85
            $ gm_disp_mult = 1

    elif chr.disposition > 500:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 3
            $ gm_disp_mult = 1
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 90
            $ gm_disp_mult = 0.7
        else:
            $ gm_dice = 70
            $ gm_disp_mult = 1    

    elif chr.disposition > 400:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 2
            $ gm_disp_mult = 1
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 70
            $ gm_disp_mult = 0.8
        else:
            $ gm_dice = 20
            $ gm_disp_mult = 1
    elif chr.disposition > 300:
        if "Frigid" in  chr.traits or "Lesbian" in  chr.traits:
            $ gm_dice = 2
            $ gm_disp_mult = 1
        elif "Nymphomaniac" in  chr.traits:
            $ gm_dice = 50
            $ gm_disp_mult = 0.9
        else:
            $ gm_dice = 5
            $ gm_disp_mult = 1
    elif chr.disposition > 100:
        if "Nymphomaniac" in  chr.traits:
            $ gm_dice = 20
            $ gm_disp_mult = 1
        else:
            $ gm_dice = 2
            $ gm_disp_mult = 1
    else:
        if "Nymphomaniac" in  chr.traits:
            $ gm_dice = 5
            $ gm_disp_mult = 1
        else:
            $ gm_dice = 1
            $ gm_disp_mult = 1

    if "Mind Fucked" in chr.traits:
        if gm_dice+20 > 100:
            $ gm_dice = 100
        else:
            $ gm_dice += 20
        $ gm_disp_mult *= 0.5

    if dice(gm_dice):
        $ gm_last_success = True
        $chr.disposition += (randint(15, 45)*(gm_disp_mult))
    else:
        $ gm_last_success = False
        $chr.disposition -= (randint(20, 60)*(gm_disp_mult))
    
    if gm_last_success:
        if ct("Half-Sister") and dice(30):
            if if ct("Impersonal"):
                $rc("I'll take in all your cum, brother.", "Sex with my brother, initiation.", "Let's have incest.", "Even though we're siblings... it's fine to do this, right?", "Let's deepen our bond as siblings.")
            elif ct("Shy") and dice(30):
                $rc("Umm... anything is fine as long as it's you... brother.", "I-if it's you, b-brother, then anything you do makes me feel good.")
            elif ct("Masochist") and dice(25):
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
            $rc("...Please insert to continue.", "You are authorized so long as it does not hurt.", "You can do me if you want.", "So, I'll begin the sexual interaction...", "Understood. I will... service you…", "I dedicate this body to you.")
        elif ct("Shy") and dice(30):
            $rc("D-do you mean…  Ah, y-yes…  If I'm good enough…", "Eeh?! Th-that's... uh... W- well... I do... want to...", "O...okay. I'll do my best.", "I-I was thinking… That I wanted to be one with you…", "If it's you, I'm fine with anything...", "I too... wanted to be touched by you... ","I want my feelings…  To reach you…", "It's... it's... o-okay to... have... s--s-sex... with me...", "Uh... I... h...how should I say this... It... it'll be great if you could do it gently...", "Aah... p... please... I... I want it... I... I can't think of anything else now!", "I-I'll do my best... for your sake!", "Uhm... I want you... to be gentle...", "Um, I-I want to do it… Please treat me well…", "Uh, uhm, how should I...? Eh? You want it like this...? O-okay! Then, h-here I go…", "Eeh, i-is it ok with someone like me...?", "Sorry if I'm no good at this...", "Uh... p... please... d...do it for me... my whole body's aching right now...", "Umm... anything is fine as long as it's you...", "Umm… please do perverted things to me…", "I don't know how well I will do...")
        elif ct("Nymphomaniac") and dice(40):
            $rc("Come on, I'll do the same for you, so please hurry and do me.", "Ahh, I can't wait anymore... quickly... please do me fast…", "I've been waiting for you all this time, so hurry up.", "Ready anytime you are.", "Please fill my naughty holes with your hot shaft.", " Let's do it all night long, okay? ...What, I'm just a dirty-minded girl~ ♪", "I don't mind. I really loooove to have sex. ♪", "Just watching is boring, right?  So… ♪", "...Shit! Now I'm horny as hell! ...Hey? You up for a go?", "Whenever, wherever…", "If you'd made me wait any longer I would have violated you myself.", "You know, had you kept me waiting any longer I would probably have jumped you myself.", "I hope you know how to handle a pussy...", "Man, who'd have thought that you are as perverted as I am...", "Ah... actually, I have been feeling sexually frustrated lately...", "Aah~~ Geez, I can't hold it anymore! Let's fuck!", "Hyauh…  Geez, do you have any idea how long I've been wet?", "Finally!", "You can ask me as much as you like... We can do it again... and again...", "...These perverted feelings... You can make them go away, can't you...?", "Umm, I-I'm always ready for it, so...!", "Turn me into a sloppy mess...!", "Let's do it! Right now! Take off your clothes! Hurry!", "Hmmm, what should I do～? ...Do you wanna do it THAT much～? I guess there's no stopping it～", "eah, it's okay. If that's what you want. Besides... I kinda like this stuff.")
        elif ct("Masochist") and dice (20):
            $rc("Feel free to make me your personal bitch slave!", "Geez～, you could have just taken me by force～...", "Kya~... I - am - being - molested -... Oh come on, at least play along a little bit...")
        elif ct("Sadist") and dice(20):
            $rc("Become my... sex slave ♪", "Just shut up and surrender yourself to me. Good boy.", "Stay still and let me violate you.", "Come. I'll be gentle with you.")
        elif ct("Tsundere"):
            $rc("*gulp*… W-well... since you're begging to do it with me, I suppose we can…", "It...it can't be helped, right? It... it's not that I like you or anything!", "I-it's not like I want to do it! It's just that you seem to want to do it so much…", "I'll punish you if I don't feel good, got it?", "Hhmph... if...if you wanna do it... uh... go all the way with it!", "Hm hmm! Be amazed at my fabulous technique!", "If you're asking, then I'll listen… B-but it's not like I actually want to do it, too!", "I-I'm actually really good at sex! So... I-I'd like to show you…", "I...I'm only doing it because of your happy face.", "Humph! I'll show you I can do it!", "If-if you say that you really, really want it… Then I won't turn you down…", "L.... leave it to me... you idiot...", "If you want to do it now, it's okay… I just don't want to do anything weird in front of other people.", "Th-things like that should only happen after marriage… but… fine, I'll do it…", "God, people like you… Are way too honest about what they want…", "T...that can't be helped, right? B...but that doesn't mean you can do anything you like!", "You're hopeless.... Well, fine then....", "...Yes, yes, I'll do it, I'll do it so…  geez, stop making that stupid face…", "Geez, you take anything you can get...")
        elif ct("Dandere"):
            $rc("...Very well then. Please go ahead and do as you like.", "I... want you inside me.", "You're welcome to... do that.", "You can do whatever you want to me.", "I'm going to make you cum. You had better prepare yourself.", "I will not go easy on you.", "I... I'm ready for sex.", "Make me feel good...", "...If you do it, be gentle.", "I will handle... all of your urges...", "Then…  I will do it with you…", "...If you want, do it now.", "...I want to do it, too.", "...How do you want it?  ...Okay, I can do it…", "Now is your chance...")
        elif ct("Kuudere"):
            $rc("...I don't particularly mind.", "Heh. I'm just a girl too, you know. Let's do it.", "...V-Very well. I will neither run nor hide.", "Don't forget that I'm a woman after all...", "What a bothersome guy... Alright, I get it.", "...Fine, just don't use the puppy-dog eyes.", "*sigh* ...Fine, fine! I'll do it as many times as you want!", "Fine with me… Wh-what? ...Even I have times when I want to do it…")
        elif ct("Imouto"):
            $rc("Ehehe... It's ok? Doing it...", "Ehehe, I'm going to move a lot for you... ♪", "[chr.name] will show you the power of love♪", "I can do naughty stuff, you know? ...Want to see?", "Uhuhu, Well then, I'll be really nice to you, ok? ♪", "Uhuhu, Well then, what should I tease first~ ♪", "Okayyy! Let's love each other a lot. ♪", "Hey? You want to? You do, don't you? We can do it, if you waaaaant~", "Aah... I want you… To love me lots…", "Ehehe♪ Prepare to receive loads and loads of my love! ♪", "Hold me really tight, kiss me really hard, and make me feel really good. ♪", "Aha, When I am with a certain someone, I do only naughty things~… Uhuhu ♪", "Yeah, let's make lots of love♪", "I-is it okay for me to climb onto you? I'm sorry if I'm heavy...", "I-I'll do my best to pleasure you!", "Yes. I'm happy that I can help make you feel good.", "I don't know how well I will do...", "Geez, you're so forceful...♪")
        elif ct("Ane"):
            $rc("Hmhm, what is going to happen to me, I wonder?", "Come on, show me what you've got...", "This looks like it will be enjoyable.", "If you can do this properly... I'll give you a nice pat on the head.", "Seems like you can't help it, huh...", "Fufufu, please don't overdo it, okay?", "Go ahead and do it as you like, it's okay.")
        elif ct("Bokukko"):
            $rc("Heh heeeh~♪ It's cool, no one's here. ♪", "Y-yeah… I sort of want to do it, too... ehehe…", "Wha!? C-can you read my mind...?", "Ah, eh, right now?", "Okay... but I'll do it like I want, kay?" ,"...Okay, that's it! I can't stand it! I've gotta fuck ya!", "S-sure… Ehehe, I'm, uh, kind of interested, too…", "Hey, let's do it while we got some time to kill...?", "Hehee, just leave it all to me! I'll make this awesome!", "Gotcha, sounds like a plan!", "Hey, maybe… The two of us could have an anatomy lesson?", "Is that ok? Ehehe... I wanted to do it too…", "Huhu… I want to do it with a pervert like you.", "Ehehe… In that case, let's go hog wild~", "Ehehe… So... let's do it. ♪", "Hmph... if you'd like, I'll give ya' some lovin'. ♪", "Got'cha. Hehe. Now I won't go easy on you.", "Y-yeah... if we're going to do it, we should do it now...", "Huhuh, I sort of want to do it now...", "Hey, er…  Wanna try doing it with me...?")
        elif ct("Yandere"):
            $rc("Fine, if you insist...", "Hehe. How should I make you feel good?", "If we have sex you will never forget me, right?♪", "Please do your best... if it's you, it'll be okay.", "Heh heh... You're going to feel a lot of pleasure. Try not to break on me.", "Alright, I'll just kill some time playing around with your body...", "Feel grateful for even having the opportunity to touch my body.", "Huhuh, I'll kill you with my tightness...")
        elif ct("Kamidere"):
            $rc("*giggle* I'll give you a feeling you'll never get from anyone else…", "Oh? You seem quite confident. I'm looking forward to this. ♪", "You're raring to go, aren't you? Very well, let's see what you've got.", "Now then, show me sex appropriate to someone qualified to be my lover...", "Hhmn... My, my... you love my body so much? Of course you do, it can't be helped.", "Oh, you seem to understand what I want from you,.. Good doggy, good doggy ♪", "Be sure to make me feel good, got it?", "Then you're bored, too.", "Feel grateful for even having the opportunity to touch my body.", "You won't be able to think about anybody else besides me after I'm done with you.", "Huhuhu, having sex with me… pretty cheeky for a pet dog~ ♪", "Hmph, Entertain me the best you can…", "Hmph, I'll prove that I'm the greatest you'll ever have...", "...For now, I'm open to the idea.", "Huhuh, I'll be using you until I'm satisfied...", "Huhu, you can't cum until I give you permission, okay? So, get ready to endure it~ ♪", "I don't really want to, but since you look so miserable I'll allow it.", "For me to get in this state... I can't believe it...", "Haa, in the end, it turned out like this…  Fine then, do as you like…")
        else:
            $rc("Oh... I guess if you like me it's ok.", "Fufu… I hope you are looking forward to this…!", "For you, I'll do my best today as well, okay?", "If it's with you... I'd do it, you know...?", "If you're so fascinated with me, let's do it.", "Hn, I want you to feel really good, okay...", "If we're going to do it, then let's make it the best performance possible. Promise?", "Now, let us discover the shape of our love. ♪", "Let's... feel good together...", "Huhn, if you do it, then… please make sure it feels good…", "Huhu, so here we are…  you can't hold it anymore, right?", "Then… Let's do it? ♪", "Sex... O-okay, let's do it...", "I don't mind. Now get yourself ready before I change my mind.", "Please let me make you feel good...", "What do you think about me, let your body answer for you…", "If you feel like it, do what you want, with my body…", "Ok, I'll serve you! ♪", "Now, [chr.name] shall give you some pleasure ~ !", "Want to become one with me? …ok", "You're this horny...? Fine, then…", "If that's what you desire...", "Oh? You've already become like this? Heh, heh... ♪", "Okay… I'd like to.", "That expression on your face... Hehe, do you wanna fuck me that much?", "You insist, hm? Right away, then!", "Heh, how can I say no?", "Hum, What should we do? ...That, there? ..hmm", "I want to do so many dirty things... I can't hold it back...", "Huhuhu, I'll give you a really. Good. Time. ♪", "You can't you think of anything else beside having sex? You're such a perv~", "So you want to do it. Right. Now? Huhu... I very much approve. ♪", "You mean, like, have sex and stuff? ...Hmm~?  Meh, you pass!", "What? You want to do it? Geez, you're so hopeless... ♪", "Come on, I can tell that you're horny… Feel free to partake of me.", "Huhn, fine, do me to your heart's content.", "Um, if you'd like, I can do it for you… I'll do my best!", "I know you wanna feel good too. ...huhu, come here…", "I can't wait any more… Huhu, look how wet I am just thinking about you... ♪", "S-shut up and... entrust your body to me… Okay?", "You've got good intuition. That was just what I had in mind, Huhuh. ♪", "Haa, your lust knows no bounds...", "Huhu, ok then… Surrender yourself to me…", "Now... show me the dirty side of you…", "You really like it, don't you… Huhuh, okay, let's go.", "Y-yes… I don't mind letting you do as you please…", "I want to do it with you...", "Hn…  Looking at you... makes me want to do it…", "If the one corrupting my body is you, then I'll have no regrets.", "Yes. Go ahead and let my body overwhelm you.", "... Leave it to me...", "I'll do it. You better be prepared.", "I wanna do all kinds of dirty things to you. Just let yourself go, okay?", " Leave it to me... I'll make you cum so much.", "All right. Do as you like.", "Let's deepen our love for each other.", "Please, go ahead and do it.", "Are we going... All the way?", "Yup. That's the way. You need more love.", "Not good... I want to do perverted things so badly, I can't stand it...", "Sure, if you want", "Hey... do me...", "I-if it's with you... I'd go skin to skin...") 

        hide screen pyt_girl_interactions
        $renpy.show('chr', what=chr.show('sex', "partner hidden", exclude=["scared"], resize=(int(config.screen_width*0.85), int(config.screen_height*0.785)), type="first_default"), at_list=[Position(ypos = 0.8)])          #temporarily / needs better possitioning and ideally tags
        with dissolve
        $renpy.pause()
        
        if dice(75):
            $ chr.normalsex += 1
        if dice(50):
            $ hero.sex += 1

        if "Virgin" in chr.traits:
            "[chr.name] has lost her virginity."
            $ chr.removetrait(traits["Virgin"])

    else:
        if ct("Half-Sister") and dice(30):
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
            $rc("I see no possible benefit in doing that with you so I will have to decline.", "No.")
        elif ct("Not Human") and dice(20):
            $rc("I wonder why humans constantly wish to have sex...")
        elif ct("Shy") and dice(30):
            $rc("I... I don't want that! ","W-we can't do that. ","I-I don't want to. ...sorry.")
        elif ct("Lesbian") and dice(25):
            $rc("Ew, don't wanna. You're a guy.", "I'm terribly sorry, but... I can't do that with a man.", "Men for me are... well...")
        elif ct("Imouto"):
            $rc("Noooo way!", "I, I think perverted things are bad!", "That only happens after you've made your vows to be together forever, right?", "...I-I'm gonna get mad if you say that stuff, you know? Jeez!") 
        elif ct("Dandere"):
            $rc("Keep sexual advances to a minimum.", "No.", "...pathetic.", "...you're no good.")
        elif ct("Tsundere"):
            $rc("I'm afraid I must inform you of your utter lack of common sense. Hmph!", "You are so... disgusting!!", "You pervy little scamp! Not in a million years!", "Hmph! Unfortunately for you, I'm not that cheap!")
        elif ct("Kuudere"):
            $rc("...Perv.", "...Looks like I'll have to teach you about this little thing called reality.", "O-of course the answer is no!", "Hmph, how unromantic!")
        elif ct("Kamidere"):
            $rc("Wh-who do you think you are!?", "W-what are you talking about… Of course I'm against that!", "What?! How could you think that I... NO!", "What? Asking that out of the blue? Know some shame!", "You should really settle down.", "What? Dying wish? You want to die?", "The meaning of 'not knowing your place' must be referring to this, eh...?", "I don't know how anyone so despicable as you could exist outside of hell.")
        elif ct("Bokukko"):
            $rc("He- Hey, Settle down a bit, okay?", "You should keep it in your pants, okay?", "Y-you're talking crazy...")
        elif ct("Ane"):
            $rc("...Give me a bit more time, please.", "Sorry... I'm not ready for that...", "Oh my, can't you think of a better way to seduce me?", "No. I have decided that it would not be appropriate.", "I'm sorry, it's too early for that.", "I don't think our relationship has progressed to that point yet.", "I think that you are being way too aggressive.", "I'm not attracted to you in ‘that’ way.")
        elif ct("Yandere"):
            $rc("I've never met someone who knew so little about how pathetic they are.", "...I'll thank you to turn those despicable eyes away from me.")
        else:
            $rc("No! Absolutely NOT!", "With you? Don't make me laugh.", "Yeah right, dickhead.", "Yeah, get the fuck away from me, you disgusting perve.", "Get lost, pervert!", "Woah, hold on there, killer. Maybe after we get to know each other better.", "Don't tell me that you thought I was a slut...?", "I'm just really tired... ok?", "How about you fix that 'anytime's fine' attitude of yours, hmm?")  
    
    jump girl_interactions
    
