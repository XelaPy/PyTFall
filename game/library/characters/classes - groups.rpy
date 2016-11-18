# classes and methods for groups of Characters:
init -8 python:
    class listDelegator(_object):
        """ only provides obvious solutions, everything else needs a remedy """

        def __init__(self, l, flatten=None, remedy=None):

            self.lst = l
            self._flatten = flatten or []
            self.remedy = remedy if remedy is not None else {}

        def __getitem__(self, item):
            return self.unlist([c[item] for c in self.lst], at="["+self._type(item)+"]")

        def __getattr__(self, item):
            """ an undefined attribute was requested from the group """
            # required for pickle
            if item.startswith('__') and item.endswith('__'):
                return super(listDelegator, self).__getattr__(item)

            if callable(getattr(self.lst[0], item)):

                def wrapper(*args, **kwargs):
                    return self.unlist([getattr(c, item)(*args, **kwargs) for c in self.lst], at=item+"()")

                return wrapper

            return self.unlist([getattr(c, item) for c in self.lst], at=item)

        def __repr__(self):
            return repr(self)

        def _type(self, var):
            """ generalizations """
            if isinstance(var, basestring): return "<str>"
            if isinstance(var, (list, renpy.python.RevertableList)): return '<list>'
            if isinstance(var, (dict, renpy.python.RevertableDict)): return '<dict>'
            return str(type(var))

        def unlist(self, lst, at="", remedy=None):
            """ try to get a single value for a list """
            if not isinstance(lst, list):
                raise Exception("expected list "+at+"")

            if len(lst) == 0:
                return False

            if len(lst) == 1:
                return lst[0]

            tp = self._type(lst[0])

            if all(self._type(r) == tp for r in lst[1:]):
                if all(cmp(lst[0], r) == 0 for r in lst[1:]):
                    return lst[0]
            else:
                tp = '*'

            if at in self._flatten:
                return list(set([item for sublist in lst for item in sublist]))

            if remedy is None:
                remedy = self.remedy

            if isinstance(remedy, dict):
                remedy = remedy[at+":"+tp]

            """ In case of an error here: define a remedy for the unlisting"""
            return remedy(lst) if callable(remedy) else remedy


    class PytGInv(listDelegator):

        def __init__(self, inv):
            super(PytGInv, self).__init__(inv, flatten=['filters', 'page_content', 'slot_filter'])

        def __getitem__(self, item):
            return min([x[item] for x in self.lst])

        @property
        def max_page(self):
            return min([x.max_page for x in self.lst])

        def remove(self, item, amount=1):
            """ see Inventory.remove(): False means not enough items """
            return all([x.remove(item,amount) for x in self.lst])


    class PytGroup(listDelegator):

        def __init__(self, characters):

            super(PytGroup, self).__init__(characters, flatten=['traits', 'attack_skills', 'magic_skills'])

            self.status = listDelegator([c.status for c in self.selected], remedy="Various")

            # determines what to show as a count for items, if not equal
            self.inventory = PytGInv([c.inventory for c in self.selected])

            self.eqslots = listDelegator([c.eqslots for c in self.selected], remedy=False)

            self.img = "content/gfx/interface/images/group.png"
            self.portrait = "content/gfx/interface/images/group_portrait.png"
            self.entire_group_len = len(characters)

            self.name = "A group of "+str(self.entire_group_len)
            self.nickname = "group"

        @property
        def selected(self):
            return self.lst

        def equipment_access(self, item=None, silent=False):

            for c in self.selected:
                if not c.equipment_access(item, True):
                    if not silent:
                        c = choice(self.selected)
                        c.say(choice(["We refuse.", "Some of us disagree."]))
                    return False
            return True

        def show(self, what, resize=(None, None), cache=True):
            if what == "portrait":
                what = self.portrait
            elif what != self.img:
                what = self.img

            return ProportionalScale(what, resize[0], resize[1])

        def __len__(self):
            return self.entire_group_len



