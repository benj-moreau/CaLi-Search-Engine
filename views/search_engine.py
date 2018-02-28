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
def search(request):
    query = request.GET.get('query', '')
    hashed_sets = request.GET.get('license', '')
    sens = request.GET.get('sens', '')
    keywords = query.split()
    results = []
    if sens == 'compliant':
        neo_licenses = get_compliant_licenses(hashed_sets)
    else:
        neo_licenses = get_compatible_licenses(hashed_sets)
    print neo_licenses
    for neo_license in neo_licenses:
        license_object = ObjectFactory.objectLicense(neo_license)
        if keywords:
            license_object = query_filter(license_object, keywords)
        if license_object:
            results.append(license_object.to_json())
    return render(request, 'search.html', {'results': results})


def query_filter(license_object, keywords):
    contains_keyword = False
    for dataset in license_object.datasets:
        for keyword in keywords:
            if keyword in dataset.label or keyword in dataset.description:
                contains_keyword = True
            else:
                license_object.datasets.remove(dataset)
    if contains_keyword:
        return license_object
    else:
        return None
