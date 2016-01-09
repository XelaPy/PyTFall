init python:
    # Plain Events:
    class BE_Skip(BE_Event):
        """
        Simplest possible class that just skips the turn for the player and logs that fact.
        This can/should be a function but heck :D
        """
        def __init__(self, source=None):
            self.source = source
        
        def __call__(self, *args, **kwargs):
            msg = "{} skips a turn!".format(self.source.nickname)
            battle.log(msg)
            

    class RPG_Death(BE_Event):
        """
        Used to instantiate death and kill off a player at the end of any turn...
        """
        def __init__(self, target, death_effect=None, msg=None):
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
            
            if self.death_effect == "dissolve":
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
                t.mod("health", -damage)
                msg = "{color=[red]}%s is poisoned!! DMG: %d{/color}" % (self.target.name, damage)
                battle.log(msg)
            else:
                death = RPG_Death(self.target, msg="{color=[red]}Poison took out %s!\n{/color}" % self.target.name, death_effect="dissolve")
                death.apply_effects()
                
            self.counter -= 1
            
            if self.counter <= 0:
                msg = "{color=[red]}Poison effect on %s has ran it's course...{/color}" % (self.target.name)
                battle.log(msg)
            
    # Actions:
    # Simple Attack:
    class SimpleAttack(BE_Action):
        """Simplest attack, usually weapons.
        
        @Review: This will be the base for all attacks from here on out and accept all default properties relevant to Attack Skills! 
        """
        def __init__(self, name,
                           attacker_action={},
                           attacker_effects={},
                           main_effect={}, # Start @ is not working atm.
                           target_sprite_damage_effect={},
                           target_damage_effect={},
                           target_death_effect={},
                           sfx=None, gfx=None, zoom=None, # <=== These three should die off in time!
                           **kwargs):
            super(SimpleAttack, self).__init__(name,
                                                                   attacker_action=attacker_action,
                                                                   attacker_effects=attacker_effects,
                                                                   main_effect=main_effect,
                                                                   target_sprite_damage_effect=target_sprite_damage_effect,
                                                                   target_damage_effect=target_damage_effect,
                                                                   target_death_effect=target_death_effect,
                                                                   sfx=sfx,
                                                                   gfx=gfx,
                                                                   **kwargs)
            
            self.attacker_action["gfx"] = self.attacker_action.get("gfx", "step_forward")
            self.attacker_action["sfx"] = self.attacker_action.get("sfx", None)
            
            self.main_effect["duration"] = self.main_effect.get("duration", 0.1)
            
            self.target_sprite_damage_effect["shake"] = self.target_sprite_damage_effect.get("gfx", "shake")
            self.target_sprite_damage_effect["initial_pause"] = self.target_sprite_damage_effect.get("initial_pause", 0.1)
            self.target_sprite_damage_effect["duration"] = self.target_sprite_damage_effect.get("duration", self.main_effect["duration"])
            
            self.target_damage_effect["gfx"] = self.target_damage_effect.get("gfx", "battle_bounce")
            self.target_damage_effect["initial_pause"] = self.target_damage_effect.get("initial_pause", 0.1)
            
            self.target_death_effect["gfx"] = self.target_death_effect.get("gfx", "dissolve")
            self.target_death_effect["initial_pause"] = self.target_death_effect.get("initial_pause", 0.2)
            self.target_death_effect["duration"] = self.target_death_effect.get("duration", 0.5)
            
            
    class SimpleMagicalAttack(BE_Action):
        """Simplest attack, usually simple magic.
        """
        def __init__(self, name, cost=5,
                           attacker_action={},
                           attacker_effects={},
                           main_effect={},
                           target_sprite_damage_effect={},
                           target_damage_effect={},
                           target_death_effect={},
                           sfx=None, gfx=None, zoom=None, aim=None, xo=0, yo=0, pause=None, anchor=None, casting_effects=None, target_damage_gfx=None, # <=== These should die off in time!
                           **kwargs):
            super(SimpleMagicalAttack, self).__init__(name,
                                                                               attacker_action=attacker_action,
                                                                               attacker_effects=attacker_effects,
                                                                               main_effect=main_effect,
                                                                               target_sprite_damage_effect=target_sprite_damage_effect,
                                                                               target_damage_effect=target_damage_effect,
                                                                               target_death_effect=target_death_effect,
                                                                               sfx=sfx, gfx=gfx, pause=pause, zoom=zoom,
                                                                               **kwargs)
            
            # GFX properties:
            if aim:
                self.main_effect["aim"]["point"] = aim
            if xo:
                self.main_effect["aim"]["xo"] = xo
            if yo:
                self.main_effect["aim"]["yo"] = yo
            if anchor:
                self.main_effect["aim"]["anchor"] = anchor
            if casting_effects:
                self.attacker_effects["gfx"] = casting_effects[0]
                self.attacker_effects["sfx"] = casting_effects[1]
            if target_damage_gfx:
                self.target_sprite_damage_effect["initial_pause"] = target_damage_gfx[0]
                self.target_sprite_damage_effect["gfx"] = target_damage_gfx[1]
                self.target_sprite_damage_effect["duration"] = target_damage_gfx[2]
                
            # Rest:
            self.cost = cost
            
            self.attacker_action["gfx"] = self.attacker_action.get("gfx", "step_forward")
            self.attacker_action["sfx"] = self.attacker_action.get("sfx", None)
            
            self.main_effect["duration"] = self.main_effect.get("duration", 0.5)
            
            self.target_sprite_damage_effect["shake"] = self.target_sprite_damage_effect.get("gfx", "shake")
            self.target_sprite_damage_effect["initial_pause"] = self.target_sprite_damage_effect.get("initial_pause", 0.2)
            self.target_sprite_damage_effect["duration"] = self.target_sprite_damage_effect.get("duration", self.main_effect["duration"])
            
            self.target_damage_effect["gfx"] = self.target_damage_effect.get("gfx", "battle_bounce")
            self.target_damage_effect["initial_pause"] = self.target_damage_effect.get("initial_pause", 0.21)
            
            self.target_death_effect["gfx"] = self.target_death_effect.get("gfx", "dissolve")
            self.target_death_effect["initial_pause"] = self.target_death_effect.get("initial_pause", self.target_sprite_damage_effect["initial_pause"] + 0.1)
            self.target_death_effect["duration"] = self.target_death_effect.get("duration", 0.5)

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
            # Not 100% for that this will be required...
            # Here it is simple since we are only focusing on damaging health:
            # prepare the variables:
            died = list()
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            for t in targets:
                if t.health - t.beeffects[0] > 0:
                    t.mod("health", -t.beeffects[0])
                else:
                    battle.end_turn_events.append(RPG_Death(t))
                    died.append(t)
                    
            # Here we need to take of MP:
            self.source.mp -= self.cost
            return died
            
            
    class ArealMagicalAttack(SimpleMagicalAttack):
        """
        Simplest attack, usually simple magic.
        """
        def __init__(self, name, **kwargs):
            super(ArealMagicalAttack, self).__init__(name, **kwargs)

        def show_main_gfx(self, battle, attacker, targets):
            # Shows the MAIN part of the attack and handles appropriate sfx.
            gfx = self.main_effect["gfx"]
            sfx = self.main_effect["sfx"]
            
            # SFX:
            sfx = choice(sfx) if isinstance(sfx, (list, tuple)) else sfx
            if sfx:
                renpy.sound.play(sfx)
            
            # GFX:
            if gfx:
                # Flip the attack image if required:
                if self.main_effect.get("hflip", False):
                    gfx = Transform(gfx, xzoom=-1) if battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0] else gfx
                
                target = targets[0]
                teampos = target.beteampos
                aim = self.main_effect["aim"]
                point = aim.get("point", "center")
                anchor = aim.get("anchor", (0.5, 0.5))
                xo = aim.get("xo", 0)
                yo = aim.get("yo", 0)
                
                gfxtag = "areal"
                if teampos == "l":
                    teampos = BDP["perfect_middle_right"]
                else:
                    teampos = BDP["perfect_middle_left"]
                renpy.show(gfxtag, what=gfx, at_list=[Transform(pos=battle.get_cp(target, type=point, xo=xo, yo=yo, override=teampos), anchor=anchor)], zorder=1000)
                
        def hide_main_gfx(self, targets):
            renpy.hide("areal")
                
                
    class P2P_MagicAttack(SimpleMagicalAttack):
        """ ==> @Review: There may not be a good reason for this to be a magical attack instead of any attack at all!
        Point to Point magical strikes without any added effects. This is one step simpler than the MagicArrows attack.
        Used to attacks like FireBall.
        """
        def __init__(self, name, projectile_effects={}, **kwargs):
            super(P2P_MagicAttack, self).__init__(name, **kwargs)
            
            self.projectile_effects = deepcopy(projectile_effects)
            
        def show_main_gfx(self, battle, attacker, targets):
            # We simply want to add projectile effect here:
            pro_gfx = self.projectile_effects["gfx"]
            pro_sfx = self.projectile_effects["sfx"]
            pro_sfx = choice(pro_sfx) if isinstance(pro_sfx, (list, tuple)) else pro_sfx
            pause = self.projectile_effects["duration"]
            
            missle = Transform(pro_gfx, zoom=-1, xanchor=1.0) if battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0] else pro_gfx
            
            initpos = battle.get_cp(attacker, type="fc", xo=60)
            
            if pro_sfx:
                renpy.sound.play(pro_sfx)
            
            for index, target in enumerate(targets):
                aimpos = battle.get_cp(target, type="center")
                renpy.show("launch" + str(index), what=missle, at_list=[move_from_to_pos_with_easeout(start_pos=initpos, end_pos=aimpos, t=pause), Transform(anchor=(0.5, 0.5))], zorder=target.besk["zorder"]+50)
                
            renpy.pause(pause)
                
            for index, target in enumerate(targets):
                renpy.hide("launch" + str(index))
            
            # Shows the MAIN part of the attack and handles appropriate sfx.
            gfx = self.main_effect["gfx"]
            sfx = self.main_effect["sfx"]
            
            # SFX:
            sfx = choice(sfx) if isinstance(sfx, (list, tuple)) else sfx
            if sfx:
                renpy.sound.play(sfx)
            
            # GFX:
            if gfx:
                # pause = self.main_effect["duration"]
                aim = self.main_effect["aim"]
                point = aim.get("point", "center")
                anchor = aim.get("anchor", (0.5, 0.5))
                xo = aim.get("xo", 0)
                yo = aim.get("yo", 0)
                
                for index, target in enumerate(targets):
                    gfxtag = "attack" + str(index)
                    renpy.show(gfxtag, what=gfx, at_list=[Transform(pos=battle.get_cp(target, type=point, xo=xo, yo=yo), anchor=anchor)], zorder=target.besk["zorder"]+51)
                
        def hide_main_gfx(self, targets):
            for i in xrange(len(targets)):
                gfxtag = "attack" + str(i)
                renpy.hide(gfxtag)
            
                
    class P2P_ArealMagicalAttack(P2P_MagicAttack):
        """ ==> @Review: There may not be a good reason for this to be a magical attack instead of any attack at all!
        Point to Point magical strikes without any added effects. This is one step simpler than the MagicArrows attack.
        Used to attacks like FireBall.
        """
        def __init__(self, name, **kwargs):
            super(P2P_ArealMagicalAttack, self).__init__(name, **kwargs)
    
        def show_main_gfx(self, battle, attacker, targets):
            # We simply want to add projectile effect here:
            pro_gfx = self.projectile_effects["gfx"]
            pro_sfx = self.projectile_effects["sfx"]
            pro_sfx = choice(pro_sfx) if isinstance(pro_sfx, (list, tuple)) else pro_sfx
            pause = self.projectile_effects["duration"]
            
            target = targets[0]
            
            missle = Transform(pro_gfx, zoom=-1, xanchor=1.0) if battle.get_cp(attacker)[0] > battle.get_cp(target)[0] else pro_gfx
            
            initpos = battle.get_cp(attacker, type="fc", xo=60)
            
            if pro_sfx:
                renpy.sound.play(pro_sfx)
            
            aimpos = BDP["perfect_middle_right"] if target.beteampos == "l" else BDP["perfect_middle_left"]
            
            renpy.show("launch", what=missle, at_list=[move_from_to_pos_with_easeout(start_pos=initpos, end_pos=aimpos, t=pause), Transform(anchor=(0.5, 0.5))], zorder=target.besk["zorder"]+1000)
            renpy.pause(pause)
            renpy.hide("launch")
            
            # Shows the MAIN part of the attack and handles appropriate sfx.
            gfx = self.main_effect["gfx"]
            sfx = self.main_effect["sfx"]
            
            # SFX:
            sfx = choice(sfx) if isinstance(sfx, (list, tuple)) else sfx
            if sfx:
                renpy.sound.play(sfx)
            
            # GFX:
            if gfx:
                aim = self.main_effect["aim"]
                point = aim.get("point", "center")
                anchor = aim.get("anchor", (0.5, 0.5))
                xo = aim.get("xo", 0)
                yo = aim.get("yo", 0)
                
                renpy.show("projectile", what=gfx, at_list=[Transform(pos=aimpos, anchor=anchor)], zorder=target.besk["zorder"]+1001)
                
        def hide_main_gfx(self, targets):
            renpy.hide("projectile")
            
                
    class MagicArrows(P2P_MagicAttack):
        """This is the class I am going to comment out really well because this spell was not originally created by me
        and yet I had to rewrite it completely for new BE.
        """
        def __init__(self, name, firing_effects={}, **kwargs):
            super(MagicArrows, self).__init__(name, **kwargs)
            
            self.firing_effects = deepcopy(firing_effects)
            
        def show_main_gfx(self, battle, attacker, targets):
            firing_gfx = self.firing_effects["gfx"]
            firing_sfx = self.firing_effects["sfx"]
            firing_sfx = choice(firing_sfx) if isinstance(firing_sfx, (list, tuple)) else firing_sfx
            # pause = self.firing_effects["duration"]
            
            bow = Transform(firing_gfx, zoom=-1, xanchor=1.0) if battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0] else firing_gfx
            
            if firing_sfx:
                renpy.sound.play(firing_sfx)
                
            castpos = battle.get_cp(attacker, type="fc", xo=30)
                
            renpy.show("casting", what=bow, at_list=[Transform(pos=castpos, yanchor=0.5)], zorder=attacker.besk["zorder"]+50)
            renpy.pause(0.6)
            
            # We simply want to add projectile effect here:
            pro_gfx = self.projectile_effects["gfx"]
            pro_sfx = self.projectile_effects["sfx"]
            pro_sfx = choice(pro_sfx) if isinstance(pro_sfx, (list, tuple)) else pro_sfx
            pause = self.projectile_effects["duration"]
            
            missle = Transform(pro_gfx, zoom=-1, xanchor=1.0) if battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0] else pro_gfx
            
            if pro_sfx:
                renpy.sound.play(pro_sfx)
            
            castpos = battle.get_cp(attacker, type="fc", xo=75)
                
            for index, target in enumerate(targets):
                aimpos = battle.get_cp(target, type="center", yo=-20)
                renpy.show("launch" + str(index), what=missle, at_list=[move_from_to_pos_with_easeout(start_pos=castpos, end_pos=aimpos, t=pause), Transform(anchor=(0.5, 0.5))], zorder=target.besk["zorder"]+51)
                
            renpy.pause(pause)
                
            for index, target in enumerate(targets):
                renpy.hide("launch" + str(index))
            
            # Shows the MAIN part of the attack and handles appropriate sfx.
            gfx = self.main_effect["gfx"]
            sfx = self.main_effect["sfx"]
            
            # SFX:
            sfx = choice(sfx) if isinstance(sfx, (list, tuple)) else sfx
            if sfx:
                renpy.sound.play(sfx)
            
            # GFX:
            if gfx:
                # pause = self.main_effect["duration"]
                aim = self.main_effect["aim"]
                point = aim.get("point", "center")
                anchor = aim.get("anchor", (0.5, 0.5))
                xo = aim.get("xo", 0)
                yo = aim.get("yo", 0)
                
                for index, target in enumerate(targets):
                    gfxtag = "attack" + str(index)
                    renpy.show(gfxtag, what=gfx, at_list=[Transform(pos=battle.get_cp(target, type=point, xo=xo, yo=yo), anchor=anchor)], zorder=target.besk["zorder"]+52)
                
        def hide_main_gfx(self, targets):
            renpy.hide("casting")
            renpy.with_statement(Dissolve(0.5))
            for i in xrange(len(targets)):
                gfxtag = "attack" + str(i)
                renpy.hide(gfxtag)
            
                
    class ATL_ArealMagicalAttack(ArealMagicalAttack):
        """This one used ATL function for the attack, ignoring all usual targeting options.
        
        As a rule, it expects to recieve left and right targeting option we normally get from team positions for Areal Attacks.
        """
        def __init__(self, name, **kwargs):
            super(ATL_ArealMagicalAttack, self).__init__(name, **kwargs)
            
        def show_main_gfx(self, battle, attacker, targets):
            # Shows the MAIN part of the attack and handles appropriate sfx.
            sfx = self.main_effect["sfx"]
            gfx = self.main_effect["atl"]
            
            # SFX:
            sfx = choice(sfx) if isinstance(sfx, (list, tuple)) else sfx
            if sfx:
                renpy.sound.play(sfx)
            
            # GFX:
            gfx = gfx(*self.main_effect["left_args"]) if battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0] else gfx(*self.main_effect["right_args"])
            gfxtag = "areal"
            renpy.show(gfxtag, what=gfx, zorder=1000)
            
            
    class FullScreenCenteredArealMagicalAttack(ArealMagicalAttack):
        """Simple overwrite, negates offsets and shows the attack over the whole screen aligning it to truecenter.
        """
        def __init__(self, name, **kwargs):
            super(FullScreenCenteredArealMagicalAttack, self).__init__(name, **kwargs)
            
        def show_main_gfx(self, battle, attacker, targets):
            # Shows the MAIN part of the attack and handles appropriate sfx.
            gfx = self.main_effect["gfx"]
            sfx = self.main_effect["sfx"]
            
            # SFX:
            sfx = choice(sfx) if isinstance(sfx, (list, tuple)) else sfx
            if sfx:
                renpy.sound.play(sfx)
            
            # GFX:
            if gfx:
                gfxtag = "areal"
                renpy.show(gfxtag, what=gfx, at_list=[Transform(align=(0.5, 0.5))], zorder=1000)
            
                
    class BasicHealingSpell(SimpleMagicalAttack):
        def __init__(self, name, **kwargs):
            super(BasicHealingSpell, self).__init__(name, **kwargs)
            
        def effects_resolver(self, targets):
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            char = self.source
            attributes = self.attributes
                
            restore = self.effect + (char.intelligence + char.magic) * 0.25
            
            for t in targets:
                if not self.check_resistance(t):
                    # We get the multi and any effects that those may bring.
                    effects, multiplier = self.get_attributes_multiplier(t, attributes)
                    restore = int(restore*multiplier)
                else: # resisted
                    damage = 0
                    effects = list()
                    effects.append("resisted")
                    
                effects.insert(0, restore)
                t.beeffects = effects
                
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
                        damage = -damage * result
                        effects.append("absorbed")
                    effects.insert(0, damage)
                    
                    battle.mid_turn_events.append(PoisonEvent(t, a, damage))
                    
                    t.beeffects = effects
                    # String for the log:
                    s = list()
                    s.append("{color=[teal]}%s{/color} poisoned %s!" % (a.nickname, t.nickname))
                    
                    s = s + self.effects_for_string(t)
                    
                    battle.log("".join(s))
                    
                    
    class ReviveSpell(SimpleMagicalAttack):
        def __init__(self, name, **kwargs):
            super(ReviveSpell, self).__init__(name, **kwargs)
            
        def check_conditions(self, source=None):
            char = source if source else self.source
            if char.mp - self.cost >= 0:
                if self.get_targets(char):
                    return True
                
        def effects_resolver(self, targets):
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            char = self.source
            attributes = self.attributes
            
            for t in targets:
                minh, maxh = int(t.get_max("health")*0.3), int(t.get_max("health")*0.5)
                revive = randint(minh, maxh)
                
                effects = list()
                effects.insert(0, revive)
                t.beeffects = effects
                
                # String for the log:
                s = list()
                s.append("%s brings %s back!" % (char.nickname, t.name))
                
                s = s + self.effects_for_string(t, default_color="green")
                
                battle.log("".join(s))
                
        def apply_effects(self, targets):
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
                
            for t in targets:
                battle.corpses.remove(t)
                minh, maxh = int(t.get_max("health")*0.3), int(t.get_max("health")*0.5)
                t.health = t.beeffects[0]
            return []
            
        def show_main_gfx(self, battle, attacker, targets):
            for target in targets:
                renpy.show(target.betag, what=target.besprite, at_list=[Transform(pos=target.cpos), fade_from_to(start_val=0, end_val=1.0, t=1.0, wait=0.5)], zorder=target.besk["zorder"])
            super(ReviveSpell, self).show_main_gfx(battle, attacker, targets)
        
    
