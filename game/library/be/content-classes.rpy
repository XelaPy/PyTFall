init python:
    class MyTimer(renpy.display.layout.Null):
        """
        To Be Moved to appropriate file and vastly improved later!
        Ren'Py's original timer failed completely for chaining sounds in BE, this seems to be working fine.
        """
        def __init__(self, delay, action=None, repeat=False, args=(), kwargs={}, replaces=None, **properties):
            super(MyTimer, self).__init__(**properties)

            if action is None:
                raise Exception("A timer must have an action supplied.")

            if delay <= 0:
                raise Exception("A timer's delay must be > 0.")

            self.started = None

            # The delay.
            self.delay = delay

            # Should we repeat the event?
            self.repeat = repeat

            # The time the next event should occur.
            self.next_event = None

            # The function and its arguments.
            self.function = action
            self.args = args
            self.kwargs = kwargs

            # Did we start the timer?
            self.started = False

            # if replaces is not None:
                # self.state = replaces.state
            # else:
                # self.state = TimerState()


        def render(self, width, height, st, at):
            if self.started is None:
                self.started = st
                renpy.redraw(self, self.delay)
                return renpy.Render(0, 0)

            self.function()
            return renpy.Render(0, 0)


    class ChainedAttack(renpy.Displayable):
        """
        Going to try and chain gfx/sfx for simple BE attacks using a UDD.
        """
        def __init__(self, gfx, sfx, chain_sfx=True, times=2, delay=.3, sd_duration=.75, alpha_fade=.0, webm_size=(), **properties):
            """
            chain_sfx: Do we play the sound and do we chain it?
                True = Play and Chain.
                False = Play once and don't play again.
                None = Do not play SFX at all.
            times = how many times we run the animation in a sequence.
            delay = interval between the two runs.
            sf_duration = single frame duration.
            alpha_fade = Do we want alpha fade for each frame or not. 1.0 means not, .0 means yes and everything in between is partial fade.
            """
            super(ChainedAttack, self).__init__(**properties)

            self.gfx = gfx
            self.sfx = sfx
            self.chain_sfx = chain_sfx
            self.times = times
            self.delay = delay
            self.count = 0
            if webm_size:
                self.size = webm_size
            else:
                self.size = get_size(self.gfx)
            # raise Exception(self.size)
            self.last_flip = None # This is meant to make sure that we don't get two exactly same flips in the row!

            # Timing controls:
            self.next = 0
            self.displayable = [] # List of dict bindings if (D, st) to kill.
            self.single_displayable_duration = sd_duration
            self.alpha_fade = alpha_fade

        def render(self, width, height, st, at):
            # if self.count > self.times:
                # return renpy.Render(0, 0)

            if self.count < self.times and st >= self.next:
                # Prep the data:

                # get the "flip":
                flips = [{"zoom": 1}, {"xzoom": -1}, {"yzoom": -1}, {"zoom": -1}]

                if self.last_flip is None:
                    flip = choice(flips)
                    self.last_flip = flip
                else:
                    flips.remove(self.last_flip)
                    flip = choice(flips)
                    self.last_flip = flip

                # Offset:
                # Adjusting to UDD feature that I do not completely understand...
                offx, offy = choice(range(0, 15) + range(30, 60)), choice(range(0, 15) + range(30, 60))

                # GFX:
                gfx = Transform(self.gfx, **flip)
                gfx = multi_strike(gfx, (offx, offy), st, self.single_displayable_duration, self.alpha_fade)

                # Calc when we add the next gfx and remove the old one from the list. Right now it's a steady stream of ds but I'll prolly change it in the future.
                self.next = st + random.uniform(self.delay*.5, self.delay)
                self.count += 1
                self.displayable.append((gfx, st + self.single_displayable_duration))

                # We can just play the sound here:
                if self.chain_sfx is None:
                    pass
                elif self.chain_sfx is False and self.count == 0 and len(self.displayable) == 1:
                    renpy.play(self.sfx, channel="audio")
                else:
                    renpy.play(self.sfx, channel="audio")

            # Render everything else:
            render = renpy.Render(self.size[0] + 60, self.size[1] + 60)
            for d, t in self.displayable[:]:
                if st <= t:
                    render.place(d)
                else: # Remove if we're done with this displayable:
                    self.displayable.remove((d, t))

            renpy.redraw(self, .1)
            return render


    # Plain Events:
    class RunQuotes(BE_Event):
        def __init__(self, team):
            self.team = team

        def check_conditions(self):
            return True

        def kill(self):
            return True

        def apply_effects(self):
            interactions_prebattle_line(self.team)


    class BE_Skip(BE_Event):
        """
        Simplest possible class that just skips the turn for the player and logs that fact.
        This can/should be a function but heck :D

        This will now also restore 3 - 6% of Vitality!
        """
        def __init__(self, source=None):
            self.source = source

        def __call__(self, *args, **kwargs):
            msg = "{} skips a turn. ".format(self.source.nickname)

            # Restoring Vitality:
            temp = int(self.source.get_max("vitality") * random.uniform(.03, .06))
            self.source.vitality += temp
            msg = msg + "Restored: {color=[green]}%d vitality{/color} points!"%(temp)
            battle.log(msg)


    class Slave_BE_Skip(BE_Event):
        """
        Skipping for slaves. So far only with different message, but there might be more differences in the future.
        """
        def __init__(self, source=None):
            self.source = source

        def __call__(self, *args, **kwargs):
            msg = "{} stands still.".format(self.source.nickname)
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
        def __init__(self, source, target, effect):
            self.target = target
            self.source = source
            self.counter = randint(3, 5) # Poisoned for 3-5 turns
            self.effect = effect # effect should be from 0 to 1, ie part of max health the poison takes every turn
            self.type = "poison"
            self.icon = ProportionalScale("content/gfx/be/poison1.png", 30, 30)

            # We also add the icon to targets status overlay:
            target.status_overlay.append(self.icon)

        def check_conditions(self):
            if battle.controller == self.target:
                return True

        def kill(self):
            if not self.counter:
                self.target.status_overlay.remove(self.icon)
                return True

        def apply_effects(self):
            t = self.target
            s = self.source

            # Damage Calculations:
            damage = t.get_max("health") * self.effect
            damage = max(randint(5, 10), int(damage) + randint(-2, 2))

            # GFX:
            if not battle.logical:
                gfx = Transform("poison_2", zoom=1.5)
                renpy.show("poison", what=gfx, at_list=[Transform(pos=battle.get_cp(t, type="center"), anchor=(.5, .5))], zorder=t.besk["zorder"]+1)
                txt = Text("%d"%damage, style="content_label", color=red, size=15)
                renpy.show("bb", what=txt, at_list=[battle_bounce(store.battle.get_cp(t, type="tc", yo=-10))], zorder=t.besk["zorder"]+2)
                renpy.pause(1.5)
                renpy.hide("poison")
                renpy.pause(.2)
                renpy.hide("bb")

            if t.health - damage > 0:
                t.mod_stat("health", -damage)
                msg = "%s is poisoned! {color=[green]}☠: %d{/color}" % (self.target.name, damage)
                battle.log(msg)
            else:
                death = RPG_Death(self.target, msg="{color=[red]}Poison took out %s!\n{/color}" % self.target.name, death_effect="dissolve")
                death.apply_effects()

            self.counter -= 1

            if self.counter <= 0:
                msg = "{color=[teal]}Poison effect on %s has ran it's course...{/color}" % (self.target.name)
                battle.log(msg)


    class DefenceBuff(BE_Event):
        def __init__(self, source, target, bonus={}, multi=0, icon=None, group=None, gfx_effect="default"):
            # bonus and multi both expect dicts if mods are desirable.
            self.target = target
            self.source = source
            self.type = type
            self.buff = True # We may need this for debuffing later on?

            self.counter = randint(3, 5) # Active for 3-5 turns

            self.icon = icon or ProportionalScale("content/gfx/be/fists.png", 30, 30)
            self.gfx_effect = gfx_effect
            self.activated_this_turn = False # Flag used to pass to gfx methods that this buff was triggered.
            self.group = group # No two buffs from the same group can be applied twice.
            # We also add the icon to targets status overlay:
            target.status_overlay.append(self.icon)

            if bonus:
                self.defence_bonus = bonus
                # if "melee" in self.attributes:
                    # self.defence_bonus["melee"] = int(round(source.defence*.8 + source.constitution*.4) / 3)
                # elif "ranged" in self.attributes:
                    # self.defence_bonus["ranged"] = int(round(source.defence*.8 + source.constitution*.2 + source.agility*.2) / 3)
                # elif "magic" in self.attributes:
                    # self.defence_bonus["magic"] = int(round(source.defence*.8 + source.magic*.3 + source.intelligence*.1) / 3)
                # elif "status" in self.attributes:
                    # self.defence_bonus["status"] = int(round(source.defence*.6 + source.magic*.1 + source.intelligence*.5) / 3)

            if multi:
                self.defence_multiplier = multi

        def check_conditions(self):
            if battle.controller == self.target:
                return True

        def kill(self):
            if not self.counter:
                self.target.status_overlay.remove(self.icon)
                return True

        def apply_effects(self):
            self.counter -= 1

            if self.counter <= 0:
                msg = "{color=[teal]}Defence Buff on %s has warn out!{/color}" % (self.target.name)
                battle.log(msg)


    # Actions:
    class MultiAttack(BE_Action):
        """
        Base class for multi attack skills, which basically show the same displayable and play sounds (conditioned),
        """
        def __init__(self, name, **kwargs):
            super(MultiAttack, self).__init__(name, **kwargs)

        def show_main_gfx(self, battle, attacker, targets):
            # Shows the MAIN part of the attack and handles appropriate sfx.
            gfx = self.main_effect["gfx"]
            sfx = self.main_effect["sfx"]

            times = self.main_effect.get("times", 2)
            interval = self.main_effect.get("interval", .3)
            sd_duration = self.main_effect.get("sd_duration", .3)
            alpha_fade = self.main_effect.get("alpha_fade", .3)
            webm_size  = self.main_effect.get("webm_size", ())

            # GFX:
            if gfx:
                # Flip the attack image if required:
                if self.main_effect.get("hflip", None):
                    gfx = Transform(gfx, xzoom=-1) if battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0] else gfx

                # Posional properties:
                aim = self.main_effect["aim"]
                point = aim.get("point", "center")
                anchor = aim.get("anchor", (.5, .5))
                xo = aim.get("xo", 0)
                yo = aim.get("yo", 0)

                # Create a UDD:
                gfx = ChainedAttack(gfx, sfx, chain_sfx=True, times=times, delay=interval, sd_duration=sd_duration, alpha_fade=alpha_fade, webm_size=webm_size)

                for index, target in enumerate(targets):
                    gfxtag = "attack" + str(index)
                    renpy.show(gfxtag, what=gfx, at_list=[Transform(pos=battle.get_cp(target, type=point, xo=xo, yo=yo), anchor=anchor)], zorder=target.besk["zorder"]+1)


    class ArealSkill(BE_Action):
        """
        Simplest attack, usually simple magic.
        """
        def __init__(self, name, **kwargs):
            super(ArealSkill, self).__init__(name, **kwargs)

        def show_main_gfx(self, battle, attacker, targets):
            # Shows the MAIN part of the attack and handles appropriate sfx.
            gfx = self.main_effect["gfx"]
            sfx = self.main_effect["sfx"]
            loop_sfx = self.main_effect.get("loop_sfx", False)

            # SFX:
            if isinstance(sfx, (list, tuple)):
                if not loop_sfx:
                    sfx = choice(sfx)

            if sfx:
                renpy.music.play(sfx, channel='audio')

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


    class P2P_Skill(BE_Action):
        """ ==> @Review: There may not be a good reason for this to be a magical attack instead of any attack at all!
        Point to Point magical strikes without any added effects. This is one step simpler than the ArrowsSkill attack.
        Used to attacks like FireBall.
        """
        def __init__(self, name, projectile_effects={}, **kwargs):
            super(P2P_Skill, self).__init__(name, **kwargs)

            self.projectile_effects = deepcopy(projectile_effects)

        def show_main_gfx(self, battle, attacker, targets):
            # We simply want to add projectile effect here:
            pro_gfx = self.projectile_effects["gfx"]
            pro_sfx = self.projectile_effects["sfx"]
            pro_sfx = choice(pro_sfx) if isinstance(pro_sfx, (list, tuple)) else pro_sfx
            pause = self.projectile_effects["duration"]

            missle = Transform(pro_gfx, xzoom=-1, xanchor=1.0) if battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0] else pro_gfx

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
                aim = self.main_effect["aim"]
                point = aim.get("point", "center")
                anchor = aim.get("anchor", (0.5, 0.5))
                xo = aim.get("xo", 0)
                yo = aim.get("yo", 0)

                if self.main_effect.get("hflip", False) and battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0]:
                    gfx = Transform(gfx, xzoom=-1)

                for index, target in enumerate(targets):
                    gfxtag = "attack" + str(index)
                    renpy.show(gfxtag, what=gfx, at_list=[Transform(pos=battle.get_cp(target, type=point, xo=xo, yo=yo), anchor=anchor)], zorder=target.besk["zorder"]+51)

        def hide_main_gfx(self, targets):
            for i in xrange(len(targets)):
                gfxtag = "attack" + str(i)
                renpy.hide(gfxtag)


    class P2P_ArealSkill(P2P_Skill):
        """
        Used to attacks like FireBall.
        """
        def __init__(self, name, **kwargs):
            super(P2P_ArealSkill, self).__init__(name, **kwargs)

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


    class ArrowsSkill(P2P_Skill):
        """This is the class I am going to comment out really well because this spell was not originally created by me
        and yet I had to rewrite it completely for new BE.
        """
        def __init__(self, name, firing_effects={}, **kwargs):
            super(ArrowsSkill, self).__init__(name, **kwargs)

            self.firing_effects = deepcopy(firing_effects)

        def show_main_gfx(self, battle, attacker, targets):
            firing_gfx = self.firing_effects["gfx"]
            firing_sfx = self.firing_effects["sfx"]
            firing_sfx = choice(firing_sfx) if isinstance(firing_sfx, (list, tuple)) else firing_sfx
            pause = self.firing_effects.get("duration", .1)

            bow = Transform(firing_gfx, zoom=-1, xanchor=1.0) if battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0] else firing_gfx

            if firing_sfx:
                renpy.sound.play(firing_sfx)

            castpos = battle.get_cp(attacker, type="fc", xo=30)

            renpy.show("casting", what=bow, at_list=[Transform(pos=castpos, yanchor=0.5)], zorder=attacker.besk["zorder"]+50)
            if pause > .6:
                renpy.pause(pause)
            else:
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


    class ATL_ArealSkill(ArealSkill):
        """This one used ATL function for the attack, ignoring all usual targeting options.

        As a rule, it expects to recieve left and right targeting option we normally get from team positions for Areal Attacks.
        """
        def __init__(self, name, **kwargs):
            super(ATL_ArealSkill, self).__init__(name, **kwargs)

        def show_main_gfx(self, battle, attacker, targets):
            # Shows the MAIN part of the attack and handles appropriate sfx.
            sfx = self.main_effect["sfx"]
            gfx = self.main_effect["atl"]
            loop_sfx = self.main_effect.get("loop_sfx", False)

            # SFX:
            if isinstance(sfx, (list, tuple)):
                if not loop_sfx:
                    sfx = choice(sfx)

            if sfx:
                renpy.music.play(sfx, channel='audio')

            # GFX:
            gfx = gfx(*self.main_effect["left_args"]) if battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0] else gfx(*self.main_effect["right_args"])
            gfxtag = "areal"
            renpy.show(gfxtag, what=gfx, zorder=1000)


    class FullScreenCenteredArealSkill(ArealSkill):
        """Simple overwrite, negates offsets and shows the attack over the whole screen aligning it to truecenter.
        """
        def __init__(self, name, **kwargs):
            super(FullScreenCenteredArealSkill, self).__init__(name, **kwargs)

        def show_main_gfx(self, battle, attacker, targets):
            # Shows the MAIN part of the attack and handles appropriate sfx.
            gfx = self.main_effect["gfx"]
            sfx = self.main_effect["sfx"]
            loop_sfx = self.main_effect.get("loop_sfx", False)

            # SFX:
            if isinstance(sfx, (list, tuple)):
                if not loop_sfx:
                    sfx = choice(sfx)

            if sfx:
                renpy.music.play(sfx, channel='audio')

            # GFX:
            if gfx:
                gfxtag = "areal"
                renpy.show(gfxtag, what=gfx, at_list=[Transform(align=(0.5, 0.5))], zorder=1000)


    class BasicHealingSpell(BE_Action):
        def __init__(self, name, **kwargs):
            super(BasicHealingSpell, self).__init__(name, **kwargs)

        def effects_resolver(self, targets):
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            source = self.source
            attributes = self.attributes
            base_restore = self.get_attack()

            for t in targets:
                base_restore = t.get_max("health") * self.effect
                effects = []

                # We get the multi and any effects that those may bring:
                restore = self.damage_modifier(t, base_restore, "healing")
                if restore == "resisted":
                    restore = 0

                restore = int(round(restore))
                effects.append(("healing", restore))

                t.dmg_font = "lawngreen" # Color the battle bounce green!

                # String for the log:
                temp = "%s used %s to restore HP of %s!" % (source.nickname, self.name, t.name)
                self.log_to_battle(effects, restore, source, t, message=temp)

        def apply_effects(self, targets):
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            for t in targets:
                t.mod_stat("health", t.beeffects[0])

            self.settle_cost()


    class BasicPoisonSpell(BE_Action):
        def __init__(self, *args, **kwargs):
            super(BasicPoisonSpell, self).__init__(*args, **kwargs)
            self.event_class = PoisonEvent


    class ReviveSpell(BE_Action):
        def __init__(self, name, **kwargs):
            super(ReviveSpell, self).__init__(name, **kwargs)

        def check_conditions(self, source=None):
            if source:
                char = source
            else:
                char = self.source
            if not(isinstance(self.mp_cost, int)):
                mp_cost = int(char.get_max("mp")*self.mp_cost)
            else:
                mp_cost = self.mp_cost
            if not(isinstance(self.health_cost, int)):
                health_cost = int(char.get_max("health")*self.health_cost)
            else:
                health_cost = self.health_cost
            if not(isinstance(self.vitality_cost, int)):
                vitality_cost = int(char.get_max("vitality")*self.vitality_cost)
            else:
                vitality_cost = self.vitality_cost
            if (char.mp - mp_cost >= 0) and (char.health - health_cost >= 0) and (char.vitality - vitality_cost >= 0):
                if self.get_targets(char):
                    return True

        def effects_resolver(self, targets):
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            char = self.source
            attributes = self.attributes

            for t in targets:
                minh, maxh = int(t.get_max("health")*.1), int(t.get_max("health")*.3)
                revive = randint(minh, maxh)

                effects = list()
                effects.append(revive)
                t.beeffects = effects

                # String for the log:
                s = ("{color=[green]}%s brings %s back!{/color}" % (char.nickname, t.name))
                t.dmg_font = "lawngreen" # Color the battle bounce green!

                battle.log(s)

        def apply_effects(self, targets):
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]

            for t in targets:
                battle.corpses.remove(t)
                t.health = t.beeffects[0]

            self.settle_cost()

            return []

        def show_main_gfx(self, battle, attacker, targets):
            for target in targets:
                renpy.show(target.betag, what=target.besprite, at_list=[Transform(pos=target.cpos), fade_from_to(start_val=0, end_val=1.0, t=1.0, wait=0.5)], zorder=target.besk["zorder"])
            super(ReviveSpell, self).show_main_gfx(battle, attacker, targets)


    class DefenceBuffSpell(BE_Action):
        def __init__(self, *args, **kwargs):
            super(DefenceBuffSpell, self).__init__(*args, **kwargs)
            self.event_class = DefenceBuff

            self.defence_bonus = kwargs.get("defence_bonus", {}) # This is the direct def bonus.
            self.defence_multiplier = kwargs.get("defence_multiplier", {}) # This is the def multiplier.
            self.buff_icon = kwargs.get("buff_icon", None)
            self.buff_group = kwargs.get("buff_group", self.__class__)
            self.defence_gfx = kwargs.get("defence_gfx", "default")

        def effects_resolver(self, targets):
            if not isinstance(targets, (list, tuple, set)):
                targets = [targets]
            source = self.source
            attributes = self.attributes

            base_effect = 100

            for t in targets:
                effects = []

                # We get the multi and any effects that those may bring:
                effect = self.damage_modifier(t, base_effect, "status")
                if effect == "resisted":
                    effect = 0

                effect = int(round(effect))

                if effect:
                    # Check if event is in play already:
                    for event in store.battle.mid_turn_events:
                        if t == event.target and event.group == self.buff_group:
                            battle.log("%s is already buffed by %ss spell!" % (t.nickname, event.source.name))
                            break
                    else:
                        temp = self.event_class(source, t, self.defence_bonus, self.defence_multiplier,
                                                icon=self.buff_icon, group=self.buff_group,
                                                gfx_effect=self.defence_gfx)
                        battle.mid_turn_events.append(temp)
                        temp = "%s buffs %ss defence!" % (source.nickname, t.name)
                        self.log_to_battle(effects, effect, source, t, message=temp)
                else:
                    temp = "%s resisted the defence buff!" % (t.name)
                    self.log_to_battle(effects, effect, source, t, message=temp)

        def apply_effects(self, targets):
            self.settle_cost()
