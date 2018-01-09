from licenses.ConsolidatedLicense import ConsolidatedLicense, hash_label
from Lattice import Lattice
from utils.TimerDecorator import fn_timer

from threading import Thread, Lock
from itertools import combinations, islice
from sys import exit

label_dict = {}
licenses_hash_table = {}
label_dict_lock = Lock()
licenses_hash_table_lock = Lock()


class LicenseCombinor(Thread):

    def __init__(self, couples, lattice):
        Thread.__init__(self)
        self.couples = couples
        self.new_layer = set()
        self.lattice = lattice
        self.thread_finish = False

    def terminate(self):
        self.thread_finish = True

    def run(self):
        self.new_layer = set()
        for couple in self.couples:
            if not self.thread_finish:
                cl1 = couple[0]
                cl2 = couple[1]
                combined_label = cl1.label | cl2.label
                if len(combined_label) < self.lattice.height()+1:
                    hashed_label = hash_label(combined_label)
                    label_dict_lock.acquire()
                    if hashed_label in label_dict:
                        label_dict_lock.release()
                        # this licence is already created by combining other licenses
                        label_dict[hashed_label].parents.append((cl1, cl2))
                        cl1.childs.append(label_dict[hashed_label])
                        cl2.childs.append(label_dict[hashed_label])
                    else:
                        new_license = self.combination_function(cl1, cl2, combined_label)
                        if self.prune_filter(new_license):
                            label_dict[hashed_label] = new_license
                            label_dict_lock.release()
                            self.add_in_hash_table(new_license)
                            self.new_layer.add(new_license)
                        else:
                            label_dict_lock.release()

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
        licenses_hash_table_lock.acquire()
        if license.hash in licenses_hash_table:
            licenses_hash_table[license.hash].append(license)
        else:
            licenses_hash_table[license.hash] = [license]
        licenses_hash_table_lock.release()


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
    def generate_lattice(self, nb_couples_per_threads):
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
            chunk_size = nb_couples_per_threads
            nb_threads = nb_couples / chunk_size
            if nb_threads < 1:
                nb_threads = 1
            rest = nb_couples % nb_threads
            threads = []
            try:
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
            except KeyboardInterrupt:
                print "Ctrl-c pressed ..."
                for thread in threads:
                    thread.terminate()
                    exit(1)
            print ("layer {} is ok".format(self.height()-1))
        self.licenses_hash_table = licenses_hash_table
