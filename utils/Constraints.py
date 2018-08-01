import utils.ODRL as ODRL


def is_license_viable(license):
    if not(license.permissions.isdisjoint(license.obligations) and license.permissions.isdisjoint(license.prohibitions) and license.obligations.isdisjoint(license.prohibitions)):
        return False
    return True


def is_compatibility_viable(license_i, license_j):
    if ODRL.SHARE_ALIKE in license_i.obligations:
        return False
    if ODRL.DERIVATIVE_WORKS in license_i.prohibitions:
        return False
    return True


def is_conformity_viable(license_i, license_j):
    return is_compatibility_viable(license_j, license_i)
