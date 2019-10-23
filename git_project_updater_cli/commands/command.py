from abc import ABC, abstractmethod

from git_project_updater_business.settings.settings_repository import SettingsRepository
from git_project_updater_business.repository.projects_repository import ProjectsRepository
from git_project_updater_business.service.projects_service import ProjectsService
from git_project_updater_business.scanners.projects_scanner_factory import ProjectScannerFactory


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass

    def get_projects_service(self):
        projects_repository = ProjectsRepository.get_instance(SettingsRepository.get_instance(), ProjectScannerFactory.instance())
        return ProjectsService.get_instance(projects_repository)

    def __str__(self):
        "Unkown command"
