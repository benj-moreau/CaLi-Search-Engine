from neomodel import StructuredNode, ArrayProperty, StringProperty, RelationshipFrom, RelationshipTo
from neomodel import db


# DAO. Objects used to access data in neo4j database
class LicenseModel(StructuredNode):
    labels = ArrayProperty()
    licensing_terms = ArrayProperty()
    permissions = ArrayProperty(index=True)
    obligations = ArrayProperty(index=True)
    prohibitions = ArrayProperty(index=True)
    hashed_sets = StringProperty(unique_index=True)
    graph = StringProperty(index=True)

    followings = RelationshipTo("LicenseModel", "Compatible")
    precedings = RelationshipFrom("LicenseModel", "Compatible")
    datasets = RelationshipTo("DatasetModel", "Protects")


def license_filter_labels(label, graph):
    results, columns = db.cypher_query("match(license:LicenseModel) WHERE any(label in license.labels WHERE label CONTAINS '{}') AND license.graph = '{}' RETURN license".format(label, graph))
    return [LicenseModel().inflate(row[0]) for row in results]


def license_filter_sets(values, set_name, graph):
    results, columns = db.cypher_query("match(license:LicenseModel) WHERE all(value IN {values} WHERE value IN license.{set_name}) AND license.graph = '{graph}' RETURN license"
                                       .format(values=values, set_name=set_name, graph=graph))
    return [LicenseModel().inflate(row[0]) for row in results]


def get_leaf_licenses(graph):
    results, columns = db.cypher_query("match(license:LicenseModel) WHERE not ()-[:Compatible]->(license) AND license.graph = '{}' RETURN license ORDER BY (size(license.prohibitions)+size(license.obligations)) ASC".format(graph))
    return [LicenseModel().inflate(row[0]) for row in results]


def get_root_licenses(graph):
    results, columns = db.cypher_query("match(license:LicenseModel) WHERE not ()<-[:Compatible]-(license) AND license.graph = '{}' RETURN license ORDER BY (size(license.prohibitions)+size(license.obligations)) DESC".format(graph))
    return [LicenseModel().inflate(row[0]) for row in results]


def get_compatible_licenses(hashed_sets, graph):
    results, columns = db.cypher_query("match(license:LicenseModel {{hashed_sets:'{}'}})-[:Compatible *0..]->(comp_license:LicenseModel) WHERE license.graph = '{}' RETURN distinct comp_license".format(hashed_sets, graph))
    return [LicenseModel().inflate(row[0]) for row in results]


def get_compliant_licenses(hashed_sets, graph):
    results, columns = db.cypher_query("match(license:LicenseModel {{hashed_sets:'{}'}})<-[:Compatible *0..]-(comp_license:LicenseModel) WHERE license.graph = '{}' RETURN distinct comp_license".format(hashed_sets, graph))
    return [LicenseModel().inflate(row[0]) for row in results]


class DatasetModel(StructuredNode):
    label = StringProperty(index=True)
    description = StringProperty()
    uri = StringProperty(unique_index=True)
    hashed_uri = StringProperty(unique_index=True)
    graph = StringProperty(index=True)

    license = RelationshipFrom("LicenseModel", "Protects")


def dataset_filter_search(query, graph):
    results, columns = db.cypher_query("match(dataset:DatasetModel) WHERE (dataset.label CONTAINS '{query}' OR dataset.description CONTAINS '{query}' OR dataset.uri CONTAINS '{query}') AND dataset.graph = '{graph}' RETURN dataset"
                                       .format(query=query, graph=graph))
    return [DatasetModel().inflate(row[0]) for row in results]
