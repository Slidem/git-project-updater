from git_project_updater_cli.commands.command import Command
from git_project_updater_business.settings.git_credentials import GitCredentials
from git_project_updater_business.settings.settings_repository import set_settings
from git_project_updater_business.settings.settings import Settings
from git_project_updater_business.validators.project_type_validaor import is_valid_project_type
from git_project_updater_business.utils.input_utils import exitable_input


class SetSettingsCommand(Command):
    def execute(self):
        git_credentials = self.__get_git_credentials()
        projects_type = self.__get_projects_type()
        projects_root_directories = self.__get_projects_root_directories()

        set_settings(
            Settings(
                git_credentials,
                projects_root_directories,
                projects_type
            )
        )

    def __str__(self):
        return "=== Set settings ==="

    def __get_git_credentials(self):
        print("Enter git credentials:")
        username = input("Username: ")
        password = input("Password: ")
        return GitCredentials(username, password)

    def __get_projects_type(self):
        while True:
            project_type = input("Project type: ")
            if is_valid_project_type(project_type):
                return project_type

            print("Invalid project type. Try again!")

    def __get_projects_root_directories(self):
        while True:
            project_root_directories = input(
                "Enter project root directores, comma separated: ")

            if project_root_directories:
                return project_root_directories
            else:
                print("Project root directories cannot be empty")
