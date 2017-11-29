class ConsolidatedLicenses(object):

    def __init__(self, label, permissions, obligations, prohibitions):
        self.label = label
        self.permissions = permissions
        self.obligations = obligations
        self.prohibitions = prohibitions

    def is_consolidated(self, Terms):
        if self.permissions & self.obligations & self.prohibitions:
            return False
        return (self.permissions | self.obligations | self.prohibitions) == Terms

    @property
    def label(self):
        return self.label

    @property
    def permissions(self):
        return self.permissions

    @property
    def obligations(self):
        return self.obligations

    @property
    def prohibitions(self):
        return self.prohibitions

    @permissions.setter
    def permissions(self, permissions):
        self.permissions = permissions

    @obligations.setter
    def obligations(self, obligations):
        self.obligations = obligations

    @prohibitions.setter
    def prohibitions(self, prohibitions):
        self.prohibitions = prohibitions
