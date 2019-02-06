from neomodels.NeoModels import LicenseModel, DatasetModel


def NeoLicense(object_license, graph):
    return LicenseModel(labels=object_license.get_labels(),
                        licensing_terms=object_license.get_licensing_terms(),
                        permissions=object_license.get_permissions(),
                        obligations=object_license.get_obligations(),
                        prohibitions=object_license.get_prohibitions(),
                        hashed_sets=object_license.hash(),
                        graph=graph
                        )


def NeoDataset(object_dataset, graph):
    return DatasetModel(label=object_dataset.get_label(),
                        uri=object_dataset.get_uri(),
                        description=object_dataset.get_description(),
                        hashed_uri=object_dataset.hash(),
                        graph=graph
                        )
