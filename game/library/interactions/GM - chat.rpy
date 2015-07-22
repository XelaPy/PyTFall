###### j0
# quick navigation, search "j" + number, example: j0 - this panel
# 
#  1 - chat - general - GI
#  2 - chat - about her
#  3 - chat - about her - GM
#  4 - chat - interests
#  5 - chat - hang outs - GM
#  6 - chat - romance - GM
#  7 - chat - refused
#  8 - chat - occupation - GI

###### j1
label interactions_general:

    "You had a conversation with [chr.nickname]."

    #if she is tired
    if chr.vitality < 25:
        # if chr.has_image("profile","tired"):
            # $pytfall.gm.img_generate("profile", "tired", exclude=["nude","swimsuit","revealing","beach"])

        $narrator(choice(["But she was simply too tired to pay any serious attention to you.","But she fell asleep in the middle of it."]))
        
        $ chr.disposition += 1
        $ chr.vitality -= 2
        jump girl_interactions
    
    #additional part with chance
    if chr.joy < 15 and dice(25):
        # if chr.has_image("profile","happy"):
            # $ pytfall.gm.img_generate("profile", "happy", exclude=["nude","swimsuit","revealing","beach"])
        
        $ narrator(choice(["Her mood lightened up a little.","You were able to ease some of her unhappiness."]))
       
        $ chr.joy += 5
    
    elif dice(15):
        # if chr.has_image("profile","happy"):
            # $ pytfall.gm.img_generate("profile", "happy", exclude=["nude","swimsuit","revealing","beach"])
        
        if chr.disposition > 0:
            $ narrator(choice(["You feel especially close today."]))
        else:
            $ narrator(choice(["She was much more approachable today."]))
            
        $ chr.disposition += 5

    #main part      
    if chr.disposition > 150:
        # if chr.has_image("profile","happy") and dice(40):
            # $ pytfall.gm.img_generate("profile", "happy", exclude=["nude","swimsuit","revealing","beach"])
        # else:    
            # $ pytfall.gm.img_generate("profile", exclude=["angry","defiant","provocative","sad","scared","shy","tired","uncertain","nude","swimsuit","revealing","beach"])
        
        $ narrator(choice(["It was quite a friendly chat.","You gossiped like close friends.","She welcomed the chance to spend time with you.","She is visibly at ease when talking to you.","You both have enjoyed the visit."]))
    
    elif chr.disposition > -100:
        # if chr.has_image("profile","uncertain") and dice(70):
            # $ pytfall.gm.img_generate("profile", "uncertain", exclude=["nude","swimsuit","revealing","beach"])
        # else:
            # $ pytfall.gm.img_generate("profile", exclude=["angry","confident","defiant","ecstatic","shy","happy","provocative","scared","tired","nude","bikini","swimsuit","revealing","beach"])        
        
        if "Impersonal" in chr.traits or "Dandere" in chr.traits or "Kuudere" in chr.traits:
            $ narrator(choice(["But there was a lot of awkward silence.","But you had to do most of the talking.","There is no sign of her opening up to you yet.","But it was kind of one-sided."]))      
        else:
            $ narrator(choice(["It's all still a little bit stiff.","There's still some reservation though…","It's still hard to find common ground.","But it was somewhat forced."]))
    
    else:
        # if chr.has_image("profile","defiant") and dice(80):
            # $ pytfall.gm.img_generate("profile", "defiant", exclude=["nude","swimsuit","revealing","beach"])
        # elif chr.has_image("profile","angry"):
            # $ pytfall.gm.img_generate("profile", "angry", exclude=["nude","swimsuit","revealing","beach"])
        # else:
            # $ pytfall.gm.img_generate("profile", exclude=["confident","ecstatic","happy","provocative","shy","tired","nude","swimsuit","revealing","beach"])        
        
        $ narrator(choice(["There's still a good amount of mistrust between you." ,"But it was difficult for both of you.","She was not very pleased to see you.","It was clearly uncomfortable for her to speak to you.","She was suspicious of you the entire time and never let her guard down."]))
    
    $ chr.disposition += (randint(1, 5))
    $ chr.joy += (randint(0, 3))
    
    jump girl_interactions
    

