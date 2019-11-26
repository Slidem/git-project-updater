from git_project_updater_cli.commands.command import Command
import sys


class ExitCommand(Command):

    EXIT_CODE = "0"

    def execute(self):
        sys.exit()

    @property
    def code(self):
        return ExitCommand.EXIT_CODE

    def __str__(self):
        return "Exiting..."
