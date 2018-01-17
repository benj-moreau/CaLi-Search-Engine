from neomodel import StructuredNode, ArrayProperty, StringProperty, RelationshipFrom, RelationshipTo


# DAO. Objects used to access data in neo4j database
class LicenseModel(StructuredNode):
    labels = ArrayProperty()
    permissions = ArrayProperty(index=True)
    obligations = ArrayProperty(index=True)
    prohibitions = ArrayProperty(index=True)

    childs = RelationshipTo("LicenseModel", "Composes")
    parents = RelationshipFrom("LicenseModel", "ComposedBy")
    datasets = RelationshipTo("DatasetModel", "ApplyTo")


class DatasetModel(StructuredNode):
    label = StringProperty(index=True)
    description = StringProperty()
    uri = StringProperty()

    license = RelationshipFrom("LicenseModel", "ApplyTo")