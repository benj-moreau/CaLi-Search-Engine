LICENSE_CREATION = 'CREATE({}:License{{label:"{}", permissions:"{}", obligations:"{}", prohibitions:"{}", hash_terms:"{}", level:"{}"}})'
RELATION_CREATION = 'CREATE(({})-[:Preserves]->({}))'


def generate_cypher_files(lattice, nb_terms):
    with open('licenses_A{}.cypher'.format(nb_terms), 'w') as licenses_file:
        relations = ""
        licenses_file.write("{}\n".format(LICENSE_CREATION.format('L0', 'A', '{}', '{}', '{}', '{}', 0)))
        for license in lattice.set[1]:
            relations = "{}{}\n".format(relations, RELATION_CREATION.format('L0', license.get_label()))
        for level_number, level in enumerate(lattice.set):
            for license in level:
                licenses_file.write("{}\n".format(_generate_node(license, level_number)))
                for child in license.childs:
                    relations = "{}{}\n".format(relations, _generate_relation(license, child))
        licenses_file.write(relations)


def _generate_node(license, level_number):
    return LICENSE_CREATION.format(license.get_label(),
                                   license.get_label(),
                                   license.get_permissions(),
                                   license.get_obligations(),
                                   license.get_prohibitions(),
                                   license.hash,
                                   level_number)


def _generate_relation(license, child):
    return RELATION_CREATION.format(license.get_label(),
                                    child.get_label())
