from typing import Dict, Any, TypeVar


class ProjectDependencyTreeNode:

    def __init__(self, project_id: str, children: Dict[str, "ProjectDependencyTreeNode"]):
        self.project_id = project_id
        self.__children = children if children else {}

    def add_child(self, node: "ProjectDependencyTreeNode"):
        if not node:
            raise ValueError("Cannot add a null node as a child")
        self.__children[node.project_id] = node

    def get_child(self, project_id):
        return self.__children[project_id]

    @property
    def children(self):
        return list(self.__children.values())

    @property
    def children_ids(self):
        return list(self.__children.keys())
