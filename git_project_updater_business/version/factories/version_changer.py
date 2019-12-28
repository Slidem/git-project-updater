from git_project_updater_business.version.models.version import ChildVersion, ChildVersionType
from abc import ABC, abstractmethod


class VersionChanger(ABC):

    def __init__(self, project):
        self.project = project

    @abstractmethod
    def change_in(self, project_to_change_in, with_version):
        pass
