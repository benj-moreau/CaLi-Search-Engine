from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

from neomodel import UniqueProperty, DoesNotExist
from numpy import median
from copy import deepcopy
import json
import random
import time

from objectmodels.Dataset import Dataset
from objectmodels.License import License
from objectmodels.Lattice import Lattice
from neomodel import clear_neo4j_database, db
from neomodels import NeoFactory, ObjectFactory
from neomodels.NeoModels import LicenseModel, DatasetModel, license_filter_labels, dataset_filter_search, license_filter_sets
from neomodels.NeoModels import get_leaf_licenses, get_root_licenses, get_compliant_licenses, get_compatible_licenses
from utils.TimerDecorator import fn_timer, LOGGER
from utils.authentificator import need_auth
from utils import D3jsData
from utils import Constraints
from utils import Plot
from utils import LicenseGenerator
from utils import CSVExporter
from utils import ODRL

LEVELS_FILE = "license_levels.json"


@require_http_methods(['GET', 'POST', 'DELETE'])
def license_path(request):
    if request.method == 'GET':
        return get_licenses(request)
    elif request.method == 'POST':
        return add_license(request)
    elif request.method == 'DELETE':
        return delete_license(request)


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


@need_auth
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


@require_http_methods(['GET'])
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
            dataset_object = ObjectFactory.objectDataset(dataset)
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


