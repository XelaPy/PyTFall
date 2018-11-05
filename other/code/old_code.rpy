# Old Code that may not be immediately useful any longer but can still be used for referencing or in future development.
auto_equip, old:
# Old code:
    screen building_finances():
        modal True
        zorder 1

        default show_fin = "day"

        frame at slide(so1=(0, 700), t1=.7, so2=(0, 0), t2=.3, eo2=(0, -config.screen_height)):
            background Frame("content/gfx/frame/arena_d.png", 5, 5)
            align (.5, .5)

            # side "c r":
            viewport id "message_vp":
                style_group "content"
                xysize (1100, 600)
                draggable False
                mousewheel True

                if day > 1 and str(day-1) in building.fin.game_fin_log:
                    $ fin_inc = building.fin.game_fin_log[str(day-1)][0]
                    $ fin_exp = building.fin.game_fin_log[str(day-1)][1]

                    if show_fin == 'day':
                        label (u"Fin Report (Yesterday)") xalign .4 ypos 30 text_size 30
                        # Income:
                        vbox:
                            pos (50, 100)
                            label "Income:" text_size 20
                            null height 10
                            hbox:
                                vbox:
                                    xmaximum 170
                                    xfill True

                                    for key in fin_inc["work"]:
                                        text ("[key]")

                                    for key in fin_inc["private"]:
                                        if key != "work":
                                            text("[key]")

                                vbox:
                                    for key in fin_inc["work"]:
                                        $ val = fin_inc["work"][key]
                                        text("[val]")

                                    for key in fin_inc["private"]:
                                        $ val = fin_inc["private"][key]
                                        text("[val]")

                        # Expense:
                        vbox:
                            pos (450, 100)
                            label "Expense:" text_size 20
                            null height 10
                            hbox:
                                vbox:
                                    xmaximum 170
                                    xfill True

                                    for key in fin_exp["work"]:
                                        text("[key]")

                                    for key in fin_exp["private"]:
                                        text("[key]")

                                vbox:
                                    for key in fin_exp["work"]:
                                        $ val = fin_exp["work"][key]
                                        text("[val]")

                                    for key in fin_exp["private"]:
                                        $ val = fin_exp["private"][key]
                                        text("[val]")

                        python:
                            total_income = sum(fin_inc["work"].values())
                            total_expenses = sum(fin_exp["work"].values())
                            for key in fin_inc["private"]: total_income += fin_inc["private"][key]
                            for key in fin_exp["private"]: total_expenses += fin_exp["private"][key]
                            total = total_income - total_expenses
                        vbox:
                            align (.80, .60)
                            text "----------------------------------------"
                            text ("Revenue: [total]"):
                                size 25
                                xpos 15
                                if total > 0:
                                    color lawngreen
                                else:
                                    color red

                        hbox:
                            style_group "basic"
                            align (.5, .9)
                            textbutton "{size=-3}Show Total" action SetScreenVariable("show_fin", "total") minimum(200, 30)

                    elif show_fin == 'total':
                        label (u"Fin Report (Game)") xalign .4 ypos 30 text_size 30
                        python:
                            income = dict()
                            for _day in building.fin.game_fin_log:
                                for key in building.fin.game_fin_log[_day][0]["private"]:
                                    income[key] = income.get(key, 0) + building.fin.game_fin_log[_day][0]["private"][key]

                                for key in building.fin.game_fin_log[_day][0]["work"]:
                                    income[key] = income.get(key, 0) + building.fin.game_fin_log[_day][0]["work"][key]

                        # Income:
                        vbox:
                            pos (50, 100)
                            label "Income:" text_size 20
                            null height 10
                            hbox:
                                vbox:
                                    xmaximum 170
                                    xfill True
                                    for key in income:
                                        text("[key]")
                                vbox:
                                    for key in income:
                                        $ val = income[key]
                                        text("[val]")

                        python:
                            expenses = dict()
                            for _day in building.fin.game_fin_log:
                                for key in building.fin.game_fin_log[_day][1]["private"]:
                                    expenses[key] = expenses.get(key, 0) + building.fin.game_fin_log[_day][1]["private"][key]

                                for key in building.fin.game_fin_log[_day][1]["work"]:
                                    expenses[key] = expenses.get(key, 0) + building.fin.game_fin_log[_day][1]["work"][key]
                        vbox:
                            pos (450, 100)
                            label "Expense:" text_size 20
                            null height 10
                            hbox:
                                vbox:
                                    xmaximum 170
                                    xfill True
                                    for key in expenses:
                                        text("[key]")
                                vbox:
                                    for key in expenses:
                                        $ val = expenses[key]
                                        text("[val]")

                        python:
                            game_total = 0
                            total_income = sum(income.values())
                            total_expenses = sum(expenses.values())
                            game_total = total_income - total_expenses
                        vbox:
                            align (.80, .60)
                            text "----------------------------------------"
                            text ("Revenue: [game_total]"):
                                size 25
                                xpos 15
                                if game_total > 0:
                                    color lawngreen
                                else:
                                    color red

                        hbox:
                            style_group "basic"
                            align (.5, .9)
                            textbutton "{size=-3}Show Daily" action SetScreenVariable("show_fin", "day") minimum(200, 30)

                else:
                    text (u"No financial records available!") align(.5, .5)

                button:
                    style_group "basic"
                    action Hide('building_finances')
                    minimum (250, 30)
                    align (.5, .96)
                    text "OK"

def keep_chance(self, item):
    """
    return a list of chances, up to 100 indicating how much the person wants to hold on to a particular
    item. Only includes personal preferences, use inv.eval_inventory() to determine stats/skills.
    """
    if not item.eqchance or not can_equip(item, self):
        return [-1000000]

    chance = []
    when_drunk = 30
    appetite = 50

    for trait in self.traits:
        if trait in trait_selections["badtraits"] and item in trait_selections["badtraits"][trait]:
            return [-1000000]

        if trait in trait_selections["goodtraits"] and item in trait_selections["goodtraits"][trait]:
            chance.append(100)

        if trait == "Kamidere": # Vanity: wants pricy uncommon items
            chance.append((100 - item.chance + min(item.price/10, 100))/2)
        elif trait == "Tsundere": # stubborn: what s|he won't buy, s|he won't wear.
            chance.append(100 - item.badness)
        elif trait == "Bokukko": # what the farmer don't know, s|he won't eat.
            chance.append(item.chance)
        elif trait == "Heavy Drinker":
            when_drunk = 45
        elif trait == "Always Hungry":
            appetite += 20
        elif trait == "Slim":
            appetite -= 10

    if item.type == "permanent": # only allowed if also in goodtraits. but then we already returned 100
        return [-1000000]

    if item.slot == "consumable":

        if item in self.consblock or item in self.constemp:
            return [-10]
        if item.type == "alcohol":
            if self.effects['Drunk']['activation_count'] >= when_drunk:
                return [-1]
            if self.effects['Depression']['active']:
                chance.append(30 + when_drunk)

        elif item.type == "food":
            food_poisoning = self.effects['Food Poisoning']['activation_count']
            if not food_poisoning:
                chance.append(appetite)
            else:
                if food_poisoning >= 6:
                    return [-1]
                chance.append((6-food_poisoning) * 9)

    elif item.slot == "misc":
        # If the item self-destructs or will be blocked after one use,
        # it's now up to the caller to stop after the first item of this kind that is picked.
        # no blocked misc items:
        if item.id in self.miscblock:
            return [-1000000]

    chance.append(item.eqchance)
    return chance

# Problem with it is that we'd throw away an item that
# would give 1000 to HP, 1000 to attack and -.01 to exploration :(
# (for example)
#     for stat, value in item.mod.iteritems():
#         if stat in exclude_on_stats and value < min_value:
#             break # break (in any case below) will cause 0 weights to be added for this item
#
#         if stat in stats['current_stat']:
#             # a new max may have to be considered
#             new_max = min(self.max[stat] + item.max[stat], self.lvl_max[stat]) if stat in item.max else stats['current_max'][stat]
#             if not new_max:
#                 break # Some weird exception?
#
#             # what the new value would be:
#             new_stat = max(min(self.stats[stat] + self.imod[stat] + value, new_max), self.min[stat])
#
#             # add the fraction increase/decrease
#             weights.append(50 + 100*(new_stat - stats['current_stat'][stat])/new_max)
#     else:
#         for stat, value in item.max.iteritems():
#             if not stat in target_stats:
#                 continue # Use to be in exclude_on_stats but it didn't feel right.
#
#             if stat in stats['current_max']:
#                 # Next Max and Stats for the Char after item is applied:
#                 # OLD CODE:
#                 # # if the stat does change, give weight for this
#                 # new_max = min(self.max[stat] + value, self.lvl_max[stat])
#                 # new_stat = self.stats[stat] + self.imod[stat] + (item.mod[stat] if stat in item.mod else 0)
#
#                 # stat_change = new_stat - stats['current_stat'][stat]
#                 # if stat_change:
#                 #     if stat_change < min_value:
#                 #         break
#                 #     weights.append(50 + 100*stat_change/stats['current_max'][stat])
#                 # else:
#                 #     stat_remaining = new_max - stats['current_stat'][stat]
#                 #     # if training doesn't shift max, at least give a weight up to 1 for the increased max.
#                 #     # if max decreases, give a penalty, more severe if there is little stat remaining.
#                 #     weights.append(max(50 + value / max(stat_remaining + value, 1), 0))
#
#                 # I disagree with the concept, if max that we care about is improved
#                 # Other items can be used to boost, so feels like a shitty way of handling the matter.
#                 # We care about MAX stat here, not some phantom change as the result of application of
#                 # only this one item. So a rewrite:
#                 new_max = min(self.max[stat] + value, self.lvl_max[stat])
#                 curr_max = stats['current_max'][stat]
#                 if new_max == curr_max:
#                     continue
#                 elif new_max > curr_max:
#                     weights.append(50 + max(new_max-curr_max, 50))
#                 else: # Item lowers max of this stat for the character:
#                     if stat in exclude_on_stats:
#                         break # We want nothing to do with this item.
#                     else:
#                         change = curr_max-new_max
#                         if change > curr_max*.2: # If items takes off more that 20% of our stat...
#                             break
#         else:
#             for skill, effect in item.mod_skills.iteritems():
#                 # Break if any skill we truly care about is lowered by this:
#                 # This feels wrong, some skills may have tiny drawbacks but otherwise be hosted by great items :(
#                 # It feels like we need to add all to the weights, good and bad and figure out what's best later.
#                 if skill in exclude_on_skills and all(i <= 0 for i in effect):
#                     break
#
#                 if skill in target_skills:
#                     skill_remaining = SKILLS_MAX[skill] - stats['skill'][skill]
#                     if skill_remaining > 0:
#                         # calculate skill with mods applied, as in apply_item_effects() and get_skill()
#                         mod_action = self.skills[skill][0] + effect[3]
#                         mod_training = self.skills[skill][1] + effect[4]
#                         mod_skill_multiplier = self.skills_multipliers[skill][2] + effect[2]
#
#                         if upto_skill_limit: # more precise calculation of skill limits
#                             training_range = mod_training * 3
#                             beyond_training = mod_action - training_range
#                             if beyond_training >= 0:
#                                 mod_training += training_range - mod_action + beyond_training/3.0
#
#                         mod_training += mod_action
#                         new_skill = mod_training*max(min(mod_skill_multiplier, 1.5), .5)
#                         if new_skill < min_value:
#                             break
#
#                         saturated_skill = max(stats['skill'][skill] + 100, new_skill)
#
#                         weights.append(50 + 100*(new_skill - stats['skill'][skill]) / saturated_skill)
#             else:
#                 l = len(weights)
#                 if l > most_weights[item.slot]:
#                     most_weights[item.slot] = l
#
#                 weighted[item.slot].append([weights, item])
#
# return most_weights

