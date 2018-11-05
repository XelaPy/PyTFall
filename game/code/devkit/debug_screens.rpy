init python:
    def dd_cursor_position(st, at):
        x, y = renpy.get_mouse_pos()
        return Text("{size=-5}%d-%d" % (x, y)), .1

screen debug_tools():
    layer "tooltips"
    drag:
        align .0, 1.0
        id "meow____"
        frame:
            background Frame("content/gfx/frame/frame_gp2.webp", 2, 2)
            # xsize 90
            has vbox xsize 90
            hbox:
                xalign 1.0
                textbutton "H":
                    action Hide("debug_tools")
                textbutton "X":
                    action Quit(confirm=False)
                textbutton "R":
                    action ui.callsinnewcontext("_save_reload_game")
            add DynamicDisplayable(dd_cursor_position)
            text "[last_label]" size 10
            text "{}".format(renpy.get_filename_line()) size 10
            text "Call Stack: " + str(renpy.call_stack_depth()) size 10
            for i in renpy.game.context().return_stack:
                text str(i) size 10


style chars_debug_text:
    size 10

style chars_debug_fixed:
    yalign .5

screen chars_debug():
    zorder 100
    modal True

    default all_chars = [chars.values(), pytfall.arena.arena_fighters.values()]
    default all_chars_str = ["chars", "arena"]
    default shown_chars = [all_chars[0]]

    style_prefix "chars_debug"

    add black
    vbox:
        hbox:
            spacing 1
            ysize 20
            fixed:
                xysize 80, 20
                text "Name" color red bold 1
            fixed:
                xysize 80, 20
                text "Lvl/Tier" color red bold 1
            fixed:
                xysize 80, 20
                text "Class" color red bold 1
            fixed:
                xysize 80, 20
                text "Elements" color lawngreen bold 1
            fixed:
                xysize 80, 20
                text "Origin" color crimson bold 1
            fixed:
                xysize 50, 20
                text "Status" color green bold 1
            fixed:
                xysize 80, 20
                text "Location" color blue bold 1
            fixed:
                xysize 80, 20
                text "Home" color blue bold 1
            fixed:
                xysize 80, 20
                text "Work" color blue bold 1
            fixed:
                xysize 80, 20
                text "Action" color orange bold 1
            fixed:
                xysize 80, 20
                text "Inv" color gold bold 1
            fixed:
                xysize 80, 20
                text "Magic" color purple bold 1

        viewport:
            xysize 1280, 700
            child_size 1280, 10000
            draggable 1 mousewheel 1
            has vbox
            for char in list(sorted(chain.from_iterable(shown_chars), key=attrgetter("name"))):
                hbox:
                    spacing 1
                    ysize 30
                    fixed:
                        xysize 80, 20
                        text "[char.name]" color red
                    fixed:
                        xysize 80, 20
                        text "[char.level]/[char.tier]" color red bold 1
                    vbox:
                        xysize 80, 20
                        yalign .5
                        text "\n".join([e.id for e in char.elements]) color lawngreen bold 1 size 10
                    vbox:
                        xysize 80, 20
                        yalign .5
                        for t in sorted(char.traits.basetraits):
                            text t.id color blue bold 1 size 8 xalign .0
                    fixed:
                        xysize 80, 20
                        text "[char.origin]" color crimson
                    fixed:
                        xysize 50, 20
                        text "[char.status]" color green
                    fixed:
                        xysize 80, 20
                        text "[char.location]" color blue:
                            if len(str(char.location)) > 12:
                                size 6
                    fixed:
                        xysize 80, 20
                        text "[char.home]" color blue:
                            if len(str(char.home)) > 12:
                                size 6
                    fixed:
                        xysize 80, 20
                        text "[char.workplace]" color blue:
                            if len(str(char.workplace)) > 12:
                                size 6
                    fixed:
                        xysize 80, 20
                        text "[char.action]" color orange
                    python:
                        temp = []
                        for item in char.eqslots.values():
                            if isinstance(item, Item):
                                ts = []
                                ts.append("{color=#ffffff}: {/color}".join([item.slot, item.id]))
                                ts.append("{color=#00ff00}Eq!{/color}")
                                temp.append(" ==> ".join(ts))
                        for item in char.inventory:
                            ts = []
                            ts.append(item.id)
                            ts.append("{color=#ffffff}NEq{/color}")
                            temp.append(" ==> ".join(ts))
                    textbutton "Inv":
                        xysize 80, 20
                        action NullAction()
                        tooltip "\n".join(temp)
                    python:
                        temp = []
                        for bskill in char.magic_skills:
                            temp.append(bskill.name)
                    textbutton "Magic":
                        xysize 80, 20
                        text_color purple
                        action NullAction()
                        tooltip "\n".join(temp)

    hbox:
        align 1.0, .0
        for index, container in enumerate(all_chars):
            $ name = all_chars_str[index]
            if container in shown_chars:
                textbutton "[name]":
                    text_color green
                    action Function(shown_chars.remove, container)
            else:
                textbutton "[name]":
                    text_color red
                    action Function(shown_chars.append, container)
        textbutton "X":
            action Hide("chars_debug")
