init python:
    training_screen_current = None
    training_screen_course = None
    training_screen_trainer = None
    
    # Done as action to allow for easy sensitivity detection
    class TrainingSwitchAction(Action):
        
        def __init__(self, current):
            self.current = current
        
        def __call__(self):
            global training_screen_current
            global training_screen_course
            
            training_screen_current = schools[self.current]
            training_screen_course = None
            
            renpy.restart_interaction()
        
        def get_sensitive(self):
            return training_screen_current != schools[self.current]
    

label girl_training:
    show screen girl_training
    with dissolve
    
    python:
        # Ensure valid school
        if training_screen_current is None:
            for i in schools:
                if schools[i].available:
                    training_screen_current = schools[i]
                    break
        
        # Ensure valid trainer
        if training_screen_trainer is None:
            training_screen_trainer = hero
        
        # Ensure valid course if selected
        if training_screen_course is not None:
            if not training_screen_course.can_train(char, training_screen_trainer):
                training_screen_course = None
        
        while True:
            result = ui.interact()
            
            if result[0] == "trainer":
                training_screen_trainer = result[1]
            
            elif result[0] == "open":
                training_screen_course = result[1]
            
            elif result[0] == "setto":
                # Schooling
                if training_screen_current.is_school:
                    # Slave and combat incompatibility
                    if char.status == "slave" and result[1].type == "Combat":
                        renpy.call_screen("message_screen", "Slaves cannot be trained as Warriors!")
                    
                    else:
                        result[1].set_training(char, training_screen_current)
                
                # Normal training
                else:
                    result[1].set_training(char, training_screen_current, training_screen_trainer)
                
                break
            
            # Exit
            elif result[0] == "control" and result[1] == "return":
                break
    
    hide screen girl_training
    jump char_profile
    

screen girl_training:
    
    default tt = Tooltip("Perfection is impossible, there are always improvements to be made.")
    
    # Selection
    vbox:
        style_group "basic"
        null height 44
        hbox:
            for i in schools:
                if schools[i].available:
                    textbutton schools[i].name action TrainingSwitchAction(i)
    
    # Sub-screen
    if training_screen_current is None:
        null
    
    elif training_screen_current.is_school:
        use girl_training_schooling
    
    else:
        use girl_training_trainer
    
    # Tooltip related:
    frame:
        background Frame("content/gfx/frame/window_frame1.png", 10, 10)
        align(0.5, 0.997)
        xysize (1000, 100)
        xpadding 10
        ypadding 10
        text (u"{=content_text}{color=[ivory]}%s" % tt.value)
    
    use top_stripe(True)

# Personal sub-screen
screen girl_training_trainer:
    
    # Trainers:
    frame:
        style_group "content"
        background Frame("content/gfx/frame/arena_d.png", 10, 10)
        area(0, 76, 385, 617)
        has vbox
        null height 3
        frame:
            background Frame("content/gfx/frame/p_frame2.png", 10, 10)
            xysize (365, 25)
            label u"- Trainers -" align (0.5, 0.5) text_size 25 text_color ivory
        null height 3    
        side "c r":
            viewport id "trainer_vp":
                area (0, 0, 385, 545)
                draggable False
                mousewheel True
                has vbox
                for trainer in trainers_at_location(training_screen_current):
                    frame:
                        background Frame("content/gfx/frame/p_frame2.png", 10, 10)
                        xysize (358, 75)
                        hbox:
                            null width 5
                            $ girl_image_show = trainer.show("profile", resize=(70, 70), cache=True)
                            imagebutton:
                                align (0, 0.5)
                                idle girl_image_show
                                hover im.MatrixColor(girl_image_show, im.matrix.brightness(0.15))
                                action Return(["trainer", trainer])
                                hovered tt.action("Train girls with %s.\nCurrently training: %s"%(trainer.name, ", ".join([str(g) for g in girls_training_with(hero)])))
                            
                            null width 5
                            
                            vbox:
                                yalign 0.5
                                label (u"[trainer.name]"):
                                    text_size 20
                                    if training_screen_trainer is trainer:
                                        text_color red
                                    else:
                                        text_color ivory
                                null height 5
                                hbox:
                                    text (u"Girls: %d"%len(girls_training_with(trainer))) color ivory size 18
                                    null width 5
                                    text (u"AP: %d"%trainer_total_ap_cost(trainer)) color ivory size 18
            
            vbar value YScrollValue("trainer_vp")
    
    # Courses:
    frame:
        background Frame("content/gfx/frame/arena_d.png", 10, 10)
        area (395, 76, 415, 617)
        style_group "content"
        has vbox
        null height 3
        frame:
            background Frame("content/gfx/frame/p_frame2.png", 10, 10)
            xysize (385, 25)
            label u"- Courses -" align (0.5, 0.5) text_size 25 text_color ivory
        null height 3
        side "c r":
            viewport id "course_vp":
                area (0, 0, 420, 545)
                draggable False
                mousewheel True
                hbox:
                    xsize 415
                    box_wrap True
                    spacing 5
                    for course in sorted(training_screen_current.courses):
                        if course.can_train(char, hero, one_off_only=False):
                            frame:
                                background Frame("content/gfx/frame/p_frame2.png", 10, 10)
                                xysize (190, 190)
                                vbox:
                                    xalign 0.5
                                    null height 5
                                    label (u"[course.name]") xalign 0.5
                                    null height 5
                                    frame:
                                        xysize (170, 170)
                                        imagebutton:
                                            align (0.5, 0.5)
                                            idle ProportionalScale(content_path(course.get_lesson_image()), 155, 155)
                                            hover im.MatrixColor(ProportionalScale(content_path(course.get_lesson_image()), 155, 155), im.matrix.brightness(0.15))
                                            action Return(["open", course])
                                            hovered tt.action(u"%s"%course.desc)
                                    null height 5
            vbar value YScrollValue("course_vp")
    
    # Course details
    frame:
        background Frame("content/gfx/frame/arena_d.png", 10, 10)
        area (820, 76, 460, 610)
        style_group "content"
        has vbox
        if training_screen_course is not None:
            null height 3
            frame:
                background Frame("content/gfx/frame/p_frame2.png", 10, 10)
                xysize (427, 25)
                label u"- %s -"%training_screen_course.name align (0.5, 0.5) text_size 25 text_color ivory
            null height 3
            side "c r":
                viewport id "lesson_vp":
                    area (0, 0, 440, 545)
                    draggable False
                    mousewheel True
                    hbox:
                        xsize 440
                        box_wrap True
                        spacing 7
                        for course in training_screen_course.get_options(char, training_screen_trainer, one_off_only=False):
                            frame:
                                background Frame("content/gfx/frame/p_frame2.png", 10, 10)
                                xysize (210, 145)
                                use girl_training_lesson(course, tt, False)
                
                vbar value YScrollValue("lesson_vp")
    