class Rank(_object): # Will not be used for the next release...
    """
    Ranks, currently not in use in the game.
    """
    WhRANKS = OrderedDict()
    WhRANKS["0"]=dict(name=('No Rank: Kirimise', '(Almost beggar)'), price=0)
    WhRANKS["1"]=dict(name=("Rank 1: Heya-Mochi", "(Low-class prostitute)"), skills={"oral": 10, "vaginal": 10, "anal": 5}, total_skill=100, price=1000, exp=10000) # note: refinement is not a stat anymore!
    WhRANKS["2"]=dict(name=("Rank 2: Zashiki-Mochi", "(Middle-class Prostitute"), skills={"oral": 25, "vaginal": 15, "anal": 15}, total_skill=300, price=3000, exp=25000)
    WhRANKS["3"]=dict(name=("Rank 3: Tsuke-Mawashi", "(Courtesan)"), skills={"oral": 55, "vaginal": 40, "anal": 25}, total_skill=600, price=5000, exp=50000)
    WhRANKS["4"]=dict(name=("Rank 4: Chûsan", "(Famous)"), skills={"oral": 100, "vaginal": 80, "anal": 50}, total_skill=1000, stats={"refinement": 100}, price=7500, exp=100000)
    WhRANKS["5"]=dict(name=("Rank 5: Yobidashi", "(High-Class Courtesan)"), skills={"oral": 250, "vaginal": 150, "anal": 130}, total_skill=1250, stats={"refinement": 150}, price=10000, exp=250000)
    WhRANKS["6"]=dict(name=("Rank 6: Koshi", "(Nation famous)"), skills={"oral": 500, "vaginal": 500, "anal": 500}, total_skill=2500, stats={"refinement": 500}, price=25000, exp=400000)
    WhRANKS["7"]=dict(name=("Rank 7: Tayu", "(Legendary)"), skills={"oral": 1500, "vaginal": 1500, "anal": 1500}, total_skill=5000, stats={"refinement": 800}, price=50000, exp=800000)

    WaRANKS = OrderedDict()
    WaRANKS["0"]=dict(name=('No Rank', 'Nub with a stick...'), price=0)
    WaRANKS["1"]=dict(name=("Rank 1", "Thug"), skills={}, total_skill=100, stats={}, price=1000, exp=10000)
    WaRANKS["2"]=dict(name=("Rank 2", "Sword Sister"), skills={}, total_skill=300, stats={}, price=3000, exp=25000)
    WaRANKS["3"]=dict(name=("Rank 3", "War Maiden"), skills={}, total_skill=600, stats={}, price=5000, exp=50000)
    WaRANKS["4"]=dict(name=("Rank 4", "Famous"), skills={}, total_skill=1000, stats={}, price=7500, exp=100000)
    WaRANKS["5"]=dict(name=("Rank 5", "War Maiden"), skills={}, total_skill=1250, stats={}, price=10000, exp=250000)
    WaRANKS["6"]=dict(name=("Rank 6", "Valkyrie"), skills={}, total_skill=2500, stats={}, price=25000, exp=400000)
    WaRANKS["7"]=dict(name=("Rank 7", "Legendary"), skills={}, total_skill=5000, stats={}, price=50000, exp=800000)

    StRANKS = OrderedDict()
    StRANKS["0"]=dict(name=('No Rank', 'Nub wiggling her ass...'), price=0)
    StRANKS["1"]=dict(name=("Rank 1", "Stripper"), skills={"strip": 50}, total_skill=100, price=1000, exp=10000)
    StRANKS["2"]=dict(name=("Rank 2", "Lap Dancer"), skills={"strip": 100}, total_skill=300, price=3000, exp=25000)
    StRANKS["3"]=dict(name=("Rank 3", "Seductress"), skills={"strip": 250}, total_skill=600, price=5000, exp=50000)
    StRANKS["4"]=dict(name=("Rank 4", "Famous"), skills={"strip": 500}, total_skill=1000, stats={}, price=7500, exp=100000)
    StRANKS["5"]=dict(name=("Rank 5", "Ecdysiastn"), skills={"strip": 1000}, total_skill=1250, stats={}, price=10000, exp=250000)
    StRANKS["6"]=dict(name=("Rank 6", "Temptress"), skills={"strip": 2500}, total_skill=2500, stats={}, price=25000, exp=400000)
    StRANKS["7"]=dict(name=("Rank 7", "Legendary"), skills={"strip": 5000}, total_skill=5000, stats={}, price=50000, exp=800000)

    SgRANKS = OrderedDict()
    SgRANKS["0"]=dict(name=('No Rank', 'Nub breaking the china...'), price=0)
    SgRANKS["1"]=dict(name=("Rank 1", "Wench"), skills={"service": 50}, total_skill=100, price=1000, exp=10000)
    SgRANKS["2"]=dict(name=("Rank 2", "Servant"), skills={"service": 100}, total_skill=300, price=3000, exp=25000)
    SgRANKS["3"]=dict(name=("Rank 3", "Maid"), skills={"service": 250}, total_skill=600, price=5000, exp=50000)
    SgRANKS["4"]=dict(name=("Rank 4", "Chambermaid"), skills={"service": 500}, total_skill=1000, stats={}, price=7500, exp=100000)
    SgRANKS["5"]=dict(name=("Rank 5", "Housekeeper"), skills={"service": 1000}, total_skill=1250, stats={}, price=10000, exp=250000)
    SgRANKS["6"]=dict(name=("Rank 6", "Famous"), skills={"service": 2500}, total_skill=2500, stats={}, price=25000, exp=400000)
    SgRANKS["7"]=dict(name=("Rank 7", "Legendary"), skills={"service": 5000}, total_skill=5000, stats={}, price=50000, exp=800000)
    """
    Handles ranks for characters. Stores all related data and returns the correct rank/requirement/updates.
    """
    def __init__(self):
        self.current_rank = None
        self.n = None


class GuiGirlsList(_object):
    """
    Used for sorting girls in the list and maybe in profile screen in the future.
    """
    STATUS_GROUP = 'status'
    OCCUPATION_GROUP = 'occupation'
    ACTION_GROUP = 'action'
    BUILDING_GROUP = 'building'

    def __init__(self):
        self.sorted = list(girl for girl in hero.chars if girl.action != "Exploring")
        self.init_display_filters()
        self.init_active_filters()

        self.page = 0
        self.total_pages = 1

    def init_display_filters(self):
        self.display_filters = [
            ('Status', [
                ['Free', self.STATUS_GROUP, 'free'],
                ['Slaves', self.STATUS_GROUP, 'slave'],
                ["Run away", self.ACTION_GROUP, RunawayManager.ACTION] # Put here as "status" makes more sense then "job"
            ]),
            ('Current job', [ # TODO: This filter no longer makes any sense, action are now jobs:
                ['None', self.ACTION_GROUP, None],
                ['Whore', self.ACTION_GROUP, 'Whore'],
                ['Guard', self.ACTION_GROUP, 'Guard'],
                ['Server', self.ACTION_GROUP, 'Server'],
            ]),
            ('Courses', [
                [course_name, self.ACTION_GROUP, course_action] for course_name, course_action in get_all_courses()
            ]),
            ('Occupation', [
                ['Prostitutes', self.OCCUPATION_GROUP, traits['Prostitute']],
                ['Strippers', self.OCCUPATION_GROUP, traits['Stripper']],
                ['Warriors', self.OCCUPATION_GROUP, 'Warrior'],
                ['Service Girls', self.OCCUPATION_GROUP, 'Server'],
            ]),
            ('Buildings', [
                [building.name, self.BUILDING_GROUP, building] for building in list(b for b in hero.buildings if b.__class__ != Apartment)
            ]),
        ]

    def init_active_filters(self):
        self.active_filters = {
            self.STATUS_GROUP: set(),
            self.OCCUPATION_GROUP: set(),
            self.BUILDING_GROUP: set(),
            self.ACTION_GROUP: set(),
        }

    def clear(self):
        self.sorted = copy.copy(hero.chars)
        self.init_active_filters()
        renpy.restart_interaction()

    def add_filter(self, group, item):
        if item not in self.active_filters[group]:
            self.active_filters[group] = set([item])
        else:
            self.active_filters[group].remove(item)

    def sort_by_status(self, girl_list):
        for status in self.active_filters[self.STATUS_GROUP]:
            girl_list = list(girl for girl in girl_list if girl.status == status)
        return girl_list

    def sort_by_occupation(self, girl_list):
        for occupation in self.active_filters[self.OCCUPATION_GROUP]:
            girl_list = list(girl for girl in girl_list if occupation in girl.occupations)
        return girl_list

    def sort_by_action(self, girl_list):
        for action in self.active_filters[self.ACTION_GROUP]:
            girl_list = list(girl for girl in girl_list if girl.action == action)
        return girl_list

    def sort_by_brothel(self, girl_list):
        for building in self.active_filters[self.BUILDING_GROUP]:
            girl_list = list(girl for girl in girl_list if girl.location == building)
        return girl_list

    def get_sorted(self):
        return self.sort_by_brothel(
            self.sort_by_occupation(
                self.sort_by_action(
                    self.sort_by_status(self.sorted)
                )
            )
        )

    def get_focus(self, filter_group, filter_key):
        return filter_key in self.active_filters[filter_group]


screen dropdown(pos):
    # Trying to create a drop down screen with choices of actions:
    zorder 3
    modal True

    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()

    # Get mouse coords:
    python:
        x, y = pos
        xval = 1.0 if x > config.screen_width/2 else .0
        yval = 1.0 if y > config.screen_height/2 else .0

    frame:
        style_prefix "dropdown_gm"
        pos (x, y)
        anchor (xval, yval)
        has vbox

        transclude # Doesn't work as expected, no style passing to other screens, no modal, bull shit of a statement basically at this stage :(  TODO: is it still true in modern renpy?

