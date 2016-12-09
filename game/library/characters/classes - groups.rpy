# classes and methods for groups of Characters:
init -8 python:
    class Delegator(_object):
        def __init__(self, l, at, remedy=None, *args, **kwargs):
            self.lst = l
            self._at = at
            self._remedy = {} if remedy is None else remedy

        @property
        def _first(self):
            return next(iter(self.lst))

        def _defer(self, arr, at=""):
            import inspect
            # get unique types:
            at = self._at + at
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
                first = next(iter(arr))
                if all(cmp(first, r) == 0 for r in arr):
                    return first

            # else try to get a single value for a list

            if 'flatten' in self._remedy and at in self._remedy['flatten']:
                return list(frozenset([item for sublist in arr for item in sublist]))

            if not at in remedy:
                renpy.error(at+"\n"+str(totype)+"\n"+str(arr))

            if inspect.isclass(remedy[at]) and issubclass(remedy[at], Delegator):
                return remedy[at](l=arr, at=at, remedy=remedy)

            # In case of an error here: define a remedy for the unlisting
            return remedy[at](arr) if callable(remedy[at]) else remedy[at]

    class deDist(Delegator):

        def __init__(self, *args, **kwargs):
            super(deDist, self).__init__(*args, **kwargs)

        def __getitem__(self, k):
            return self._defer(arr=[d[k] for d in self.lst])

        def __setitem__(self, k, v):
            for d in self.lst:
                d[k] = v
        def __delitem__(self, k):
            for d in self.lst:
                del(d[k])
        def __iter__(self):
            if isinstance(self._first, dict):
                return iter({k: self._defer(arr=[x[k] for x in self.lst]) for k in self._first})

            return iter(self._defer(arr=[x[i] for x in self.lst]) for i in range(len(self._first)))

        def __len__(self): return len(self._first)


    class deAttr(Delegator):
        """ only provides obvious solutions, everything else needs a remedy """

        def __init__(self, *args, **kwargs):
            # attributes of this class are added here to prevent infinite __setattr__ recursion
            self._attrs = ['lst', '_remedy', '_at']
            super(deAttr, self).__init__(*args, **kwargs)

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

            if callable(getattr(self._first, item)):

                def wrapper(*args, **kwargs):
                    return self._defer(arr=[getattr(c, item)(*args, **kwargs) for c in self.lst], at="."+item+"()")

                return wrapper

            return self._defer(arr=[getattr(c, item) for c in self.lst], at="."+item)


    class PytGInv(deAttr):

        def __init__(self, inv):
            super(PytGInv, self).__init__(l=inv, at="inventory")
            self._attrs.extend(('slot_filter', 'page'))
            self.slot_filter = False

        def __getitem__(self, item):
            if isinstance(item, list):
                return 0
            return min([x[item] for x in self.lst])

        @property
        def filters(self):
            return list(frozenset([item for sublist in self.lst for item in sublist.filters]))

        @property
        def filtered_items(self):
            return set([item for sublist in self.lst for item in sublist.filtered_items])

        @property
        def page_content(self):
            ps = self.page_size
            start = self.page*ps
            return list(self.filtered_items)[start : (start+ps)]
            #return list(frozenset([item for sublist in self.lst for item in sublist.page_content]))

        @property
        def max_page(self):
            ps = self.page_size
            l = len(self.filtered_items)
            return int(l / ps) + (l % ps > 0)

        def next(self):
            if self.page + 1 < self.max_page:
                self.page += 1
        def prev(self): self.page = max(self.page - 1, 0)
        def first(self): self.page = 0
        def last(self): self.page = max(self.max_page - 1, 0)

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
            self.page = 0

        def append(self, item, amount=1):
            all([x.append(item, amount) for x in self.lst])


    class PytGroup(deAttr):

        def __init__(self, chars):
            remedy={
                ".eqslots{}": self._ordered_on_abundance,
                ".status": ".various", ".action": "various", ".location": "various",
                ".autobuy": [], ".front_row": [], ".autoequip": [], ".autocontrol{}": [],
                "flatten": [".traits", ".attack_skills", ".magic_skills"]
            }
            super(PytGroup, self).__init__(l=chars, remedy=remedy, at="")
            self._attrs.extend(['_inventory', 'img', 'portrait', 'nickname', 'effects', '_stats', 'unselected'])

            self._inventory = PytGInv([c.inventory for c in self.lst])
            self.img = "content/gfx/interface/images/group.png"
            self.portrait = "content/gfx/interface/images/group_portrait.png"
            self.nickname = "group"
            self.effects = {}
            stat_remedy = {'.stats._get_stat()': self._average, '.stats._raw_skill()': self._average}
            self._stats = deAttr(l=[c.stats for c in self.lst], remedy=stat_remedy,at=".stats")
            self.unselected = set()

        def __new__(cls, chars):
            return next(iter(chars)) if len(chars) == 1 else super(Delegator, cls).__new__(cls, chars)

        # for pickle & __new__
        def __getnewargs__(self): return (PytGroup.__repr__(self),)
        def __repr__(self): return '<PytGroup %r>' % self.lst

        def __len__(self): return len(self.lst)

        @property
        def name(self): return "A group of "+str(len(self));

        @property
        def all(self): return sorted(list(self.lst) + list(self.unselected));

        @property
        def shuffled(self): return random.sample(self.lst, len(self))

        @property
        def inventory(self):
            self._inventory.lst = [c.inventory for c in self.lst]
            return self._inventory

        @property
        def stats(self):
            self._stats.lst = [c.stats for c in self.lst]
            return self._stats

        @property
        def given_items(self):
            return {k:min([c.given_items[k] for c in self.lst]) for k in self._first.given_items}
        @property
        def wagemod(self): return self._average([c.wagemod for c in self.lst])
        @wagemod.setter
        def wagemod(self, v):
            for c in self.lst:
                c.wagemod = v

        def show(self, what, resize=(None, None), cache=True):
            if what == "portrait":
                what = self.portrait
            elif what != self.img:
                what = self.img

            return ProportionalScale(what, resize[0], resize[1])

        # remedy functions below
        def _ordered_on_abundance(self, arr):
            return [x[1] for x in sorted(((arr.count(e) if e else -1, e) for e in set(arr)), reverse=True)]

        def _average(self, arr):
            return round(float(sum(arr)) / max(len(arr), 1), 1)

