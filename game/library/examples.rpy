init python:
    """
    init phase is initiation phase that is used to declare constant stuff. At most, you will be defining images in it and using it to create events/quest and their conditions! There will be examples of that in different files.
    This file is the first you should read if you wish to get into written/story development of PyTFall as it contains all the basics.
    
    This is a way to leave a long, multiline comment in Python and Ren'Py.
    There is a very detailed Ren'Py and (far more complicated) Python documentation avalible if you want to learn about something in greater detail.
    Ren'Py comes with a number of script languages. Python is the main one, everything can be done with it but it often requires a long and complicated code.
    That's why other script languages were created as wrappers around it:
    
    **Python:
    Everrything that starts with:
    $
    or
    python:
    
    1) Ren'Py Script: It's evething you see in .rpy files that is not declared as being something else.
    *Examples:
    label
    show
    menu
    image
    define
    and so on.
    
    2) Screen Language (short: SL (Ren'Py in 6.18 was updated to Screen Language 2))
    Screens are used to diplay information to the players and enable any interaction that is not anticipated in default Ren'Py (Anything more than default VN capabilities basically)
    evething that comes after:
    screen my_screen:
        # Screen Language statements
    
    3) ATL (Animation and Transformation Language). 
    Used to move displayable, zoom, crop, rotate and so on.
    Examples:
    transform my_transform:
        # Transformation instructions
    image my_image:
        # Transformation instructions
    
    4) Style Script:
    This is used to create styles and customise the displyable.
    style my_syle:
        # style statements
    
    ===
    init: (initiation phase, it runs every time Ren'Py game is launched from the OS) should be mensioned as well.
    """
    
# init:
    # image sinstar = anim.Filmstrip('content/gfx/images/sinstar.png', (192, 192), (5, 3), 0.1, loop=True) # This is a simplest way to declare an image in Ren'Py
    # image sinstar_reverced = ReversedFilmstrip('content/gfx/images/sinstar.png', (192, 192), (5, 3), 0.1, loop=True)
    # image sinstar_loop:
        # "sinstar"
        # 1.5
        # "sinstar_reverced"
        # 1.5
        # repeat
    
