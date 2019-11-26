from git_project_updater_cli.commands.command import Command


class ListProjectChildrenIds(Command):
    LIST_CHILDREN_CODE_COMMAND = "4"

    def execute(self):
        project_id = input("Enter project id:")

        project_children_ids = super().projects_service.get_project_children(
            project_id)

        print(*project_children_ids, sep="\n")

    @property
    def code(self):
        return ListProjectChildrenIds.LIST_CHILDREN_CODE_COMMAND

    def __str__(self):
        return "=== Project children ids ==="
