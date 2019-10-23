from git_project_updater_business.repository.projects_repository import ProjectsRepository
from git_project_updater_business.visitors.project_children_visitor import ChildrenVisitor
from git_project_updater_business.visitors.project_dependencies_visitor import DependenciesVisitor


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

        return map(lambda p: p.project_id,
                   filter(lambda p: p.project_parent_id not in projects, projects.values())) if projects else []

    def get_project_dependencies(self, project_id):
        project = self.projects_repository.projects.get(project_id, None)
        if not project:
            return []

        dependency_visitor = DependenciesVisitor(self.projects_repository)
        project.accept(dependency_visitor)
        return dependency_visitor.dependency_ids.copy()

    def get_project_children(self, project_id):
        projects = self.projects_repository.projects
        project = projects.get(project_id, None)
        return project.children_ids if project else []

    def get_project_details(self, project_id):
        project = self.projects_repository.projects.get(project_id, None)
        if not project:
            return "No details found"
        return str(project)

    def get_project_version(self, project_id):
        pass

    def get_version_used(self, project_id, project_used_in_id):
        pass

    def change_version(self, project_id, for_project_id, version):
        pass
