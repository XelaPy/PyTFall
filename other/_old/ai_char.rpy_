def auto_discard(self, slots=None):
    """
    This function is to prevent that chars accumulate too many items in inventory. In particular
    multiple copies. Given items will not be discarded. TODO: looks like it's not used anymore thus not needed?
    """

    weighted = {}
    slotmax = {}
    slotcount = {}

    for k in slots if slots else self.eqslots:
        if k == "ring1" or k == "ring2":
            continue
        weighted[k] = []
        slotmax[k] = 10
        slotcount[k] = 0

    # maybe these could be a consequence of a selected class?
    target_stats = set()
    target_skills = set()
    exclude_on_skills = set()
    exclude_on_stats = set()

    most_weights = self.stats.eval_inventory(self.inventory, weighted, target_stats, target_skills,
                                             exclude_on_skills, exclude_on_stats,
                                             chance_func=self.keep_chance, min_value=-1000000000,
                                             upto_skill_limit=True)
    returns = []
    for slot, picks in weighted.iteritems():

        if not picks:
            continue

        # prefilter items
        selected = []
        last_resort = []

        # create averages for items, and count items per slot.
        for r in picks:
            # devlog.warn("[%s/%s]: %s" % (r[1].slot, r[1].id, str(r[0])))

            som = sum(r[0])

            # impute with weights of 50 for items that have less weights
            som += 50 * (len(r[0]) - most_weights[slot])

            r[0] = som/most_weights[slot]
            selected.append(r)
            slotcount[slot] += self.inventory[r[1]]


        for weight, item in sorted(selected, key=lambda x: x[0], reverse=False):

            while slotcount[slot] > slotmax[slot] and item in self.inventory.items:

                if item.id in self.given_items and self.inventory[item] <= self.given_items[item.id]:
                    break

                if self.inventory[item] == 1: # first only remove dups
                    last_resort.append(item)
                    break

                self.inventory.remove(item)
                returns.append(item.id)
                slotcount[slot] -= 1

            if slotcount[slot] <= slotmax[slot]:
                break
        else:
            # if we still have items above treshold also remove some of the last items (non dups)
            for item in last_resort:
                self.inventory.remove(item)
                returns.append(item.id)
                slotcount[slot] -= 1

                if slotcount[slot] <= slotmax[slot]:
                    break

    return returns
