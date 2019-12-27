from git_project_updater_business.repository.projects_repository import ProjectsRepository
from git_project_updater_business.utils.node_dependency_tree_traversal import createDependencyTreeNodeTraversalStrategy
from git_project_updater_business.builders.builders_factory import get_builder


class ProjectsService:
    __instance = None

    @staticmethod
    def get_instance(projects_repository):
        if ProjectsService.__instance is None:
            ProjectsService(projects_repository)
        return ProjectsService.__instance

    def __init__(self, projects_repository):
        if self.__instance is None:
            self.projects_repository = projects_repository
            ProjectsService.__instance = self
        else:
            raise Exception("This class is a singleton")

    def get_project_ids(self):
        if not self.projects_repository.projects:
            return []
        return list(self.projects_repository.projects)

    def get_top_level_projects_ids(self):
        """ Returns top level project ids, meaning that projects which belong to a parent will not be shown"""
        projects = self.projects_repository.projects

        if not projects:
            return []

        return [p.project_id for p in projects.values() if p.project_parent_id not in projects]

    def get_project_children(self, project_id):
        projects = self.projects_repository.projects
        project = projects.get(project_id, None)
        return project.children_ids if project else []

    def get_project_details(self, project_id):
        project = self.projects_repository.projects.get(project_id, None)
        if not project:
            return "No details found"
        return str(project)

    def traverse_project_dependency_tree(self, project_id, traversal_type, node_traversal_observer):
        traversal_strategy = createDependencyTreeNodeTraversalStrategy(
            traversal_type,
            node_traversal_observer
        )

        project = self.projects_repository.projects[project_id]
        traversal_strategy.traverse(project.dependency_tree)

    def get_project_version(self, project_id):
        project = self.projects_repository.projects.get(project_id, None)
        return project.version if project else "UNKOWN"

    def get_version_used(self, project_id, project_used_in_id):
        projects = self.projects_repository.projects
        project_used_in = projects.get(project_used_in_id, None)

        if not project_used_in:
            return "UNKOWN"

        version_used = project_used_in.dependency_tree.get_child_version(
            project_id)

        return version_used if version_used else "UNKOWN"

    def build_project(self, project_id, *mnv_commands):
        projects = self.projects_repository.projects
        project = projects.get(project_id, None)
        get_builder(project).build(project, mnv_commands)

    # TODO
    def change_version(self, project_id, for_project_id, version):
        pass
