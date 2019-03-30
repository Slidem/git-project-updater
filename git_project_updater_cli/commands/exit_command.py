from git_project_updater_cli.commands.command import Command
import sys


class ExitCommand(Command):
    def execute(self):
        sys.exit()

    def __str__(self):
        return "Exiting..."
