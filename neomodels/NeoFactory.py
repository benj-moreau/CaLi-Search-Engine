from neomodels.NeoModels import LicenseModel, DatasetModel


def neoLicense(object_license):
    return LicenseModel(labels=object_license.get_labels(),
                        permissions=object_license.get_permissions(),
                        obligations=object_license.get_obligations(),
                        prohibitions=object_license.get_prohibitions(),
                        hashed_sets=object_license.hash()
                        )


def neoDataset(object_dataset):
    return DatasetModel(label=object_dataset.get_label(),
                        uri=object_dataset.get_uri(),
                        description=object_dataset.get_description(),
                        hashed_uri=object_dataset.hash()
                        )
