from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

from neomodel import UniqueProperty, DoesNotExist
import json

from objectmodels.Dataset import Dataset
from objectmodels.License import License
from neomodels import NeoFactory, ObjectFactory
from neomodels.NeoModels import LicenseModel, DatasetModel, license_filter_labels, dataset_filter_search, license_filter_sets


@require_http_methods(['GET', 'POST'])
def license_path(request):
    if request.method == 'GET':
        return get_licenses(request)
    elif request.method == 'POST':
        return add_license(request)


@require_http_methods(['GET', 'POST'])
def dataset_path(request):
    if request.method == 'GET':
        return get_datasets(request)
    elif request.method == 'POST':
        return add_dataset(request)


def get_licenses(request):
    response_content = []
    for neo_license in LicenseModel.nodes:
        license_object = ObjectFactory.objectLicense(neo_license)
        response_content.append(license_object.to_json())
    response = HttpResponse(
        json.dumps(response_content),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


def get_datasets(request):
    response_content = []
    for neo_dataset in DatasetModel.nodes:
        dataset_object = ObjectFactory.objectDataset(neo_dataset)
        response_content.append(dataset_object.to_json())
    response = HttpResponse(
        json.dumps(response_content),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


def add_license(request):
    json_license = json.loads(request.body)
    object_license = License()
    object_license.from_json(json_license)
    neo_license = LicenseModel.nodes.get_or_none(hashed_sets=object_license.hash())
    if neo_license:
        # update of labels list if needed
        neo_license.labels = list(set(object_license.get_labels()).union(neo_license.labels))
        neo_license.save()
    else:
        # license does not exists in db
        neo_license = NeoFactory.NeoLicense(object_license)
        neo_license.save()
    for dataset in object_license.get_datasets():
        neo_dataset = DatasetModel.nodes.get_or_none(hashed_uri=dataset.hash())
        if not neo_dataset:
            neo_dataset = NeoFactory.NeoDataset(dataset)
            neo_dataset.save()
        neo_license.datasets.connect(neo_dataset)
    object_license = ObjectFactory.objectLicense(neo_license)
    response = HttpResponse(
        json.dumps(object_license.to_json()),
        content_type='application/json',
        status=201,
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def add_dataset(request):
    json_dataset = json.loads(request.body)
    object_dataset = Dataset()
    object_dataset.from_json(json_dataset)
    neo_dataset = NeoFactory.NeoDataset(object_dataset)
    object_dataset = ObjectFactory.objectDataset(neo_dataset)
    try:
        neo_dataset.save()
        response = HttpResponse(
            json.dumps(object_dataset.to_json()),
            content_type='application/json',
            status=201,
        )
    except UniqueProperty:
        response = HttpResponse(
            json.dumps(object_dataset.to_json()),
            content_type='application/json',
            status=409,
        )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def get_license_by_hash(request, hashed_sets):
    try:
        neo_license = LicenseModel.nodes.get(hashed_sets=hashed_sets)
        license_object = ObjectFactory.objectLicense(neo_license)
        response = HttpResponse(
            json.dumps(license_object.to_json()),
            content_type='application/json')
    except DoesNotExist:
        response = HttpResponse(
            "{}",
            content_type='application/json',
            status=404,
        )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def get_dataset_by_hash(request, hashed_uri):
    try:
        neo_dataset = DatasetModel.nodes.get(hashed_uri=hashed_uri)
        dataset_object = ObjectFactory.objectDataset(neo_dataset)
        response = HttpResponse(
            json.dumps(dataset_object.to_json()),
            content_type='application/json')
    except DoesNotExist:
        response = HttpResponse(
            "{}",
            content_type='application/json',
            status=404,
        )
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_license_search(request):
    query = request.GET.get('query', None)
    label = request.GET.get('label', None)
    permissions = request.GET.get('permissions', None)
    if is_empty(permissions):
        permissions = None
    obligations = request.GET.get('obligations', None)
    if is_empty(obligations):
        obligations = None
    prohibitions = request.GET.get('prohibitions', None)
    if is_empty(prohibitions):
        prohibitions = None
    neo_licenses = LicenseModel.nodes
    if query:
        neo_licenses = license_filter_labels(query)
    else:
        if label:
            neo_licenses = license_filter_labels(label)
        if permissions:
            neo_licenses = license_filter_sets(permissions, 'permissions')
        if obligations:
            neo_licenses = license_filter_sets(obligations, 'obligations')
        if prohibitions:
            neo_licenses = license_filter_sets(prohibitions, 'prohibitions')
    response_content = []
    for neo_license in neo_licenses:
        license_object = ObjectFactory.objectLicense(neo_license)
        response_content.append(license_object.to_json())
    response = HttpResponse(
        json.dumps(response_content),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_dataset_search(request):
    query = request.GET.get('query', None)
    label = request.GET.get('label', None)
    descr = request.GET.get('descr', None)
    uri = request.GET.get('uri', None)
    neo_datasets = DatasetModel.nodes
    if query:
        neo_datasets = dataset_filter_search(query)
    else:
        if label:
            neo_datasets = neo_datasets.filter(label__icontains=label)
        if uri:
            neo_datasets = neo_datasets.filter(uri__icontains=uri)
        if descr:
            neo_datasets = neo_datasets.filter(description__icontains=descr)
    response_content = []
    for neo_dataset in neo_datasets:
        dataset_object = ObjectFactory.objectDataset(neo_dataset)
        response_content.append(dataset_object.to_json())
    response = HttpResponse(
        json.dumps(response_content),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_datasets_of_licenses(request, hashed_sets):
    try:
        neo_license = LicenseModel.nodes.get(hashed_sets=hashed_sets)
        license_datasets = []
        for dataset in neo_license.datasets.all():
            dataset_object = ObjectFactory.Dataset(dataset)
            license_datasets.append(dataset_object.to_json())
        response = HttpResponse(
            json.dumps(license_datasets),
            content_type='application/json')
    except DoesNotExist:
        response = HttpResponse(
            "[]",
            content_type='application/json',
            status=404,
        )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def is_empty(str_list):
    if str_list is not None:
        if str_list.replace(' ', '').replace('[', '').replace(']', '').split(',')[0] == '':
            return True
    return False
