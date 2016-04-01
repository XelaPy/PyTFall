init -3 python:
    # We create a font group to resolve rare characters in pretty fonts so we can use both at the same time.
    tisa_otm_adv = FontGroup().add("fonts/DejaVuSans.ttf", 0x00A0, 0xE007F).add("fonts/TisaOTM.otf", 0x0020, 0x007f)
    # tisa_otb_adv = FontGroup().add("fonts/", 0x00A0, 0xE007F).add("fonts/TisaOTB.otf", 0x0020, 0x007f)

# Well... better late than never :)
# My first ever style is created here!
# Neow!
init -3:
    # Style resets:
    style say_label:
        clear
     
    # style window:
        # clear
         
    # style frame:
        # clear
     
    # style say_vbox:
        # clear
     
    # style say_who_window:
        # clear
     
    # style say_two_window_vbox:
        # clear
     
    # style menu_choice:
        # clear
     
    # style input:
        # clear
     
    # style hyperlink_text:
        # clear
     
    # style button:
        # clear
     
    # style button_text:
        # clear

init -2: # Base Styles like Texts and Buttons just with the basic properties.
    # ----------------------------------- Buttons:
    style flashing:
        activate_sound "content/sfx/sound/sys/click_1.ogg"
        # hover_sound "content/sfx/sound/sys/hover.mp3"
        idle_background None
        selected_background None
        insensitive_background None
        hover_background flashing("#0390fc")
        selected_hover_background flashing("#0390fc")
        
    # Simple button we use to call the dropdowns:
    # This is a really basic, stipped down button.
    style ddlist_button:
        is button
        left_padding -2
        background Null()
    style ddlist_text:
        is garamond
        yalign 0
        line_leading -3
        idle_color ivory
        hover_color red
        size 17
    
    # Master Styles of the GREY and BROWNish buttons we use all over the place. 
    style basic_choice_button:
        background Frame("content/gfx/interface/buttons/choice_buttons1.png", 10, 10)
        hover_background Frame("content/gfx/interface/buttons/choice_buttons1h.png", 10, 10)
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/choice_buttons1.png"), 10, 10)
        selected_idle_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons1.png", im.matrix.tint(1, 0.75, 0.75)), 10, 10)
        selected_hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons1h.png", im.matrix.tint(0.75, 0.75, 1)), 10, 10)
    
    style basic_choice2_button:
        background Frame("content/gfx/interface/buttons/choice_buttons2.png", 5, 5)
        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/choice_buttons2h.png", im.matrix.brightness(0.15)), 5, 5)
        selected_idle_background Frame(Transform("content/gfx/interface/buttons/choice_buttons2s.png", alpha=1.12), 5, 5)
        selected_hover_background Frame(Transform("content/gfx/interface/buttons/choice_buttons2s.png", alpha=1.32), 5, 5)
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/choice_buttons2.png"), 5, 5)
        
    # Presently used in Main Menu.
    style mmenu1_button:
        take flashing
        background Frame ("content/gfx/interface/buttons/main1.png", 5, 5)
        hover_background  Fixed(Frame("content/gfx/interface/buttons/main1.png", 5, 5),
                                                  flashing(Frame("content/gfx/interface/buttons/flashing2.png", 5, 5)))
        
    # Parent for the new MM button.
    style smenu1_button:
        take flashing
        background Frame("content/gfx/interface/buttons/s_menu1.png", 5, 5)
        hover_background  Fixed(Frame("content/gfx/interface/buttons/s_menu1.png", 5, 5),
                                                  flashing(Frame("content/gfx/interface/buttons/flashing2.png", 5, 5)))
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/s_menu1.png"), 5, 5)
        
    # Parent for the cool buttons in MCs Profile.
    style hframe_button:
        take flashing
        background Frame("content/gfx/interface/buttons/hp_1s.png", 5, 5)
        hover_background  Fixed(Frame("content/gfx/interface/buttons/hp_1s.png", 5, 5),
                                                  flashing(Frame("content/gfx/interface/buttons/flashing2.png", 5, 5)))
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/hp_1s.png"), 5, 5)
        
    # Black button with a thin outlines, not used anywhere.
    style smenu2_button:
        background Frame ("content/gfx/interface/buttons/s_menu2.png", 5, 5)
        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/s_menu2h.png", im.matrix.brightness(0.19)), 5, 5)
        selected_idle_background Frame(Transform("content/gfx/interface/buttons/choice_buttons2s.png", alpha=1.12), 5, 5)
        selected_hover_background Frame(Transform("content/gfx/interface/buttons/choice_buttons2s.png", alpha=1.32), 5, 5)
        
    # Based Wooden buttons we inherited from WM Wood Skin.
    style wood_button:
        is button
        idle_background Frame("content/gfx/interface/buttons/idle_wood.png", 5, 5)
        hover_background Frame("content/gfx/interface/buttons/hover_wood.png", 5, 5)
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/idle_wood.png"), 5, 5)
        hover_sound "content/sfx/sound/sys/hover_2.wav"
        
    style left_wood_button:
        is button
        idle_background Frame("content/gfx/interface/buttons/button_wood_left_idle.png", 5, 5)
        hover_background Frame("content/gfx/interface/buttons/button_wood_left_hover.png", 5, 5)
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/button_wood_left_idle.png"), 5, 5)
        hover_sound "content/sfx/sound/sys/hover_2.wav"
        
    style right_wood_button:
        is button
        idle_background Frame("content/gfx/interface/buttons/button_wood_right_idle.png", 5, 5)
        hover_background Frame("content/gfx/interface/buttons/button_wood_right_hover.png", 5, 5)
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/button_wood_right_idle.png"), 5, 5)
        hover_sound "content/sfx/sound/sys/hover_2.wav"
        
    style wood_text:
        align (0.5, 0.5)
        size 14
        color ivory
        hover_color red
        
    # This is a simple white, semi transparrent button, prolly should be deleted.
    style white_cry_button:
        background Transform(Frame(im.Twocolor("content/gfx/frame/cry_box.png", white, white), 5, 5), alpha=0.8)
        hover_background Transform(Frame(im.MatrixColor(im.Twocolor("content/gfx/frame/cry_box.png", white, aquamarine), im.matrix.brightness(0.20)), 5, 5), alpha=0.8)
        insensitive_background Transform(Frame(im.Sepia("content/gfx/frame/cry_box.png"), 5, 5), alpha=0.8)
        ypadding 3
        
    # Parent of the Gismo's Blue Marble button that was used in Main Menu Screen for a while.
    style marbleG_button:
        is button
        idle_background Frame("content/gfx/interface/buttons/marbleG_button.png", 5, 5)
        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/marbleG_button.png", im.matrix.brightness(0.15)), 5, 5)
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/marbleG_button.png"), 5, 5)
        
    # Cool Blue button we use in a number of places (Main Screen that leads to Buildings/GL for example)
    style blue1:
        is button
        idle_background Frame("content/gfx/interface/buttons/blue3.png", 5, 5)
        idle_foreground Frame("content/gfx/interface/buttons/f1.png", 5, 5)
        
        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/blue3.png", im.matrix.brightness(0.15)), 5, 5)
        hover_foreground Frame(im.MatrixColor("content/gfx/interface/buttons/f1.png", im.matrix.brightness(0.07)), 5, 5)
        
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/blue3.png"), 5, 5)
        insensitive_foreground Frame("content/gfx/interface/buttons/f1.png", 5, 5)
        
        selected_idle_background Frame(im.MatrixColor("content/gfx/interface/buttons/blue3.png", im.matrix.tint(0.6, 0.6, 0.6)), 5, 5)
        selected_idle_foreground Frame("content/gfx/interface/buttons/f1.png", 5, 5)
        
        selected_hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/blue3.png", im.matrix.tint(0.6, 0.6, 0.6) * im.matrix.brightness(0.15)), 5, 5)
        selected_hover_foreground Frame(im.MatrixColor("content/gfx/interface/buttons/f1.png", im.matrix.brightness(0.07)), 5, 5)
        
    # Decent Wooden button, Used as a ND.
    style op1:
        is button
        idle_background Frame("content/gfx/interface/buttons/op3.png", 5, 5)
        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/op3.png", im.matrix.brightness(0.15)), 5, 5)
        idle_foreground Frame("content/gfx/interface/buttons/f1.png", 5, 5)
        hover_foreground Frame("content/gfx/interface/buttons/f1.png", 5, 5)
        
    # ---------------------------------- Text:
    # Base Fonts (*Just the fontname/alignment):
    style garamond:
        is text
        antialias True # Text in modern Ren'Py is always aa rendered?
        font "fonts/EBGaramond-Regular.ttf"
        
    style TisaOTM:
        is text
        font tisa_otm_adv
        
    style della_respira:
        is text
        antialias True # Text in modern Ren'Py is always aa rendered?
        font "fonts/dellarespira-regular.ttf"
        
    style myriadpro_reg:
        is text
        font "fonts/myriadpro-regular.otf"
        
    style myriadpro_sb:
        is text
        font "fonts/myriadpro-semibold.otf"
    
    style earthkid is text:
        size 20
        font "fonts/earthkid.ttf"
        align (0.5, 0.5)
        
    style agrevue is text:
        size 20
        font "fonts/agrevue.ttf"
        align (0.5, 0.5)
        
    style rubius is text:
        size 20
        font "fonts/rubius.ttf"
        align (0.5, 0.5)
        
    style TisaSansOT is text:
        size 20
        font "fonts/TisaSansOT.otf"
        
    style TisaOTB:
        is text
        size 20
        font "fonts/TisaOTB.otf"
        
    style TisaOTBc:
        is TisaOTB
        align (0.5, 0.5)
        
    style TisaOTMc:
        is TisaOTM
        align (0.5, 0.5)
        
        
