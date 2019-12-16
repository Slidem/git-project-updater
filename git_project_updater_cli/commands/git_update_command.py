from git_project_updater_cli.commands.command import Command
from git_project_updater_business.service.git_service import GitProcessObserver


class GitUpdateCommandProcessObserver(GitProcessObserver):

    # Overriden methods ---------------------------
    def fetching(self):
        print("Fetching git sources ...")

    def fetching_finished(self):
        print("Fetching of git sources finished.")

    def up_to_date(self):
        print("Project alreay up to date")

    def performed_fast_forward(self):
        print("Updating sources by fast forwarding")

    def could_not_update_current_branch(self, current_branch_name):
        print(
            f"Could not update current branch {current_branch_name}. \nWorking directory not clean.. Try stashing your unsaved changes and try again...")


class GitUpdateCommand(Command):

    GIT_INFO_CODE = "9"
    UPDATE_PROCESS_OBSERVER = GitUpdateCommandProcessObserver()

    def execute(self):
        project_id = input("Update git sources for project id:")
        self.git_service.update_git_sources(
            project_id, GitUpdateCommand.UPDATE_PROCESS_OBSERVER)

    @property
    def code(self):
        return GitUpdateCommand.GIT_INFO_CODE

    def __str__(self):
        return "=== Project git update ==="
