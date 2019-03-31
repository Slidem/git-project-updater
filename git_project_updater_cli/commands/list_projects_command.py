from git_project_updater_cli.commands.command import Command


class ListProjectsCommand(Command):
    def execute(self):
        pass

    def __str__(self):
        return "=== Projects list ==="