###### j2
label interactions_abouther:
    
    if chr.disposition < -400:
        if chr.status != "slave":
            $ pytfall.gm.img_generate('profile', 'sad')
            $ rc("You're a shitty employer; I have no idea why I'm still working here!", "A crazy axe-murderer would be a better employer than you!")
        
        else:
            $ pytfall.gm.img_generate('profile', 'sad')
            $ rc("I wish that I the resolve to kill myself...", "My life in your service is awful.")
        
        $ chr.disposition += 5
        
        if dice(int(round(hero.charisma*0.5))):
            $ chr.refinement += 1
            $ chr.joy += 3
            $ chr.disposition += 1
        
        $ hero.exp += adjust_exp(hero, randint(5, 10))
        $ chr.exp += adjust_exp(chr, randint(5, 10))
    
    elif chr.mech_relay["daysemployed"] < 10:
        # Less than 10 days in service:
        if chr.status != "slave":
            $ pytfall.gm.img_generate('profile', 'indifferent')
            $ rc("I'm still adjusting to the new position.", "Trying to find my bearings with this new career.")
        
        else:
            $ pytfall.gm.img_generate('profile', 'indifferent')
            $ rc("I want to serve you better, master.", "A new master takes a while to get used to...")
        
        $ chr.disposition += 5
        $ chr.joy += 3
        
        if dice(int(round(hero.charisma*0.5))):
            $ chr.refinement += 1
            $ chr.joy += 3
            $ chr.disposition += 1
        
        $ hero.exp += adjust_exp(hero, randint(5, 10))
        $ chr.exp += adjust_exp(chr, randint(5, 10))
    
    elif chr.disposition < 0:
        if chr.status != "slave":
            if chr.joy >= 50:
                $ pytfall.gm.img_generate('profile', 'indifferent')
                $ rc("I'm fine, but I just wish you weren't such a terrible employer!", "As good as can be expected under the circumstances, 'boss'...")
            
            else:
                $ pytfall.gm.img_generate('profile', 'sad')
                $ rc("I'm sad and you suck... what else do you want me to say?", "I'm looking for new employment opportunities; that's how I'm feeling!")
        
        else:
            if chr.joy >= 50:
                $ pytfall.gm.img_generate('profile', 'indifferent')
                $ rc("I am 'ok'. Just wish I had a better owner...")
            
            else:
                $ pytfall.gm.img_generate('profile', 'sad')
                $ rc("There isn't much to say... I'm sad and you're mean...", "I feel like it would be better if you sold me off at the next auction!")
        
        $ chr.disposition += 5
        $ chr.joy += 3
        
        if dice(int(round(hero.charisma*0.5))):
            $ chr.refinement += 1
            $ chr.joy += 3
            $ chr.disposition += 1
        
        $ hero.exp += adjust_exp(hero, randint(5, 10))
        $ chr.exp += adjust_exp(chr, randint(5, 10))
    
    # elif chr.disposition < 400:
    else:
        if chr.status != "slave":
            if chr.joy >= 50:
                $ pytfall.gm.img_generate('profile', 'happy')
                $ rc("I'm happy and this job definitly doesn't suck!", "I'm comfortable and content with this arrangement.")
            
            else:
                $ pytfall.gm.img_generate('profile', 'sad')
                $ rc("Not very chipper but I expect things to get better soon!", "Bit sad, if truth be told.")
        
        else:
            $ pytfall.gm.img_generate('profile', 'happy')
            
            if chr.joy >= 50:
                $ rc("Very well, thank you Master!", "I am satisfied with my life as a slave!")
            
            else:
                $ pytfall.gm.img_generate('profile', 'sad')
                $ rc("I'm a bit sad, but Master is kind so I'm looking for a brighter tomorrow!", "You've been very nice to me in general, so I won't complain!")
        
        $ chr.disposition += 5
        $ chr.joy += 3
        
        if dice(int(round(hero.charisma*0.5))):
            $ chr.refinement += 1
            $ chr.joy += 3
            $ chr.disposition += 1
        
        $ hero.exp += adjust_exp(hero, randint(5, 10))
        $ chr.exp += adjust_exp(chr, randint(5, 10))
    
    jump girl_interactions
    
