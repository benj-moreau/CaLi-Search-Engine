var api_doc = new Vue({
  el: '#doc',
  data: {
    api: [
      {
        'method': 'GET',
        'path': 'api/[classification]/resources',
        'params': [{'name': '[classification]', 'descr': 'classification \'ld\' or \'rep\''}],
        'descr': 'Retrieve all resources'
      },
      {
        'method': 'GET',
        'path': 'api/[classification]/resources/[id]',
        'params': [{'name': '[classification]', 'descr': 'classification \'ld\' or \'rep\''},
                   {'name': '[id]', 'descr': 'The id of the dataset'}],
        'descr': 'Retrieve a specific resource using dataset\'s id'
      },
      {
        'method': 'GET',
        'path': 'api/[classification]/resources/search',
        'params': [{'name': '[classification]', 'descr': 'classification \'ld\' or \'rep\''},
                   {'name': 'query', 'descr': 'FullText search in every dataset\'s attribute'},
                   {'name': 'label', 'descr': 'FullText search in label attribute'},
                   {'name': 'descr', 'descr': 'FullText search in description attribute'},
                   {'name': 'uri', 'descr': 'FullText search in uri attribute'}
                  ],
        'descr': 'Retrieve resources using FullText search'
      },
      {
        'method': 'GET',
        'path': 'api/[classification]/licenses',
        'params': [{'name': '[classification]', 'descr': 'classification \'ld\' or \'rep\''}],
        'descr': 'Retrieve all licenses'
      },
      {
        'method': 'GET',
        'path': 'api/[classification]/licenses/[id]',
        'params': [{'name': '[classification]', 'descr': 'classification \'ld\' or \'rep\''},
                   {'name': '[id]', 'descr': 'The id of the license'}],
        'descr': 'Retrieve a specific license using license id'
      },
      {
        'method': 'GET',
        'path': 'api/[classification]/licenses/[id]/compatible',
        'params': [{'name': '[classification]', 'descr': 'classification \'ld\' or \'rep\''},
                   {'name': '[id]', 'descr': 'The id of the license'}],
        'descr': 'Retrieve all licenses that are compatible with a specific license using the id of the license'
      },
      {
        'method': 'GET',
        'path': 'api/[classification]/licenses/[id]/compliant',
        'params': [{'name': '[classification]', 'descr': 'classification \'ld\' or \'rep\''},
                   {'name': '[id]', 'descr': 'The id of the license'}],
        'descr': 'Retrieve all licenses that are compliant with a specific license using the id of the license'
      },
      {
        'method': 'GET',
        'path': 'api/[classification]/licenses/[id]/resources',
        'params': [{'name': '[classification]', 'descr': 'classification \'ld\' or \'rep\''},
                   {'name': '[id]', 'descr': 'The id of the license'}],
        'descr': 'Retrieve resources licensed under a specific license using the id of the license'
      },
      {
        'method': 'GET',
        'path': 'api/[classification]/licenses/graph',
        'params': [{'name': '[classification]', 'descr': 'classification \'ld\' or \'rep\''}],
        'descr': 'Retrieve the subgraph of the lattice in JSON format'
      },
      {
        'method': 'GET',
        'path': 'api/[classification]/licenses/search',
        'params': [{'name': '[classification]', 'descr': 'classification \'ld\' or \'rep\''},
                   {'name': 'query', 'descr': 'FullText search in every license\'s attribute'},
                   {'name': 'label', 'descr': 'FullText search in label attribute'},
                   {'name': 'permissions', 'descr': 'A set of action contained in the license permissions set'},
                   {'name': 'obligations', 'descr': 'A set of action contained in the license obligations set'},
                   {'name': 'prohibitions', 'descr': 'A set of action contained in the license prohibitions set'}
                  ],
        'descr': 'Search API to retrieve specific licenses and licensed resource\'s'
      },
      {
        'method': 'GET',
        'path': 'api/[classification]/exports/[format]',
        'params': [{'name': '[classification]', 'descr': 'classification \'ld\' or \'rep\''},
                   {'name': '[format]', 'descr': 'rdf serialization format: \'n3\', \'nt\', \'xml\', \'turtle\', \'json-ld\''}],
        'descr': 'Export classification in RDF. Licenses are described using ODRL vocabulary'
      },
      {
        'method': 'GET',
        'path': 'api/[classification]/tpf',
        'params': [{'name': '[classification]', 'descr': 'classification \'ld\' or \'rep\''},
                   {'name': 'subject', 'descr': 'The subject of the triple pattern query (URI)'},
                   {'name': 'predicate', 'descr': 'The predicate of the triple pattern query (URI)'},
                   {'name': 'object', 'descr': 'The object of the triple pattern query (URI or Term)'},
                   {'name': 'page', 'descr': 'The page number of the result that will be returned (Integer)'},
                  ],
        'descr': 'Triple Pattern Fragments endpoint to query the graph. Use a TPF or Comunica client to execute SPARQL queries'
      },
    ],
  },
});
