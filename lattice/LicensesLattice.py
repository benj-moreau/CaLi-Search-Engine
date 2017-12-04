from licenses.ConsolidatedLicense import ConsolidatedLicense
from Lattice import Lattice


class LicensesLattice(Lattice):

    def combination_function(self, CL1, CL2):
        label = CL1.label | CL2.label
        permissions = CL1.permissions & CL2.permissions
        obligations = CL1.obligations | CL2.obligations
        prohibitions = CL1.prohibitions | CL2.prohibitions
        ConsolidatedLicense(label, permissions, obligations, prohibitions)

    def generate_lattice(self):
        print self.powerset
