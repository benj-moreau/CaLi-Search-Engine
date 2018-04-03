def hash_label(label):
    """Using label to spot equivalent licenses."""
    return hash(label)


class ConsolidatedLicense(object):

    def __init__(self, label, permissions, obligations, prohibitions, parents, childs):
        self.label = label
        self.permissions = permissions
        self.obligations = obligations
        self.prohibitions = prohibitions
        self.parents = parents
        self.childs = childs

    def is_consolidated(self, terms):
        return (self.permissions | self.obligations | self.prohibitions) == terms

    def is_viable(self):
        if not(self.permissions.isdisjoint(self.obligations) and self.permissions.isdisjoint(self.prohibitions) and self.obligations.isdisjoint(self.prohibitions)):
            return False
        return True

    def get_label(self):
        label = ""
        for l in self.label:
            label = "{}{}".format(label, l)
        return label

    def get_permissions(self):
        return [str(item) for item in self.permissions]

    def get_obligations(self):
        return [str(item) for item in self.obligations]

    def get_prohibitions(self):
        return [str(item) for item in self.prohibitions]

    @property
    def hash(self):
        """Using Permissions, obligations, prohibitions to spot equivalent licenses."""
        return hash("{}".format([self.permissions, self.obligations, self.prohibitions]))

    def repr_terms(self):
        """Using Permissions, obligations, prohibitions to print licence."""
        return "Permissions:{}, Obligations:{}, Prohibitions:{}".format(list(self.permissions),
                                                                        list(self.obligations),
                                                                        list(self.prohibitions))

    def __eq__(self, other):
        """Using label to differentiate licenses in lattice' sets."""
        return isinstance(other, ConsolidatedLicense) and self.hash == other.hash

    def __hash__(self):
        """Using label to differentiate licenses in lattice' sets."""
        return hash_label(self.label)

    def __repr__(self):
        """Using label to print licenses."""
        label = []
        for lic in self.label:
            label.append(lic)
        return "{}".format(label)

    def __str__(self):
        """Using label to print licenses."""
        return self.__repr__()
