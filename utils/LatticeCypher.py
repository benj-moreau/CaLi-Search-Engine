LICENSE_CREATION = 'CREATE({}:License{{label:"{}", permissions:"{}", obligations:"{}", prohibitions:"{}", hash_terms:"{}", level:"{}"}})'
RELATION_CREATION = 'CREATE(({})-[:Preserves]->({}))'


def generate_cypher_files(lattice, nb_terms):
    with open('licenses_A{}.cypher'.format(nb_terms), 'w') as licenses_file:
        relations = ""
        for level_number, level in enumerate(lattice.set):
            for license in level:
                licenses_file.write("{}\n".format(_generate_node(license, level_number)))
                for child in license.childs:
                    relations = "{}{}\n".format(relations, _generate_relation(license, child, level_number))
        licenses_file.write(relations)


def _generate_node(license, level_number):
    return LICENSE_CREATION.format("{}_{}".format(license.get_label(), level_number),
                                   license.get_label(),
                                   license.get_permissions(),
                                   license.get_obligations(),
                                   license.get_prohibitions(),
                                   license.hash,
                                   level_number)


def _generate_relation(license, child, level_number):
    return RELATION_CREATION.format("{}_{}".format(license.get_label(), level_number),
                                    "{}_{}".format(child.get_label(), level_number + 1))