###### j3
label girl_meets_abouther:
    $ gm_abouther_list = []
    
    if chr.disposition > 500:
        $ gm_dice = 98
        $ gm_disp_mult = 0.4
    
    elif chr.disposition > 50:
        $ gm_dice = 98
        $ gm_disp_mult = 0.8
    
    elif chr.disposition > 20:
        $ gm_dice = 95
        $ gm_disp_mult = 1
    
    elif chr.disposition > -20:
        $ gm_dice = 90
        $ gm_disp_mult = 1
    
    elif chr.disposition > -300:
        $ gm_dice = 75
        $ gm_disp_mult = 1
    
    else:
        $ gm_dice = 25
        $ gm_disp_mult = 1.8
    
    if ct("Half-Sister") and dice(35):
        if ct("Yandere"):
            $rc("We used to play doctor and tear off each other's clothes, heh.", "We used to bathe together, so... you got to touch sister's body all over....", "*She smiles and stares at you.*", "Whenever we took a bath together, I used to wash your every nook and cranny. And I mean EVERY nook and cranny♪")
        elif ct("Impersonal"):
            $rc("Do you remember how you used to pull pranks on me?", "I have always observed you. I know all there is to your character.", "I've known what kinds of sexual fetishes you have since a long time ago, brother.")
        elif ct("Tsundere"):
            $rc("We used to take a bath together back in the days, didn't we? Now...? B...but... hey! You know we shouldn't do that!", "Now that I think about it, I spent more time with you, brother, than Mom and Dad.", "You've always gone out of your way to protect your sister. I should thank you for that.", "I went overboard when I tried to discipline you back when we were little. To be honest, I'm sorry about that now.", "Remember that collection of dirty magazines you used to cherish? I was the one who threw them away. I am... still sorry about that, brother.")
        elif ct("Dandere"):
            $rc("We've been together since we were small... Have you had enough of it? Well, I'm still not tired of it yet.", "You've taught me all kinds of things since a long time ago... even perverted things.", "You used to play doctor with me all the time... You were so perverted, even back then.")
        elif ct("Kuudere"):
            $rc("I used to be a crybaby? D-don't remind me of such things...", "M-my promise to marry you? T-there's no way I'd remember something like that!", "Getting engaged with my brother... I only thought that was possible back when we're kids.", "You always protected me. Therefore, I decided that I had to become strong.")
        elif ct("Ane"):
            $rc("Hehe, you've grown so much... That makes your sis proud.", "You weren't able to fall asleep without sis by your side when we were little.", "Whenever I wore a skirt, you always tried to peek underneath it... You were already so perverted when we were little.", "I've taken care of you since you were little. Therefore, sister knows everything about you.", "My purpose in life has always been staying by your side.", "When we were younger, I was always by your side because I swore I would always protect you.")
        elif ct("Imouto"):
            $rc("I used to think I'd get as tall as you.", "You remember we used to play shop when we were little? Wha... You should forget about THAT game!", "You have protected me from bullies when I was little.... That made me so happy.")
        elif ct("Kamidere"):
            $rc("I decided that you'd be mine when I was still very little.", "You've belonged to sis ever since you were born.", "You're my brother who I've personally helped to raise. There's no way I'd let you go.")
        elif ct("Bokukko"):
            $rc("When we were little, didn't you say you'd make me your wife someday or something?", "When we were kids, we went exploring in the forest together and we both got lost.", "We used to climb fences and then jump off them. The two of us got injuries all over.", "You used to be so wee and now that huge, na?")
        else:
            $rc("We used to bathe together a lot when we were little.♪", "The bath used to be our playground... but you tickled me way too much.", "When it was night time, you would always try to slip into my bed unnoticed.", "You used to tag along with me wherever I went when we were little.")
    
    if ct("Lesbian"): 
        $ gm_disp_mult = ((gm_disp_mult)*1.3)
    
    if dice(gm_dice):
        $ chr.disposition += (randint(6, 12)*(gm_disp_mult))
        $ pytfall.gm.abouther_count = 0
        
        if chr.disposition > 600:
            if dice(50):
                $ gm_abouther_list.append(choice(["I think you're intresting."])) 
        
        if ct("Big Boobs", "Abnormally Large Boobs"):
            if dice(50):
                $gm_abouther_list.append(choice(["I notice men, everyone of them, staring at nothing but my boobs.", "I've outgrown yet another bra... I wish something could be done about this...", "Hey, [hero.name], do you know what my charms are? Ufu, shall I show you? I'm pretty sure I can make your heart skip a beat♪", "[hero.name], my charms are the best, aren't they?", "All the men just keep staring at my breasts. Are such big ones really that fascinating?", "The reason you're interested in me is my big breasts, right?", "They say that big breasts are the best, but truth be told they're heavy and make the shoulders stiff, not good at all."]))
        
        if ct("Small Boobs"):
            if dice(50):
                $gm_abouther_list.append(choice(["I read lately that the hunt is on for small breasts. Who cares about big tits!", "It's better without large breasts. They'd only get in the way... Probably...", "Small breasts have their good points as well, don't you think? You do think so, right?"]))     
        
        if ct("Lesbian"):
            $gm_abouther_list.append(choice(["I am REALLY interested in female's bodycurves.", "I would like to go to an all girls' school. Imagine, only girls, everywhere... That would be great...", "Have you ever brought a girl home? I want to try that.", "I'd like to bring a cute girl home.", "Isn't it normal to be attracted to charming girls? I think it's totally proper♪", "Something I like? Hmm~ Maybe watching cute girls?", "Girls look really cute, don't they? I just want to eat one up.", "I like cute things. Like girls, for example.", "If I were a boy, I sure would explore every inch of the girl I was dating…"]))
        
        if ct("Bisexual"):
            $gm_abouther_list.append(choice(["In love, gender makes no difference..."]))
        
        if co("Warrior"):
            if ct("Shy") or ct("Coward"):
                $gm_abouther_list.append(choice(["I have been trained in combat, but I really dislike violence.", "I know a lot about self-defense… but I really hope that I wouldn’t ever need to use it.", "I know how to use a weapon… but it still scares me a bit.", "I can do well in combat training, but in practice…", "They say that I may have the skill, but not the spirit of a warrior…", "I carry a weapon, but I don’t think I would have the heart to hurt someone."]))
            
            elif ct("Virtuous"): 
                $gm_abouther_list.append(choice(["I know how to pacify someone without hurting them. That’s the right way to do it.", "I learned how to fight so I can protect others."]))

            elif ct("Adventurer"): 
                $gm_abouther_list.append(choice(["I like to sharpen my battle skills.", "I enjoy exploring catacombs.", "A duel sounds interesting, do you mind?"]))
            else:
                $gm_abouther_list.append(choice(["I have been trained in combat. So you better not be trying anything funny <grins>", "I may not look like it, but I can handle my weapons really well.", "Some creeps tried to ambush me once. I gave them plenty of time to repent at the infirmary.", "Sometimes I watch the matches in the arena to get inspiration to improve my own technique.", "It's better to know how to defend yourself in this town. You never know what may happen, especially if you are a woman."]))
        
        if ct("Dawdler"):
            $gm_abouther_list.append(choice(["Hey, have you heard the saying, “Good things come to those who sleep?” … Uh, and wait?", "I aways get sleepy after a meal~ It's just natural providence.", "Yearning for the bed is part of being human.", "Fuwa~ This season sure makes me sleepy~", "It's fine to skip a bath if you don't reek of sweat.", "I can't get rid of this sleepiness...", "No matter how much I sleep I can't get enough of it....", "*Yawn* You know lack of sleep is damaging to the skin.", "I'm sick of being sleepy. I don't think it's from a lack of sleep though.", "Unlike most days, today I got up early… *Yaaawn~*…", "I'm not really a morning person…  Ah, It's not because I'm too busy at night, though…", "There are days when I just don't feel like doing anything... a lot of them, actually."]))
                       
        if ct("Frigid"):
            $gm_abouther_list.append(choice(["Why does everyone get so excited about underwear? It's just fabric…", "Relations should be clean and wholesome, an example to others."]))
        
        if ct("Exhibitionnist"):
            $gm_abouther_list.append(choice(["I just love attention...", "Have you ever thought of doing it in public? Just imagine all those eyes…", "It would be a waste not to show some skin when the weather is nice.", "It arouses me when strangers are staring... Stripping me with their eyes..."]))
        
        if ct("Clumsy"):
            $gm_abouther_list.append(choice(["It's commonplace to spill all the contents when opening a bag of candy, isn't it?", "I broke another plate. How many has it been now..? I wish I could do something about this."]))
        
        if ct("Sexy Air"):
            $gm_abouther_list.append(choice(["Everyone keeps saying that the way I lick my lips is incredibly erotic.", "I like to use my tongue to play around with candy in my mouth. Don't you?", "Aah, I wanna eat something sour..."]))
        
        if ct("Nymphomaniac"):
            $gm_abouther_list.append(choice(["No matter how much I do it, I still can't cool down. Hehe, what do you *think* I'm talking about?", "I've been having these unintentional s... sexual urges lately....", "My body gets horny all on its on even when I'm by myself... It's so frustrating!", "What's with this heat in my body...", "I can become horny just like that all of a sudden... And before I even realize, I'm already...", "My needs are left unsatisfied!", "There's not enough. I get no love, cock, or cum... I'm lacking all of it!"]))
        
        if ct("Virtuous"):
            $gm_abouther_list.append(choice(["It would be great if people would be nicer to each other…", "I did some volunteer work the other day, it was a pleasant experience.", "It really pains me when I see someone suffering.", "It’s the most elevating feeling when you can help someone, isn’t it?"]))
        
        if ct("Sadist"):
            $gm_abouther_list.append(choice(["I want to violate a guy with a strap-on. You game?", "It makes me so wet when my lover gets a scared look on his face.", "Huhu, discipline is lovely, isn't it..."]))
        
        if ct("Psychic"):
            $gm_abouther_list.append(choice(["Just small gestures and facial expressions can reveal even the most ulterior motives.", "I can tell a lot about your personality just from your posture.", "I'm able to read emotions easily.", "It's not difficult for me to guess what people will do, if I'm able to observe them for a while.", "While it's hard to tell the motives of some, the majority of people are so predictable…", "It's hard to predict the movements of a warrior. They are trained to hide their thoughts.", "A sea of darkness... will consume everything...", "You... have a shadow of death hanging over you...", "A spell has been cast... Long ago... But it's still here...", "...Aren't you dead? Ah, never mind.", "This world could be destroyed..."]))
        
        if ct("Serious"):
            $gm_abouther_list.append(choice(["Only with a clear mind can you be truly effective. Emotions just get in the way.", "Nothing good can come from being too emotional.", "If a problem has a solution, there's no reason to be worried. And if it doesn't… then there's no reason to be worried either.", "Anger or tears cannot solve anything."]))
        
        if ct("Masochist"):
            $gm_abouther_list.append(choice(["I don't hate the pain. Because...it can feel good in its own way...", "Tied up and blindfolded... Isn't it exciting?", "Being mistreated a little... can be fun....", "No, I don't like pain. Even so, sometimes chains are... oh no, what am I saying?!", "If you tied me up... the experience... Both my body and soul... Oh no, what am I saying..."]))
        
        if ct("Athletic"):
            $gm_abouther_list.append(choice(["I may look slow, but I'm actually really good at sports.", "I like to exercise.", "I think it's important to keep yourself in good shape.", "Want to race? I won't lose.", "I went exercising and ran up quite a sweat. It's a good feeling."]))
        
        if ct("Artificial Body"):
            $gm_abouther_list.append(choice(["Do I actually appear human to you? Oh nothing, nevermind that.", "I can keep going even without much sleep. Isn't that great?", "I've been having these weird dreams where I'm me, yet, I'm not me.... I wonder what this could be about...."]))
        
        if ct("Neat"):
            $gm_abouther_list.append(choice(["It's a good day for doing laundry.", "When you don't diligently clean wet areas of the house you can get an outbreak of mold and various bacteria.", "For some reason, the dust on the windowsill really bothers me.", "Looks like I might really like cleaning... What's with those suspicious eyes?", "I have training in providing good customer service.", "Most people don't like them, but chores are an important job, too.", "You can make any place clean and cozy with thorough work.", "Chores take much less time when properly organized.", "Pleasant service is the foundation of any successful business. Nothing can drive off customers faster than rudeness.", "Cleanliness is next to godliness. Don't you agree?"]))
        
        if ct("Heavy Drinker"):
            $gm_abouther_list.append(choice(["You wanna have a drinking contest? Hehe, I won't lose to you.", "Whenever I drink alcohol I want to tear all my clothes off... Hehe.", "I say, there's always a reason to drink."]))
        
        if ct("Curious"):
            $gm_abouther_list.append(choice(["Experiencing new things is loads of fun, isn't it?", "The truth always comes up at the very end... No, it's nothing.", "Hey, I totally found 100 money on the ground earlier today. Isn't that crazy?!", "I found some more money -oh wait, it's just a shiny rock. Boo =/", "Want to see the shells I picked up at the beach?", "I spent a long time chasing a really cute cat I saw."]))
        
        if ct("Shy"):
            $gm_abouther_list.append(choice(["It would be good... if I could just be a bit more confident... I think...", "I'm no good with public speaking...", "I don't like being competitive...", "Umm, I'm... not really good with standing out...", "I don't like making eye contact...", "...Appearing in front of people... I'm reluctant...", "I'm not fond of... talking to people..."]))
        
        if ct("Always Hungry"):
            $gm_abouther_list.append(choice(["I'm still hungry, no matter how much I eat.", "I can eat nonstop, is there something wrong with that?", "No matter how much I devour, my stomach is still empty. Am I still growing or something?", "I'm feeling hungry...", "There's so much delicious food at this time of year... It's dangerous!", "You'll get heat fatigue if you don't eat properly.", "I wonder why I'm always so hungry. I'm not gaining much weight, so it's fine, but...", "I really do eat too much but I still manage to keep in shape, so....", "Have I gained some weight? No, that's just my imagination....", "I've got a craving for sweets just now...", "I've had a huge appetite lately. If this continues then I might gain weight... This has to stop."]))
        
        # if there is not enough specific aswers, a vague one is added to the list
        if len(gm_abouther_list) < 3:
            $gm_abouther_list.append(choice(["Hm? A little of this, a little of that?", "...I don't really have much to say.", "Nothing much, there's nothing worth mentioning.", "What I'm doing? The usual stuff...", "I'm just normal, I guess.", "I like just about anything.", "Hmm, there's not much to talk about.", "Now that I think about it... am I just boring?", "I'm just about average, I guess."]))
    
    else:
        $ chr.disposition -= (randint(1, 7)*(gm_disp_mult))
        jump interactions_refused
    
    $ g(choice(gm_abouther_list))
    $ gm_abouther_list = None
    jump girl_interactions

