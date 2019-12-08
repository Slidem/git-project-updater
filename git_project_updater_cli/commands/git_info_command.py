from git_project_updater_cli.commands.command import Command


class GitInfoCommand(Command):

    GIT_INFO_CODE = "8"

    def execute(self):
        project_id = input("Print git info for project id:")
        git_info = self.git_service.get_git_info(project_id)
        # TODO print it
        print(git_info)

    @property
    def code(self):
        return GitInfoCommand.GIT_INFO_CODE

    def __str__(self):
        return "=== Project git info ==="
