import random
from operator import methodcaller

import utils.ODRL as ODRL
from objectmodels.License import License


# Generate a set of licenses using ODRL vocabulary.
# structure: linear_order/no_order/partial_order
# order: asc/desc/rand
def generate(structure='linear_order', order='asc', limit=144):
    licenses = []
    # structure
    if structure == 'linear_order':
        _linear_order(licenses, limit)
    elif structure == 'no_order':
        _no_order(licenses, limit)
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
        label += 1
        obligations.append(action)
        licenses.append(License())
        licenses[-1].set_labels([str(label)])
        licenses[-1].set_obligations(frozenset(obligations))
    # prohibitions
    for action in ODRL.ACTIONS:
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
        licenses.append(License())
        licenses[-1].set_labels([str(label)])
        licenses[-1].set_obligations(frozenset([action]))
        label += 1
    for action in ODRL.ACTIONS:
        licenses.append(License())
        licenses[-1].set_labels([str(label)])
        licenses[-1].set_prohibitions(frozenset([action]))
        label += 1


def _partial_order(licenses, limit=144):
    if limit > 1000000000:
        limit = 1000000000
    label = 0
    while label < limit:
        license = _random_license(label)
        if license not in licenses:
            licenses.append(license)
            label += 1
    licenses = sorted(licenses, key=methodcaller('get_level'))


def _random_license(label):
    license = License()
    license.set_labels([str(label)])
    nb_permissions = random.randint(0, len(ODRL.ACTIONS[:10])-1)
    nb_obligations = random.randint(0, len(ODRL.ACTIONS[:10])-1)
    nb_prohibitions = random.randint(0, len(ODRL.ACTIONS[:10])-1)
    license.set_permissions(frozenset(random.sample(ODRL.ACTIONS[:10], nb_permissions)))
    license.set_obligations(frozenset(random.sample(ODRL.ACTIONS[:10], nb_obligations)))
    license.set_prohibitions(frozenset(random.sample(ODRL.ACTIONS[:10], nb_prohibitions)))
    return license
