from licenses.ConsolidatedLicense import ConsolidatedLicense


def generate_minimal_licences_set(Terms):
    powerset = []
    ind = 0
    for term in Terms:
        permissions = []
        for t in Terms:
            if t != term:
                permissions.append(t)
        ind += 1
        label = "L{}".format(ind)
        powerset.append(ConsolidatedLicense(frozenset([label]), set(permissions), set([term]), set(), [], []))
        ind += 1
        label = "L{}".format(ind)
        powerset.append(ConsolidatedLicense(frozenset([label]), set(permissions), set(), set([term]), [], []))
    return powerset
