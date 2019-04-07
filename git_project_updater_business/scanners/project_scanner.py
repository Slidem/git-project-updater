from abc import ABC, abstractmethod


class ProjectScanner(ABC):

    @abstractmethod
    def get_projects(self, settings):
        pass
