from licenses.ConsolidatedLicense import ConsolidatedLicense
from itertools import permutations


def generate_licenses(Terms):
    permutations = _generate(Terms)
    powerset = []
    for ind, permut in enumerate(permutations):
        label = "L{}".format(ind)
        powerset.append(ConsolidatedLicense(frozenset([label]), set(permut[0]), set(permut[1]), set(permut[2])))
    return powerset


def _generate(Terms):
    result = []
    for p in _partition(Terms):
        if (len(p) < 4):
            while (len(p) < 3):
                p.append([])
            for ind, permut in enumerate(permutations(p)):
                if permut not in result:
                    result.append(permut)
    return result


def _partition(collection):
    if len(collection) == 1:
        yield [collection]
        return

    first = collection[0]
    for smaller in _partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[first] + subset] + smaller[n+1:]
        # put `first` in its own subset
        yield [[first]] + smaller
