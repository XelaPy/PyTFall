init python:
    # Plain Events:
    class BE_Skip(BE_Event):
        """
        Simplest possible class that just skips the turn for the player and logs that fact.
        This can/should be a function but heck :D
        """
        def __init__(self, source=None):
            self.source = source
        
        def __call__(self):
            msg = "{} skips a turn!".format(self.source.nickname)
            battle.log(msg)
            

    class RPG_Death(BE_Event):
        """
        Used to instantiate death and kill off a player at the end of any turn...
        """
        def __init__(self, target, death_effect="dissolve", msg=None):
            self.target = target
            self.death_effect = death_effect
            if not msg:
                self.msg = "{color=[red]}%s was (heroically?!?) knocked out!{/color}" % self.target.name
            else:
                self.msg = msg    
            
        def check_conditions(self):
            # We want to run this no matter the f*ck what or we'll have fighting corpses on our hands :)
            return True
            
        def kill(self):
            return True
            
        def apply_effects(self):
            battle.corpses.add(self.target)
            
            if not battle.logical:
                renpy.hide(self.target.betag)
                if self.death_effect == "dissolve":
                    renpy.with_statement(dissolve)
            
            # Forgot to remove poor sods from the queue:
            for target in battle.queue[:]:
                if self.target == target:
                    store.battle.queue.remove(self.target)
            
            battle.log(self.msg)
            
            
    class PoisonEvent(BE_Event):
        def __init__(self, target, source, effect):
            self.target = target
            self.source = source
            if target.constitution <= 0:
                self.counter = source.intelligence+2
            else:
                self.counter = round(source.intelligence/target.constitution)+2 # We remove the event if counter reaches 0.
            self.effect = effect / 1000.0
            self.attributes = ['status', 'poison']
            
        def check_conditions(self):
            if battle.controller == self.target:
                return True
                
        def kill(self):
            if not self.counter:
                return True
                
        def apply_effects(self):
            t = self.target
            s = self.source
            
            # Damage Calculations:
            damage = t.get_max("health") * self.effect
            damage = max(randint(15, 20), int(damage) + randint(-4, 4))
            
            # GFX:
            if not battle.logical:
                gfx = Transform("poison_2", zoom=1.5)
                renpy.show("poison", what=gfx, at_list=[Transform(pos=battle.get_cp(t, type="center"), anchor=(0.5, 0.5))], zorder=t.besk["zorder"]+1)
                txt = Text("%d"%damage, style="content_label", color=red, size=15)
                renpy.show("bb", what=txt, at_list=[battle_bounce(store.battle.get_cp(t, type="tc", yo=-10))], zorder=t.besk["zorder"]+2)
                renpy.pause(1.5)
                renpy.hide("poison")
                renpy.pause(0.2)
                renpy.hide("bb")
            
            if t.health - damage > 0:
                t.mod("health", damage * -1)
                msg = "{color=[red]}%s is poisoned!! DMG: %d{/color}" % (self.target.name, damage)
                battle.log(msg)
            else:
                death = RPG_Death(self.target, msg="{color=[red]}Poison took out %s!\n{/color}" % self.target.name)
                death.apply_effects()
                
            self.counter -= 1
            
            if self.counter <= 0:
                msg = "{color=[red]}Poison effect on %s has ran it's course...{/color}" % (self.target.name)
                battle.log(msg)
            
    # Actions:
    # Simple Attack:
    class SimpleAttack(BE_Action):
        """
        Simplest attack, usually weapons.
        """
        def __init__(self, name, aim="center", xo=0, yo=0, pause=0.1, **kwargs):
            super(SimpleAttack, self).__init__(name, **kwargs)
            
            # Aiming properties:
            self.aim = aim
            self.xo = xo
            self.yo = yo
            
            # Rest:
            self.pause = pause # Animation length

        def show_gfx(self, target):
            # Simple effects for the sword attack:
            char = self.source
            
            if not battle.logical:
                battle.move(char, battle.get_cp(char, xo=50), 0.5)
            
                gfxtag = "attack"
                bbtag = "battle_bouce"
                
            # This we can run elsewhere so this whole method can be skipped:
            self.effects_resolver([target]) # This can also be moved elsewhere. This causes the actual damage.
            self.apply_effects([target]) # This can also be moved elsewhere. This causes the actual damage.
            
            if not battle.logical:
                s = "%s"%target.beeffects[0]
                if "critical_hit" in target.beeffects:
                    s = "\n".join([s, "Critical hit!"])
                txt = Text(s, style="content_label", color=red, size=15)  # This I should (prolly) move to a separate class/function. For now it is here:
                if self.sfx:
                    if isinstance(self.sfx, (list, tuple)):
                        sfx = choice(self.sfx)
                    else:
                        sfx = self.sfx
                    renpy.sound.play(sfx)
                
                # Zoom (If any):
                if self.zoom is not None:
                    gfx = Transform(self.gfx, zoom=self.zoom)
                else:
                    gfx = self.gfx
                    
                if self.gfx:
                    renpy.show(gfxtag, what=gfx, at_list=[Transform(pos=battle.get_cp(target, type=self.aim, xo=self.xo, yo=self.yo), anchor=(0.5, 0.5))], zorder=target.besk["zorder"]+1)
                renpy.show(bbtag, what=txt, at_list=[battle_bounce(battle.get_cp(target, type="tc", yo=-10))], zorder=target.besk["zorder"]+2)
                
                battle.move(char, char.dpos, 0.5, pause=False)
                
                renpy.pause(self.pause)
                renpy.hide(gfxtag)
                renpy.with_statement(dissolve)
                renpy.pause(1.4-self.pause)
                renpy.hide(bbtag)
            
            
    # Simple Magic:
    class SimpleMagicalAttack(BE_Action):
        """
        Simplest attack, usually simple magic.
        """
        def __init__(self, name, aim="bc", xo=0, yo=0, pause=0.5, cost=5, anchor=(0.5, 1.0), casting_effects=["default_1", "default"], **kwargs):
            super(SimpleMagicalAttack, self).__init__(name, **kwargs)
            
            # Aiming properties:
            self.aim = aim
            self.xo = xo
            self.yo = yo
            
            # Rest:
            self.cost = cost
            self.anchor = anchor
            self.pause = pause
            
            # Casting effects:
            self.casting_effects = casting_effects

        def check_conditions(self, source=None):
            if source:
                char = source
            else:
                char = self.source
                
            # We need to make sure that we have enought mp for this one:
            if char.mp - self.cost >= 0:
                if self.get_targets(char):
                    return True
                    
        def apply_effects(self, targets):
            # **At Review, Returns target, True if target dies!
            # Not 100% for that this will be required...
            # Here it is simple since we are only focusing on damaging health:
            # prepare the variables:
            died = list()
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            for t in targets:
                if t.health - t.beeffects[0] > 0:
                    t.mod("health", t.beeffects[0] * -1)
                else:
                    battle.end_turn_events.append(RPG_Death(t))
                    died.append(t)
                    
            # Here we need to take of MP:
            self.source.mp -= self.cost
            return died
            
        def show_gfx(self, targets):
            # Simple effects for the magic attack:
            char = self.source
            
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            
            if not battle.logical:
                # Inicial movement of the sprtite:
                battle.move(char, battle.get_cp(char, xo=50), 0.5)
            
            # if self.casting_effects[1] == "default":
                # renpy.sound.play("content/sfx/sound/be/cannon_3.mp3")
            
                if self.casting_effects[0]:
                    casting_effect(char, self.casting_effects[0], sfx=self.casting_effects[1])
            
            self.effects_resolver(targets) # This can also be moved elsewhere. This causes the actual damage.
            died = self.apply_effects(targets) # This can also be moved elsewhere. This causes the actual damage.
            
            if not battle.logical:
                if self.sfx:
                    if isinstance(self.sfx, (list, tuple)):
                        sfx = choice(self.sfx)
                    else:
                        sfx = self.sfx
                    renpy.sound.play(sfx)
                
                # Zoom (If any):
                if self.zoom is not None:
                    gfx = Transform(self.gfx, zoom=self.zoom)
                else:
                    gfx = self.gfx
                    
                # Showing the impact effects:  
                if self.gfx:
                    for index, target in enumerate(targets):
                        gfxtag = "attack" + str(index)
                        renpy.show(gfxtag, what=gfx, at_list=[Transform(pos=battle.get_cp(target, type=self.aim, xo=self.xo, yo=self.yo), anchor=self.anchor)], zorder=target.besk["zorder"]+1)
                        
                # Pause before battle bounce + damage on target effects:
                renpy.pause(self.td_gfx[0])
                
                for index, target in enumerate(targets):
                    self.show_gfx_dmg(target)
                    if len(self.td_gfx) > 1:
                        self.show_gfx_td(target, 0.5, self.td_gfx[1])
                
                battle.move(char, char.dpos, 0.5, pause=False)
                
                # Pause before termination of damage on target effects, if there are any:
                # @Review: OR Pause before application of special death effects!
                # Since it is not (very) plausible that any death effect should appear after the damage from a spell to the target:
                # **This will always assume 
                if self.death_effect or len(self.td_gfx) > 1:
                    if len(self.td_gfx) > 1:
                        renpy.pause(self.td_gfx[2])
                        for target in targets:
                            renpy.hide(target.betag)
                            renpy.show(target.betag, what=target.besprite, at_list=[Transform(pos=target.cpos)], zorder=target.besk["zorder"])
                    
                # Shatter or some other death effect we want to handle in this method:
                if died and self.death_effect == "shatter":
                    for target in died:
                        renpy.hide(target.betag)
                        renpy.show(target.betag, what=HitlerKaputt(target.besprite, 30), at_list=[Transform(pos=target.cpos)], zorder=target.besk["zorder"])
                
                total_pause = self.td_gfx[0]
                if len(self.td_gfx) > 1:
                    total_pause = total_pause + self.td_gfx[2]
                    
                # Check we need any more pause:
                if self.pause > total_pause:
                    renpy.pause(self.pause - total_pause)
                    
                for i in xrange(len(targets)):
                    gfxtag = "attack" + str(i)
                    renpy.hide(gfxtag)
                    
                # Check if we need any more pause before we kill the battle bounce:
                if self.pause - total_pause < 1.7:
                    renpy.pause(1.7 - (self.pause - total_pause))
                    
                    
    class ArealMagicalAttack(SimpleMagicalAttack):
        """
        Simplest attack, usually simple magic.
        """
        def __init__(self, name, aim="bc", xo=0, yo=0, pause=0.5, cost=5, anchor=(0.5, 1.0), casting_effects=["default_1", "default"], **kwargs):
            super(ArealMagicalAttack, self).__init__(name, **kwargs)
            
            # Aiming properties:
            self.aim = aim
            self.xo = xo
            self.yo = yo
            
            # Rest:
            self.cost = cost
            self.anchor = anchor
            self.pause = pause
            
            # Casting effects:
            self.casting_effects = casting_effects

        def show_gfx(self, targets):
            # Simple effects for the magic attack:
            char = self.source
            
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            
            if not battle.logical:
                battle.move(char, battle.get_cp(char, xo=50), 0.5)
                if self.casting_effects[0]:
                    casting_effect(char, self.casting_effects[0], sfx=self.casting_effects[1])
            
            self.effects_resolver(targets) # This can also be moved elsewhere. This causes the actual damage.
            died = self.apply_effects(targets) # This can also be moved elsewhere. This causes the actual damage.
            
            if not battle.logical:
                if self.sfx:
                    if isinstance(self.sfx, (list, tuple)):
                        sfx = choice(self.sfx)
                    else:
                        sfx = self.sfx
                    renpy.sound.play(sfx)
                
                # Zoom (If any):
                if self.zoom is not None:
                    gfx = Transform(self.gfx, zoom=self.zoom)
                else:
                    gfx = self.gfx
                    
                # Showing the impact effects:  
                if self.gfx:
                    for index, target in enumerate(targets):
                        gfxtag = "attack" + str(index)
                        renpy.show(gfxtag, what=gfx, at_list=[Transform(pos=battle.get_cp(target, type=self.aim, xo=self.xo, yo=self.yo), anchor=self.anchor)], zorder=target.besk["zorder"]+1)
                        
                # Pause before battle bounce + damage on target effects:
                renpy.pause(self.td_gfx[0])
                
                for index, target in enumerate(targets):
                    self.show_gfx_dmg(target)
                    if len(self.td_gfx) > 1:
                        self.show_gfx_td(target, 0.5, self.td_gfx[1])
                
                battle.move(char, char.dpos, 0.5, pause=False)
                
                # Pause before termination of damage on target effects, if there are any:
                # @Review: OR Pause before application of special death effects!
                # Since it is not (very) plausible that any death effect should appear after the damage from a spell to the target:
                # **This will always assume 
                if self.death_effect or len(self.td_gfx) > 1:
                    if len(self.td_gfx) > 1:
                        renpy.pause(self.td_gfx[2])
                        for target in targets:
                            renpy.hide(target.betag)
                            renpy.show(target.betag, what=target.besprite, at_list=[Transform(pos=target.cpos)], zorder=target.besk["zorder"])
                    
                # Shatter or some other death effect we want to handle in this method:
                if died and self.death_effect == "shatter":
                    for target in died:
                        renpy.hide(target.betag)
                        renpy.show(target.betag, what=HitlerKaputt(target.besprite, 30), at_list=[Transform(pos=target.cpos)], zorder=target.besk["zorder"])
                
                total_pause = self.td_gfx[0]
                if len(self.td_gfx) > 1:
                    total_pause = total_pause + self.td_gfx[2]
                    
                # Check we need any more pause:
                if self.pause > total_pause:
                    renpy.pause(self.pause - total_pause)
                    
                for i in xrange(len(targets)):
                    gfxtag = "attack" + str(i)
                    renpy.hide(gfxtag)
                    
                # Check if we need any more pause before we kill the battle bounce:
                if self.pause - total_pause < 1.7:
                    renpy.pause(1.7 - (self.pause - total_pause))
                
                
    class P2P_MagicAttack(SimpleMagicalAttack):
        """ ==> @Review: There may not be a good reason for this to be a magical attack instead of any attack at all!
        Point to Point magical strikes without any added effects. This is one step simpler than the MagicArrows attack.
        Used to attacks like FireBall.
        """
        def __init__(self, name, aim="center", xo=0, yo=0, pause=0.4, pause2=0.4, cost=5, anchor=(0.5, 0.5), gfx2=None, casting_effects=["default_1", "default"], **kwargs):
            super(P2P_MagicAttack, self).__init__(name, **kwargs)
            
            self.aim = aim
            self.xo = xo
            self.yo = yo
            self.anchor = anchor
            
            # Rest:
            self.cost = cost
            self.pause = pause
            self.pause2 = pause2
            
            self.gfx2 = gfx2
            self.casting_effects = casting_effects
    
        def show_gfx(self, targets):
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            else:
                targets = list(targets)
            
            char = self.source
            target = targets[0]
            
            if not battle.logical:
                # Inicial char move
                battle.move(char, battle.get_cp(char, xo=50), 0.5)
                
                if self.casting_effects[0]:
                    casting_effect(char, self.casting_effects[0], sfx=self.casting_effects[1])
            
            self.effects_resolver(targets)
            self.apply_effects(targets)
            
            if not battle.logical:
                if self.sfx:
                    if isinstance(self.sfx, (list, tuple)):
                        sfx = choice(self.sfx)
                    else:
                        sfx = self.sfx
                    renpy.sound.play(sfx)
                    
                if battle.get_cp(char)[0] > battle.get_cp(target)[0]:
                    missle = Transform(self.gfx, zoom=-1, xanchor=1.0)
                else:
                    missle = self.gfx
                    
                initpos = battle.get_cp(char, type="fc", xo=60)
                aimpos = battle.get_cp(target, type="center")
                renpy.show("launch", what=missle, at_list=[move_from_to_pos_with_easeout(start_pos=initpos, end_pos=aimpos, t=self.pause), Transform(anchor=(0.5, 0.5))], zorder=target.besk["zorder"]+50)
                renpy.pause(self.pause)
                
                renpy.hide("launch")
                renpy.with_statement(Dissolve(0.2))
                renpy.show("impact", what=self.gfx2, at_list=[Transform(pos=aimpos, anchor=(0.5, 0.5))], zorder=target.besk["zorder"]+51)
                renpy.pause(0.1)
                self.show_gfx_dmg(target)
                
                renpy.pause(self.pause2)
                # Time to move character back to it's positions as well:
                battle.move(char, char.dpos, 0.5, pause=False)
                
                renpy.hide("impact")
                # renpy.with_statement(dissolve)
                # renpy.pause(1.5)
                # renpy.hide("bounce")
            
                
    class MagicArrows(P2P_MagicAttack):
        """This is the class I am going to comment out really well because this spell was not originally created by me
        and yet I had to rewrite it completely for new BE.
        """
        def __init__(self, name, aim="center", xo=0, yo=0, pause=0.4, cost=5, anchor=(0.5, 0.5), gfx2=None, gfx3=None, **kwargs):
            super(MagicArrows, self).__init__(name, **kwargs)
            
            # Aiming properties: What these are will be explained in the show_gfx method.
            self.aim = aim
            self.xo = xo
            self.yo = yo
            self.anchor = anchor
            
            # Rest:
            self.cost = cost # We add this because it is a magical spell, it's cost and damage will be resolved by Parent classes so we don't need to worry about that.
            self.pause = pause # This is not particulary useful for this spell since it's custom made, but we'll keep it just in case. There is no requirement to ues it.
            
            self.gfx2 = gfx2
            self.gfx3 = gfx3 # Since we want to reuse this for Fire and Ice arrows, we'll add two new properties. Since delays are always the same, we're not going to add those.
            

        def show_gfx(self, targets):
            # ALL of the graphical effects are handled in this method. This is also the only method we'll override from the parent since we're happy with everything else!
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            else:
                targets = list(targets)
            # This is a check to see nothing goes wrong. It has no effect value.   
            
            char = self.source # Just a simple reasignment for convinience, this is the source of the attack (Attacker).
            target = targets[0] # We can do this since we're sure that there is only one target for this spell.
            
            if not battle.logical:
                # This returns the position of battle sprite (To be exact, it return the position of TOP, LEFT CORNER of the battle sprite, this is it's default behavior).
                # xo is means we want to adjust position alogn the x axis. xo with value of -30 plainly means 30 pixels backwards (to the side characters back is pointed to).
                newpos = battle.get_cp(char, xo=-30)
                
                # Inicial movement of the sprtite:
                # renpy.hide(char.betag) # We need to hide the sprite that we're looking at (this will not create any kind of visible effect, just a programming thing).
                # # Renpy show function is what we use here to display stuff on the screen where:
                # """
                # char.betag: name (tag) assigned to this show command so we can hide/replace it.
                # what=char.besprite: This is the battle_sprite image.
                # at_list=[move_from_to_pos_with_ease(start_pos=char.dpos, end_pos=newpos, t=0.5)]: At list takes a set of ATL instructions and executes them. ATL is the Animation and Transformation Language of Ren'Py.
                # You can find more about it in the Ren'Py Documentation.
                # zorder=char.besk["zorder"]: Ren'Py will show stuff with higher zorder infront of the stuff with lower zorder. It's as simple as that. char.best is the dict where we keep our dedault values for the character.
                # You can just follow the lead with zorders from the examples.
                # """
                # renpy.show(char.betag, what=char.besprite, at_list=[move_from_to_pos_with_ease(start_pos=char.dpos, end_pos=newpos, t=0.5)], zorder=char.besk["zorder"]) # So this moves the character slightly to the back.
                # renpy.pause(0.5) # Need to add pauses for effects to take place!
                ### >>> Now done through move method:
                battle.move(char, battle.get_cp(char, xo=50), 0.5)
            
            # This two functions do the actual calculation of the damage:
            self.effects_resolver(targets) # This can also be moved elsewhere. This causes the actual damage.
            self.apply_effects(targets) # This can also be moved elsewhere. This causes the actual damage.
            
            if not battle.logical:
                # Sound: We don't really need the checks here since all our arrow spells have sound... but I copied this from elsewhere :)
                if self.sfx:
                    if isinstance(self.sfx, (list, tuple)):
                        sfx = choice(self.sfx)
                    else:
                        sfx = self.sfx
                    renpy.sound.play(sfx)
                    
                # We need to make sure that attack sprites are facing the correct way:
                if battle.get_cp(char)[0] > battle.get_cp(target)[0]:
                    castsprite = Transform(self.gfx, zoom=-1, xanchor=1.0) # We also need to add yanchor here for obvious reasons.
                    arrowsprite = Transform(self.gfx2, zoom=-1, xanchor=1.0)
                else:
                    castsprite = self.gfx
                    arrowsprite = self.gfx2
                    
                # We need to apply all effects here simulteniously (Unline in Jake's BE where damage is aftereffect *Damage as aftereffect is obviously also perfectly possible to all or one by one as in Jake's BE)
                castpos = battle.get_cp(char, type="fc", xo=-60) # Ok, so get_cp method we've covered. "fc" returns front center position of the image. We add a xo as well because we've moved the sprite and this animation has a large empty space space...
                # I think the bow looks looker infront of the sprite but feel free to change this.
                renpy.show("casting", what=castsprite, at_list=[Transform(pos=castpos, yanchor=0.5)], zorder=char.besk["zorder"]+50)
                renpy.pause(0.6)
    
                
                # Next lets do the flying animation:
                aimpos = battle.get_cp(target, type="center", yo=-20) # We want to aim slight above the center of the enemy sprite, which is usually the heart :)
                # move_from_to_pos_with_easeout are the transform instruction that tell something to start moving slow, going increasingly faster the closer they get to the target.
                renpy.show("fly", what=arrowsprite, at_list=[move_from_to_pos_with_easeout(start_pos=castpos, end_pos=aimpos, t=0.4), Transform(yanchor=0.5)], zorder=target.besk["zorder"]+51)
                renpy.pause(0.4)
                
                renpy.hide("fly")
                # renpy.with_statement(Dissolve(0.2))
                renpy.pause(0.01)
                
                # Last we can just add the impact, it doesn't need to be flipped and can be put right at the aiming position:
                renpy.show("impact", what=self.gfx3, at_list=[Transform(pos=aimpos, anchor=(0.5, 0.5))], zorder=target.besk["zorder"]+52)
                renpy.pause(0.01) # We'll wait for 0.2 seconds and add the bouncing effect
                
                # txt = Text("%s"%target.beeffects[0], style="content_label", color=crimson, size=20) # We'll make it larger and in crimson color cause it's a cool attack :)
                # renpy.show("bounce", what=txt, at_list=[battle_bounce(battle.get_cp(target, type="tc", yo=-10))], zorder=target.besk["zorder"]+53)
                # renpy.pause(0.01)
                # @Review, replaced with:
                self.show_gfx_dmg(target)
                
                renpy.hide("casting")
                renpy.with_statement(Dissolve(1.0)) # Cool effect for hiding :)
                
                renpy.pause(0.1)
                # Time to move character back to it's positions as well:
                battle.move(char, char.dpos, 0.5, pause=False)
                
                renpy.pause(0.7)
                renpy.hide("impact")
                renpy.with_statement(Dissolve(0.3))
                # renpy.pause(0.2) # Just for the good count :)
                # renpy.hide("bounce")
            
                
    class BasicHealingSpell(SimpleMagicalAttack):
        def __init__(self, name, aim="bc", xo=0, yo=0, pause=0.5, cost=5, anchor=(0.5, 1.0), type="sa", casting_effects=["default_1", "default"], **kwargs):
            super(SimpleMagicalAttack, self).__init__(name, type=type, **kwargs)
            
            # Aiming properties:
            self.aim = aim
            self.xo = xo
            self.yo = yo
            
            # Rest:
            self.cost = cost
            self.anchor = anchor
            self.pause = pause
            
            self.casting_effects = casting_effects
            
        def effects_resolver(self, targets):
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            char = self.source
            attributes = self.attributes
                
            restore = self.effect + (char.intelligence + char.magic) * 0.25
            
            for t in targets:
                if not self.check_resistance(t):
                    # We get the mupliplier and any effects that those may bring.
                    effects, multiplier = self.get_attributes_multiplier(t, attributes)
                    restore = int(restore*multiplier)
                else: # resisted
                    damage = 0
                    effects = list()
                    effects.append("resisted")
                    
                effects.insert(0, restore)
                t.beeffects = effects
            
                # String for the log:
                # String for the log:
                s = list()
                s.append("%s used %s to restore HP of %s!" % (char.nickname, self.name, t.name))
                
                s = s + self.effects_for_string(t, default_color="green")
                
                battle.log("".join(s))
            
        def apply_effects(self, targets):
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            for t in targets:
                t.mod("health", t.beeffects[0])
                    
        def show_gfx(self, targets):
            # Simple effects for the magic attack:
            char = self.source
            
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
                
            if not battle.logical:
                if self.casting_effects[0]:
                    casting_effect(char, self.casting_effects[0], sfx=self.casting_effects[1])
            
            self.effects_resolver(targets) # This can also be moved elsewhere. This causes the actual damage.
            self.apply_effects(targets) # This can also be moved elsewhere. This causes the actual damage.
            
            if not battle.logical:
                if self.sfx:
                    if isinstance(self.sfx, (list, tuple)):
                        sfx = choice(self.sfx)
                    else:
                        sfx = self.sfx
                    renpy.sound.play(sfx)
                
                # Zoom (If any):
                if self.zoom is not None:
                    gfx = Transform(self.gfx, zoom=self.zoom)
                else:
                    gfx = self.gfx
                    
                # We need to apply all effects here simulteniously (Unline in Jake's BE where damage is aftereffect *Damage as aftereffect is obviously also perfectly possible to all or one by one as in Jake's BE)    
                if self.gfx:
                    for index, target in enumerate(targets):
                        gfxtag = "heal" + str(index)
                        renpy.show(gfxtag, what=gfx, at_list=[Transform(pos=battle.get_cp(target, type=self.aim, xo=self.xo, yo=self.yo), anchor=self.anchor)], zorder=target.besk["zorder"]+1)
                renpy.pause(0.1)
                for index, target in enumerate(targets):
                    bbtag = "bb" + str(index)
                    txt = Text("%s"%target.beeffects[0], style="content_label", color=green, size=15)
                    renpy.show(bbtag, what=txt, at_list=[battle_bounce(battle.get_cp(target, type="tc", yo=-10))], zorder=target.besk["zorder"]+2)
                
                renpy.pause(self.pause - 0.1)
                for i in xrange(len(targets)):
                    gfxtag = "heal" + str(i)
                    renpy.hide(gfxtag)
                    
                if self.pause - 0.1 < 1.7:
                    renpy.pause(1.7 - (self.pause - 0.1))
                for i in xrange(len(targets)):
                    bbtag = "bb" + str(i)
                    renpy.hide(bbtag)
                
                
    class BasicPoisonSpell(SimpleMagicalAttack):
        def __init__(self, *args, **kwargs):
            super(BasicPoisonSpell, self).__init__(*args, **kwargs)
            
        def effects_resolver(self, targets):
            """Logical effect of the action. More often than not, it calculates the damage.
            
            Expects a list or tuple with targets.
            This should return it's results through PytCharacters property called damage so the show_gfx method can be adjusted accordingly.
            But it is this method that writes to the log to be displayed later... (But you can change even this :D)
            """
            # prepare the variables:
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            a = self.source
            for t in targets:
                # Make sure target does not resist poison by nature:
                if "poison" in t.resist:
                    battle.log("%s resisted poison!" % t.nickname)
                    t.beeffects = [0]
                    continue
                # Target resisted due to stats being too l33t:
                elif (t.intelligence + t.luck) > (a.intelligence + a.luck) * 1.3:
                    battle.log("%s not skilled enough to poison %s!" % (a.nickname, t.nickname))
                    t.beeffects = [0]
                    continue
                # And last, in case target is already poisoned:
                for ev in store.battle.mid_turn_events:
                    if t == ev.target and "poison" in ev.attributes:
                        battle.log("%s is already poisoned!" % (t.nickname))
                        t.beeffects = [0]
                        break
                else: # Damage Calculations:
                    effects, multiplier = self.get_attributes_multiplier(t, self.attributes)
                    
                    damage = t.get_max("health") * (self.effect/1000.0)
                    damage = max(randint(15, 20), int(damage) + randint(-4, 4))
                    
                    # Lets check the absobtion:
                    result = self.check_absorbtion(t)
                    if result:
                        damage = damage * -1 * result
                        effects.append("absorbed")
                    effects.insert(0, damage)
                    
                    battle.mid_turn_events.append(PoisonEvent(t, a, damage))
                    
                    t.beeffects = effects
                    # String for the log:
                    s = list()
                    s.append("{color=[teal]}%s{/color} poisoned %s!" % (a.nickname, t.nickname))
                    
                    s = s + self.effects_for_string(t)
                    
                    battle.log("".join(s))
 
            
