## This file contains some of the options that can be changed to customize
## your Ren'Py game. It only contains the most common options... there
## is quite a bit more customization you can do.
##
## Lines beginning with two '#' marks are comments, and you shouldn't
## uncomment them. Lines beginning with a single '#' mark are
## commented-out code, and you may want to uncomment them when
## appropriate.

python early:
    # These control the name and version of the game, that are reported
    # with tracebacks and other debugging logs.
    config.name = "PyTFall"
    config.version = "0.56 Step by Step..."
    #########################################
    ## This is the name of the directory where the game's data is
    ## stored. (It needs to be set early, before any other init code
    ## is run, so the persistent information can be found by the init code.)
    config.save_directory = None

    ## These control the width and height of the screen.
    config.screen_width = 1280
    config.screen_height = 720

define config.quicksave_slots = 6

init -999 python:
    def show_panic_screen_func():
        if persistent.unsafe_mode:
            config.window_title = "System Log"
            config.window_icon = "content/gfx/interface/icons/terminal.png"
            renpy.game.interface.set_icon()
            renpy.show_screen("panic_screen")
            renpy.restart_interaction()
    config.keymap['panic_screen'] = ['q', 'Q', 'й', 'Й']
    config.underlay.append(renpy.Keymap(panic_screen=show_panic_screen_func))

define config.window_icon = "content/gfx/interface/icons/win_icon.png"

define config.adjust_view_size = None

# Imagecache:
# define config.debug_image_cache = True
define config.image_cache_size_mb = 1000

