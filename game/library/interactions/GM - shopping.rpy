###### j0
# quick navigation, search "j" + number, example: j0 - this panel
# 
#  1 - shopping - shopping
###### j1
label interactions_shopping:
    # TODO: Get rid of this or update it to modern PyTFall!
    #copied from tailor shop
    #then modified for own use
    hide screen pyt_girl_interactions
    
    scene bg tailor_store
    with dissolve
    
    show npc tailor_store_assistant
    with dissolve
    
    if global_flags.flag('visited_tailor_store'):
        "Welcome Back!"
        "Ah with one of your ladies. Let see what they'd like! "
    
    else:
        $global_flags.set_flag('visited_tailor_store')
        "Welcome to my store!"
        "Just the best clothing you'll ever see! "
        "Check out our latest collection, your girl will love it: "
    
    hide npc tailor_store_assistant
    with dissolve
    
    python:
        focus = False
        pytfall.tailor_store.inventory.apply_filter('all')
        chr.inventory.set_page_size(18)
        chr.inventory.apply_filter('all')
    
    show screen pyt_tailor_store_shopping_girl
    with dissolve
    
    python:
        txt = ''
        while True:
            result = ui.interact()
            if result[0] == 'shop':
                if result[1] == 'first_page':pytfall.tailor_store.inventory.first()
                elif result[1] == 'last_page':pytfall.tailor_store.inventory.last()
                elif result[1] == 'next_page':pytfall.tailor_store.inventory.next()
                elif result[1] == 'prev_page':pytfall.tailor_store.inventory.prev()
                elif result[1] == 'prev_filter':pytfall.tailor_store.inventory.apply_filter('prev')
                elif result[1] == 'next_filter':pytfall.tailor_store.inventory.apply_filter('next')
                else:
                    purchasing_dir = 'buy'
                    focus = pytfall.tailor_store.inventory.getitem(result[1])
            
            elif result[0] == 'inv':
                if result[1] == 'first_page':chr.inventory.first()
                elif result[1] == 'last_page':chr.inventory.last()
                elif result[1] == 'next_page':chr.inventory.next()
                elif result[1] == 'prev_page':chr.inventory.prev()
                elif result[1] == 'prev_filter':chr.inventory.apply_filter('prev')
                elif result[1] == 'next_filter':chr.inventory.apply_filter('next')
                else:
                    purchasing_dir = 'sell'
                    focus = chr.inventory.getitem(result[1])
            
            elif result[0] == 'control':
                if result[1] == 'buy/sell':
                    if purchasing_dir == 'buy':
                        result = hero.take_money(focus.price, reason="Gifts")
                        
                        if result:
                            if chr.status == 'slave':
                                if chr.occupation=='Prostitute':
                                    for entry in focus.mod:
                                        if entry =='anal' or entry =='normalsex' or entry =='lesbian':
                                            txt =="%s will definitly make me a better whore for master.\n"%focus.id
                                            chr.mod('disposition', 1)
                                
                                if chr.occupation=='Stripper':
                                    for entry in focus.mod:
                                        if entry =='strip':
                                            txt =="%s will make my stripping performance even better Master.\n"%focus.id
                                            chr.mod('disposition', 1)
                                
                                if chr.occupation=='ServiceGirl':
                                    txt += "ServiceGirl Slave"
                                
                                if chr.occupation=='Warrior':
                                    txt += "Warrior Slavet"
                                
                                if chr.occupation=='Healer':
                                    txt += "Healer Slave"
                            
                            else:
                                if chr.occupation=='Prostitute':
                                    for entry in focus.mod:
                                        if entry =='anal' or entry =='normalsex' or entry =='lesbian':
                                            txt =="%s will definitly make me a better whore for master."%focus.id
                                            chr.mod('disposition', 1)
                                
                                if chr.occupation=='Stripper':
                                    txt += "Stripper Slave"
                                
                                if chr.occupation=='ServiceGirl':
                                    txt += "ServiceGirl Slave"
                                
                                if chr.occupation=='Warrior':
                                    txt += "Warrior Slavet"
                                
                                if chr.occupation=='Healer':
                                    txt += "Healer Slave"
                            
                            if chr.joy < 40:
                                if focus.price > 1000:
                                    txt += "Thank you very much Master. I will put the %s to good use.\n"%focus.id
                                    chr.mod('joy', 2)
                                    chr.mod('disposition', 4)
                                    chr.mod('disposition', 1)
                                
                                else:
                                    txt += "Thank you Master for the %s.\n"%focus.id
                                    chr.mod('disposition', 2)
                                    chr.mod('joy', 1)
                            
                            elif 39 < chr.joy < 80:
                                if focus.price > 1000:
                                    txt += "Thank you *KISS* very *VERY* much Master *KISS* for the %s .\n"%focus.id
                                    chr.mod('disposition', 5)
                                    chr.mod('joy', 3)
                                
                                else:
                                    txt += "*KISS* Thank you Master. I like the %s.\n"%focus.id
                                    chr.mod('disposition', 2)
                                    chr.mod('joy', 2)
                            
                            else:
                                if focus.price > 1000:
                                    txt += "MASTER! I love the %s. Thank you so much.\nShe gives you a kiss that leaves you breathless for a moment.\n"%focus.id
                                    chr.mod('disposition', 6)
                                    chr.mod('joy', 4)
                                
                                else:
                                    txt += "Master *KISS* Thank you Master. I like the %s.\n"%focus.id
                                    chr.mod('disposition', 3)
                                    chr.mod('joy', 3)
                            
                            pytfall.tailor_store.inventory.remove(focus)
                            chr.inventory.append(focus)
                            pytfall.tailor_store.gold += focus.price
                            break
                        
                        focus = False
                    
                    elif purchasing_dir == 'sell':
                        result = bool(pytfall.tailor_store.gold - focus.price >= 0)
                        
                        if result:
                            pytfall.tailor_store.gold -= focus.price
                            hero.add_money(focus.price, reason="Items")
                            chr.inventory.remove(focus)
                            pytfall.tailor_store.inventory.append(focus)
                            
                            if chr.occupation=='Prostitute':
                                txt += "Prostitute test"
                            
                            if chr.occupation=='Stripper':
                                txt += "Stripper test"
                            
                            if chr.occupation=='ServiceGirl':
                                txt += "ServiceGirl test"
                            
                            if chr.occupation=='Warrior':
                                txt += "Warrior test"
                            
                            if chr.occupation=='Healer':
                                txt += "Healer test"
                            
                            break
                        
                        focus = False
                
                elif result[1] == 'return':   
                    focus = False
                    break
    
    hide screen pyt_tailor_store_shopping_girl
    with dissolve
    
    python:
        pytfall.tailor_store.inventory.apply_filter('all')
        chr.inventory.apply_filter('all')
    
    if txt !='':
        g "[txt]"
    
    scene bg gallery
    with dissolve
    jump girl_interactions
    

