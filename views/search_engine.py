import json

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from neomodels.NeoModels import get_compatible_licenses, get_compliant_licenses
from neomodels import ObjectFactory


@require_http_methods(['GET'])
def index(request):
    return render(request, 'index.html')


@require_http_methods(['GET'])
def graph(request):
    return render(request, 'graph.html')


@require_http_methods(['GET'])
def api(request):
    return render(request, 'doc.html')


@require_http_methods(['GET'])
def about(request):
    return render(request, 'about.html')


@require_http_methods(['GET'])
def search(request):
    query = request.GET.get('query', '')
    hashed_sets = request.GET.get('license', '')
    sens = request.GET.get('sens', '')
    keywords = query.split()
    results = []
    if sens == 'compatible':
        neo_licenses = get_compliant_licenses(hashed_sets)
    else:
        neo_licenses = get_compatible_licenses(hashed_sets)
    for neo_license in neo_licenses:
        license_object = ObjectFactory.objectLicense(neo_license)
        if keywords:
            license_object = query_filter(license_object, keywords)
        if license_object:
            results.append(license_object.to_json())
    return render(request, 'search.html', {'results': json.dumps(results), 'nb_datasets': nb_datasets(results)})


def query_filter(license_object, keywords):
    license_contains_keyword = False
    for dataset in license_object.datasets:
        dataset_contains_keyword = False
        for keyword in keywords:
            if keyword in dataset.label or keyword in dataset.description:
                dataset_contains_keyword = True
                license_contains_keyword = True
                break
        if not dataset_contains_keyword:
            license_object.datasets.remove(dataset)
    if license_contains_keyword:
        return license_object
    else:
        return None


def nb_datasets(results):
    nb_datasets = 0
    for license in results:
        nb_datasets += len(license['datasets'])
    return nb_datasets
