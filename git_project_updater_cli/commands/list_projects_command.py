from git_project_updater_cli.commands.command import Command


class ListProjectsCommand(Command):
    LIST_PROJECTS_COMMAND = "3"

    def execute(self):
        project_ids = super().projects_service.get_top_level_projects_ids()
        print(*project_ids, sep="\n")

    @property
    def code(self):
        return ListProjectsCommand.LIST_PROJECTS_COMMAND

    def __str__(self):
        return "=== Projects list ==="
