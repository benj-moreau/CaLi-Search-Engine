class License(object):

    def __init__(self, labels, permissions, obligations, prohibitions, datasets):
        self.labels = labels
        if not isinstance(permissions, set):
            raise TypeError("permissions must be of type: set")
        self.permissions = permissions
        if not isinstance(obligations, set):
            raise TypeError("obligations must be of type: set")
        self.obligations = obligations
        if not isinstance(prohibitions, set):
            raise TypeError("prohibitions must be of type: set")
        self.prohibitions = prohibitions
        self.datasets = datasets

    def is_consolidated(self, terms):
        if self.permissions.isdisjoint(self.obligations):
            if self.permissions.isdisjoint(self.prohibitions):
                if self.obligations.isdisjoint(self.prohibitions):
                    return (self.permissions | self.obligations | self.prohibitions) == terms
        return False

    def get_labels(self):
        return [str(label) for label in self.labels]

    def get_permissions(self):
        return [str(permission) for permission in self.permissions]

    def get_obligations(self):
        return [str(obligation) for obligation in self.obligations]

    def get_prohibitions(self):
        return [str(prohibitions) for prohibitions in self.prohibitions]

    def get_datasets(self):
        return self.datasets

    def to_json(self):
        return {
            'labels': self.get_labels(),
            'permissions': self.get_permissions(),
            'obligations': self.get_obligations(),
            'prohibitions': self.get_prohibitions(),
            'datasets': [dataset.to_json() for dataset in self.datasets]
        }

    def repr_terms(self):
        """Using Permissions, obligations, prohibitions to print licence."""
        return "Permissions:{}, Obligations:{}, Prohibitions:{}".format(list(self.permissions),
                                                                        list(self.obligations),
                                                                        list(self.prohibitions))

    def __eq__(self, other):
        """Using label to differentiate licenses in lattice' sets."""
        return isinstance(other, License) and self.label == other.label

    def __hash__(self):
        """Using label to differentiate licenses in lattice' sets."""
        return hash("{}".format([self.permissions, self.obligations, self.prohibitions]))

    def __repr__(self):
        """Using label to print licenses."""
        return "{}".format(self.get_labels)

    def __str__(self):
        """Using label to print licenses."""
        return self.__repr__()
