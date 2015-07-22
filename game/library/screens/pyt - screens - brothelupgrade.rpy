label brothel_upgrade:
    
    hide screen pyt_brothel_management
    
    scene bg scroll
    show screen pyt_brothel_upgrade
    with fade
    
    python:
        confirm_purchase = None
        
        while True:
            result = ui.interact()
            
            if result[0] == 'buy':
                confirm_purchase = result[1]
                
                if renpy.call_screen("yesno_prompt",
                                     message="Would you like to add %s to your brothel?" % confirm_purchase['name'],
                                     yes_action=Return(True), no_action=Return(False)):
                    
                    if brothel.used_upgrade_slots < brothel.upgrade_slots:
                        if hero.take_money(brothel.get_upgrade_price(confirm_purchase), reason="Brothel Upgrades"):
                            confirm_purchase["active"] = True
                            brothel.used_upgrade_slots += 1
                        
                        else:
                            renpy.call_screen("pyt_message_screen", "You don't have enough gold!")
                    
                    else:
                        renpy.call_screen("pyt_message_screen", "There are no more upgrade slots available in the building!")
                
                else:
                    confirm_purchase = None
            
            if result[0] == 'control':
                if result[1] == 'return':
                    break
    
    hide screen pyt_brothel_upgrade
    jump brothel_management
    

screen pyt_brothel_upgrade:
    
    default tt = Tooltip("Improve your buildings here. Choose upgrades wisely.")
    
    # Slots frame
    frame:
        style_group "content"
        xalign 0.5
        ypos 48
        xysize (200, 50)
        xpadding 4
        ypadding 10
        background Frame("content/gfx/frame/mes11.jpg", 10, 10)
        text ("Slots: %d/%d"%(brothel.used_upgrade_slots, brothel.upgrade_slots)) align (0.5, 0.5) color ivory
    
    # Upgrades
    vbox:
        xalign 0.50
        ypos 105
        xminimum 500
        ymaximum 600
        box_wrap True
        spacing 5
        
        for xkey in brothel.upgrades:
            if brothel.upgrades[xkey]['1']['available']:
                hbox:
                    frame:
                        background Frame("content/gfx/frame/arena_d.png", 5, 5)
                        xminimum 430
                        xpadding 15
                        ypadding 10
                        hbox:
                            spacing 5
                            xalign 0.5
                            for ukey in sorted(brothel.upgrades[xkey].keys()):
                                if brothel.upgrades[xkey][ukey]['available']:
                                    if brothel.upgrades[xkey][ukey]['active']:
                                        vbox:
                                            spacing 5
                                            frame:
                                                xysize (130, 130)
                                                background Frame("content/gfx/frame/mes11.jpg", 5, 5)
                                                xpadding 5
                                                ypadding 5
                                                add (im.Scale(brothel.upgrades[xkey][ukey]['img'], 130, 130)) align(0.5, 0.5)
                                    else:
                                        vbox:
                                            spacing 5
                                            frame:
                                                align(0.5, 0.99)
                                                xysize (130, 130)
                                                background Frame("content/gfx/frame/mes11.jpg", 5, 5)
                                                xpadding 5
                                                ypadding 5
                                                if ukey == '1':
                                                    use rtt_lightbutton(img=im.Scale(brothel.upgrades[xkey][ukey]['img'], 130, 130),
                                                                                  return_value=['buy',brothel.upgrades[xkey][ukey]],
                                                                                  tooltip="%s \n%s \nPrice: %d Gold. "%(brothel.upgrades[xkey][ukey]['name'],
                                                                                  brothel.upgrades[xkey][ukey]['desc'],
                                                                                  brothel.get_upgrade_price(brothel.upgrades[xkey][ukey])))
                                                elif brothel.upgrades[xkey][str(int(ukey)-1)]['active']:
                                                    use rtt_lightbutton(img=im.Scale(brothel.upgrades[xkey][ukey]['img'], 130, 130),
                                                                                  return_value=['buy',brothel.upgrades[xkey][ukey]],
                                                                                  tooltip="%s \n%s \nPrice: %d Gold. "%(brothel.upgrades[xkey][ukey]['name'],
                                                                                  brothel.upgrades[xkey][ukey]['desc'],
                                                                                  brothel.get_upgrade_price(brothel.upgrades[xkey][ukey])))
                                                else:
                                                    add(im.Sepia(im.Scale(brothel.upgrades[xkey][ukey]['img'], 130,130))) align(0.5, 0.99)
                    null width 10
    # Tooltip text            
    frame:
        xpadding 10
        ypadding 12
        background Frame("content/gfx/frame/frame_hor_stripe.png", 10, 10)
        align (0.5, 1.0)
        xysize (1150, 110)
        has vbox
        text (u"{=content_text}{color=[ivory]}%s" % tt.value)
    
    use pyt_top_stripe(True)
