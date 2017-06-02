###### j0
# quick navigation, search "j" + number, example: j0 - this panel
# 
#  1 - training - disobey
#  2 - training - stop
#  3 - training - runaway
#  4 - training - girl ap
#  5 - training - hero ap
#  6 - training - no gold
#  7 - reward - praise
#  8 - reward - treat
#  9 - reward - pleasure
# 10 - punishment - scold
# 11 - punishment - beat
# 12 - punishment - rape

###### j1
label training_event_disobey:
    
    "You attempt to train [char.name], but she won't obey you."
    
    jump girl_interactions
    

###### j2
label training_event_stop:
    
    "You attempt to train [char.name], but she wants nothing to do with this course."
    
    jump girl_interactions
    

###### j3
label training_event_runaway:
    
    "You attempt to train [char.name], but she manages to escape before you can start!"
    
    jump girl_interactions
    

###### j4
label training_event_girl_ap:
    
    "You try to train [char.name], but she doesn't have enough AP!"
    
    jump girl_interactions
    

###### j5
label training_event_hero_ap:
    
    "You try to train [char.name], but you don't have enough AP!"
    
    jump girl_interactions
    

###### j6
label training_event_no_gold:
    
    "You try to train [char.name], but can't afford the necessary materials."
    
    jump girl_interactions
    

###### j7
label training_reward_praise:
    
    "You praise [char.name] for her good behaviour."
    
    $ gm_job()
    jump girl_interactions
    

###### j8
label training_reward_treat:
    
    "You treat [char.name] for her good behaviour."
    
    $ gm_job()
    jump girl_interactions
    

###### j9
label training_reward_pleasure:
    
    "You sexually pleasure [char.name] for her good behaviour."
    
    if gm_job.does_obey:
        "She responds brilliantly."
    
    $ gm_job()
    jump girl_interactions
     

###### j10
label training_punishment_scold:
    
    "You scold [char.name] for her bad behaviour."
    
    $ gm_job()
    jump girl_interactions
    

###### j11
label training_punishment_beat:
    
    "You beat [char.name] for her bad behaviour."
    
    $ gm_job()
    jump girl_interactions
    

###### j12
label training_punishment_rape:
    
    "You rape [char.name] for her bad behaviour."
    
    $ gm_job()
    jump girl_interactions
    
