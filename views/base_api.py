from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from neomodel import UniqueProperty, DoesNotExist
import json

from objectmodels.Dataset import Dataset
from objectmodels.License import License
from neomodels import NeoFactory, ObjectFactory
from neomodels.NeoModels import LicenseModel, DatasetModel


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
    neo_license = NeoFactory.neoLicense(object_license)
    object_license = ObjectFactory.objectLicense(neo_license)
    try:
        neo_license.save()
        response = HttpResponse(
            json.dumps(object_license.to_json()),
            content_type='application/json',
            status=201,
        )
        response['Access-Control-Allow-Origin'] = '*'
    except UniqueProperty:
        response = HttpResponse(
            json.dumps(object_license.to_json()),
            content_type='application/json',
            status=409,
        )
        response['Access-Control-Allow-Origin'] = '*'
    return response


def add_dataset(request):
    json_dataset = json.loads(request.body)
    object_dataset = Dataset()
    object_dataset.from_json(json_dataset)
    neo_dataset = NeoFactory.neoDataset(object_dataset)
    object_dataset = ObjectFactory.objectDataset(neo_dataset)
    try:
        neo_dataset.save()
        response = HttpResponse(
            json.dumps(object_dataset.to_json()),
            content_type='application/json',
            status=201,
        )
        response['Access-Control-Allow-Origin'] = '*'
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
        response['Access-Control-Allow-Origin'] = '*'
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
        response['Access-Control-Allow-Origin'] = '*'
    except DoesNotExist:
        response = HttpResponse(
            "{}",
            content_type='application/json',
            status=404,
        )
        response['Access-Control-Allow-Origin'] = '*'
    return response
