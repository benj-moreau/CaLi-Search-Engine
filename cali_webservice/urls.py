from django.conf.urls import url

from views import base_api, search_engine

urlpatterns = [
    url(r'^api/(?P<graph>[\w_@-]+)/licenses/graph/?$', base_api.get_graph, name='get_graph'),
    url(r'^api/(?P<graph>[\w_@-]+)/licenses/(?P<hashed_sets>[\w_@-]+)/compatible/?$', base_api.get_compatible, name='get_compatible'),
    url(r'^api/(?P<graph>[\w_@-]+)/licenses/(?P<hashed_sets>[\w_@-]+)/compliant/?$', base_api.get_compliant, name='get_compliant'),
    url(r'^api/(?P<graph>[\w_@-]+)/licenses/(?P<hashed_sets>[\w_@-]+)/datasets/?$', base_api.get_datasets_of_licenses, name='get_datasets_of_licenses'),
    url(r'^api/(?P<graph>[\w_@-]+)/licenses/search/?$', base_api.get_license_search, name='get_license_search'),
    url(r'^api/(?P<graph>[\w_@-]+)/licenses/(?P<hashed_sets>[\w_@-]+)/?$', base_api.get_license_by_hash, name='get_license_by_hash'),
    url(r'^api/(?P<graph>[\w_@-]+)/licenses/?$', base_api.license_path, name='licenses_path'),
    url(r'^api/(?P<graph>[\w_@-]+)/resources/search/?$', base_api.get_dataset_search, name='get_dataset_search'),
    url(r'^api/(?P<graph>[\w_@-]+)/resources/(?P<hashed_uri>[\w_@-]+)/?$', base_api.get_dataset_by_hash, name='get_dataset_by_hash'),
    url(r'^api/(?P<graph>[\w_@-]+)/exports/(?P<serialization_format>[\w_@-]+)/?$', base_api.export_licenses, name='export_licenses'),
    url(r'^api/(?P<graph>[\w_@-]+)/resources/?$', base_api.dataset_path, name='dataset_path'),
    url(r'^api/(?P<graph>[\w_@-]+)/tpf/?$', base_api.tpf_endpoint, name='tpf_endpoint'),
    url(r'^api/licenses/experiment/algo?$', base_api.quadratic_experiment, name='quadratic_experiment'),
    url(r'^api/licenses/experiment/?$', base_api.add_license_experiment, name='experiment'),
    url(r'^ld/graph/?$', search_engine.ld_graph, name='ldgraph'),
    url(r'^ld/search?$', search_engine.ld_search, name='ldsearch'),
    url(r'^ld/?$', search_engine.ld_engine, name='ldengine'),
    url(r'^rep/graph/?$', search_engine.rep_graph, name='repgraph'),
    url(r'^rep/search?$', search_engine.rep_search, name='repsearch'),
    url(r'^rep/?$', search_engine.rep_engine, name='repengine'),
    url(r'^api/?$', search_engine.api, name='api'),
    url(r'^about/?$', search_engine.about, name='about'),
    url(r'^publi/?$', search_engine.publi, name='publi'),
    url(r'^ontology/?$', base_api.get_cali_ontology, name='ontology'),
    url(r'', search_engine.about, name='index'),
]
