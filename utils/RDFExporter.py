from rdflib import Graph, Namespace, Literal, URIRef, RDFS, RDF

LICENSE_SUBJECT = "http://cali.priloo.univ-nantes.fr/api/{}/licenses/{}"
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")


def get_rdf(licenses, graph):
    rdf_graph = Graph()
    rdf_graph.bind("odrl", ODRL)
    for license in licenses:
        subject = URIRef(LICENSE_SUBJECT.format(graph, license['hashed_sets']))
        rdf_graph.add((subject, RDF.type, ODRL['Policy']))
        for label in license.get('labels'):
            rdf_graph.add((subject, RDFS.label, Literal(label)))
        for action in license.get('permissions'):
            rdf_graph.add((subject, ODRL['permissions'], ODRL[action]))
        for action in license.get('prohibitions'):
            rdf_graph.add((subject, ODRL['prohibition'], ODRL[action]))
        for action in license.get('obligations'):
            rdf_graph.add((subject, ODRL['duty'], ODRL[action]))
        for resource in license.get('resources'):
            subject_resource = URIRef(resource['uri'])
            rdf_graph.add((subject_resource, RDF.type, ODRL['Asset']))
            rdf_graph.add((subject_resource, RDFS.label, Literal(resource.get('label'))))
            rdf_graph.add((subject_resource, RDFS.comment, Literal(resource.get('description'))))
            rdf_graph.add((subject_resource, ODRL['hasPolicy'], subject))
            rdf_graph.add((subject, ODRL['target'], subject_resource))
    return rdf_graph
