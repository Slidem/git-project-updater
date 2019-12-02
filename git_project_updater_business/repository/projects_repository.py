import logging

from git_project_updater_business.settings.settings_repository import SettingsRepository
from git_project_updater_business.scanners.projects_scanner_factory import ProjectScannerFactory


class ProjectsRepository:
    __instance = None

    @staticmethod
    def get_instance(settings_repository: SettingsRepository, project_scanner_factory: ProjectScannerFactory):
        if ProjectsRepository.__instance is None:
            ProjectsRepository(settings_repository, project_scanner_factory)
        return ProjectsRepository.__instance

    def __init__(self, settings_repository, project_scanner_factory):
        """ Virtually private constructor. """
        if ProjectsRepository.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.settings_repository = settings_repository
            self.project_scanner_factory = project_scanner_factory
            self.__projects = None
            ProjectsRepository.__instance = self

    @property
    def projects(self):
        if not self.__projects:
            self.refresh_projects()
        return self.__projects

    def refresh_projects(self):
        self.__read_projects()

    # --------------------------------------------- PRIVATE METHODS

    def __read_projects(self):
        logging.info("Reading projects...")
        settings = self.settings_repository.settings
        if not settings:
            logging.error("No settings found in repository")
        else:
            self.__projects = self.project_scanner_factory.compute_scanner(
                settings).scan_for_projects(settings)
