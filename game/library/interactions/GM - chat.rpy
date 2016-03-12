# general chat
label interactions_general:

label interactions_general:
    "You have a small chat with [char.nickname]."
    $ interactions_check_for_bad_stuff(char)
    $ interactions_check_for_minor_bad_stuff(char)
    $ m = interactions_flag_count_checker(char, "flag_interactions_general")
    if m >= (randint(3,5) + interactions_set_repeating_lines_limit(char)):
        call interactions_too_many_lines
        $ char.disposition -= randint(1,m)
        $ char.joy -= randint(0,1)
        $ del m
        jump girl_interactions
    $ del m
    if dice(randint(40,60)) and dice(hero.charisma*0.5) and dice(char.joy):
        if char.disposition >= 50:
            $ narrator(choice(["You feel especially close today."]))
            $ hero.exp += randint(2, 5)
            $ char.exp += randint(2, 5)
            $ char.joy += randint(0, 1)
        else:
            $ narrator(choice(["She was much more approachable today."]))
            $ hero.exp += randint(2, 5)
            $ char.exp += randint(2, 5)
            $ char.disposition += randint(1, 4)

    if char.disposition >= 100:
        if ct("Impersonal") or ct("Dandere") or ct("Shy"):
            $ narrator(choice(["She didn't talked much, but she enjoyed your company nevertheless.", "You had to do most of the talking, but she listened you with a smile.", "She welcomed the chance to spend some time with you.", "She is visibly at ease when talking to you, even though she didn't talked much."]))
        else:
            $ narrator(choice(["It was quite a friendly chat.", "You gossiped like close friends.", "She welcomed the chance to spend some time with you.", "She is visibly at ease when talking to you.", "You both have enjoyed the conversation."]))
    elif char.disposition >=-100:
        if ct("Impersonal") or ct("Dandere") or ct("Shy"):
            $ narrator(choice(["But there was a lot of awkward silence.", "But you had to do most of the talking.", "There is no sign of her opening up to you yet.", "But it was kind of one-sided."]))      
        else:
            $ narrator(choice(["It's all a little bit stiff.", "There's some reservation though...", "It's hard to find common ground.", "But it was somewhat forced."]))
    else:
        $ narrator(choice(["There's a good amount of mistrust between you.", "But it was difficult for both of you.", "She was not very pleased to see you.", "It was clearly uncomfortable for her to speak to you.", "She was suspicious of you the entire time and never let her guard down."]))
    if char.disposition <= -250:
        $ char.disposition += randint(1, 3)
    if char.disposition <= 0:
        $ char.disposition += randint(2, 5)
    if char.disposition <= 200:
        $ char.disposition += randint(1, 4)
    elif dice(50):
        $ char.disposition += randint(1, 2)
    elif dice(50):
        $ char.disposition += 1
    else:
        $ char.joy += 1
    $ hero.exp += randint(1, 3)
    $ char.exp += randint(1, 3)
    jump girl_interactions
    
# ask about job
label girl_interactions_aboutjob: # TO DO: here would help additional logic based on actual recent jobs events
    "You asking about her job."
    $ interactions_check_for_bad_stuff(char)
    $ m = interactions_flag_count_checker(char, "flag_girl_interactions_aboutjob")
    if m > 1:
        call interactions_too_many_lines
        $ char.disposition -= randint(0,m)
        $ del m
        jump girl_interactions
    $ del m
    $ hero.exp += randint(1, 2)
    if char.flag("daysemployed") < 5:
        # Less than 10 days in service:
        $ char.override_portrait("portrait", "indifferent")
        if char.status != "slave":
            $ rc("I'm still adjusting to the new position.", "I'm trying to find my bearings with this new career.")
        else:
            $ rc("I want to serve you better, master.", "A new master takes a while to get used to...")
        $ char.disposition += 1
        $ char.joy += 1
        if dice(round(hero.charisma*0.5)):
            $ narrator(choice(["She was much more approachable today."]))
            $ char.joy += 1
            $ char.disposition += randint(1, 2)
            $ hero.exp += randint(0, 2)
            $ char.exp += randint(0, 2)
        $ char.restore_portrait()
    elif char.disposition <= -350:
        $ char.override_portrait("portrait", "sad")
        if char.status != "slave":
            if ct("Impersonal") or ct("Dandere") or ct("Kuudere"):
                $ rc("... <She doesn't want to talk>", "I don't think I'll linger here for a long time.", "I do not wish to about it. Leave me alone.")
            elif ct("Shy"):
                $ rc("Um... I-I don't think this job is for me...", "I... I'm looking for another job... Sorry.")
            else:
                $ rc("You're a terrible employer; I have no idea why I'm still working here...", "Maybe I should try to beg in the streets instead of this 'job'...")
        else:
            if ct("Impersonal") or ct("Dandere") or ct("Kuudere") or ct("Shy"):
                $ rc("...I don't want to live.", "My life is awful. I want to end this...", "... <She looks extremely depressed>")
            else:
                $ rc("I wish that I the resolve to kill myself...", "My life in your service is awful.", "Just sell me off to someone. To anyone!")
        $ char.disposition += randint(0, 1)
        $ char.restore_portrait()
    elif char.disposition <= -50:
        $ char.override_portrait("portrait", "indifferent")
        if char.status != "slave":
            if char.joy >= 50:
                if ct("Impersonal") or ct("Dandere") or ct("Kuudere"):
                    $ rc("I don't like my job.", "You are a bad employer.")
                elif ct("Shy"):
                    $ rc("I-I'm fine. J-just wish I had a better job... No, nevermind.", "I'm fine, I think... I-I mean it's not such a bad job, there are much worse ones!")
                else:
                    $ rc("I'm fine, but I just wish you weren't such a terrible employer.", "As good as can be expected under the circumstances, 'boss'...")
            else:
                if ct("Impersonal") or ct("Dandere") or ct("Kuudere"):
                    $ rc("I hate my job.", "I'm not in the mood. Why? Because of my job, obviously.")
                elif ct("Shy"):
                    $ rc("I wish I had a better job... S-sorry.", "I-I don't particularly like my job. M-maybe I should try something else...")
                else:
                    $ rc("I'm sad and you are the worst... what else do you want me to say?", "I'm looking for new employment opportunities; that's how I'm feeling...")
        else:
            if char.joy >= 50:
                if ct("Impersonal") or ct("Dandere") or ct("Kuudere"):
                    $ rc("I suppose a slave like me doesn't have much of a choice.", "I follow your orders. That's all.")
                elif ct("Shy"):
                    $ rc("Um, I do my best. Even though my master is... Nevermind, sorry.", "M-master, please be nice to me... I'll work harder, I promise.")
                else:
                    $ rc("I am 'ok'. Just wish I had a better owner...", "I guess it is better than the slave market. A bit.")
            else:
                if ct("Impersonal") or ct("Dandere") or ct("Kuudere"):
                    $ rc("...I want another owner.", "I wish I had a better life as a slave.")
                elif ct("Shy"):
                    $ rc("...Yes, master. I'm fine. <you notice tears in her eyes>")
                else:
                    $ rc("There isn't much to say... I'm sad and you're mean...", "I feel like it would be better if you sold me off at the next auction.")
        $ char.disposition += randint(1, 2)
        $ char.joy += randint(0, 1)
        $ char.restore_portrait()
        if dice(round(hero.charisma*0.5)):
            $ narrator(choice(["She was much more approachable today."]))
            $ char.disposition += randint(1, 3)
            $ hero.exp += randint(1, 5)
            $ char.exp += randint(1, 5)
    else:
        $ char.override_portrait("portrait", "happy")
        if char.status != "slave":
            if char.joy >= 50:
                if ct("Impersonal") or ct("Dandere") or ct("Kuudere"):
                    $ rc("I like my job. Nothing more to say.", "No complaints.")
                elif ct("Shy"):
                    $ rc("I-I like my job. T-thank you.", "I-I'm perfectly fine! <shyly smiling>")
                else:
                    $ rc("I'm happy and this job is not so bad.", "I'm comfortable and content with this arrangement.")
            else:
                if ct("Impersonal") or ct("Dandere") or ct("Kuudere"):
                    $ rc("I like my job. I think.", "Not bad. It's not perfect, but...")
                elif ct("Shy"):
                    $ rc("I'm just a bit sad today, b-but my job is nice.", "Um, I'm ok, I think. You can't be happy all the time, r-right?")
                else:
                    $ rc("Not very chipper but I hope things become better soon.", "Bit sad, if truth be told. Don't want to complain though.")
        else:
            if char.joy >= 50:
                if ct("Impersonal") or ct("Dandere") or ct("Kuudere"):
                    $ rc("I'm satisfied with everything, master.", "I am at your service, master. My life is my job.")
                elif ct("Shy"):
                     $ rc("E-everything is well, master! <shyly smiling>", "It's fine. Thanks for asking, master. <blushes>")
                else:
                      $ rc("I'm very well, thank you Master!", "I am satisfied with my life and job as a slave.")
            else:
                if ct("Impersonal") or ct("Dandere") or ct("Kuudere"):
                    $ rc("Nothing to worry about, Master.", "Good enough.")
                elif ct("Shy"):
                    $ rc("Y-yes, Master. I can do it, I know I can!", "It's normal, I suppose...")
                else:
                    $ rc("I'm a bit sad, but Master is kind so I'm looking for a brighter tomorrow!", "You've been very nice to me in general, so I won't complain!")
        $ char.disposition += randint(1, 3)
        $ char.joy += randint(0, 1)
        if dice(round(hero.charisma*0.6)):
            $ narrator(choice(["You feel especially close today."]))
            $ char.disposition += randint(1, 4)
            $ hero.exp += randint(1, 5)
            $ char.exp += randint(1, 5)
        $ char.restore_portrait()
    jump girl_interactions

