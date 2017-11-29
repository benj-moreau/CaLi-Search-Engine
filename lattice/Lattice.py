class Lattice(object):

    def __init__(self, powerset):
        self.powerset = powerset

    def combination_function(self, element1, element2):
        raise NotImplementedError()

    def generate_lattice(self):
        raise NotImplementedError()
