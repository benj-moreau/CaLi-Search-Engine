from objectmodels.License import License


class Lattice(object):

    def __init__(self, actions):
        self.infimum = License()
        self.infimum.set_labels(['infimum'])
        self.infimum.set_permissions(frozenset(actions))
        self.supremum = License()
        self.supremum.set_labels(['supremum'])
        self.supremum.set_obligations(frozenset(actions))
        self.supremum.set_prohibitions(frozenset(actions))
        self.infimum.followings.append(self.supremum)
        self.supremum.precedings.append(self.infimum)
        self.licenses = []

    def len(self):
        return len(self.licenses) + 2

    def get_supremum(self):
        return self.supremum

    def get_infimum(self):
        return self.infimum

    def add_license(self, license):
        if license not in self.licenses:
            self.licenses.append(license)

    def reset(self):
        self.infimum.followings.clear()
        self.infimum.precedings.clear()
        self.supremum.followings.clear()
        self.supremum.precedings.clear()
        self.licenses.clear()
