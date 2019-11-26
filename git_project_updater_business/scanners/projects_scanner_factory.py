from git_project_updater_business.settings.settings_repository import SettingsRepository
from git_project_updater_business.scanners.maven_scanner import MavenProjectsScanner


class ProjectScannerFactory:

    __instance = None

    @staticmethod
    def instance():
        if ProjectScannerFactory.__instance is None:
            ProjectScannerFactory()
        return ProjectScannerFactory.__instance

    def __init__(self):
        if ProjectScannerFactory.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ProjectScannerFactory.__instance = self

    @staticmethod
    def compute_scanner(settings):
        projects_type = settings.projects_type
        if projects_type == "maven":
            return MavenProjectsScanner()
        else:
            raise ValueError(
                f"No project scanners found for project_type {projects_type}")