###### j4
label interactions_interests:
    if ct("Exhibitionnist") and dice(15):
        $rc("Showing off my 'goods' to the crowd,", "Just being one with nature, if you catch my meaning.")
        
        if d(80) and chr.flag("gm_stripped_today") != day:
            menu:
                g "Would you like to see me naked?"
                
                "Hell Yeah":
                    g "You're weird... but I'm weird too ;)"
                    $pytfall.gm.change_img(chr.show("nude", "simple bg", type="first_default", exclude=main_sex_tags))
                    g "So, what do you think?"
                    $pytfall.gm.restore_img()
                    $chr.disposition += 10
                    $chr.set_flag("gm_stripped_today", value=day)
                
                "Yes!":
                    $pytfall.gm.change_img(chr.show("nude", "simple bg", type="first_default", exclude=main_sex_tags))
                    g "You like?"
                    $pytfall.gm.restore_img()
                    $chr.disposition += 5
                    $chr.set_flag("gm_stripped_today", value=day)
                
                "No":
                    g "Well, screw you then!"
                    $chr.disposition -= 20
    
    else:
        $ line = rts(chr, {"Dandere": ["I sleep on my days off. ...Is that bad?"], "Athletic": ["Working out.", "Exercising", "Running laps"], "Dawdler": ["I spend my days just lying around. Isn't there anything to do around here?", "I like beach sports, y'know?　Just watching, though."],
                            "Curious": ["In order to keep up with the latest fads, intelligence gathering is essential.", "Strolling through town is a nice change of pace."], "Ane": ["I think living every day as an ordinary girl is the ultimate happiness.", "Reading in the bath. It's nice to do in such a confined space."],
                            "Well-mannered": ["Etiquette classes at PyTFalls Educators", "Proper manners.", "Style and grace."], "Imouto": ["Gardening is so much fun, you know...?"], "co('Caster')": ["The study of magic.", "Arcane Arts.", "Shooting lightning and fireballs at things."],
                            "Adventurer": ["Treasure hunting!", "Adventuring!", "Exploring dungeons!"], "Kuudere": ["I'm not really in the mood right now...", "Leave me alone."], "Tsundere": ["I-It's not like I find small animals and children and that stuff charming!"], "Yandere": ["Mmmbfrs?", "What's up there?", "Spinning", "Do you know who I am? I am... I am forgot..."],
                            "co('Warrior')": ["I like to sharpen my battle skills.", "I rather enjoy exploring catacombs.", "A duel sounds interesting; do you mind?"], "co('SIW')": ["Finding the best ways to please others.", "Trying to find someone who'd try interesting positions, if you know what I mean."], "Dancer": ["Exotic dancing!", "Admiration from people.", "Dancing, poles, you know... the usual stuff.", "Searching for new moves on the podium.", "Perfecting my dance moves."],
                            "co('Server')": ["Best way to get the wine stains out. Do you know any?", "Chatting with strange customers at the bar.", "Keeping the bar running."], "default": ["Nothing special, really."]})
        
        g "[line]"
    
    $ chr.disposition += randint(1, 4)
    jump girl_interactions

