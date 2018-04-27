label start_Hinata:
    python hide:
        char = copy_char(store.chars["Hinata"])
        store.chars[char.id + "_Twin"] = char

        # Set new name(s):
        char.name = "Hinata-chan"
        char.nickname = "Hinata's sis."
        char.init() # Normalize.
        store.hero.add_char(char)
    return
