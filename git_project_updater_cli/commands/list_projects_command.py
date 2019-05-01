from git_project_updater_cli.commands.command import Command
from git_project_updater_business.settings.settings_repository import SettingsRepository
from git_project_updater_business.repository.projects_repository import ProjectsRepository
from git_project_updater_business.scanners.projects_scanner_factory import ProjectScannerFactory


class ListProjectsCommand(Command):
    def execute(self):
        settings = SettingsRepository.get_instance().get_settings()
        projects = ProjectsRepository.get_instance().get_projects(
            settings, ProjectScannerFactory.get_instance())

        for p in projects:
            print()
            print(p.get_project_id(), "\n")

    def __str__(self):
        return "=== Projects list ==="
