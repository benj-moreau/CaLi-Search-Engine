import argparse
import json
import utils.LicensesPowersetGenerator as PowersetGenerator
from lattice.LicensesLattice import LicensesLattice
from utils.LatticeCypher import generate_cypher_files


def main():
    parser = argparse.ArgumentParser(prog='cali', description='Experiments with lattice.')
    parser.add_argument('filename', metavar='f', type=str, nargs='+',
                        help='json file containing terms')
    args = parser.parse_args()
    result = json.load(open(args.filename[0]))
    terms = result["terms"]
    powerset = PowersetGenerator.generate_minimal_licences_set(terms)
    cali = LicensesLattice(terms, powerset)
    cali.generate_lattice()
    generate_cypher_files(cali, len(terms))


if __name__ == "__main__":
    main()