screen girl_training_lesson(course, tt, show_image):
    vbox:
        style_group "content"
        xalign 0.5
        null height 2
        
        # Do we have an image
        if show_image:
            # Use plain title
            if course.is_schooling:
                label (u"[course.action]") xalign 0.5 text_color ivory
            else:
                label (u"[course.name]") xalign 0.5 text_color ivory
            
            null height 2
            
            # Image is button
            frame:
                xysize (190, 190)
                imagebutton:
                    align (0.5, 0.5)
                    idle ProportionalScale(content_path(course.get_lesson_image()), 175, 175)
                    hover im.MatrixColor(ProportionalScale(content_path(course.get_lesson_image()), 175, 175), im.matrix.brightness(0.15))
                    action Return(["setto", course])
                    hovered tt.action(u"%s\nGirls being trained: %s"%(course.desc, ", ".join([girl.fullname for girl in hero.chars if char_is_training(girl) is course])))
             
            null height 3
            
        # Else
        else:
            # Use title as button
            vbox:
                style_group "basic"
                xalign 0.5
                
                null height 3
                
                textbutton (u"[course.%s]"%("action" if course.is_schooling else "name")):
                    xsize 185
                    action Return(["setto", course])
                    hovered tt.action(u"%s\nGirls being trained: %s"%(course.desc, ", ".join([girl.fullname for girl in hero.chars if char_is_training(girl) is course])))
                
                null height 3
        
        vbox:
            xalign 0.5
            hbox:
                xalign 0.5
                vbox:
                    xmaximum 120
                    xfill True
                    
                    if not course.is_one_off_event:
                        text "Days:"
                    else:
                        text "Girls AP:"
                    
                    if course.is_schooling:
                        text "Days Left:"
                    
                    else:
                        text "Trainer AP:"
                    
                    text "Daily Fee:"
                    
                    text "Status:"
                    
                vbox:
                    if not course.is_one_off_event:
                        text (u"%s"%(course.duration))
                    
                    else:
                        text (u"%s"%(course.AP))
                    
                    if course.is_schooling:
                        text (u"%s"%(course.daysLeft()))
                    
                    else:
                        text (u"%s"%(course.heroAP))
                    
                    text (u"%s"%(course.gold))
            
            text (u"%s"%(course.trainerStatus(char, training_screen_trainer)))
    

# Schools sub-screen
screen girl_training_schooling:
    # Course viewport
    frame:
        background Frame("content/gfx/frame/arena_d.png", 10, 10)
        area (620, 71, 660, 622)
        side "c r":
            viewport id "course_vp":
                area (0, 0, 660, 610)
                draggable False
                mousewheel True
                hbox:
                    xsize 660
                    box_wrap True
                    spacing 7
                    for course in training_screen_current.courses:
                        frame:
                            background Frame("content/gfx/frame/p_frame2.png", 10, 10)
                            xysize (210, 330)
                            xpadding 5
                            ypadding 5
                            use girl_training_lesson(course, tt, True)
            vbar value YScrollValue("course_vp")
    
    # Detail viewport
    frame:
        style_group "content"
        background Frame("content/gfx/frame/mes11.jpg", 10, 10)
        align (0, 0.7)
        xpadding 10
        ypadding 10
        xysize (590, 610)
        has vbox
        null height 3
        label ("[training_screen_current.name]") xalign 0.5 text_color ivory text_size 25
        null height 3
        add (ProportionalScale("content/schools/school.jpg", 585, 400)) xalign 0.5
        null height 8
        text "The Beautiful educational facilities in PyTFall offer any training one may require for free citizens, foreigners and slaves alike. Century old traditions will make sure that no girl taking classes here will ever be sad or unhappy. Nothing in this world is free however, so courses here might cost you a dime and if you wish to be trained by the Masters, a small fortune." color ivory
        null height 5
        side "c r":
            viewport id "school_vp":
                xsize 580
                draggable False
                mousewheel True
                vbox:
                    xmaximum 590
                    spacing 10
                    text "Girls currently taking courses here:" color ivory
                    for entry in [girl for girl in hero.chars if girl.location == training_screen_current]:
                        hbox:
                            vbox:
                                xmaximum 180
                                xfill True
                                text (u"[entry.fullname]:") color ivory
                            vbox:
                                text (u"[entry.action]") color ivory
            
            vbar value YScrollValue("school_vp")
    
