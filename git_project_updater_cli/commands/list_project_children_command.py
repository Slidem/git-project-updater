from git_project_updater_cli.commands.command import Command

class ListProjectChildrenIds(Command):
    def execute(self):
        project_id = input("Enter project id:")
        project_children_ids = self.get_projects_service().get_project_children(project_id)
        print(*project_children_ids, sep="\n")

    def __str__(self):
        return "=== Project children ids ==="
