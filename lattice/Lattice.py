class Lattice(object):

    def __init__(self, terms, powerset):
        self.set = (set([]), set(powerset))
        self.terms = set(terms)

    def combination_function(self, element1, element2):
        raise NotImplementedError()

    def generate_lattice(self):
        raise NotImplementedError()

    def height(self):
        return len(self.set)

    def nb_nodes(self):
        nb_nodes = 0
        for floor in self.set:
            nb_nodes += len(floor)
        return nb_nodes

    def layer_nb_nodes(self, layer):
        return len(self.set[layer])