# ask how she feels
label interactions_howshefeels:
    "You asking how she feels today."
    $ m = interactions_flag_count_checker(char, "flag_interactions_howshefeels")
    if m >= randint(5, 6): # we don't have to limit it because of bonuses (there are none), but because of the common sense
        call interactions_too_many_lines
        $ char.disposition -= randint(0,m)
        $ del m
        jump girl_interactions
    $ del m
    if char.effects["Food Poisoning"]['active']: # at least no penalty to disposition, unlike other cases with food poisoning
        $ char.override_portrait("portrait", "sad")
        $ rc("I ate something wrong. Ow-ow-ow...", "Ouh. I think I need to use bathroom again...")
        $ char.restore_portrait()
        jump girl_interactions_end
    elif char.effects["Down with Cold"]['active'] or char.vitality < round(char.get_max("vitality")*0.3) or (char.health < round(char.get_max("health")*0.2)) or char.joy<25: # we select one suitable image in the very beginning
        $ char.override_portrait("portrait", "sad")
    elif char.joy>70:
        if ct("Shy"):
            $ char.override_portrait("portrait", "shy")
        else:
            $ char.override_portrait("portrait", "happy")
    else:
        if ct("Shy"):
            $ char.override_portrait("portrait", "shy")
        else:
            $ char.override_portrait("portrait", "indifferent")
            
    if char.effects["Down with Cold"]['active']: #illness
        $ rc("I think I caught a cold...", "I'm not feeling well today. *sneezes*", "I have a fever... <She looks pale>")
        
    #body checks
    if char.vitality <= round(char.get_max("vitality")*0.1):
        $ rc("I want to sleep so badly... <yawns>", "I'm very tired lately... <yawns>")
    elif char.vitality < round(char.get_max("vitality")*0.3):
        $ rc("My body a bit tired.", "I could use some rest.", "I feel weakness, I really should rest more...")
    elif char.vitality >= round(char.get_max("vitality")*0.9):
        $ rc("I'm full of strength and energy.", "My body rested very well lately.")

    if char.health <= round(char.get_max("health")*0.3):
        $ rc("My whole body hurts. I think I need a doctor.", "My body is not feeling very well lately... I could use some medical attention.")
    elif char.health >= round(char.get_max("health")*0.9) and not(char.effects["Food Poisoning"]['active']) and not(char.effects["Down with Cold"]['active']):
        $ rc("My body is in top condition.", "My health is pretty good lately.")
        
    if cgo("Caster"):
        if char.mp <= round(char.get_max("mp")*0.2):
            $ rc("I feel drained.", "My mind is tired. Perhaps I should use magic less frequently.")
        elif char.mp >= round(char.get_max("mp")*0.9):
            $ rc("I feel like magic overflows me.", "I'm filled with magic energy.")
            
    if char.joy <= 30: #begin joy checks
        if ct("Impersonal") or ct("Dandere"):
            $ rc("I'm not in the mood today.", "I'm just a bit sad. That's all.")
        elif ct("Shy"):
            $ rc("I'm kinda sad...", "I-I cried a bit some time ago. Why? Because I felt like it...")
        else:
            $ rc("I'm depressed. Don't wanna talk about it.", "I'm sad. Isn't it obvious to you?")
    elif char.joy >= 65:
        if ct("Impersonal") or ct("Dandere") or ct("Kuudere"):
            $ rc("I'm pretty happy. I think.", "I'm fine. <barely smiling>")
        elif ct("Shy"):
            $ rc("I think I'm... happy.", "<shyly smiling> I'm in a good mood today...")
        else:
            $ rc("I'm quite happy.", "You could say I enjoy my life.")
    else:
        if ct("Impersonal") or ct("Dandere") or ct("Kuudere"):
            $ rc("I'm perfectly calm.", "Don't concern yourself about me, I'm fine.")
        elif ct("Shy"):
            $ rc("Um, I suppose I'm ok.", "N-nothing to worry about, I'm f-fine.")
        else:
            $ rc("I'm ok, I guess.", "Everything is as usual.")
            
    $ char.restore_portrait()        
    jump girl_interactions

