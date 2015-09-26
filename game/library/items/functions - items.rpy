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
        elif item.sex != char.gender and item.sex != "unisex":
            if not silent:
                renpy.show_screen('pyt_message_screen', "{} item cannot be equipped on a eqtargetacter of {} gender!".format(item.id, char.gender))
            return
        elif item.slot == "quest":
            if not silent:
                renpy.show_screen("pyt_message_screen", "Quest items cannot be equipped!")
            return
        elif item.slot == "gift":
            if not silent:
                renpy.call_screen("pyt_message_screen", "Gift slot items only serve purpose during girl meets!")
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
                
    def transfer_items(source, target, item, amount=1):
        """
        Attempts to transfer amount of items from source to target.
        Returns True in case of sucess and False if it fails.
        """
        if isinstance(item, basestring):
            item = items[item]
        if item.slot == "quest":
            renpy.call_screen('pyt_message_screen', "Quest items cannot be transferred!")
            return False
        if item.unique and item.unqiue == target.id:
            renpy.call_screen('pyt_message_screen', "%s cannot be transferred to this character!" % item.id)
            return False
        # Free girls should always refuse giving up their items unless MC gave it to them.
        if all([isinstance(source, Char), source.status != "slave"]):
            if any([item.slot == "consumable", (item.slot == "misc" and item.mdestruct), source.given_items.get(item.id, 0) - amount < 0]):
                # She will not give up the item:
                return False
            else:
                if source.inventory.remove(item, amount):
                    source.given_items[item.id] = source.given_items.get(item.id, 0) - amount
                    if all([isinstance(target, Char), target.status != "slave"]):
                        target.given_items[item.id] = target.given_items.get(item.id, 0) + amount
                    target.inventory.append(item, amount)
                    return True
                    
        if source.inventory.remove(item, amount):
            if all([isinstance(target, Char), target.status != "slave"]) or not any([item.slot == "consumable", (item.slot == "misc" and item.mdestruct), isinstance(target, Player)]):
                target.given_items[item.id] = target.given_items.get(item.id, 0) + amount 
            target.inventory.append(item, amount)
            return True
            
        return False
