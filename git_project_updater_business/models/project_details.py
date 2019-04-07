from abc import ABC, abstractmethod


class ProjectDetails(ABC):

    def accept(self, details_visitor):
        details_visitor.visit(self)

    @abstractmethod
    def _get_details_string(self):
        pass

    def __str__(self):
        return self._get_details_string()
