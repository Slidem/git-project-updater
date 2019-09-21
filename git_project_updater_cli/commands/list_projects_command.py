from git_project_updater_cli.commands.command import Command
from git_project_updater_business.settings.settings_repository import SettingsRepository
from git_project_updater_business.repository.projects_repository import ProjectsRepository
from git_project_updater_business.service.projects_service import ProjectsService
from git_project_updater_business.scanners.projects_scanner_factory import ProjectScannerFactory


class ListProjectsCommand(Command):
    def execute(self):
        settings_repository = SettingsRepository.get_instance()

        if not settings_repository.get_settings():
            print("No projects available! No settings set")
            return

        projects_scanner_factory = ProjectScannerFactory.get_instance()
        projects_repository = ProjectsRepository.get_instance(
            settings_repository, projects_scanner_factory)
        projects_service = ProjectsService.get_instance(projects_repository)

        project_ids = projects_service.get_top_level_projects_ids()
        print(*project_ids, sep="\n")

    def __str__(self):
        return "=== Projects list ==="