# ask about her
label interactions_abouther:
    "You trying to learn a bit about her."
    $ interactions_check_for_bad_stuff(char)
    $ interactions_check_for_minor_bad_stuff(char)
    $ m = interactions_flag_count_checker(char, "flag_interactions_abouther")
    if m > (randint(1,2) + round(interactions_set_repeating_lines_limit(char)*0.5)):
        call interactions_too_many_lines
        $ char.disposition -= randint(1,m)
        $ char.joy -= randint(0,2)
        $ del m
        jump girl_interactions
    $ del m
    if dice(char.disposition*0.5):
        if dice(randint(40,60)) and dice(hero.charisma*0.4) and dice(char.joy):
            if char.disposition >= 400:
                $ narrator(choice(["You feel especially close today."]))
                $ hero.exp += randint(4, 8)
                $ char.exp += randint(4, 8)
                $ char.joy += randint(0, 1)
                $ char.disposition += randint(1, 2)
            else:
                $ narrator(choice(["She was much more approachable today."]))
                $ hero.exp += randint(4, 8)
                $ char.exp += randint(4, 8)
                $ char.disposition += randint(3, 6)
        
        $ char.disposition += round(randint(6, 15) - (char.disposition * 0.005) + (char.joy * 0.02))
        $ hero.exp += randint(4, 8)
        $ char.exp += randint(4, 8)
        $ gm_abouther_list = []
        if ct("Half-Sister"):
            if ct("Yandere"):
                $gm_abouther_list.append(choice(["We used to play doctor and tear off each other's clothes, heh.", "We used to bathe together, so... you got to touch sister's body all over....", "Whenever we took a bath together, I used to wash your every nook and cranny. And I mean EVERY nook and cranny ♪"]))
            elif ct("Impersonal"):
                $gm_abouther_list.append(choice(["Do you remember how you used to pull pranks on me?", "I have always observed you. I know all there is to your character.", "I've known what kinds of sexual fetishes you have since a long time ago."]))
            elif ct("Tsundere"):
                $gm_abouther_list.append(choice(["We used to take a bath together back in the days, didn't we? Now...? B...but... hey! You know we shouldn't do that!", "Now that I think about it, I spent more time with you than Mom and Dad.", "You've always gone out of your way to protect your sister. I should thank you for that.", "I went overboard when I tried to discipline you back when we were little. To be honest, I'm sorry about that now.", "Remember that collection of dirty magazines you used to cherish? I was the one who threw them away. I am... still sorry about that."]))
            elif ct("Dandere"):
                $gm_abouther_list.append(choice(["We've been together since we were small... Have you had enough of it? Well, I'm still not tired of it yet.", "You've taught me all kinds of things since a long time ago... even perverted things.", "You used to play doctor with me all the time... You were so perverted, even back then."]))
            elif ct("Kuudere"):
                $gm_abouther_list.append(choice(["I used to be a crybaby? D-don't remind me of such things...", "M-my promise to marry you? T-there's no way I'd remember something like that!", "Getting engaged with my brother... I only thought that was possible back when we're kids.", "You always protected me. Therefore, I decided that I had to become strong."]))
            elif ct("Ane"):
                $gm_abouther_list.append(choice(["Hehe, you've grown so much... That makes your sis proud.", "You weren't able to fall asleep without sis by your side when we were little.", "Whenever I wore a skirt, you always tried to peek underneath it... You were already so perverted when we were little.", "I've taken care of you since you were little. Therefore, sister knows everything about you.", "When we were younger, I was always by your side because I swore I would always protect you."]))
            elif ct("Imouto"):
                $gm_abouther_list.append(choice(["I used to think I'd get as tall as you.", "You remember we used to play shop when we were little? Wha... You should forget about THAT game!", "You have protected me from bullies when I was little.... That made me so happy."]))
            elif ct("Kamidere"):
                $gm_abouther_list.append(choice(["I decided that you'd be mine when I was still very little.", "You've belonged to sis ever since you were born.", "You're my brother who I've personally helped to raise. There's no way I'd let you go."]))
            elif ct("Bokukko"):
                $gm_abouther_list.append(choice(["When we were little, didn't you say you'd make me your wife someday or something?", "When we were kids, we went exploring in the forest together and we both got lost.", "We used to climb fences and then jump off them. The two of us got injuries all over.", "You used to be so wee and now that huge, na?"]))
            else:
                $gm_abouther_list.append(choice(["We used to bathe together a lot when we were little ♪", "The bath used to be our playground... but you tickled me way too much.", "When it was night time, you would always try to slip into my bed unnoticed.", "You used to tag along with me wherever I went when we were little."]))
        
        if ct("Big Boobs", "Abnormally Large Boobs") and dice(80):
            $gm_abouther_list.append(choice(["I notice men, everyone of them, staring at nothing but my boobs.", "I've outgrown yet another bra... I wish something could be done about this...", "Hey, [hero.name], do you know what my charms are? Ufu, shall I show you? I'm pretty sure I can make your heart skip a beat ♪", "All the men just keep staring at my breasts. Are such big ones really that fascinating?", "The reason you're interested in me is my big breasts, right?", "They say that big breasts are the best, but truth be told they're heavy and make the shoulders stiff, not good at all."]))
        
        if ct("Small Boobs") and dice(80):
            $gm_abouther_list.append(choice(["I read lately that the hunt is on for small breasts. Who cares about big tits!", "It's better without large breasts. They'd only get in the way... Probably...", "Small breasts have their good points as well, don't you think? You do think so, right?"]))     
        
        if ct("Lesbian"):
            $gm_abouther_list.append(choice(["I am REALLY interested in female's bodycurves.", "I would like to go to an all girls' school. Imagine, only girls, everywhere... That would be great...", "I'd like to bring a cute girl home.", "Isn't it normal to be attracted to charming girls? I think it's totally proper ♪", "Something I like? Hmm... Maybe watching cute girls?", "Girls look really cute, don't they? I just want to eat one up.", "I like cute things. Like girls, for example.", "If I were a boy, I sure would explore every inch of the girl I was dating..."]))
        
        if ct("Bisexual"):
            $gm_abouther_list.append(choice(["In love, gender makes no difference...", "I like boys and girls alike ♫"]))
            
        if ct("Fire"):
            $gm_abouther_list.append(choice(["I'm pretty good with fire magic."]))
        if ct("Water"):
            $gm_abouther_list.append(choice(["I'm pretty good with water magic."]))
        if ct("Air"):
            $gm_abouther_list.append(choice(["I'm pretty good with air magic."]))
        if ct("Earth"):
            $gm_abouther_list.append(choice(["I'm pretty good with earth magic."]))
        if ct("Darkness"):
            $gm_abouther_list.append(choice(["I'm pretty good with dark magic."]))
        if ct("Light"):
            $gm_abouther_list.append(choice(["I'm pretty good with light magic."]))
        if ct("Electricity"):
            $gm_abouther_list.append(choice(["I'm pretty good with electricity magic."]))
        if ct("Ice"):
            $gm_abouther_list.append(choice(["I'm pretty good with ice magic."]))
        if ct("Neutral"):
            $gm_abouther_list.append(choice(["They say some people have no talent for magic. I'm one of them, it seems."]))
            
        if ct("Slim"):
            $gm_abouther_list.append(choice(["I have a great figure, don't you think?", "No matter how much I eat, I never get fat. I'm so lucky with my body ♫"]))
            
        if ct("Chubby"):
            $gm_abouther_list.append(choice(["I may be a bit chubby, but men like it.", "I thought about a diet, but I just can't resist fresh cupcakes ♫"]))
            
        if ct("Scars"):
            $gm_abouther_list.append(choice(["I tried many doctors, but they all said that my scars cannot be healed. *sigh*"]))
            
        if ct("Energetic"):
            $gm_abouther_list.append(choice(["I always was a good runner. I'm good at moving fast.", "I hate waiting, and I hate when people have to wait me."]))
            
        if ct("Optimist"):
            $gm_abouther_list.append(choice(["They say I'm always cheerful. I just enjoy my life, that's all.", "Hey, do you know this one? <tells you an anecdote> A good one, eh?"]))
            
        if ct("Pessimist"):
            $gm_abouther_list.append(choice(["It's not like I dislike jokes... I just don't find most of them funny enough.", "The world is cruel and unforgiving... You can't hide this truth behind jokes."]))
            
        if ct("Aggressive"):
            $gm_abouther_list.append(choice(["They say I'm too hot-headed. But it's not my fault when they try to pick a fight with me!", "I smacked that rude shopkeeper the other day right in the face. Will teach him a lesson how to talk with customers."]))
            
        if ct("Courageous"):
            $gm_abouther_list.append(choice(["Some my friends afraid of darkness, can you imagine that? Even as a child I was not afraid of it, or anything else.", "Don't move, you have a spider on your shoulder. <calmly removes it> Here."]))

        if ct("Coward"):
            $gm_abouther_list.append(choice(["The other day I noticed a bug under my bed. I had to spend the night at a neighbor... <shudders>", "I dislike dark places. And night. Why? Because... because it's so dark that I cannot see a thing!"]))
            
        if ct("Nerd"):
            $gm_abouther_list.append(choice(["As a child I liked to to read books more than to play with peers, so they teased me a lot. Nothing changed since then..."]))
            
        if ct("Strange Eyes"):
            $gm_abouther_list.append(choice(["People often say that my eyes are unusual. What do you think of them?", "Do you like my eyes? As a child I was often teased because of them."]))
            
        if ct("Manly"):
            $gm_abouther_list.append(choice(["Do you like my muscles? It took a while to build them.", "Every girl should build herself some muscles for self-protection, don't you think?"]))
            
        if ct("Lolita"):
            $gm_abouther_list.append(choice(["My body is so small, everyone think I'm still a child.", "Maybe I should drink more milk to grow up... What do you think?"]))
            
        if ct("Alien"):
            $gm_abouther_list.append(choice(["This place is so strange. I don't think I'll ever get used to it completely.", "Everything was very different where I used to live. But... I like it here too."]))
            
        if ct("Great Arse"):
            $gm_abouther_list.append(choice(["I notice men often staring at my ass. What's wrong with them?", "The other day I dropped my purse and bent down to pick it up. All the men in the street started to applaud me. It was sooo embarrassing!"]))
            
        if ct("Not Human"):
            $gm_abouther_list.append(choice(["Some humans don't like my appearance. But I don't care.", "The other day they refused to serve me in that fancy cafe because I'm not human enough. Can you imagine that?!"]))
            
        if cgo("Warrior"):
            if ct("Shy") or ct("Coward"):
                $gm_abouther_list.append(choice(["I have been trained in combat, but I really dislike violence.", "I know a lot about self-defense... but I really hope that I wouldn’t ever need to use it.", "I know how to use a weapon... but it still scares me a bit.", "I can do well in combat training, but in practice...", "They say that I may have the skill, but not the spirit of a warrior...", "I carry a weapon, but I don’t think I would have the heart to hurt someone."]))
            elif ct("Virtuous"): 
                $gm_abouther_list.append(choice(["I know how to pacify someone without hurting them. That’s the right way to do it.", "I learned how to fight so I can protect others."]))
            elif ct("Adventurer"): 
                $gm_abouther_list.append(choice(["I like to sharpen my battle skills.", "I enjoy exploring catacombs.", "A duel sounds interesting, do you mind?"]))
            else:
                $gm_abouther_list.append(choice(["I have been trained in combat. So you better not be trying anything funny <grins>", "I may not look like it, but I can handle my weapons really well.", "Some creeps tried to ambush me once. I gave them plenty of time to repent at the infirmary.", "Sometimes I watch the matches in the arena to get inspiration to improve my own technique.", "It's better to know how to defend yourself in this town. You never know what may happen, especially if you are a woman."]))

        if ct("Homebody"):
            $gm_abouther_list.append(choice(["I like my home a lot. I don't understand all those travellers and adventurers.", "I think living every day as an ordinary girl is the ultimate happiness.", "I enjoy reading in the bath. It's nice to do in such a confined space."]))
            
        if ct("Natural Follower"):
            $gm_abouther_list.append(choice(["I'm not a leader, I never wanted to be one. Too much responsibility."]))
            
        if ct("Natural Leader"):
            $gm_abouther_list.append(choice(["People say I'm quite charismatic. I bet I'd be a good leader, don't you thing? <smiles>"]))
            
        if ct("Well-mannered"):
            $gm_abouther_list.append(choice(["They say nothing costs so little and is valued so much as courtesy. I always keep that in mind."]))
            
        if ct("Ill-mannered"):
            $gm_abouther_list.append(choice(["People often tell me that I lack politeness. Fucking hypocrites! I just say what I really think, nothing more."]))
            
        if ct("Half-Sister"):
            $gm_abouther_list.append(choice(["Do you miss our father? ...Yes, I miss him too.", "We should chat more often. We are family after all."])) 
            
        if not(cgo("Warrior")) and ct("Adventurer"):
            $gm_abouther_list.append(choice(["I always dreamed about my own adventures. But I never had a combat training, so... <sigh>"]))
            
        if cgo("Caster"):
            $gm_abouther_list.append(choice(["I like to study magic.", "Arcane arts are passion of mine", "Magic is so fascinating, I can't live without it!"]))
            
        if cgo("Server"):
            $gm_abouther_list.append(choice(["I'm just an ordinary worker, I guess.", "I work where I can. You can't be picky if you want to pay your bills."]))
            
        if cgo("SIW"):
            $gm_abouther_list.append(choice(["I enjoy sex, thus I enjoy my job <grins>", "I think there is nothing wrong with selling your body as long as you having fun and it's well paid."]))
            
        if ct("Dawdler"):
            $gm_abouther_list.append(choice(["Hey, have you heard the saying, “Good things come to those who sleep?” ... Uh, and wait?", "I always get sleepy after a meal... It's just natural providence.", "Fuwa... This season sure makes me sleepy...", "No matter how much I sleep I can't get enough of it....", "*Yawn* You know lack of sleep is damaging to the skin.", "There are days when I just don't feel like doing anything... a lot of them, actually."]))
                       
        if ct("Frigid"):
            $gm_abouther_list.append(choice(["Why does everyone get so excited about underwear? It's just fabric...", "Relations should be clean and wholesome, an example to others."]))
        
        if ct("Exhibitionist"):
            $gm_abouther_list.append(choice(["Have you ever thought of doing it in public? Just imagine all those eyes...", "It would be a waste not to show some skin when the weather is nice.", "It arouses me when strangers are staring... Stripping me with their eyes..."]))
        
        if ct("Clumsy"):
            $gm_abouther_list.append(choice(["It's common place to spill all the contents when opening a bag of candy, isn't it?", "I broke another plate. How many has it been now..? I wish I could do something about this."]))
        
        if ct("Sexy Air"):
            $gm_abouther_list.append(choice(["Everyone keeps saying that the way I lick my lips is incredibly erotic.", "I like to use my tongue to play around with candy in my mouth. Don't you?", "Aah, I wanna eat something sour..."]))
        
        if ct("Nymphomaniac"):
            $gm_abouther_list.append(choice(["No matter how much I do it, I still can't cool down. Hehe, what do you *think* I'm talking about?", "I've been having these unintentional s... sexual urges lately....", "My body gets horny all on its on even when I'm by myself... It's so frustrating!", "I can become horny just like that all of a sudden... And before I even realize, I'm already..."]))
        
        if ct("Virtuous"):
            $gm_abouther_list.append(choice(["It would be great if people would be nicer to each other...", "I did some volunteer work the other day, it was a pleasant experience.", "It really pains me when I see someone suffering.", "It’s the most elevating feeling when you can help someone, isn’t it?"]))

        if ct("Vicious"):
            $gm_abouther_list.append(choice(["Those disgusting beggars... If you want money, go and earn them! What's the problem?", "The other day a man tried to steal my purse. He won't bother anyone anymore. <ominously grins>"]))

        if ct("Sadist"):
            $gm_abouther_list.append(choice(["I want to violate a guy with a strap-on. You game?", "It makes me so wet when my lover gets a scared look on his face.", "Huhu, discipline is lovely, isn't it..."]))
        
        if ct("Psychic"):
            $gm_abouther_list.append(choice(["Just small gestures and facial expressions can reveal even the most ulterior motives.", "I can tell a lot about your personality just from your posture.", "It's not difficult for me to guess what people will do, if I'm able to observe them for a while.", "While it's hard to tell the motives of some, the majority of people are so predictable...", "It's hard to predict the movements of a warrior. They are trained to hide their thoughts.", "You... have a shadow of death hanging over you... No, it's nothing. Nevermind that.", "A spell has been cast... Long ago... But it's still here... Hm? Did I just... said something?"]))
        
        if ct("Serious"):
            $gm_abouther_list.append(choice(["Only with a clear mind can you be truly effective. Emotions just get in the way.", "Nothing good can come from being too emotional.", "If a problem has a solution, there's no reason to be worried. And if it doesn't... then there's no reason to be worried either.", "Anger or tears cannot solve anything."]))
        
        if ct("Masochist"):
            $gm_abouther_list.append(choice(["I don't hate the pain. Because...it can feel good in its own way...", "Tied up and blindfolded... Isn't it exciting?", "Being mistreated a little... can be fun....", "No, I don't like pain. Even so, sometimes chains are... oh no, what am I saying?!", "If you tied me up... the experience... Both my body and soul... Oh no, what am I saying..."]))
        
        if ct("Athletic"):
            $gm_abouther_list.append(choice(["I may look slow, but I'm actually really good at sports.", "I think it's important to keep yourself in good shape.", "Want to race? I won't lose.", "I went exercising and ran up quite a sweat. It's a good feeling."]))
        
        if ct("Artificial Body"):
            $gm_abouther_list.append(choice(["Do I actually appear human to you? Oh nothing, nevermind that.", "I can keep going even without much sleep. Isn't that great?", "I've been having these weird dreams where I'm me, yet, I'm not me.... I wonder what this could be about...."]))
        
        if ct("Neat"):
            $gm_abouther_list.append(choice(["It's a good day for doing laundry.", "When you don't diligently clean wet areas of the house you can get an outbreak of mold and various bacteria.", "For some reason, the dust on the windowsill really bothers me.", "Most people don't like them, but chores are an important job, too.", "You can make any place clean and cozy with thorough work.", "Chores take much less time when properly organized.", "Pleasant service is the foundation of any successful business. Nothing can drive off customers faster than rudeness.", "Cleanliness is next to godliness. Don't you agree?"]))
            
        if ct("Messy"):
            $gm_abouther_list.append(choice(["It's fine to skip a bath if you don't reek of sweat.", "Do you think I'm sweaty? Some perv in the alley told me he likes sweaty ones. Yuicks.", "My room might look like it's in a mess, but I always know where to find anything there."]))
       
        if ct("Heavy Drinker"):
            $gm_abouther_list.append(choice(["You wanna have a drinking contest? Hehe, I won't lose to you.", "I say, there's always a reason to drink."]))
        
        if ct("Curious"):
            $gm_abouther_list.append(choice(["Experiencing new things is loads of fun, isn't it?", "The truth always comes up at the very end... No, it's nothing.", "Huh? Hey, I found some more money... Oh wait, it's just a shiny rock.", "Want to see the shells I picked up at the beach?", "I spent a long time chasing a really cute cat I saw.", "In order to keep up with the latest fads, intelligence gathering is essential.", "Strolling through town is a nice change of pace."]))
        
        if ct("Shy"):
            $gm_abouther_list.append(choice(["It would be good... if I could just be a bit more confident... I think...", "I'm no good with public speaking...", "I don't like being competitive...", "Umm, I'm... not really good with standing out...", "I don't like making eye contact...", "...Appearing in front of people... I'm reluctant...", "I'm not fond of... talking to people..."]))
            
        if ct("Elf"):
            $gm_abouther_list.append(choice(["Gardening is so much fun, you know?", "Sometimes I feed forest animals next to the city."]))

        if ct("Always Hungry"):
            $gm_abouther_list.append(choice(["I'm still hungry, no matter how much I eat.", "I can eat nonstop, is there something wrong with that?", "No matter how much I devour, my stomach is still empty. Am I still growing or something?", "You'll get heat fatigue if you don't eat properly.", "I wonder why I'm always so hungry. I'm not gaining much weight, so it's fine, but...", "I really do eat too much but I still manage to keep in shape, so....", "I've got a craving for sweets just now...", "I've had a huge appetite lately. If this continues then I might gain weight... This has to stop."]))
        
        # if there is not enough specific answers, a vague one is added to the list
        if len(gm_abouther_list) < 3:
            $gm_abouther_list.append(choice(["Hm? A little of this, a little of that?", "...I don't really have much to say.", "Nothing much, there's nothing worth mentioning.", "What I'm doing? The usual stuff...", "I'm just normal, I guess.", "I like just about anything.", "Hmm, there's not much to talk about.", "Now that I think about it... am I just boring?", "I'm just about average, I guess."]))
    
    else:
        $ char.disposition -= randint(0, 1)
        $ char.joy -= randint(0,1)
        jump interactions_refused
    
    $ g(choice(gm_abouther_list))
    $ gm_abouther_list = None
    jump girl_interactions

