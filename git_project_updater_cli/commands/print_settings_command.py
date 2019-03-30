from git_project_updater_cli.commands.command import Command
from git_project_updater_business.settings.settings_repository import get_settings


class PrintCommand(Command):
    def execute(self):
        settings = get_settings()
        if settings:
            print(settings)
        else:
            print("Settings have not been set yet !")

    def __str__(self):
        return "=== Settings ==="
