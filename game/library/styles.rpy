# Well... better late than never :)
# My first ever style is created here!
# Neow!

init 998:
    #--------------------------------------- Groups:
    # DropDowns *Or Frames/Button sets:
    # Simple dropdown screen group
    style dropdown_frame:
        is default
        background Frame(Transform(im.Twocolor("content/gfx/frame/ink_box.png", white, aliceblue), alpha=0.5), 10, 10)
        xpadding 10
        ypadding 10
        
    style dropdown_text:
        is della_respira
        color black
        xalign 0.5
    
    style dropdown_button:
        background Transform(Frame(im.Twocolor("content/gfx/frame/cry_box.png", white, azure), 5, 5), alpha=0.8)
        hover_background Transform(Frame(im.MatrixColor(im.Twocolor("content/gfx/frame/cry_box.png", white, aquamarine), im.matrix.brightness(0.20)), 5, 5), alpha=0.8)
        insensitive_background Transform(Frame(im.Sepia("content/gfx/frame/cry_box.png"), 5, 5), alpha=0.8)
        size_group "dropdown"
        ypadding 5
        xalign 0
        
    style dropdown_button_text:
        is garamond
        line_leading -5
        color black
        size 18
        xalign 0
    
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
        is TisaOTM
        color black
        size 18
        align (0.5, 0.5)
        
    # 2 # dropdown
        
    style dropdown_gm2_button:
        is basic_choice2_button
        
    style dropdown_gm2_button_text:
        is TisaOTM
        drop_shadow [(1, 1)]
        drop_shadow_color black
        color "#EEE8CD"
        insensitive_color "#808069" # warmgrey
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
        
    # Main Menu
        
    style mmenu_button:
        is mmenu1_button
        ypadding 5
        xsize 170
        
    style mmenu_button_text:
        is TisaOTM
        color "#66CDAA"
        hover_color "#CDC673"
        outlines [(1, "#3a3a3a", 0, 0)]
        hover_outlines [(1, "#3a3a3a", 0, 0)]
        selected_idle_color "#CDC673"
        selected_hover_color "#CDC673"
        insensitive_color "#808069"
        size 18
        align (0.5, 0.5)
        
    # smenu
        
    style smenu_button:
        is smenu1_button
        xysize (134, 44)
        
    # Same as above, just without size_group
    style basic_button:
        is basic_choice_button
        ypadding 1
        
    style basic_button_text:
        is TisaOTM
        color black
        size 18
        align (0.5, 0.5)
        
    style basic_text:
        is TisaOTM
        color black
        hover_color red
        outlines [(1, "#aaa697", 0, 0)]
        hover_outlines [(1, "#3a3a3a", 0, 0)]
        size 18
        align (0.5, 0.5)
        
    # Interactions:
    style interactions_text:
        is TisaOTM
        drop_shadow [(1, 1)]
        drop_shadow_color black
        color "#7FFFD4"
        hover_color "#D2691E"
        size 20
        
    style interactions_text1:
        is TisaOTM
        drop_shadow [(1, 1)]
        drop_shadow_color black
        color "#c8ffff"
        #hover_color "#D2691E"
        size 20
        
    style interactions_button:
        is chat_button
        xpadding 0
        ypadding -10
        
    # This is the main style we'll use for normal content in the game (only the button for now)
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
        
    # Style for stats
    style stats_frame:
        is frame
        xysize (307, 31)
        background Frame("content/gfx/frame/stat_box.png", 5, 5)
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
    
    # Style for profile buttons "pb"
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
    
