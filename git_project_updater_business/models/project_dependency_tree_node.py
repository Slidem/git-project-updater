from typing import Dict, Any, TypeVar
from git_project_updater_business.models.version.version import ChildVersion


class ProjectDependencyTreeNode:

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.__children = {}
        self.__children_versions = {}

    def add_child(self, node: "ProjectDependencyTreeNode"):
        if not node:
            raise ValueError("Cannot add a null node as a child")
        self.__children[node.project_id] = node

    def set_child_version(self, child_id: str, version: ChildVersion):
        if child_id not in self.__children:
            raise ValueError(
                "Cannot set version. Child not found for the given node")

        self.__children_versions[child_id] = version

    def get_child_version(self, child_id) -> ChildVersion:
        if child_id not in self.__children_versions:
            return None

        return self.__children_versions[child_id]

    def get_child(self, project_id):
        return self.__children[project_id]

    @property
    def children(self):
        return list(self.__children.values())

    @property
    def children_ids(self):
        return list(self.__children.keys())
