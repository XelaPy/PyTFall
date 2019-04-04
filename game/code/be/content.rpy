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
                raise Exception("A timer's delay must be > .")

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
        def __init__(self, gfx, sfx, chain_sfx=True, times=2, delay=.35,
                     sd_duration=.5, alpha_fade=.0, webm_size=(), **properties):
            """
            chain_sfx: Do we play the sound and do we chain it?
                True = Play and Chain.
                False = Play once and don't play again.
                None = Do not play SFX at all.
            times = how many times we run the animation in a sequence.
            delay = time between showing displayables.
            sd_duration = single frame (displayable) duration.
            alpha_fade = Do we want alpha fade for each frame or not. 1.0 means not,
                .0 means yes and everything in between is partial fade.
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
                gfx = multi_strike(gfx, (offx, offy), st,
                                   self.single_displayable_duration, self.alpha_fade)

                # Calc when we add the next gfx and remove the old one from the list.
                # Right now it's a steady stream of ds but I'll prolly change it in the future.
                next_disp = uniform(self.delay*.85, self.delay)
                self.next = st + next_disp
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


    class BESkip(BE_Event):
        """
        Simplest possible class that just skips the turn for the player and logs that fact.
        This can/should be a function but heck :D

        This will now also restore 3 - 6% of Vitality!
        """
        def __init__(self, source=None):
            self.source = source

        def __call__(self, *args, **kwargs):
            source = self.source
            if source.be.controller == None:
                modifier = 1
            else:
                modifier = 2

            if source.status == "free":
                temp = []
                temp.append("{} skips a turn:".format(source.nickname))

                # Restoring stats:
                vp = round_int(source.get_max("vitality") * uniform(.03, .06))
                source.vitality += vp*modifier
                temp.append("{color=[green]}+%d VP{/color}" % vp)

                mp = round_int(source.get_max("mp") * uniform(.03, .06))
                source.mp += mp*modifier
                temp.append("{color=[gold]}+%d MP{/color}" % mp)

                temp = " ".join(temp)
                battle.log(temp)
            else: # Slaves case...
                msg = "{} stands still.".format(source.nickname)
                battle.log(msg)

            return "break"


    class BEEscape(BESkip):
        """Try to escape from the battle field"""
        def __init__(self, source=None):
            self.source = source

        def __call__(self, *args, **kwargs):
            if renpy.call_screen("yesno_prompt", message="Are you sure that you want to escape?", yes_action=Return(True), no_action=Return(False)):
                if not battle.logical:
                    renpy.show("escape_gates", what="portal_webm",  at_list=[Transform(align=(.5, .5))], zorder=100)
                    renpy.sound.play("content/sfx/sound/be/escape_portal.ogg")
                    tkwargs = {"color": gray,
                               "outlines": [(1, black, 0, 0)]}
                    gfx_overlay.notify("Escaped...", tkwargs=tkwargs)
                    renpy.pause(1.0)
                battle.combat_status = "escape"
                return "break"


    class BESurrender(BEEscape):
        """Try to escape from the battle field"""
        def __init__(self, source=None):
            self.source = source

        def __call__(self, *args, **kwargs):
            if renpy.call_screen("yesno_prompt", message="Are you sure that you want to surrender?", yes_action=Return(True), no_action=Return(False)):
                battle.combat_status = "surrender"
                if not battle.logical:
                    tkwargs = {"color": gray,
                               "outlines": [(1, black, 0, 0)]}
                    gfx_overlay.notify("Surrendered...", tkwargs=tkwargs)
                    renpy.pause(1.0)
                return "break"


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

            if not store.battle.logical:
                if self.death_effect == "dissolve":
                    renpy.hide(self.target.be.tag)
                    if self.death_effect == "dissolve":
                        renpy.with_statement(dissolve)

            # Forgot to remove poor sods from the queue:
            for target in battle.queue[:]:
                if self.target == target:
                    store.battle.queue.remove(self.target)

            battle.log(self.msg, delayed=True)


    class PoisonEvent(BE_Event):
        def __init__(self, source, target, effect, duration=5):
            self.target = target
            self.source = source
            self.counter = duration
            self.effect = effect
            self.type = "poison"
            self.group = "poison" # Or we collide with Buffs
            self.icon = "content/gfx/be/poison1.webp"

        def check_conditions(self):
            if battle.controller == self.target:
                return True

        def kill(self):
            if not self.counter:
                self.target.be.status_overlay.remove(self.icon)
                return True

        def apply_effects(self):
            target = self.target
            attacker = self.source

            # Damage Calculations:
            damage = target.get_max("health") * self.effect
            damage = max(randint(5, 10), int(damage) + randint(-2, 2))

            # Take care of modifiers:
            damage = round_int(self.apply_damage_modifier(attacker, target, damage, self.type))

            # GFX:
            if not battle.logical:
                gfx = Transform("poison_2", zoom=1.5)
                renpy.show("poison", what=gfx, at_list=[Transform(pos=battle.get_cp(target, type="center"), anchor=(.5, .5))], zorder=target.be.show_kwargs["zorder"]+1)
                renpy.play("content/sfx/sound/be/poisoned.mp3", channel="audio")
                txt = Text("%d"%damage, style="content_label", color=red, size=15)
                renpy.show("bb", what=txt, at_list=[battle_bounce(store.battle.get_cp(target, type="tc", yo=-10))], zorder=target.be.show_kwargs["zorder"]+2)
                renpy.pause(1.5)
                renpy.hide("poison")
                renpy.pause(.2)
                renpy.hide("bb")

            if target.health - damage > 0:
                target.mod_stat("health", -damage)
                msg = "%s is poisoned! {color=[green]}☠: %d{/color}" % (target.name, damage)
                battle.log(msg)
            else:
                target.health = 1
                death = RPG_Death(target,
                                  msg="{color=[red]}Poison took out %s!\n{/color}" % target.name,
                                  death_effect="dissolve")
                death.apply_effects()

            if not battle.logical:
                target.stats.update_delayed()

            self.counter -= 1

            if self.counter <= 0:
                msg = "{color=[teal]}Poison effect on %s has ran it's course...{/color}" % (target.name)
                battle.log(msg)


    class DefenceBuff(BE_Event):
        def __init__(self, source, target, bonus={}, multi=0, icon=None, group=None, gfx_effect="default"):
            # bonus and multi both expect dicts if mods are desirable.
            self.target = target
            self.source = source
            self.type = type
            self.buff = True # We may need this for debuffing later on?

            self.counter = randint(5, 8) # Active for 5-8 turns

            self.icon = icon or "content/gfx/be/fists.webp"
            self.gfx_effect = gfx_effect
            self.activated_this_turn = False # Flag used to pass to gfx methods that this buff was triggered.
            self.group = group # No two buffs from the same group can be applied twice.
            # We also add the icon to targets status overlay:
            target.be.status_overlay.append(self.icon)

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
                self.target.be.status_overlay.remove(self.icon)
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
        def __init__(self):
            super(MultiAttack, self).__init__()

        def show_main_gfx(self, battle, attacker, targets):
            # Shows the MAIN part of the attack and handles appropriate sfx.
            gfx = self.main_effect["gfx"]
            sfx = self.main_effect["sfx"]

            times = self.main_effect.get("times", 2)
            interval = self.main_effect.get("interval", .2)
            sd_duration = self.main_effect.get("sd_duration", .3)
            alpha_fade = self.main_effect.get("alpha_fade", .3)
            webm_size  = self.main_effect.get("webm_size", ())

            # GFX:
            if gfx:
                what = self.get_main_gfx()

                # Flip the attack image if required:
                if self.main_effect.get("hflip", None) and battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0]:
                    what = Transform(what, xzoom=-1)

                # Posional properties:
                aim = self.main_effect["aim"]
                point = aim.get("point", "center")
                anchor = aim.get("anchor", (.5, .5))
                xo = aim.get("xo", 0)
                yo = aim.get("yo", 0)

                # Create a UDD:
                what = ChainedAttack(what, sfx, chain_sfx=True, times=times, delay=interval, sd_duration=sd_duration, alpha_fade=alpha_fade, webm_size=webm_size)

                for index, target in enumerate(targets):
                    gfxtag = "attack" + str(index)
                    renpy.show(gfxtag, what=what, at_list=[Transform(pos=battle.get_cp(target, type=point, xo=xo, yo=yo), anchor=anchor)], zorder=target.be.show_kwargs["zorder"]+1)


    class ArealSkill(BE_Action):
        """
        Simplest attack, usually simple magic.
        """
        def __init__(self):
            super(ArealSkill, self).__init__()

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
                what = self.get_main_gfx()
                # Flip the attack image if required:
                if self.main_effect.get("hflip", False) and battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0]:
                    what = Transform(what, xzoom=-1)

                target = targets[0]
                teampos = target.be.teampos
                aim = self.main_effect["aim"]
                point = aim.get("point", "center")
                anchor = aim.get("anchor", (.5, .5))
                xo = aim.get("xo", 0)
                yo = aim.get("yo", 0)

                gfxtag = "areal"
                if teampos == "l":
                    teampos = BDP["perfect_middle_right"]
                else:
                    teampos = BDP["perfect_middle_left"]
                renpy.show(gfxtag, what=what, at_list=[Transform(pos=battle.get_cp(target, type=point, xo=xo, yo=yo, override=teampos), anchor=anchor)], zorder=1000)

        def hide_main_gfx(self, targets):
            renpy.hide("areal")


    class P2P_Skill(BE_Action):
        """ ==> @Review: There may not be a good reason for this to be a magical attack instead of any attack at all!
        Point to Point magical strikes without any added effects. This is one step simpler than the ArrowsSkill attack.
        Used to attacks like FireBall.
        """
        def __init__(self):
            super(P2P_Skill, self).__init__()

            self.projectile_effects = {}

        def show_main_gfx(self, battle, attacker, targets):
            # We simply want to add projectile effect here:
            pro_gfx = self.projectile_effects.get("gfx", Null())
            pro_sfx = self.projectile_effects.get("sfx", None)
            pro_sfx = choice(pro_sfx) if isinstance(pro_sfx, (list, tuple)) else pro_sfx
            pause = self.projectile_effects["duration"]

            missle = Transform(pro_gfx, xzoom=-1, xanchor=1.0) if battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0] else pro_gfx

            initpos = battle.get_cp(attacker, type="fc", xo=60)

            if pro_sfx:
                renpy.sound.play(pro_sfx)

            for index, target in enumerate(targets):
                aimpos = battle.get_cp(target, type="center")
                renpy.show("launch" + str(index), what=missle,
                        at_list=[move_from_to_pos_with_easeout(start_pos=initpos, end_pos=aimpos, t=pause),
                        Transform(anchor=(.5, .5))], zorder=target.be.show_kwargs["zorder"]+50)

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
                what = self.get_main_gfx()

                aim = self.main_effect["aim"]
                point = aim.get("point", "center")
                anchor = aim.get("anchor", (.5, .5))
                xo = aim.get("xo", 0)
                yo = aim.get("yo", 0)

                c0 = self.main_effect.get("hflip", False)
                c1 = battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0]
                if c0 and c1:
                    what = Transform(what, xzoom=-1)

                for index, target in enumerate(targets):
                    gfxtag = "attack" + str(index)
                    renpy.show(gfxtag, what=what,
                        at_list=[Transform(pos=battle.get_cp(target, type=point, xo=xo, yo=yo), anchor=anchor)],
                        zorder=target.be.show_kwargs["zorder"]+51)

        def hide_main_gfx(self, targets):
            for i in xrange(len(targets)):
                gfxtag = "attack" + str(i)
                renpy.hide(gfxtag)


    class P2P_ArealSkill(P2P_Skill):
        """
        Used to attacks like FireBall.
        """
        def __init__(self):
            super(P2P_ArealSkill, self).__init__()

        def show_main_gfx(self, battle, attacker, targets):
            # We simply want to add projectile effect here:
            pro_gfx = self.projectile_effects.get("gfx", Null())
            pro_sfx = self.projectile_effects.get("sfx", None)
            pro_sfx = choice(pro_sfx) if isinstance(pro_sfx, (list, tuple)) else pro_sfx
            pause = self.projectile_effects["duration"]

            target = targets[0]

            missle = Transform(pro_gfx, zoom=-1, xanchor=1.0) if battle.get_cp(attacker)[0] > battle.get_cp(target)[0] else pro_gfx

            initpos = battle.get_cp(attacker, type="fc", xo=60)

            if pro_sfx:
                renpy.sound.play(pro_sfx)

            aimpos = BDP["perfect_middle_right"] if target.be.teampos == "l" else BDP["perfect_middle_left"]

            renpy.show("launch", what=missle, at_list=[move_from_to_pos_with_easeout(start_pos=initpos,
                                                       end_pos=aimpos,
                                                       t=pause),
                       Transform(anchor=(.5, .5))],
                       zorder=target.be.show_kwargs["zorder"]+1000)
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
                what = self.get_main_gfx()

                aim = self.main_effect["aim"]
                point = aim.get("point", "center")
                anchor = aim.get("anchor", (.5, .5))
                xo = aim.get("xo", 0)
                yo = aim.get("yo", 0)

                renpy.show("projectile", what=what, at_list=[Transform(pos=aimpos, anchor=anchor)], zorder=target.be.show_kwargs["zorder"]+1001)

        def hide_main_gfx(self, targets):
            renpy.hide("projectile")


    class ArrowsSkill(P2P_Skill):
        """This is the class I am going to comment out really well because this spell was not originally created by me
        and yet I had to rewrite it completely for new BE.
        """
        def __init__(self):
            super(ArrowsSkill, self).__init__()

            self.firing_effects = None

        def show_main_gfx(self, battle, attacker, targets):
            firing_gfx = self.firing_effects["gfx"]
            firing_sfx = self.firing_effects["sfx"]
            firing_sfx = choice(firing_sfx) if isinstance(firing_sfx, (list, tuple)) else firing_sfx
            pause = self.firing_effects.get("duration", .1)

            bow = Transform(firing_gfx, zoom=-1, xanchor=1.0) if battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0] else firing_gfx

            if firing_sfx:
                renpy.sound.play(firing_sfx)

            castpos = battle.get_cp(attacker, type="fc", xo=30)

            renpy.show("casting", what=bow, at_list=[Transform(pos=castpos, yanchor=.5)], zorder=attacker.be.show_kwargs["zorder"]+50)
            if pause > .6:
                renpy.pause(pause)
            else:
                renpy.pause(.6)

            # We simply want to add projectile effect here:
            pro_gfx = self.projectile_effects.get("gfx", Null())
            pro_sfx = self.projectile_effects.get("sfx", None)
            pro_sfx = choice(pro_sfx) if isinstance(pro_sfx, (list, tuple)) else pro_sfx
            pause = self.projectile_effects["duration"]

            missle = Transform(pro_gfx, zoom=-1, xanchor=1.0) if battle.get_cp(attacker)[0] > battle.get_cp(targets[0])[0] else pro_gfx

            if pro_sfx:
                renpy.sound.play(pro_sfx)

            castpos = battle.get_cp(attacker, type="fc", xo=75)

            for index, target in enumerate(targets):
                aimpos = battle.get_cp(target, type="center", yo=-20)
                renpy.show("launch" + str(index), what=missle, at_list=[
                           move_from_to_pos_with_easeout(start_pos=castpos, end_pos=aimpos, t=pause),
                           Transform(anchor=(.5, .5))],
                           zorder=target.be.show_kwargs["zorder"]+51)

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
                what = self.get_main_gfx()

                # pause = self.main_effect["duration"]
                aim = self.main_effect["aim"]
                point = aim.get("point", "center")
                anchor = aim.get("anchor", (.5, .5))
                xo = aim.get("xo", 0)
                yo = aim.get("yo", 0)

                for index, target in enumerate(targets):
                    gfxtag = "attack" + str(index)
                    renpy.show(gfxtag, what=what, at_list=[Transform(pos=battle.get_cp(target, type=point, xo=xo, yo=yo), anchor=anchor)], zorder=target.be.show_kwargs["zorder"]+52)

        def hide_main_gfx(self, targets):
            renpy.hide("casting")
            renpy.with_statement(Dissolve(.5))
            for i in xrange(len(targets)):
                gfxtag = "attack" + str(i)
                renpy.hide(gfxtag)


    class ATL_ArealSkill(ArealSkill):
        """This one used ATL function for the attack, ignoring all usual targeting options.

        As a rule, it expects to recieve left and right targeting option we normally get from team positions for Areal Attacks.
        """
        def __init__(self):
            super(ATL_ArealSkill, self).__init__()

        def show_main_gfx(self, battle, attacker, targets):
            # Shows the MAIN part of the attack and handles appropriate sfx.
            sfx = self.main_effect["sfx"]
            gfx = getattr(store, self.main_effect["atl"])
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
        def __init__(self):
            super(FullScreenCenteredArealSkill, self).__init__()

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
                renpy.show(gfxtag, what=gfx, at_list=[Transform(align=(.5, .5))], zorder=1000)


    class BasicHealingSpell(BE_Action):
        def __init__(self):
            super(BasicHealingSpell, self).__init__()

        def assess_logical_effects(self, source, targets):
            type = "healing"

            for target in targets:
                restore = target.get_max("health") * self.effect

                self.assess_resistance(target, type)
                self.assess_elemental(source, target, type)
                self.assess_damage_multipliers(source, target, type)

                # Base:
                target.be.damage[type]["base"] = restore

                # Direct and Elemental multipliers:
                a = target.be.damage[type]["items_damage_multiplier"]
                b = target.be.damage[type]["traits_damage_multiplier"]
                c = target.be.damage[type]["elemental_damage_multiplier"]
                multi = sum([1.0, a, b, c])
                restore *= multi

                # rng factors:
                restore *= uniform(.95, 1.05)

                # Resistance:
                if target.be.damage[type]["resisted"]:
                    restore = 0

                restore = round_int(restore)
                target.be.damage[type]["result"] = restore
                target.be.total_damage += restore

                target.be.damage_font = "lawngreen" # Color the battle bounce green!

                # String for the log:
                temp = "%s used %s to heal %s!" % (source.nickname, self.name, target.name)
                self.log_to_battle(source, target, message=temp)

        def apply_effects(self, targets):
            for t in targets:
                t.mod_stat("health", t.be.total_damage)

            self.settle_cost()


    class BasicPoisonSpell(BE_Action):
        def __init__(self):
            super(BasicPoisonSpell, self).__init__()
            self.event_class = PoisonEvent
            self.buff_group = self.__class__
            self.event_duration = 3


    class ReviveSpell(BE_Action):
        def __init__(self):
            super(ReviveSpell, self).__init__()

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

        def assess_logical_effects(self, source, targets):
            for target in targets:
                minh, maxh = int(target.get_max("health")*.1), int(target.get_max("health")*.3)
                revive = randint(minh, maxh)

                t.be.total_damage = revive

                target.be.damage_font = "lawngreen" # Color the battle bounce green!

                # String for the log:
                s = ("{color=[green]}%s revives %s!{/color}" % (source.nickname, target.name))
                battle.log(s)

        def apply_effects(self, targets):
            for t in targets:
                battle.corpses.remove(t)
                t.health = t.be.damage_effects[0]

            self.settle_cost()

            return []

        def show_main_gfx(self, battle, attacker, targets):
            for target in targets:
                renpy.show(target.be.tag, what=target.be.sprite, at_list=[Transform(pos=target.be.current_pos), fade_from_to(start_val=0, end_val=1.0, t=1.0, wait=.5)], zorder=target.be.show_kwargs["zorder"])
            super(ReviveSpell, self).show_main_gfx(battle, attacker, targets)


    class DefenceBuffSpell(BE_Action):
        def __init__(self):
            super(DefenceBuffSpell, self).__init__()
            self.event_class = DefenceBuff

            self.defence_bonus = {} # This is the direct def bonus.
            self.defence_multiplier = {} # This is the def multiplier.
            self.buff_icon = None
            self.buff_group = self.__class__
            self.defence_gfx = "default"

        def assess_logical_effects(self, source, targets):
            for target in targets:
                self.assess_resistance(target, type)

                if target.be.damage[type]["resisted"]:
                    temp = "%s resisted the defence buff!" % (target.name)
                    self.log_to_battle(source, target, message=temp)
                else:
                    # Check if event is in play already:
                    for event in store.battle.mid_turn_events:
                        if target == event.target and event.group == self.buff_group:
                            battle.log("%s is already buffed by %ss spell!" % (target.nickname, event.source.name))
                            break
                    else:
                        temp = self.event_class(source, target, self.defence_bonus,
                                                self.defence_multiplier,
                                                icon=self.buff_icon, group=self.buff_group,
                                                gfx_effect=self.defence_gfx)
                        battle.mid_turn_events.append(temp)
                        temp = "%s buffs %ss defence!" % (source.nickname, target.name)
                        self.log_to_battle(source, target, message=temp)

        def apply_effects(self, targets):
            self.settle_cost()


    class ConsumeItem(BE_Action):
        def __init__(self):
            super(ConsumeItem, self).__init__()
            self.item = None # item to use...

            self.type = "sa"
            self.attributes = ["item"]
            self.kind = "item"
            self.desc = "Use an item!"

            self.target_damage_effect["gfx"] = None
            self.target_sprite_damage_effect["gfx"] = "being_healed"
            self.main_effect["gfx"] = None
            self.main_effect["sfx"] = "content/sfx/sound/be/heal2.mp3"

            super(ConsumeItem, self).init()

        def assess_logical_effects(self, attacker, targets):
            source = attacker
            item = self.item

            for target in targets:
                battle.log("%s uses a %s!" % (source.nickname, item.id))

        def apply_effects(self, targets):
            item = self.item

            self.source.remove_item(item)
            for t in targets:
                t.equip(item)