init -2:
    # Frames:
    style alt_frame:
        is default
        
    style alt_frame_frame:
        is frame
        background Frame(im.Twocolor("content/gfx/frame/cry_box.png", "#d65f4c", "#a64a3b"), 5, 5)
        
    style inter_frame:
        is default
        background Frame(Transform(im.Twocolor("content/gfx/frame/window_frame.png", black, white), alpha=0.5), 30, 30)
        xpadding 10
        ypadding 10
    
    # ----------------------------------- Buttons:
        
    style flashing:
        activate_sound "content/sfx/sound/sys/click_1.ogg"
        #hover_sound "content/sfx/sound/sys/hover.mp3"
        idle_background None
        selected_background None
        insensitive_background None
        hover_background flashing ("#0390fc")
        selected_hover_background flashing ("#0390fc")
        
    style ddlist_button:
        # Simple button we use to call the dropdowns
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
        
    style mmenu1_button:
        take flashing
        background Frame ("content/gfx/interface/buttons/main1.png", 5, 5)
        hover_background  Fixed(Frame("content/gfx/interface/buttons/main1.png", 5, 5),
            flashing(Frame("content/gfx/interface/buttons/flashing2.png", 5, 5)))
        
    style smenu1_button:
        take flashing
        background Frame("content/gfx/interface/buttons/s_menu1.png", 5, 5)
        hover_background  Fixed(Frame("content/gfx/interface/buttons/s_menu1.png", 5, 5),
                                                  flashing(Frame("content/gfx/interface/buttons/flashing2.png", 5, 5)))
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/s_menu1.png"), 5, 5)
        
    style hframe_button:
        take flashing
        background Frame("content/gfx/interface/buttons/hp_1s.png", 5, 5)
        hover_background  Fixed(Frame("content/gfx/interface/buttons/hp_1s.png", 5, 5),
                                                  flashing(Frame("content/gfx/interface/buttons/flashing2.png", 5, 5)))
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/hp_1s.png"), 5, 5)
        
    style smenu2_button:
        background Frame ("content/gfx/interface/buttons/s_menu2.png", 5, 5)
        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/s_menu2h.png", im.matrix.brightness(0.19)), 5, 5)
        selected_idle_background Frame(Transform("content/gfx/interface/buttons/choice_buttons2s.png", alpha=1.12), 5, 5)
        selected_hover_background Frame(Transform("content/gfx/interface/buttons/choice_buttons2s.png", alpha=1.32), 5, 5)
        
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
        
    style chat_button:
        is button
        idle_background Transform(Frame("content/gfx/interface/buttons/chat.png", 5, 5), alpha=0.8)
        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/chat.png", im.matrix.brightness(0.15)), 5, 5)
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/chat.png"), 5, 5)
        
    style beveled_glass_button:
        background Transform(Frame("content/gfx/interface/buttons/beveled_glass.png", 5, 5), alpha=0.9)
        hover_background Transform(Frame(im.MatrixColor("content/gfx/interface/buttons/beveled_glass.png", im.matrix.brightness(0.15)), 5, 5), alpha=0.9)
        xpadding 6
        ypadding 4
        
    style vista_button:
        background Transform(Frame("content/gfx/interface/buttons/vista_button.png", 5, 5), alpha=0.7)
        hover_background Transform(Frame(im.MatrixColor("content/gfx/interface/buttons/vista_button.png", im.matrix.brightness(0.15)), 5, 5), alpha=0.7)
        insensitive_background Transform(Frame(im.Sepia("content/gfx/interface/buttons/vista_button.png"), 5, 5), alpha=0.7)
        xpadding 8
        ypadding 6
        
    style white_cry_button:
        background Transform(Frame(im.Twocolor("content/gfx/frame/cry_box.png", white, white), 5, 5), alpha=0.8)
        hover_background Transform(Frame(im.MatrixColor(im.Twocolor("content/gfx/frame/cry_box.png", white, aquamarine), im.matrix.brightness(0.20)), 5, 5), alpha=0.8)
        insensitive_background Transform(Frame(im.Sepia("content/gfx/frame/cry_box.png"), 5, 5), alpha=0.8)
        ypadding 3
        
    style marbleG_button:
        is button
        idle_background Frame("content/gfx/interface/buttons/marbleG_button.png", 5, 5)
        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/marbleG_button.png", im.matrix.brightness(0.15)), 5, 5)
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/marbleG_button.png"), 5, 5)
        
    style blue1:
        is button
        idle_background Frame("content/gfx/interface/buttons/blue3.png", 5, 5)
        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/blue3.png", im.matrix.brightness(0.15)), 5, 5)
        idle_foreground Frame("content/gfx/interface/buttons/f1.png", 5, 5)
        hover_foreground Frame(im.MatrixColor("content/gfx/interface/buttons/f1.png", im.matrix.brightness(0.07)), 5, 5)
        
    style op1:
        is button
        idle_background Frame("content/gfx/interface/buttons/op3.png", 5, 5)
        hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/op3.png", im.matrix.brightness(0.15)), 5, 5)
        idle_foreground Frame("content/gfx/interface/buttons/f1.png", 5, 5)
        hover_foreground Frame("content/gfx/interface/buttons/f1.png", 5, 5)
        
    style chat_textbox:
        is button
        idle_background Frame("content/gfx/frame/chat_text_box2.png", 5, 5)
        hover_background Frame(im.MatrixColor("content/gfx/frame/chat_text_box2.png", im.matrix.brightness(0.15)), 5, 5)
        insensitive_background Frame(im.Sepia("content/gfx/frame/chat_text_box2.png"), 5, 5)
        
    # ----
    # Cutsomized to specific screens from default choices:
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
        
        insensitive_background Frame(im.Sepia("content/gfx/interface/buttons/blue3.png"), 5, 5)
        insensitive_foreground Frame("content/gfx/interface/buttons/f1.png", 5, 5)
        
        selected_idle_background Frame(im.MatrixColor("content/gfx/interface/buttons/blue3.png", im.matrix.tint(0.6, 0.6, 0.6)), 5, 5)
        selected_idle_foreground Frame("content/gfx/interface/buttons/f1.png", 5, 5)
        
        selected_hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/blue3.png", im.matrix.tint(0.6, 0.6, 0.6) * im.matrix.brightness(0.15)), 5, 5)
        selected_hover_foreground Frame(im.MatrixColor("content/gfx/interface/buttons/f1.png", im.matrix.brightness(0.07)), 5, 5)
    
    style main_screen_3_button_text:
        is TisaOTB
        xalign 0.5
        size 20
        drop_shadow [(1, 1)]
        color azure
        
    style main_screen_4_button:
        is op1
        xminimum 200
        xpadding 20
        ypadding 10
        activate_sound "content/sfx/sound/sys/hover_2.wav"
        
    style main_screen_4_button_text:
        is TisaOTB
        xalign 0.5
        size 20
        drop_shadow [(1, 1)]
        color azure
        

    style sound_button:
        subpixel True
        idle_background Frame(im.Sepia("content/gfx/interface/buttons/sound_icon.png"), 5, 5)
        hover_background Frame(im.MatrixColor(im.Sepia("content/gfx/interface/buttons/sound_icon.png"), im.matrix.brightness(0.15)), 5, 5)
        selected_idle_background Frame("content/gfx/interface/buttons/sound_icon.png", 5, 5)
        selected_hover_background Frame(im.MatrixColor("content/gfx/interface/buttons/sound_icon.png", im.matrix.brightness(0.15)), 5, 5)
        
    style white_cry_button_text:
        is text
        xalign 0
        size 12
        bold True
        color black
        
    # ---------------------------------- Text:
    # Base Fonts (*Just the fontname):
    style garamond:
        is text
        antialias True
        font "fonts/EBGaramond-Regular.ttf"
        
    style tisa_otm:
        is text
        font "fonts/TisaOTM.otf"
        
    style della_respira:
        is text
        antialias True
        font "fonts/dellarespira-regular.ttf"
        
    style myriadpro_reg:
        is text
        font "fonts/myriadpro-regular.otf"
        
    style myriadpro_sb:
        is text
        font "fonts/myriadpro-semibold.otf"
    
    # Specialized text styles:
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
        align (0.5, 0.5)
        
    style TisaOTM:
        is tisa_otm
        font "fonts/TisaOTM.otf"
        align (0.5, 0.5)
        
    style TisaOTB is text:
        size 20
        font "fonts/TisaOTB.otf"
        align (0.5, 0.5)
        
    style credits_text:
        font "fonts/rubius.ttf"
        antialias True
        line_spacing 6
        color azure
        
