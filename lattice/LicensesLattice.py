from licenses.ConsolidatedLicense import ConsolidatedLicense
from Lattice import Lattice


class LicensesLattice(Lattice):
    def prune_filter(self, cl):
        return True
        return cl.is_consolidated(self.terms)

    def combination_function(self, cl1, cl2):
        label = cl1.label | cl2.label
        permissions = cl1.permissions & cl2.permissions
        obligations = cl1.obligations | cl2.obligations
        prohibitions = cl1.prohibitions | cl2.prohibitions
        parents = [cl1, cl2]
        return ConsolidatedLicense(label, permissions, obligations, prohibitions, parents)

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

    def repr(self):
        self.repr_rec(list(self.set[self.height()-1])[0])

    def repr_rec(self, cl):
        print cl
        for license in cl.parents:
            self.repr_rec(license)