init -5 python hide:
    config.console_history_size = 50
    ## This controls the title of the window, when Ren'Py is
    ## running in a window.
    config.window_title = "%s %s" % (config.name, config.version)

    # ----------------------------- Moved from initialization.rpy -------------------------------------->>>
    config.quit_action = Quit()
    if DEBUG:
        config.keymap['game_menu'] = ["K_ESCAPE"]
    else:
        config.keymap['game_menu'] = []
    # Fixing path:
    config.reject_backslash = False

    # disabling rollback as not being compatible with games nature
    config.rollback_enabled = False
    config.hard_rollback_limit = 0
    config.rollback_length = -1

    # Game may bug out on saving, in such case, comment should be removed
    # config.use_cpickle = False
    config.save_dump = False

    config.layers.append("tooltips")
    config.layers.append("pytfall")
    config.layers.append("panic")

    # getting rid of auto-saves
    config.has_autosave = False
    config.autosave_frequency = None
    config.autosave_on_choice = False
    config.autosave_on_quit = False

    # causes a really odd crash otherwise:
    # config.screenshot_callback = None

    # Lets see if we can establish json callback:
    def simple_save_dict(some_dict):
        if hasattr(store, "hero"):
            some_dict["name"] = hero.name
            some_dict["level"] = hero.level
            some_dict["chars"] = len(hero.chars)
            some_dict["gold"] = hero.gold
            some_dict["buildings"] = len(hero.buildings)
            try:
                img = hero.select_image(hero.id, "portrait")
                path = "/".join([hero.path_to_imgfolder, img])
                some_dict["portrait"] = path
            except:
                pass
    config.save_json_callbacks = [simple_save_dict]

    if not config.developer:
        # Hotkeys:
        # Stop right click menu:
        config.keymap["game_menu"] = None

    # Stop middle click hide menus
    config.keymap["hide_windows"] = None

    BLOCKED_LABELS = ["after_load", "save_screen",
                      "sort_items_for_gameplay",
                      "sort_traits_for_gameplay"]

    # Saves last label in a variable "last_label". Might be useful to jump back to from labels with multiple entry points.
    def label_callback(name, abnormal):
        store.last_label_pure = name

        if "pytfall" in globals():
            labels = _list(event.label for event in pytfall.world_events.events_cache)
        else:
            labels = _list()

        labels.extend(BLOCKED_LABELS)

        if not name.startswith("_") and name not in labels:
            store.last_label = name
    config.label_callback = label_callback
    # --------------- Ends Here ----------------------------------------------->>>

    # config.main_menu_music = "content/sfx/music/foregone.ogg"

    #########################################
    # Themes

    ## We then want to call a theme function. themes.roundrect is
    ## a theme that features the use of rounded rectangles. It's
    ## the only theme we currently support.
    ##
    ## The theme function takes a number of parameters that can
    ## customize the color scheme.

    theme.crayon(
        ## Theme: Crayon
        ## Color scheme: White Chocolate

        ## The color of an idle widget face.
        widget = "#33271C",

        ## The color of a focused widget face.
        widget_hover = "#ECE7C4",

        ## The color of the text in a widget.
        widget_text = "#B99D83",

        ## The color of the text in a selected widget. (For
        ## example, the current value of a preference.)
        widget_selected = "#ffffff",

        ## The color of a disabled widget face.
        disabled = "#614D3A",

        ## The color of disabled widget text.
        disabled_text = "#80654D",

        ## The color of informational labels.
        label = "#F1EBE5",

        ## The color of a frame containing widgets.
        frame = "#926841",

        ## The background of the main menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        # mm_root = ImageReference("humans"),

        ## The background of the game menu. This can be a color
        ## beginning with '#', or an image filename. The latter
        ## should take up the full height and width of the screen.
        gm_root = "content/gfx/bg/gallery.webp",

        ## If this is True, the in-game window is rounded. If False,
        ## the in-game window is square.
        rounded_window = False,

        ## And we're done with the theme. The theme will customize
        ## various styles, so if we want to change them, we should
        ## do so below.
        )

    # Fall back to defaults:
    # layout.defaults()
    #########################################
    ## This lets you change the placement of the main menu.

    ## The way placement works is that we find an anchor point
    ## inside a displayable, and a position (pos) point on the
    ## screen. We then place the displayable so the two points are
    ## at the same place.

    ## An anchor/pos can be given as an integer or a floating point
    ## number. If an integer, the number is interpreted as a number
    ## of pixels from the upper-left corner. If a floating point,
    ## the number is interpreted as a fraction of the size of the
    ## displayable or screen.

    ## The background of the game menu. This can be a color
    ## beginning with '#', or an image filename. The latter
    ## should take up the full height and width of the screen.

    #########################################
    ## These let you customize the default font used for text in Ren'Py.

    ## The file containing the default font.

    # style.default.font = "DejaVuSans.ttf"

    ## The default size of text.

    # style.default.size = 22

    ## Note that these only change the size of some of the text. Other
    ## buttons have their own styles.


    #########################################
    ## These settings let you change some of the sounds that are used by
    ## Ren'Py.

    ## Set this to False if the game does not have any sound effects.

    config.has_sound = True

    ## Set this to False if the game does not have any music.

    config.has_music = True

    ## Set this to True if the game has voicing.

    config.has_voice = False

    ## Sounds that are used when button and imagemaps are clicked.

    # style.button.activate_sound = "content/sfx/sound/sys/hover.mp3"
    # style.imagemap.activate_sound = "click.wav"

    ## Sounds that are used when entering and exiting the game menu.

    # config.enter_sound = "click.wav"
    # config.exit_sound = "content/sfx/sound/sys/close.mp3"

    ## A sample sound that can be played to check the sound volume.

    # config.sample_sound = "click.wav"

    ## Music that is played while the user is at the main menu.

    config.main_menu_music = "content/sfx/music/world/main menu.mp3"


    #########################################
    ## Help.

    ## This lets you configure the help option on the Ren'Py menus.
    ## It may be:
    ## - A label in the script, in which case that label is called to
    ##   show help to the user.
    ## - A file name relative to the base directory, which is opened in a
    ##   web browser.
    ## - None, to disable help.
    config.help = None

    # Adjust framerate:
    config.framerate = 90
    #########################################
    ## Transitions.

    ## Used when entering the game menu from the game.
    config.enter_transition = dissolve

    ## Used when exiting the game menu to the game.
    config.exit_transition = dissolve

    ## Used between screens of the game menu.
    config.intra_transition = dissolve

    ## Used when entering the game menu from the main menu.
    config.main_game_transition = dissolve

    ## Used when returning to the main menu from the game.
    config.game_main_transition = dissolve

    ## Used when entering the main menu from the splashscreen.
    config.end_splash_transition = dissolve

    ## Used when entering the main menu after the game has ended.
    config.end_game_transition = dissolve

    ## Used when a game is loaded.
    config.after_load_transition = dissolve

    ## Used when the window is shown.
    config.window_show_transition = dissolve

    ## Used when the window is hidden.
    config.window_hide_transition = dissolve

    ## Used when showing NVL-mode text directly after ADV-mode text.
    config.adv_nvl_transition = dissolve

    ## Used when showing ADV-mode text directly after NVL-mode text.
    config.nvl_adv_transition = dissolve

    ## Used when yesno is shown.
    config.enter_yesno_transition = dissolve

    ## Used when the yesno is hidden.
    config.exit_yesno_transition = dissolve

    ## Used when entering a replay
    config.enter_replay_transition = dissolve

    ## Used when exiting a replay
    config.exit_replay_transition = dissolve

    ## Used when the image is changed by a say statement with image attributes.
    config.say_attribute_transition = dissolve

