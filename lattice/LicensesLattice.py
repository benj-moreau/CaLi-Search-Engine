from licenses.ConsolidatedLicense import ConsolidatedLicense, hash_label
from Lattice import Lattice
from utils.TimerDecorator import fn_timer
from threading import Thread
from itertools import combinations, islice

label_dict = {}
licenses_hash_table = {}


class LicenseCombinor(Thread):

    def __init__(self, couples, lattice):
        Thread.__init__(self)
        self.couples = couples
        self.new_layer = set()
        self.lattice = lattice

    def run(self):
        self.new_layer = set()
        for couple in self.couples:
            cl1 = couple[0]
            cl2 = couple[1]
            combined_label = cl1.label | cl2.label
            print len(combined_label)
            hashed_label = hash_label(combined_label)
            if hashed_label in label_dict:
                # this licence is already created by combining other licenses
                label_dict[hashed_label].parents.append((cl1, cl2))
                cl1.childs.append(label_dict[hashed_label])
                cl2.childs.append(label_dict[hashed_label])
                if label_dict[hashed_label] in self.lattice.set[self.lattice.height()-1]:
                    # The license have to 1 layer up
                    self.new_layer.add(label_dict[hashed_label])
                    self.lattice.set[self.lattice.height()-1].remove(label_dict[hashed_label])
            else:
                new_license = self.combination_function(cl1, cl2, combined_label)
                if self.prune_filter(new_license):
                    label_dict[hashed_label] = new_license
                    self.add_in_hash_table(new_license)
                    self.new_layer.add(new_license)

    def combination_function(self, cl1, cl2, label):
        permissions = cl1.permissions & cl2.permissions
        obligations = cl1.obligations | cl2.obligations
        prohibitions = cl1.prohibitions | cl2.prohibitions
        obligations, prohibitions = self.combination_priority(obligations, prohibitions, "obligation")
        parents = [(cl1, cl2)]
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

    def prune_filter(self, cl):
        # return cl.is_consolidated(self.terms)
        return True

    def add_in_hash_table(self, license):
        if license.hash in licenses_hash_table:
            licenses_hash_table[license.hash].append(license)
        else:
            licenses_hash_table[license.hash] = [license]


class LicensesLattice(Lattice):

    def __init__(self, terms, powerset):
        super(LicensesLattice, self).__init__(terms, powerset)
        self.licenses_hash_table = {}
        # Update hash table with powerset's licenses
        for license in self.set[self.height()-1]:
            if license.hash in licenses_hash_table:
                licenses_hash_table[license.hash].append(license)
            else:
                licenses_hash_table[license.hash] = [license]

    @fn_timer
    def generate_lattice(self, nb_threads):
        print ("layer 0 is ok")
        for license in self.set[self.height()-1]:
            if license.hash in self.licenses_hash_table:
                self.licenses_hash_table[license.hash].append(license)
            else:
                self.licenses_hash_table[license.hash] = [license]
        print ("layer 1 is ok")
        while self.layer_nb_nodes(self.height()-1) > 1:
            previous_layer = self.set[self.height()-1]
            couples = combinations(previous_layer, 2)
            nb_couples = (len(previous_layer)) * (len(previous_layer)-1) / 2
            chunk_size = nb_couples / nb_threads
            rest = nb_couples % nb_threads
            threads = []
            for i in range(0, nb_threads):
                if i == 0 and rest:
                    chunk_couples = islice(couples, 0, chunk_size+rest)
                else:
                    chunk_couples = islice(couples, 0, chunk_size)
                threads.append(LicenseCombinor(chunk_couples, self))
                threads[i].start()
            new_layer = set()
            for thread in threads:
                thread.join()
                new_layer = new_layer | thread.new_layer
            self.set += (new_layer,)
            print ("layer {} is ok".format(self.height()-1))
        self.licenses_hash_table = licenses_hash_table
