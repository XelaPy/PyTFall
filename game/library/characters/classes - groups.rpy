# classes and methods for groups of Characters:
init -8 python:
    class Delegator(_object):
        def __init__(self, l, remedy=None):
            self.lst = l
            self._remedy = {} if remedy is None else remedy

        def _defer(self, arr, at):
            # get unique types:
            totype = []
            for var in arr:
                if isinstance(var, basestring):
                    totype.append("<str>")
                elif isinstance(var, (list, tuple)):
                    totype.append("<list("+str(len(var))+")>")
                elif isinstance(var, dict):
                    totype.append("<dict("+",".join(sorted(var.keys()))+")>")
                elif isinstance(var, Char):
                    totype.append("<char>")
                else:
                    totype.append(str(type(var)))
            totype = list(set(totype))

            remedy = self._remedy
            # multiple types or not?
            if len(totype) == 1:
                if totype[0][0:5] == "<list":
                    return deDist(arr, remedy=remedy, at=at+"[]")
                if totype[0][0:5] == "<dict":
                    return deDist(arr, remedy=remedy, at=at+"{}")
                if all(cmp(arr[0], r) == 0 for r in arr[1:]):
                    return arr[0]

            # else try to get a single value for a list

            if 'flatten' in self._remedy and at in self._remedy['flatten']:
                return list(frozenset([item for sublist in arr for item in sublist]))

            # In case of an error here: define a remedy for the unlisting
            return remedy[at](arr) if callable(remedy[at]) else remedy[at]

    class deDist(Delegator):

        def __init__(self, l, at, remedy=None, *args, **kwargs):
            super(deDist, self).__init__(l, remedy=remedy)
            self._at = at

        def __getitem__(self, k):
            return self._defer(arr=[d[k] for d in self.lst], at=self._at)

        def __setitem__(self, k, v):
            for d in self.lst:
                d[k] = v
        def __delitem__(self, k):
            for d in self.lst:
                del(d[k])
        def __iter__(self):
            if isinstance(self.lst[0], dict):
                return iter({k: self._defer(arr=[x[k] for x in self.lst], at=self._at) for k in self.lst[0]})

            return iter(self._defer(arr=[x[i] for x in self.lst], at=self._at) for i in range(len(self.lst[0])))

        def __len__(self): return len(self.lst[0])


    class deAttr(Delegator):
        """ only provides obvious solutions, everything else needs a remedy """

        def __init__(self, l, at=None, remedy=None):
            self._attrs = ['lst', '_remedy', '_at']
            super(deAttr, self).__init__(l, remedy=remedy)
            self._remedy = {} if remedy is None else remedy
            self._at = at if at is not None else ""

        def __setattr__(self, k, v):
             if k != '_attrs' and k not in self._attrs:
                 for c in self.lst:
                     setattr(c, k, v)
             else:
                 super(deAttr, self).__setattr__(k, v)

        def __getattr__(self, item):
            """ an undefined attribute was requested from the group """
            # required for pickle
            if item.startswith('__') and item.endswith('__'):
                return super(deAttr, self).__getattr__(item)

            if callable(getattr(self.lst[0], item)):

                def wrapper(*args, **kwargs):
                    return self._defer(arr=[getattr(c, item)(*args, **kwargs) for c in self.lst], at=self._at+item+"()")

                return wrapper

            return self._defer(arr=[getattr(c, item) for c in self.lst], at=self._at+item)


    class PytGInv(deAttr):

        def __init__(self, inv):
            super(PytGInv, self).__init__(inv)
            self._attrs.append('slot_filter')
            self.slot_filter = False

        def __getitem__(self, item):
            if isinstance(item, list):
                return 0
            return min([x[item] for x in self.lst])

        @property
        def filters(self):
            return list(frozenset([item for sublist in self.lst for item in sublist.filters]))

        @property
        def page_content(self):
            return list(frozenset([item for sublist in self.lst for item in sublist.page_content]))

        @property
        def max_page(self):
            return min([x.max_page for x in self.lst])

        def remove(self, item, amount=1):
            """ see Inventory.remove(): False means not enough items """
            return all([x.remove(item,amount) for x in self.lst])

        def apply_filter(self, filter):
            if filter in ('next', 'prev'):
                for x in self.lst:
                    x.apply_filter(filter)
            else:
                self.slot_filter = filter
                for x in self.lst:
                    if filter in x.filters:
                        x.apply_filter(filter)
                    else:
                        x.filtered_items = []

        def append(self, item, amount=1):
            all([x.append(item,amount) for x in self.lst])


    class PytGroup(deAttr):

        def __init__(self, chars):
            remedy={
                "eqslots{}": self.most_abundant_not_False,
                "status": "various",
                "autobuy": [], "front_row": [], "autoequip": [], "autocontrol{}": [],
                "flatten": ["traits", "attack_skills", "magic_skills"]
            }
            super(PytGroup, self).__init__(chars, remedy=remedy)
            self._attrs.extend(['inventory', 'name', 'img', 'portrait', 'nickname', 'effects', 'stats'])

            self.inventory = PytGInv([c.inventory for c in self.selected])
            self.name = "A group of "+str(len(self.selected));
            self.img = "content/gfx/interface/images/group.png"
            self.portrait = "content/gfx/interface/images/group_portrait.png"
            self.nickname = "group"
            self.effects = {}
            stat_remedy = {'_get_stat()': self._average, '_raw_skill()': self._average}
            self.stats = deAttr([c.stats for c in self.selected], remedy=stat_remedy)

        def __new__(cls, chars):
            return chars[0] if len(chars) == 1 else super(Delegator, cls).__new__(cls, chars)

        # for pickle & __new__
        def __getnewargs__(self): return (PytGroup.__repr__(self),)
        def __repr__(self): return '<PytGroup %r>' % self.lst

        @property
        def shuffled(self):
            return random.sample(self.selected, len(self.selected))

        @property
        def selected(self):
            return self.lst

        @property
        def given_items(self):
            return {k:min([c.given_items[k] for c in self.lst]) for k in self.lst[0].given_items}
        @property
        def wagemod(self):
            return self._average([c.wagemod for c in self.selected])
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

        # remedy functions below
        def most_abundant_not_False(self, arr):
            return [sorted(((arr.count(e), e) for e in set(arr) if e is not False), reverse=True)[0][1]]

        def _average(self, arr):
            return round(float(sum(arr)) / max(len(arr), 1), 1)