init python: # Helper Functions:
    def death_effect(char, kind, sfx=None, pause=False):
        if kind == "shatter":
            pass
    
    def casting_effect(char, gfx=None, sfx="content/sfx/sound/be/casting_1.mp3", pause=True):
        """GFX and SFX effects on the caster of any attack (usually magic).
        """
        if sfx == "default":
            sfx="content/sfx/sound/be/casting_1.mp3"
        
        if gfx == "orb":
            renpy.show("casting", what=Transform("cast_orb_1", zoom=1.85),  at_list=[Transform(pos=battle.get_cp(char, type="center"), align=(0.5, 0.5))], zorder=char.besk["zorder"]+1)
            pause = 0.84
        elif gfx in ["dark_1", "light_1", "water_1", "air_1", "fire_1", "earth_1", "electricity_1", "ice_1"]:
            renpy.show("casting", what=Transform("cast_" + gfx, zoom=1.5),  at_list=[Transform(pos=battle.get_cp(char, type="bc", yo=-75), align=(0.5, 0.5))], zorder=char.besk["zorder"]+1)
            pause = 0.84
        elif gfx in ["dark_2", "light_2", "water_2", "air_2", "fire_2", "earth_2", "ice_2", "electricity_2"]:
            renpy.show("casting", what=Transform("cast_" + gfx, zoom=0.9),  at_list=[Transform(pos=battle.get_cp(char, type="center"), align=(0.5, 0.5))], zorder=char.besk["zorder"]+1)
            pause = 1.4
        elif gfx == "default_1":
            renpy.show("casting", what=Transform("cast_default_1", zoom=1.6),  at_list=[Transform(pos=battle.get_cp(char, type="bc"), align=(0.5, 0.5))], zorder=char.besk["zorder"]-1)
            pause = 1.12
        elif gfx == "circle_1":
            renpy.show("casting", what=Transform("cast_circle_1", zoom=1.9),  at_list=[Transform(pos=battle.get_cp(char, type="bc", yo=-10), align=(0.5, 0.5))], zorder=char.besk["zorder"]-1)
            pause = 1.05
        elif gfx == "circle_2":
            renpy.show("casting", what=Transform("cast_circle_2", zoom=1.8),  at_list=[Transform(pos=battle.get_cp(char, type="bc", yo=-100), align=(0.5, 0.5))], zorder=char.besk["zorder"]+1)
            pause = 1.1
        elif gfx == "circle_3":
            renpy.show("casting", what=Transform("cast_circle_3", zoom=1.8),  at_list=[Transform(pos=battle.get_cp(char, type="bc", yo=-100), align=(0.5, 0.5))], zorder=char.besk["zorder"]+1)
            pause = 1.03
        elif gfx == "runes_1":
            renpy.show("casting", what=Transform("cast_runes_1", zoom=1.1),  at_list=[Transform(pos=battle.get_cp(char, type="bc", yo=-50), align=(0.5, 0.5))], zorder=char.besk["zorder"]-1)
            pause = 0.75
            
        if sfx:
            renpy.sound.play(sfx)
        if gfx:
            renpy.pause(pause)
            renpy.hide("casting")
