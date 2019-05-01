from git_project_updater_business.utils.argument_utils import *


class Project:
    __project_id = None
    __project_type = None
    __path = None
    __details = None
    __children = []

    def __init__(self, project_id, project_parent_id, project_type, path, details, children, dependencies):
        self.__project_id = validate_string(project_id, "project_id")
        self.__project_parent_id = validate_string(
            project_parent_id, "project_parent_id")
        self.__project_type = validate_string(project_type, "project_type")
        self.__path = path = validate_path(path, "path")
        self.__details = validate_details(details, "details")
        self.__children = validate_and_get_new_list(
            children, Project, "children")
        self.__dependencies = validate_and_get_new_list(
            dependencies, Project, "children")

    def add_dependency(self, dependency):
        if not dependency or not isinstance(dependency, Project):
            raise ValueError("Invalid Project argument")

        if not self.__dependencies:
            self.__dependencies = []

        self.__dependencies.append(dependency)

    def add_child(self, child):
        if not child or not isinstance(child, Project):
            raise ValueError("Invalid Project argument")

        if not self.__children:
            self.__children = []

        self.__children.append(child)

    def get_children(self):
        return this.__children

    def get_project_id(self):
        return self.__project_id

    def get_details(self):
        return self.__details

    def __str__(self):
        project_str = "------------ Project -------------\n"
        project_str += "parent-id: " + self.__project_parent_id + "\n"
        project_str += "id: " + self.__project_id + "\n"
        project_str += "type: " + self.__project_type + "\n"
        project_str += "path: " + str(self.__path) + "\n"
        project_str += "children ids: " + \
            ", ".join(map(lambda p: p.__project_id, self.__children)) + "\n"
        project_str += "dependencies ids: " + \
            ", ".join(map(lambda p: p.__project_id,
                          self.__dependencies)) + "\n"
        project_str += "----------- Details --------------\n"
        project_str += str(self.__details)
        return project_str