###### j5
label interactions_hangouts:
    if chr.disposition < 200:
        jump interactions_refused
    
    else:
        if ct("Nymphomaniac") and dice(40):
            $rc("Wherever there is something or someone I can shag.", "At the sex-club, oh no--I've said too much...#1 rule...Never talk about the sex club! WTF was I thinking?")
        elif ct("Nerd"):
            $rc("Library, where do {color=[red]}you{/color} go for fun?", "I cozy under a tree with a good book.")
        elif co("Warrior"):
            $rc("The Arena, where else?", "Window shopping at the blacksmith's!")
        elif co("SIW"):
            $rc("Wherever men with full pockets are hanging.", 'Us "Fancy Girls" usually hang around in the Red Light District', "Brothel...Don't look at me like that!")
        elif ct("Dancer"):
            $rc("Exotic Dancing academy", "Close to a pole and not any of the two you're thinking.", "Strip Club.")
        elif co("Server"):
            $rc("At the bar, tending to it.", "I love broom and dustbins exhibits.", "Wherever cleaning is required.")
    
    jump girl_interactions

###### j6
label interactions_romance:
    if chr.disposition < 500:
        jump interactions_refused
    
    else:
        if ct("Impersonal"):
            $rc("To express it in words is very difficult...", "Infatuation and love are different. Infatuation will fade, but love's memory continues forever.")
        elif ct("Shy") and dice(30):
            $rc("Lovers... Th-they're supposed to...hold hands, after all... Right?", "Wh-what comes after a k-kiss is... It's... Awawa...", "If it's the person you love, just having them turn around and smile... Is enough to make you happy...")
        elif ct("Nymphomaniac") and dice(20):
            $rc("*sigh* I always have such a high libido...", "Um... Love can start from lust... right?", "If you are in love, having sex is totally normal, right?", "People are no more than animals, so it's only natural to copulate...right?", "Well, doing perverted stuff is proof that you're healthy.", "Me thinking about sex? Not at all... Great. Now that you brought it up...")
        elif ct("Bisexual", "Lesbian") and dice(25):
            $rc("Love runs deeper than gender.")
        elif ct("Dandere"):
            $rc("If you like them, you like them. If you hate them, you hate them. That's all there is to it. Right?", "My dream yesterday... It was so lovey-dovey and erotic.", "I think it is a good thing to be loved by someone.", "Getting close to people other than the one you love is kind of...", "You can still live a good life without a lover, don't you think?")
        elif ct("Tsundere"):
            $rc("M...men and women feels arousal differently.... F-f-forget what I just said!", "Thick and hard? What the... You idiot, what are you saying! That's not what you meant? ... You idiot!", "E-even I want to be a good bride someday, you know...?", "Things like l-love or affection, are all excuses.")
        elif ct("Kuudere"):
            $rc("To feel the same feelings towards each other... To be partners for life... That's what I long for.", "Two people in love devoting themselves to each other, that sounds like pure bliss to me...", "True love isn't about showing off to everyone else... It's the small things you do for your partner that matter.", "There's gotta be someone willing to support me out there somewhere...", "Chance encounters only happen with both time and luck...Well, I suppose you could call it fate.")
        elif ct("Imouto"):
            $rc("Hey, when's my knight in shining armor gonna come along? I guess I gotta need saving first?", "That's weird... Today's love fortune was supposed to be a sure thing... Hmm...", "That book is very interesting... A boy and a girl who you'd think are twins get together, but in fact...", "L-love and affection and th-that stuff, I don't really get it very well...", "If I'm going to date someone, they should be rich~, and want kids~ And they should be totally committed to me~")
        elif ct("Ane"):
            $rc("You're deciding who will be your partner for life.　It would be strange not to be worried about it.", "I think just having the one you love beside you is the ultimate happiness.", "I need a person whom I can rely on.", "Lost loves are important to build character, I think.", "As you've probably noticed, I'm the devoted type♪", "Of course, I'd wanna stay by my loved one's side. Or, rather than being by their side, it's more, like, I want to support them?")
        elif ct("Kamidere"):
            $rc("Seriously, how can I... think of such unpleasant thoughts...", "When my body gets hot, it's like my discipline starts to crumble...", "There are things more important than physical infatuation.","Making men my playthings is a simple matter for one such as I. Eheh!", "Love is nothing but an expression of ego, you know.", "You can't disobey your instincts. Isn't keeping up this charade painful for you?")
        elif ct("Bokukko"):
            $rc("Love is a competition! A conflict! A war!", "If the other person won't give you a second glance, you need to make 'em. It's simple, really.", "Love, hmm~ ... Hn, just thinking about it makes me sort of embarrassed...", "I'm gonna be the bestest wife!", "Is this that fate thing they're talking about?")
        elif ct("Yandere"):
            $rc("Huhu, a girl in love is invincible~", "Nothing motivates you quite like 'love', huh...", "If it's just with their mouth, everyone can talk about love. Even though none of them know how hard it is in reality...")
        else:
            $rc("Getting your heart broken is scary, but everything going too well is kinda scary for its own reasons too.", "One day, I want to be carried like a princess by the one I love～...", "Hehe! Love conquers all!", "I'm the type to stick to the one I love.", "Being next to someone who makes you feel safe, that must be happiness...", "Love... sure is a good thing...", "Everyone wants to fall in love.")

    $ chr.disposition += randint(10, 20)
    jump girl_interactions