# ask about occupation
label interactions_aboutoccupation:
    "You asking about her occupation."
    $ interactions_check_for_bad_stuff(char)
    $ m = interactions_flag_count_checker(char, "flag_interactions_aboutoccupation")
    if m > randint(2,3):
        call interactions_too_many_lines
        $ char.disposition -= randint(1,m)
        $ del m
        jump girl_interactions
    $ del m
    $ hero.exp += randint(1, 2)
    if char.disposition > -250:
        if cgo("Warrior") and not(cgo("Caster")):
            $rc("I was trained to fight.", "I have combat training.", "I know how to fight.", "I know how to behave on the battlefield.")
            if co("Defender"):
                $rc("I'm more like a bodyguard.", "In battle I was taught to protect others.", "My job is to hold the enemy.")
            if co("Shooter"):
                $rc("I prefer to keep the enemy at a distance.", "I prefer to use ranged weapons.", "I'm a pretty good marksman.")
            if co("Assassin"):
                $rc("I was taught the art of stealthy assassination.", "I'm an assassin. They never see me coming.", "I have had training to kill at any cost. So my methods are... concealed.")
        if cgo("Caster"):
            $rc("I'm a magician.", "I have arcane energies at my command.", "I have a magical talent. It's very useful in many cases.")
            if co("Battle Mage"):
                $rc("I prefer battle magic, myself.", "I have plenty experience in combat magic.", "And I know how to effectively use my gift on the battlefield.")
            if co("Healer"):
                $rc("I know a lot about healing magic.", "My job is to heal wounds.", "I'm a healer, my magic helps other people.")
        if cgo("SIW"):
            $rc("I'm a fancy girl.", "I'm a merchant. And my merchandise is my beautiful body ♪", "I provide personal services. I mean very personal.", "I sell my love to those who need it.")
            if co("Anal Prostitute"):
                $rc("Anal sex is my strong point.", "I love it in my poop chute.", "I've got an onion booty, it makes men cry. Haha.")
            if co("Oral Prostitute"):
                $rc("Oral sex is my strong point.", "I'll give head until I'm dead.", "I can suck a golf ball through a garden hose.")
            if co("Straight Prostitute"):
                $rc("Vaginal sex is my strong point.", "My pussy's made of gold.", "I can milk a cock with my vaginal muscles alone.")
            if co("Mistress"):
                $rc("I prefer S&M, myself. Wanna try sometime? ♪", "Lick my boots worm!.", "I wanna tie you up and make you my bitch.")
            if co("Stripper"):
                $rc("I specialize in erotic dances.", "I'm undressing on stage, if you know what I mean.")
        if cgo("Server") and not(co("Stripper")):
            $rc("I specialize in service industry.", "I'm a service girl.")
            if co("Entertainer"):
                $rc("I entertain the public.", "I don't allow customers to get bored.")
            if co("Dancer"):
                $rc("I specialize in art of dancing.", "I'm a pretty good dancer.")
            if co("Maid"):
                $rc("I perform menial tasks around the household.", "And I'm a professional maid.")
            if co("Cleaner"):
                $rc("I specialize in cleaning.", "I'm especially good in cleaning.")
            if co("Waitress"):
                $rc("I have some experience in serving customers in a restaurant.", "I think I'm a pretty good waitress.")
            if co("Bartender"):
                $rc("Also I know how to serve customers behind the bar.", "I'm a bartender. It's a rare profession, I know.")
        if co("Manager"):
            $rc("I know a thing or two about managing.", "I know how to manage people.")
        if not(cgo("Server") or cgo("SIW") or cgo("Warrior") or cgo("Caster") or co("Manager")): #you never know
            $rc("I don't really have a profession...")
    else:
        $ char.disposition -= randint(0, 1)
        jump interactions_refused
    jump girl_interactions

