init -11 python:
    # Equipment checks and area effects!
    def can_equip(item, char, silent=True):
        """Checks if it is legal for a character to equip the item.
        
        @param: silent: If False, game will notify the player with a reason why an item cannot be equipped.
        """
        if all([item.unique, isinstance(char, Player), item.unique != "mc"]) or all([item.unique, item.unique != char.id]):
            if not silent:
                renpy.show_screen("pyt_message_screen", "This unique item cannot be equipped on {}!".format(char.name))
            return
        elif item.sex not in ["unisex", char.gender]:
            if not silent:
                renpy.show_screen('pyt_message_screen', "{} item cannot be equipped on a character of {} gender!".format(item.id, char.gender))
            return
        elif not item.usable:
            if not silent:
                renpy.show_screen("pyt_message_screen", "This item cannot be used or equipped!")
            return
        return True
        
    def equip_item(item, char, silent=False, area_effect=False):
        """
        First level of checks, all items should be equiped through this function!
        TODO: Move this to Chracter equipment method? And Restore AREA EFFECT!
        """
        if not can_equip(item, char, silent=silent):
            return
        
        if item.slot == 'consumable' and area_effect:
            if not item.ceffect:
                char.equip(item)
            elif item.ceffect == 'brothelgirls':
                if char.location in hero.brothels:
                    char.inventory.remove(item)
                    for girl in [chars[key] for key in chars if chars[key].location == char.location]:
                        girl.equip(item)
                else:
                    renpy.call_screen('pyt_message_screen', "%s in not in any brothel! "% char.nickname)

            elif item.ceffect == 'brothelfree':
                if char.location in hero.brothels:
                    char.inventory.remove(item)
                    for girl in [chars[key] for key in chars if chars[key].location == char.location]:
                        if girl.status != 'slave':
                            girl.equip(item)
                else:
                    renpy.call_screen('pyt_message_screen', "%s in not in any brothel! "%char.nickname)

            elif item.ceffect == 'brothelslave':
                if char.location in hero.brothels:
                    char.inventory.remove(item)
                    for girl in [chars[key] for key in chars if chars[key].location == char.location]:
                        if girl.status == 'slave':
                            girl.equip(item)
                else:
                    renpy.call_screen('pyt_message_screen', "%s in not in any brothel! "%char.nickname)

            elif item.ceffect == 'allslaves':
                char.inventory.remove(item)
                for girl in [girl for girl in hero.girls if girl.status == 'slave']:
                    girl.equip(item)

            elif item.ceffect == 'allfree':
                char.inventory.remove(item)
                for girl in [girl for girl in hero.girls if girl.status != 'slave']:
                    girl.equip(item)

            elif item.ceffect == 'allgirls':
                char.inventory.remove(item)
                for girl in [girl for girl in hero.girls]:
                    girl.equip(item)
        else:
            char.equip(item)
            
    def equip_for(girl, jobtype):
        # TODO: Must be updated to work with new base-traits and jobs system.
        if girl.autoequip:
            if jobtype == "Guard":
                girl.equip_for("Combat")
            elif jobtype == "ServiceGirl":
                girl.equip_for("Service")
            elif jobtype == "Stripper":
                girl.equip_for("Striptease")
            elif jobtype == "Whore":
                girl.equip_for("Sex")
                
    def can_transfer(source, target, item, amount=1, silent=True):
        """Checks if it is legal for a character to transfer the item.
        
        @param: silent: If False, game will notify the player with a reason why an item cannot be equipped.
        """
        if all([item.unique, isinstance(target, Player), item.unique != "mc"]) or all([item.unique, item.unique != target.id]):
            if not silent:
                renpy.show_screen("pyt_message_screen", "This unique item cannot be given to {}!".format(char.name))
            return
        if item.slot == "quest":
            if not silent:
                renpy.show_screen('pyt_message_screen', "Quest items cannot be transferred!")
            return
        # Free girls should always refuse giving up their items unless MC gave it to them.
        if all([isinstance(source, Char), source.status != "slave"]):
            if any([item.slot == "consumable", (item.slot == "misc" and item.mdestruct), source.given_items.get(item.id, 0) - amount < 0]):
                if not silent:
                    source.say(choice(["Like hell am I giving away!", "Go get your own!", "Go find your own %s!" % item.id, "Would you like fries with that?",
                                                   "Perhaps you would like me to give you the key to my flat where I keep my money as well?"]))
                return
        return True
                
    def transfer_items(source, target, item, amount=1, silent=False):
        """Transfers items between characters. 
        
        This will also log a fact of transfer between a character and MC is appropriate.
        """
        if isinstance(item, basestring):
            item = items[item]
            
        if not can_transfer(source, target, item, amount=1, silent=silent):
            return
            
        cond = any([item.slot == "consumable", (item.slot == "misc" and item.mdestruct)])
        if source.inventory.remove(item, amount):
            if all([isinstance(source, Char), source.status != "slave"]) and not cond:
                source.given_items[item.id] = source.given_items.get(item.id, 0) - amount
            if all([isinstance(target, Char), target.status != "slave"]) and not cond:
                target.given_items[item.id] = target.given_items.get(item.id, 0) + amount
            target.inventory.append(item, amount)
            return True
                    
        return False
