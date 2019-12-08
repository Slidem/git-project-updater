from git_project_updater_cli.commands.command import Command
import uuid


class UnkownCommand(Command):

    def execute(self):
        pass

    @property
    def code(self):
        return str(uuid.uuid1())

    def __str__(self):
        return "Unkown command ! Please chose a valid command"
