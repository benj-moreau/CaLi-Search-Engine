# DB schema updated during run-server
from neomodel import install_labels
from neomodels.NeoModels import DatasetModel, LicenseModel

install_labels(DatasetModel)
install_labels(LicenseModel)