init: # Ren'Py Styles:
    ## FRAMEWORK FOR DIALOGUE
    ## Main (Say) window
    style window is default:
        background Frame("content/gfx/frame/frameD.png", 50, 50)
        xpos 640
        xfill True
        xmargin 0
        left_padding 205
        right_padding 75
        #xpadding 210
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
    style say_thought is default:
        font "fonts/TisaOTM.otf"
        size 18
        drop_shadow [(2, 2)]
    
    ## Dialogue two_window text
    style say_dialogue is default:
        font  "fonts/TisaOTM.otf"
        size 18
        drop_shadow [(2, 2)]
    
    style say_label:
        font "fonts/TisaOTM.otf"
        bold False
        size 18
        xalign 0.5
        yalign 0.5
        
        
    # Yes/No Prompt
    # style yesno_frame:
        # is dropdown_gm_frame
        
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
        
        
    # Main Menu:
    style mm_frame:
        is default
        background Frame(Transform(im.Twocolor("content/gfx/frame/window_frame.png", white, purple), alpha=0.5), 30, 30)
        xpadding 10
        ypadding 10
        
    style mm_button:
        is marbleG_button
        xpadding 34
        ypadding 20
        size_group "mm"
        
    style mm_button_text:
        is TisaOTB
        size 22
        color "#1C1C1C"
        drop_shadow [(1, 1)]
        drop_shadow_color grey
        
        
    # Preferences:
    style pref_frame:
        is inter_frame
        xfill True
        xmargin 5
        top_margin 5
        
    style pref_label_text:
        is agrevue
        size 17
        drop_shadow [(1, 1)]
        drop_shadow_color grey
        
    style pref_vbox:
        xfill True
        
    style pref_button:
        size_group "pref"
        is vista_button
        xalign 1.0
        
    style pref_button_text:
        is myriadpro_sb
        align (0.5, 0.65)
        drop_shadow [(1, 1)]
        drop_shadow_color grey
        selected_color crimson
        insensitive_color "#808069"
        
    style pref_slider:
        is bar
        left_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_full.png", 192, 20), black, white)
        right_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_empty.png", 192, 20), black, white)
        hover_left_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_full.png", 192, 20), white, crimson)
        hover_right_bar im.Twocolor(im.Scale("content/gfx/interface/bars/cryslider_empty.png", 192, 20), white, crimson)
        thumb None
        hover_thumb None
        xmaximum 192
        xalign 1.0
        
    style soundtest_button:
        xalign 1.0
    
        
    # Save/Load:
    style file_picker_frame:
        is inter_frame
        
    style file_picker_nav_button:
        is vista_button
        
    style file_picker_nav_button_text:
        is agrevue
        size 10
        
    style file_picker_button:
        is vista_button
        
    style file_picker_text:
        is agrevue
        size 15
        
        
    # Menu:
    style menu_window is default

    style menu_choice is interactions_text1:
        clear

    style menu_choice_button is chat_textbox:
        xminimum int(config.screen_width * 0.10)
        xmaximum int(config.screen_width * 0.80)
        xpadding 50
        size_group "choice_menu"
        background Frame("content/gfx/frame/chat_text_box_idle.png", 5, 5)
        hover_background Transform(Frame("content/gfx/frame/chat_text_box_hover.png", 5, 5), xzoom=1.07, yzoom=1.5, align=(0.5, 0.5))
        ysize 29
        
    style menu_choice_button_blue is menu_choice_button:
        background Frame(im.Twocolor("content/gfx/frame/chat_text_box_idle.png", white, blue), 5, 5)
        hover_background Transform(Frame(im.Twocolor("content/gfx/frame/chat_text_box_hover.png", white, blue), 5, 5), xzoom=1.07, yzoom=1.5, align=(0.5, 0.5))
        
    # Quickbuttons:
    style quick_button:
        is default
        background None
        xpadding 5

    style quick_button_text:
        is default
        size 14
        idle_color "#8888"
        hover_color "#ccc"
        selected_idle_color "#cc08"
        selected_hover_color "#cc0"
        insensitive_color "#4448"    
        
    # Navigation:
    style gm_nav_button:
        is beveled_glass_button
        size_group "gm_nav"
        
    style gm_nav_button_text:
        is black_serpent
        drop_shadow [(1, 1)]
        drop_shadow_color grey
        selected_color crimson
        insensitive_color grey 
        
    style gm_nav_frame:
        is inter_frame