init python:
Old Upgrades from Building.__init__
    # Upgrades
    # self.used_upgrade_slots = 0
    # self.upgrade_slots = 3

    # self.upgrades['bar'] =  {
        # '1': {'id': 1, 'active': False, 'available': False, 'price': 500, 'name': 'Bar', 'desc': 'Serve drinks and snacks to your customers! ',
              # 'img': 'content/buildings/upgrades/bar.jpg'},
        # '2': {'id': 2, 'active': False, 'available': False, 'price': 200, 'name': 'Draught Beer', 'desc': 'Chilled brew served in cold glassware, like a nectar from gods themselves. ',
              # 'img': 'content/buildings/upgrades/beer.jpg'},
        # '3': {'id': 3, 'active': False, 'available': False, 'price': 300, 'name': 'Tapas', 'desc': 'Tasty snacks that are just perfect with cold draught beer. ',
              # 'img': 'content/buildings/upgrades/tapas.jpg'}
        # }

    # self.upgrades['garden'] = {
        # '1': {'id': 1, 'active': False, 'available': False, 'price': 150, 'name': 'Flowerbeds', 'desc': 'Live Flowers for your girls to improve the grim designs of work in brothel. ',
              # 'img': 'content/buildings/upgrades/flowers.jpg'},
        # '2': {'id': 2, 'active': False, 'available': False, 'price': 500, 'name': 'Garden', 'desc': 'Beautiful garden to relax in for your girls and customers. Will have positive effect on Rest and Costumer Satisfaction',
              # 'img': 'content/buildings/upgrades/garden.jpg'},
        # '3': {'id': 3, 'active': False, 'available': False, 'price': 1000, 'name': 'Landscape Design', 'desc': 'Create a landscape filled with the most beautiful flora for amusement and enjoyment of your girls and customers alike!',
              # 'img': 'content/buildings/upgrades/landscape.jpg'}
        # }

    # self.upgrades['room_upgrades'] = {
        # '1': {'id': 1, 'active': False, 'available': False, 'price': 400, 'name': 'Improved Interior', 'desc': "Every room in brothel will be decorated in proper fashion! (+1/10 of the price for every room in the brothel)",
              # 'img': 'content/buildings/upgrades/room.jpg', "room_dependant": True, "room_upgrade": 40},
        # '2': {'id': 2, 'active': False, 'available': False, 'price': 800, 'name': 'Luxury Rooms', 'desc': "Room design farther improved to provide the best atmosphere imaginable! (+1/10 of the price for every room in the brothel)",
              # 'img': 'content/buildings/upgrades/luxury_room.jpg', "room_dependant": True, "room_upgrade": 40},
        # '3': {'id': 3, 'active': False, 'available': False, 'price': 2000, 'name': 'VIP Rooms', 'desc': "Bit of an overkill if you ask me. Royalty would not look out of place in one of these rooms! (+1/10 of the price for every room in the brothel)",
              # 'img': 'content/buildings/upgrades/vip_room.jpg', "room_dependant": True, "room_upgrade": 120}
        # }

    # self.upgrades['guards'] = {
        # '1': {'id': 1, 'active': False, 'available': False, 'price': 1000, 'name': 'Guard Quarters', 'desc': "Comforable locale for warriors guarding the building. (5 girls max)",
              # 'img': 'content/buildings/upgrades/guard_qt.jpg', "security_bonus": 30},
        # '2': {'id': 2, 'active': False, 'available': False, 'price': 1500, 'name': 'Training Quarters', 'desc': "Place for your guards to improve their skills when there is nothing else to do. ",
              # 'img': 'content/buildings/upgrades/training_qt.jpg', "security_bonus": 25},
        # '3': {'id': 3, 'active': False, 'available': False, 'price': 2000, 'name': 'Sparring Quarters', 'desc': "Your guards can harness their skills by safely fighting one another. ",
              # 'img': 'content/buildings/upgrades/sparring_qt.jpg', "security_bonus": 25}
        # }

    # self.upgrades['stripclub'] = {
        # '1': {'id': 1, 'active': False, 'available': False, 'price': 1000, 'name': 'Strip Club', 'desc': 'Skilled and beautiful Strippers are the key to filling your Club and Bar with Costumers! ',
              # 'img': 'content/buildings/upgrades/strip_club.jpg'},
        # '2': {'id': 2, 'active': False, 'available': False, 'price': 700, 'name': 'Large Podium', 'desc': 'Equip your club with a better podium for your girls to dance on! ',
              # 'img': 'content/buildings/upgrades/podium.jpg'},
        # '3': {'id': 3, 'active': False, 'available': False, 'price': 2000, 'name': 'Golden Cages', 'desc': 'Girls now can strip inside golden cages, truly a show to behold! ',
              # 'img': 'content/buildings/upgrades/golden_cage.jpg'}
        # }

    # self.upgrades['mainhall'] = {
        # '1': {'id': 1, 'active': False, 'available': False, 'price': 500, 'name': 'Main Hall', 'desc': 'All customers will have to go through this beautiful hall! This can increase reputation, customer satisfaction as well as improve security. ',
              # 'img': 'content/buildings/upgrades/main_hall.jpg', "security_bonus": 30, "whore_mult": 0.1},
        # '2': {'id': 2, 'active': False, 'available': False, 'price': 700, 'name': 'Reception', 'desc': 'Reception to improve income and customer satisfaction through good organization and service. ',
              # 'img': 'content/buildings/upgrades/reception.jpg', "security_bonus": 50, "whore_mult": 0.1},
        # '3': {'id': 3, 'active': False, 'available': False, 'price': 1000, 'name': 'Statue of Sex Goddess', 'desc': 'Great way to improve fame and income of your brothel! ',
              # 'img': 'content/buildings/upgrades/statue_sexgoddess.jpg', "whore_mult": 0.2}
        # }

    # Guard events delimiters
    # self.guardevents = dict(prostituteattackedevents = 0, barbrawlevents = 0)

Old code from Building next_day, dealt with (old) security rating and upgrades.
# Taking care of security rating:
# Without logging for now
# TODO: Move to WarriorQuarters!
# if self.upgrades['mainhall']['2']['active']: self.security_rating -= self.get_clients()
# elif self.upgrades['mainhall']['1']['active']: self.security_rating -= self.get_clients() * 2
self.security_rating -= self.total_clients * 3
if self.security_rating < 0: self.security_rating = 0

security_power = 0
guardslist = self.get_girls("Guard")

for guard in guardslist:
    security_power += (guard.attack + guard.defence + guard.magic) / 3

self.security_rating += int(security_power * ((self.security_presence/10)+1))
if self.security_rating < 0: self.security_rating = 0
if self.security_rating > 1000: self.security_rating = 1000

txt.append("Security Rating in now %d out of 1000, you currently have %d guards on duty with security presence of %d %%. \n\n"% (self.security_rating, len(guardslist), self.security_presence))

# Effects from upgrades:
# TODO: Upgrade to new style!
# if self.upgrades['mainhall']['3']['active']:
    # txt += "Statue in your main hall spreads mystical energy, your brothel will soon be known through out the whole word! \n"
    # self.modfame(1)
    # tmodrep += 1
    # self.modrep(1)
    # tmodfame += 1

# if self.upgrades['mainhall']['2']['active']:
    # txt += "Clients loved having a reception where they could enquire about girls, prices and possibilities. \n"
    # repinc = choice([0, 0, 1])
    # self.modrep(repinc)



class SmartTrackerOld(_list):
    """
    Basically a smart list that tracks anything that can be added by items and events/game.
    Prevents removal when unequipping items and/or other types of ralated errors/bugs.
    """
    def __init__(self, instance, be_skill=True):
        _list.__init__(self)
        self.instance = instance # Owner of this object, this is being instanciated as character.magic_skills = SmartTracker(character)
        self.normal = set() # Normal we concider anything that's been applied by normal game operations like events, loading routines and etc.
        self.items = dict() # Stuff that's been applied through items, it's a counter as multiple items can apply the same thing (like a trait).
        self.be_skill = be_skill # If we expect a be skill or similar mode.
        # raise Exception("zzzz", self.instance)

    def __getattr__(self, item):
        raise AttributeError("%s object has no attribute named %r, __dict__: %s" %
                             (self.__class__.__name__, item, self.__dict__))

    def set_instance(self, instance):
        self.instance = instance

    def append(self, item, normal=True):
        # Overwriting default list method, always assumed normal game operations and never adding through items.
        # ==> For battle & magic skills:
        if self.be_skill:
            if isinstance(item, basestring):
                if item in store.battle_skills:
                    item = store.battle_skills[item]
                else:
                    devlog.warning("Tried to apply unknown skill %s to %s!" % (item, self.instance.__class__))
                    return
        if normal: #  Item applied by anything other than that
            self.normal.add(item)
        else:
            self.items[item] = self.items.get(item, 0) + 1

        # The above is enough for magic/battle skills, but for traits... we need to know if the effects should be applied.
        if item in self.normal or self.items.get(item, 0) > 0:
            if not item in self:
                super(SmartTracker, self).append(item)
                return True

    def remove(self, item, normal=True):
        # Overwriting default list method.
        # ==> For battle & magic skills:
        if self.be_skill:
            if isinstance(item, basestring):
                if item in store.battle_skills:
                    item = store.battle_skills[item]
                else:
                    devlog.warning("Tried to remove unknown skill %s from %s!" % (item, self.instance.__class__))
                    return
        if normal:
            if item in self.normal:
                self.normal.remove(item)
        else:
            self.items[item] = self.items.get(item, 0) - 1

        # The above is enough for magic/battle skills, but for traits... we need to know if the effects should be applied.
        if not item in self.normal and self.items.get(item, 0) <= 0:
            if item in self:
                super(SmartTracker, self).remove(item)
                return True