label examples:
    # <-- Hashtag is how we leave single line comments in Ren'Py script and Python. Ren'Py script does not support multiline as above and requires to define those comments as python code.
    # Labels are logical deviders for code/content in Ren'Py.
    # This label hosts and leads to examples of what can be done in the game.
    
    scene black
    # Scene statement clears current layer (master layer in this case). (It hides all pictures, sprites, backgrounds, texts and other displayble that are shown on the layer!)
    # Statement just like in any other script or programming language means a logical command (cycle). We'll be mostly dealing with simple commands, as this guide is meant for content creators, not core devs.
    # It will hide everything except screens (They are being displayed on a screens layer) and maybe something else we decided to show on a different layer.
    
    # "Quick interruption to show off the image we declared a few lines ealier!"
    # # show sinstar at Transform(align=(0.3, 0.5))
    # # show sinstar_reverced at Transform(align=(0.5, 0.5))
    # show sinstar_loop at Transform(align=(0.5, 0.5))
    # pause # This will wait for user to click somewhere...
    # "This was it... sorry for inconvenience..."
    # scene black
    $ renpy.maximum_framerate(60)
    "First attempt to emulate dizziness:"
    show expression Mirage("bg cafe", amplitude=0.04, ycrop=1, wavelength=10) as testing
    pause
    hide testing
    
    "Second Try:"
    $ double_vision_on("bg cafe")
    pause
    $ double_vision_off()
    
    "Third..."
    $ temp = im.Scale(ImageReference("bg cafe"), 128, 72)
    $ temp = Transform(temp, size=(1280, 720))
    show expression temp as bg
    with Dissolve(0.4)
    show bg cafe
    with Dissolve(0.4)
    show expression temp as bg
    with Dissolve(0.5)
    show bg cafe
    with Dissolve(0.5)
    show expression temp as bg
    with Dissolve(0.6)
    show bg cafe
    with Dissolve(0.4)
    show expression temp as bg
    with Dissolve(1.0)
    show bg cafe
    with dissolve
    
    "Third... ver 2.0"
    $ blurred_vision("bg cafe")
    
    scene black
    "All Done!"
    
    "Hello... "
    extend "I am the narrator! And will be guiding you in this example!"
    # Narrator will just display the text. Not from a name of any particular character.
    
    "Note that all the good stuff is written as comments in examples.rpy file and you will not be able to see it from the game!"
    "There is also a very good tutorial availible if you download Ren'Py SDK kit (less than 30 MB and does not require instalation)!"
    "You should get SDK if you want to develop content for PyTFall. It's not really a 'MUST HAVE' but it's most definetly a should have :)'"
    "There will be a great demonstration tutorial there of what the engine is capable of! This shows similar things but those that are more relevant to {color=[red]}PyTFall{/color}!"
    # {color=[red]}Text{/color} changes something about text styling! You can use a lot here... like {b}Text{/b} will write text in bold!
    # You can check all properties by googling RenPy + Text + Style + Properties
    
    $ pass # DOES NOTHING! :) It is just an example of what Python oneliner looks like!
    
    python:
        # Python code, any amount of lines.
        # Identation is always important, no matter what script is in use.
        # Everything in Python is an object, we can pass those objects around and assign them to anything we like.
        # Every character in the game has a predefined Character property that can be used to display text lines in characters name and auto-display characters portraits.
        # So lets define a few that we're going to work with:
        mc = hero.say # every character has a say attribute as previously stated. We can use it to define sayers quickly.
    "We've just defined an mc (Main Character) Sayer in the file!"    
        
    mc "Yey! Now I can talk!"
    mc "CW's Naruto pack needs to be installed in order to proceed from this point!"
    
    $ h = chars["Hinata"].say
    # char is a container (a dictionary) that holds all characters in the game. That's also made for convinience. Characters can be retrieved by girls ids we defined in their data files.
    h "Now I can talk too!"
    extend " And my portrait side-picture is being properly displayed!"
    
    # We add two more characters:
    python:
        s = chars["Sakura"].say
        t = chars["Tenten"].say
        
    s "I am here now as well!"
    t "And don't forget about me!"
    
    "Now that we've seen how they can talk... one more thing should be noted, if we just need a character to speak once, a simple:"
    
    hero.say "Something simple..."
    chars["Sakura"].say "You god damn right, that wasn't hard!"
    
    "(It makes more sense if you read the file and not just the game :) )"
    
    "Ok... so now, once we've established talking... lets try some Sprites!"
    "We do not use internal image tagging system that Ren'Py comes with for image tracking, that doesn't mean however that we cannot make use of default Ren'Py statements!"
    
    # So lets declare (assign) some images as well:
    $ hi = chars["Hinata"].get_vnsprite()
    show expression hi at right with dissolve
    
    h "Just two lines of script and you can see me in at a specific location shown with special effects!"
    extend " you can even do it with one! :)"
    
    # This does look a bit complicated I suppose :)
    python:
        """
        hi: (Hinate Image) we assign a VN type of an image to a variable hi
        show: is a Ren'Py statement that shows something like a picture, image or any displayable... normally show expects a defined Ren'Py tagged image (using image statement).
        expression: means that we are not using an internally (Ren'Py) tagged image but some other displyable (PyTFall tagged displayable, here it is called ProportionalScale in case anyone want to know).
        at: is used to apply a transform to the displayble (our Hinata Sprite). Here we tell it to position the sprite to the right position of the screen.
        with: is used to apply transision (kinda special effect), in this example it's a dissolve.
        """
        
    h "I am going to move to the left now! Once again, one line of code! Doesn't really get simpler than this..."
    show expression hi at left with move
    
    h "Sakura?"
    extend  " Where are you???"
    
    python:
        si = chars["Sakura"].get_vnsprite()
        ti = chars["Tenten"].get_vnsprite()
        
    show expression si at right with dissolve
    s "Here I am!"
    show expression ti at center with dissolve
    t "And you keep forgetting about me!!!"
    
    "It's easier than it looks... especially if you try it yourself a couple of times!"
    
    "Lets shuffle them a bit!"
    show expression hi at center with move
    show expression si at left with move
    show expression ti at right with move
    
    s "Stop doing that!"
    
    "Well... that's it for the basics. Lets go to the good stuff!"
    
    jump examples_2
    # Jump means jump to a label. It does exactly what it sounds like.
    