init 2: # Advanced style that can carry a lot of properies to be used in screens/labels.
    # ----
    # Cutsomized to specific screens from default choices:
    # Default dropdown/interactions and etc.
    style dropdown_gm_frame:
        is default
        background Frame("content/gfx/frame/BG_choicebuttons.png", 10, 10)
        xpadding 10
        ypadding 10
        
    style dropdown_gm_text:
        is black_serpent
        xalign 0.5
        
    style dropdown_gm_button:
        is basic_choice_button
        size_group "dropdown_gm"
        ypadding 1
        xalign 0
        
    style dropdown_gm_button_text:
        is TisaOTMc
        color black
        size 18
        
    # Second set of DD buttons:
    style dropdown_gm2_button:
        is basic_choice2_button
        
    style dropdown_gm2_button_text:
        is TisaOTMc
        drop_shadow [(1, 1)]
        drop_shadow_color black
        color "#EEE8CD"
        insensitive_color "#808069"
        size 16
        outlines [(1, "#3a3a3a", 0, 0)]
        selected_outlines [(1, "#8B3E2F", 0, 0)]
    
    style dropdown_gm2_button_value_text:
        is della_respira
        color "#EEE8CD"
        size 16
        outlines [(1, "#3a3a3a", 0, 0)]
        selected_outlines [(1, "#8B3E2F", 0, 0)]
        
    style dropdown_gm2_slider:
        is bar
        left_bar im.Scale("content/gfx/interface/bars/pref_full.png", 166, 21)
        right_bar im.Scale("content/gfx/interface/bars/pref_empty.png", 166, 21)
        hover_left_bar im.Scale("content/gfx/interface/bars/pref_full.png", 166, 21)
        hover_right_bar im.Scale("content/gfx/interface/bars/pref_empty.png", 166, 21)
        thumb None #im.Scale("content/gfx/interface/bars/pref_thumb.png", 18, 21)
        hover_thumb  None #im.Scale("content/gfx/interface/bars/pref_thumb.png", 18, 21)
        xmaximum 166
        align (0.5, 0.5)
        
    # One of the most widely used styles in the game:
    # These are Gismo's Grey Button style we use all over the place.
    style basic_button:
        is basic_choice_button
        ypadding 1
        
    style basic_button_text:
        is TisaOTMc
        color black
        size 18
        
    style basic_text:
        is TisaOTMc
        color black
        hover_color red
        outlines [(1, "#aaa697", 0, 0)]
        hover_outlines [(1, "#3a3a3a", 0, 0)]
        size 18
        
    # Interactions:
    style interactions_text:
        is TisaOTMc
        drop_shadow [(1, 1)]
        drop_shadow_color black
        color "#c8ffff"
        # hover_color "#D2691E"
        size 20
        
    # This is the main style we'll use for normal content in the game (only the button for now).
    # Basically holds the two of the five fonts used in the game.
    style content:
        is default
    style content_text:
        is garamond
        line_leading -5
        size 17
        color black
    style content_label_text:
        is della_respira
        size 19
        color black
        
    # Style used for Stats.
    style base_stats_frame: # This one is presently used in the equipment screen. It overrides silly theme settings to allow for a better positioning and more convinient use.
        left_padding 9
        right_padding 11
        top_padding 4
        bottom_padding 1
        xmargin 0
        ymargin 0
    
    style stats_frame:
        is frame
        xysize (307, 31)
        background Frame("content/gfx/frame/stat_box.png", 1, 1)
    style stats_text:
        is garamond
        color ivory
        outlines [(1, "#3a3a3a", 0, 0)]
        size 18
    style stats_label_text:
        is della_respira
        outlines [(2, "#424242", 0, 0)]
        size 19
        color ivory
    style stats_value_text:
        is della_respira
        outlines [(1, "#3a3a3a", 0, 0)]
        size 14
        color ivory
        
    style proper_stats_frame:
        is frame
        xpadding 0
        ypadding 0
        xmargin 0
        ymargin 0
        background Frame("content/gfx/frame/stat_box_proper.png", 5, 5)
    style proper_stats_text:
        is stats_text
    style proper_stats_label_text:
        is stats_label_text
    style proper_stats_value_text:
        is stats_value_text
    
    # Style for profile buttons "pb"
    # Pretty and advanced style used in Heros Profile:
    style pb_button:
        is hframe_button
        xysize (60, 30)
    style pb_button_text:
        font "fonts/rubius.ttf"
        size 17
        idle_color "#CDCDC1"
        hover_color "#F5F5DC"
        selected_idle_color "#CDAD00"
        selected_hover_color "#CDAD00"
        xalign 0.5
        ypos 15
    
    # Notifications:
    style notify_bubble:
        is default
    style notify_bubble_frame:
        background "#000"
        minimum (350, 15)
    style notify_bubble_vbox:
        xfill True
    style notify_bubble_text:
        is garamond
        line_leading -5
        size 15
        align (0.5, 0.5)
    
    # MC Setup Screen:
    style mcsetup_button:
        is button
        xysize (175, 51)
        idle_background Frame("content/gfx/interface/images/story12.png", 1, 1)
        hover_background Frame(im.MatrixColor("content/gfx/interface/images/story12.png", im.matrix.brightness(0.1)), 1, 1)
        insensitive_background Frame(im.Sepia("content/gfx/interface/images/story12.png"), 1, 1)
        
    style mcsetup_text:
        is text
        size 16
        font "fonts/TisaOTm.otf"
        color ivory
        hover_color red
        selected_color green
        insensitive_color "#808069"
        
    style sqstory_button:
        is button
        background Frame("content/gfx/frame/cry_box.png", 10, 10)
        xysize (60, 60)
        
    # Interactions are presently using these:
    style main_screen_3_frame:
        # This is for girlsmeets:
        is frame
        background Null()
    
    style main_screen_3_button:
        is blue1
        xalign 0.5
        xminimum 180
        xpadding 20
        ypadding 8
        activate_sound "content/sfx/sound/sys/hover_2.wav"
    
    style main_screen_3_button_text:
        is TisaOTBc
        size 20
        drop_shadow [(1, 1)]
        color azure
        
    # Used mainly as Next Day Button
    style main_screen_4_button:
        is op1
        xminimum 200
        xpadding 20
        ypadding 10
        activate_sound "content/sfx/sound/sys/hover_2.wav"
        
    style main_screen_4_button_text:
        is TisaOTBc
        size 20
        drop_shadow [(1, 1)]
        color azure
        
    # Sound button...
    style sound_button:
        subpixel True
        idle_background Frame(im.Sepia("content/gfx/interface/buttons/sound_icon.png"), 5, 5)
        hover_background Frame(im.MatrixColor(im.Sepia("content/gfx/interface/buttons/sound_icon.png"), im.matrix.brightness(0.15)), 5, 5)
        selected_idle_background Frame("content/gfx/interface/buttons/sound_icon.png", 5, 5)
        selected_hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/sound_icon.png", im.matrix.brightness(0.15)), 5, 5)
        
    # Specialized text styles: ===============>
    style TisaOTMol:
        is TisaOTM
        color "#ecc88a"
        size 14
        outlines [(1, "#3a3a3a", 0, 0)]
    
    style TisaOTMolxm: # With outlines:
        is TisaOTMol
        xalign 0.5
        size 17
        
    style library_book_header_main:
        is della_respira
        color black
        xalign 0.5
        bold True
        size 20
        
    style library_book_header_sub:
        is library_book_header_main
        size 18
        
    style library_book_content:
        is garamond
        color black
        size 15
    
    style black_serpent:
        is text
        size 20
        font "fonts/serpentn.ttf"
        color black
        align (0.5, 0.5)
        
    style next_day_summary_text is text:
        size 16
        font "fonts/agrevue.ttf"
        color black
        
    style credits_text:
        font "fonts/rubius.ttf"
        antialias True
        line_spacing 6
        color azure
        
    # Text that goes with the wc button.
    style white_cry_button_text:
        is text
        xalign 0
        size 12
        bold True
        color black
        
    style arena_header_text:
        is garamond
        color red
        size 35
        outlines [(3, "#3a3a3a", 1, 1)]
        drop_shadow [(2, 3)]
        drop_shadow_color black

