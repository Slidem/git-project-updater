from git_project_updater_cli.commands.command import Command
from git_project_updater_business.models.git.git_model import git_info_to_str


class GitInfoCommand(Command):

    GIT_INFO_CODE = "9"

    def execute(self):
        project_id = input("Print git info for project id:")
        print(git_info_to_str(self.git_service.get_git_info(project_id)))

    @property
    def code(self):
        return GitInfoCommand.GIT_INFO_CODE

    def __str__(self):
        return "=== Project git info ==="
