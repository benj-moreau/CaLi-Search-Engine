import argparse
import utils.LicensesPowersetGenerator as PowersetGenerator
from lattice.LicensesLattice import LicensesLattice


def main():
    parser = argparse.ArgumentParser(prog='cali', description='Experiments with lattice.')
    parser.add_argument('filename', metavar='f', type=str, nargs='+',
                        help='json file containing terms')
    args = parser.parse_args()
    terms = ['a', 'b']
    powerset = PowersetGenerator.generate_licenses(terms)
    cali = LicensesLattice(terms, powerset)
    cali.generate_lattice()
    for v in cali.licenses_hash_table:
        print len(cali.licenses_hash_table[v])
        print cali.licenses_hash_table[v][0].repr_terms()
        for lic in cali.licenses_hash_table[v]:
            print lic


if __name__ == "__main__":
    main()