###### j7
label interactions_refused:
    if ct("Impersonal"):
        $rc("Conversation denied.", "It's none of your business.", "...")
    elif ct("Shy") and dice(50):
        $rc("I-I won't tell you... ", "It's nothing. ...sorry.", "I don't want to talk... sorry.", "W-Well... I d-don't want to tell you...", "Ah, ugh... Do I have to tell you...?")
    elif ct("Dandere"):
        $rc("I don't feel the need to answer that question.", "...later...maybe...", "*she stares into the sky*")
    elif ct("Kuudere"):
        $rc("I've got no reason to tell you.", "I'm not in the mood for that right now.", "Why do I have to tell you?")
    elif ct("Tsundere"):
        $rc("Hmph! Who would tell you!", "Eh? You expect me to tell you?")
    elif ct("Imouto"):
        $rc("Uhuhu♪ I won't tell you~ ♪ ","I'm not going to tell you~ ","It's a secret!", "Umm, is it bad if I don't answer...?")
    elif ct("Yandere"):
        $rc("Shut up, leave me alone...", "Conversation... What a pain...", "<She is not listening>", "You talk too much.")
    elif ct("Kamidere"):
        $rc("Ahhh, geez, just shut up already!", "And what will hearing that do for you?", "And what good would knowing that do you?")
    elif ct("Ane"):
        $rc("...I don't feel like answering.", "Sorry, can we talk later?", "Sorry, but I don't want to answer.", "*sigh*… Don't you have anything else to do?")
    elif ct("Bokukko"):
        $rc("Eh, say what?", "Why do I hafta give you an answer?", "I'm not gonna answer that.")
    else:
        $rc("I don't want to answer.", "I don't want to talk now.", "It's none of your business ", "Hmph, Why should I have to tell you?", "I'm not in a mood for chatting.", "Must I give you an answer?")
    
    jump girl_interactions
    

