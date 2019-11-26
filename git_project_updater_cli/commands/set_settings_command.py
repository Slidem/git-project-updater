from git_project_updater_cli.commands.command import Command
from git_project_updater_business.settings.git_credentials import GitCredentials
from git_project_updater_business.settings.settings import Settings
from git_project_updater_business.validators.project_type_validator import is_valid_project_type
from git_project_updater_business.utils.input_utils import exitable_input


class SetSettingsCommand(Command):

    SET_SETTINGS_COMMAND_CODE = "1"

    def execute(self):

        setting_input_util = SettingsInputUtil()

        git_credentials = setting_input_util.git_credentials
        projects_type = setting_input_util.projects_type
        projects_root_directories = setting_input_util.projects_root

        super().settings_repository().set_settings(
            Settings(
                git_credentials,
                projects_root_directories,
                projects_type
            )
        )

    @property
    def code(self):
        return SetSettingsCommand.SET_SETTINGS_COMMAND_CODE

    def __str__(self):
        return "=== Set settings ==="


class SettingsInputUtil:
    """
    Utility class to get console input from the user regarind:
    - git credentials
    - projects type : maven / gradle / ....
    - projects root directory 
    """

    @property
    def git_credentials(self):
        print("Enter git credentials:")
        username = exitable_input("Username: ")
        password = exitable_input("Password: ")
        return GitCredentials(username, password)

    @property
    def projects_type(self):
        while True:
            project_type = exitable_input("Project type: ")
            if is_valid_project_type(project_type):
                return project_type

            print("Invalid project type. Try again!")

    @property
    def projects_root(self):
        while True:
            projects_root_directory = exitable_input(
                "Enter project root directory: ")

            if projects_root_directory:
                return projects_root_directory
            else:
                print("Project root directories cannot be empty")
