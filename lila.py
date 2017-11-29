import argparse
import utils.LicensesPowersetGenerator as PowersetGenerator


def main():
    parser = argparse.ArgumentParser(prog='lila', description='Experiments with lattice.')
    parser.add_argument('terms_number', metavar='t', type=int, nargs='+',
                        help='Terms set cardinality (e.g. number of actions)')
    args = parser.parse_args()
    terms_number = args.terms_number[0]
    PowersetGenerator.generate(['a', 'b', 'c'])
    print terms_number


if __name__ == "__main__":
    main()