label interactions_interests:
    "You asking about her interests."
    $ interactions_check_for_bad_stuff(char)
    $ interactions_check_for_minor_bad_stuff(char)
    $ m = interactions_flag_count_checker(char, "flag_interactions_interests")
    if m > (randint(2,3) + round(interactions_set_repeating_lines_limit(char)*0.5)):
        call interactions_too_many_lines
        $ char.disposition -= randint(1,m)
        $ char.joy -= randint(0,2)
        $ del m
        jump girl_interactions
    $ del m
    if not(dice(char.disposition*0.5)):
        $ char.disposition -= randint(0,3)
        $ char.joy -= randint(0,1)
        jump interactions_refused
    else:
        $ line = rts(char, {
        "Exhibitionist": ["She tells you pretty hot stories about her exhibitionistic adventures in a local park."],
        "Athletic": ["You discuss beach volleyball which became quite popular among local girls lately.", "You discuss places for swimming. Looks like most girls prefer beaches to pools because it's free."],
        "Manly": ["She gives you a lecture on how to build your muscles properly. You feel a bit offended, but keep your cool.", "She casually remarks that you should exercise more often, and gives you some advice."],
        "Chubby": ["You have a lively discussion about your favorite local bakeries and pastry shops.", "Your conversation turns toward cooking, and she shares some of her recipes. They are all pretty high in calories..."],
        "Slim": ["You compliment her figure, and the conversation quickly turns toward healthy lifestyle. Ugh.", "She brags about her metabolism, allowing her to eat sweets and not get fat. You envy her."],
        "Alien": ["She talks about her homeland. You are listening with interest.", "You discuss local events she witnessed. She doesn't understand the meaning of some of them, and you spend some of your time to explain."],
        "Half-Sister": ["You discuss your common father. The sad discussion quickly turns into a sarcastic one, when you try to count all his lovers and daughters.", "She tells you about her mother. You listen in silence, trying to imagine yours.", "You spend time together you reminiscing about fun and embarrassing moments from your childhood."],
        "Scars": ["She complains about how her scars cause inconvenience. You comfort her."], 
        "Artificial Body": ["Tempted by curiosity, you ask about her artificial body. Her explanations are very long and confusing.", "You discuss the regular maintenance required by her body. It's a pretty complex, but piquant conversation."],
        "Lolita": ["She complains about how hard it is to find adult clothes for her figure. You're trying to take her away from this sensitive topic.", "She tells you funny stories about disappointed (and imprisoned) paedophiles confused by her body size. What a strange topic."], 
        "Strange Eyes": ["She notices how you look at her unusual eyes. Embarrassed, she refuses to look at you or discuss anything."], 
        "Great Arse": ["You try to keep it to small talk, trying not to think about her gorgeous butt and what would you do if you were behind her."], 
        "Long Legs": ["During your small conversation you can't help but glance at her long legs. Looks like she is used to it and doesn't care much."], 
        "Abnormally Large Boobs": ["You vaguely remember your conversation, paying most of your attention to her amazing chest.", "She complains about high costs for the purchase of new bra. It appears that the fabric is not strong enough to withstand such loads. Without knowing what reaction she expected, you keep your poker face."], 
        "Big Boobs": ["She complains how a big chest spoils the posture. You sympathize with her, very convincingly and almost sincerely."], 
        "Small Boobs": ["She starts a conversation about irrelevance of chest size. You carefully assent, trying to not piss her off."], 
        "Fire": ["Your conversation turns to magic, and she enthusiastically tells you the intricacies of dealing with the power of fire."], 
        "Water": ["Your conversation turns to magic, and she enthusiastically tells you the intricacies of dealing with the power of water."], 
        "Air": ["Your conversation turns to magic, and she enthusiastically tells you the intricacies of dealing with the power of air."], 
        "Earth": ["Your conversation turns to magic, and she enthusiastically tells you the intricacies of dealing with the power of earth."], 
        "Ice": ["Your conversation turns to magic, and she enthusiastically tells you the intricacies of dealing with the power of ice."], 
        "Electricity": ["Your conversation turns to magic, and she enthusiastically tells you the intricacies of dealing with the power of electricity."], 
        "Light": ["Your conversation turns to magic, and she enthusiastically tells you the intricacies of dealing with the power of light."], 
        "Darkness": ["Your conversation turns to magic, and she enthusiastically tells you the intricacies of dealing with the power of darkness."], 
        "Nerd": ["You discuss new books in local stores and libraries.", "Somehow your conversation comes to board games, and she enthusiastically explains to you the intricate rules of one of them."], 
        "Psychic": ["It's difficult to participate in the conversation when your interlocutor knows your words in advance. She seems to enjoy teasing you, however.", "She complains about headaches, dizziness and other neural disorders that are common for psychics."],
        "Optimist": ["Looks like she is in a good mood. Laughing and joking during your conversation, she quickly turns it into a humorous one.", "You exchange your freshest anecdotes."],
        "Pessimist": ["Looks like she's not in the mood. Your conversation is pretty gloomy, though you managed to cheer her up a bit."],
        "Serious": ["You have a very serious conversation about local politics and taxes. You feel squeezed like a lemon.", "She gives you a lecture about the importance of planning for the future. You heroically hold back a yawn."],
        "Extremely Jealous": ["She inquires about your relationships with other girls. You carefully dispel her concern, trying not to make definitive statements."],
        "Virtuous": ["She tells about her volunteer work. It's nice, but a bit boring."], 
        "Vicious": ["She gossips with obvious pleasure about her acquaintance's misfortunes."], 
        "Dawdler": ["You have a lazy, indolent discussion. Looks like she's half asleep.", "She pensively tells you about her recent dreams. You begin to feel drowsy."],
        "Clumsy": ["You talk about misfortunes caused by her clumsiness. You heroically hold back a smile and comfort her instead."],
        "Nymphomaniac": ["An innocent conversation turns into the discussion about sexual positions. She's really into this stuff.", "She passionately talks about her recent sexual adventures. Wow."], 
        "Heavy Drinker": ["You discuss various types of alcohol, sharing your drinking experience."],
        "Always Hungry": ["You talk about food for some time. Looks like she can do it for hours, so you carefully interrupt the conversation."],
        "Curious": ["You exchange the latest news and gossip. She really knows a lot about it."],
        "cgo('Warrior')": ["You discuss the recent fights at the arena and their participants.", "You discuss a variety of fighting styles."], 
        "cgo('Caster')": ["She enthusiastically talks about mysteries of arcane arts.", "You discuss her magical studies."], 
        "cgo('SIW')": ["You gossip about the strangeness of some of her customers."], 
        "cgo('Server')": ["She recounts rumors that she heard from customers lately. People tend to not notice service workers when they are not needed."], 
        "default": ["You chat for some time."]
        })
        
        "[line]"
        $ del line
        $ hero.exp += randint(4, 8)
        $ char.exp += randint(4, 8)
        $ char.disposition += round(randint(6, 11) - (char.disposition * 0.005) + (char.joy * 0.03))
        
        if char.joy >= 65:
            if dice(char.joy):
                "You had a very lively and enjoyable conversation."
                $ char.joy += randint(3, 4)
            else:
                "You had a pretty lively conversation."
                $ char.joy += randint(2, 3)
        elif char.joy >= 30:
            if dice(char.joy + 30):
                "You had a fairly normal conversation."
                $ char.joy += randint(1, 2)
            else: 
                "You had a short conversation."
        else:
            "It was a short and not very pleasant conversation."
        jump girl_interactions
