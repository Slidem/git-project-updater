from git_project_updater_business.models.maven.maven_project import MavenProject


class DependenciesVisitor:

    def __init__(self, projects_repository):
        self.projects_repository = projects_repository
        self.dependency_ids = []

    def visit(self, project):
        if not project:
            return

        if isinstance(project, MavenProject):
            self.__visit_maven(project)

    def __visit_maven(self, maven_project):
        if not maven_project:
            return

        repository_projects = self.projects_repository.get_projects()
        dependency_ids = set()

        self.add_dependencies(maven_project.maven_pom, repository_projects)
        modules = maven_project.maven_pom.modules
        if not modules:
            for m in modules:
                module_project = repository_projects.get(m, None)
                if module_project:
                    self.add_dependencies(
                        module_project.maven_pom, repository_projects)

        self.dependency_ids = list(dependency_ids)

    def add_dependencies(self, maven_pom, repository_projects):
        for artifact in maven_pom.dependencies:
            if artifact.artifact_id in repository_projects:
                dependency_ids.add(artifact.artifact_id)