init -1 python hide:
    #########################################
    ## Default values of Preferences.

    ## Note: These options are only evaluated the first time a
    ## game is run. To have them run a second time, delete
    ## game/saves/persistent

    ## Should we start in fullscreen mode?

    config.default_fullscreen = False

    ## The default text speed in characters per second. 0 is infinite.

    config.default_text_cps = 60

    ## The default auto-forward time setting.

    config.default_afm_time = 10

    #########################################
    ## More customizations can go here.



## This section contains information about how to build your project into
## distribution files.
init python:

    ## The name that's used for directories and archive files. For example, if
    ## this is 'mygame-1.0', the windows distribution will be in the
    ## directory 'mygame-1.0-win', in the 'mygame-1.0-win.zip' file.
    build.directory_name = "-".join([config.name, config.version.replace(" ", "-")])

    ## The name that's uses for executables - the program that users will run
    ## to start the game. For example, if this is 'mygame', then on Windows,
    ## users can click 'mygame.exe' to start the game.
    build.executable_name = config.name

    ## If True, Ren'Py will include update information into packages. This
    ## allows the updater to run.
    build.include_update = False

    ## File patterns:
    ##
    ## The following functions take file patterns. File patterns are case-
    ## insensitive, and matched against the path relative to the base
    ## directory, with and without a leading /. If multiple patterns match,
    ## the first is used.
    ##
    ##
    ## In a pattern:
    ##
    ## /
    ##     Is the directory separator.
    ## *
    ##     Matches all characters, except the directory separator.
    ## **
    ##     Matches all characters, including the directory separator.
    ##
    ## For example:
    ##
    ## *.txt
    ##     Matches txt files in the base directory.
    ## game/**.ogg
    ##     Matches ogg files in the game directory or any of its subdirectories.
    ## **.psd
    ##    Matches psd files anywhere in the project.

    ## Classify files as None to exclude them from the built distributions.

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.classify('**/chars/**', None)
    build.classify('**/rchars/**', None)
    build.classify('**/_old/**', None)
    build.classify('**devlog**', None)
    build.classify("game/cache/", None)
    build.classify("game/saves/", None)
    build.classify('game/00debug.rpy', None)
    # build.classify("game/**.rpy", None)
    build.classify("game/**.rpy_", None)

    ## To archive files, classify them as 'archive'.

    # build.classify('game/**.png', 'archive')
    # build.classify('game/**.jpg', 'archive')

    ## Files matching documentation patterns are duplicated in a mac app
    ## build, so they appear in both the app and the zip file.

    build.documentation('*.html')
    build.documentation('*.txt')
