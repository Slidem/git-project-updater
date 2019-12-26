from git_project_updater_cli.commands.command import Command


class ProjectVersionCommand(Command):
    def execute(self):
        project_id = input("Get project version for project id:")
        print(self.projects_service.get_project_version(project_id))

    @property
    def code(self):
        return "6"

    def __str__(self):
        return "=== Project version ==="


