"""cali_webservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url

from views import base_api, search_engine

urlpatterns = [
    # url(r'^api/', include('')),
    url(r'^api/licenses/graph/?$', base_api.get_graph, name='get_graph'),
    url(r'^api/licenses/(?P<hashed_sets>[\w_@-]+)/compatible/?$', base_api.get_compatible, name='get_compatible'),
    url(r'^api/licenses/(?P<hashed_sets>[\w_@-]+)/compliant/?$', base_api.get_compliant, name='get_compliant'),
    url(r'^api/licenses/(?P<hashed_sets>[\w_@-]+)/datasets/?$', base_api.get_datasets_of_licenses, name='get_datasets_of_licenses'),
    url(r'^api/licenses/search/?$', base_api.get_license_search, name='get_license_search'),
    url(r'^api/licenses/(?P<hashed_sets>[\w_@-]+)/?$', base_api.get_license_by_hash, name='get_license_by_hash'),
    url(r'^api/licenses/?$', base_api.license_path, name='licenses_path'),
    url(r'^api/datasets/search/?$', base_api.get_dataset_search, name='get_dataset_search'),
    url(r'^api/datasets/(?P<hashed_uri>[\w_@-]+)/?$', base_api.get_dataset_by_hash, name='get_dataset_by_hash'),
    url(r'^api/datasets/?$', base_api.dataset_path, name='dataset_path'),
    url(r'^graph/?$', search_engine.graph, name='graph'),
    url(r'', search_engine.index, name='index'),
]
