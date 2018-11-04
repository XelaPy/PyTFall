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

            if (name, screen) not in self.sub.get(main, []):
                self.sub.setdefault(main, []).append((name, screen))


init python:
    pyp = PyTFallopedia()
    pyp.add_main("Characters", "pyp_characters")
    pyp.add_sub("Tiers/Level", "pyp_tiers", "Characters")
    pyp.add_sub("Stats", "pyp_stats", "Characters")
    pyp.add_sub("Skills", "pyp_skills", "Characters")
    pyp.add_sub("Controls", "pyp_controls", "Characters")
    pyp.add_sub("Status", "pyp_status", "Characters")
    pyp.add_sub("Actions", "pyp_actions", "Characters")

    pyp.add_main("Traits", "pyp_traits")
    pyp.add_sub("Classes", "pyp_classes", "Traits")
    pyp.add_sub("Fixed Traits", "pyp_fixed_traits", "Traits")
    pyp.add_sub("Elements", "pyp_elements", "Traits")
    pyp.add_sub("Effects", "pyp_effects", "Traits")


    # pyp.add_sub("Skills", "pyp_skills", "Traits")
