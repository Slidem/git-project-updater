from git_project_updater_business.models.maven.maven_project import MavenProject


class ChildrenVisitor:

    def __init__(self, projects_repository):
        self.projects_repository = projects_repository
        self.children_ids = []

    def visit(self, project):
        if not project:
            return

        if isinstance(project, MavenProject):
            self.__visit_maven(project)

    def __visit_maven(self, maven_project):
        modules = maven_project.maven_pom.modules
        if not modules:
            return

        self.children_ids = modules.copy()