###### j5           Until we actually will have real, existing places where they hang out, better to not use this stuff
#label interactions_hangouts:
#    if char.disposition < 200:
#        jump interactions_refused
#    
#    else:
#        if ct("Nymphomaniac") and dice(40):
#            $rc("Wherever there is something or someone I can shag.", "At the sex-club, oh no--I've said too much...#1 rule...Never talk about the sex club! WTF was I thinking?")
#        elif ct("Nerd"):
#            $rc("Library, where do {color=[red]}you{/color} go for fun?", "I cozy under a tree with a good book.")
#        elif cgo("Warrior"):
#            $rc("The Arena, where else?", "Window shopping at the blacksmith's!")
#        elif cgo("SIW"):
#            $rc("Wherever men with full pockets are hanging.", 'Us "Fancy Girls" usually hang around in the Red Light District', "Building...Don't look at me like that!")
#        elif ct("Dancer"):
#            $rc("Exotic Dancing academy", "Close to a pole and not any of the two you're thinking.", "Strip Club.")
#        elif cgo("Server"):
#            $rc("At the bar, tending to it.", "I love broom and dustbins exhibits.", "Wherever cleaning is required.")
#    
#    jump girl_interactions

# ask about love
label interactions_romance:
    "You ask her about love and romantic stuff."
    $ interactions_check_for_bad_stuff(char)
    $ interactions_check_for_minor_bad_stuff(char)
    $ m = interactions_flag_count_checker(char, "flag_interactions_romance")
    if m > (randint(2,3) + round(interactions_set_repeating_lines_limit(char)*0.5)):
        call interactions_too_many_lines
        $ char.disposition -= randint(1, m)+randint(1,4)
        $ char.joy -= randint(2,4)
        $ del m
        jump girl_interactions
    $ del m
    if not(dice(char.disposition * 0.35)):
        $ char.disposition -= randint(5, 10)
        jump interactions_refused
    else:
        $ char.override_portrait("portrait", "shy")
        if dice(randint(40,60)) and dice(hero.charisma*0.3) and dice(char.joy):
            if char.disposition >= 600:
                    $ narrator(choice(["You feel especially close today."]))
                    $ hero.exp += randint(5, 10)
                    $ char.exp += randint(5, 10)
                    $ char.joy += randint(0, 1)
                    $ char.disposition += randint(4, 6)
            else:
                $ narrator(choice(["She was much more approachable today."]))
                $ hero.exp += randint(5, 10)
                $ char.exp += randint(5, 10)
                $ char.disposition += randint(5, 10)
        $ hero.exp += randint(5, 15)
        $ char.exp += randint(5, 15)
        $ char.disposition += round(randint(11, 20) - (char.disposition * 0.01) + (char.joy * 0.05))
        if ct("Impersonal"):
            $rc("To express it in words is very difficult...", "Infatuation and love are different. Infatuation will fade, but love's memory continues forever.", "I think it is a good thing to be loved by someone.")
        elif ct("Shy") and dice(40):
            $rc("Lovers... Th-they're supposed to...hold hands, after all... Right?", "Wh-what comes after a k-kiss is... It's... Awawa...", "If it's the person you love, just having them turn around and smile... Is enough to make you happy...", "Love... sure is a good thing...")
        elif ct("Nymphomaniac") and dice(40):
            $rc("*sigh* I always have such a high libido...", "Um... Love can start from lust... right?", "If you are in love, having sex is totally normal, right?", "People are no more than animals, so it's only natural to copulate...right?", "Well, doing perverted stuff is proof that you're healthy.", "Me thinking about sex? Not at all... Great. Now that you brought it up...")
        elif ct("Bisexual", "Lesbian") and dice(20):
            $rc("Love runs deeper than gender.")
        elif ct("Dandere"):
            $rc("If you like them, you like them. If you hate them, you hate them. That's all there is to it. Right?", "My dream yesterday... It was so lovey-dovey and erotic.", "Getting close to people other than the one you love is kind of...", "You can still live a good life without a lover, don't you think?")
        elif ct("Tsundere"):
            $rc("M...men and women feel arousal differently.... F-f-forget what I just said!", "Thick and hard? What the... You idiot, what are you saying! That's not what you meant? ... You idiot!", "E-even I want to be a good bride someday, you know...?", "Things like l-love or affection, are all excuses.")
        elif ct("Kuudere"):
            $rc("To feel the same feelings towards each other... To be partners for life... That's what I long for.", "Two people in love devoting themselves to each other, that sounds like pure bliss to me...", "True love isn't about showing off to everyone else... It's the small things you do for your partner that matter.", "There's gotta be someone willing to support me out there somewhere...", "Chance encounters only happen with both time and luck... Well, I suppose you could call it fate.")
        elif ct("Imouto"):
            $rc("That's weird... Today's love fortune was supposed to be a sure thing... Hmm...", "That book is very interesting... A boy and a girl who you'd think are twins get together, but in fact...", "L-love and affection and th-that stuff, I don't really get it very well...", "If I'm going to date someone, they should be rich ♪, and want kids ♪ And they should be totally committed to me ♪")
        elif ct("Ane"):
            $rc("You're deciding who will be your partner for life.　It would be strange not to be worried about it.", "I think just having the one you love beside you is the ultimate happiness.", "I need a person whom I can rely on.", "Lost loves are important to build character, I think.", "As you've probably noticed, I'm the devoted type ♪", "Of course, I'd wanna stay by my loved one's side. Or, rather than being by their side, it's more, like, I want to support them?")
        elif ct("Kamidere"):
            $rc("Seriously, how can I... think of such unpleasant thoughts...", "When my body gets hot, it's like my discipline starts to crumble...", "There are things more important than physical infatuation.", "Making men my playthings is a simple matter for one such as I. Eheh!", "Love is nothing but an expression of ego, you know.", "You can't disobey your instincts. Isn't keeping up this charade painful for you?")
        elif ct("Bokukko"):
            $rc("Love is a competition! A conflict! A war!", "If the other person won't give you a second glance, you need to make 'em. It's simple, really.", "Love, hmm ♪ ... Hn, just thinking about it makes me sort of embarrassed...", "I'm gonna be the bestest wife!", "Is this that fate thing they're talking about?")
        elif ct("Yandere"):
            $rc("Huhu, a girl in love is invincible ♪", "Nothing motivates you quite like 'love', huh...", "If it's just with their mouth, everyone can talk about love. Even though none of them know how hard it is in reality...")
        else:
            $rc("Getting your heart broken is scary, but everything going too well is kinda scary for its own reasons too.", "One day, I want to be carried like a princess by the one I love ♪...", "Hehe! Love conquers all!", "I'm the type to stick to the one I love.", "Being next to someone who makes you feel safe, that must be happiness...", "Everyone wants to fall in love, I suppose. Don't you think?")
        $ char.restore_portrait()
        jump girl_interactions