screen pyt_tailor_store_shopping_girl:
    
    frame:
        align(0.5,0)
        xmaximum 600
        ymaximum 120
        
        hbox:
            null width 30
            add(im.Scale("content/gfx/interface/icons/gold.png", 40, 40)) align(0.5,0.5)
            null width 20
            text(u'{size=+1}{color=[gold]}{b}= %s{/b}'%hero.gold) align(0.5,0.5)
            null width 60 
            text(u'{size=+1}Day  =  %d'%day) align(0.5,0.5)
            null width 50

    use shop_inventory(root='inv',ref=chr,x=0.0,title="Inventory")
    use shop_inventory(root='shop',ref=pytfall.tailor_store,x=1.0,title="Tailor Store")
    
    if focus:
        frame background Frame("content/gfx/frame/mes12.jpg",5,5): 
            align (0.5,0.15)
            xmaximum 700
            ymaximum 400 #changed so the other frame can go below
            hbox:
                use itemstats(item=focus,mode='normal')                                                                 
            frame background Solid((0,0,0,0)):
                align (0.5,1.0)
                hbox:
                    text (u' Price: %s'%focus.price)
                    null width 20
                    textbutton "Buy/Sell" action Return(['control','buy/sell']) maximum(150,30)
        if chr.eqslots['body']: #only show the currently equiped item if there is one
            frame background Frame("content/gfx/frame/mes12.jpg",5,5): 
                align (0.5,0.95)
                xmaximum 700
                ymaximum 300
                use itemstats(item=chr.eqslots['body']) #added a mode to the itemstats
                    
        
    use r_lightbutton(img=im.Scale("content/gfx/interface/buttons/shape69.png",40,40),return_value =['control','return'], align=(0.99,0))
