# Base Events File
init -1 python:
    register_event("found_money_event", locations=["all"], run_conditions=["dice(max(15, hero.luck+10))"], priority=50, dice=0, restore_priority=0)
    register_event("found_item_event", locations=["all"], run_conditions=["dice(max(35, hero.luck+20))"], priority=50, dice=0, restore_priority=0)

label found_money_event(event):
    $ amount = locked_random("randint", 5, 10) + max(0, hero.luck) + hero.level
    $ hero.add_money(amount, "Luck")
    $ gfx_overlay.random_find(amount, 'gold')
    $ hero.say(choice(["Some money... Excellent.", "Free gold, nice!",
                       "A few coins! I'm lucky today.", "Did someone drop a wallet?"]))
    return

label found_item_event(event):
    python:
        if locked_dice(60):
            items_pool = list(item for item in items.values() if "Look around" in item.locations and dice(item.chance))
            found_item = choice(items_pool)
        else:
            found_item = items["Rebels Leaflet"]

    $ gfx_overlay.random_find(found_item, 'item')
    $ hero.inventory.append(found_item)

    python:
        if found_item != items["Rebels Leaflet"]:
            hero.say(choice(["Hmm. I found something. ([found_item.id])",
                             "[found_item.id] might be useful...",
                             "[found_item.id]? Nice, might be useful.",
                             "Oh, [found_item.id]! Never look a gift horse in the mouth..."]))
        else:
            hero.say("An old prewar leaflet... I probably shouldn't keep it in my pockets for long.")
    return
