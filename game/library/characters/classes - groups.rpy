# classes and methods for groups of Characters:
init -9 python:

    class listDelegator(_object):

        def __init__(self, l, strategy=None):
            self.selection = l
            self._strategy = strategy

        @property
        def selected(self):

            if not isinstance(self.selection, dict):
                return self.selection

            return [c for c in self.selection.values() if c is not None]

        def __getitem__(self, item):

            result = [c[item] for c in self.selected if item in c]

            if len(result) == 1 or not any(cmp(result[0], r) for r in result):
                return result[0]

            if any(type(result[0]) != type(r) for r in result):
                if self._strategy is not None:
                    return self._strategy(result) if callable(self._strategy) else self._strategy
                if not all(isinstance(r, basestring) for r in result):
                    raise Exception("Not all equal types, strategy required for "+name+":\n"+repr(result))

            if isinstance(result[0], type(self.selected[0])):
                result = listDelegator(result)

            devlog.warn("One item ("+str(item)+") randomly picked")
            return choice(result)

        def __getattr__(self, item):
            """ an undefined attribute was requested from characters in the group """
            # required for pickle
            if item.startswith('__') and item.endswith('__'):
                return super(listDelegator, self).__getattr__(item)

            #if len(self.selected) == 0:
            #    raise Exception("FIXME: disallow unselecting all characters")

            if callable(getattr(self.selected[0], item)):
                return self._toDelegator(item, self.selected)

            return self._delistified([getattr(c, item) for c in self.selected], item)

        def __repr__(self):
            return repr(self.selected)

        def _toDelegator(self, func, key):
            """ delegate call to individual characters and tries to sanitise return value """

            devlog.warn("Called character function from group:"+repr(func))

            def wrapper(*args, **kwargs):
                return self._delistified([getattr(c, func)(*args, **kwargs) for c in key], func)

            return wrapper

        def _delistified(self, result, name):
            """
            Called after 'name' (whether function or attribute) was requested from individual
            characters in the group. Looks at the type of the first and tries to come up with
            a sensible value to return. for anything non-standard profide a stratigy on init.
            """
            if not isinstance(result, list) or len(result) == 0:
                return None

            if len(result) == 1 or all(cmp(result[0], r) == 0 for r in result):
                return result[0]

            if any(type(result[0]) != type(r) for r in result):
                if self._strategy:
                    return self._strategy(result)
                if not all(isinstance(r, basestring) for r in result):
                    raise Exception("Not all equal types, strategy required for "+name+":\n"+repr(result))

            if result[0] is None:
                return self._delistified([r for r in result if r is not None], name)

            if isinstance(result[0], bool):
                return any(result)

            if isinstance(result[0], (int, float)):
                return sum(result) / len(result)

            if isinstance(result[0], basestring):
                result = [x+"("+str(result.count(x))+")" for x in set(result)]

                # XXX 3 is just random
                return "multiple" if len(result) > 3 else ", ".join(result)

            return listDelegator(result)


    class PytGroup(listDelegator):

        def __init__(self, characters):

            # The selection provided may have characters as None to be excluded
            selection = { c.name: c for c in characters if c is not None}

            super(PytGroup, self).__init__(selection)

            self.img = "content/gfx/interface/images/group.png"
            self.portrait = "content/gfx/interface/images/group_portrait.png"

            self.name = "A group of "+str(len(self.selection))
            self.nickname = "group"

        @property
        def chars(self):
            return self.selection.values()

        @property
        def eqslots(self):
            #TODO: display occupied inventory symbol here?
            return listDelegator([getattr(c, "eqslots") for c in self.selected], strategy=False)

        def show(self, what, resize=(None, None), cache=True):
            if what == "portrait":
                what = self.portrait
            elif what != self.img:
                what = self.img

            return ProportionalScale(what, resize[0], resize[1])

        def get_max(self, key):
            return max(c.get_max(key) for c in self.selected)

        def anyone_left(self):
            return len(self.selected)

