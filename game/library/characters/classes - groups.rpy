# classes and methods for groups of Characters:
init -8 python:
    class listDelegator(_object):
        """ only provides obvious solutions, everything else needs a remedy """

        def __init__(self, l, remedy=None):
            self.lst = l
            self._remedy = {} if remedy is None else remedy

        def _defer(self, arr, at):
            # get unique types:
            totype = []
            for var in arr:
                if isinstance(var, basestring):
                    totype.append("<str>")
                elif isinstance(var, (list, tuple, renpy.python.RevertableList)):
                    totype.append("<list("+str(len(var))+")>")
                elif isinstance(var, (dict, renpy.python.RevertableDict)):
                    totype.append("<dict("+",".join(sorted(var.keys()))+")>")
                elif isinstance(var, (Char, rChar)):
                    totype.append("<char>")
                else:
                    totype.append(str(type(var)))
            totype = list(set(totype))

            # multiple types or not?
            if len(totype) == 1:
                if totype[0][0:5] == "<list":
                    return [self._defer(arr=[x[i] for x in arr], at=at+"[]") for i in range(len(arr[0]))]
                if totype[0][0:5] == "<dict":
                    return {k: self._defer(arr=[x[k] for x in arr], at=at+"{}") for k in arr[0]}
                if all(cmp(arr[0], r) == 0 for r in arr[1:]):
                    return arr[0]

            return self._unlist(arr=arr, at=at)

        def __getattr__(self, item):
            """ an undefined attribute was requested from the group """
            # required for pickle
            if item.startswith('__') and item.endswith('__'):
                return super(listDelegator, self).__getattr__(item)

            if callable(getattr(self.lst[0], item)):

                def wrapper(*args, **kwargs):
                    return self._defer(arr=[getattr(c, item)(*args, **kwargs) for c in self.lst], at=item+"()")

                attr = wrapper
            else:
                attr = self._defer(arr=[getattr(c, item) for c in self.lst], at=item)

            return attr

        def __setattr__(self, k, v):
             if k not in ('lst', '_remedy'):
                 for c in self.lst:
                     setattr(c, k, v)
             else:
                 super(listDelegator, self).__setattr__(k, v)

        def _type(self, var):
            """ generalizations """
            if isinstance(var, basestring): return "<str>"
            if isinstance(var, (list, renpy.python.RevertableList)): return '<list>'
            if isinstance(var, (dict, renpy.python.RevertableDict)): return '<dict>'
            return str(type(var))

        def _unlist(self, arr, at=""):
            """ try to get a single value for a list """

            if all(self._type(r) == self._type(arr[0]) for r in arr[1:]):

                if all(cmp(arr[0], r) == 0 for r in arr[1:]):
                    return arr[0]

            if 'flatten' in self._remedy and at in self._remedy['flatten']:
                return list(set([item for sublist in arr for item in sublist]))

            """ In case of an error here: define a remedy for the unlisting"""
            remedy = self._remedy[at]
            return remedy(arr) if callable(remedy) else remedy

        def most_abundant_not_False(self, arr):
            return [sorted(((arr.count(e), e) for e in set(arr) if e is not False), reverse=True)[0][1]]

        def order_abundance(self, arr):
            return sorted(((arr.count(e), e) for e in set(arr)), reverse=True)


    class PytGInv(listDelegator):

        def __init__(self, inv):
            remedy={
                "filters[]": self.most_abundant_not_False,
                "page_content[]": self.most_abundant_not_False,
                "slot_filter[]": self.most_abundant_not_False,
                "flatten": ["filters", "page_content", "slot_filter"]
            }
            super(PytGInv, self).__init__(inv, remedy=remedy)

        def __getitem__(self, item):
            if isinstance(item, (list, renpy.python.RevertableList)):
                return 0
            return min([x[item] for x in self.lst])

        @property
        def max_page(self):
            return min([x.max_page for x in self.lst])

        def remove(self, item, amount=1):
            """ see Inventory.remove(): False means not enough items """
            return all([x.remove(item,amount) for x in self.lst])

        def append(self, item, amount=1):
            all([x.append(item,amount) for x in self.lst])

    class PytGroup(listDelegator):

        def __init__(self, characters):
            remedy={
                "eqslots{}": self.most_abundant_not_False,
                "status": "Various",
                "autobuy": self.order_abundance,
                "autoequip": self.order_abundance,
                "autocontrol{}": self.order_abundance,
                "flatten": ["traits", "attack_skills", "magic_skills"]
            }
            super(PytGroup, self).__init__(characters, remedy=remedy)

        @property
        def name(self): return "A group of "+str(len(self.selected))
        @property
        def img(self): return "content/gfx/interface/images/group.png"
        @property
        def portrait(self): return "content/gfx/interface/images/group_portrait.png"
        @property
        def nickname(self): return "group"

        @property
        def inventory(self): return PytGInv([c.inventory for c in self.selected])

        @property
        def shuffled(self):
            return random.sample(self.selected, len(self.selected))

        @property
        def selected(self):
            return self.lst

        @property
        def given_items(self):
            return {k:min([c.given_items[k] for c in self.lst]) for k in self.lst[0].given_items.keys()}
        @property
        def wagemod(self):
            return round(float(sum([c.wagemod for c in self.selected])) / max(len(self.selected), 1), 1)
        @wagemod.setter
        def wagemod(self, v):
            for c in self.selected:
                c.wagemod = v

        def show(self, what, resize=(None, None), cache=True):
            if what == "portrait":
                what = self.portrait
            elif what != self.img:
                what = self.img

            return ProportionalScale(what, resize[0], resize[1])

        def __len__(self):
            return len(self.selected)



