from abc import *


class Project(ABC):

    def __init__(self, **kwargs):
        self.project_id = kwargs["project_id"]
        self.project_type = kwargs["project_type"]
        self.path = kwargs["path"]
        self.version = "UNKOWN"

        # optional fields
        self.project_parent_id = kwargs.get("project_parent_id", None)
        self.children_ids = kwargs.get("children_ids", None)
        self.dependency_tree = kwargs.get("depdency_tree", None)

    def accept(self, visitor):
        if not visitor:
            raise ValueError("Cannot accept an empty visitor")

        visitor.visit(self)

    @abstractmethod
    def _get_details_str(self):
        pass

    def __str__(self):
        project_str = "------------ Project -------------\n"
        project_str += "parent-id: " + self.project_parent_id + "\n"
        project_str += "id: " + self.project_id + "\n"
        project_str += "type: " + self.project_type + "\n"
        project_str += "path: " + str(self.path) + "\n"
        project_str += "----------- Details --------------\n"
        project_str += str(self._get_details_str)
        return project_str
