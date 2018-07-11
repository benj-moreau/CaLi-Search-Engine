from objectmodels.Dataset import Dataset
from utils.ODRL import ACTIONS as ODRL_ACTIONS


class License(object):

    def __init__(self):
        self.labels = []
        self.permissions = frozenset()
        self.obligations = frozenset()
        self.prohibitions = frozenset()
        self.datasets = []

    def hash(self):
        # used to compare licenses in terms of permissions, obligations, prohibitions
        return self.__hash__()

    def is_consolidated(self, terms):
        # is consolidated if self uses all actions in terms set
        if self.permissions.isdisjoint(self.obligations):
            if self.permissions.isdisjoint(self.prohibitions):
                if self.obligations.isdisjoint(self.prohibitions):
                    return (self.permissions | self.obligations | self.prohibitions) == terms
        return False

    def is_preceding(self, license):
        # is self compatible with license?
        if self.permissions.issuperset(license.permissions):
            if self.obligations.issubset(license.obligations):
                if self.prohibitions.issubset(license.prohibitions):
                    return True
        return False

    def is_following(self, license):
        # is self compliant with license?
        return license.is_preceding(self)

    def get_labels(self):
        return self.labels

    def get_permissions(self):
        return [str(permission) for permission in self.permissions]

    def get_obligations(self):
        return [str(obligation) for obligation in self.obligations]

    def get_prohibitions(self):
        return [str(prohibitions) for prohibitions in self.prohibitions]

    def get_level(self):
        return len(self.obligations) + len(self.prohibitions)

    def get_datasets(self):
        return self.datasets

    def set_labels(self, labels):
        self.labels = labels

    def set_permissions(self, permissions):
        if not isinstance(permissions, frozenset):
            raise TypeError("permissions must be of type: frozenset")
        self.permissions = permissions

    def set_obligations(self, obligations):
        if not isinstance(obligations, frozenset):
            raise TypeError("obligations must be of type: frozenset")
        self.obligations = obligations

    def set_prohibitions(self, prohibitions):
        if not isinstance(prohibitions, frozenset):
            raise TypeError("prohibitions must be of type: frozenset")
        self.prohibitions = prohibitions

    def set_datasets(self, datasets):
        self.datasets = datasets

    def from_json(self, json_license):
        self.set_labels(json_license['labels'])
        self.set_permissions(frozenset(json_license['permissions']))
        self.set_obligations(frozenset(json_license['obligations']))
        self.set_prohibitions(frozenset(json_license['prohibitions']))
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

    def contains_only_odrl_actions(self):
        for action in self.permissions:
            if action not in ODRL_ACTIONS:
                return False
        for action in self.obligations:
            if action not in ODRL_ACTIONS:
                return False
        for action in self.prohibitions:
            if action not in ODRL_ACTIONS:
                return False
        return True

    def repr_terms(self):
        """Using Permissions, obligations, prohibitions to print licence."""
        return "Permissions:{}, Obligations:{}, Prohibitions:{}".format(list(self.permissions),
                                                                        list(self.obligations),
                                                                        list(self.prohibitions))

    def __eq__(self, other):
        """Using label to differentiate licenses."""
        return isinstance(other, License) and self.__hash__() == other.__hash__()

    def __hash__(self):
        """Using Permissions, obligations, prohibitions to differentiate licenses."""
        return str(hash(self.permissions) + hash(self.obligations) + hash(self.prohibitions))

    def __repr__(self):
        """Using label to print licenses."""
        labels = self.get_labels()
        license_label = ""
        for i, label in enumerate(labels):
            if i < 1:
                license_label = "{}".format(label)
            else:
                license_label = "{}, {}".format(license_label, label)
        return license_label

    def __str__(self):
        """Using label to print licenses."""
        return self.__repr__()
