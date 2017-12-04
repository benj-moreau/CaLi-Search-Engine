from itertools import permutations


def generate(Terms):
    result = []
    for p in partition(Terms):
        if (len(p) < 4):
            while (len(p) < 3):
                p.append([])
            for perm in permutations(p):
                if perm not in result:
                    result.append(perm)
    return result


def partition(collection):
    if len(collection) == 1:
        yield [collection]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[first] + subset] + smaller[n+1:]
        # put `first` in its own subset
        yield [[first]] + smaller
