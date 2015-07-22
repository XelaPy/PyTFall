init -11 python:
    # Equipment checks and area effects!
    def equip_item(item, chr):
        """
        First level of checks, all items should be equiped through this function!
        TODO: Move this to Chracter equipment method?
        """
        if item.unique and item.unique != item.id:
            renpy.show_screen("pyt_message_screen", "This unique item cannot be equipped on %s!" % chr.name)
            return
        if item.slot == "quest":
            renpy.show_screen("pyt_message_screen", "Quest items cannot be equipped!")
            return
        if item.slot == 'consumable':
            if not item.ceffect:
                chr.equip(item)
            elif item.ceffect == 'brothelgirls':
                if chr.location in hero.brothels:
                    chr.inventory.remove(item)
                    for girl in [char[key] for key in char if char[key].location == chr.location]:
                        girl.equip(item)
                else:
                    renpy.call_screen('pyt_message_screen', "%s in not in any brothel! "% chr.nickname)

            elif item.ceffect == 'brothelfree':
                if chr.location in hero.brothels:
                    chr.inventory.remove(item)
                    for girl in [char[key] for key in char if char[key].location == chr.location]:
                        if girl.status != 'slave':
                            girl.equip(item)
                else:
                    renpy.call_screen('pyt_message_screen', "%s in not in any brothel! "%chr.nickname)

            elif item.ceffect == 'brothelslave':
                if chr.location in hero.brothels:
                    chr.inventory.remove(item)
                    for girl in [char[key] for key in char if char[key].location == chr.location]:
                        if girl.status == 'slave':
                            girl.equip(item)
                else:
                    renpy.call_screen('pyt_message_screen', "%s in not in any brothel! "%chr.nickname)

            elif item.ceffect == 'allslaves':
                chr.inventory.remove(item)
                for girl in [girl for girl in hero.girls if girl.status == 'slave']:
                    girl.equip(item)

            elif item.ceffect == 'allfree':
                chr.inventory.remove(item)
                for girl in [girl for girl in hero.girls if girl.status != 'slave']:
                    girl.equip(item)

            elif item.ceffect == 'allgirls':
                chr.inventory.remove(item)
                for girl in [girl for girl in hero.girls]:
                    girl.equip(item)

        elif item.slot == "gift":
            renpy.call_screen("pyt_message_screen", "Gift slot items only serve purpose during girl meets!")
        elif item.slot == "quest":
            renpy.call_screen("pyt_message_screen", "Quest Items cannot be equipped!")
        else:    
            chr.equip(item)
            
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
        if all([isinstance(source, Girl), source.status != "slave"]):
            if any([item.slot == "consumable", (item.slot == "misc" and item.mdestruct), source.given_items.get(item.id, 0) - amount < 0]):
                # She will not give up the item:
                return False
            else:
                if source.inventory.remove(item, amount):
                    source.given_items[item.id] = source.given_items.get(item.id, 0) - amount
                    if all([isinstance(target, Girl), target.status != "slave"]):
                        target.given_items[item.id] = target.given_items.get(item.id, 0) + amount
                    target.inventory.append(item, amount)
                    return True
                    
        if source.inventory.remove(item, amount):
            if all([isinstance(target, Girl), target.status != "slave"]) or not any([item.slot == "consumable", (item.slot == "misc" and item.mdestruct), isinstance(target, Player)]):
                target.given_items[item.id] = target.given_items.get(item.id, 0) + amount 
            target.inventory.append(item, amount)
            return True
            
        return False