# interaction check fail
label interactions_refused:
    $ char.override_portrait("portrait", "indifferent")
    if ct("Impersonal"):
        $rc("Denied.", "It's none of your business.", "...")
    elif ct("Shy") and dice(50):
        $ char.override_portrait("portrait", "shy")
        $rc("I-I won't tell you... ", "It's nothing. ...sorry.", "I don't want to talk... sorry.", "W-Well... I d-don't want to tell you...", "Ah, ugh... Do I have to tell you...?")
    elif ct("Dandere"):
        $rc("I don't feel the need to answer that question.", "...Let's talk later...maybe.", "I'm not going to tell you.")
    elif ct("Kuudere"):
        $rc("I've got no reason to tell you.", "I'm not in the mood for that right now.", "Why do I have to tell you?")
    elif ct("Tsundere"):
        $rc("Hmph! Who would tell you!", "Eh? You expect me to tell you?", "It's none of your business.")
    elif ct("Imouto"):
        $rc("Uhuhu♪ I won't tell you ♪ ", "It's a secret!", "Umm, is it bad if I don't answer...?")
    elif ct("Yandere"):
        $rc("I'm not in a mood for chatting.",  "<She is not listening>", "You talk too much.")
    elif ct("Kamidere"):
        $rc("And what will hearing that do for you?", "And what good would knowing that do you?")
    elif ct("Ane"):
        $rc("...I don't feel like answering.", "Sorry, can we talk later?", "Sorry, but I don't want to answer.", "*sigh*... Don't you have anything else to do?")
    elif ct("Bokukko"):
        $rc("Eh, say what?", "Why do I hafta give you an answer?", "I'm not gonna answer that.")
    else:
        $rc("I don't want to answer.", "I don't want to talk now.", "Hmph, Why should I have to tell you?", "Must I give you an answer?")
    $ char.restore_portrait()
    jump girl_interactions
    

