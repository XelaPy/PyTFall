init -999 python:
    class RadarChart(renpy.Displayable):
        def __init__(self, stat1, stat2, stat3, stat4, stat5, size, xcenter, ycenter, color, **kwargs):
            super(RadarChart, self).__init__(self, **kwargs)
            # renpy.Displayable.__init__(self, **kwargs)
            self.color = color
            self.stat1_vertex = (xcenter, ycenter - (self.get_length_for_rating(size, stat1)))
            self.stat2_vertex = self.get_tangent_offset(xcenter, ycenter, 90+(72*1), self.get_length_for_rating(size, stat2))
            self.stat3_vertex = self.get_tangent_offset(xcenter, ycenter, 90+(72*2), self.get_length_for_rating(size, stat3))
            self.stat4_vertex = self.get_tangent_offset(xcenter, ycenter, 90+(72*3), self.get_length_for_rating(size, stat4))
            self.stat5_vertex = self.get_tangent_offset(xcenter, ycenter, 90+(72*4), self.get_length_for_rating(size, stat5))
            
        def render(self, width, height, st, at):
            r = renpy.Render(width, height)
            rr = r.canvas()
            rr.polygon(color("%s"%self.color), (self.stat1_vertex,
                                                                    self.stat2_vertex,
                                                                    self.stat3_vertex,
                                                                    self.stat4_vertex,
                                                                    self.stat5_vertex))
            return r
        
        @staticmethod
        def get_tangent_offset(xorigin, yorigin, angle, length):
            return int(xorigin + (cos(radians(angle)) * length)), int(yorigin - (sin(radians(angle)) * length))
            
        @staticmethod
        def get_length_for_rating(size, rating):
            return 7 + int(size*rating)
            
            
    class HitlerKaputt(renpy.Displayable):
        def __init__(self, displayable, crops, neg_range=(-8, -1), pos_range=(1, 8), **kwargs):
            """
            Crops the displayable and sends the bits flying...
            """
            super(HitlerKaputt, self).__init__(**kwargs)
            self.displayable = displayable
            self.crops = crops # This is doubled...
            
            self.args = None
            
            self.neg_range = neg_range
            self.pos_range = pos_range
            
            self.width = 0
            self.height = 0
        
        def render(self, width, height, st, at):
            if not st:
                self.args = None
            
            if not self.args:
                t = Transform(self.displayable)
                child_render = renpy.render(t, width, height, st, at)
                self.width, self.height = child_render.get_size()
                
                # Size of one crop:
                crop_xsize = int(round(self.width / float(self.crops)))
                crop_ysize = int(round(self.height / float(self.crops)))
                
                # The list:
                i = 0
                args = OrderedDict()
                half = self.crops / 2.0
                choices = range(*self.neg_range) + range(*self.pos_range)
            
                for r in xrange(0, self.crops):
                    for c in xrange(0, self.crops):
            
                        x = c * crop_xsize
                        y = r * crop_ysize
                        
                        direction = choice(choices), choice(choices)
            
                        args[(Transform(t, rotate=randint(0, 90), crop=(x, y, crop_xsize, crop_ysize)))] = {"coords": [x, y], "direction": direction}
                self.args = args
                
            render = renpy.Render(self.width, self.height)
            for r in self.args:
                cr = renpy.render(r, width, height, st, at)
                coords = self.args[r]["coords"]
                direction = self.args[r]["direction"]
                render.blit(cr, tuple(coords))
                coords[0] = coords[0] + direction[0]
                coords[1] = coords[1] + direction[1]
            renpy.redraw(self, 0)
            return render
    
    
    class FilmStrip(renpy.Displayable):
        """Simple UDD that cuts a spreadsheet and animates it.
        """
        def __init__(self, displayable, framesize, gridsize, delay, include_frames=None, exclude_frames=None, loop=True, reverse=False, **kwargs):
            """Creates a list of Transforms ready to be rendered. This may take up a little bit more memory than doing the same on the fly but it should be faster.
            
            @params:
            displayable: Displayable we will cut, usually a path to image.
            framesize: A size of a single frame in pixels.
            gridsize: Height and width of the grid as a tuple: (5, 5) means 5 by 5 frames.
            delay: Time between each frame in seconds.
            include_frames: If not None, espects a list of frames from the sheet that should be incuded in animation. Frames are numbered 0 to z where 0 is the top-left frame and z id the bottom-right frame.
            exclude_frames: If not None, frames to exclude. Rules same as above. Included frame will exclude all but themselves and excuded frames will never be shown.
            loop: Loop endlessly if True, will show the animation once if False.
            reverse: Reverse the order of frames in animation.
            """
            super(FilmStrip, self).__init__(**kwargs)
            self.displayable = renpy.easy.displayable(displayable)
            width, height = framesize
            cols, rows = gridsize
            
            total_frames = cols * rows
        
            i = 0
        
            # Arguments to Animation
            args = []
            
            for r in range(0, rows):
                for c in range(0, cols):
                    if include_frames and i not in include_frames:
                        i = i + 1
                        continue
                    if exclude_frames and i in exclude_frames:
                        i = i + 1
                        continue
                        
                    x = c * width
                    y = r * height
                    args.append(Transform(self.displayable, crop=(x, y, width, height)))
                    
                    i = i + 1
                    
                    if i == total_frames:
                        break
                        
                if i == total_frames:
                    break
                    
            # Reverse the list:
            if reverse:
                args.reverse()
                
            self.width, self.height = width, height
            self.frames = args
            self.delay = delay
            self.index = 0
            self.loop = loop
        
        def render(self, width, height, st, at):
            if not st:
                self.index = 0
            
            t = self.frames[self.index]
            
            if self.index == len(self.frames) - 1:
                if self.loop:
                    self.index = 0
            else:
                self.index = self.index + 1
                
            render = renpy.Render(self.width, self.height)
            child_render = t.render(width, height, st, at)
            render.blit(child_render, (0, 0))
            renpy.redraw(self, self.delay)
            return render
            
        # def visit(self):
            # return [self.image]
            
            
    class AnimateFromList(renpy.Displayable):
        def __init__(self, args, loop=True, **kwargs):
            super(AnimateFromList, self).__init__(**kwargs)
            self.images = list()
            for t in args:
                self.images.append([renpy.easy.displayable(t[0]), t[1]])
            self.loop = loop
            self.index = 0
        
        def render(self, width, height, st, at):
            if not st:
                self.index = 0
            # We just need to animate once over the list, no need for any calculations:
            try:
                t = self.images[self.index][0]
                child_render = t.render(width, height, st, at)
                
                w, h = child_render.get_size()
                
                render = renpy.Render(w, h)
                render.blit(child_render, (0, 0))
                renpy.redraw(self, self.images[self.index][1])
                
                self.index = self.index + 1
                if self.loop:
                    if self.index > len(self.images) - 1:
                        self.index = 0
                return render
            except IndexError:
                return renpy.Render(0, 0)
            
        # def visit(self):
            # return [img[0] for img in self.images]
            
    
    class ProportionalScale(im.ImageBase):
        '''Resizes a renpy image to fit into the specified width and height.
        The aspect ratio of the image will be conserved.'''
        def __init__(self, img, maxwidth, maxheight, bilinear=True, **properties):
            self.image = renpy.easy.displayable(img)
            super(ProportionalScale, self).__init__(self.image, maxwidth, maxheight, bilinear, **properties)
            self.maxwidth = int(maxwidth)
            self.maxheight = int(maxheight)
            self.bilinear = bilinear

        def load(self):
            child = im.cache.get(self.image)
            width, height = child.get_size()
            
            ratio = min(self.maxwidth/float(width), self.maxheight/float(height))
            width = ratio * width
            height = ratio * height

            if self.bilinear:
                try:
                    renpy.display.render.blit_lock.acquire()
                    rv = renpy.display.scale.smoothscale(child, (width, height))
                finally:
                    renpy.display.render.blit_lock.release()
            else:
                try:
                    renpy.display.render.blit_lock.acquire()
                    rv = renpy.display.pgrender.transform_scale(child, (newwidth, newheight))
                finally:
                    renpy.display.render.blit_lock.release()
            return rv
            
        def true_size(self):
            """
            I use this for the BE. Will do the callulations but not render anything.
            """
            child = im.cache.get(self.image)
            width, height = child.get_size()
            
            ratio = min(self.maxwidth/float(width), self.maxheight/float(height))
            width = int(round(ratio * width))
            height = int(round(ratio * height))
            return width, height
            
        def get_image_name(self):
            """Returns the name of an image bound to the ProportionalScale.
            """
            path = self.image.filename
            image_name = path.split("/")[-1]
            return image_name
            
        def get_image_tags(self):
            """Returns a list of tags bound to the image.
            """
            image_name = self.get_image_name()
            image_name_base = image_name.split(".")[0]
            obfuscated_tags = image_name_base.split("-")[1:]
            return [tags_dict[tag] for tag in obfuscated_tags]

        def predict_files(self):
            return self.image.predict_files()
            
            
    class Mirage(renpy.Displayable):
        def __init__(self, displayable, resize=(1280, 720), ycrop=8, amplitude=0, wavelength=0, **kwargs):
            super(renpy.Displayable, self).__init__(**kwargs)
            displayable = Transform(displayable, size=resize)
            self.displayable = list()
            for r in xrange(resize[1]/ycrop):
                y = r * ycrop
                self.displayable.append((Transform(displayable, crop=(0, y, resize[0], ycrop)), y))
                
            # self.image = [Transform(renpy.easy.displayable(image), crop=(0, i+1, width, 2)) for i in range(height/2)]
            self.amplitude = amplitude
            self.wavelength = wavelength
            self.W2 = config.screen_width * 0.5

            zoom_factor = 1.0 - self.amplitude
            self.x_zoom_factor = 1 / zoom_factor
           
        # Stretch each scanline horizontally, oscillating from +amplitude to -amplitude across specified wavelength
        # Shift oscillation over time by st
        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
             
            h = 1.0
            for scanline in self.displayable:   
                # math.sin(x) returns the sine of x radians
                t = Transform(scanline[0], xzoom = self.x_zoom_factor + (math.sin(h / self.wavelength + st) * self.amplitude), yzoom = (1.01))
                h += 1.0
                child_render = renpy.render(t, 0, 0, st, at)
                cW, cH = child_render.get_size()
                # final amount subtracted from h sets y placement
                render.blit(child_render, ((self.W2) - (cW * 0.5), scanline[1]))
            renpy.redraw(self, 0)
            return render
            
            
    class Vortex(renpy.Displayable):
        def __init__(self, displayable, amount=25, radius=300, adjust_radius=None, time=10, circles=3, reverse=False, **kwargs):
            super(Vortex, self).__init__(**kwargs)
            self.displayable = renpy.easy.displayable(displayable)
            self.amount = amount
            self.adjust_radius = adjust_radius
            self.time = time
            self.circles = circles
            self.vp = None
            
            self.reverse = reverse
            self.radius = radius

        def render(self, width, height, st, at):
            if not st:
                self.args = None
            
            if not self.args:
                self.args = list()
                step = self.radius/self.amount
                for i in xrange(1, self.amount+1):
                    if isinstance(self.time, (tuple, list)):
                        t = random.uniform(*self.time)
                    else:
                        t = self.time
                        
                    if isinstance(self.circles, (tuple, list)):
                        c = random.uniform(*self.circles)
                    else:
                        c = self.circles
                        
                    r = self.radius - step*i
                    if self.adjust_radius:
                        r = r + randint(*self.adjust_radius)
                    if self.reverse:
                        self.args.append(vortex_particle(self.displayable, t=t, angle=randint(0, 360), start_radius=0, end_radius=r, circles=c))
                    else:
                        self.args.append(vortex_particle(self.displayable, t=t, angle=randint(0, 360), start_radius=r, circles=c))
                    
            render = renpy.Render(width, height)
            for r in self.args:
                cr = r.render(width, height, st, at)
                render.blit(cr, (r.xpos, r.ypos))
            renpy.redraw(self, 0)
            return render
            
            
