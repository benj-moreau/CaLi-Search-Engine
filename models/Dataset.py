class Dataset(object):

    def __init__(self, label, uri, description):
        self.label = label
        self.uri = uri
        self.description = description

    def get_label(self):
        return self.label

    def get_uri(self):
        return self.uri

    def get_description(self):
        return self.description

    def to_json(self):
        return {
            'label': self.get_label(),
            'uri': self.get_uri(),
            'description': self.get_description(),
        }

    def __eq__(self, other):
        """Using uri to differentiate Datasets."""
        return isinstance(other, Dataset) and self.uri == other.uri

    def __hash__(self):
        """Using uri to spot equivalent Datasets."""
        return hash(self.uri)

    def __repr__(self):
        """Using label&uri to print Datasets."""
        return "{label}@{uri}".format(label=self.get_label(), uri=self.get_uri())

    def __str__(self):
        """Using label&uri to print Datasets."""
        self.__repr__()
