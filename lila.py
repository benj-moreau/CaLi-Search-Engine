import argparse
import utils.LicensesPowersetGenerator as PowersetGenerator
from lattice.LicensesLattice import LicensesLattice


def main():
    parser = argparse.ArgumentParser(prog='lila', description='Experiments with lattice.')
    parser.add_argument('terms_number', metavar='t', type=int, nargs='+',
                        help='Terms set cardinality (e.g. number of actions)')
    args = parser.parse_args()
    Terms = ['a', 'b', 'c']
    powerset = PowersetGenerator.generate(Terms)
    lila = LicensesLattice(powerset)
    lila.generate_lattice()


if __name__ == "__main__":
    main()