init python:
    def get_size(d):
        d = renpy.easy.displayable(d)
        w, h = renpy.render(d, 0, 0, 0, 0).get_size()
        w, h = int(round(w)), int(round(h))
        return w, h
    
    def gen_randmotion(count, dist, delay):
        args = [ ]
        for i in xrange(count):
            args.append(anim.State(i, None,
                                   Position(xpos=randrange(-dist, dist),
                                            ypos=randrange(-dist, dist),
                                            xanchor='left',
                                            yanchor='top',
                                            )))

        for i in xrange(count):
            for j in xrange(count):
                if i == j:
                    continue
                    
                args.append(anim.Edge(i, delay, j, MoveTransition(delay)))
        return anim.SMAnimation(0, *args)

    def double_vision_on(img, alpha=0.5, count=10, dist=7, delay=0.4):
        renpy.scene()
        renpy.show(img)
        renpy.show(img, at_list=[Transform(alpha=alpha), gen_randmotion(count, dist, delay)], tag="blur_image")
        renpy.with_statement(dissolve)

    def double_vision_off():
        renpy.hide("blur_image")
        renpy.with_statement(dissolve)
            
    def blurred_vision(img):
        img = renpy.easy_displayable(img)
        width, height = get_size(img)
        
        factor = im.Scale(img, width/5, height/5)
        factor = Transform(factor, size=(width, height))
        renpy.show("blur_effect", what=factor)
        renpy.with_statement(Dissolve(0.6))
        renpy.hide("blur_effect")
        
        renpy.show("blur_effect", what=img)
        renpy.with_statement(Dissolve(0.4))
        renpy.hide("blur_effect")
        
        factor = im.Scale(img, width/10, height/10)
        factor = Transform(factor, size=(width, height))
        renpy.show("blur_effect", what=factor)
        renpy.with_statement(Dissolve(0.8))
        renpy.hide("blur_effect")
        
        factor = im.Scale(img, width/5, height/5)
        factor = Transform(factor, size=(width, height))
        renpy.show("blur_effect", what=factor)
        renpy.with_statement(Dissolve(0.6))
        renpy.hide("blur_effect")
        
        factor = im.Scale(img, width/15, height/15)
        factor = Transform(factor, size=(width, height))
        renpy.show("blur_effect", what=factor)
        renpy.with_statement(Dissolve(1.0))
        renpy.hide("blur_effect")
        
        factor = im.Scale(img, width/10, height/10)
        factor = Transform(factor, size=(width, height))
        renpy.show("blur_effect", what=factor)
        renpy.with_statement(Dissolve(0.8))
        renpy.hide("blur_effect")
        
        factor = im.Scale(img, width/20, height/20)
        factor = Transform(factor, size=(width, height))
        renpy.show("blur_effect", what=factor)
        renpy.with_statement(Dissolve(1.2))
        renpy.hide("blur_effect")
        
    def _shake_function(trans, st, at, dt=.5, dist=256): #dt is duration timebase, dist is maximum shake distance in pixel
        if st <= dt:
            trans.xoffset = int((dt-st)*dist*(.5-renpy.random.random())*2)
            trans.yoffset = int((dt-st)*dist*(.5-renpy.random.random())*2)
            return .01
        else:
            return None
            
    def get_random_image_dissolve(time):
        transitions = list()
        path = content_path("gfx/masks")
        for file in os.listdir(path):
            transitions.append("/".join(["content/gfx/masks", file]))
        return ImageDissolve(choice(transitions), time)
            
transform shake(dt=.4, dist=128):
    function renpy.curry(_shake_function)(dt=dt,dist=dist)
