from licenses.ConsolidatedLicense import ConsolidatedLicense
from Lattice import Lattice
from utils.TimerDecorator import fn_timer


class LicensesLattice(Lattice):

    def __init__(self, terms, powerset):
        super(LicensesLattice, self).__init__(terms, powerset)
        self.licenses_hash_table = {}
        # Update hash table with powerset's licenses
        for license in self.set[self.height()-1]:
            self._add_in_hash_table(license)

    def prune_filter(self, cl):
        # return cl.is_consolidated(self.terms)
        return True

    def combination_function(self, cl1, cl2):
        label = cl1.label | cl2.label
        permissions = cl1.permissions & cl2.permissions
        obligations = cl1.obligations | cl2.obligations
        prohibitions = cl1.prohibitions | cl2.prohibitions
        obligations, prohibitions = self.combination_priority(obligations, prohibitions, "obligation")
        parents = [cl1, cl2]
        new_cl = ConsolidatedLicense(label, permissions, obligations, prohibitions, parents, [])
        cl1.childs.append(new_cl)
        cl2.childs.append(new_cl)
        return new_cl

    def combination_priority(self, obligations, prohibitions, priority="obligation"):
        if priority == "obligation":
            prohibitions = prohibitions - obligations
        else:
            obligations = obligations - prohibitions
        return obligations, prohibitions

    @fn_timer
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
                        self._add_in_hash_table(new_license)
            self.set += (new_layer,)
            print self.layer_nb_nodes(self.height()-1)

    def repr(self):
        self.repr_rec(list(self.set[self.height()-1])[0])

    def repr_rec(self, cl):
        print cl
        for license in cl.parents:
            self.repr_rec(license)

    def _add_in_hash_table(self, license):
        if license.hash in self.licenses_hash_table:
            self.licenses_hash_table[license.hash].append(license)
        else:
            self.licenses_hash_table[license.hash] = [license]
