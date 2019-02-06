from urllib import urlencode
from urlparse import urlparse
from rdflib import Graph, Namespace, Literal, URIRef, RDFS, RDF, Dataset, BNode, XSD
from neomodels.NeoModels import LicenseModel
from neomodels import ObjectFactory

LICENSE_SUBJECT = "http://cali.priloo.univ-nantes.fr/api/{}/licenses/{}"
LICENSE_SUBJECT_PREFIX = "http://cali.priloo.univ-nantes.fr/api/"

ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
ODRS = Namespace("http://schema.theodi.org/odrs#")
HYDRA = Namespace("http://www.w3.org/ns/hydra/core#")
VOID = Namespace("http://rdfs.org/ns/void#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
PROV = Namespace("http://www.w3.org/ns/prov#")
PURL = Namespace('http://purl.org/dc/terms/')
L4LOD = Namespace('http://ns.inria.fr/l4lod/v2/')

TPF_URL = '{}://{}/api/{}/tpf/'


def get_rdf(licenses, graph):
    rdf_graph = Graph()
    rdf_graph.bind("odrl", ODRL)
    rdf_graph.bind("odrs", ODRS)
    rdf_graph.bind('l4lod', L4LOD)
    for license in licenses:
        subject = URIRef(LICENSE_SUBJECT.format(graph, license['hashed_sets']))
        rdf_graph.add((subject, RDF.type, ODRL['Policy']))
        for label in license.get('labels'):
            rdf_graph.add((subject, RDFS.label, Literal(label)))
        for licensing_term in license.get('licensing_terms'):
            try:
                licensing_term = URIRef(licensing_term)
                rdf_graph.add((subject, L4LOD['licensingTerms'], licensing_term))
            except Exception:
                pass
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
        for compatible_license in license.get('compatible_licenses'):
            object_resource = URIRef(LICENSE_SUBJECT.format(graph, compatible_license))
            rdf_graph.add((subject, ODRS['compatibleWith'], object_resource))
    return rdf_graph


def get_fragment(request, subject, predicate, obj, page, graph):
    fragment = Dataset()
    tpf_url = urlparse(request.build_absolute_uri())
    tpf_url = TPF_URL.format(tpf_url.scheme, tpf_url.netloc, graph)
    licenses = []
    neo_licenses = LicenseModel.nodes.filter(graph__exact=graph)
    if subject and subject.startswith(LICENSE_SUBJECT_PREFIX):
        license_id = subject.split('/')[-1]
        neo_licenses.filter(hashed_sets__exact=license_id)
    for neo_license in neo_licenses:
        license_object = ObjectFactory.objectLicense(neo_license)
        license_object = license_object.to_json()
        license_object['compatible_licenses'] = []
        for compatible_neo_license in neo_license.followings.all():
            compatible_license = ObjectFactory.objectLicense(compatible_neo_license)
            license_object['compatible_licenses'].append(compatible_license.hash())
        licenses.append(license_object)
    rdf_licenses = get_rdf(licenses, graph).triples((subject, predicate, obj))
    total_nb_triples = 0
    for s, p, o in rdf_licenses:
        fragment.add((s, p, o))
        total_nb_triples += 1
    last_result = True
    nb_triple_per_page = total_nb_triples
    _frament_fill_meta(subject, predicate, obj, page, graph, fragment, last_result, total_nb_triples, nb_triple_per_page, request, tpf_url)
    return fragment


def _frament_fill_meta(subject, predicate, obj, page, graph, fragment, last_result, total_nb_triples, nb_triple_per_page, request, tpf_url):
    meta_graph = _tpf_uri(tpf_url, 'metadata')
    fragment.add_graph(meta_graph)
    dataset_base = _tpf_uri(tpf_url)
    source = URIRef(request.build_absolute_uri())
    dataset_template = Literal('%s%s' % (dataset_base, '{?subject,predicate,object}'))
    data_graph = _tpf_uri(tpf_url, 'dataset')
    tp_node = BNode('triplePattern')
    subject_node = BNode('subject')
    predicate_node = BNode('predicate')
    object_node = BNode('object')

    fragment.add((meta_graph, FOAF['primaryTopic'], dataset_base, meta_graph))
    fragment.add((data_graph, HYDRA['member'], data_graph, meta_graph))
    fragment.add((data_graph, RDF.type, VOID['Dataset'], meta_graph))
    fragment.add((data_graph, RDF.type, HYDRA['Collection'], meta_graph))
    fragment.add((data_graph, VOID['subset'], dataset_base, meta_graph))
    fragment.add((data_graph, VOID['uriLookupEndpoint'], dataset_template, meta_graph))
    fragment.add((data_graph, HYDRA['search'], tp_node, meta_graph))
    fragment.add((tp_node, HYDRA['template'], dataset_template, meta_graph))
    fragment.add((tp_node, HYDRA['variableRepresentation'], HYDRA['ExplicitRepresentation'], meta_graph))
    fragment.add((tp_node, HYDRA['mapping'], subject_node, meta_graph))
    fragment.add((tp_node, HYDRA['mapping'], predicate_node, meta_graph))
    fragment.add((tp_node, HYDRA['mapping'], object_node, meta_graph))
    fragment.add((subject_node, HYDRA['variable'], Literal("subject"), meta_graph))
    fragment.add((subject_node, HYDRA['property'], RDF.subject, meta_graph))
    fragment.add((predicate_node, HYDRA['variable'], Literal("predicate"), meta_graph))
    fragment.add((predicate_node, HYDRA['property'], RDF.predicate, meta_graph))
    fragment.add((object_node, HYDRA['variable'], Literal("object"), meta_graph))
    fragment.add((object_node, HYDRA['property'], RDF.object, meta_graph))

    fragment.add((dataset_base, VOID['subset'], source, meta_graph))
    fragment.add((source, RDF.type, HYDRA['PartialCollectionView'], meta_graph))
    fragment.add((source, DCTERMS['title'], Literal("CaLi TPF endpoint"), meta_graph))
    fragment.add((source, DCTERMS['description'], Literal("Triples from the CaLi TPF endpoint matching the pattern {?s=%s, ?p=%s, ?o=%s}" % (subject, predicate, obj)), meta_graph))
    fragment.add((source, DCTERMS['source'], data_graph, meta_graph))
    fragment.add((source, HYDRA['totalItems'], Literal(total_nb_triples, datatype=XSD.int), meta_graph))
    fragment.add((source, VOID['triples'], Literal(total_nb_triples, datatype=XSD.int), meta_graph))
    fragment.add((source, HYDRA['itemsPerPage'], Literal(nb_triple_per_page, datatype=XSD.int), meta_graph))
    fragment.add((source, HYDRA['first'], _tpf_url(dataset_base, 1, subject, predicate, obj), meta_graph))

    fragment.add((source, RDF.type, PROV['Entity'], meta_graph))
    fragment.add((source, PROV['wasGeneratedBy'], URIRef("https://github.com/benjimor/CaLi/"), meta_graph))
    if page > 1:
        fragment.add((source, HYDRA['previous'], _tpf_url(dataset_base, page - 1, subject, predicate, obj), meta_graph))
    if not last_result:
        fragment.add((source, HYDRA['next'], _tpf_url(dataset_base, page + 1, subject, predicate, obj), meta_graph))
    fragment.bind('cali{}'.format(graph), Namespace("%s#" % tpf_url[:-1]))
    fragment.bind('void', VOID)
    fragment.bind('foaf', FOAF)
    fragment.bind('hydra', HYDRA)
    fragment.bind('purl', PURL)
    fragment.bind('prov', PROV)


def _tpf_uri(tpf_url, tag=None):
    if tag is None:
        return URIRef(tpf_url)
    return URIRef("%s%s" % (tpf_url[:-1], '#%s' % tag))


def _tpf_url(dataset_base, page, subject, predicate, obj):
    subject_parameter = subject if subject else ''
    predicate_parameter = predicate if predicate else ''
    if obj:
        if isinstance(obj, URIRef):
            object_parameter = obj
        else:
            object_parameter = ('"%s"^^%s' % (obj, obj._datatype))
    else:
        object_parameter = ''
    parameters = {'page': page, 'subject': subject_parameter, 'predicate': predicate_parameter, 'object': object_parameter}
    return URIRef("%s?%s" % (dataset_base, urlencode(parameters)))