class ExplorationData(Job):
    def __init__(self):
        """Creates a new GuardJob.
        """
        super(GuardJob, self).__init__()
        self.id = "Guarding"
        self.type = "Combat"

        # Traits/Job-types associated with this job:
        self.occupations = ["Warrior"] # General Strings likes SIW, Warrior, Server...
        self.occupation_traits = [traits["Warrior"], traits["Mage"], traits["Knight"], traits["Shooter"], traits["Battle Mage"]] # Corresponding traits...

        # Relevant skills and stats:
        self.skills = ["cleaning"]
        self.stats = ["agility"]

        workermod = {}
        self.locmod = {}

    def __call__(self):
        pass

    def explore(self):
        """Makes a ND report of the Exploration run.
        """
        # Create a dict of characters to enable im.Sepia (=dead)) when constructing the image.
        # False for alive and True for dead.
        characters = {c: False for c in self.team}
        dead = 0

        for char in self.team:
            if worker.location != "After Life":
                worker.action = None
                worker.location = worker.flag("loc_backup")
                worker.del_flag("loc_backup")

                for stat in self.stats:
                    if stat == "exp":
                        self.stats[stat] = worker.adjust_exp(self.stats[stat])
                        worker.exp += self.stats[stat]
                    else:
                        worker.mod_stat(stat, self.stats[stat])

            else:
                characters[char] = True
                dead = dead + 1

        # Handle the dead chars:
        skip_rewards = False

        if dead:
            if len(self.team) == dead:
                log.append("\n{color=[red]}The entire party was wiped out (Those poor girlz...)! This can't be good for your reputation (and you obviously not getting any rewards))!{/color}\n")
                hero.reputation -= 30
                skip_rewards = True

            else:
                log.append("\n{color=[red]}You get reputation penalty as %d of your girls never returned from the expedition!\n{/color}" % dead)
                hero.reputation -= 7*dead

        if not skip_rewards:
            # Rewards + logging in global area
            cash = sum(self.cash)
            hero.add_money(cash, reason="Fighters Guild")
            fg.fin.log_logical_income(cash, "Fighters Guild")

            for item in self.items:
                hero.inventory.append(items[item])

            self.cash = sum(self.cash)
            if self.captured_girl:
                # We place the girl in slave pens (general jail of pytfall)
                jail.add_prisoner(self.captured_girl, flag="SE_capture")
                log.append("{color=[green]}\nThe team has captured a girl, she's been sent to City Jail for 'safekeeping'!{/color}\n")

            area = fg_areas[self.area.id]
            area.known_items |= set(self.found_items)
            area.cash_earned += self.cash
            area.known_mobs |= self.area.known_mobs

            for key in area.unlocks.keys():
                area.unlocks[key] += randrange(1, int(max(self.day, (self.day * self.risk/25), 2)))

                if dice(area.unlocks[key]):
                    if key in fg_areas:
                        fg_areas[key].unlocked = True
                        log.append("\n {color=[blue]}Team found Area: %s, it is now unlocked!!!{/color}" % key)

                    del area.unlocks[key]

        fg.exploring.remove(self)

        if not self.flag_red:
            self.flag_green = True
            fg.flag_green = True

        if self.flag_red:
            fg.flag_red = True

        # Create the event:
        evt = NDEvent()
        evt.red_flag = self.flag_red
        evt.green_flag = self.flag_green
        evt.charmod = self.stats
        evt.type = 'exploration_report'
        evt.char = None
        self.loc = fg

        # New style:
        args = list()
        for g in characters:
            if characters[g]:
                # Dead:
                args.append(im.Sepia(g.show("battle_sprite", resize=(200, 200), cache=True)))

            else:
                # Alive!
                args.append(g.show("battle_sprite", resize=(200, 200), cache=True))

        # args = list(g.show("battle_sprite", resize=(200, 200), cache=True) for g in self.team)
        img = Fixed(ProportionalScale(self.area.img, 820, 705, align=(0.5, 0.5)),
                    Text("%s"%self.team.name, style="agrevue", outlines=[ (1, crimson, 3, 3) ], antialias=True, size=30, color=red, align=(0.5, 0)),
                    HBox(*args, spacing=10, align=(0.5, 1.0)),
                    xysize=(820, 705))

        evt.img = img
        evt.txt = "".join(log)
        NextDayEvents.append(evt)

