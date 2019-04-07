from git_project_updater_business.utils.argument_utils import *


class Project:
    __project_id = None
    __project_type = None
    __path = None
    __details = None
    __children = []

    def __init__(self, project_id, project_type, path, details, children):
        self.__project_id = validate_string(project_id, "project_id")
        self.__project_type = validate_string(project_type, "project_type")
        self.__path = path = validate_path(path, "path")
        self.__details = validate_details(details, "details")
        self.__children = validate_and_get_new_list(
            children, Project, "children")

    def get_details(self):
        return self.__details
