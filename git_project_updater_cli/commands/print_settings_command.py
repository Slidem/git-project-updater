from git_project_updater_cli.commands.command import Command
from git_project_updater_business.settings.settings_repository import SettingsRepository


class PrintCommand(Command):
    def execute(self):
        settings = super().settings_repository.get_settings()
        if settings:
            print(settings)
        else:
            print("Settings have not been set yet !")

    def code(self):
        return "2"

    def __str__(self):
        return "=== Settings ==="