class ServiceJob(Job):
    """The class that solves Bartending, Waitressing and Cleaning.

    TODO: Rewrite to work with SimPy! *Or this actually should prolly be split into three Jobs...
    """
    def __init__(self):
        """
        This is meant to pick a job that makes most sense out if Cleaning, Service and Bartending
        """
        super(ServiceJob, self).__init__()
        self.type = "Service"

        # Traits/Job-types associated with this job:
        self.occupations = ["Server"] # General Strings likes SIW, Warrior, Server...
        # self.occupation_traits = [traits["Service"]] # Corresponding traits...

    def __call__(self, char, loc):
        worker, self.loc = char, loc

        self.task = None # Service task

        # Get the ap cost and cash it
        if worker.AP >= 2:
            aprelay = choice([1, 2])
            self.APr = aprelay
            worker.AP -= aprelay
        else:
            self.APr = worker.AP
            worker.AP = 0

        workermod = {}
        self.locmod = {}

        # tl.timer("Life/Injury/Vitality")
        self.check_life()
        if not self.finished: self.check_injury()
        if not self.finished: self.check_vitality()

        # tl.timer("Occupation", nested=False)
        if not self.finished: self.check_occupation()

        # tl.timer("Client Relay", nested=False)
        if not self.finished: self.client_relay()

        # tl.timer("Setting task", nested=False)
        if not self.finished: self.set_task()

        # tl.timer("Bar", nested=False)
        if self.task == "Bar" and not self.finished: self.bar_task()

        # tl.timer("Club", nested=False)
        if self.task == 'Club' and not self.finished: self.club_task()

        # tl.timer("Clean", nested=False)
        if not self.finished: self.cleaning_task()
        # tl.timer("Clean")

    def check_occupation(self):
        """Checks the workers occupation against the job.
        """
        if [t for t in self.all_occs if t in worker.occupations]:
            if worker.status == 'slave':
                log.append(choice(["%s has no choice but to agree to clean and serve tables."%worker.fullname,
                                                    "She'll clean and tend to customer needs for you, does not mean she'll enjoy it.",
                                                    "%s is a slave so she'll do as she is told. However you might want to concider giving her work fit to her profession."%worker.name]))

                log.logws("joy", -3)

            elif worker.disposition < 700:
                log.append(choice(["%s refused to serve! It's not what she wishes to do in life."%worker.name,
                                        "%s will not work as a Service Girl, find better suited task for her!"%worker.fullname]))

                log.logws('disposition', -50)
                self.img = worker.show("profile", "confident", "angry", "uncertain", exclude=["happy", "sad", "ecstatic", "suggestive"], resize=(740, 685), type="normal")

                worker.action = None
                self.apply_stats()
                self.finish_job()

            else:
                log.append("%s reluctantly agreed to be a servicer. It's not what she wishes to do in life but she admires you to much to refuse. "%worker.name)

        else:
            log.append(choice(["%s will work as a service girl!"%worker.name,
                                    "Cleaning, cooking, bartending...",
                                    "%s will clean or tend to customers next!"%worker.fullname]))

        if isinstance(log, list):
            log.append("\n")

    def set_task(self):
        """
        Sets the task for the girl.
        """
        if self.loc.servicer['second_round']:
            if not worker.autocontrol['S_Tasks']['clean']:
                log.append("%s will not clean (check her profile for more information)." % worker.nickname)
                self.img = 'profile'
                self.apply_stats()
                workers.remove(worker)
                self.finish_job()
            elif self.loc.dirt > 0:
                self.task = "Cleaning"
            else:
                workers.remove(worker)

        elif self.loc.get_dirt_percentage()[0] > 80 and not worker.autocontrol['S_Tasks']['clean']:
            if self.loc.auto_clean:
                self.auto_clean()
                if self.loc.get_dirt_percentage()[0] <= 80:
                    self.set_task()
                    return
                else:
                    log.append("%s doesn't clean and you do not have the fund to pay professional cleaners!" % worker.nickname)
                    self.img = 'profile'
                    self.apply_stats()
                    workers.remove(worker)
                    self.finish_job()
                    return

            elif worker.autocontrol['S_Tasks']['clean']:
                log.append("Your brothel was too dirty for any task but cleaning!")
                self.task = "Cleaning"

        elif self.loc.servicer['barclientsleft'] > 0 or self.loc.servicer['clubclientsleft'] > 0:
            if self.loc.servicer['barclientsleft'] > 0 and self.loc.servicer['clubclientsleft'] > 0:
                if worker.autocontrol['S_Tasks']['bar'] and worker.autocontrol['S_Tasks']['waitress']:
                    self.task = choice(['Bar', 'Club'])
            elif self.loc.servicer['barclientsleft'] > 0 and worker.autocontrol['S_Tasks']['bar']:
                self.task = "Bar"
            elif self.loc.servicer['clubclientsleft'] > 0 and worker.autocontrol['S_Tasks']['waitress']:
                self.task = "Club"
            elif self.loc.dirt > 0 and worker.autocontrol['S_Tasks']['clean']:
                self.task = "Cleaning"
            else:
                log.append("There were no tasks remaining or this girl is not willing to do them (check her profile for more info).")
                self.img = 'profile'
                self.apply_stats()
                workers.remove(worker)
                self.finish_job()

        elif self.loc.dirt > 0 and worker.autocontrol['S_Tasks']['clean']:
            self.task = "Cleaning"

        log.append("\n")

    def bar_brawl_event(self):
        """
        Solve for bar brawls.
        """
        aggressive_clients = [client for client in self.clients if "Aggressive" in client.traits]

        if self.task == 'Bar':
            # Brawl event (For now activates on pure chance, should be improved upon later)
            # TODO!: Refactor to activate on clientList after traits are hardcoded in clients class!

            if len(aggressive_clients) >= 2 and self.loc.guardevents['barbrawlevents'] < 1 and not dice(self.loc.security_rating/10):
                # Relay
                self.loc.guardevents['barbrawlevents'] += 1

                if self.loc.servicer['barclientsleft'] < 10:
                    pass

                else:
                    log.append("{color=[red]}%s has spotted a number of customers about to start trouble. "%(worker.fullname))
                    log.append("She immediately called for security! \n{/color}")

                    if not solve_job_guard_event(self, "bar_event", clients=self.loc.servicer["barclientsleft"], enemies=aggressive_clients, no_guard_occupation="ServiceGirl"):
                        self.apply_stats()
                        self.finish_job()

            if not self.finished:
                log.append("\n")


    class NextGenWhoreJob(Job):
        """
        The class that solves whoring jobs.
        @ Abandoned until 1.0 due to complexity of adding new content.
        """
        def __init__(self):
            """
            Creates a new WhoreJob.
            worker = The worker this job is for.
            client = The client this worker is servicing.
            loc = The brothel this worker is in.
            workers = The list of workers this worker is in.
            clients = The list of clients this client is in.
            """
            super(WhoreJob, self).__init__()
            self.id = "Whore Job"

            # Traits/Job-types associated with this job:
            self.occupations = list() # General Strings likes SIW, Warrior, Server...
            self.occupation_traits = [traits["Prostitute"]] # Corresponing traits...

            # TODO: Rewrite for skills? Or simply leave it like this and add skills with a check in this dict...
            self.workermod = {}

            self.locmod = 0

        def __call__(self):
            self.reset()

            self.event_type = "jobreport"
            self.worker, self.client, self.loc = store.char, store.clients.pop(), store.char.location
            self.workermod, self.locmod = {}, {}
            self.skill = None

            # if not self.finished: self.check_injury()
            # if not self.finished: self.check_vitality()

            # Returning client to the list if girl wasn't actually availible TODO:
            # if self.finished:
                # self.client.traitmatched = False
                # self.clients.append(client)
                # return

            # if self.check_dirt(): TODO:
                # global stop_whore_job
                # stop_whore_job = True

            if not self.finished: self.check_occupation()

            # AP cost of the job if all checks for refusals have failed.
            if not self.finished:
                self.worker.AP -= 1
                self.payout_mod()

            # if not self.finished: self.guard_event()

            if not self.finished: self.acts()

        def check_rank(self):
            """
            @Review: We are disabling ranks until better times :)
            Checks the whore rank against the client rank.
            """
            if self.worker.rank < self.client.rank - 2 and self.worker.status == 'free':
                self.txt.append("The customer quickly realized that %s was too poor of a whore rank to bother with her, "%self.worker.name + \
                                "%s pushed her out of the way as if she was not even there and left pissed at the establishment... \n"%self.client.pronoun)

                self.txt.append("You should not forget that people in PyTFall take prostitute ranks very seriously and all workers who choose that lifestyle or were forced into it, "+ \
                                "should strive to improve rank. Being told that she was not good enough is not likely to increase your workers happiness... ")

                self.locmod['reputation'] -= (randint(1, 5) + self.client.rank)
                self.workermod['joy'] -= randint(4, 10)

                self.img = self.worker.show("profile", "sad", resize=(740, 685))

                self.apply_stats()
                self.finish_job()
                return

            elif self.client.rank < self.worker.rank - 2 and self.worker.status != 'slave':
                self.txt.append("This customer of yours can go to hell! %s is not worthy of even kissing my feet!  \n"%self.client.pronoun)
                self.txt.append("Even if an event like this was to damage your brothels reputation, such damage would be insignificant because noone would want to brag about a girl refusing them. \n")

                self.locmod['reputation'] -= randint(0, 1)

                self.img = self.worker.show("profile", "angry", resize=(740, 685))

                self.apply_stats()
                self.finish_job()
                return

            elif self.client.rank < self.worker.rank - 2 and self.worker.status == 'slave':
                self.txt.append("%s didn't want to fuck someone so far below her own hard earned rank, but slaves have little choice...' "%self.worker.name)
                self.workermod['joy'] -= 10

        def check_occupation(self):
            """
            Checks the workers occupation.
            # TODO: We need to check this when assigning to Job! Not during it!
            # Still, we'll check this...
            """
            if [t for t in self.occupation_traits if t in self.worker.occupations]:
                if self.worker.status != 'slave' and self.worker.disposition > 900:
                    self.txt.append("%s: I am not thrilled about having some stranger 'do' me but you've been really good to me so... " % self.worker.nickname)
                    self.loggs('disposition', -randint(10, 30))

                elif self.worker.status != 'slave':
                    self.txt.append(choice(["%s: I am not some cheap whore that will do whatever you please! Find someone else for this debauchery! " % self.worker.nickname,
                                                         "Don't be absurd, I am not fucking anyone for you!"]))

                    self.loggs('disposition', -50)
                    self.img = self.worker.show("profile", "angry", resize=(740, 685))
                    self.worker.action = None

                    self.apply_stats()
                    self.finish_job()
                    return

                else:
                    self.txt.append(choice(["%s is a slave so noone really cares but doing something that's not a part of her job has upset her a little bit." % self.worker.name,
                                                         "She'll do as she is told, doesn't mean that she'll be happy about.",
                                                         "%s will do as you command but you cannot expect her to enjoy this..." % self.worker.fullname]))

                    self.loggs('joy', -randint(1, 3))

            else:
                self.txt.append(choice(["{} is doing her shift as Prostitute!".format(self.worker.name),
                                                     "%s does her shift as a Prostitute!" % self.worker.fullname,
                                                     "{color=[red]}Whore?{/color} WTF?? I am a {color=[pink]}Fancy Girl!!!{/color}"]))

            self.txt.append("\n\n")

        # I need to rebuild relay so it makes more sense and then rewrite this method
        # Doing it now :)
        def payout_mod(self):
            # No matched traits
            self.payout = 1

            if not self.client.traitmatched:
                if self.client.favtraits:
                    self.txt.append("%s came to the %s looking for a girl with a %s traits but didn't find one so %s picked %s randomly. \n"%(self.client.caste,
                                                                                                                                                                                                                  self.loc.name, ", ".join(self.client.favtraits),
                                                                                                                                                                                                                  self.client.pronoun.lower(),
                                                                                                                                                                                                                  self.worker.fullname))
                else:
                    self.txt.append("%s came to the %s brothel. Not wanting any kind of girl in particular %s went for %s. \n"%(self.client.caste,
                                                                                                                                self.loc.name,
                                                                                                                                self.client.pronoun.lower(),
                                                                                                                                self.worker.name))
            else:
                self.txt.append("%s came into %s and was looking for a girl with %s traits so %s went straight for %s. \n"%(self.client.caste,
                                                                                                                            self.loc.name,
                                                                                                                            ", ".join(self.client.favtraits),
                                                                                                                            self.client.pronoun.lower(),
                                                                                                                            self.worker.name))
                self.payout = int(self.payout * 1.3)

            # Building room upgrades modifiers, simple version for now
            # Might have to be improved to match customers expectations based on their castes later
            # bru = self.loc.get_upgrade_mod("room_upgrades")
            # if bru == 3:
                # self.txt.append("Any of your customers would be willing to chop off a finger just to spend a couple of hours in room so fine. "+ \
                                # "The companionship that %s provides is just a bonus. \n"%self.worker.nickname)
                # self.workermod['joy'] += choice([0,0,3])
                # self.workermod['refinement'] += choice([0,0,0,0,3])
                # self.payout = int(self.payout * 1.6)
            # elif bru == 2:
                # self.txt.append("Luxury rooms had every convenience that could possibly spice up the upcoming intercource, this was definitely a sound investment on your part. \n")
                # self.workermod['joy'] += choice([0,0,2])
                # self.workermod['refinement'] += choice([0,0,0,0,2])
                # self.payout = int(self.payout * 1.3)
            # elif bru == 1:
                # self.txt.append("Improved rooms interior with an exotic sexual theme were much appreciated by your girl and her client. \n")
                # self.workermod['joy'] += choice([0,0,1])
                # self.workermod['refinement'] += choice([0,0,0,1])
                # self.payout = int(self.payout * 1.2)

            self.txt.append("\n")

            # Statisfaction is determined by dividing total satisfaction by the number of strippers.
            # Can run high since strippers can go more than for one round a day but that shouldn't be a problem or can be balanced out later.
            # if self.client.seenstrip:
                # satisfaction = self.client.stripsatisfaction / self.loc.servicer['strippers']
                # if satisfaction <= 0:
                    # self.txt.append('Customer seemed really put off by an earlier stripper performance, this will cost you a lot of income, consider doing something about your strippers! \n ')
                    # self.payout = int(self.payout*0.5)
                # elif satisfaction <= 25:
                    # self.client.libido -= 80
                    # self.txt.append("Client is in a bad mood due to a strippers poor performance in your club! This will cost you some income. \n")
                    # self.payout = int(self.payout*0.7)
                # elif satisfaction <= 50:
                    # self.txt.append("Client is definitely not disappointed with the strippers performance in your club! This means a bit of extra income for you. \n")
                    # self.payout = int(self.payout*1.1)
                # elif satisfaction <= 75:
                    # self.txt.append("Client was really pleased with the strippers performance in the club and craving for a good fuck as a result! This means extra income for you. \n")
                    # self.payout = int(self.payout*1.2)
                # elif satisfaction <= 100:
                    # self.txt.append("Customer was crazed with passion after seeing the most amazing stripper performance in your club! This means a lot of extra income for you. \n")
                    # self.payout = int(self.payout*1.5)
                # self.txt.append("\n")

        def guard_event(self):
            """
            Solves guard events for agressive clients.
            """
            if "Aggressive" in self.client.traits and self.loc.guardevents["prostituteattackedevents"] < int(self.loc.id * 1.5) and not dice(self.loc.security_rating/10):
                # Relay
                self.loc.guardevents["prostituteattackedevents"] += 1
                self.txt.append("{color=[red]}Getting ready for some action with %s, %s became violent and threatened to beat the shit out of your girl.{/color} \n"%(self.worker.name,
                                                                                                                                                                      self.client.pronoun.lower()))

                # If conflict is not resolved, act ends here, else act goes on to interactions.
                # Function calls girls.remove(girl) for us. # TODO: Get Rid of this!
                if not solve_job_guard_event(self, "whore_event", enemies=self.client):
                    self.apply_stats()
                    self.finish_job()

        def acts(self):
            """Solves the sexual acts performed by the worker.
            """
            # Get the unique sex case
            if self.client.act in pytWhoringActs: act = pytWhoringActs[self.client.act].for_girl(self.worker)
            else: act = pytWhoringActs["sex"].for_girl(self.worker)

            # Act text and image
            if act.has_preface: self.txt.append(act.get_preface())
            self.txt.append(act.get_text())
            self.img = act.get_image()

            # Virginity checks
            if act.is_vaginal and "Virgin" in self.worker.traits:
                tips = self.worker.charisma * 10
                self.txt.append("\n{color=[pink]}%s lost her virginity!{/color} The customer thought it was super hot so he left a tip of {color=[gold]}%d Gold{/color}.\n\n"%(self.worker.nickname, tips))
                self.worker.remove_trait(traits["Virgin"])
                self.worker.fin.log_tips(tips, "WhoreJob")
                self.loc.fin.log_logical_income(tips, "WhoreJob")

            else:
                self.txt.append("\n")

            # Skill
            t, m = act.get_skill()
            self.txt.append(t + "\n")
            self.loggs("exp", randint(15, 25))
            self.loggs("joy", m)

            # Improvement:
            sexmod = 1 if dice(20) else 0
            constmod = 1 if dice(12) else 0
            # TODO: Rewrite to work with skillz!
            self.loggs("normalsex", sexmod)
            self.loggs("constitution", constmod)
            self.loggs("vitality", -randint(18, 28))

            if sexmod + constmod > 0:
                self.txt.append("\n%s feels like she learned something! \n"%self.worker.name)
                self.loggs("joy", 1)

            # Dirt:
            self.logloc("dirt", randint(2, 5))

            # Log income for girl and MC:
            self.txt.append("{color=[gold]}\nA total of %d Gold was earned!{/color}"%self.payout)
            self.worker.fin.log_logical_income(self.payout, "WhoreJob")
            self.loc.fin.log_logical_income(self.payout, "WhoreJob")

            self.apply_stats()
            self.finish_job()


    class Job(Job):
        # Whole Job:
        def check_rank(self):
            """
            @Review: We are disabling ranks until better times :)
            Checks the whore rank against the client rank.
            """
            if self.char.rank < self.client.rank - 2 and self.char.status == 'free':
                self.txt.append("The customer quickly realized that %s was too poor of a whore rank to bother with her, "%self.char.name + \
                                "%s pushed her out of the way as if she was not even there and left pissed at the establishment... \n"%self.client.pronoun)

                self.txt.append("You should not forget that people in PyTFall take prostitute ranks very seriously and all workers who choose that lifestyle or were forced into it, "+ \
                                "should strive to improve rank. Being told that she was not good enough is not likely to increase your girls happiness... ")

                self.locmod['reputation'] -= (randint(1, 5) + self.client.rank)
                self.workermod['joy'] -= randint(4, 10)

                self.img = self.char.show("profile", "sad", resize=(740, 685))

                self.apply_stats()
                self.finish_job()
                return

            elif self.client.rank < self.char.rank - 2 and self.char.status != 'slave':
                self.txt.append("This customer of yours can go to hell! %s is not worthy of even kissing my feet!  \n"%self.client.pronoun)
                self.txt.append("Even if an event like this was to damage your brothels reputation, such damage would be insignificant because noone would want to brag about a girl refusing them. \n")

                self.locmod['reputation'] -= randint(0, 1)

                self.img = self.char.show("profile", "angry", resize=(740, 685))

                self.apply_stats()
                self.finish_job()
                return

            elif self.client.rank < self.char.rank - 2 and self.char.status == 'slave':
                self.txt.append("%s didn't want to fuck someone so far below her own hard earned rank, but slaves have little choice...' "%self.char.name)
                self.workermod['joy'] -= 10

        def guard_event(self):
            """
            Solves guard events for agressive clients.
            """
            if "Aggressive" in self.client.traits and self.loc.guardevents["prostituteattackedevents"] < int(self.loc.id * 1.5) and not dice(self.loc.security_rating/10):
                # Relay
                self.loc.guardevents["prostituteattackedevents"] += 1
                self.txt.append("{color=[red]}Getting ready for some action with %s, %s became violent and threatened to beat the shit out of your girl.{/color} \n"%(self.worker.name,
                                                                                                                                                                      self.client.pronoun.lower()))

                # If conflict is not resolved, act ends here, else act goes on to interactions.
                # Function calls girls.remove(girl) for us. # TODO: Get Rid of this!
                if not solve_job_guard_event(self, "whore_event", enemies=self.client):
                    self.apply_stats()
                    self.finish_job()

        def auto_clean(self):
            """
            Auto cleans the building if needed.
            """
            if isinstance(self.loc, DirtyBuilding):
                if self.loc.auto_clean and self.loc.get_dirt_percentage()[0] > 80:
                    price = self.loc.get_cleaning_price()
                    if hero.take_money(price, reason="Pro-Cleaning"):
                        self.loc.fin.log_expense(price, "Pro-Cleaning")
                        self.loc.dirt = 0
                        self.txt.append("Cleaners were hired to tidy up your building. Cost: {color=[gold]} %s Gold.{/color}\n\n"%price)

                    else:
                        self.txt.append("You did not have enough funds to pay for the professional cleaning service (%d Gold).\n\n"%price)

        def check_dirt(self):
            """
            Checks the dirt for the building and reports it.
            """
            if isinstance(self.loc, DirtyBuilding):
                if self.loc.get_dirt_percentage()[0] > 80:
                    self.txt.append(choice(["Your building looks like a pigstall, fix this or keep losing your clients!",
                                                         "Your building is to dirty to do business!",
                                                         "Clean your damn establishment or keep losing money and rep!"]))

                    if dice(self.loc.get_dirt_percentage()[0]):
                        self.locmod["reputation"] -= randint(2, 5)

                    self.apply_stats()
                    self.img = self.worker.show("profile", "angry", resize=(740, 685))
                    self.finish_job()

                    return True

                else:
                    return False

            else:
                return False

        # REST JOB:
        def trait_events(self):
            """
            Solve events for certain traits.
            TODO: Currently disabled due to being useless anyhow... restore when ready.
            """
            # Prepear the lists:
            rgList = list(entry for entry in hero.chars if entry.location == self.loc and entry.action in ['Rest', 'AutoRest'])
            rgList.remove(self.worker)
            gl = rgList * 1

            evcount = 0
            loopcount = 0

            while self.worker.traits and evcount == 0 and loopcount < 5:
                tgl = list() # Temporary Girls List...
                rt = choice(self.worker.traits)

                if evcount < 1: # rt = randomtrait
                    if "Magic Gift" == rt:
                        for girl in gl:
                            if set(["Magic Gift" , "Magic Talent"]).intersection(girl.traits) and girl.action in ["Rest", "AutoRest"]:
                                tgl.append(girl)

                        if tgl:
                            secondgirl = choice(tgl)
                            self.txt.append("She took some time idly discussing the finer aspects of magic with %s. \n"%secondgirl.name)
                            self.img = self.worker.show("profile", "happy", resize=(740, 685))
                            secondgirl.magic += choice([0, 0, 0, 1])

                        elif dice(75) and self.loc.upgrades['garden']['2']['active']:
                            self.txt.append("She used her day off to harvest ingredients for her spells in the garden. \n")
                            self.img = self.worker.show("rest", "generic outdoor", "forest", "meadow", resize=(740, 685))

                        elif self.worker.reputation > 75 and self.worker.status != "slave":
                            self.txt.append("She decided to take a walk in the city, ending up showing magic tricks to local children. \n")
                            self.img = self.worker.show("profile", "urban", resize=(740, 685))

                            if dice(20):
                                self.workermod["reputation"] += 1

                            self.workermod["joy"] += 1

                        else:
                            self.txt.append("She spent her time reading her Arcane book and unfriendly staring at passersby. \n")
                            self.img = self.worker.show("reading", resize=(740, 685))

                        evcount += 1

                    elif "Magic Talent" == rt:
                        for girl in gl:
                            if "Magic Talent" in girl.traits:
                                tgl.append(girl)

                        if tgl:
                            secondgirl = choice(tgl)
                            self.txt.append("With a little reluctance she shared a bit of her Arcane knowledge with %s in exchange for an evening dessert. \n"%secondgirl.name)
                            self.img = self.worker.show("profile", "happy", resize=(740, 685))
                            secondgirl.magic += choice([0, 0, 0, 1])

                        elif self.worker.status != 'slave' and self.loc.upgrades['garden']['2']['active']:
                            self.txt.append("Some customer tried to get it on with her and wouldn't leave her alone as she was resting in the garden, "+ \
                                            "until she summoned a small fireball and threatened to burn his hair. \n")
                            self.img = self.worker.show("rest", "generic outdoor", "forest", "meadow", resize=(740, 685), type="first_default")

                        else:
                            self.txt.append("She spent her day in her pocket dimension with every possible comfort. \n")
                            self.img = "rest"

                        evcount += 1

                    elif "Athletic" == rt:
                        if self.worker.status != 'slave':
                            self.txt.append("She spent her resting day on the beach taking occasional swims in the ocean. \n")
                            self.img = self.worker.show("beach", "bikini", "topless", exclude=["sex"], resize=(740, 685))
                            self.workermod['constitution'] += choice([0, 0, 0, 0, 1])

                        else:
                            self.txt.append("She spent her day off exercising, occasionally taking a break, believing that to be the best rest for her.  \n")
                            self.img = self.worker.show("exercising", "sport", resize=(740, 685), type="any")
                            self.workermod['constitution'] += choice([0, 0, 0, 0, 1])

                        evcount += 1

                    elif "Smart" == rt:
                        for girl in gl:
                            if set(["Smart" , "Genius"]).intersection(girl.traits) and girl.action in ["Rest", 'AutoRest']:
                                tgl.append(girl)

                        if tgl:
                            secondgirl = choice(tgl)
                            self.txt.append("She spent some time playing board games with %s. \n"%secondgirl.name)
                            self.img = self.worker.show("profile", "happy", resize=(740, 685))
                            self.workermod['intelligence'] += choice([0, 0, 0, 0, 1])
                            secondgirl.intelligence += choice([0, 0, 0, 0, 1])

                        else:
                            self.txt.append("She spent part of her rest day translating some runes from ancient looking books. \n")
                            self.img = self.worker.show("reading", "studying", resize=(740, 685), type="any")

                        evcount += 1

                    elif "Nerd" == rt:
                        if dice(60) and self.loc.upgrades['garden']['2']['active']:
                            self.txt.append("She used her day off trying to get some strange device in the garden to work. \n")
                            self.img = self.worker.show("rest", "generic outdoor", "forest", "meadow", resize=(740, 685), type="first_default")

                        else:
                            self.txt.append("She spent all day reading books in her room. \n")
                            self.img = self.worker.show("reading", "studying", resize=(740, 685), type="any")

                        evcount += 1

                    elif "Genius" == rt:
                        for girl in gl:
                            if set(["Smart", "Genius"]).intersection(girl.traits) and girl.action in ["Rest", 'AutoRest']:
                                tgl.append(girl)

                        if len(tgl) > 0:
                            secondgirl = choice(tgl)
                            self.txt.append("She spent some time playing board games with %s. \n"%secondgirl.name)
                            self.img = self.worker.show("profile", "happy", resize=(740, 685))
                            self.workermod['intelligence'] += choice([0,0,0,0,1])
                            secondgirl.intelligence += choice([0,0,0,0,1])

                        else:
                            self.txt.append("She spent part of her rest day translating some runes from ancient looking books. \n")
                            self.img = self.worker.show("reading", "studying", resize=(740, 685))

                        evcount += 1

                    elif rt in ['Long legs', 'Big Boobs', 'Abnormally Large Boobs', 'Great Arse', 'Great Figure']:
                        if self.worker.status != 'slave':
                            self.txt.append("She spent her time enjoying sunbathing as well as receiving envious and admiring glances on a local beach. Too bad you were too busy to join her. \n")
                            self.img = self.worker.show("beach", "bikini", "topless", exclude=["sex"], resize=(740, 685))
                            self.workermod['reputation'] += choice([0, 0, 0, 0, 1])

                        else:
                            self.txt.append("She spent better part of her rest day trying to figure out how to use her heavenly body features to her advantage. \n")
                            self.img = self.worker.show("profile", "exposed", "beauty", resize=(740, 685))
                            if dice(10):
                                self.workermod['charisma'] += 1

                        evcount += 1

                    elif "Nymphomaniac" == rt:
                        self.workermod['libido'] += 20
                        self.txt.append("She spent some of her day having fun with herself in her room. \n")
                        self.img = 'mast'
                        evcount += 1

                    elif "Exhibitionist" == rt:
                        if dice(70):
                            self.txt.append("Since she is going to walk around with barely any clothes on anyway, you asked her to do it around the brothel this time. "+ \
                                            "Free advertising is good for business, and she will have less problems with the city guards this way. \n")
                            self.img = self.worker.show("strip", "exposed", "topless", "nude", "undress", exclude=["sex"], resize=(740, 685), type="any")

                            if dice(10):
                                self.workermod['strip'] += 1

                            if dice(25):
                                self.workermod['joy'] += 3

                            if dice(75):
                                self.locmod["fame"] += 1

                            evcount += 1

                        else:
                            evcount += 1

                    elif "Professional Maid" == rt:
                        self.txt.append("Even though today is her day off, she insisted on doing some cleaning. \n")
                        self.img = self.worker.show("cleaning", resize=(740, 685))

                        if dice(10):
                            self.workermod['service'] += 1

                        self.locmod['dirt'] -= int(self.worker.serviceskill*0.2)

                        evcount += 1

                    loopcount += 1

            # If girl is down with cold:
            if self.worker.effects['Down with Cold']['active']:
                self.worker.effects['Down with Cold']['count'] += 2
                self.txt.append("Allowing her to rest is a really good idea considering that she has a cold! \n ")

            if self.worker.effects['Food Poisoning']['active']:
                self.worker.effects['Food Poisoning']['count'] += 2
                self.txt.append("Allowing her to rest is a really good idea considering that she has food poisoning! \n ")

            if evcount == 0:
                self.txt.append(choice(['%s took a break today. '%(self.worker.name),
                                        'She spent the day relaxing. ',
                                        '%s comfortably rested in her room. '%(self.worker.name)]))


    class FighterGuild(DirtyBuilding):
        """
        The Fighters Guild building.

        Looks like nothing can be salvadged from here for SimPy land, I'll leave this so the interface keeps working.
        """

        ACTIONS = ["Rest", "Training", "ServiceGirl", "BarGirl"]

        def __init__(self):
            """
            Creates a new Fighters Guild.
            """
            super(FighterGuild, self).__init__()
            self.fin = Finances(self)

            # Related to exploration code:
            self.exploring = list()
            self.focus_team = None

            # Building related:
            self.upgrades = OrderedDict()
            self.upgrades["bar"] = [False, "content/buildings/upgrades/bar.jpg", 5000]
            self.upgrades["healing onsen"] = [False, "content/buildings/upgrades/onsen.jpg", 10000]
            self.upgrades["sparring quarters"] = [False, "content/buildings/upgrades/sparring_qt.jpg", 20000]

            self.manager = None # Manager of the FG
            self.managers = dict() # Managers tracker (days counter)

            self.capture_girls = False

        def get_exp_chars(self):
            """
            Returns a list of all exploring girls
            """
            pass

        def get_team_price(self):
            """
            Gets the price for all the teams.
            """
            bp = 20000
            if len(self.teams):
                bp = bp + bp * self.multi * len(self.teams)

            return bp

        def next_day(self):
            """
            Solve the next day logic.
            """
            # Early reset:
            self.flag_red = False
            self.flag_green = False
            sg = None # Service Girl
            bg = None # Bar Girl

            stats = dict()
            txt = list()

            txt.append("Fighters Guild Reporting:\n\n")

            _girls = len(list(g for g in self.get_girls() if g.action == "Exploring"))
            girls = list(g for g in self.get_girls() if g.action != "Exploring")

            if _girls:
                txt.append("You currently have %d %s on Explorating!\n\n" % (_girls, plural("girl", _girls)))

            if girls:
                txt.append("There are %d %s in the guild!\n\n" % (len(girls), plural("girl", len(girls))))

            if not _girls and not girls:
                txt.append("There is nothing to report...")

            for g in girls:
                if g.action == "ServiceGirl":
                    if g.health < 60 or g.vitality < 35:
                        g.previousaction = g.action
                        g.action = "Rest"
                        girls.append(g)

                    else:
                        cleffect = int(round(self.APr * (12 + g.serviceskill * 0.25 + g.agility * 0.3)))
                        self.clean(cleffect)
                        sg = g

                        evt = NDEvent()
                        evt.type = 'fg_job'
                        evt.char = g
                        self.loc = fg
                        evt.img = g.show("maid", "cleaning", exclude=["sex"], resize=(740, 685), type="any")
                        evt.txt = choice(["[g.name] is taking care of the girls in the Guild.", "[g.nickname] keeping the Guild running, clean and happy :)"])
                        NextDayEvents.append(evt)

                elif g.action == "BarGirl":
                    if g.health < 60 or g.vitality < 35:
                        g.previousaction = g.action
                        g.action = "Rest"
                        girls.append(g)

                    else:
                        cleffect = int(round(self.APr * (12 + g.serviceskill * 0.25 + g.agility * 0.3)))/2
                        self.clean(cleffect)
                        sg = g

                        evt = NDEvent()
                        evt.type = 'fg_job'
                        evt.char = g
                        self.loc = fg
                        evt.img = g.show("waitress", "maid", exclude=["sex"], resize=(740, 685), type="any")
                        evt.txt = choice(["[g.name] took care of the Bar and the guild, making sure all of the members were happy.", "[g.nickname] keeping the Bar running and the Guild clean and happy :)"])
                        NextDayEvents.append(evt)

                elif g.action == "Training":
                    if g.health < 60 or g.vitality < 35:
                        g.previousaction = g.action
                        g.action = "Rest"
                        girls.append(g)

                    else:
                        FG_CombatTraining(g)

                elif g.action == "Rest":
                    FG_Rest(g)

                else:
                    # In all other cases we set girl trianing or rest for slaves:
                    if g.action != "slave":
                        g.previousaction = None
                        g.action = "Training"
                        girls.append(g)

                    else:
                        g.previousaction = None
                        g.action = "Rest"
                        girls.append(g)

            # Exploration Jobs:
            for i in self.exploring:
                i.next_day()

            # Create the event:
            evt = NDEvent()
            evt.red_flag = self.flag_red
            evt.green_flag = self.flag_green
            #evt.girlmod = stats
            evt.type = 'fg_report'
            evt.char = None
            self.loc = fg
            evt.img = self.img
            if isinstance(txt, (list, tuple)):
                try:
                    evt.txt = "".join(txt)
                except TypeError:
                    evt.txt = "".join(str(i) for i in txt)
            # evt.txt = "".join(txt)
            NextDayEvents.append(evt)

            self.fin.next_day()

            init -5 python:
                class GuardJob(Job):
                    def __init__(self):
                        """Creates reports for GuardJob.
                        """
                        super(GuardJob, self).__init__()
                        self.id = "Guarding"
                        self.type = "Combat"

                        self.event_type = "jobreport"

                        # Traits/Job-types associated with this job:
                        self.occupations = ["Warrior"] # General Strings likes SIW, Warrior, Server...
                        self.occupation_traits = [traits["Warrior"], traits["Mage"], traits["Knight"], traits["Shooter"]] # Corresponding traits...

                        # Relevant skills and stats:
                        self.base_skills = {"attack": 20, "defence": 20, "agility": 60, "magic": 20}
                        self.base_stats = {"security": 100}

                        self.desc = "Don't let them take your shit!"

                    def traits_and_effects_effectiveness_mod(self, worker, log):
                        """Affects worker's effectiveness during one turn. Should be added to effectiveness calculated by the function below.
                           Calculates only once per turn, in the very beginning.
                        """
                        effectiveness = 0
                         # effects always work
                        if worker.effects['Food Poisoning']['active']:
                            log.append("%s suffers from Food Poisoning, and is very far from her top shape." % worker.name)
                            effectiveness -= 50
                        elif worker.effects['Down with Cold']['active']:
                            log.append("%s is not feeling well due to colds..." % worker.name)
                            effectiveness -= 15
                        elif worker.effects['Drunk']['active']:
                            log.append("%s is drunk, which affects her coordination. Not the best thing when you need to guard something." % worker.name)
                            effectiveness -= 20
                        elif worker.effects['Revealing Clothes']['active']:
                            if dice(50):
                                log.append("Her revealing clothes attract unneeded attention, interfering with work.")
                                effectiveness -= 10
                            else:
                                log.append("Her revealing clothes help to pacify some aggressive customers.")
                                effectiveness += 10

                        if locked_dice(65): # traits don't always work, even with high amount of traits there are normal days when performance is not affected

                            traits = list(i.id for i in worker.traits if i in ["Abnormally Large Boobs",
                                          "Aggressive", "Coward", "Stupid", "Neat", "Psychic", "Adventurous",
                                          "Natural Leader", "Scars", "Artificial Body", "Sexy Air",
                                          "Courageous", "Manly", "Sadist", "Nerd", "Smart", "Peaceful"])

                            if "Lolita" in worker.traits and worker.height == "short":
                                traits.append("Lolita")
                            if traits:
                                trait = choice(traits)
                            else:
                                return effectiveness

                            if trait == "Abnormally Large Boobs":
                                log.append("Her massive tits get in the way and keep her off balance as %s tries to work security." % worker.name)
                                effectiveness -= 25
                            elif trait == "Aggressive":
                                if dice(50):
                                    log.append("%s keeps disturbing customers who aren't doing anything wrong. Maybe it's not the best job for her." % worker.name)
                                    effectiveness -= 35
                                else:
                                    log.append("Looking for a good fight, %s patrols the area, scaring away the rough customers." % worker.name)
                                    effectiveness += 50
                            elif trait == "Lolita":
                                log.append("%s is too small to be taken seriously. Some of the problematic customers just laugh at her." % worker.name)
                                effectiveness -= 50
                            elif trait == "Coward":
                                log.append("%s keeps asking for backup every single time an incident arises." % worker.name)
                                effectiveness -= 25
                            elif trait == "Stupid":
                                log.append("%s has trouble adapting to the constantly evolving world of crime prevention." % worker.name)
                                effectiveness -= 15
                            elif trait == "Smart":
                                log.append("%s keeps learning new ways to prevent violence before it happens." % worker.name)
                                effectiveness += 15
                            elif trait == "Neat":
                                log.append("%s refuses to dirty her hands on some of the uglier looking criminals." % worker.name)
                                effectiveness -= 15
                            elif trait == "Psychic":
                                log.append("%s knows when customers are going to start something, and prevents it easily." % worker.name)
                                effectiveness += 30
                            elif trait == "Adventurous":
                                log.append("Her experience fighting bandits as an adventurer makes working security relatively easier.")
                                effectiveness += 25
                            elif trait == "Natural Leader":
                                log.append("%s often manages to talk customers of starting an incident." % worker.name)
                                effectiveness += 50
                            elif trait == "Scars":
                                log.append("One look at her scars is enough to tell the violators that %s means business." % worker.name)
                                effectiveness += 20
                            elif trait == "Artificial Body":
                                log.append("%s makes no effort to hide the fact that she was a construct, intimidating would-be violators." % worker.name)
                                effectiveness += 25
                            elif trait == "Sexy Air":
                                log.append("People around %s back her up her just because of her sexiness." % worker.name)
                                effectiveness += 15
                            elif trait == "Courageous":
                                log.append("%s refuses to back down no matter the odds, making a great guard." % worker.name)
                                effectiveness += 25
                            elif trait == "Manly":
                                log.append("Considering %s is bigger than a number of the guys, she prevents a lot of trouble just by being there." % worker.name)
                                effectiveness += 35
                            elif trait == "Sadist":
                                log.append("%s gladly beats it out of any violators. Everyone deserves to be punished." % worker.name)
                                effectiveness += 15
                            elif trait == "Nerd":
                                log.append("%s feels like a super hero while protecting your workers." % worker.name)
                                effectiveness += 15
                            elif trait == "Peaceful":
                                log.append("%s has to deal with some very unruly patrons that give her a hard time." % worker.name)
                                effectiveness -= 35
                        return effectiveness

                    def get_events(self):
                        """
                        Get the guard events this girl will respond to.
                        """
                        log.append(choice(["%s worked as guard in %s! \n"%(worker.fullname, self.loc.name),
                                                "%s did guard duty in %s! \n"%(worker.fullname, self.loc.name)]))

                        log.append("\n")
                        self.img = "battle"

                        if worker.guard_relay['bar_event']['count']:
                            if worker.has_image("fighting"):
                                self.img = "fighting"

                            g_events = plural("event", worker.guard_relay["bar_event"]["count"])

                            log.append("She responded to %d brawl %s. "%(worker.guard_relay['bar_event']['count'], g_events))
                            log.append("That resulted in victory(ies): %d and loss(es): %d! "%(worker.guard_relay['bar_event']['won'], worker.guard_relay['bar_event']['lost']))
                            log.append("\n")

                            workermod = dict( (n, workermod.get(n, 0)+worker.guard_relay['bar_event']['stats'].get(n, 0)) for n in set(workermod)|set(worker.guard_relay['bar_event']['stats']) )

                        if worker.guard_relay['whore_event']['count']:
                            if worker.has_image("fighting"):
                                self.img = "fighting"

                            g_events = plural("attack", worker.guard_relay["whore_event"]["count"])

                            log.append("With %d victory(ies) and %d loss(es) she settled %d %s on your prostitutes. \n"%(worker.guard_relay['whore_event']['won'],
                                                                                                                              worker.guard_relay['whore_event']['lost'],
                                                                                                                              worker.guard_relay['whore_event']['count'],
                                                                                                                              g_events))

                            workermod = dict( (n, workermod.get(n, 0)+worker.guard_relay['whore_event']['stats'].get(n, 0)) for n in set(workermod)|set(worker.guard_relay['whore_event']['stats']) )
                            log.append("\n")

                    def post_job_activities(self):
                        """
                        Solve the post job events.
                        """

                        if worker.AP <= 0:
                            log.append(choice(["Nothing else happened during her shift.", "She didn't have the stamina for anything else today."]))
                        else:
                            gbu = self.loc.get_upgrade_mod("guards")
                            if gbu == 3:
                                guardlist = [girl for girl in hero.chars if girl.location == self.loc and girl.action == 'Guard' and girl.health > 60]
                                guards = len(guardlist)

                                if guards > 0:
                                    if guards >= 3:
                                        log.append(", ".join(girl.name for girl in guardlist[:guards-1]))
                                        log.append(" and %s "%guardlist[guards-1].nickname)
                                        log.append("spent the rest of the day dueling each other in Sparring Quarters. \n")

                                        while worker.AP > 0:
                                            workermod['attack'] = workermod.get('attack', 0) + choice([0, 0, 0, 0, 1, guards])
                                            workermod['defence'] = workermod.get('defence', 0) + choice([0, 0, 0, 0, 1, guards])
                                            workermod['magic'] = workermod.get('magic', 0) + choice([0, 0, 0, 0, 1, guards])
                                            workermod['joy'] = workermod.get('joy', 0) + choice([0, 1, 2, 3])
                                            workermod['vitality'] = workermod.get('vitality', 0) - randint(15, 20)
                                            worker.AP -=  1

                                        workermod['exp'] = workermod.get('exp', 0) + worker.AP * randint(8, 12) + 5 * (guards-1) # Moved to prevent insane exp increases at higher levels.

                                    elif guards == 2:
                                        log.append("%s and %s spent time dueling each other! \n"%(guardlist[0].name, guardlist[1].name))

                                        while worker.AP > 0:
                                            workermod['attack'] = workermod.get('attack', 0) + choice([0,0,0,0,1,guards])
                                            workermod['defence'] = workermod.get('defence', 0) + choice([0,0,0,0,1,guards])
                                            workermod['magic'] = workermod.get('magic', 0) + choice([0,0,0,0,1,guards])
                                            workermod['joy'] = workermod.get('joy', 0) + choice([0,1,2,3])
                                            workermod['vitality'] = workermod.get('vitality', 0) - randint(15, 20)
                                            worker.AP -=  1

                                        workermod['exp'] = workermod.get('exp', 0) + worker.AP * randint(8, 12) + 5

                                    elif guards == 1:
                                        log.append("%s had the whole Sparring Quarters to herself! \n"%(guardlist[0].name))

                                        while worker.AP > 0:
                                            workermod['attack'] = workermod.get('attack', 0) + choice([0,0,0,0,1,guards])
                                            workermod['defence'] = workermod.get('defence', 0) + choice([0,0,0,0,1,guards])
                                            workermod['magic'] = workermod.get('magic', 0) + choice([0,0,0,0,1,guards])
                                            workermod['joy'] = workermod.get('joy', 0) + choice([0,1,2,3])
                                            workermod['vitality'] = workermod.get('vitality', 0) - randint(15, 20)
                                            worker.AP -=  1

                                        workermod['exp'] = workermod.get('exp', 0) + worker.AP * randint(8, 12)

                            elif gbu == 2:
                                log.append("She spent remainder of her shift practicing in Training Quarters. \n")

                                while worker.AP > 0:
                                    workermod['attack'] = workermod.get('attack', 0) + choice([0,0,0,1])
                                    workermod['defence'] = workermod.get('defence', 0) + choice([0,0,0,1])
                                    workermod['magic'] = workermod.get('magic', 0) + choice([0,0,0,1])
                                    workermod['joy'] = workermod.get('joy', 0) + choice([0,1,1,2])
                                    workermod['vitality'] = workermod.get('vitality', 0) - randint(15, 20)
                                    worker.AP -= 1

                                workermod['exp'] = workermod.get('exp', 0) + worker.AP * randint(8, 12)

                            elif self.loc.upgrades['guards']['1']['active']:
                                if dice(50):
                                    log.append("She spent time relaxing in Guard Quarters. \n")
                                    workermod['vitality'] = workermod.get('vitality', 0) + randint(15, 20) * worker.AP
                                    worker.AP = 0

                                else:
                                    log.append("She did some rudimentary training in Guard Quarters. \n")
                                    workermod['attack'] = workermod.get('attack', 0) + choice([0,0,0,0,1])
                                    workermod['defence'] = workermod.get('defence', 0) + choice([0,0,0,0,1])
                                    workermod['magic'] = workermod.get('magic', 0) + choice([0,0,0,0,1])
                                    workermod['joy'] = workermod.get('joy', 0) + choice([0,1,1,1])
                                    workermod['exp'] = workermod.get('exp', 0) +  randint(15, 25)
                                    workermod['vitality'] = workermod.get('vitality', 0) - randint(15, 20)
                                    worker.AP = 0

                            else:
                                if dice(50):
                                    log.append("She spent time relaxing. \n")

                                    #display rest only if they did not fight
                                    if not worker.guard_relay['bar_event']['count'] and not worker.guard_relay['whore_event']['count']:
                                        self.img = "rest"

                                    workermod['vitality'] = workermod.get('vitality', 0) + randint(7, 12) * worker.AP
                                    worker.AP = 0

                                else:
                                    log.append("She did some rudimentary training. \n")
                                    workermod['attack'] = workermod.get('attack', 0) + choice([0,0,0,0,0,1])
                                    workermod['defence'] = workermod.get('defence', 0) + choice([0,0,0,0,0,1])
                                    workermod['magic'] = workermod.get('magic', 0) + choice([0,0,0,0,0,1])
                                    workermod['joy'] = workermod.get('joy', 0) + choice([0,1])
                                    workermod['exp'] = workermod.get('exp', 0) +  randint(8, 15)
                                    workermod['vitality'] = workermod.get('vitality', 0) - randint(15, 20)
                                    worker.AP = 0

