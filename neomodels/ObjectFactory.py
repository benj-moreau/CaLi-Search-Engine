from objectmodels.License import License
from objectmodels.Dataset import Dataset


def objectLicense(neo_license):
    return License(labels=neo_license.labels,
                   permissions=set(neo_license.permissions),
                   obligations=set(neo_license.obligations),
                   prohibitions=set(neo_license.prohibitions),
                   datasets=[]
                   )


def objectDataset(neo_dataset):
    return Dataset(label=neo_dataset.label,
                   uri=neo_dataset.uri,
                   description=neo_dataset.description
                   )
