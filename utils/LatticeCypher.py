LICENSE_CREATION = 'CREATE({}:License{{label:"{}", permissions:"{}", obligations:"{}", prohibitions:"{}", hash_terms:"{}", level:"{}"}})'
RELATION_CREATION = 'CREATE(({})-[:Preserves]->({}))'


def generate_cypher_files(lattice):
    with open('licenses.cypher', 'w') as licenses_file:
        with open('licenses_relations.cypher', 'w') as relations_file:
            for level_number, level in enumerate(lattice.set):
                for license in level:
                    licenses_file.write("{}\n".format(_generate_node(license, level_number)))
                    for child in license.childs:
                        relations_file.write("{}\n".format(_generate_relation(license, child, level_number)))


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