###### j8
label interactions_occupation:
    menu:
        "Ask her to switch to:"
        "Prostitute" if chr.occupation != "Prostitute":
            if chr.status == "slave" and chr.disposition > -500:
                g "As you wish Master..."
                if chr.occupation != "Stripper" and chr.disposition < 200:
                    "She doesn't look too happy about this..."
                    python:
                        chr.joy -= 40
                        chr.disposition -= 50
                        chr.occupation = "Prostitute"
                else:
                    $ chr.occupation = "Prostitute"
                    
            elif chr.status == "slave":
                g "Never, not for you!"
                "She seems rather cross with you..."
                
            else:
                # Case free girl:
                if chr.disposition < 950 + chr.level:
                    $ rc("Don't even think of me in that way!", "Nope!", "I refuse")
                else:
                    g "Well... why not, I am willing to try new things..."
                    $ chr.occupation = "Prostitute"
                
        "Stripper" if chr.occupation != "Stripper":
            if chr.status == "slave" and chr.disposition > -500:
                g "As you wish Master..."
                if chr.occupation != "Prostitute" and chr.disposition < 200:
                    "She doesn't look too happy about this..."
                    python:
                        chr.joy -= 40
                        chr.disposition -= 50
                        chr.occupation = "Stripper"
                else:
                    $ chr.occupation = "Stripper"
                    
            elif chr.status == "slave":
                g "Never, not for you!"
                "She seems rather cross with you..."
                
            else:
                # Case free girl:
                if chr.disposition < 950 + chr.level:
                    $ rc("Don't even think of me in that way!", "Nope!", "I refuse")
                else:
                    g "Well... why not, I am willing to try new things..."
                    $ chr.occupation = "Stripper"
                
        "ServiceGirl" if chr.occupation != "ServiceGirl":
            if chr.status == "slave" and chr.disposition > -500:
                g "As you wish Master..."
                $ chr.occupation = "ServiceGirl"
                    
            elif chr.status == "slave":
                g "Never, not for you!"
                "She seems rather cross with you..."
                
            else:
                # Case free girl:
                if chr.disposition < 950 + chr.level:
                    $ rc("Don't even thing of me in that way!", "Nope!", "I refuse")
                else:
                    g "Well... why not, I am willing to try new things..."
                    $ chr.occupation = "ServiceGirl"
                
        "Warrior" if chr.occupation != "Warrior" and chr.status != "slave" and chr.has_image("battle_sprite"):
                # Case free girl:
                if chr.disposition < 950 + chr.level:
                    $ rc("Don't even thing of me in that way!", "Nope!", "I refuse")
                else:
                    g "Well... why not, I am willing to try new things..."
                    $ chr.occupation = "Warrior"
                    
        "Just kidding":
            python:
                chr.AP += 1
                hero.AP += 1
    
    jump girl_interactions
    