init: # Ren'Py Styles (Or replacements):
    ## FRAMEWORK FOR DIALOGUE
    ## Main (Say) window
    style window is default:
        background Frame("content/gfx/frame/frameD.png", 50, 50)
        xpos 640
        xfill True
        xmargin 0
        left_padding 205
        right_padding 75
        # xpadding 210
        ypadding 10
        yfill False
        ymargin 0
        yminimum 156
        xmaximum 1100
    
    ## Name two_window Box
    style say_who_window is default:
        background Frame("content/gfx/frame/Namebox.png", 25, 25)
        yalign 1.0
        pos (165, 38)
        xpadding 3
        ypadding 2
        minimum (115, 28)
    
    ## Dialogue main window text
    style say_thought:
        is TisaOTM
        size 18
        drop_shadow [(2, 2)]
    
    ## Dialogue two_window text
    style say_dialogue:
        is TisaOTM
        size 18
        drop_shadow [(2, 2)]
    
    style say_label:
        is TisaOTMc
        bold False
        size 18
        
    # Yes/No Prompt:
    style yesno_button:
        is dropdown_gm_button
        xpadding 7
        ypadding 5
        size_group "yesno"
        
    style yesno_button_text:
        is agrevue
        color black

    style yesno_label_text:
        is content_text
        text_align 0.5
        size 23
        bold True
        layout "subtitle"
        
    # # Choice Menu:
    style menu_window is default 
    style menu_choice is interactions_text:
        clear

    style menu_choice_button:
        is button
        xminimum int(config.screen_width * 0.10)
        xmaximum int(config.screen_width * 0.80)
        xpadding 50
        size_group "choice_menu"
        background Frame("content/gfx/frame/chat_text_box_idle.png", 5, 5)
        hover_background Transform(Frame("content/gfx/frame/chat_text_box_hover.png", 5, 5), xzoom=1.07, yzoom=1.5, align=(0.5, 0.5))
        insensitive_background Frame(im.Sepia("content/gfx/frame/chat_text_box_idle.png"), 5, 5)
        ysize 29
        
    style menu_choice_button_blue is menu_choice_button:
        background Frame(im.Twocolor("content/gfx/frame/chat_text_box_idle.png", white, blue), 5, 5)
        hover_background Transform(Frame(im.Twocolor("content/gfx/frame/chat_text_box_hover.png", white, blue), 5, 5), xzoom=1.07, yzoom=1.5, align=(0.5, 0.5))
        
    # Main Menu and Preferences:
    # Gismo's New MM Version!
    style mmenu_button:
        is mmenu1_button
        ypadding 5
        xsize 170
        
    style mmenu_button_text:
        is smenu_text
    
    style smenu_button:
        is smenu1_button
        xysize (134, 44)
        
    style smenu_text:
        is TisaOTMc
        color "#66CDAA"
        hover_color "#CDC673"
        outlines [(1, "#3a3a3a", 0, 0)]
        hover_outlines [(1, "#3a3a3a", 0, 0)]
        selected_idle_color "#CDC673"
        selected_hover_color "#CDC673"
        insensitive_color "#808069"
        size 18
