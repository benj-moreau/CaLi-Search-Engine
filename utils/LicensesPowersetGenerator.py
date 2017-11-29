import licenses.ConsolidatedLicenses as ConsolidatedLicenses

import itertools


def generate(Terms):
    powerset = []
    for i in range(1, len(Terms)+1):
        for a in itertools.combinations(Terms, i):
            print a
    return powerset
