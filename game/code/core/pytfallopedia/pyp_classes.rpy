init python:
    class PyTFallopedia(_object):
        def __init__(self):
            self.main_focused = None
            self.sub_focused = None

            self.main = OrderedDict()
            # name: screen
            self.sub = OrderedDict()
            # main: (sub, sub_screen)

        @property
        def main_screen(self):
            return self.main.get(self.main_focused, None)

        @property
        def sub_screen(self):
            try:
                return self.sub_focused[1]
            except:
                return None

        def add_main(self, name, screen):
            if name in self.main:
                return

            self.main[name] = screen

        def add_sub(self, name, screen, main):
            if main not in self.main:
                return
            elif not len(self.sub.get(main, [])):
                self.sub[main] = [(main, self.main[main])]

            if (name, screen) not in self.sub[main]:
                self.sub[main].append((name, screen))


init python:
    pyp = PyTFallopedia()
    pyp.add_main("General", "pyp_general")
    pyp.add_sub("Flow of Time", "pyp_time_flow", "General")
    pyp.add_sub("Action Points", "pyp_action_points", "General")
    pyp.add_sub("Next Day", "pyp_next_day", "General")
    pyp.add_sub("Controls", "pyp_controls", "General")
    pyp.add_sub("Gazette", "pyp_gazette", "General")

    pyp.add_main("Characters", "pyp_characters")
    pyp.add_sub("Tiers/Level", "pyp_tiers", "Characters")
    pyp.add_sub("Stats", "pyp_stats", "Characters")
    pyp.add_sub("Skills", "pyp_skills", "Characters")
    pyp.add_sub("Controls", "pyp_char_controls", "Characters")
    pyp.add_sub("Status", "pyp_status", "Characters")
    pyp.add_sub("Actions", "pyp_action_points", "Characters")

    pyp.add_main("Traits", "pyp_traits")
    pyp.add_sub("Classes", "pyp_classes", "Traits")
    pyp.add_sub("Fixed Traits", "pyp_fixed_traits", "Traits")
    pyp.add_sub("Elements", "pyp_elements", "Traits")
    pyp.add_sub("Effects", "pyp_effects", "Traits")

    pyp.add_main("City", "pyp_city")
    pyp.add_sub("Interactions", "pyp_interactions", "City")
    pyp.add_sub("MC Actions", "pyp_mc_actions", "City")
    pyp.add_sub("Slave Market", "pyp_slave_market", "City")
    pyp.add_sub("NPCs", "pyp_npcs", "City")
    pyp.add_sub("Arena", "pyp_arena", "City")
    pyp.add_sub("Main Street", "pyp_main_street", "City")

    pyp.add_main("Combat", "pyp_battle_engine")
    pyp.add_sub("Teams", "pyp_teams", "Combat")
    pyp.add_sub("Attacks", "pyp_attacks", "Combat")
    pyp.add_sub("Magic", "pyp_magic", "Combat")
    pyp.add_sub("Items", "pyp_be_items", "Combat")
    pyp.add_sub("Escape", "pyp_escape", "Combat")

    pyp.add_main("Items", "pyp_items")
    pyp.add_sub("Consumable", "pyp_consumables", "Items")
    pyp.add_sub("Weapons", "pyp_weapons", "Items")
    pyp.add_sub("Unequipable", "pyp_materials", "Items")
    pyp.add_sub("Equippable", "pyp_equippables", "Items")
    pyp.add_sub("MISC", "pyp_misc", "Items")
    pyp.add_sub("Stats/Skills", "pyp_stats_bonuses", "Items")
    pyp.add_sub("Inventory", "pyp_inventory", "Items")
    pyp.add_sub("Shopping", "pyp_shopping", "Items")
    pyp.add_sub("Auto Equip", "pyp_auto_equip", "Items")
    pyp.add_sub("Transfer", "pyp_transfer", "Items")
    pyp.add_sub("Storage", "pyp_storage", "Items")

    pyp.add_main("Buildings&Businesses", "pyp_buildings_and_businesses")
    pyp.add_sub("Buildings", "pyp_buildings", "Buildings&Businesses")
    pyp.add_sub("Businesses", "pyp_businesses", "Buildings&Businesses")
    pyp.add_sub("Clients", "pyp_clients", "Buildings&Businesses")
    pyp.add_sub("Building Stats", "pyp_building_stats", "Buildings&Businesses")
    pyp.add_sub("Advertising", "pyp_advertising", "Buildings&Businesses")
    pyp.add_sub("Management", "pyp_manager", "Buildings&Businesses")
    pyp.add_sub("Controls", "pyp_buildings_controls", "Buildings&Businesses")
    pyp.add_sub("Workers", "pyp_workers", "Buildings&Businesses")
    pyp.add_sub("Jobs", "pyp_jobs", "Buildings&Businesses")
    pyp.add_sub("Simulation", "pyp_simulation", "Buildings&Businesses")

    pyp.add_main("School", "pyp_school")

    pyp.add_main("Quest&Events", "pyp_quests_and_events")
    pyp.add_sub("Quests", "pyp_quests", "Quest&Events")
    pyp.add_sub("Events", "pyp_events", "Quest&Events")
