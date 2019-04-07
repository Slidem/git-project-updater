from pathlib import Path
from git_project_updater_business.models.project_details import ProjectDetails
from git_project_updater_business.settings.settings import Settings


def validate_string(str_argument, str_argument_name):
    """ Validates if the given argument is of type string and returns it"""
    if not isinstance(str_argument, str):
        raise ValueError(
            "Illegal str argument: {argument_name}".format(argument_name=str_argument_name))
    return str_argument


def validate_and_get_new_list(list_argument, list_argument_type, list_argument_name):
    """ Validates if the given argument is of type list and if all elements in the list are of list_argument_type.
        Returns a new copy of the list (shallow copy).
    """

    if not isinstance(list_argument, list):
        raise ValueError("Illegal list argument: {argument_name}".format(
            argument_name=list_argument_name))

    if not list_argument:
        return list_argument

    list_copy = []

    for index, param in enumerate(list_argument):
        if not isinstance(param, list_argument_type):
            invalid_type = type(param)
            raise ValueError(
                """Illegal list argument ({argument_name}), with invalid element types.
                   Expected type: {list_argument_type} ,
                   but got type {invalid_type} at index {index}"""
                .format(
                    argument_name=list_argument_name,
                    list_argument_type=list_argument_type,
                    invalid_type=invalid_type,
                    index=index)
            )
        list_copy.append(param)
    return list_copy


def validate_path(path_argument, path_argument_name):
    """ Validates if the given argument is of type Path"""
    if not isinstance(path_argument, Path):
        raise ValueError("Illegal str argument: {argument_name}".format(
            argument_name=path_argument_name))
    return path_argument


def validate_details(details_argument, details_argument_name):
    """ Validates if the given argument is of type ProjectDetails"""

    if not isinstance(details_argument, ProjectDetails):
        raise ValueError("Illegal details argument: {argument_name}".format(
            argument_name=details_argument_name))

    return details_argument


def validate_settings(settings_argument):
    """ Validates if the given argument is of type ProjectDetails"""

    if not isinstance(settings_argument, Settings):
        raise ValueError("Illegal settings argument")

    return settings_argument
