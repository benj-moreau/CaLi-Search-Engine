class ConsolidatedLicense(object):

    def __init__(self, label, permissions, obligations, prohibitions, parents):
        self.label = label
        self.permissions = permissions
        self.obligations = obligations
        self.prohibitions = prohibitions
        self.parents = parents

    def is_consolidated(self, Terms):
        if self.permissions.isdisjoint(self.obligations):
            if self.permissions.isdisjoint(self.prohibitions):
                if self.obligations.isdisjoint(self.prohibitions):
                    return (self.permissions | self.obligations | self.prohibitions) == Terms
        return False

    def __eq__(self, other):
        return isinstance(other, ConsolidatedLicense) and self.label == other.label

    def __hash__(self):
        return hash(self.label)

    def __repr__(self):
        return "{}".format(self.label)

    def __str__(self):
        return "{}".format(self.label)
