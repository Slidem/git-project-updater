def is_valid_project_type(type):
    """ Validates supported project types; currently only maven is supported; hopefully gradle in the future """

    if not type:
        return False

    if "maven" != type:
        return False

    return True
