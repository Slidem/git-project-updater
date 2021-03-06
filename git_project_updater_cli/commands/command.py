from abc import ABC, abstractmethod

from git_project_updater_business.settings.settings_repository import SettingsRepository
from git_project_updater_business.repository.projects_repository import ProjectsRepository
from git_project_updater_business.service.projects_service import ProjectsService
from git_project_updater_business.service.git_service import GitService
from git_project_updater_business.scanners.projects_scanner_factory import ProjectScannerFactory
from git_project_updater_cli.commands import command_factory


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass

    @property
    @abstractmethod
    def code(self):
        pass

    @property
    def settings_repository(self):
        return SettingsRepository.instance()

    @property
    def projects_repository(self):
        return ProjectsRepository.instance(self.settings_repository, ProjectScannerFactory.instance())

    @property
    def projects_service(self):
        return ProjectsService.instance(self.projects_repository)

    @property
    def git_service(self):
        return GitService.get_instance(self.projects_repository)

    def __str__(self):
        "Unkown command"
