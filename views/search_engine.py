import json

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from neomodels.NeoModels import get_compatible_licenses, get_compliant_licenses
from neomodels import ObjectFactory
from utils import D3jsData


@require_http_methods(['GET'])
def ld_graph(request):
    return render(request, 'ld_graph.html')


@require_http_methods(['GET'])
def rep_graph(request):
    return render(request, 'rep_graph.html')


@require_http_methods(['GET'])
def ld_engine(request):
    return render(request, 'ld_engine.html')


@require_http_methods(['GET'])
def rep_engine(request):
    return render(request, 'rep_engine.html')


@require_http_methods(['GET'])
def api(request):
    return render(request, 'doc.html')


@require_http_methods(['GET'])
def about(request):
    return render(request, 'about.html')


@require_http_methods(['GET'])
def ld_search(request):
    graph = 'ld'
    query = request.GET.get('query', '')
    hashed_sets = request.GET.get('license', '')
    sens = request.GET.get('sens', '')
    keywords = query.split()
    results = []
    nodes = []
    links = []
    added_nodes = []
    if sens == 'compatible':
        neo_licenses = get_compliant_licenses(hashed_sets, graph)
    else:
        neo_licenses = get_compatible_licenses(hashed_sets, graph)
    for neo_license in neo_licenses:
        license_object = ObjectFactory.objectLicense(neo_license)
        if keywords:
            license_object = query_filter(license_object, keywords)
        if license_object.datasets:
            results.append(license_object.to_json())
        # we add license and datasets to the graph
        if license_object not in added_nodes:
            nodes.append(D3jsData.license_node(license_object))
            added_nodes.append(license_object)
        for dataset_object in license_object.datasets:
            nodes.append(D3jsData.dataset_node(dataset_object, license_object.get_level()))
            links.append(D3jsData.dataset_link(license_object, dataset_object))
        for compatible_neo_license in neo_license.followings.all():
            compatible_license_object = ObjectFactory.objectLicense(compatible_neo_license)
            if compatible_license_object not in added_nodes:
                nodes.append(D3jsData.license_node(compatible_license_object))
                added_nodes.append(compatible_license_object)
            links.append(D3jsData.compatible_link(license_object, compatible_license_object))
    return render(request, 'search.html', {'results': json.dumps(results), 'nb_datasets': nb_datasets(results), 'graph': json.dumps(D3jsData.graph(nodes, links))})


@require_http_methods(['GET'])
def rep_search(request):
    graph = 'rep'
    query = request.GET.get('query', '')
    hashed_sets = request.GET.get('license', '')
    sens = request.GET.get('sens', '')
    keywords = query.split()
    results = []
    nodes = []
    links = []
    added_nodes = []
    if sens == 'compatible':
        neo_licenses = get_compliant_licenses(hashed_sets, graph)
    else:
        neo_licenses = get_compatible_licenses(hashed_sets, graph)
    for neo_license in neo_licenses:
        license_object = ObjectFactory.objectLicense(neo_license)
        if keywords:
            license_object = query_filter(license_object, keywords)
        if license_object.datasets:
            results.append(license_object.to_json())
        # we add license and datasets to the graph
        if license_object not in added_nodes:
            nodes.append(D3jsData.license_node(license_object))
            added_nodes.append(license_object)
        for dataset_object in license_object.datasets:
            nodes.append(D3jsData.dataset_node(dataset_object, license_object.get_level()))
            links.append(D3jsData.dataset_link(license_object, dataset_object))
        for compatible_neo_license in neo_license.followings.all():
            compatible_license_object = ObjectFactory.objectLicense(compatible_neo_license)
            if compatible_license_object not in added_nodes:
                nodes.append(D3jsData.license_node(compatible_license_object))
                added_nodes.append(compatible_license_object)
            links.append(D3jsData.compatible_link(license_object, compatible_license_object))
    return render(request, 'search.html', {'results': json.dumps(results), 'nb_datasets': nb_datasets(results), 'graph': json.dumps(D3jsData.graph(nodes, links))})


def query_filter(license_object, keywords):
    matching_datasets = []
    for dataset in license_object.datasets:
        for keyword in keywords:
            if keyword.lower() in dataset.label.lower() or keyword.lower() in dataset.description.lower():
                matching_datasets.append(dataset)
                break
    license_object.datasets = matching_datasets
    return license_object


def nb_datasets(results):
    nb_datasets = 0
    for license in results:
        nb_datasets += len(license['resources'])
    return nb_datasets
