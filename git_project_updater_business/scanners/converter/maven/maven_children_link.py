from git_project_updater_business.scanners.converter.project_processor_link import ProjectProcessorLink


class MavenProjectChildrenLink(ProjectProcessorLink):

    def process(self, projects):

        if not projects:
            return projects

        for project_id, project in projects.items():
            self.__add_children(project)

        return projects

    def __add_children(self, project):

        maven_pom = project.maven_pom
        if not maven_pom:
            return

        project.children_ids = maven_pom.modules.copy()