init python: # Helper Functions:
    def death_effect(char, kind, sfx=None, pause=False):
        if kind == "shatter":
            pass
    
    def casting_effect(char, kind, sfx="default", pause=True):
        """
        GFX and SFX effects on the caster of any attack (usually magic).
        """
        if sfx and sfx == "default":
            sfx = "content/sfx/sound/be/casting_1.mp3"
        if kind == "orb":
            if sfx:
                renpy.sound.play(sfx)
            renpy.show("casting", what=Transform("cast_orb_1", zoom=1.85),  at_list=[Transform(pos=battle.get_cp(char, type="center"), align=(0.5, 0.5))], zorder=char.besk["zorder"]+1)
            if pause:
                renpy.pause(0.84)
                renpy.hide("casting")
        elif kind in ["dark_1", "light_1", "water_1", "air_1", "fire_1", "earth_1", "electricity_1", "ice_1"]:
            if sfx:
                renpy.sound.play(sfx)
            renpy.show("casting", what=Transform("cast_" + kind, zoom=1.5),  at_list=[Transform(pos=battle.get_cp(char, type="bc", yo=-75), align=(0.5, 0.5))], zorder=char.besk["zorder"]+1)
            if pause:
                renpy.pause(0.84)
                renpy.hide("casting")
        elif kind in ["dark_2", "light_2", "water_2", "air_2", "fire_2", "earth_2", "ice_2", "electricity_2"]:
            if sfx:
                renpy.sound.play(sfx)
            renpy.show("casting", what=Transform("cast_" + kind, zoom=0.9),  at_list=[Transform(pos=battle.get_cp(char, type="center"), align=(0.5, 0.5))], zorder=char.besk["zorder"]+1)
            if pause:
                renpy.pause(1.4)
                renpy.hide("casting")
        elif kind == "default_1":
            if sfx:
                renpy.sound.play(sfx)
            renpy.show("casting", what=Transform("cast_default_1", zoom=1.6),  at_list=[Transform(pos=battle.get_cp(char, type="bc"), align=(0.5, 0.5))], zorder=char.besk["zorder"]-1)
            if pause:
                renpy.pause(1.12)
                renpy.hide("casting")
        elif kind == "circle_1":
            if sfx:
                renpy.sound.play(sfx)
            renpy.show("casting", what=Transform("cast_circle_1", zoom=1.9),  at_list=[Transform(pos=battle.get_cp(char, type="bc", yo=-10), align=(0.5, 0.5))], zorder=char.besk["zorder"]-1)
            if pause:
                renpy.pause(1.05)
                renpy.hide("casting")
        elif kind == "circle_2":
            if sfx:
                renpy.sound.play(sfx)
            renpy.show("casting", what=Transform("cast_circle_2", zoom=1.8),  at_list=[Transform(pos=battle.get_cp(char, type="bc", yo=-100), align=(0.5, 0.5))], zorder=char.besk["zorder"]+1)
            if pause:
                renpy.pause(1.1)
                renpy.hide("casting")
        elif kind == "circle_3":
            if sfx:
                renpy.sound.play(sfx)
            renpy.show("casting", what=Transform("cast_circle_3", zoom=1.8),  at_list=[Transform(pos=battle.get_cp(char, type="bc", yo=-100), align=(0.5, 0.5))], zorder=char.besk["zorder"]+1)
            if pause:
                renpy.pause(1.03)
                renpy.hide("casting")
        elif kind == "runes_1":
            if sfx:
                renpy.sound.play(sfx)
            renpy.show("casting", what=Transform("cast_runes_1", zoom=1.1),  at_list=[Transform(pos=battle.get_cp(char, type="bc", yo=-50), align=(0.5, 0.5))], zorder=char.besk["zorder"]-1)
            if pause:
                renpy.pause(0.75)
                renpy.hide("casting")
        
