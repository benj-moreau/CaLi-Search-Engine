def license_node(object_license):
    return {
        'labels': object_license.get_labels(),
        'permissions': object_license.get_permissions(),
        'obligations': object_license.get_obligations(),
        'prohibitions': object_license.get_prohibitions(),
        'hashed_sets': str(object_license.hash()),
        'group': 1
    }


def compatible_link(object_license, compatible_object_license):
    return {"source": str(object_license.hash()), "target": str(compatible_object_license.hash()), "value": 1}


def dataset_node(object_dataset):
    return {
        'label': object_dataset.get_label(),
        'uri': object_dataset.get_uri(),
        'description': object_dataset.get_description(),
        'group': 2,
    }


def dataset_link(object_license, object_dataset):
    return {"source": str(object_license.hash()), "target": str(object_dataset.get_uri()), "value": 2}


def graph(nodes, links):
    return {'nodes': nodes, 'links': links}
