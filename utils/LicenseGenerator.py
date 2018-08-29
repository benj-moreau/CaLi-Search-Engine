import random
import itertools
from operator import methodcaller
from numpy.random import choice

import utils.ODRL as ODRL
from utils.TimerDecorator import fn_timer
from objectmodels.License import License

# Weights are calculated from http://purl.org/NET/rdflicense (probability to find an ation in a random license)
ODRL_WEIGHTS = [0.15, 0.29, 0.14, 0.09, 0.15, 0.09, 0.09]

SET_SIZE_WEIGHTS = [0.05, 0.1, 0.2, 0.3, 0.2, 0.1, 0.05]

NB_ACTIONS_LATTICE = 7


# Generate a set of licenses using ODRL vocabulary.
# structure: linear_order/no_order/partial_order
# order: asc/desc/rand
@fn_timer
def generate(structure='linear_order', order='asc', limit=144):
    licenses = []
    # structure
    if structure == 'linear_order':
        _linear_order(licenses, limit)
    elif structure == 'no_order':
        _no_order(licenses, limit)
    elif structure == 'lattice':
        _lattice(licenses, NB_ACTIONS_LATTICE)
    else:
        _partial_order(licenses, limit)
    # order
    if order == 'desc':
        licenses.reverse()
    elif order == 'rand':
        random.shuffle(licenses)
    return licenses


def _linear_order(licenses, limit=144):
    # More than 144 is not possible here
    if limit > 144:
        limit = 144
    label = 0
    obligations = []
    prohibitions = []
    licenses.append(License())
    licenses[-1].set_labels([str(label)])
    # obligations
    for action in ODRL.ACTIONS:
        if len(licenses) < limit:
            label += 1
            obligations.append(action)
            licenses.append(License())
            licenses[-1].set_labels([str(label)])
            licenses[-1].set_obligations(frozenset(obligations))
    # prohibitions
    for action in ODRL.ACTIONS:
        if len(licenses) < limit:
            label += 1
            prohibitions.append(action)
            licenses.append(License())
            licenses[-1].set_labels([str(label)])
            licenses[-1].set_obligations(frozenset(obligations))
            licenses[-1].set_prohibitions(frozenset(prohibitions))


def _no_order(licenses, limit=144):
    # More than 144 is not possible here
    if limit > 144:
        limit = 144
    label = 0
    for action in ODRL.ACTIONS:
        if len(licenses) < limit:
            licenses.append(License())
            licenses[-1].set_labels([str(label)])
            licenses[-1].set_obligations(frozenset([action]))
            label += 1
    for action in ODRL.ACTIONS:
        if len(licenses) < limit:
            licenses.append(License())
            licenses[-1].set_labels([str(label)])
            licenses[-1].set_prohibitions(frozenset([action]))
            label += 1


def _partial_order(licenses, limit=144):
    if limit > 1000000000:
        limit = 1000000000
    label = 0
    while len(licenses) < limit:
        license = _random_license(label)
        if license not in licenses:
            licenses.append(license)
            label += 1
    licenses = sorted(licenses, key=methodcaller('get_level'))


def _random_license(label):
    license = License()
    license.set_labels([str(label)])
    license.set_permissions(frozenset(_generate_set()))
    license.set_obligations(frozenset(_generate_set()))
    license.set_prohibitions(frozenset(_generate_set()))
    return license


def _generate_set():
    # print sum(ODRL_WEIGHTS)
    set_size = choice(len(SET_SIZE_WEIGHTS), size=1, replace=True, p=SET_SIZE_WEIGHTS)[0]
    return choice(ODRL.ACTIONS[:len(ODRL_WEIGHTS)], size=set_size, replace=False, p=ODRL_WEIGHTS)


def _lattice(licenses, nb_actions):
    actions = ODRL.ACTIONS[:nb_actions]
    for comb_perm in _all_actions_combinations(actions):
        for permission_set in comb_perm:
            permissions = frozenset(permission_set)
            for comb_oblig in _all_actions_combinations(actions):
                for obligation_set in comb_oblig:
                    obligations = frozenset(obligation_set)
                    if permissions.isdisjoint(obligations):
                        for comb_prohib in _all_actions_combinations(actions):
                            for prohibition_set in comb_prohib:
                                prohibitions = frozenset(prohibition_set)
                                if permissions.isdisjoint(prohibitions) and obligations.isdisjoint(prohibitions):
                                    licenses.append(License())
                                    licenses[-1].set_labels(['{}{}{}'.format(permissions, prohibitions, obligations)])
                                    licenses[-1].set_permissions(permissions)
                                    licenses[-1].set_obligations(obligations)
                                    licenses[-1].set_prohibitions(prohibitions)


def _all_actions_combinations(actions):
    all_actions_combinations = []
    for i in range(len(actions)+1):
        all_actions_combinations.append(itertools.combinations(actions, i))
    return all_actions_combinations
