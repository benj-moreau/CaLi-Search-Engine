var api_doc = new Vue({
  el: '#doc',
  data: {
    api: [
      {
        'method': 'GET',
        'path': 'api/datasets',
        'params': null,
        'descr': 'Retrieve all datasets'
      },
      {
        'method': 'GET',
        'path': 'api/datasets/[id]',
        'params': [{'name': '[id]', 'descr': 'The id of the dataset'}],
        'descr': 'Retrieve a specific dataset using dataset\'s id'
      },
      {
        'method': 'GET',
        'path': 'api/datasets/search',
        'params': [{'name': 'query', 'descr': 'FullText search in every dataset\'s attribute'},
                   {'name': 'label', 'descr': 'FullText search in label attribute'},
                   {'name': 'descr', 'descr': 'FullText search in description attribute'},
                   {'name': 'uri', 'descr': 'FullText search in uri attribute'}

                  ],
        'descr': 'Retrieve datasets using FullText search'
      },
      {
        'method': 'GET',
        'path': 'api/licenses',
        'params': null,
        'descr': 'Retrieve all licensed datasets'
      },
      {
        'method': 'GET',
        'path': 'api/licenses/[id]',
        'params': [{'name': '[id]', 'descr': 'The id of the license'}],
        'descr': 'Retrieve a specific license using license id'
      },
      {
        'method': 'GET',
        'path': 'api/licenses/[id]/compatible',
        'params': [{'name': '[id]', 'descr': 'The id of the license'}],
        'descr': 'Retrieve all licenses that are compliant with a specific license using the id of the license'
      },
      {
        'method': 'GET',
        'path': 'api/licenses/[id]/compliant',
        'params': [{'name': '[id]', 'descr': 'The id of the license'}],
        'descr': 'Retrieve all licenses that are compliant with a specific license using the id of the license'
      },
      {
        'method': 'GET',
        'path': 'api/licenses/[id]/datasets',
        'params': [{'name': '[id]', 'descr': 'The id of the license'}],
        'descr': 'Retrieve datasets licensed under a specific license using the id of the license'
      },
      {
        'method': 'GET',
        'path': 'api/licenses/graph',
        'params': null,
        'descr': 'Retrieve the subgraph of the lattice in JSON format'
      },
      {
        'method': 'GET',
        'path': 'api/licenses/search',
        'params': [{'name': 'query', 'descr': 'FullText search in every license\'s attribute'},
                   {'name': 'label', 'descr': 'FullText search in label attribute'},
                   {'name': 'permissions', 'descr': 'A set of action contained in the license permissions set'},
                   {'name': 'obligations', 'descr': 'A set of action contained in the license obligations set'},
                   {'name': 'prohibitions', 'descr': 'A set of action contained in the license prohibitions set'}
                  ],
        'descr': 'Search API to retrieve specific licenses and licensed dataset\'s'
      }
    ],
  },
});
