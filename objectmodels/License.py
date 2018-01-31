from objectmodels.Dataset import Dataset


class License(object):

    def __init__(self):
        self.labels = []
        self.permissions = set()
        self.obligations = set()
        self.prohibitions = set()
        self.datasets = []

    def hash(self):
        return self.__hash__()

    def is_viable(self):
        if not self.premission:
            return True

    def is_consolidated(self, terms):
        if self.permissions.isdisjoint(self.obligations):
            if self.permissions.isdisjoint(self.prohibitions):
                if self.obligations.isdisjoint(self.prohibitions):
                    return (self.permissions | self.obligations | self.prohibitions) == terms
        return False

    def is_preceding(self, license):
        # is self a precedor of license?
        if self.permissions.issuperset(license.permissions):
            if self.obligations.issubset(license.obligations):
                if self.prohibitions.issubset(license.prohibitions):
                    return True
        return False

    def is_following(self, license):
        # is self a follower of license?
        return license.is_preceding(self)

    def get_labels(self):
        return self.labels

    def get_permissions(self):
        return [str(permission) for permission in self.permissions]

    def get_obligations(self):
        return [str(obligation) for obligation in self.obligations]

    def get_prohibitions(self):
        return [str(prohibitions) for prohibitions in self.prohibitions]

    def get_datasets(self):
        return self.datasets

    def set_labels(self, labels):
        self.labels = labels

    def set_permissions(self, permissions):
        if not isinstance(permissions, set):
            raise TypeError("permissions must be of type: set")
        self.permissions = permissions

    def set_obligations(self, obligations):
        if not isinstance(obligations, set):
            raise TypeError("obligations must be of type: set")
        self.obligations = obligations

    def set_prohibitions(self, prohibitions):
        if not isinstance(prohibitions, set):
            raise TypeError("prohibitions must be of type: set")
        self.prohibitions = prohibitions

    def set_datasets(self, datasets):
        self.datasets = datasets

    def from_json(self, json_license):
        self.set_labels(json_license['labels'])
        self.set_permissions(set(json_license['permissions']))
        self.set_obligations(set(json_license['obligations']))
        self.set_prohibitions(set(json_license['prohibitions']))
        datasets = []
        for dataset in json_license['datasets']:
            dataset_object = Dataset()
            dataset_object.from_json(dataset)
            datasets.append(dataset_object)
        self.set_datasets(datasets)

    def to_json(self):
        return {
            'labels': self.get_labels(),
            'permissions': self.get_permissions(),
            'obligations': self.get_obligations(),
            'prohibitions': self.get_prohibitions(),
            'datasets': [dataset.to_json() for dataset in self.datasets],
            'hashed_sets': self.hash()
        }

    def repr_terms(self):
        """Using Permissions, obligations, prohibitions to print licence."""
        return "Permissions:{}, Obligations:{}, Prohibitions:{}".format(list(self.permissions),
                                                                        list(self.obligations),
                                                                        list(self.prohibitions))

    def __eq__(self, other):
        """Using label to differentiate licenses."""
        return isinstance(other, License) and self.label == other.label

    def __hash__(self):
        """Using Permissions, obligations, prohibitions to differentiate licenses."""
        return hash("{}".format([self.permissions, self.obligations, self.prohibitions]))

    def __repr__(self):
        """Using label to print licenses."""
        return "{}".format(self.get_labels)

    def __str__(self):
        """Using label to print licenses."""
        return self.__repr__()
