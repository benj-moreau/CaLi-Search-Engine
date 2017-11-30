import licenses.ConsolidatedLicenses as ConsolidatedLicenses
from Lattice import Lattice


class LicensesLattice(Lattice):

    def combination_function(self, CL1, CL2):
        label = "{label1},{label2}".format(label1=CL1.label, label2=CL2.label)
        permissions = CL1.permissions & CL2.permissions
        obligations = CL1.obligations | CL2.obligations
        prohibitions = CL1.prohibitions | CL2.prohibitions
        ConsolidatedLicenses(label, permissions, obligations, prohibitions)

    def generate_lattice(self):
        print self.powerset
