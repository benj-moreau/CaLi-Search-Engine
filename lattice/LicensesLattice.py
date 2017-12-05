from licenses.ConsolidatedLicense import ConsolidatedLicense
from Lattice import Lattice


class LicensesLattice(Lattice):
    def prune_filter(self, CL):
        return CL.is_consolidated(self.terms)

    def combination_function(self, CL1, CL2):
        label = CL1.label | CL2.label
        permissions = CL1.permissions & CL2.permissions
        obligations = CL1.obligations | CL2.obligations
        prohibitions = CL1.prohibitions | CL2.prohibitions
        return ConsolidatedLicense(label, permissions, obligations, prohibitions)

    def generate_lattice(self):
        print self.layer_nb_nodes(0)
        print self.layer_nb_nodes(1)
        while self.layer_nb_nodes(self.height()-1) > 1:
            new_layer = set([])
            previous_layer = list(self.set[self.height()-1])
            for i in range(len(previous_layer)-1):
                for j in range(i+1, len(previous_layer)):
                    new_license = self.combination_function(previous_layer[i],
                                                            previous_layer[j])
                    if self.prune_filter(new_license):
                        new_layer.add(new_license)
            self.set += (new_layer,)
            print len(new_layer)