# changing occupation
label interactions_occupation:
    # TODO: Remove this from the game completely??? Dark: yeap, it's too easy to do it via small talk
    menu:
        "Ask her to switch to:"
        "Prostitute" if char.occupation != "Prostitute":
            if char.status == "slave" and char.disposition > -500:
                g "As you wish Master..."
                if char.occupation != "Stripper" and char.disposition < 200:
                    "She doesn't look too happy about this..."
                    python:
                        char.joy -= 40
                        char.disposition -= 50
                        char.occupation = "Prostitute"
                else:
                    $ char.occupation = "Prostitute"
                    
            elif char.status == "slave":
                g "Never, not for you!"
                "She seems rather cross with you..."
                
            else:
                # Case free girl:
                if char.disposition < 950 + char.level:
                    $ rc("Don't even think of me in that way!", "Nope!", "I refuse")
                else:
                    g "Well... why not, I am willing to try new things..."
                    $ char.occupation = "Prostitute"
                
        "Stripper" if char.occupation != "Stripper":
            if char.status == "slave" and char.disposition > -500:
                g "As you wish Master..."
                if char.occupation != "Prostitute" and char.disposition < 200:
                    "She doesn't look too happy about this..."
                    python:
                        char.joy -= 40
                        char.disposition -= 50
                        char.occupation = "Stripper"
                else:
                    $ char.occupation = "Stripper"
                    
            elif char.status == "slave":
                g "Never, not for you!"
                "She seems rather cross with you..."
                
            else:
                # Case free girl:
                if char.disposition < 950 + char.level:
                    $ rc("Don't even think of me in that way!", "Nope!", "I refuse")
                else:
                    g "Well... why not, I am willing to try new things..."
                    $ char.occupation = "Stripper"
                
        "ServiceGirl" if char.occupation != "ServiceGirl":
            if char.status == "slave" and char.disposition > -500:
                g "As you wish Master..."
                $ char.occupation = "ServiceGirl"
                    
            elif char.status == "slave":
                g "Never, not for you!"
                "She seems rather cross with you..."
                
            else:
                # Case free girl:
                if char.disposition < 950 + char.level:
                    $ rc("Don't even thing of me in that way!", "Nope!", "I refuse")
                else:
                    g "Well... why not, I am willing to try new things..."
                    $ char.occupation = "ServiceGirl"
                
        "Warrior" if char.occupation != "Warrior" and char.status != "slave" and char.has_image("battle_sprite"):
                # Case free girl:
                if char.disposition < 950 + char.level:
                    $ rc("Don't even think of me in that way!", "Nope!", "I refuse")
                else:
                    g "Well... why not, I am willing to try new things..."
                    $ char.occupation = "Warrior"
                    
        "Just kidding":
            python:
                char.AP += 1
                hero.AP += 1
    
    jump girl_interactions
# testing stuff
label interactions_disp:
    $ char.disposition += 250
    jump girl_interactions
    
label interactions_becomefr:
    $ char.disposition += 500
    $ set_friends(hero, char)
    jump girl_interactions
    
label interactions_becomelv:
    $ char.disposition += 500
    $ set_lovers(hero, char)
    jump girl_interactions