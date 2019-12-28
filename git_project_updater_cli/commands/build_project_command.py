from git_project_updater_cli.commands.command import Command
from git_project_updater_business.utils.input_utils import exitable_input


class BuildProjectCommand(Command):

    BUILD_PROOJECT_COMMAND_CODE = "11"

    def execute(self):
        project_id = exitable_input("Project id:")
        self.projects_service.build_project(project_id)

    @property
    def code(self):
        return BuildProjectCommand.BUILD_PROOJECT_COMMAND_CODE

    def __str__(self):
        return "=== Build project ==="
