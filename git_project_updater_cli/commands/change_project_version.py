from git_project_updater_cli.commands.command import Command


class ChangeProjectVersionCommand(Command):

    CHANGE_PROJECT_VERSION_CODE = "8"

    def execute(self):
        project_id = input("Update version for project id: ")
        change_in = input("Used in project id: ")
        new_version = input("Set to new version: ")
        self.projects_service.change_version(
            change_in, project_id, new_version)

    @property
    def code(self):
        return ChangeProjectVersionCommand.CHANGE_PROJECT_VERSION_CODE

    def __str__(self):
        return "=== Change project version ==="