@require_http_methods(['GET'])
@need_auth
@fn_timer
def add_license_experiment(request):
    structure = request.GET.get('structure', 'linear_order')
    order = request.GET.get('order', 'rand')
    limit = int(request.GET.get('limit', '144'))
    measure = request.GET.get('measure', 'time')
    nb_exec = int(request.GET.get('executions', '1'))
    aggregate = int(request.GET.get('aggregate', '1'))
    measure_array_inf = {}
    measure_array_supr = {}
    measure_arry_med = {}
    # We do not check viability
    # Add from the bottom
    lattice = Lattice(ODRL.ACTIONS)
    for i in range(0, nb_exec):
        LOGGER.info("infimum insertion begin")
        licenses = LicenseGenerator.generate(structure, order, limit)
        measure_array_inf[i] = []
        inf_times = []
        inf_nb_visits = []
        for j, license in enumerate(licenses):
            object_license = deepcopy(license)
            if j % 100 == 0:
                LOGGER.info("infimum: {}/{} classified".format(j, len(licenses)))
            t0 = time.time()
            nb_visit = add_license_to_lattice(object_license, lattice, method='infimum')
            t1 = time.time()
            if measure == 'time':
                measure_array_inf[i].append(t1-t0)
            else:
                measure_array_inf[i].append(nb_visit)
            inf_times.append(t1-t0)
            inf_nb_visits.append(nb_visit)
        # clear_neo4j_database(db)
        # add_lattice_to_db(lattice.get_infimum())
        LOGGER.info("infimum insertion end")
        lattice = Lattice(ODRL.ACTIONS)
        LOGGER.info("supremum insertion begin")
        # Add from the top
        measure_array_supr[i] = []
        supr_times = []
        supr_nb_visits = []
        for j, license in enumerate(licenses):
            object_license = deepcopy(license)
            if j % 100 == 0:
                LOGGER.info("supremum: {}/{} classified".format(j, len(licenses)))
            t0 = time.time()
            nb_visit = add_license_to_lattice(object_license, lattice, method='supremum')
            t1 = time.time()
            if measure == 'time':
                measure_array_supr[i].append(t1-t0)
            else:
                measure_array_supr[i].append(nb_visit)
            supr_times.append(t1-t0)
            supr_nb_visits.append(nb_visit)
        LOGGER.info("supremum insertion end")
        lattice = Lattice(ODRL.ACTIONS)
        LOGGER.info("median insertion begin")
        # from median
        license_levels = []
        level_median = 0
        measure_arry_med[i] = []
        med_times = []
        med_nb_visits = []
        for j, license in enumerate(licenses):
            object_license = deepcopy(license)
            if j % 100 == 0:
                LOGGER.info("median: {}/{} classified".format(j, len(licenses)))
            license_level = object_license.get_level()
            t0 = time.time()
            if license_levels:
                level_median = median(license_levels)
            if license_level > level_median:
                nb_visit = add_license_to_lattice(object_license, lattice, method='supremum', license_levels=license_levels)
            else:
                nb_visit = add_license_to_lattice(object_license, lattice, method='infimum', license_levels=license_levels)
            t1 = time.time()
            if measure == 'time':
                measure_arry_med[i].append(t1-t0)
            else:
                measure_arry_med[i].append(nb_visit)
            med_times.append(t1-t0)
            med_nb_visits.append(nb_visit)
        LOGGER.info("median insertion end")
        lattice = Lattice(ODRL.ACTIONS)
    CSVExporter.export(inf_times, inf_nb_visits, supr_times, supr_nb_visits, med_times, med_nb_visits, structure, order, limit, measure, nb_exec, aggregate)
    Plot.draw(measure_array_inf, measure_array_supr, measure_arry_med, structure, order, limit, measure, nb_exec, aggregate)
    response = HttpResponse(
        content_type='application/json',
        status=201,
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


@need_auth
def add_license(request):
    json_licenses = json.loads(request.body)
    added_licenses = []
    random.shuffle(json_licenses)
    license_levels = []
    level_median = 0
    try:
        with open(LEVELS_FILE, 'r') as f:
            license_levels = json.load(f)
    except IOError:
        pass
    for json_license in json_licenses:
        object_license = License()
        object_license.from_json(json_license)
        if object_license.contains_only_odrl_actions():
            if Constraints.is_license_viable(object_license):
                if license_levels:
                    level_median = median(license_levels)
                if object_license.get_level() > level_median:
                    object_license, nb_visit = add_license_to_db(object_license, method='supremum', license_levels=license_levels)
                else:
                    object_license, nb_visit = add_license_to_db(object_license, method='infimum', license_levels=license_levels)
                added_licenses.append(object_license.to_json())
            else:
                added_licenses.append("Not a valid license: License is non-viable")
        else:
            added_licenses.append("Not a valid license: Use only ODRL actions")
    with open(LEVELS_FILE, 'w') as outfile:
        json.dump(license_levels, outfile)
    response = HttpResponse(
        json.dumps(added_licenses),
        content_type='application/json',
        status=201,
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


def add_lattice_to_db(infimum):
    neo_infimum = LicenseModel.nodes.get_or_none(hashed_sets=infimum.hash())
    if not neo_infimum:
        neo_infimum = NeoFactory.NeoLicense(infimum)
        neo_infimum.save()
    for license_followers in infimum.followings:
        neo_follower = LicenseModel.nodes.get_or_none(hashed_sets=license_followers.hash())
        if not neo_follower:
            neo_follower = NeoFactory.NeoLicense(license_followers)
            neo_follower.save()
        neo_follower.precedings.connect(neo_infimum)
        add_lattice_to_db(license_followers)


def add_license_to_db(object_license, method='infimum', license_levels=[], viability_check=True, nb_visit=0):
    neo_license = LicenseModel.nodes.get_or_none(hashed_sets=object_license.hash())
    if neo_license:
        # update of labels list if needed
        neo_license.labels = list(set(object_license.get_labels()).union(neo_license.labels))
        neo_license.save()
    else:
        # license does not exists in db
        if method == 'infimum':
            neo_license, nb_visit = update_licenses_relations_infimum(object_license, viability_check, nb_visit)
        else:
            neo_license, nb_visit = update_licenses_relations_supremum(object_license, viability_check, nb_visit)
        license_levels.append(object_license.get_level())
    for dataset in object_license.get_datasets():
        neo_dataset = DatasetModel.nodes.get_or_none(hashed_uri=dataset.hash())
        if not neo_dataset:
            neo_dataset = NeoFactory.NeoDataset(dataset)
            neo_dataset.save()
        neo_license.datasets.connect(neo_dataset)
    object_license = ObjectFactory.objectLicense(neo_license)
    return object_license, nb_visit


def add_license_to_lattice(object_license, lattice, method='infimum', license_levels=[], nb_visit=0):
    # We consider that object_license is not in the lattice
    if method == 'infimum':
        nb_visit = update_licenses_relations_infimum_lattice(object_license, lattice, nb_visit)
    else:
        nb_visit = update_licenses_relations_supremum_lattice(object_license, lattice, nb_visit)
    license_levels.append(object_license.get_level())
    return nb_visit


def update_licenses_relations_infimum(object_license, viability_check, nb_visit):
    tested_licenses = [object_license]
    license_leaves = get_leaf_licenses()
    neo_license = NeoFactory.NeoLicense(object_license)
    neo_license.save()
    for neo_license_leaf in license_leaves:
        object_license_leaf = ObjectFactory.objectLicense(neo_license_leaf)
        if object_license.is_preceding(object_license_leaf) and (Constraints.is_compatibility_viable(object_license, object_license_leaf) or not viability_check):
            update_transitivity_follower(neo_license, object_license_leaf)
            neo_license_leaf.precedings.connect(neo_license)
        else:
            nb_visit = update_licenses_relations_infimum_rec(neo_license, object_license, neo_license_leaf, object_license_leaf, viability_check, nb_visit, tested_licenses)
    return neo_license, nb_visit


def update_licenses_relations_infimum_lattice(object_license, lattice, nb_visit):
    tested_licenses = [object_license]
    license_leaves = [lattice.get_infimum()]
    lattice.add_license(object_license)
    for object_license_leaf in license_leaves:
        if object_license.is_preceding(object_license_leaf):
            object_license_leaf.precedings.append(object_license)
            object_license.followings.append(object_license_leaf)
        else:
            nb_visit = update_licenses_relations_infimum_lattice_rec(object_license, object_license_leaf, lattice, nb_visit, tested_licenses)
    return nb_visit


def update_licenses_relations_supremum(object_license, viability_check, nb_visit):
    tested_licenses = [object_license]
    license_roots = get_root_licenses()
    neo_license = NeoFactory.NeoLicense(object_license)
    neo_license.save()
    for neo_license_root in license_roots:
        object_license_root = ObjectFactory.objectLicense(neo_license_root)
        if object_license.is_following(object_license_root) and (Constraints.is_compatibility_viable(object_license_root, object_license) or not viability_check):
            update_transitivity_preceder(neo_license, object_license_root)
            neo_license_root.followings.connect(neo_license)
        else:
            nb_visit = update_licenses_relations_supremum_rec(neo_license, object_license, neo_license_root, object_license_root, viability_check, nb_visit, tested_licenses)
    return neo_license, nb_visit


def update_licenses_relations_supremum_lattice(object_license, lattice, nb_visit):
    tested_licenses = [object_license]
    license_roots = [lattice.get_supremum()]
    lattice.add_license(object_license)
    for object_license_root in license_roots:
        if object_license.is_following(object_license_root):
            object_license_root.followings.append(object_license)
            object_license.precedings.append(object_license_root)
        else:
            nb_visit = update_licenses_relations_supremum_lattice_rec(object_license, object_license_root, lattice, nb_visit, tested_licenses)
    return nb_visit


def update_licenses_relations_infimum_rec(new_neo_license, new_object_license, neo_license, object_license, viability_check, nb_visit, tested_licenses):
    # update precedings and followings of license recursively.
    if object_license in tested_licenses:
        return nb_visit
    nb_visit += 1
    tested_licenses.append(object_license)
    grand_follower = False
    for neo_license_following in neo_license.followings:
        object_license_following = ObjectFactory.objectLicense(neo_license_following)
        if already_follower(object_license_following, new_neo_license):
            continue
        if new_object_license.is_preceding(object_license_following) and (Constraints.is_compatibility_viable(new_object_license, object_license_following) or not viability_check):
            update_transitivity_follower(new_neo_license, object_license_following)
            new_neo_license.followings.connect(neo_license_following)
            if new_object_license.is_following(object_license) and (Constraints.is_compatibility_viable(object_license, new_object_license) or not viability_check):
                new_neo_license.precedings.connect(neo_license)
                neo_license.followings.disconnect(neo_license_following)
        else:
            if new_object_license.is_following(object_license_following) and (Constraints.is_compatibility_viable(object_license_following, new_object_license) or not viability_check):
                grand_follower = True
            nb_visit = update_licenses_relations_infimum_rec(new_neo_license, new_object_license, neo_license_following, object_license_following, viability_check, nb_visit, tested_licenses)
    if not grand_follower and (new_object_license.is_following(object_license) and (Constraints.is_compatibility_viable(object_license, new_object_license) or not viability_check)):
        new_neo_license.precedings.connect(neo_license)
    return nb_visit


def update_licenses_relations_infimum_lattice_rec(new_object_license, object_license, lattice, nb_visit, tested_licenses):
    # update precedings and followings of license recursively.
    if object_license in tested_licenses:
        return nb_visit
    nb_visit += 1
    tested_licenses.append(object_license)
    grand_follower = False
    for object_license_following in object_license.get_followings():
        if already_follower_lattice(object_license_following, new_object_license) or object_license_following == new_object_license:
            continue
        if new_object_license.is_preceding(object_license_following):
            update_transitivity_follower_lattice(new_object_license, object_license_following)
            new_object_license.followings.append(object_license_following)
            object_license_following.precedings.append(new_object_license)
            if new_object_license.is_following(object_license):
                new_object_license.precedings.append(object_license)
                object_license.followings.append(new_object_license)
                object_license.followings.remove(object_license_following)
                object_license_following.precedings.remove(object_license)
        else:
            if new_object_license.is_following(object_license_following):
                grand_follower = True
            nb_visit = update_licenses_relations_infimum_lattice_rec(new_object_license, object_license_following, lattice, nb_visit, tested_licenses)
    if not grand_follower and new_object_license.is_following(object_license):
        new_object_license.precedings.append(object_license)
        object_license.followings.append(new_object_license)
    return nb_visit


def update_licenses_relations_supremum_lattice_rec(new_object_license, object_license, lattice, nb_visit, tested_licenses):
    # update precedings and followings of license recursively.
    if object_license in tested_licenses:
        return nb_visit
    nb_visit += 1
    tested_licenses.append(object_license)
    grand_preceder = False
    for object_license_preceding in object_license.get_precedings():
        if already_preceder_lattice(object_license_preceding, new_object_license) or object_license_preceding == new_object_license:
            continue
        if new_object_license.is_following(object_license_preceding):
            update_transitivity_preceder_lattice(new_object_license, object_license_preceding)
            new_object_license.precedings.append(object_license_preceding)
            object_license_preceding.followings.append(new_object_license)
            if new_object_license.is_preceding(object_license):
                new_object_license.followings.append(object_license)
                object_license.precedings.append(new_object_license)
                object_license.precedings.remove(object_license_preceding)
                object_license_preceding.followings.remove(object_license)
        else:
            if new_object_license.is_preceding(object_license_preceding):
                grand_preceder = True
            nb_visit = update_licenses_relations_supremum_lattice_rec(new_object_license, object_license_preceding, lattice, nb_visit, tested_licenses)
    if not grand_preceder and new_object_license.is_preceding(object_license):
        new_object_license.followings.append(object_license)
        object_license.precedings.append(new_object_license)
    return nb_visit


def update_licenses_relations_supremum_rec(new_neo_license, new_object_license, neo_license, object_license, viability_check, nb_visit, tested_licenses):
    # update precedings and followings of license recursively.
    if object_license in tested_licenses:
        return nb_visit
    nb_visit += 1
    tested_licenses.append(object_license)
    grand_preceder = False
    for neo_license_preceding in neo_license.precedings:
        object_license_preceding = ObjectFactory.objectLicense(neo_license_preceding)
        if already_preceder(object_license_preceding, new_neo_license):
            continue
        if new_object_license.is_following(object_license_preceding) and (Constraints.is_compatibility_viable(object_license_preceding, new_object_license) or not viability_check):
            update_transitivity_preceder(new_neo_license, object_license_preceding)
            new_neo_license.precedings.connect(neo_license_preceding)
            if new_object_license.is_preceding(object_license) and (Constraints.is_compatibility_viable(new_object_license, object_license) or not viability_check):
                new_neo_license.followings.connect(neo_license)
                neo_license.precedings.disconnect(neo_license_preceding)
        else:
            if new_object_license.is_preceding(object_license_preceding) and (Constraints.is_compatibility_viable(new_object_license, object_license_preceding) or not viability_check):
                grand_preceder = True
            nb_visit = update_licenses_relations_supremum_rec(new_neo_license, new_object_license, neo_license_preceding, object_license_preceding, viability_check, nb_visit, tested_licenses)
    if not grand_preceder and (new_object_license.is_preceding(object_license) and (Constraints.is_compatibility_viable(new_object_license, object_license) or not viability_check)):
        new_neo_license.followings.connect(neo_license)
    return nb_visit


def already_follower(object_license, new_neo_license):
    for neo_follower in new_neo_license.followings:
        object_follower = ObjectFactory.objectLicense(neo_follower)
        if object_license != object_follower and object_license.is_following(object_follower):
            return True
    return False


def already_follower_lattice(object_license, new_object_license):
    for object_follower in new_object_license.followings:
        if object_license != object_follower and object_license.is_following(object_follower):
            return True
    return False


def already_preceder(object_license, new_neo_license):
    for neo_preceder in new_neo_license.precedings:
        object_preceder = ObjectFactory.objectLicense(neo_preceder)
        if object_license != object_preceder and object_license.is_preceding(object_preceder):
            return True
    return False


def already_preceder_lattice(object_license, new_object_license):
    for object_preceder in new_object_license.precedings:
        if object_license != object_preceder and object_license.is_preceding(object_preceder):
            return True
    return False


def update_transitivity_follower(new_neo_license, new_object_follower):
    for neo_follower in new_neo_license.followings:
        object_follower = ObjectFactory.objectLicense(neo_follower)
        if object_follower.is_following(new_object_follower):
            new_neo_license.followings.disconnect(neo_follower)


def update_transitivity_follower_lattice(new_object_license, new_object_follower):
    for object_follower in new_object_license.followings:
        if object_follower.is_following(new_object_follower):
            new_object_license.followings.remove(object_follower)
            object_follower.precedings.remove(new_object_license)


def update_transitivity_preceder(new_neo_license, new_object_preceder):
    for neo_preceder in new_neo_license.precedings:
        object_preceder = ObjectFactory.objectLicense(neo_preceder)
        if object_preceder.is_preceding(new_object_preceder):
            new_neo_license.precedings.disconnect(neo_preceder)


def update_transitivity_preceder_lattice(new_object_license, new_object_preceder):
    for object_preceder in new_object_license.precedings:
        if object_preceder.is_preceding(new_object_preceder):
            new_object_license.precedings.remove(object_preceder)
            object_preceder.followings.remove(new_object_license)


@need_auth
def delete_license(request):
    clear_neo4j_database(db)
    try:
        with open(LEVELS_FILE, 'w') as outfile:
            json.dump([], outfile)
    except IOError:
        pass
    response = HttpResponse(
        '',
        content_type='application/json',
        status=200,
    )
    response['Access-Control-Allow-Origin'] = '*'
    return response


@fn_timer
@require_http_methods(['GET'])
def get_compliant(request, hashed_sets):
    try:
        neo_licenses = get_compatible_licenses(hashed_sets)
        compatible_licenses = []
        for neo_license in neo_licenses:
            license_object = ObjectFactory.objectLicense(neo_license)
            compatible_licenses.append(license_object.to_json())
        response = HttpResponse(
            json.dumps(compatible_licenses),
            content_type='application/json')
    except DoesNotExist:
        response = HttpResponse(
            "[]",
            content_type='application/json',
            status=404,
        )
    response['Access-Control-Allow-Origin'] = '*'
    return response


@fn_timer
@require_http_methods(['GET'])
def get_compatible(request, hashed_sets):
    try:
        neo_licenses = get_compliant_licenses(hashed_sets)
        compatible_licenses = []
        for neo_license in neo_licenses:
            license_object = ObjectFactory.objectLicense(neo_license)
            compatible_licenses.append(license_object.to_json())
        response = HttpResponse(
            json.dumps(compatible_licenses),
            content_type='application/json')
    except DoesNotExist:
        response = HttpResponse(
            "[]",
            content_type='application/json',
            status=404,
        )
    response['Access-Control-Allow-Origin'] = '*'
    return response


@fn_timer
@require_http_methods(['GET'])
def get_graph(request):
    nodes = []
    links = []
    for neo_license in LicenseModel.nodes:
        license_object = ObjectFactory.objectLicense(neo_license)
        nodes.append(D3jsData.license_node(license_object))
        license_level = license_object.get_level()
        for neo_dataset in neo_license.datasets.all():
            dataset_object = ObjectFactory.objectDataset(neo_dataset)
            nodes.append(D3jsData.dataset_node(dataset_object, license_level))
            links.append(D3jsData.dataset_link(license_object, dataset_object))
        for compatible_neo_license in neo_license.followings.all():
            compatible_license_object = ObjectFactory.objectLicense(compatible_neo_license)
            links.append(D3jsData.compatible_link(license_object, compatible_license_object))
    response = HttpResponse(
        json.dumps(D3jsData.graph(nodes, links)),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response
