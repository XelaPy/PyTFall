init python:
    register_event("events_thugs_robbery", locations=["main_street"], dice=100, trigger_type = "look_around", max_runs=1, priority = 1, times_per_days=(2,6), start_day=1, restore_priority=1, jump=True)
    

label events_thugs_robbery:
    show expression npcs["street_thug"].get_vnsprite() as npc
    $ t = npcs["street_thug"].say
    t "Sup m8?"
    
    jump main_street