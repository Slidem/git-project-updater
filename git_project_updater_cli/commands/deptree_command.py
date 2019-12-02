from git_project_updater_cli.commands.command import Command
from git_project_updater_business.utils.node_dependency_tree_traversal import NodeTraversalObserver, TraversalStrategyType, TraversalSate


class LevelBasedPrinter(NodeTraversalObserver):
    tab_per_level = "   "

    def node_visited(self, traversal_state: TraversalSate):
        level = traversal_state.level
        tabs = LevelBasedPrinter.tab_per_level * level
        print(f"{tabs}{level} {traversal_state.node.project_id}")


class ProjectDependencyTreeCommand(Command):
    level_based_printer = LevelBasedPrinter()

    def execute(self):
        project_id = input("Enter project id:")

        self.projects_service.traverse_project_dependency_tree(
            project_id,
            TraversalStrategyType.DFS,
            ProjectDependencyTreeCommand.level_based_printer
        )

    @property
    def code(self):
        return "5"

    def __str__(self):
        return "=== Project dependency tree ==="
