from git_project_updater_cli.commands.command import Command


class ProjectVersionUsedInCommand(Command):
    def execute(self):
        project_id = input("Get project version for project id:")
        project_used_in_id = input("Used in project id:")

        child_version = self.projects_service.get_version_used(
            project_id, project_used_in_id)

        print(str(child_version))

    @property
    def code(self):
        return "7"

    def __str__(self):
        return "=== Project version used in project ==="
