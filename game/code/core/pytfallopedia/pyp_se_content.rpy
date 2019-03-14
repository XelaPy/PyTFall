screen pyp_se_guild():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Exploration Guild" size 30

            vbox:
                ypos 80
                text ("The guild is a specialized business that enables exploration of magically unstable areas around PyTFall."+
                      " The events that ended the age of Old Masters and lead to the destruction of the city resulted in interdimensional breaches,"+
                      " many hazardous, ever-changing areas to be explored with unending amounts of riches to be found.")
                null height 5
                text ("Most of the original explorers have found nothing but death on their exploration runs, so the city authorities enforced a system"+
                      " of guilds to try and stabilize the situation and prevent further loss of life of the best warriors and mages of the land.")
                null height 5
                text ("Even now, death on exploration runs is reasonably common, and caution is advised! A number of upgrades to the guild are also available.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/se_4.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_se_teams():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Teams management" size 30

            vbox:
                ypos 80
                text ("Guild team management screen is a drag and drop interface which allows you to form exploration teams."+
                      " You can disband, rename and create new teams (limited by guild capacity) and filter/sort available characters.")
                null height 5
                text ("Drag the characters to put them in teams or left click on them from extra options.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/se_0.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_se_log():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Next Day Exploration Log" size 30

            vbox:
                ypos 80
                text ("When the team comes back to the guild, a report is generated. You can view"+
                      " it under guild reports or under the building which hosts the guild.")
                null height 5
                text ("If team doesn't survive the exploration run, you will be notified of that"+
                      " but all their loot and information about their movements and actions will be lost.")

        fixed:
            xpos 601
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/se_1.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_se_exploration_1():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Exploration GUI" size 30

            vbox:
                ypos 80
                text ("Areas are structured into mail location which contains a number of smaller areas to be explored."+
                      " Each of those areas has difficulty, items, gold to be found, etc. New location can be unlocked"+
                      " by exploring areas, throughs quest or interacting with the game world. If areas are left unexplored,"+
                      " exploration will slowly be reduced on daily basis.")
                null height 5
                text ("Teams can construct a camp in each area. Camp provides extra healing for damaged teams and overnight."+
                      " Multiple teams can be sent to construct a camp at the same time.")
                null height 5
                text ("Risk determines how far the teams will push to gain rewards when exploring an area."+
                      " While high risk will yield better results"+
                      " it will also increase chance of explorers or even the entire teams dying.")

        fixed:
            xpos 601
            spacing 3
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/se_3.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"

screen pyp_se_exploration_2():
    zorder 1001

    fixed:
        pos 302, 49
        xysize 971, 664
        style_prefix "pyp"
        fixed:
            xysize 600, 664
            # Title and text bits:
            frame:
                style_suffix "title_frame"
                xalign .5 ypos 10
                text "Exploration GUI" size 30

            vbox:
                ypos 80
                text ("Hazards damage the entire team regardless of risk or other factors and cannot be avoided."+
                      " Usually more of an annoyance, you may want to consider sending a well equipped,"+
                      " experienced teams to such places.")
                null height 5
                text ("Player may set number of days (3-15) for teams to remain in the area. If things get to"+
                      " dangerous, team may fall back prematurely. The longer a team explores an area"+
                      " in a single exploration run, the greater the rewards become."+
                      " Teams travel to and back from the location. Time required to do so is not included in"+
                      " exploration time.")
                null height 5
                text ("In certain areas teams may meet and capture characters. By law, those characters are to be"+
                      " submitted to City Jail until their situations can be sorted out. Visit them there for more info."
                      " You can decide if your teams going to capture characters.")
                null height 5
                text ("You can view latest events for each areas, what items have been located and what mobs have been encountered by your teams.")

        fixed:
            xpos 601
            spacing 3
            xysize 370, 664
            style_prefix "pyp"
            frame:
                xalign .5 ypos 80
                add pscale("content/gfx/interface/pyp/se_2.webp", 350, 1000)

    # ForeGround frame (should be a part of every screen with Info):
    add "content/gfx/frame/h3.webp"
