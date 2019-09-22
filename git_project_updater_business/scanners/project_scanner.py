from abc import ABC, abstractmethod


class ProjectScanner(ABC):

    @abstractmethod
    def scan_for_projects(self, settings):
        pass
