class ConsolidatedLicense(object):

    def __init__(self, label, permissions, obligations, prohibitions):
        self.label = [].append(label)
        self.permissions = permissions
        self.obligations = obligations
        self.prohibitions = prohibitions

    def is_consolidated(self, Terms):
        if self.permissions & self.obligations & self.prohibitions:
            return False
        return (self.permissions | self.obligations | self.prohibitions) == Terms
