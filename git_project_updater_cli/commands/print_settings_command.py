from git_project_updater_cli.commands.command import Command
from git_project_updater_business.settings.settings_repository import SettingsRepository


class PrintSettingsCommand(Command):

    PRINT_SETTINGS_COMMAND_CODE = "2"

    def execute(self):
        settings = super().settings_repository.settings
        if settings:
            print(settings)
        else:
            print("Settings have not been set yet !")

    @property
    def code(self):
        return PrintSettingsCommand.PRINT_SETTINGS_COMMAND_CODE

    def __str__(self):
        return "=== Settings ==="