label examples_2:
    "Lets clear the master layer!"
    scene
    
    # The game autodefines all background images. We are using that very effectively...
    # bg in this case is a prefix tag, cafe is the name of the image that was autodefined. It's a name without extension.
    # If we show another bg prefixed image, the current one will be automatically replaced with the new one.
    
    show bg cafe
    
    "Cafe in the center of PyTFall!"
    "Normally you can shop here, but for now we're just going to hang out."
    
    "Lets bring one of the girls in!"
    show expression ti at center with dissolve
    
    t "Lets play a simple game!"
    show expression ti at right with move
    
    t "I'll think of a number from 1 to 5. You'll have to guess which one it is! "
    extend "I promise that I am not going to cheat!"
    
    menu:
        # Menu allows you to add choices to the game and create forks in the story.
        t "So how about it?"
        "Play":
            call simple_numbers_game from _call_simple_numbers_game
            # Calling a label puts it in a stack
            # Main advantage is that we can return from a called label to the next statement in this label!
        "Skip":
            t "You're no fun at all :("
          
    show expression ti at center with move
    t "So... How about we go to the park? Maybe meet up with rest of the girls!?"
    
    hide expression ti
    show bg city_park with dissolve
    show expression ti at center with dissolve
    
    t "Finally some fresh air! That black void and dusty cafe sure sucked!"
    t "Lets see if other girls are around..."
    extend " SAKURA!?!?"
    extend " HINATA!?!?"
    
    show expression hi at left with dissolve
    show expression si at right with dissolve
    s "Here we are!"
    
    "This concludes this intro. All possibilities Ren'Py & PyTFall offer are too broad to be explained in one tutorail. There will be other soon, maybe even examples from the game itself!"
    
    # It is always a good idea to get rid of the variable once we're done with them:
    python:
        del t
        del ti
        del h
        del hi
        del s
        del si
        del mc
        
    
    jump mainscreen
    # Mainscreen has it's own scene statement so it will clear sprites and backgroud we left here!

label simple_numbers_game:
    $ n = randrange(1, 6)
    # This is a python function... it returns a random number from 1 to 5.
    
    menu:
        t "Guess!?!?"
        "1":
            $ answer = 1
        "2":
            $ answer = 2
        "3":
            $ answer = 3
        "4":
            $ answer = 4
        "5":
            $ answer = 5
        "That's it for now" if global_flags.flag("been_here_once"):
            # This choice will only appear if a flag is set. We'll get to this a bit later.
            return # Since this label was originally called, we can return. Otherwise, this would have terminated the game.
            
            
    if n == answer:
        t "WOW! It's almost like mind reading! :)"
    else:
        if not global_flags.flag("been_here_once"):
            t "Well..."
            extend " you suck! The number was [n]!"
        else:
            t "You still suck! "
            extend "The number was [n]!"
       # Now: [n] is an interpolation. We can put contents of a variable into the text this way. In this case it's a number.
       # Same thing can be used for player name for example: [hero.name] or a stat value: [hero.attack].
       
    $ global_flags.set_flag("been_here_once")
    # This is an example of flags used in PyTFall. Flags are set to remember something that happened at one point of the game. It can be set to anything at all, set or read anywhere.
    # In this particular default case, we'll set the flag to True. It just works that way if no additional arguments are provided.
    # All characters and most buildings have flags as well: chars["Hinata"].set_flag("met_with_sakura_in_the_park")
    # Would set up an unique flag for Hinata for example.
    
    jump simple_numbers_game
    # This is one way of creating an infinite loop. We'll keep jumping to the same label over and over :) But we've set a flag which will allow us to fall back through the menu!
    
    
        