GuardJob:
def request_action(self, building=None, start_job=True, priority=True, any=False, action=None):
    """This checks if there are idle workers willing/ready to do an action in the building.

    This will also start the job by default.
    Priority will call just the real warriors.
    Any will also add everyone else who might be willing to act.

    TODO: Once done, see if this can be generalized like the previous two upgrade types!
    """
    if not action:
        raise Exception("Action Must Be provided to .request_action method!")

    if not building:
        building = self.instance

    job = simple_jobs["Guarding"]
    # dirt = building.get_dirt()
    workers = self.get_workers(job, amount=10, priority=priority, any=any)
    process = None
    if not workers:
        return False, process # No workers available
    else:
        # Might require optimization so we don't send all the warriors to once.
        # Update worker lists:
        if start_job:
            if action == "patrol":
                self.active_workers = workers[:]
                self.instance.available_workers = list(i for i in self.instance.available_workers if i not in workers)
                process = self.env.process(self.patrol(workers, building))
        return True, process

def patrol(self, workers, building):
    """Patrolling the building...
    IMPORTANT SIMPY SETUP EXPAMPLE!
    """
    workers_original = workers[:]
    power_flag_name = "jobs_guard_power"
    for w in workers:
        # Set their defence capabilities as temp flag:
        value = round((1 + w.defence * 0.025 + w.agility * 0.3), 2) # Is defence sound here? We don't have guarding still...
        w.set_flag(power_flag_name, value)

    wlen = len(workers)
    if self.env:
        t = self.env.now
        temp = "{}: {} guards are going to patrol halls of {}!".format(self.env.now, set_font_color(wlen, "red"), building.name)
        self.log(temp)

    counter = 0 # counter for du, lets say that a single patrol run takes 20 du...

    while (workers and counter <= 100) and self.env.now < 99:
        # Job Points:
        try:
            flag_name = "_jobs_guard_points"
            for w in workers[:]:
                # if not w.flag(flag_name) or w.flag(flag_name) <= 0:
                #     self.convert_AP(w, workers, flag_name)

                # Cleaning itself:
                if w in workers:
                    w.mod_flag("_jobs_guard_points", 1) # 1 point per 1 dp? Is this reasonable...? Prolly, yeah.
                    w.mod_flag("job_guard_points_spent", 1) # So we know what to do during the job event buildup and stats application.

            if config.debug and self.env and not counter % 4:
                wlen = len(workers)
                # We run this once per 2 du and only for debug purposes.
                temp = "{}: Debug: ".format(self.env.now)
                temp = temp + " {} Guards are currently patrolling {}!".format(set_font_color(wlen, "red"), building.name)
                temp = temp + set_font_color(" DU spent: {}!".format(counter), "blue")
                self.log(temp)

            # We may be running this outside of SimPy... not really? not in this scenario anyway...
            if self.env:
                yield self.env.timeout(1)
            counter = counter + 1

        except simpy.Interrupt as reason:
            temp = "{}: Debug: ".format(self.env.now)
            temp = temp + " {} Guards responding to an event ({}), patrol is halted in {}".format(set_font_color(wlen, "red"), reason.cause, building.name)
            temp = temp + set_font_color("!!!!".format(counter), "crimson")
            self.log(temp)

            yield self.env.timeout(5)

            temp = "{}: Debug: ".format(self.env.now)
            temp = temp + " {} Guards finished their response to the event, back to patrolling {}".format(set_font_color(wlen, "red"), building.name)
            temp = temp + set_font_color("....".format(counter), "crimson")
            self.log(temp)

    temp = "{}: Patrol of {} is now finished! Guards are falling back to their quarters!".format(self.env.now, building.name)
    temp = set_font_color(temp, "red")
    self.log(temp)

    # Once the loop is broken:
    # Restore the lists:
    self.active_workers = list()
    for w in workers:
        self.instance.available_workers.append(w)

    # Build the report:
    self.write_nd_report(workers_original, workers)
    # simple_jobs["Guarding"](workers_original, workers, building, action="patrol")
