from git_project_updater_cli.commands.command import Command


class ProjectDependencyTreeCommand(Command):
    def execute(self):
        # todo
        raise NotImplementedError()

    def code(self):
        return "5"

    def __str__(self):
        return "=== Project dependency ids ==="
