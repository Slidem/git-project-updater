from git_project_updater_cli.commands.command import Command
from git_project_updater_business.settings.settings_repository import SettingsRepository
from git_project_updater_business.repository.projects_repository import ProjectsRepository
from git_project_updater_business.service.projects_service import ProjectsService
from git_project_updater_business.scanners.projects_scanner_factory import ProjectScannerFactory


class ListProjectsCommand(Command):
    def execute(self):
        project_ids = super().projects_service.get_top_level_projects_ids()
        print(*project_ids, sep="\n")

    def code(self):
        return "3"

    def __str__(self):
        return "=== Projects list ==="
