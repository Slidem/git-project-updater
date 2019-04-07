from git_project_updater_business.settings.settings_repository import SettingsRepository
from git_project_updater_business.scanners.maven_scanner import MavenProjectsScanner
from git_project_updater_business.scanners.empty_project_scanner import EmptyProjectScanner


class ProjectScannerFactory:
    __instance = None

    @staticmethod
    def get_instance():
        if ProjectScannerFactory.__instance == None:
            ProjectScannerFactory()
        return ProjectScannerFactory.__instance

    def __init__(self):
        if ProjectScannerFactory.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ProjectScannerFactory.__instance = self

    def get_projects_scanner(self, settings):
        projects_type = settings.get_projects_type()
        if projects_type == "maven":
            return MavenProjectsScanner()
        else:
            return EmptyProjectScanner()
